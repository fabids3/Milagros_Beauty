"""
================================================================================
 app/repositories/usuario_repository.py — REPOSITORIO DE USUARIOS
--------------------------------------------------------------------------------
 Capa: Acceso a datos
 Patrón aplicado: Repository (Eric Evans — Domain-Driven Design)
--------------------------------------------------------------------------------
 Responsabilidad:
   ÚNICA fuente de SQL relacionado a la tabla `usuarios`. Nadie más en el
   sistema debe escribir SELECT/INSERT/UPDATE/DELETE sobre esta tabla.

 Justificación didáctica:
   Si mañana cambiamos de MySQL a PostgreSQL o decidimos usar un ORM como
   SQLAlchemy, SOLO este archivo se modifica. Los servicios y rutas no se
   enteran.
================================================================================
"""

from typing import List, Optional

from app.database import db_cursor
from app.models.usuario import Usuario


class UsuarioRepository:
    """Operaciones de persistencia para la entidad Usuario."""

    # --- Consultas ---------------------------------------------------------

    @staticmethod
    def obtener_por_id(id_usuario: int) -> Optional[Usuario]:
        with db_cursor() as cursor:
            cursor.execute(
                "SELECT * FROM usuarios WHERE id_usuario = %s",
                (id_usuario,),
            )
            return Usuario.from_row(cursor.fetchone())

    @staticmethod
    def obtener_por_correo(correo: str) -> Optional[Usuario]:
        with db_cursor() as cursor:
            cursor.execute(
                "SELECT * FROM usuarios WHERE correo = %s",
                (correo,),
            )
            return Usuario.from_row(cursor.fetchone())

    @staticmethod
    def existe_correo(correo: str) -> bool:
        with db_cursor() as cursor:
            cursor.execute(
                "SELECT 1 FROM usuarios WHERE correo = %s LIMIT 1",
                (correo,),
            )
            return cursor.fetchone() is not None

    @staticmethod
    def listar_por_rol(id_rol: int) -> List[Usuario]:
        """Devuelve usuarios filtrados por rol (clientes, moderadores, etc.)."""
        with db_cursor() as cursor:
            cursor.execute(
                """
                SELECT id_usuario, nombre, apellido, correo, telefono,
                       id_rol, fecha_registro, estado
                FROM usuarios
                WHERE id_rol = %s AND estado = 1
                ORDER BY fecha_registro DESC
                """,
                (id_rol,),
            )
            return [Usuario.from_row(r) for r in cursor.fetchall()]

    @staticmethod
    def listar_todos() -> List[Usuario]:
        with db_cursor() as cursor:
            cursor.execute(
                """
                SELECT id_usuario, nombre, apellido, correo, telefono,
                       id_rol, fecha_registro, estado
                FROM usuarios
                ORDER BY fecha_registro DESC
                """
            )
            return [Usuario.from_row(r) for r in cursor.fetchall()]

    # --- Mutaciones --------------------------------------------------------

    @staticmethod
    def crear(usuario: Usuario) -> int:
        """
        Inserta un usuario nuevo. Devuelve el ID generado.
        IMPORTANTE: usuario.password debe llegar YA HASHEADO con bcrypt.
        """
        with db_cursor(commit=True) as cursor:
            cursor.execute(
                """
                INSERT INTO usuarios
                    (nombre, apellido, telefono, correo, password, id_rol)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    usuario.nombre,
                    usuario.apellido,
                    usuario.telefono,
                    usuario.correo,
                    usuario.password,
                    usuario.id_rol,
                ),
            )
            return cursor.lastrowid

    @staticmethod
    def cambiar_rol(id_usuario: int, nuevo_rol: int) -> bool:
        """
        Cambia el rol de un usuario.
        Regla de negocio (validada en el service): NUNCA se debe poder asignar
        el rol 1 (Superadmin) desde aquí. Esa restricción vive en el servicio.
        """
        with db_cursor(commit=True) as cursor:
            cursor.execute(
                "UPDATE usuarios SET id_rol = %s WHERE id_usuario = %s",
                (nuevo_rol, id_usuario),
            )
            return cursor.rowcount > 0
