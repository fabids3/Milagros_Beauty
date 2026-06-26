"""Paquete decorators: anotaciones reutilizables (autenticación, roles)."""
from app.decorators.auth_decorators import login_required, requiere_rol

__all__ = ["login_required", "requiere_rol"]