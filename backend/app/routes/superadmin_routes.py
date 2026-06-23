"""
================================================================================
 app/routes/superadmin_routes.py — RUTAS EXCLUSIVAS DEL SUPERADMIN
--------------------------------------------------------------------------------
 Capa: Presentación
--------------------------------------------------------------------------------
 Endpoints exclusivos para la propietaria:
   POST /admin/moderadores/nuevo    — crear un moderador (admin).
   GET  /admin/clientes             — ver clientes registrados.
   PUT  /admin/usuarios/<id>/rol    — cambiar el rol de un usuario.

 NOTA: dejamos los endpoints bajo /admin/* porque así los conoce el frontend
 actual, pero la protección es @requiere_rol("superadmin"), no admin.
================================================================================
"""

from flask import Blueprint, request, jsonify

from app.services.auth_service import AuthService
from app.services.usuario_service import UsuarioService
from app.decorators import requiere_rol

superadmin_bp = Blueprint("superadmin", __name__, url_prefix="/admin")


@superadmin_bp.route("/moderadores/nuevo", methods=["POST"])
@requiere_rol("superadmin")
def crear_moderador():
    """Crea un usuario con rol admin (moderador)."""
    usuario = AuthService.registrar_moderador(
        request.get_json(silent=True) or {}
    )
    return jsonify({
        "mensaje": "¡Moderador creado con éxito!",
        "user": usuario.to_dict(),
    }), 201


@superadmin_bp.route("/clientes", methods=["GET"])
@requiere_rol("superadmin")
def listar_clientes():
    """Listado de clientes (solo lo ve la propietaria)."""
    return jsonify(UsuarioService.listar_clientes()), 200


@superadmin_bp.route("/usuarios/<int:id_usuario>/rol", methods=["PUT"])
@requiere_rol("superadmin")
def cambiar_rol(id_usuario: int):
    """
    Cambia el rol de un usuario.
    El nuevo_rol debe ser 2 (cliente) o 3 (admin). El rol superadmin (1)
    NUNCA se puede asignar desde aquí — el servicio lo bloquea.
    """
    data = request.get_json(silent=True) or {}
    usuario = UsuarioService.cambiar_rol(
        id_usuario=id_usuario,
        nuevo_rol=int(data.get("nuevo_rol", 0)),
    )
    return jsonify({
        "mensaje": "Rol actualizado",
        "user": usuario.to_dict(),
    }), 200

@app.route('/configuracion/terminos')
def obtener_terminos():

    conexion = conectar_db()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT terminos
        FROM configuracion
        WHERE id_config = 1
    """)

    data = cursor.fetchone()

    cursor.close()
    conexion.close()

    return jsonify(data)
