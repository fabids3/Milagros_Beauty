"""
================================================================================
 app/repositories/pedido_repository.py — REPOSITORIO DE PEDIDOS
--------------------------------------------------------------------------------
 Capa: Acceso a datos
--------------------------------------------------------------------------------
 Maneja las dos tablas relacionadas: `pedidos` (cabecera) y
 `pedido_detalle` (líneas). Usa transacciones explícitas para garantizar
 atomicidad: si falla una línea, se revierte el pedido completo.
================================================================================
"""

from typing import List

from app.database import db_cursor, get_db
from app.models.pedido import Pedido, PedidoDetalle


class PedidoRepository:

    @staticmethod
    def crear_pedido_completo(pedido: Pedido) -> int:
        """
        Crea el pedido + todas sus líneas en una sola transacción.
        MySQL calcula automáticamente el subtotal de cada línea.
        Si algo falla, hace ROLLBACK completo.
        """
        conn = get_db()
        cursor = conn.cursor()
        try:
            # 1) Insertar cabecera
            cursor.execute(
                """
                INSERT INTO pedidos (id_usuario, total, id_estado)
                VALUES (%s, %s, %s)
                """,
                (pedido.id_usuario, pedido.total, pedido.id_estado),
            )
            id_pedido = cursor.lastrowid

            # 2) Insertar cada línea (subtotal lo calcula MySQL automáticamente)
            for linea in pedido.detalle:
                cursor.execute(
                    """
                    INSERT INTO pedido_detalle
                    (id_pedido, id_producto, cantidad, precio_unitario)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (
                        id_pedido,
                        linea.id_producto,
                        linea.cantidad,
                        linea.precio_unitario,
                    ),
                )

            conn.commit()
            return id_pedido
        except Exception:
            conn.rollback()
            raise
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def listar_ventas() -> List[dict]:
        """
        Listado para el panel admin: pedidos con nombre del cliente y estado.
        Devuelve dicts directos porque es una proyección (vista), no la
        entidad pura.
        """
        with db_cursor() as cursor:
            cursor.execute(
                """
                SELECT p.id_pedido,
                       u.nombre,
                       u.apellido,
                       p.total,
                       p.fecha_pedido,
                       p.id_estado,         # <--- ¡ESTA ES LA MAGIA!
                       e.nombre_estado
                FROM pedidos p
                JOIN usuarios u        ON p.id_usuario = u.id_usuario
                JOIN estados_pedido e  ON p.id_estado  = e.id_estado
                ORDER BY p.fecha_pedido DESC
                """
            )
            ventas = cursor.fetchall()
            # Convertimos Decimal/datetime para que jsonify funcione bien
            for v in ventas:
                if v.get("total") is not None:
                    v["total"] = float(v["total"])
                if v.get("fecha_pedido") is not None:
                    v["fecha_pedido"] = v["fecha_pedido"].isoformat()
            return ventas
        



    @staticmethod
    def cambiar_estado(id_pedido: int, id_estado: int) -> bool:
        """Actualiza el estado de un pedido en la base de datos."""
        with db_cursor(commit=True) as cursor:
            cursor.execute(
                "UPDATE pedidos SET id_estado = %s WHERE id_pedido = %s",
                (id_estado, id_pedido)
            )
            return cursor.rowcount > 0