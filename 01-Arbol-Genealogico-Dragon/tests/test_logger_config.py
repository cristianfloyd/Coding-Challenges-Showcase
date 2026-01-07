"""
Tests para LoggerConfig.
"""

import logging
from pathlib import Path
from unittest.mock import MagicMock, patch

from src.utils.logger import LoggerConfig, get_logger


def test_setup_logger_singleton_behavior():
    """Verifica que si un logger ya tiene handlers, no se agregan más."""
    name = "singleton_test"
    logger = logging.getLogger(name)
    mock_handler = MagicMock(spec=logging.Handler)
    logger.addHandler(mock_handler)

    result = LoggerConfig.setup_logger(name)

    assert result == logger
    assert len(result.handlers) == 1


def test_setup_logger_with_file(tmp_path: Path):
    """Verifica la creación de un logger con handler de archivo."""
    log_file = tmp_path / "subdir" / "test.log"
    name = "file_logger_test"

    logger = LoggerConfig.setup_logger(name, log_file=log_file)

    assert log_file.exists()
    assert any(isinstance(h, logging.FileHandler) for h in logger.handlers)

    # Limpieza para que otros tests no hereden este logger
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)


def test_get_logger_convenience():
    """Verifica la función get_logger."""
    with patch("src.utils.logger.LoggerConfig.setup_logger") as mock_setup:
        get_logger("test_name")
        mock_setup.assert_called_once_with("test_name")
