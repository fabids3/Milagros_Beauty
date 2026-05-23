"""
================================================================================
 app/errors/exceptions.py — EXCEPCIONES DEL DOMINIO
--------------------------------------------------------------------------------
 Capa: Errores / Contratos
--------------------------------------------------------------------------------
 Responsabilidad:
   Definir excepciones SEMÁNTICAS que representan errores de negocio
   (no técnicos). Cada excepción incluye un código HTTP sugerido.

 Justificación didáctica:
   En lugar de lanzar Exception genéricas, lanzamos clases con nombre claro
   (CorreoDuplicadoError, CredencialesInvalidasError). Esto:
     - Documenta el dominio: el lector entiende qué falló sin leer el mensaje.
     - Permite respuestas HTTP automáticas vía handler global.
     - Facilita las pruebas unitarias: assertRaises(CorreoDuplicadoError).
================================================================================
"""


class ErrorDominio(Exception):
    """
    Clase base de todos los errores propios del sistema.
    Toda excepción del dominio debe heredar de aquí.
    """
    status_code = 500
    mensaje = "Error interno del servidor"

    def __init__(self, mensaje: str = None, status_code: int = None):
        super().__init__(mensaje or self.mensaje)
        if mensaje:
            self.mensaje = mensaje
        if status_code:
            self.status_code = status_code

    def to_dict(self):
        """Serializa la excepción a un dict listo para jsonify()."""
        return {"error": self.mensaje}


# --- Errores de autenticación / autorización -------------------------------

class CredencialesInvalidasError(ErrorDominio):
    """El correo no existe o la contraseña es incorrecta."""
    status_code = 401
    mensaje = "Correo o contraseña incorrectos"


class NoAutenticadoError(ErrorDominio):
    """El usuario no ha iniciado sesión y la ruta lo exige."""
    status_code = 401
    mensaje = "Debes iniciar sesión para acceder a este recurso"


class AccesoDenegadoError(ErrorDominio):
    """El usuario está autenticado pero no tiene el rol requerido."""
    status_code = 403
    mensaje = "No tienes permisos para realizar esta acción"


# --- Errores de validación / datos -----------------------------------------

class DatosInvalidosError(ErrorDominio):
    """Faltan campos obligatorios o tienen formato incorrecto."""
    status_code = 400
    mensaje = "Datos inválidos o incompletos"


class CorreoDuplicadoError(ErrorDominio):
    """Se intenta registrar un correo que ya existe en la base."""
    status_code = 409
    mensaje = "Este correo ya está registrado"


class PasswordDebilError(ErrorDominio):
    """La contraseña no cumple los requisitos mínimos de seguridad."""
    status_code = 400
    mensaje = (
        "La contraseña debe tener mínimo 8 caracteres, una mayúscula, "
        "una minúscula, un número y un símbolo (@$!%*?&.#_-)"
    )


# --- Errores de recursos ---------------------------------------------------

class RecursoNoEncontradoError(ErrorDominio):
    """No se encuentra el producto, usuario o pedido solicitado."""
    status_code = 404
    mensaje = "Recurso no encontrado"


class StockInsuficienteError(ErrorDominio):
    """No hay suficientes unidades del producto."""
    status_code = 400
    mensaje = "Stock insuficiente"


# --- Errores de infraestructura --------------------------------------------

class BaseDeDatosError(ErrorDominio):
    """Error al conectar o consultar la base de datos."""
    status_code = 503
    mensaje = "Servicio de base de datos no disponible"
