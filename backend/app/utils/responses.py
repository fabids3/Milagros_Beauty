"""
================================================================================
 app/utils/responses.py — HELPERS PARA RESPUESTAS JSON UNIFORMES
--------------------------------------------------------------------------------
 Capa: Utilidades
--------------------------------------------------------------------------------
 Responsabilidad:
   Generar respuestas JSON con el mismo "contrato" en toda la API:
     - éxito:  {"mensaje": "...", "data": {...}}
     - error:  {"error": "..."}
================================================================================
"""

from flask import jsonify


def ok(data=None, mensaje: str = None, status: int = 200):
    """Respuesta exitosa estándar."""
    body = {}
    if mensaje is not None:
        body["mensaje"] = mensaje
    if data is not None:
        body["data"] = data
    # Si no hay nada más que reportar, devolvemos solo los datos para no
    # romper el contrato que ya espera el frontend (lista de productos, etc.)
    if not body and data is not None:
        return jsonify(data), status
    return jsonify(body or data or {}), status


def error(mensaje: str, status: int = 400):
    """Respuesta de error estándar."""
    return jsonify({"error": mensaje}), status
