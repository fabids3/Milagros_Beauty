"""
================================================================================
 app/routes/pedido_routes.py — RUTAS DE PEDIDOS
--------------------------------------------------------------------------------
 Capa: Presentación
--------------------------------------------------------------------------------
 Endpoints:
   POST /finalizar-compra   — finaliza el pedido (URL canónica).
   POST /finalizar_compra   — alias con guion bajo (compatibilidad histórica
                              porque el frontend actual usa ambas).
================================================================================
"""

from flask import Blueprint, request, jsonify, session

from app.services.pedido_service import PedidoService
from app.decorators import login_required

pedido_bp = Blueprint("pedidos", __name__)


def _procesar_finalizacion():
    """Lógica común. Toma id_usuario de la sesión, NO del body."""
    data = request.get_json(silent=True) or {}
    id_usuario = session.get("id_usuario") or data.get("id_usuario")
    resultado = PedidoService.finalizar_compra(
        id_usuario=id_usuario,
        carrito=data.get("carrito", []),
    )
    return jsonify({"mensaje": "Pedido guardado con éxito", **resultado}), 201


# Dos rutas registradas para apuntar a la misma función (compat. histórica).
@pedido_bp.route("/finalizar-compra", methods=["POST"])
def finalizar_compra_guion():
    return _procesar_finalizacion()


@pedido_bp.route("/finalizar_compra", methods=["POST"])
def finalizar_compra_underscore():
    return _procesar_finalizacion()