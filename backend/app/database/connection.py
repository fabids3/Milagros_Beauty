"""
================================================================================
 app/database/connection.py — GESTIÓN DE CONEXIONES A MYSQL
--------------------------------------------------------------------------------
 Capa: Acceso a datos (infraestructura)
--------------------------------------------------------------------------------
 Responsabilidad:
   1. Crear conexiones MySQL usando la configuración del .env.
   2. Proveer un context manager (`with db_cursor() as cursor: ...`) que
      garantiza que la conexión y el cursor SIEMPRE se cierran, incluso si
      ocurre una excepción.

 Justificación didáctica:
   En el código original (app.py) el patrón se repetía 14 veces:
       conn = get_db(); cursor = conn.cursor()
       try: ...
       finally: cursor.close(); conn.close()
   Con un context manager (PEP 343 + decorador @contextmanager), esto se
   reduce a:
       with db_cursor() as cursor:
           cursor.execute(...)
   El cierre y el rollback se vuelven automáticos. Es Python idiomático.
================================================================================
"""

from contextlib import contextmanager
from typing import Generator

import mysql.connector
from flask import current_app

from app.errors.exceptions import BaseDeDatosError


def get_db():
    """
    Crea y devuelve una conexión nueva a MySQL.

    Importante: NO mantenemos un pool global porque para un proyecto académico
    monolítico no se justifica. Cada petición HTTP abre y cierra su conexión.

    Retorna:
        mysql.connector.connection.MySQLConnection
    """
    try:
        return mysql.connector.connect(**current_app.config["DB_CONFIG"])
    except mysql.connector.Error as err:
        # Encapsulamos el error de driver en una excepción del dominio
        # para que las capas superiores no dependan de mysql.connector.
        raise BaseDeDatosError(
            f"No se pudo conectar a la base de datos: {err}"
        ) from err


@contextmanager
def db_cursor(dictionary: bool = True, commit: bool = False) -> Generator:
    """
    Context manager que entrega un cursor listo para usar y se encarga del
    cierre y del commit/rollback automático.

    Parámetros:
        dictionary: si True, fetchall() devuelve list[dict] (cómodo para JSON).
                    Si False, devuelve list[tuple] (más rápido en algunos casos).
        commit:     si True, hace COMMIT automático al salir sin error.
                    Útil para INSERT/UPDATE/DELETE.

    Uso:
        with db_cursor() as cursor:
            cursor.execute("SELECT * FROM productos")
            return cursor.fetchall()

        with db_cursor(commit=True) as cursor:
            cursor.execute("UPDATE ...")
    """
    conn = get_db()
    cursor = conn.cursor(dictionary=dictionary)
    try:
        yield cursor
        if commit:
            conn.commit()
    except Exception:
        # Cualquier error: deshacer cambios y relanzar para que lo capture
        # el handler global de errores.
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()
