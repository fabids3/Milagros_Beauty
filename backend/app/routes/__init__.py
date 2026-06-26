"""
================================================================================
 app/routes/__init__.py — REGISTRO DE BLUEPRINTS
--------------------------------------------------------------------------------
 Capa: Presentación (controllers)
--------------------------------------------------------------------------------
 Responsabilidad:
   Importar TODOS los blueprints del proyecto y registrarlos en la app.
   Es el único punto donde la app conoce los módulos de rutas.

 Cómo agregar un nuevo módulo:
   1) Crear el archivo en app/routes/mi_modulo_routes.py
   2) Definir   mi_bp = Blueprint("mi_modulo", __name__, url_prefix="/mi")
   3) Importarlo aquí y añadirlo a `app.register_blueprint`.
================================================================================
"""

from app.routes.public_routes import public_bp
from app.routes.auth_routes import auth_bp
from app.routes.producto_routes import producto_bp
from app.routes.pedido_routes import pedido_bp
from app.routes.admin_routes import admin_bp
from app.routes.superadmin_routes import superadmin_bp
from app.routes.configuracion_routes import config_bp


def registrar_blueprints(app):
    """Registra todos los blueprints sobre la instancia de Flask."""
    app.register_blueprint(public_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(producto_bp)
    app.register_blueprint(pedido_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(superadmin_bp)
    app.register_blueprint(config_bp)