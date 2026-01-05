"""
Tests para el módulo de logging de UI.

Estos tests verifican que el sistema de logging de UI
funciona correctamente siguiendo los principios SOLID.
"""

from unittest.mock import patch

from src.utils.logger import get_logger
from src.utils.ui_logger import UILogger, create_ui_logger


def test_create_ui_logger_creates_instance():
    """Test: create_ui_logger crea una instancia de UILogger"""
    ui_logger = create_ui_logger()
    assert isinstance(ui_logger, UILogger)


def test_ui_logger_info_logs_message():
    """Test: UILogger.info registra mensaje con nivel INFO"""
    base_logger = get_logger("test")
    ui_logger = UILogger(base_logger)

    # No debería lanzar excepción
    ui_logger.info("Mensaje informativo")


def test_ui_logger_error_logs_message():
    """Test: UILogger.error registra mensaje con nivel ERROR"""
    base_logger = get_logger("test")
    ui_logger = UILogger(base_logger)

    # No debería lanzar excepción
    ui_logger.error("Error en operación")


def test_ui_logger_success_logs_with_emoji():
    """Test: UILogger.success registra mensaje con emoji ✅"""
    base_logger = get_logger("test")
    ui_logger = UILogger(base_logger)

    # No debería lanzar excepción
    ui_logger.success("Operación exitosa")


def test_ui_logger_uses_correct_log_levels():
    """Test: UILogger usa los niveles de logging correctos"""
    base_logger = get_logger("test")

    # Mock del logger para verificar llamadas
    with (
        patch.object(base_logger, "info") as mock_info,
        patch.object(base_logger, "error") as mock_error,
    ):
        ui_logger = UILogger(base_logger)

        ui_logger.info("Info message")
        mock_info.assert_called_once_with("Info message")

        ui_logger.error("Error message")
        mock_error.assert_called_once_with("Error message")

        ui_logger.success("Success message")
        mock_info.assert_called_with("✅ Success message")
