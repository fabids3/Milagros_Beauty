"""
================================================================================
 app/models/producto.py — ENTIDAD PRODUCTO
--------------------------------------------------------------------------------
 Capa: Dominio (Model en MVC)
================================================================================
"""

from dataclasses import dataclass, asdict
from datetime import datetime
from decimal import Decimal
from typing import Optional


@dataclass
class Producto:
    """Entidad Producto del catálogo."""
    id_producto: Optional[int] = None
    nombre: str = ""
    descripcion: str = ""
    contenido: str = ""
    precio: Decimal = Decimal("0.00")
    imagen: str = ""
    id_categoria: Optional[int] = None
    id_marca: Optional[int] = None
    stock: int = 0
    estado: int = 1                  # 1 = visible, 0 = oculto
    ideal_para: str = ""
    beneficios: str = ""
    ingredientes: str = ""
    modo_uso: str = ""
    fecha_creacion: Optional[datetime] = None

    def to_dict(self) -> dict:
        """Serializa el producto a un dict listo para JSON."""
        data = asdict(self)
        # Decimal y datetime no son serializables directamente
        if isinstance(data.get("precio"), Decimal):
            data["precio"] = float(data["precio"])
        if isinstance(data.get("fecha_creacion"), datetime):
            data["fecha_creacion"] = data["fecha_creacion"].isoformat()
        return data

    @classmethod
    def from_row(cls, row: dict) -> "Producto":
        if row is None:
            return None
        return cls(**{k: row.get(k) for k in cls.__dataclass_fields__})