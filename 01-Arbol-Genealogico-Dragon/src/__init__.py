"""
House of the Dragon Genealogy System
"""

from .exceptions import (
    ArbolGenealogicoError,
    CicloTemporalError,
    EliminacionConDescendientesError,
    IDInvalidoError,
    LimitePadresExcedidoError,
    ParejaNoExisteError,
    PersonaNoEncontradaError,
    RelacionIncestuosaError,
    RelacionInvalidaError,
    ValidacionError,
)
from .models import Persona
from .repository import ArbolGenealogico
from .ui import DinastiaUI

__all__ = [
    "Persona",
    "ArbolGenealogico",
    "DinastiaUI",
    # Excepciones
    "ArbolGenealogicoError",
    "PersonaNoEncontradaError",
    "ValidacionError",
    "IDInvalidoError",
    "RelacionInvalidaError",
    "CicloTemporalError",
    "LimitePadresExcedidoError",
    "RelacionIncestuosaError",
    "ParejaNoExisteError",
    "EliminacionConDescendientesError",
]

__version__ = "1.0.0"
__author__ = "Cristian Arenas"
