"""
Tests para el módulo main.py

Verifica la orquestación principal de la aplicación y el manejo de errores.
"""

import logging
from unittest.mock import MagicMock, patch

from src.config import AppConfig
from src.main import (
    _handle_critical_error,  # type: ignore
    _handle_user_interruption,  # type: ignore
    main,
    setup_application_logging,
)


@patch("src.main.ApplicationContainer")
@patch("src.main.setup_application_logging")
def test_main_flujo_completo(mock_setup_logging: MagicMock, mock_container_cls: MagicMock):
    """
    Test: Flujo principal de la aplicación

    Verifica que main() orquesta correctamente los componentes.
    """
    # ARRANGE
    mock_container_instance = mock_container_cls.return_value
    mock_arbol = MagicMock()
    mock_arbol.personas = {}
    mock_data_loader = MagicMock()
    mock_ui = MagicMock()

    mock_container_instance.get_arbol.return_value = mock_arbol
    mock_container_instance.get_data_loader.return_value = mock_data_loader
    mock_container_instance.get_ui.return_value = mock_ui

    # ACT
    main()

    # ASSERT
    mock_setup_logging.assert_called_once()
    mock_container_cls.assert_called_once()
    mock_data_loader.cargar_datos.assert_called_once_with(mock_arbol)
    mock_ui.mostrar_menu_principal.assert_called_once()


@patch("sys.exit")
@patch("src.main.ApplicationContainer")
@patch("src.main.setup_application_logging")
def test_main_keyboard_interrupt(
    mock_setup_logging: MagicMock, mock_container_cls: MagicMock, mock_exit: MagicMock
):
    """Verifica que KeyboardInterrupt se recoja y termine con éxito (0)."""
    # ARRANGE
    mock_container_instance = mock_container_cls.return_value
    mock_container_instance.get_arbol.side_effect = KeyboardInterrupt

    # ACT
    main()

    # ASSERT
    mock_exit.assert_called_once_with(0)


@patch("sys.exit")
@patch("src.main.ApplicationContainer")
@patch("src.main.setup_application_logging")
def test_main_generic_exception(
    mock_setup_logging: MagicMock, mock_container_cls: MagicMock, mock_exit: MagicMock
):
    """Verifica que excepciones genéricas terminen con error (1)."""
    # ARRANGE
    mock_container_instance = mock_container_cls.return_value
    mock_container_instance.get_arbol.side_effect = Exception("Test Error")

    # ACT
    main()

    # ASSERT
    mock_exit.assert_called_once_with(1)


@patch("src.main.AppConfig.from_env")
@patch("src.main.LoggerConfig.setup_logger")
def test_setup_application_logging_defaults(mock_setup: MagicMock, mock_from_env: MagicMock):
    """Verifica setup_application_logging cuando no se pasa configuración."""
    # ARRANGE
    mock_config = MagicMock(spec=AppConfig)
    mock_config.log_dir = MagicMock()
    mock_config.log_file = "test.log"
    mock_from_env.return_value = mock_config

    # ACT
    setup_application_logging(None)

    # ASSERT
    mock_from_env.assert_called_once()
    mock_setup.assert_called_once()


def test_handle_user_interruption_no_output():
    """Verifica el manejo de interrupción sin objeto output previo."""
    logger = MagicMock(spec=logging.Logger)
    with patch("src.main.ConsoleOutput") as mock_console:
        _handle_user_interruption(logger, None)
        mock_console.return_value.show_message.assert_called_once()


def test_handle_critical_error_no_output():
    """Verifica el manejo de error crítico sin objeto output previo."""
    logger = MagicMock(spec=logging.Logger)
    error = Exception("Fatal")
    with patch("src.main.ConsoleOutput") as mock_console:
        _handle_critical_error(error, logger, None)
        mock_console.return_value.show_error.assert_called_once()
