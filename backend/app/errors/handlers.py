"""
================================================================================
 app/errors/handlers.py — MANEJADORES GLOBALES DE ERRORES
--------------------------------------------------------------------------------
 Capa: Errores / Infraestructura
--------------------------------------------------------------------------------
 Responsabilidad:
   Convertir cualquier excepción que llegue a Flask en una respuesta uniforme.
   - Si es JSON (petición de API)  → devuelve {"error": "..."} con status code.
   - Si es navegación HTML normal  → muestra mantenimiento.html.

 Justificación didáctica:
   El requerimiento académico exige que la página NUNCA muestre la pantalla
   por defecto de Flask en caso de error. Este handler garantiza ese
   comportamiento sin tener que poner try/except en cada ruta.
================================================================================
"""

from flask import jsonify, render_template, request

from app.errors.exceptions import ErrorDominio


def _es_peticion_api(req) -> bool:
    """
    Heurística para decidir si la petición espera JSON o HTML.
    Reglas:
      - Si pide JSON explícitamente en el header Accept → API.
      - Si la URL es una ruta de página HTML conocida → HTML.
    """
    if req.is_json or "application/json" in (req.headers.get("Accept") or ""):
        return True
    rutas_html = ("/", "/admin", "/superadmin", "/carrito.html", "/mantenimiento")
    return req.path not in rutas_html


def registrar_handlers(app):
    """
    Registra todos los handlers globales en la app.
    Se llama desde create_app().
    """

    # --- Excepciones del dominio (las nuestras) ----------------------------
    @app.errorhandler(ErrorDominio)
    def manejar_error_dominio(err: ErrorDominio):
        """Cualquier excepción que herede de ErrorDominio cae aquí."""
        if _es_peticion_api(request):
            return jsonify(err.to_dict()), err.status_code
        # Errores de infraestructura → página de mantenimiento
        if err.status_code >= 500:
            return render_template("mantenimiento.html"), err.status_code
        return jsonify(err.to_dict()), err.status_code

    # --- Errores HTTP estándar de Flask -----------------------------------
    @app.errorhandler(404)
    def manejar_404(_err):
        if _es_peticion_api(request):
            return jsonify({"error": "Recurso no encontrado"}), 404
        return render_template("mantenimiento.html"), 404

    @app.errorhandler(405)
    def manejar_405(_err):
        return jsonify({"error": "Método HTTP no permitido"}), 405

    @app.errorhandler(500)
    def manejar_500(_err):
        if _es_peticion_api(request):
            return jsonify({"error": "Error interno del servidor"}), 500
        return render_template("mantenimiento.html"), 500

    # --- Cualquier otra excepción no controlada ---------------------------
    @app.errorhandler(Exception)
    def manejar_excepcion_no_controlada(err: Exception):
        """
        Último recurso: cualquier error inesperado (incluida una caída
        de la base de datos) acaba aquí. Se muestra mantenimiento.html
        para cumplir el requerimiento académico.
        """
        # En modo debug, dejamos que Flask muestre el traceback completo.
        if app.config.get("DEBUG"):
            raise err
        if _es_peticion_api(request):
            return jsonify({"error": "Error interno del servidor"}), 500
        return render_template("mantenimiento.html"), 500
