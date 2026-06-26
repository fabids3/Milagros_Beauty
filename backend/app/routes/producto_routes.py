"""
================================================================================
 app/routes/producto_routes.py — RUTAS PÚBLICAS DE PRODUCTOS
--------------------------------------------------------------------------------
 Capa: Presentación
--------------------------------------------------------------------------------
 Endpoints:
   GET  /productos              — catálogo visible.
   PUT  /productos/<id>         — editar precio/stock (admin o superadmin).
   POST /descontar_stock        — usado al finalizar compra.
   POST /sumar_stock            — devolución de stock cuando se elimina del
                                   carrito.
================================================================================
"""

from flask import Blueprint, request, jsonify

from app.services.producto_service import ProductoService
from app.decorators import requiere_rol

producto_bp = Blueprint("productos", __name__)


@producto_bp.route("/productos", methods=["GET"])
def listar_productos():
    """Catálogo público: solo productos visibles."""
    return jsonify(ProductoService.listar_visibles()), 200


@producto_bp.route("/productos/<int:id_producto>", methods=["PUT"])
@requiere_rol("admin", "superadmin")
def editar_producto(id_producto: int):
    """Permite cambiar precio y stock. Protegido por rol."""
    resultado = ProductoService.editar_precio_y_stock(
        id_producto, request.get_json(silent=True) or {}
    )
    return jsonify({"mensaje": "Producto actualizado", "data": resultado}), 200


@producto_bp.route("/descontar_stock", methods=["POST"])
def descontar_stock():
    """
    Resta una unidad de stock.
    NOTA: la ruta es pública porque la usa el carrito desde el navegador,
    pero idealmente debería ser parte del flujo de /finalizar-compra.
    """
    data = request.get_json(silent=True) or {}
    ProductoService.descontar_stock(
        id_producto=data.get("id"),
        cantidad=int(data.get("cantidad", 1)),
    )
    return jsonify({"mensaje": "Stock descontado"}), 200


@producto_bp.route("/sumar_stock", methods=["POST"])
def sumar_stock():
    """Devuelve cantidad al stock (cuando el cliente quita del carrito)."""
    data = request.get_json(silent=True) or {}
    ProductoService.sumar_stock(
        id_producto=data.get("id"),
        cantidad=int(data.get("cantidad", 1)),
    )
    return jsonify({"mensaje": "Stock sumado"}), 200