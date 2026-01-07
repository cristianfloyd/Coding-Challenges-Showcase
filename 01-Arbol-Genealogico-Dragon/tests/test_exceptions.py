"""
Tests para excepciones personalizadas.
"""

import pytest

from src.exceptions import PersonaNoEncontradaError, RelacionIncestuosaError


def test_persona_no_encontrada_default_message():
    """Verifica el mensaje por defecto cuando no se pasa ID ni mensaje."""
    exc = PersonaNoEncontradaError()
    assert str(exc) == "Persona no encontrada"


def test_relacion_incestuosa_invalid_type():
    """Verifica que se lance ValueError si el tipo de intento no es válido."""
    with pytest.raises(ValueError) as exc_info:
        RelacionIncestuosaError("A", "B", "tipo_invalido")  # type: ignore

    assert "tipo_intento debe ser uno de" in str(exc_info.value)
