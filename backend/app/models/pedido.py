"""
================================================================================
 app/models/pedido.py — ENTIDADES PEDIDO Y PEDIDO_DETALLE
--------------------------------------------------------------------------------
 Capa: Dominio (Model en MVC)
================================================================================
"""

from dataclasses import dataclass, field, asdict
from datetime import datetime
from decimal import Decimal
from typing import List, Optional


@dataclass
class PedidoDetalle:
    """Línea individual de un pedido (un producto, una cantidad, un precio)."""
    id_detalle: Optional[int] = None
    id_pedido: Optional[int] = None
    id_producto: Optional[int] = None
    cantidad: int = 1
    precio_unitario: Decimal = Decimal("0.00")
    subtotal: Decimal = Decimal("0.00")

    def to_dict(self) -> dict:
        data = asdict(self)
        for k in ("precio_unitario", "subtotal"):
            if isinstance(data.get(k), Decimal):
                data[k] = float(data[k])
        return data

    @classmethod
    def from_row(cls, row: dict) -> "PedidoDetalle":
        if not row: return None
        return cls(**{k: row.get(k) for k in cls.__dataclass_fields__ if k in row})


@dataclass
class Pedido:
    """Pedido completo: cabecera + lista de líneas (detalle)."""
    id_pedido: Optional[int] = None
    id_usuario: Optional[int] = None
    id_estado: int = 1               # 1=Pendiente por defecto
    fecha_pedido: Optional[datetime] = None
    total: Decimal = Decimal("0.00")
    detalle: List[PedidoDetalle] = field(default_factory=list)

    def to_dict(self) -> dict:
        data = asdict(self)
        if isinstance(data.get("total"), Decimal):
            data["total"] = float(data["total"])
        if isinstance(data.get("fecha_pedido"), datetime):
            data["fecha_pedido"] = data["fecha_pedido"].isoformat()
        data["detalle"] = [d.to_dict() if isinstance(d, PedidoDetalle)
                           else d for d in self.detalle]
        return data

    @classmethod
    def from_row(cls, row: dict) -> "Pedido":
        if not row: return None
        return cls(**{k: row.get(k) for k in cls.__dataclass_fields__ if k in row})