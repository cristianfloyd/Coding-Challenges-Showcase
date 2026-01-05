from src.models import Persona


def test_persona_str_repr():
    p = Persona(1, "Viserys")

    # Esto ejecuta la línea 25
    assert str(p) == "Viserys (1)"
    # Esto ejecuta la línea 28 (que llama a la 25)
    assert repr(p) == "Viserys (1)"


def test_persona_accept_visitor():
    from unittest.mock import Mock

    p = Persona(1, "Test")
    visitor = Mock()
    p.accept_visitor(visitor)
    visitor.visitar.assert_called_once_with(p)
