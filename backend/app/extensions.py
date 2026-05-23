"""
================================================================================
 app/extensions.py — INSTANCIAS DE EXTENSIONES FLASK
--------------------------------------------------------------------------------
 Capa: Infraestructura
--------------------------------------------------------------------------------
 Responsabilidad:
   Crear (sin inicializar todavía) las extensiones que usa la aplicación.
   Cada extensión se conecta luego a la app dentro de create_app() vía
   `extension.init_app(app)`.

 Justificación didáctica:
   Este archivo evita el problema de "imports circulares". Si pusiéramos
   `bcrypt = Bcrypt(app)` directamente en __init__.py, otros módulos no
   podrían importarlo sin importar también la app. El patrón init_app()
   permite tener una sola instancia compartida en todo el proyecto.
================================================================================
"""

from flask_bcrypt import Bcrypt
from flask_cors import CORS


# Hashing de contraseñas con bcrypt.
# Lo usamos en services/auth_service.py para registrar y validar usuarios.
bcrypt = Bcrypt()


# Cross-Origin Resource Sharing.
# Necesario porque el frontend hace peticiones fetch() desde el navegador.
# - supports_credentials=True: permite que viajen las cookies de sesión.
# - origins=*: en producción se debe restringir al dominio real.
cors = CORS(supports_credentials=True)
