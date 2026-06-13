"""
================================================================================
 run.py — PUNTO DE ENTRADA DE LA APLICACIÓN
--------------------------------------------------------------------------------
 Proyecto : Milagro's Beauty
 Capa     : Bootstrap / Arranque
 Autor    : Equipo ADSO
--------------------------------------------------------------------------------
 Responsabilidad:
   Único archivo ejecutable directamente. Su trabajo es:
     1. Crear la instancia de la aplicación llamando al Application Factory.
     2. Levantar el servidor de desarrollo de Flask en el puerto configurado.

 Por qué existe este archivo y no se mete todo en app/__init__.py:
   - Separa el "cómo construyo la app" (factory) del "cómo la ejecuto".
   - Permite que herramientas como gunicorn, pytest o un IDE importen la app
     SIN ejecutar automáticamente el servidor.
================================================================================
"""

import os
from app import create_app

# Construimos la aplicación a través del Application Factory.
# Esta línea se ejecuta tanto si corres "python run.py" como si la importa
# un servidor WSGI externo (gunicorn, uwsgi).
app = create_app()


if __name__ == "__main__":
    # Solo se ejecuta cuando lanzas el archivo manualmente con python.
    # Los valores se leen desde el archivo .env (cargado por config.py).
    host = os.getenv("APP_HOST", "0.0.0.0")
    port = int(os.getenv("APP_PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "1") == "1"

    print("=" * 70)
    print(f"  Milagro's Beauty — servidor iniciando en http://{host}:{port}")
    print(f"  Modo debug: {debug}")
    print("=" * 70)

    app.run(host=host, port=port, debug=debug)
