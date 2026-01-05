"""
Módulo de logging estructurado para el sistema de árbol genealógico.

Este módulo proporciona una configuración centralizada de logging
siguiendo principios SOLID y Clean Code.

Principios aplicados:
- Single Responsibility: LoggerConfig tiene una única responsabilidad
- Open/Closed: Extensible mediante configuración, sin modificar código
- Dependency Inversion: Depende de abstracciones (logging estándar de Python)
"""

import logging
import sys
from pathlib import Path
from typing import Optional


class LoggerConfig:
    """
    Configurador de logging siguiendo el principio de Single Responsibility.

    Esta clase tiene una única responsabilidad: configurar el sistema
    de logging de manera centralizada y reutilizable.

    Attributes:
        DEFAULT_LEVEL: Nivel de logging por defecto (INFO)
        DEFAULT_FORMAT: Formato estándar de los mensajes de log
        DEFAULT_DATE_FORMAT: Formato de fecha/hora para los logs
    """

    # Constantes de clase para configuración por defecto
    DEFAULT_LEVEL = logging.INFO
    DEFAULT_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    DEFAULT_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

    @staticmethod
    def setup_logger(
        name: str,
        level: int = DEFAULT_LEVEL,
        log_file: Optional[Path] = None,
        format_string: Optional[str] = None,
    ) -> logging.Logger:
        """
        Configura y retorna un logger con handlers para consola y archivo.

        Este método sigue el patrón Factory para crear loggers configurados.
        Implementa el principio Open/Closed: extensible mediante parámetros
        sin necesidad de modificar el código.

        Args:
            name: Nombre del logger (típicamente __name__ del módulo que lo llama).
                  El nombre ayuda a identificar el origen de los logs.
            level: Nivel de logging (logging.DEBUG, INFO, WARNING, ERROR, CRITICAL).
                   Por defecto INFO.
            log_file: Ruta opcional para guardar logs en archivo.
                     Si se proporciona, se crea el directorio si no existe.
            format_string: Formato personalizado para los mensajes (opcional).
                          Si no se proporciona, usa DEFAULT_FORMAT.

        Returns:
            Logger configurado y listo para usar. Si el logger ya existe
            y tiene handlers, retorna el existente (evita duplicación).

        Example:
            >>> # Logger básico (solo consola)
            >>> logger = LoggerConfig.setup_logger(__name__)
            >>> logger.info("Sistema iniciado")

            >>> # Logger con archivo
            >>> log_path = Path("logs/app.log")
            >>> logger = LoggerConfig.setup_logger(__name__, log_file=log_path)
            >>> logger.debug("Mensaje de debug")

            >>> # Logger con nivel personalizado
            >>> logger = LoggerConfig.setup_logger(__name__, level=logging.DEBUG)
        """
        logger = logging.getLogger(name)

        # Evitar duplicar handlers si el logger ya está configurado
        # Esto sigue el patrón Singleton para la configuración
        if logger.handlers:
            return logger

        logger.setLevel(level)

        # Crear formatter con formato personalizado o por defecto
        formatter = logging.Formatter(
            format_string or LoggerConfig.DEFAULT_FORMAT, datefmt=LoggerConfig.DEFAULT_DATE_FORMAT
        )

        # Handler para consola (siempre presente)
        # Usa sys.stdout en lugar de sys.stderr para compatibilidad
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # Handler para archivo (opcional)
        # El archivo siempre guarda en nivel DEBUG para tener historial completo
        if log_file:
            # Crear directorio si no existe (parents=True crea toda la jerarquía)
            log_file.parent.mkdir(parents=True, exist_ok=True)
            file_handler = logging.FileHandler(log_file, encoding="utf-8")
            file_handler.setLevel(logging.DEBUG)  # Archivo siempre DEBUG
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        return logger


def get_logger(name: str) -> logging.Logger:
    """
    Función de conveniencia para obtener un logger configurado.

    Esta función sigue el patrón Factory y simplifica el uso
    del logging en todo el proyecto. Es un wrapper alrededor de
    LoggerConfig.setup_logger() con valores por defecto.

    Args:
        name: Nombre del logger (usar __name__ del módulo que lo llama).
              Ejemplo: get_logger(__name__)

    Returns:
        Logger configurado con valores por defecto (nivel INFO, solo consola).

    Example:
        >>> from src.utils.logger import get_logger
        >>>
        >>> logger = get_logger(__name__)
        >>> logger.info("Operación completada")
        >>> logger.warning("Advertencia importante")
        >>> logger.error("Error en operación")

        >>> # En un módulo específico
        >>> # src/repository.py
        >>> from src.utils.logger import get_logger
        >>> logger = get_logger(__name__)  # logger.name = "src.repository"
    """
    return LoggerConfig.setup_logger(name)
