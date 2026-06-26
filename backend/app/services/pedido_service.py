"""
================================================================================
 app/services/pedido_service.py — SERVICIO DE PEDIDOS
--------------------------------------------------------------------------------
 Capa: Lógica de negocio
--------------------------------------------------------------------------------
 Responsabilidad:
   Procesar la "finalización de compra": validar carrito, calcular totales,
   persistir cabecera + detalle de forma atómica.

 Regla de negocio importante:
   El TOTAL se recalcula en el servidor a partir de los precios reales
   de los productos. NUNCA se confía en el `total` que envía el navegador
   (podría haberse manipulado en DevTools).
================================================================================
"""

from decimal import Decimal
from typing import List

from app.models.pedido import Pedido, PedidoDetalle
from app.repositories.pedido_repository import PedidoRepository
from app.repositories.producto_repository import ProductoRepository
from app.errors.exceptions import (
    DatosInvalidosError,
    RecursoNoEncontradoError,
)


class PedidoService:

    @staticmethod
    def listar_ventas() -> List[dict]:
        """Listado de pedidos para el panel admin."""
        return PedidoRepository.listar_ventas()

    @staticmethod
    def finalizar_compra(id_usuario: int, carrito: list) -> dict:
        """
        Crea un pedido a partir del carrito enviado por el cliente.
        - id_usuario:   se toma de la sesión (no del body, por seguridad).
        - carrito:      lista de {id, cantidad} enviada desde el frontend.
        """
        if not id_usuario:
            raise DatosInvalidosError("Sesión inválida o expirada")

        if not isinstance(carrito, list) or len(carrito) == 0:
            raise DatosInvalidosError("El carrito está vacío")

        # 1) Construir las líneas del pedido con precios REALES de la BD.
        lineas: List[PedidoDetalle] = []
        total = Decimal("0.00")

        for item in carrito:
            id_prod = item.get("id")
            cantidad = int(item.get("cantidad", 1))

            if not id_prod or cantidad <= 0:
                raise DatosInvalidosError(
                    "Cada item del carrito requiere id y cantidad positiva"
                )

            producto = ProductoRepository.obtener_por_id(id_prod)
            if producto is None:
                raise RecursoNoEncontradoError(
                    f"Producto {id_prod} no encontrado"
                )

            subtotal = producto.precio * cantidad
            total += subtotal

            lineas.append(PedidoDetalle(
                id_producto=id_prod,
                cantidad=cantidad,
                precio_unitario=producto.precio,
                subtotal=subtotal,
            ))

        # 2) Crear el pedido completo en una sola transacción.
        pedido = Pedido(
            id_usuario=id_usuario,
            id_estado=1,                # 1 = Pendiente
            total=total,
            detalle=lineas,
        )
        id_pedido = PedidoRepository.crear_pedido_completo(pedido)

        return {
            "id_pedido": id_pedido,
            "total": float(total),
            "items": len(lineas),
        }