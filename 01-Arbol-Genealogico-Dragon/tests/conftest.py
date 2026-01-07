from typing import Callable
from unittest.mock import Mock

import pytest

from src.models import Persona
from src.repository import ArbolGenealogico
from src.validators import FamilyValidator


@pytest.fixture
def arbol_vacio() -> ArbolGenealogico:
    """
    Fixture: Árbol Genealógico Vacío

    Retorna un ArbolGenealogico sin personas registradas.
    """
    return ArbolGenealogico()


@pytest.fixture
def arbol_con_persona_simple(arbol_vacio: ArbolGenealogico) -> ArbolGenealogico:
    """
    Fixture: Árbol con una persona simple (sin relaciones)

    Estructura:
    - Persona 1 (id: 1, nombre: "Persona 1")
    """
    arbol_vacio.registrar_persona("Persona 1")
    return arbol_vacio


@pytest.fixture
def arbol_con_datos(arbol_vacio: ArbolGenealogico) -> ArbolGenealogico:
    """
    Fixture: Árbol con estructura básica de relaciones

    Estructura:
    - Padre (id: 1)
    - Madre (id: 2) <- pareja de Padre
    - Hijo (id: 3) <- hijo de Padre y Madre
    """
    padre = arbol_vacio.registrar_persona("Padre")
    madre = arbol_vacio.registrar_persona("Madre")
    hijo = arbol_vacio.registrar_persona("Hijo")

    arbol_vacio.add_pareja(padre, madre)
    arbol_vacio.add_hijo(padre, hijo)
    arbol_vacio.add_hijo(madre, hijo)

    return arbol_vacio


@pytest.fixture
def arbol_completo(arbol_vacio: ArbolGenealogico) -> ArbolGenealogico:
    """
    Fixture: Árbol con múltiples generaciones

    Estructura:
    - Abuelo (id: 1)
    - Abuela (id: 2) <- pareja de Abuelo
    - Padre (id: 3) <- hijo de Abuelo y Abuela
    - Madre (id: 4) <- pareja de Padre
    - Hijo (id: 5) <- hijo de Padre y Madre
    - Hija (id: 6) <- hija de Padre y Madre
    """
    abuelo = arbol_vacio.registrar_persona("Abuelo")
    abuela = arbol_vacio.registrar_persona("Abuela")
    padre = arbol_vacio.registrar_persona("Padre")
    madre = arbol_vacio.registrar_persona("Madre")
    hijo = arbol_vacio.registrar_persona("Hijo")
    hija = arbol_vacio.registrar_persona("Hija")

    # Relaciones
    arbol_vacio.add_pareja(abuelo, abuela)
    arbol_vacio.add_hijo(abuelo, padre)
    arbol_vacio.add_hijo(abuela, padre)

    arbol_vacio.add_pareja(padre, madre)
    arbol_vacio.add_hijo(padre, hijo)
    arbol_vacio.add_hijo(madre, hijo)
    arbol_vacio.add_hijo(padre, hija)
    arbol_vacio.add_hijo(madre, hija)

    return arbol_vacio


@pytest.fixture
def arbol_con_multiples_raices(arbol_vacio: ArbolGenealogico) -> ArbolGenealogico:
    """
    Fixture: Árbol con múltiples raíces independientes

    Estructura:
    - Raiz 1 (id: 1)
    - Raiz 2 (id: 2)
    """
    raiz1 = arbol_vacio.registrar_persona("Raiz 1")
    raiz2 = arbol_vacio.registrar_persona("Raiz 2")
    hijo1 = arbol_vacio.registrar_persona("Hijo 1")
    hijo2 = arbol_vacio.registrar_persona("Hijo 2")
    arbol_vacio.add_hijo(raiz1, hijo1)
    arbol_vacio.add_hijo(raiz2, hijo2)

    return arbol_vacio


# ==================== FIXTURES DE PERSONAS ====================


@pytest.fixture
def persona_simple() -> Persona:
    """
    Fixture: Persona simple sin relaciones

    Retorna una Persona con id=1, nombre="Persona Test"
    sin pareja, padres ni hijos.
    """
    return Persona(1, "Persona Test")


@pytest.fixture
def persona_con_hijos(arbol_vacio: ArbolGenealogico) -> tuple[Persona, Persona, Persona]:
    """
    Fixture: Persona con hijos

    Retorna una tupla (padre, hijo1, hijo2) donde:
    - padre tiene 2 hijos
    - Los hijos están registrados en el árbol
    """
    padre = arbol_vacio.registrar_persona("Padre")
    hijo1 = arbol_vacio.registrar_persona("Hijo 1")
    hijo2 = arbol_vacio.registrar_persona("Hijo 2")

    arbol_vacio.add_hijo(padre, hijo1)
    arbol_vacio.add_hijo(padre, hijo2)

    return (padre, hijo1, hijo2)


@pytest.fixture
def pareja_simple(arbol_vacio: ArbolGenealogico) -> tuple[Persona, Persona]:
    """
    Fixture: Pareja simple

    Retorna una tupla (persona1, persona2) donde:
    - Ambas están registradas en el árbol
    - Están relacionadas como pareja
    """
    persona1 = arbol_vacio.registrar_persona("Persona 1")
    persona2 = arbol_vacio.registrar_persona("Persona 2")

    arbol_vacio.add_pareja(persona1, persona2)

    return (persona1, persona2)


@pytest.fixture
def familia_completa(arbol_vacio: ArbolGenealogico) -> dict[str, Persona]:
    """
    Fixture: Familia completa con todas las relaciones

    Retorna un diccionario con las siguientes claves:
    - 'padre': Persona padre
    - 'madre': Persona madre (pareja del padre)
    - 'hijo': Persona hijo (hijo de padre y madre)
    - 'hija': Persona hija (hija de padre y madre)

    Todas las personas están registradas en el árbol con sus relaciones.
    """
    padre = arbol_vacio.registrar_persona("Padre")
    madre = arbol_vacio.registrar_persona("Madre")
    hijo = arbol_vacio.registrar_persona("Hijo")
    hija = arbol_vacio.registrar_persona("Hija")

    arbol_vacio.add_pareja(padre, madre)
    arbol_vacio.add_hijo(padre, hijo)
    arbol_vacio.add_hijo(madre, hijo)
    arbol_vacio.add_hijo(padre, hija)
    arbol_vacio.add_hijo(madre, hija)

    return {
        "padre": padre,
        "madre": madre,
        "hijo": hijo,
        "hija": hija,
    }


# ==================== FIXTURES DE VALIDADORES ====================
@pytest.fixture
def validador_vacio() -> FamilyValidator:
    """Validador con diccionario vacío."""
    return FamilyValidator({})


@pytest.fixture
def validador_con_persona() -> FamilyValidator:
    """Validador con una persona preexistente."""
    return FamilyValidator({1: Persona(1, "Persona 1")})


# ==================== FIXTURES DE FACTORY ====================
@pytest.fixture
def persona_mock_factory() -> (
    Callable[
        [
            int,
            str,
            Persona | None,
            tuple[Persona | None, Persona | None],
            list[Persona] | None,
        ],
        Persona,
    ]
):
    """Factory para crear mocks de Persona de forma consistente."""

    def _create_persona_mock(
        persona_id: int,
        nombre: str,
        pareja: Persona | None = None,
        padres: tuple[Persona | None, Persona | None] = (None, None),
        hijos: list[Persona] | None = None,
    ):
        return Mock(
            id=persona_id,
            nombre=nombre,
            pareja=pareja,
            padres=padres,
            hijos=hijos or [],
        )

    return _create_persona_mock
