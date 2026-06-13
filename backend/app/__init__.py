"""
================================================================================
 app/__init__.py — APPLICATION FACTORY
--------------------------------------------------------------------------------
 Patrón aplicado: Factory Method (Gang of Four)
 Capa           : Bootstrap del paquete principal
--------------------------------------------------------------------------------
 Responsabilidad:
   Construir y configurar la instancia de Flask. Aquí NO se define lógica de
   negocio ni rutas: solo se ensamblan los componentes.

 Justificación didáctica (para sustentación):
   - El patrón Application Factory permite tener varias configuraciones de la
     app (desarrollo, pruebas, producción) llamando a create_app(ConfigX).
   - Evita el problema clásico de Flask conocido como "circular imports", que
     ocurre cuando módulos diferentes importan la misma instancia global.
   - Es el patrón oficial recomendado por la documentación de Flask desde 1.0.
================================================================================
"""

import logging
from flask import Flask

from app.config import get_config
from app.extensions import bcrypt, cors
from app.routes import registrar_blueprints
from app.errors.handlers import registrar_handlers


def create_app(config_class=None):
    """
    Construye una instancia de Flask totalmente configurada.

    Parámetros:
        config_class: clase de configuración (Config, DevelopmentConfig, etc.)
                      Si es None, se determina automáticamente según FLASK_ENV.

    Retorna:
        Una instancia de Flask lista para servir peticiones.
    """

    # 1) Instanciar Flask indicándole dónde están las plantillas y los estáticos.
    #    Como ambos están DENTRO del paquete app/, Flask los encuentra solo.
    app = Flask(
        __name__,
        static_folder="static",
        template_folder="templates",
    )

    # En producción con Gunicorn, hacemos que app.logger escriba en los mismos
    # handlers que gunicorn.error para que Railway muestre bien los tracebacks.
    gunicorn_error_logger = logging.getLogger("gunicorn.error")
    if gunicorn_error_logger.handlers:
        app.logger.handlers = gunicorn_error_logger.handlers
        app.logger.setLevel(gunicorn_error_logger.level or logging.DEBUG)

    # 2) Cargar configuración (lee variables del archivo .env).
    config = config_class or get_config()
    app.config.from_object(config)
    app.logger.warning(f"FLASK_ENV activo: {app.config.get('ENV', 'no-env')}")
    app.logger.warning(f"DB host: {app.config['DB_CONFIG'].get('host')}")
    app.logger.warning(f"DB port: {app.config['DB_CONFIG'].get('port')}")
    app.logger.warning(f"DB user: {app.config['DB_CONFIG'].get('user')}")
    app.logger.warning(f"DB name: {app.config['DB_CONFIG'].get('database')}")
    app.logger.warning(f"DB ssl_disabled: {app.config['DB_CONFIG'].get('ssl_disabled')}")

    # 3) Inicializar extensiones de Flask (bcrypt, CORS) sobre esta app.
    #    El patrón init_app() permite que las extensiones se creen una sola vez
    #    en app/extensions.py y se "conecten" aquí. Útil para pruebas.
    bcrypt.init_app(app)
    cors.init_app(app)

    # 4) Registrar todos los Blueprints (módulos de rutas).
    #    Cada Blueprint agrupa endpoints de un mismo dominio: auth, productos,
    #    pedidos, admin, superadmin, públicas.
    registrar_blueprints(app)

    # 5) Registrar los manejadores globales de errores y excepciones
    #    personalizadas. Garantiza respuestas JSON uniformes ante fallos.
    registrar_handlers(app)

    return app