"""
================================================================================
 app/repositories/producto_repository.py — REPOSITORIO DE PRODUCTOS
--------------------------------------------------------------------------------
 Capa: Acceso a datos
================================================================================
"""

from typing import List, Optional

from app.database import db_cursor
from app.models.producto import Producto


class ProductoRepository:
    """SQL para la tabla `productos`."""

    @staticmethod
    def listar_visibles() -> List[Producto]:
        """Productos con estado = 1 (visibles para el cliente)."""
        with db_cursor() as cursor:
            cursor.execute(
                "SELECT * FROM productos WHERE estado = 1 ORDER BY id_producto"
            )
            return [Producto.from_row(r) for r in cursor.fetchall()]

    @staticmethod
    def listar_todos() -> List[Producto]:
        """Todos los productos, visibles u ocultos (panel admin)."""
        with db_cursor() as cursor:
            cursor.execute("SELECT * FROM productos ORDER BY id_producto DESC")
            return [Producto.from_row(r) for r in cursor.fetchall()]

    @staticmethod
    def obtener_por_id(id_producto: int) -> Optional[Producto]:
        with db_cursor() as cursor:
            cursor.execute(
                "SELECT * FROM productos WHERE id_producto = %s",
                (id_producto,),
            )
            return Producto.from_row(cursor.fetchone())

    @staticmethod
    def crear(producto: Producto) -> int:
        with db_cursor(commit=True) as cursor:
            cursor.execute(
                """
                INSERT INTO productos
                  (nombre, descripcion, contenido, precio, imagen,
                   id_categoria, id_marca, stock, estado,
                   ideal_para, beneficios, ingredientes, modo_uso)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    producto.nombre,
                    producto.descripcion,
                    producto.contenido,
                    producto.precio,
                    producto.imagen,
                    producto.id_categoria,
                    producto.id_marca or 1,   # marca por defecto si no llega
                    producto.stock,
                    producto.estado,
                    producto.ideal_para,
                    producto.beneficios,
                    producto.ingredientes,
                    producto.modo_uso,
                ),
            )
            return cursor.lastrowid

    @staticmethod
    def actualizar_precio_y_stock(
        id_producto: int, precio: float, stock: int
    ) -> bool:
        with db_cursor(commit=True) as cursor:
            cursor.execute(
                """
                UPDATE productos
                SET precio = %s, stock = %s
                WHERE id_producto = %s
                """,
                (precio, stock, id_producto),
            )
            return cursor.rowcount > 0

    @staticmethod
    def descontar_stock(id_producto: int, cantidad: int = 1) -> bool:
        """Resta stock sólo si hay suficientes unidades disponibles."""
        with db_cursor(commit=True) as cursor:
            cursor.execute(
                """
                UPDATE productos
                SET stock = stock - %s
                WHERE id_producto = %s AND stock >= %s
                """,
                (cantidad, id_producto, cantidad),
            )
            return cursor.rowcount > 0

    @staticmethod
    def sumar_stock(id_producto: int, cantidad: int) -> bool:
        with db_cursor(commit=True) as cursor:
            cursor.execute(
                "UPDATE productos SET stock = stock + %s WHERE id_producto = %s",
                (cantidad, id_producto),
            )
            return cursor.rowcount > 0

    @staticmethod
    def cambiar_visibilidad(id_producto: int, visible: bool) -> bool:
        """Activa (1) o desactiva (0) el producto del catálogo público."""
        with db_cursor(commit=True) as cursor:
            cursor.execute(
                "UPDATE productos SET estado = %s WHERE id_producto = %s",
                (1 if visible else 0, id_producto),
            )
            return cursor.rowcount > 0