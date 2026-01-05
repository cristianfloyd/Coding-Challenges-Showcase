"""
House of the Dragon Genealogy System
"""

from .models import Persona
from .repository import ArbolGenealogico
from .ui import DinastiaUI

__all__ = [
    "Persona",
    "ArbolGenealogico",
    "DinastiaUI",
]

__version__ = "1.0.0"
__author__ = "Cristian Arenas"
