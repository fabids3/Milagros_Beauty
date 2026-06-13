"""
================================================================================
 app/routes/auth_routes.py — RUTAS DE AUTENTICACIÓN
--------------------------------------------------------------------------------
 Capa: Presentación (Controllers)
--------------------------------------------------------------------------------
 Endpoints:
   POST /registrar  — registro público de clientes.
   POST /login      — autenticación.
   POST /logout     — cierre de sesión.
   GET  /sesion     — devuelve el usuario en sesión (utilidad para el front).
================================================================================
"""

from flask import Blueprint, request, jsonify

from app.services.auth_service import AuthService

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/registrar", methods=["POST"])
def registrar():
    """Registra un cliente nuevo. Devuelve mensaje 201."""
    usuario = AuthService.registrar_cliente(request.get_json(silent=True) or {})
    return jsonify({
        "mensaje": "¡Registro exitoso! Ya puedes iniciar sesión.",
        "user": usuario.to_dict(),
    }), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    """Autentica un usuario y abre una sesión firmada."""
    data = request.get_json(silent=True) or {}
    usuario = AuthService.login(
        correo=data.get("correo"),
        password=data.get("password"),
    )
    # Mantenemos el contrato histórico: el frontend espera {"user": ...}
    return jsonify({"user": usuario.to_dict()}), 200


@auth_bp.route("/logout", methods=["POST"])
def logout():
    """Cierra la sesión actual."""
    AuthService.cerrar_sesion()
    return jsonify({"mensaje": "Sesión cerrada"}), 200


@auth_bp.route("/sesion", methods=["GET"])
def sesion_actual():
    """Devuelve la sesión activa o null si no hay."""
    return jsonify({"user": AuthService.usuario_actual()}), 200
