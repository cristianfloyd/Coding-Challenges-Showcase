from typing import TYPE_CHECKING
from unittest.mock import patch

import pytest

from src.data_loader import DataLoaderDemo
from src.exceptions import (
    ParejaNoExisteError,
    PersonaNoEncontradaError,
)
from src.models import Persona

if TYPE_CHECKING:
    from src.interfaces import ArbolRepository


def test_cargar_datos_crea_personas(arbol_vacio: "ArbolRepository"):
    """
    Test de integración: Verificar que cargar_datos puebla el árbol.

    Este test verifica que cualquier implementación de ArbolRepository
    puede ser utilizada con DataLoaderDemo.
    """
    # ARRANGE
    loader = DataLoaderDemo()

    # ACT
    loader.cargar_datos(arbol_vacio)

    # ASSERT
    assert len(arbol_vacio.personas) > 0
    # Verificar algunos personajes clave
    assert any(p.nombre == "Aegon I" for p in arbol_vacio.personas.values())
    assert any(p.nombre == "Rhaenyra" for p in arbol_vacio.personas.values())
    assert any(p.nombre == "Daemon" for p in arbol_vacio.personas.values())


def test_cargar_datos_establece_relaciones(arbol_vacio: "ArbolRepository"):
    """
    Test de integración: Verificar relaciones clave.
    """
    # ARRANGE
    loader = DataLoaderDemo()
    # ACT
    loader.cargar_datos(arbol_vacio)

    # Recuperar personas por nombre (helper simple para el test)
    def get_by_name(nombre: str) -> Persona | None:
        for p in arbol_vacio.personas.values():
            if p.nombre == nombre:
                return p
        return None

    aegon_i = get_by_name("Aegon I")
    aenys_i = get_by_name("Aenys I")
    viserys_i = get_by_name("Viserys I")
    rhaenyra = get_by_name("Rhaenyra")

    # Verificar relación Padre-Hijo (Aegon I -> Aenys I)
    assert aenys_i in aegon_i.hijos  # type: ignore
    assert aegon_i in aenys_i.padres

    # Verificar relación Padre-Hijo (Viserys I -> Rhaenyra)
    assert rhaenyra in viserys_i.hijos  # type: ignore
    assert viserys_i in rhaenyra.padres


def test_cargar_datos_maneja_parejas_complejas(arbol_vacio: "ArbolRepository"):
    """
    Test de integración: Verificar lógica compleja de parejas (Daemon y Rhaenyra).
    """
    loader = DataLoaderDemo()
    loader.cargar_datos(arbol_vacio)

    def get_by_name(nombre: str) -> Persona | None:
        for p in arbol_vacio.personas.values():
            if p.nombre == nombre:
                return p
        return None

    daemon = get_by_name("Daemon")
    rhaenyra = get_by_name("Rhaenyra")
    laena = get_by_name("Laena Velaryon")

    # Al final de la carga, Daemon debería estar casado con Rhaenyra
    assert daemon.pareja == rhaenyra  # type: ignore
    assert rhaenyra.pareja == daemon  # type: ignore

    # Y ya no con Laena
    assert laena.pareja is None  # type: ignore


def test_remover_pareja_seguro_maneja_error(arbol_vacio: "ArbolRepository"):
    """
    Test: _remover_pareja_seguro maneja errores de remove_pareja

    Verifica que si remove_pareja() lanza un error inesperado,
    _remover_pareja_seguro lo captura silenciosamente.
    """
    # ARRANGE
    loader = DataLoaderDemo()
    persona1 = arbol_vacio.registrar_persona("Persona 1")
    persona2 = arbol_vacio.registrar_persona("Persona 2")
    persona1.pareja = persona2  # Simular que son parejas

    # Simular que remove_pareja lanza un error
    with patch.object(
        arbol_vacio, "remove_pareja", side_effect=ParejaNoExisteError(persona1, persona2)
    ):
        # ACT
        loader._remover_pareja_seguro(arbol_vacio, persona1, persona2)  # type: ignore

        # ASSERT
        # Si no lanza excepción, el test pasa (el error fue capturado)
        assert True  # El éxito es que no lanzó excepción


def test_get_persona_lanza_error_si_no_existe(arbol_vacio: "ArbolRepository"):
    """
    Test: _get_persona lanza error si la persona no existe

    Verifica el manejo de errores cuando se busca una persona inexistente.
    """
    loader = DataLoaderDemo()
    # ARRANGE
    arbol_vacio.registrar_persona("Persona Existente")

    # ACT & ASSERT
    with pytest.raises(PersonaNoEncontradaError) as exc_info:
        loader._get_persona(arbol_vacio, "Persona Inexistente")  # type: ignore

    assert "Persona 'Persona Inexistente' no encontrada" in str(exc_info.value)
