"""
Tests para AppConfig.
"""

import os
from pathlib import Path
from unittest.mock import patch

from src.config import AppConfig


def test_app_config_from_env():
    """Verifica la carga de configuración desde variables de entorno."""
    with patch.dict(os.environ, {"LOG_DIR": "custom_logs", "LOG_FILE": "custom.log"}):
        config = AppConfig.from_env()
        assert config.log_dir == Path("custom_logs")
        assert config.log_file == "custom.log"


def test_app_config_defaults():
    """Verifica los valores por defecto."""
    config = AppConfig()
    assert config.log_dir == Path("logs")
    assert config.log_file == "arbol_genealogico.log"
