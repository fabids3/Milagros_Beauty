"""
================================================================================
 app/routes/admin_routes.py — RUTAS DEL PANEL ADMIN
--------------------------------------------------------------------------------
 Capa: Presentación
--------------------------------------------------------------------------------
 Endpoints accesibles para "admin" (moderadores) Y "superadmin":
   GET  /admin/ventas               — listado de ventas.
   POST /admin/productos/nuevo      — crear producto.
================================================================================
"""

from flask import Blueprint, request, jsonify

from app.services.producto_service import ProductoService
from app.services.pedido_service import PedidoService
from app.decorators import requiere_rol

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/ventas", methods=["GET"])
@requiere_rol("admin", "superadmin")
def listar_ventas():
    """Listado de ventas para los empleados."""
    return jsonify(PedidoService.listar_ventas()), 200


@admin_bp.route("/productos/nuevo", methods=["POST"])
@requiere_rol("admin", "superadmin")
def crear_producto():
    """Crea un producto nuevo en el catálogo."""
    producto = ProductoService.crear(request.get_json(silent=True) or {})
    return jsonify({
        "mensaje": "¡Producto creado con éxito!",
        "producto": producto.to_dict(),
    }), 201