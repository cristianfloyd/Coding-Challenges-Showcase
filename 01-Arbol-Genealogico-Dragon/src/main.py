"""
Punto de entrada principal de la aplicación de árbol genealógico.

Este módulo inicializa el sistema de logging y orquesta
la ejecución de la aplicación siguiendo principios SOLID y Clean Code.
"""

import logging
import sys
from typing import TYPE_CHECKING

from .config import AppConfig
from .container import ApplicationContainer, ContainerProtocol
from .utils.logger import LoggerConfig
from .utils.output import ConsoleOutput, UserOutputInterface

if TYPE_CHECKING:
    from .interfaces import ArbolRepository, DataLoaderProtocol, UIProtocol

# Constantes
LOG_SEPARATOR_LENGTH = 70
APP_NAME = "Sistema de Árbol Genealógico"


def setup_application_logging(config: AppConfig | None = None) -> None:
    """
    Configura el logging de la aplicación al inicio.

    Args:
        config: Configuración de la aplicación. Si es None, se carga desde entorno.
    """
    if config is None:
        config = AppConfig.from_env()

    config.log_dir.mkdir(exist_ok=True)
    log_file = config.log_dir / config.log_file

    LoggerConfig.setup_logger(
        name="src",
        level=logging.INFO,
        log_file=log_file,
    )

    logger = logging.getLogger("src")
    _log_banner(logger, f"{APP_NAME} - Iniciado")
    logger.info(f"Logging configurado - Archivo: {log_file.absolute()}")


def _log_banner(logger: logging.Logger, message: str) -> None:
    """Registra un mensaje con banner decorativo."""
    separator = "=" * LOG_SEPARATOR_LENGTH
    logger.info(separator)
    logger.info(message)
    logger.info(separator)


def _initialize_dependencies(
    container: "ContainerProtocol",
) -> tuple["ArbolRepository", "DataLoaderProtocol", "UIProtocol"]:
    """
    Inicializa y retorna todas las dependencias necesarias.

    Args:
        container: Contenedor de dependencias.

    Returns:
        Tupla con (arbol, data_loader, ui)
    """
    arbol = container.get_arbol()
    data_loader = container.get_data_loader()
    ui = container.get_ui()
    return arbol, data_loader, ui


def _load_application_data(
    data_loader: "DataLoaderProtocol", arbol: "ArbolRepository", logger: logging.Logger
) -> None:
    """
    Carga los datos de demostración en el árbol.

    Args:
        data_loader: Cargador de datos.
        arbol: Repositorio del árbol genealógico.
        logger: Logger para registrar operaciones.
    """
    logger.info("Cargando datos de demostración...")
    data_loader.cargar_datos(arbol)
    logger.info(f"Datos cargados exitosamente: {len(arbol.personas)} personas registradas")


def _run_application_ui(ui: "UIProtocol", logger: logging.Logger) -> None:
    """
    Ejecuta la interfaz de usuario principal.

    Args:
        ui: Interfaz de usuario.
        logger: Logger para registrar operaciones.
    """
    logger.info("Inicializando interfaz de usuario...")
    ui.mostrar_menu_principal()


def _handle_user_interruption(logger: logging.Logger, output: UserOutputInterface | None) -> None:
    """Maneja la interrupción del usuario de forma elegante."""
    logger.info("Aplicación interrumpida por el usuario (Ctrl+C)")
    if output is None:
        output = ConsoleOutput()
    output.show_message("\n\n¡Hasta luego!")


def _handle_critical_error(
    error: Exception, logger: logging.Logger, output: UserOutputInterface | None
) -> None:
    """
    Maneja errores críticos mostrando mensaje al usuario y registrándolos.

    Args:
        error: Excepción ocurrida.
        logger: Logger para registrar el error.
        output: Output para mostrar mensajes al usuario (None para crear uno nuevo).
    """
    logger.exception(f"Error crítico en la aplicación: {error}")
    logger.error("La aplicación se cerrará debido a un error crítico")
    if output is None:
        output = ConsoleOutput()
    output.show_error(f"\nError crítico: {error}")
    output.show_message("Por favor, revisa el archivo de logs para más detalles.")


def _cleanup(logger: logging.Logger) -> None:
    """
    Ejecuta tareas de limpieza al finalizar la aplicación.

    Args:
        logger: Logger para registrar la finalización.
    """
    logger.debug("Ejecutando limpieza final...")
    _log_banner(logger, f"{APP_NAME} - Finalizado")


def main(config: AppConfig | None = None, container: ContainerProtocol | None = None) -> None:
    """Función principal que orquesta la ejecución de la aplicación.

    Esta función coordina:
    1. Configuración del sistema de logging
    2. Inicialización de dependencias
    3. Carga de datos
    4. Ejecución de la UI
    5. Manejo de errores y limpieza

    Args:
        config: Configuración de la aplicación. Si es None, se carga desde entorno.
        container: Contenedor de dependencias. Si es None, se crea una nueva instancia.
    Raises:
        SystemExit: Siempre termina con sys.exit() para indicar estado de salida.
    """
    setup_application_logging(config)
    logger = logging.getLogger(__name__)
    output: UserOutputInterface = ConsoleOutput()

    try:
        logger.info("Inicializando aplicación...")

        if container is None:
            container = ApplicationContainer()

        arbol, data_loader, ui = _initialize_dependencies(container)

        _load_application_data(data_loader, arbol, logger)
        _run_application_ui(ui, logger)

        logger.info("Aplicación finalizada normalmente")

    except KeyboardInterrupt:
        _handle_user_interruption(logger, output)
        sys.exit(0)

    except Exception as e:
        _handle_critical_error(e, logger, output)
        sys.exit(1)

    finally:
        _cleanup(logger)


if __name__ == "__main__":
    main()
