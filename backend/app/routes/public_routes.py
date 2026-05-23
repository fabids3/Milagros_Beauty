"""
================================================================================
 app/routes/public_routes.py — RUTAS PÚBLICAS (VISTAS HTML)
--------------------------------------------------------------------------------
 Capa: Presentación (V de MVC: View)
--------------------------------------------------------------------------------
 Sirve las plantillas HTML estáticas. No procesa datos: solo renderiza.
================================================================================
"""

from flask import Blueprint, render_template

public_bp = Blueprint("public", __name__)


@public_bp.route("/")
def inicio():
    """Página principal con catálogo."""
    return render_template("index.html")


@public_bp.route("/admin")
def admin_view():
    """
    Panel de administración (rol admin = moderador).
    Nota: la protección de los DATOS está en las rutas /admin/* del API.
    Esta es solo la página HTML; sin sesión el JS la deja vacía.
    """
    return render_template("admin.html")


@public_bp.route("/superadmin")
def superadmin_view():
    """Panel del superadmin (la propietaria)."""
    return render_template("superadmin.html")


@public_bp.route("/carrito.html")
def carrito_page():
    """Página del carrito de compras."""
    return render_template("carrito.html")


@public_bp.route("/mantenimiento")
def mantenimiento_page():
    """Página de mantenimiento (mostrada cuando algo falla)."""
    return render_template("mantenimiento.html")
