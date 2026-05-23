"""
================================================================================
 app/routes/configuracion_routes.py — RUTAS DE CONFIGURACIÓN DE LA TIENDA
--------------------------------------------------------------------------------
 Capa: Presentación
--------------------------------------------------------------------------------
 Endpoints:
   GET  /configuracion/titulo         — título público (cualquiera).
   GET  /configuracion/info           — info pública (cualquiera).
   POST /admin/configuracion/titulo   — editar título (admin / superadmin).
   POST /admin/configuracion/info     — editar info (admin / superadmin).
================================================================================
"""

from flask import Blueprint, request, jsonify

from app.services.configuracion_service import ConfiguracionService
from app.decorators import requiere_rol

config_bp = Blueprint("configuracion", __name__)


# --- Lectura pública --------------------------------------------------------

@config_bp.route("/configuracion/titulo", methods=["GET"])
def obtener_titulo():
    return jsonify(ConfiguracionService.obtener_titulo()), 200


@config_bp.route("/configuracion/info", methods=["GET"])
def obtener_info():
    return jsonify(ConfiguracionService.obtener_info_empresa()), 200


# --- Escritura restringida --------------------------------------------------

@config_bp.route("/admin/configuracion/titulo", methods=["POST"])
@requiere_rol("admin", "superadmin")
def actualizar_titulo():
    data = request.get_json(silent=True) or {}
    ConfiguracionService.actualizar_titulo(data.get("titulo"))
    return jsonify({"mensaje": "¡Título actualizado con éxito!"}), 200


@config_bp.route("/admin/configuracion/info", methods=["POST"])
@requiere_rol("admin", "superadmin")
def actualizar_info():
    data = request.get_json(silent=True) or {}
    ConfiguracionService.actualizar_info_empresa(data)
    return jsonify({"mensaje": "¡Información actualizada con éxito!"}), 200
