"""
================================================================================
 app/utils/validators.py — VALIDADORES REUTILIZABLES
--------------------------------------------------------------------------------
 Capa: Utilidades
--------------------------------------------------------------------------------
 Responsabilidad:
   Funciones puras de validación (no tocan la base de datos ni HTTP).
================================================================================
"""

import re

from app.errors.exceptions import DatosInvalidosError, PasswordDebilError


# Expresión regular para contraseñas seguras.
# Equivale al trigger SQL original, pero ahora se valida ANTES de hashear,
# porque el hash no se puede validar contra este patrón.
REGEX_PASSWORD = re.compile(
    r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[@$!%*?&.#_\-]).{8,}$"
)

REGEX_CORREO = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def validar_password(password: str) -> str:
    """
    Verifica que la contraseña en texto plano cumpla los requisitos
    de complejidad. Lanza PasswordDebilError si no.
    """
    if not password or not REGEX_PASSWORD.match(password):
        raise PasswordDebilError()
    return password


def validar_correo(correo: str) -> str:
    """Verifica un formato razonable de correo electrónico."""
    if not correo or not REGEX_CORREO.match(correo):
        raise DatosInvalidosError("El correo electrónico no tiene un formato válido")
    return correo.strip().lower()


def requerir_campos(data: dict, campos: list) -> None:
    """
    Verifica que todos los campos obligatorios estén presentes y no vacíos.
    Lanza DatosInvalidosError listando los faltantes.
    """
    if not isinstance(data, dict):
        raise DatosInvalidosError("El cuerpo de la petición debe ser JSON")
    faltantes = [c for c in campos if not data.get(c)]
    if faltantes:
        raise DatosInvalidosError(
            f"Campos obligatorios faltantes: {', '.join(faltantes)}"
        )
