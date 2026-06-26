"""
================================================================================
 app/services/usuario_service.py — SERVICIO DE USUARIOS
--------------------------------------------------------------------------------
 Capa: Lógica de negocio
--------------------------------------------------------------------------------
 Responsabilidad:
   Operaciones de gestión de usuarios distintas a la autenticación:
     - listar clientes (para el superadmin)
     - cambiar rol de un usuario (ascender cliente a admin, o degradar)

 Reglas de negocio importantes:
   - NUNCA se puede asignar el rol Superadmin (id_rol = 1) desde la API,
     aunque el solicitante sea el propio superadmin. Esto evita que un
     descuido cree un segundo "dueño".
   - Sólo el superadmin puede cambiar roles.
================================================================================
"""

from typing import List

from app.models.usuario import (
    Usuario,
    ROL_CLIENTE,
    ROL_ADMIN,
    ROL_SUPERADMIN,
)
from app.repositories.usuario_repository import UsuarioRepository
from app.errors.exceptions import (
    AccesoDenegadoError,
    DatosInvalidosError,
    RecursoNoEncontradoError,
)


# Roles que SÍ se pueden asignar vía API (Superadmin nunca).
ROLES_ASIGNABLES = {ROL_CLIENTE, ROL_ADMIN}


class UsuarioService:

    @staticmethod
    def listar_clientes() -> List[dict]:
        """Devuelve clientes (rol = 2) sin exponer la contraseña."""
        clientes = UsuarioRepository.listar_por_rol(ROL_CLIENTE)
        return [c.to_dict() for c in clientes]

    @staticmethod
    def listar_moderadores() -> List[dict]:
        """Devuelve moderadores (rol = 3)."""
        mods = UsuarioRepository.listar_por_rol(ROL_ADMIN)
        return [m.to_dict() for m in mods]

    @staticmethod
    def cambiar_rol(id_usuario: int, nuevo_rol: int) -> Usuario:
        """
        Cambia el rol de un usuario. Reglas:
          - nuevo_rol debe ser 2 (cliente) o 3 (admin). 1 está prohibido.
          - el usuario destino debe existir.
          - no se puede cambiar el rol del propio superadmin.
        """
        if nuevo_rol not in ROLES_ASIGNABLES:
            raise DatosInvalidosError(
                "Solo se puede asignar 'cliente' (2) o 'admin' (3). "
                "El rol superadmin no es asignable."
            )

        objetivo = UsuarioRepository.obtener_por_id(id_usuario)
        if objetivo is None:
            raise RecursoNoEncontradoError("Usuario no encontrado")

        if objetivo.id_rol == ROL_SUPERADMIN:
            raise AccesoDenegadoError(
                "No se puede modificar el rol del Superadmin"
            )

        UsuarioRepository.cambiar_rol(id_usuario, nuevo_rol)
        objetivo.id_rol = nuevo_rol
        return objetivo