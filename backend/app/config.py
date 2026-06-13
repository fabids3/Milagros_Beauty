"""
================================================================================
 app/config.py — CONFIGURACIÓN DE LA APLICACIÓN
--------------------------------------------------------------------------------
 Capa: Infraestructura / Configuración
--------------------------------------------------------------------------------
 Responsabilidad:
   Centralizar TODOS los valores configurables (credenciales, claves, puertos)
   leyéndolos desde variables de entorno (.env), nunca desde el código.

 Justificación didáctica:
   Aplica el principio III (Config) de los Twelve-Factor App:
   "La configuración debe estar separada del código, en variables de entorno".
   Esto permite cambiar credenciales o entornos sin recompilar/redistribuir.
================================================================================
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Localizamos el archivo .env un nivel arriba de este paquete (en backend/).
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


class Config:
    """Configuración BASE — compartida por todos los entornos."""

    # --- Seguridad de sesiones ---------------------------------------------
    # Esta clave firma las cookies de sesión. Si cambia, todas las sesiones
    # existentes se invalidan (los usuarios deben volver a iniciar sesión).
    SECRET_KEY = os.getenv("SECRET_KEY", "clave-insegura-solo-para-desarrollo")

    # Duración de la sesión y banderas de seguridad de la cookie
    SESSION_COOKIE_HTTPONLY = True   # JS no puede leer la cookie (anti-XSS)
    SESSION_COOKIE_SAMESITE = "Lax"  # Mitigación de CSRF básica
    # SESSION_COOKIE_SECURE = True   # Activar en producción cuando haya HTTPS

    # --- Base de datos -----------------------------------------------------
    # Los valores se leen del .env. Si falta alguno, se usa un default seguro
    # para desarrollo con XAMPP (root sin contraseña).
    DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 3306)),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "railway"),
    "charset": "utf8mb4",
    "use_unicode": True,
    "ssl_disabled": True,
    "connection_timeout": 10,
    "auth_plugin": "mysql_native_password",
    }

    # --- Configuración de hashing bcrypt -----------------------------------
    # "rounds" es el costo computacional: a mayor número, más lento (más seguro).
    # 12 es el estándar recomendado por OWASP para 2024-2026.
    BCRYPT_LOG_ROUNDS = 12

    # --- JSON --------------------------------------------------------------
    JSON_AS_ASCII = False  # Permite acentos y emojis en respuestas JSON


class DevelopmentConfig(Config):
    """Configuración para desarrollo local (XAMPP, debug activado)."""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Configuración para producción (hosting real con HTTPS)."""
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True  # Solo enviar cookie por HTTPS


class TestingConfig(Config):
    """Configuración para pruebas automatizadas."""
    DEBUG = False
    TESTING = True
    BCRYPT_LOG_ROUNDS = 4  # Más rápido en pruebas


def get_config():
    """
    Devuelve la clase de configuración adecuada según FLASK_ENV.
    Si la variable no está definida, asume 'development'.
    """
    env = os.getenv("FLASK_ENV", "development").lower()
    mapping = {
        "development": DevelopmentConfig,
        "production": ProductionConfig,
        "testing": TestingConfig,
    }
    return mapping.get(env, DevelopmentConfig)
