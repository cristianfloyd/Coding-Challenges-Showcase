import os
from dataclasses import dataclass
from pathlib import Path


@dataclass
class AppConfig:
    log_dir: Path = Path("logs")
    log_file: str = "arbol_genealogico.log"

    @classmethod
    def from_env(cls) -> "AppConfig":
        """Carga configuración desde variables de entorno"""
        log_dir = Path(os.getenv("LOG_DIR", "logs"))
        log_file = os.getenv("LOG_FILE", "arbol_genealogico.log")
        return cls(log_dir=log_dir, log_file=log_file)
