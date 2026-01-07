import logging
from typing import Protocol


class UILoggerInterface(Protocol):
    """
    Interfaz para logging de UI usando Protocol (structural subtyping).

    Protocol permite definir una interfaz sin herencia explícita.
    Cualquier clase que implemente estos métodos será compatible.

    Dependency Inversion: dependemos de
    la abstracción (Protocol) no de la implementación concreta.

    Methods:
        debug: Registra un mensaje de debug
        info: Registra un mensaje informativo
        warning: Registra un mensaje de advertencia
        error: Registra un mensaje de error
        success: Registra un mensaje de éxito
    """

    def debug(self, message: str) -> None:
        """
        Registra un mensaje de debug.

        Args:
            message: Mensaje a registrar
        """
        ...  # pragma: no cover

    def info(self, message: str) -> None:
        """
        Registra un mensaje informativo.

        Args:
            message: Mensaje a registrar
        """
        ...  # pragma: no cover

    def warning(self, message: str) -> None:
        """
        Registra un mensaje de advertencia.

        Args:
            message: Mensaje de advertencia a registrar
        """
        ...  # pragma: no cover

    def error(self, message: str) -> None:
        """
        Registra un mensaje de error.

        Args:
            message: Mensaje de error a registrar
        """
        ...  # pragma: no cover

    def success(self, message: str) -> None:
        """
        Registra un mensaje de éxito.

        Args:
            message: Mensaje de éxito a registrar
        """
        ...  # pragma: no cover


class UILogger:
    """
    Implementación de logger para mensajes de UI.

    Encapsula la lógica de logging de UI, separando concerns
    entre presentación (UI) y logging técnico.

    Esta clase implementa UILoggerInterface y puede ser reemplazada
    por cualquier otra implementación que siga el Protocol.

    Attributes:
        _logger: Logger base de Python logging usado internamente
    """

    def __init__(self, logger: logging.Logger):
        """
        Inicializa el logger de UI.

        Args:
            logger: Logger base de Python logging. Debe estar configurado
                   previamente (usando LoggerConfig o get_logger).

        Example:
            >>> from src.utils.logger import get_logger
            >>> from src.utils.ui_logger import UILogger
            >>>
            >>> base_logger = get_logger(__name__)
            >>> ui_logger = UILogger(base_logger)
            >>> ui_logger.success("Operación exitosa")
        """
        self._logger = logger

    def info(self, message: str) -> None:
        """
        Registra un mensaje informativo.

        Usa el nivel INFO del logger base.

        Args:
            message: Mensaje informativo a registrar

        Example:
            >>> ui_logger.info("Cargando datos...")
        """
        self._logger.info(message)

    def debug(self, message: str) -> None:
        """
        Registra un mensaje de debug.

        Usa el nivel DEBUG del logger base. Estos mensajes son útiles
        para depuración y solo se muestran cuando el nivel de logging
        está configurado en DEBUG.

        Args:
            message: Mensaje de debug a registrar

        Example:
            >>> ui_logger.debug("Detalle técnico de la operación")
        """
        self._logger.debug(message)

    def warning(self, message: str) -> None:
        """
        Registra un mensaje de advertencia.

        Usa el nivel WARNING del logger base. Se usa para situaciones
        que requieren atención pero no son errores críticos.

        Args:
            message: Mensaje de advertencia a registrar

        Example:
            >>> ui_logger.warning("Operación completada con advertencias")
        """
        self._logger.warning(message)

    def error(self, message: str) -> None:
        """
        Registra un mensaje de error.

        Usa el nivel ERROR del logger base, que es apropiado
        para errores que requieren atención.

        Args:
            message: Mensaje de error a registrar

        Example:
            >>> ui_logger.error("No se pudo cargar el archivo")
        """
        self._logger.error(message)

    def success(self, message: str) -> None:
        """
        Registra un mensaje de éxito.

        Usa el nivel INFO pero con formato especial (✅) para
        distinguirlo visualmente en los logs. Esto permite filtrar
        mensajes de éxito en análisis posteriores.

        Args:
            message: Mensaje de éxito a registrar

        Example:
            >>> ui_logger.success("Persona registrada exitosamente")
        """
        # Usamos INFO porque "success" no es un nivel estándar de logging
        # pero agregamos el emoji para identificación visual
        self._logger.info(f"✅ {message}")


def create_ui_logger(logger_name: str = "src.ui") -> UILogger:
    """
    Función factory para crear un UILogger configurado.

    Esta función simplifica la creación de loggers de UI,
    encapsulando la lógica de inicialización.

    Args:
        logger_name: Nombre del logger base. Por defecto "src.ui"
                    para identificar logs provenientes de la UI.

    Returns:
        UILogger configurado y listo para usar.

    Example:
        >>> from src.utils.ui_logger import create_ui_logger
        >>>
        >>> ui_logger = create_ui_logger()
        >>> ui_logger.success("Bienvenido al sistema")
    """
    from .logger import get_logger  # ✅ Cambio: import relativo

    base_logger = get_logger(logger_name)
    return UILogger(base_logger)
