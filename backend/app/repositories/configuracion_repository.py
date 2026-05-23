"""
================================================================================
 app/repositories/configuracion_repository.py — REPOSITORIO DE CONFIGURACIÓN
--------------------------------------------------------------------------------
 Capa: Acceso a datos
--------------------------------------------------------------------------------
 La tabla `configuracion` es un singleton: siempre tiene id = 1.
 Aquí encapsulamos esa convención.
================================================================================
"""

from typing import Optional

from app.database import db_cursor
from app.models.configuracion import Configuracion


SINGLETON_ID = 1


class ConfiguracionRepository:

    @staticmethod
    def obtener() -> Configuracion:
        with db_cursor() as cursor:
            cursor.execute(
                "SELECT * FROM configuracion WHERE id = %s",
                (SINGLETON_ID,),
            )
            return Configuracion.from_row(cursor.fetchone())

    @staticmethod
    def actualizar_titulo(titulo: str) -> bool:
        with db_cursor(commit=True) as cursor:
            cursor.execute(
                "UPDATE configuracion SET titulo = %s WHERE id = %s",
                (titulo, SINGLETON_ID),
            )
            return cursor.rowcount > 0

    @staticmethod
    def actualizar_info(
        sobre_nosotros: str, mision: str, vision: str, ubicacion: str
    ) -> bool:
        with db_cursor(commit=True) as cursor:
            cursor.execute(
                """
                UPDATE configuracion
                SET sobre_nosotros = %s,
                    mision         = %s,
                    vision         = %s,
                    ubicacion      = %s
                WHERE id = %s
                """,
                (sobre_nosotros, mision, vision, ubicacion, SINGLETON_ID),
            )
            return cursor.rowcount > 0
