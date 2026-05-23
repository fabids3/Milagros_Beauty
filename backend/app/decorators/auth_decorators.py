"""
================================================================================
 app/decorators/auth_decorators.py — DECORADORES DE SEGURIDAD
--------------------------------------------------------------------------------
 Capa: Seguridad transversal
 Patrón aplicado: Decorator Pattern (Gang of Four)
--------------------------------------------------------------------------------
 Responsabilidad:
   Proteger rutas exigiendo sesión activa y/o un rol específico, sin
   contaminar la lógica de cada endpoint con verificaciones repetitivas.

 Justificación didáctica:
   En el código original cada ruta admin que quería proteger sus datos
   tenía que repetir el patrón:
       id_solicitante = request.args.get('id_usuario')
       if not id_solicitante: return 401
       cursor.execute("SELECT id_rol FROM usuarios ...")
       if rol != 1: return 403
   Aquí lo reemplazamos por una anotación de UNA LÍNEA:
       @requiere_rol("superadmin")
================================================================================
"""

from functools import wraps

from flask import session

from app.errors.exceptions import NoAutenticadoError, AccesoDenegadoError
from app.models.usuario import NOMBRES_ROL


def login_required(funcion):
    """
    Garantiza que haya una sesión activa.
    Lanza NoAutenticadoError (401) si nadie ha iniciado sesión.
    """
    @wraps(funcion)
    def wrapper(*args, **kwargs):
        if "id_usuario" not in session:
            raise NoAutenticadoError()
        return funcion(*args, **kwargs)
    return wrapper


def requiere_rol(*roles_permitidos):
    """
    Garantiza que el usuario en sesión tenga al menos uno de los roles
    permitidos. Los roles se pasan por nombre lógico:
        @requiere_rol("admin", "superadmin")
        @requiere_rol("superadmin")
    """
    # Normalizamos los nombres por si llegan con mayúsculas/espacios
    roles_normalizados = {r.lower().strip() for r in roles_permitidos}

    def decorador(funcion):
        @wraps(funcion)
        def wrapper(*args, **kwargs):
            if "id_usuario" not in session:
                raise NoAutenticadoError()

            rol_actual = (session.get("rol") or "").lower()
            if rol_actual not in roles_normalizados:
                raise AccesoDenegadoError(
                    f"Requiere uno de los roles: {', '.join(roles_normalizados)}"
                )
            return funcion(*args, **kwargs)
        return wrapper
    return decorador
