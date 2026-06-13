"""
================================================================================
 app/models/usuario.py — ENTIDAD USUARIO
--------------------------------------------------------------------------------
 Capa: Dominio (Model en MVC)
--------------------------------------------------------------------------------
 Representa un usuario del sistema en cualquiera de sus tres roles:
   1 = Administrador (Superadmin)   — la propietaria.
   2 = Cliente                      — visitantes registrados.
   3 = Moderador (Admin/Empleados)  — empleados de la tienda.

 NOTA importante (deuda funcional documentada):
   En el esquema actual la tabla `roles` define:
     id_rol = 1 → "Administrador"  (en el código actúa como SUPERADMIN)
     id_rol = 2 → "Cliente"
     id_rol = 3 → "Moderador"      (en el código actúa como ADMIN)
   Mantenemos esta semántica para no romper datos existentes, pero los
   nombres "lógicos" del sistema son: superadmin / cliente / admin.
================================================================================
"""

from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Optional


# Mapeo entre ID en la BD y nombre lógico del rol en el sistema.
ROL_SUPERADMIN = 1
ROL_CLIENTE = 2
ROL_ADMIN = 3

NOMBRES_ROL = {
    ROL_SUPERADMIN: "superadmin",
    ROL_CLIENTE: "cliente",
    ROL_ADMIN: "admin",
}


@dataclass
class Usuario:
    """
    Entidad Usuario.
    Usamos @dataclass para autogenerar __init__, __repr__ y __eq__.
    """
    id_usuario: Optional[int] = None
    nombre: str = ""
    apellido: str = ""
    correo: str = ""
    password: str = ""               # SIEMPRE almacenado hasheado (bcrypt)
    telefono: str = ""
    id_rol: int = ROL_CLIENTE
    fecha_registro: Optional[datetime] = None
    estado: int = 1                  # 1 = activo, 0 = inactivo

    @property
    def rol_nombre(self) -> str:
        """Devuelve el nombre lógico del rol (cliente, admin, superadmin)."""
        return NOMBRES_ROL.get(self.id_rol, "desconocido")

    def to_dict(self, incluir_password: bool = False) -> dict:
        """
        Serializa la entidad para enviarla al frontend.
        Por defecto NUNCA expone la contraseña (aunque esté hasheada).
        """
        data = asdict(self)
        if not incluir_password:
            data.pop("password", None)
        # datetime no es serializable JSON nativamente
        if isinstance(data.get("fecha_registro"), datetime):
            data["fecha_registro"] = data["fecha_registro"].isoformat()
        return data

    @classmethod
    def from_row(cls, row: dict) -> "Usuario":
        """Construye un Usuario a partir de una fila de MySQL (dict)."""
        if row is None:
            return None
        return cls(
            id_usuario=row.get("id_usuario"),
            nombre=row.get("nombre", ""),
            apellido=row.get("apellido", ""),
            correo=row.get("correo", ""),
            password=row.get("password", ""),
            telefono=row.get("telefono", ""),
            id_rol=row.get("id_rol", ROL_CLIENTE),
            fecha_registro=row.get("fecha_registro"),
            estado=row.get("estado", 1),
        )
