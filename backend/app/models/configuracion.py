"""
================================================================================
 app/models/configuracion.py — ENTIDAD CONFIGURACION
--------------------------------------------------------------------------------
 Capa: Dominio (Model en MVC)
--------------------------------------------------------------------------------
 Representa la configuración general de la tienda (singleton: una sola fila
 con id = 1). Almacena título, "Sobre nosotros", misión, visión y ubicación,
 además de la información de contacto dinámico.
================================================================================
"""

from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class Configuracion:
    id: int = 1
    titulo: Optional[str] = "Milagro's Beauty"
    sobre_nosotros: Optional[str] = ""
    mision: Optional[str] = ""
    vision: Optional[str] = ""
    ubicacion: Optional[str] = ""
    
    # --- NUEVOS CAMPOS AGREGADOS ---
    whatsapp: Optional[str] = "573246454318"
    correo_contacto: Optional[str] = "soporte@milagrosbeauty.com"
    instagram: Optional[str] = "https://instagram.com/tu_usuario"

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_row(cls, row: dict) -> "Configuracion":
        if row is None:
            return cls()
        return cls(**{k: row.get(k) for k in cls.__dataclass_fields__ if k in row}) 