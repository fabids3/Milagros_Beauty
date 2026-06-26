"""
================================================================================
 app/services/configuracion_service.py — SERVICIO DE CONFIGURACIÓN
--------------------------------------------------------------------------------
 Capa: Lógica de negocio
================================================================================
"""

from app.repositories.configuracion_repository import ConfiguracionRepository
from app.errors.exceptions import DatosInvalidosError


class ConfiguracionService:

    @staticmethod
    def obtener_titulo() -> dict:
        config = ConfiguracionRepository.obtener()
        return {"titulo": config.titulo or "Milagro's Beauty"}

    @staticmethod
    def obtener_info_empresa() -> dict:
        config = ConfiguracionRepository.obtener()
        return {
            "sobre_nosotros": config.sobre_nosotros or "",
            "mision": config.mision or "",
            "vision": config.vision or "",
            "ubicacion": config.ubicacion or "",
        }

    @staticmethod
    def actualizar_titulo(titulo: str) -> None:
        if not titulo or not titulo.strip():
            raise DatosInvalidosError("El título no puede estar vacío")
        ConfiguracionRepository.actualizar_titulo(titulo.strip())

    @staticmethod
    def actualizar_info_empresa(data: dict) -> None:
        ConfiguracionRepository.actualizar_info(
            sobre_nosotros=data.get("sobre_nosotros", ""),
            mision=data.get("mision", ""),
            vision=data.get("vision", ""),
            ubicacion=data.get("ubicacion", ""),
        )