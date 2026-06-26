"""
================================================================================
 app/services/auth_service.py — SERVICIO DE AUTENTICACIÓN
--------------------------------------------------------------------------------
 Capa: Lógica de negocio
 Patrón aplicado: Service Layer (Martin Fowler)
--------------------------------------------------------------------------------
 Responsabilidad:
   Centralizar todo lo relacionado con identidad del usuario:
     - registro (con hashing bcrypt)
     - login (con verificación de hash)
     - sesión (creación / destrucción / lectura)
     - migración de contraseñas planas legadas

 SEGURIDAD — DECISIONES CLAVE (para sustentación):
   1) HASHING: usamos bcrypt vía Flask-Bcrypt. Una contraseña como "Abc123!@"
      se transforma en "$2b$12$...". Es unidireccional: no se puede revertir.
      Bcrypt incluye SAL automática: dos usuarios con la misma password
      producen hashes distintos. Resistente a rainbow tables.

   2) RETROCOMPATIBILIDAD: la BD tiene tres tipos de contraseñas legadas:
        a) Plano (ej: "123")          → migrar en el primer login exitoso.
        b) bcrypt de PHP ($2y$10$...) → bcrypt de Python las acepta como $2b$.
        c) bcrypt de Python ($2b$12$..) → uso normal.
      Implementamos detección automática para que ningún usuario quede fuera.

   3) SESIONES firmadas: flask.session usa SECRET_KEY para firmar la cookie.
      El cliente NO puede modificar id_usuario ni rol sin invalidar la firma.
================================================================================
"""

from typing import Optional

from flask import session

from app.extensions import bcrypt
from app.models.usuario import Usuario, ROL_CLIENTE, ROL_ADMIN, ROL_SUPERADMIN
from app.repositories.usuario_repository import UsuarioRepository
from app.errors.exceptions import (
    CorreoDuplicadoError,
    CredencialesInvalidasError,
    NoAutenticadoError,
)
from app.utils.validators import (
    validar_correo,
    validar_password,
    requerir_campos,
)


class AuthService:

    # -----------------------------------------------------------------
    # REGISTRO
    # -----------------------------------------------------------------
    @staticmethod
    def registrar_cliente(data: dict) -> Usuario:
        """
        Registro público de un nuevo cliente.
        Fuerza siempre id_rol = 2 (Cliente). NUNCA confiar en lo que envíe
        el navegador: aunque el usuario mande {"id_rol": 1}, lo ignoramos.
        """
        return AuthService._registrar(data, id_rol=ROL_CLIENTE)

    @staticmethod
    def registrar_moderador(data: dict) -> Usuario:
        """Registro de moderador (admin de tienda). Solo lo invoca el superadmin."""
        return AuthService._registrar(data, id_rol=ROL_ADMIN)

    @staticmethod
    def _registrar(data: dict, id_rol: int) -> Usuario:
        """Lógica común de registro. Privada (prefijo _)."""
        # 1) Validaciones de entrada
        requerir_campos(data, ["nombre", "apellido", "telefono",
                               "correo", "password"])
        correo = validar_correo(data["correo"])
        validar_password(data["password"])

        # 2) Verificar unicidad del correo
        if UsuarioRepository.existe_correo(correo):
            raise CorreoDuplicadoError()

        # 3) Hashear la contraseña con bcrypt antes de tocar la BD
        password_hash = bcrypt.generate_password_hash(
            data["password"]
        ).decode("utf-8")

        # 4) Construir entidad y persistir
        usuario = Usuario(
            nombre=data["nombre"].strip(),
            apellido=data["apellido"].strip(),
            telefono=data["telefono"].strip(),
            correo=correo,
            password=password_hash,
            id_rol=id_rol,
        )
        usuario.id_usuario = UsuarioRepository.crear(usuario)
        return usuario

    # -----------------------------------------------------------------
    # LOGIN
    # -----------------------------------------------------------------
    @staticmethod
    def login(correo: str, password: str) -> Usuario:
        """
        Valida credenciales y, si todo está bien, abre la sesión.

        Reglas:
          - Si el password almacenado parece bcrypt ($2a$, $2b$, $2y$),
            se verifica con bcrypt.check_password_hash.
          - Si es texto plano (legado), se compara directo y se migra
            automáticamente a bcrypt en el mismo request.
        """
        requerir_campos({"correo": correo, "password": password},
                        ["correo", "password"])
        correo = validar_correo(correo)

        usuario = UsuarioRepository.obtener_por_correo(correo)
        if usuario is None:
            raise CredencialesInvalidasError()

        password_ok = AuthService._verificar_password(
            password_plano=password,
            password_almacenado=usuario.password,
            id_usuario=usuario.id_usuario,
        )
        if not password_ok:
            raise CredencialesInvalidasError()

        # Abrir sesión firmada
        AuthService._abrir_sesion(usuario)
        return usuario

    @staticmethod
    def _verificar_password(password_plano: str,
                            password_almacenado: str,
                            id_usuario: int) -> bool:
        """Verifica contraseñas en cualquier formato legado o moderno."""
        if not password_almacenado:
            return False

        # Caso 1: hash bcrypt (puede ser $2a$, $2b$ o $2y$ de PHP)
        if password_almacenado.startswith(("$2a$", "$2b$", "$2y$")):
            # Normalizamos $2y$ → $2b$ para que Python lo acepte
            hash_compatible = password_almacenado.replace("$2y$", "$2b$", 1)
            try:
                return bcrypt.check_password_hash(hash_compatible, password_plano)
            except (ValueError, TypeError):
                return False

        # Caso 2: texto plano legado → migramos al hash bcrypt al instante
        if password_plano == password_almacenado:
            AuthService._migrar_password_a_bcrypt(id_usuario, password_plano)
            return True

        return False

    @staticmethod
    def _migrar_password_a_bcrypt(id_usuario: int, password_plano: str) -> None:
        """
        Reemplaza la contraseña plana por su versión bcrypt.
        Se ejecuta de forma transparente en el primer login exitoso.
        """
        from app.database import db_cursor
        nuevo_hash = bcrypt.generate_password_hash(
            password_plano
        ).decode("utf-8")
        with db_cursor(commit=True) as cursor:
            cursor.execute(
                "UPDATE usuarios SET password = %s WHERE id_usuario = %s",
                (nuevo_hash, id_usuario),
            )

    # -----------------------------------------------------------------
    # SESIÓN
    # -----------------------------------------------------------------
    @staticmethod
    def _abrir_sesion(usuario: Usuario) -> None:
        """Guarda los datos esenciales en la sesión firmada de Flask."""
        session.clear()
        session["id_usuario"] = usuario.id_usuario
        session["nombre"] = usuario.nombre
        session["apellido"] = usuario.apellido
        session["correo"] = usuario.correo
        session["telefono"] = usuario.telefono
        session["id_rol"] = usuario.id_rol
        session["rol"] = usuario.rol_nombre
        session.permanent = True

    @staticmethod
    def cerrar_sesion() -> None:
        """Logout: limpia toda la sesión."""
        session.clear()

    @staticmethod
    def usuario_actual() -> Optional[dict]:
        """Devuelve el dict de la sesión, o None si no hay sesión."""
        if "id_usuario" not in session:
            return None
        return dict(session)

    @staticmethod
    def requerir_autenticacion() -> dict:
        """Igual que usuario_actual() pero lanza excepción si no hay sesión."""
        actual = AuthService.usuario_actual()
        if actual is None:
            raise NoAutenticadoError()
        return actual