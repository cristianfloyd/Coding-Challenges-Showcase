"""
Punto de entrada principal de la aplicación de árbol genealógico.

Este módulo inicializa el sistema de logging y orquesta
la ejecución de la aplicación.
"""

import logging
import sys
from pathlib import Path

from .container import ApplicationContainer
from .utils.logger import LoggerConfig


def setup_application_logging(log_dir: Path = Path("logs")) -> None:
    """
    Configura el logging de la aplicación al inicio.

    Esta función centraliza la configuración de logging siguiendo
    el principio de Single Responsibility. Configura:
    - Logger raíz del paquete 'src'
    - Handler para consola (nivel INFO)
    - Handler para archivo (nivel DEBUG, con historial completo)

    El archivo de log se guarda en logs/arbol_genealogico.log
    """
    # Crear directorio de logs si no existe
    log_dir.mkdir(exist_ok=True)

    # Ruta del archivo de log
    log_file = log_dir / "arbol_genealogico.log"

    # Configurar el logger raíz del paquete 'src'
    # Esto afectará a todos los loggers que empiecen con 'src.'
    LoggerConfig.setup_logger(
        name="src",
        level=logging.INFO,  # Nivel INFO por defecto para consola
        log_file=log_file,  # Archivo con historial completo (DEBUG)
    )

    logger = logging.getLogger("src")
    logger.info("=" * 70)
    logger.info("Sistema de Árbol Genealógico - Iniciado")
    logger.info("=" * 70)
    logger.info(f"Logging configurado - Archivo: {log_file.absolute()}")


def main():
    """
    Función principal que orquesta la ejecución de la aplicación.

    Esta función:
    1. Configura el sistema de logging
    2. Crea el árbol genealógico
    3. Carga los datos de demostración
    4. Inicializa la UI
    5. Maneja errores críticos y cierre elegante

    Raises:
        SystemExit: En caso de error crítico o cierre normal
    """
    # Configurar logging al inicio
    setup_application_logging()

    # Obtener logger para este módulo
    logger = logging.getLogger(__name__)

    try:
        logger.info("Inicializando aplicación...")

        # Crear árbol genealógico
        container = ApplicationContainer()
        arbol =container.get_arbol()
        data_loader = container.get_data_loader()
        ui = container.get_ui()

        # carga de datos
        logger.info("Cargando datos de demostración...")
        data_loader.cargar_datos(arbol)
        logger.info(f"Datos cargados exitosamente: {len(arbol.personas)} personas registradas")

        # Inicializar UI
        logger.info("Inicializando interfaz de usuario...")
        ui.mostrar_menu_principal()

        logger.info("Aplicación finalizada normalmente")

    except KeyboardInterrupt:
        # Manejar interrupción del usuario (Ctrl+C)
        logger.info("Aplicación interrumpida por el usuario (Ctrl+C)")
        print("\n\n¡Hasta luego!")
        sys.exit(0)

    except Exception as e:
        # Manejar errores críticos no esperados
        logger.exception(f"Error crítico en la aplicación: {e}")
        logger.error("La aplicación se cerrará debido a un error crítico")
        print(f"\nError crítico: {e}")
        print("Por favor, revisa el archivo de logs para más detalles.")
        sys.exit(1)

    finally:
        # Código de limpieza (si es necesario en el futuro)
        logger.debug("Ejecutando limpieza final...")
        logger.info("=" * 70)
        logger.info("Sistema de Árbol Genealógico - Finalizado")
        logger.info("=" * 70)


if __name__ == "__main__":
    main()
