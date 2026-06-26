"""
================================================================================
 app/services/producto_service.py — SERVICIO DE PRODUCTOS
--------------------------------------------------------------------------------
 Capa: Lógica de negocio
================================================================================
"""

from decimal import Decimal, InvalidOperation
from typing import List

from app.models.producto import Producto
from app.repositories.producto_repository import ProductoRepository
from app.errors.exceptions import (
    DatosInvalidosError,
    RecursoNoEncontradoError,
    StockInsuficienteError,
)
from app.utils.validators import requerir_campos


class ProductoService:

    @staticmethod
    def listar_visibles() -> List[dict]:
        return [p.to_dict() for p in ProductoRepository.listar_visibles()]

    @staticmethod
    def crear(data: dict) -> Producto:
        """Crea un producto nuevo (lo invocan admin y superadmin)."""
        requerir_campos(data, ["nombre", "precio", "stock", "id_categoria"])

        try:
            precio = Decimal(str(data["precio"]))
            stock = int(data["stock"])
        except (InvalidOperation, ValueError, TypeError):
            raise DatosInvalidosError("Precio o stock con formato inválido")

        if precio < 0 or stock < 0:
            raise DatosInvalidosError("Precio y stock no pueden ser negativos")

        producto = Producto(
            nombre=data["nombre"].strip(),
            descripcion=(data.get("descripcion") or "").strip(),
            contenido=(data.get("contenido") or "").strip(),
            precio=precio,
            imagen=(data.get("imagen") or "").strip(),
            id_categoria=int(data["id_categoria"]),
            id_marca=int(data.get("id_marca") or 1),
            stock=stock,
            estado=1,
            ideal_para=(data.get("ideal_para") or "").strip(),
            beneficios=(data.get("beneficios") or "").strip(),
            ingredientes=(data.get("ingredientes") or "").strip(),
            modo_uso=(data.get("modo_uso") or "").strip(),
        )
        producto.id_producto = ProductoRepository.crear(producto)
        return producto

    @staticmethod
    def editar_precio_y_stock(id_producto: int, data: dict) -> dict:
        if "precio" not in data or "stock" not in data:
            raise DatosInvalidosError("Debes enviar precio y stock")

        if ProductoRepository.obtener_por_id(id_producto) is None:
            raise RecursoNoEncontradoError("Producto no encontrado")

        try:
            precio = float(data["precio"])
            stock = int(data["stock"])
        except (ValueError, TypeError):
            raise DatosInvalidosError("Precio o stock con formato inválido")

        if precio < 0 or stock < 0:
            raise DatosInvalidosError("Precio y stock no pueden ser negativos")

        ProductoRepository.actualizar_precio_y_stock(id_producto, precio, stock)
        return {"id_producto": id_producto, "precio": precio, "stock": stock}

    @staticmethod
    def descontar_stock(id_producto: int, cantidad: int = 1) -> None:
        """Resta unidades. Lanza StockInsuficienteError si no alcanza."""
        if cantidad <= 0:
            raise DatosInvalidosError("La cantidad debe ser positiva")
        ok = ProductoRepository.descontar_stock(id_producto, cantidad)
        if not ok:
            raise StockInsuficienteError()

    @staticmethod
    def sumar_stock(id_producto: int, cantidad: int) -> None:
        if cantidad <= 0:
            raise DatosInvalidosError("La cantidad debe ser positiva")
        ProductoRepository.sumar_stock(id_producto, cantidad)