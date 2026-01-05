# test_repository.py

from unittest.mock import MagicMock, patch

import pytest

from src.models import Persona
from src.repository import ArbolGenealogico
from src.visitors import PrintArbolVisitor, SearchArbolVisitor


def test_registrar_persona_exito(arbol_vacio: ArbolGenealogico):
    """
    Test: Registrar persona exitosamente

    Verifica que registrar_persona() crea una persona con el ID correcto
    y la almacena en el árbol.
    """
    # ARRANGE
    nombre = "Persona 1"

    # ACT
    persona = arbol_vacio.registrar_persona(nombre)

    # ASSERT
    assert persona.id == 1
    assert persona.nombre == nombre
    assert arbol_vacio.get_persona(1) == persona
    assert persona in arbol_vacio.personas.values()


@patch("src.repository.FamilyValidator.validar_id")
def test_registrar_persona_lanza_error_si_validacion_falla(
    mock_validar_id: MagicMock, arbol_vacio: ArbolGenealogico
):
    """
    Test: Registrar persona lanza error si validacion falla

    Verifica que registrar_persona() lanza ValueError si la validacion falla.
    """
    # ARRANGE
    mock_validar_id.side_effect = ValueError("ID INVALIDO")

    # ACT & ASSERT
    with pytest.raises(ValueError) as exc_info:
        arbol_vacio.registrar_persona("Persona No Valida")

    assert "Error al registrar persona: ID INVALIDO" in str(exc_info.value)


def test_registrar_persona_genera_ids_secuenciales(arbol_vacio: ArbolGenealogico):
    """
    Test: IDs secuenciales automáticos

    Verifica que cada persona registrada recibe un ID incremental.
    """
    # ARRANGE & ACT
    p1 = arbol_vacio.registrar_persona("Persona 1")
    p2 = arbol_vacio.registrar_persona("Persona 2")
    p3 = arbol_vacio.registrar_persona("Persona 3")

    # ASSERT
    assert p1.id == 1
    assert p2.id == 2
    assert p3.id == 3
    assert len(arbol_vacio.personas) == 3


def test_registrar_persona_incrementa_proximo_id(arbol_vacio: ArbolGenealogico):
    """
    Test: _proximo_id se incrementa correctamente

    Verifica que el contador interno se actualiza después de cada registro.
    """
    # ARRANGE & ACT
    p1 = arbol_vacio.registrar_persona("Persona 1")
    p2 = arbol_vacio.registrar_persona("Persona 2")

    # ASSERT
    assert p1.id == 1
    assert p2.id == 2
    # El próximo ID debería ser 3
    p3 = arbol_vacio.registrar_persona("Persona 3")
    assert p3.id == 3


# ==================== TESTS PARA get_persona ====================
def test_get_persona_existe(arbol_con_persona_simple: ArbolGenealogico):
    """
    Test: Obtener persona que existe

    Verifica que get_persona() retorna la persona correcta cuando existe.
    """
    # ARRANGE
    persona_id = 1

    # ACT
    persona = arbol_con_persona_simple.get_persona(persona_id)

    # ASSERT
    assert persona.id == persona_id
    assert persona.nombre == "Persona 1"


def test_get_persona_no_existe(arbol_vacio: ArbolGenealogico):
    """
    Test: Obtener persona que no existe

    Verifica que get_persona() lanza ValueError cuando la persona no existe.
    """
    # ARRANGE
    persona_id_inexistente = 999

    # ACT & ASSERT
    with pytest.raises(ValueError) as exc_info:
        arbol_vacio.get_persona(persona_id_inexistente)

    assert f"Persona con ID {persona_id_inexistente} no encontrada" in str(exc_info.value)


# ==================== TESTS PARA init_get_root ====================
def test_init_get_root_vacio(arbol_vacio: ArbolGenealogico):
    """
    Test: Raíces en árbol vacío

    Verifica que init_get_root() retorna lista vacía cuando no hay personas.
    """
    # ACT
    raices = arbol_vacio.init_get_root()

    # ASSERT
    assert raices == []
    assert len(raices) == 0


def test_init_get_root_encuentra_raices(arbol_con_datos: ArbolGenealogico):
    """
    Test: Raíces en árbol con datos

    Verifica que init_get_root() retorna las raíces correctas cuando hay personas.
    """
    # ACT
    raices = arbol_con_datos.init_get_root()

    # ASSERT
    assert len(raices) == 2
    nombre_raices = {r.nombre for r in raices}
    assert "Padre" in nombre_raices
    assert "Madre" in nombre_raices
    assert "Hijo" not in nombre_raices


def test_init_get_root_con_multiples_raices(arbol_con_multiples_raices: ArbolGenealogico):
    """
    Test: Múltiples raíces independientes

    Verifica que init_get_root() encuentra todas las raíces.
    """
    # ACT
    raices = arbol_con_multiples_raices.init_get_root()

    # ASSERT
    assert len(raices) == 2
    nombres_raices = {r.nombre for r in raices}
    assert "Raiz 1" in nombres_raices
    assert "Raiz 2" in nombres_raices


# ==================== TESTS PARA recorrer_arbol_completo ====================
def test_recorrer_arbol_completo_con_visitor(arbol_con_datos: ArbolGenealogico):
    """
    Test: Recorrer árbol completo con visitor

    Verifica que recorrer_arbol_completo() visita todas las raíces.
    """
    # ARRANGE
    visitor = PrintArbolVisitor()

    # ACT
    arbol_con_datos.recorrer_arbol_completo(visitor)
    resultado = visitor.get_resultado()

    # ASSERT
    assert "Padre" in resultado
    assert "Madre" in resultado
    assert "Hijo" in resultado
    assert len(resultado.split("\n")) == 3


def test_recorrer_arbol_completo_con_search_visitor(arbol_con_datos: ArbolGenealogico):
    """
    Test: Recorrer árbol con SearchVisitor

    Verifica que el visitor de búsqueda funciona correctamente.
    """
    # ARRANGE
    visitor = SearchArbolVisitor("Hijo")

    # ACT
    arbol_con_datos.recorrer_arbol_completo(visitor)
    resultados = visitor.obtener_resultado()

    # ASSERT
    assert len(resultados) == 1
    assert resultados[0].nombre == "Hijo"


def test_recorrer_arbol_vacio(arbol_vacio: ArbolGenealogico):
    """
    Test: Recorrer árbol vacío

    Verifica que recorrer_arbol_completo() no falla con árbol vacío.
    """
    # ARRANGE
    visitor = PrintArbolVisitor()

    # ACT
    arbol_vacio.recorrer_arbol_completo(visitor)
    resultado = visitor.get_resultado()

    # ASSERT
    assert resultado == "No hay personajes registrados."


# ==================== TESTS PARA add_hijo ====================
def test_add_hijo_exito(arbol_vacio: ArbolGenealogico):
    """
    Test: Agregar hijo exitosamente

    Verifica que add_hijo() establece la relación padre-hijo correctamente.
    """
    # ARRANGE
    padre = arbol_vacio.registrar_persona("Padre")
    hijo = arbol_vacio.registrar_persona("Hijo")

    # ACT
    arbol_vacio.add_hijo(padre, hijo)

    # ASSERT
    assert hijo in padre.hijos
    assert padre in hijo.padres
    assert hijo.padres[0] == padre or hijo.padres[1] == padre


def test_add_hijo_actualiza_padres_primer_slot(arbol_vacio: ArbolGenealogico):
    """
    Test: add_hijo actualiza el primer slot de padres

    Verifica que cuando el hijo no tiene padres, se asigna al primer slot.
    """
    # ARRANGE
    padre = arbol_vacio.registrar_persona("Padre")
    hijo = arbol_vacio.registrar_persona("Hijo")

    # ACT
    arbol_vacio.add_hijo(padre, hijo)

    # ASSERT
    assert hijo.padres[0] == padre
    assert hijo.padres[1] is None


def test_add_hijo_actualiza_padres_segundo_slot(arbol_vacio: ArbolGenealogico):
    """
    Test: add_hijo actualiza el segundo slot de padres

    Verifica que cuando el hijo ya tiene un padre, se asigna al segundo slot.
    """
    # ARRANGE
    padre1 = arbol_vacio.registrar_persona("Padre 1")
    padre2 = arbol_vacio.registrar_persona("Padre 2")
    hijo = arbol_vacio.registrar_persona("Hijo")

    # ACT
    arbol_vacio.add_hijo(padre1, hijo)
    arbol_vacio.add_hijo(padre2, hijo)

    # ASSERT
    assert hijo.padres[0] == padre1
    assert hijo.padres[1] == padre2
    assert hijo in padre1.hijos
    assert hijo in padre2.hijos


def test_add_hijo_lanza_error_si_validacion_falla(arbol_vacio: ArbolGenealogico):
    """
    Test: add_hijo lanza error cuando la validación falla

    Verifica que add_hijo() propaga errores de validación.
    """
    # ARRANGE
    persona = arbol_vacio.registrar_persona("Persona")

    # ACT & ASSERT
    # Intentar que una persona sea su propio padre (ciclo)
    with pytest.raises(ValueError) as exc_info:
        arbol_vacio.add_hijo(persona, persona)

    assert "Error al añadir hijo" in str(exc_info.value)


def test_add_hijo_bloquea_ciclo_temporal(arbol_vacio: ArbolGenealogico):
    """
    Test: add_hijo bloquea ciclos temporales

    Verifica que no se puede crear un ciclo padre-hijo.
    """
    # ARRANGE
    abuelo = arbol_vacio.registrar_persona("Abuelo")
    padre = arbol_vacio.registrar_persona("Padre")
    arbol_vacio.add_hijo(abuelo, padre)

    # ACT & ASSERT
    # Intentar que el padre sea padre del abuelo (ciclo)
    with pytest.raises(ValueError) as exc_info:
        arbol_vacio.add_hijo(padre, abuelo)

    assert "Error al añadir hijo" in str(exc_info.value)


# ==================== TESTS PARA add_pareja ====================


def test_add_pareja_exito(arbol_vacio: ArbolGenealogico):
    """
    Test: Agregar pareja exitosamente

    Verifica que add_pareja() establece la relación bidireccional correctamente.
    """
    # ARRANGE
    persona1 = arbol_vacio.registrar_persona("Persona 1")
    persona2 = arbol_vacio.registrar_persona("Persona 2")

    # ACT
    arbol_vacio.add_pareja(persona1, persona2)

    # ASSERT
    assert persona1.pareja == persona2
    assert persona2.pareja == persona1


def test_add_pareja_lanza_error_si_validacion_falla(arbol_vacio: ArbolGenealogico):
    """
    Test: add_pareja lanza error cuando la validación falla

    Verifica que add_pareja() propaga errores de validación.
    """
    # ARRANGE
    persona = arbol_vacio.registrar_persona("Persona")

    # ACT & ASSERT
    # Intentar que una persona sea su propia pareja
    with pytest.raises(ValueError) as exc_info:
        arbol_vacio.add_pareja(persona, persona)

    assert "Error al añadir pareja" in str(exc_info.value)


def test_add_pareja_bloquea_si_ya_tiene_pareja(arbol_vacio: ArbolGenealogico):
    """
    Test: add_pareja bloquea si ya tiene pareja

    Verifica que no se puede agregar una segunda pareja.
    """
    # ARRANGE
    persona1 = arbol_vacio.registrar_persona("Persona 1")
    persona2 = arbol_vacio.registrar_persona("Persona 2")
    persona3 = arbol_vacio.registrar_persona("Persona 3")
    arbol_vacio.add_pareja(persona1, persona2)

    # ACT & ASSERT
    # Intentar agregar una segunda pareja
    with pytest.raises(ValueError) as exc_info:
        arbol_vacio.add_pareja(persona1, persona3)

    assert "Error al añadir pareja" in str(exc_info.value)


# ==================== TESTS PARA remove_pareja ====================


def test_remove_pareja_exito(
    pareja_simple: tuple["Persona", "Persona"], arbol_vacio: ArbolGenealogico
):
    """
    Test: Remover pareja exitosamente

    Verifica que remove_pareja() elimina la relación bidireccional.
    """
    # ARRANGE
    persona1, persona2 = pareja_simple
    assert persona1.pareja == persona2
    assert persona2.pareja == persona1

    # ACT
    arbol_vacio.remove_pareja(persona1, persona2)

    # ASSERT
    assert persona1.pareja is None
    assert persona2.pareja is None


def test_remove_pareja_lanza_error_si_validacion_falla(arbol_vacio: ArbolGenealogico):
    """
    Test: remove_pareja lanza error cuando la validación falla

    Verifica que remove_pareja() propaga errores de validación.
    """
    # ARRANGE
    persona1 = arbol_vacio.registrar_persona("Persona 1")
    persona2 = arbol_vacio.registrar_persona("Persona 2")
    # No son parejas

    # ACT & ASSERT
    with pytest.raises(ValueError) as exc_info:
        arbol_vacio.remove_pareja(persona1, persona2)

    assert "Error al remover pareja" in str(exc_info.value)


# ==================== TESTS PARA eliminar_persona ====================


def test_eliminar_persona_exito(arbol_con_persona_simple: ArbolGenealogico):
    """
    Test: Eliminar persona sin relaciones

    Verifica que eliminar_persona() elimina la persona del árbol.
    """
    # ARRANGE
    persona_id = 1
    assert persona_id in arbol_con_persona_simple.personas

    # ACT
    arbol_con_persona_simple.eliminar_persona(persona_id)

    # ASSERT
    assert persona_id not in arbol_con_persona_simple.personas
    with pytest.raises(ValueError):
        arbol_con_persona_simple.get_persona(persona_id)


def test_eliminar_persona_no_existe(arbol_vacio: ArbolGenealogico):
    """
    Test: Eliminar persona que no existe

    Verifica que eliminar_persona() lanza error si la persona no existe.
    """
    # ARRANGE
    persona_id_inexistente = 999

    # ACT & ASSERT
    with pytest.raises(ValueError) as exc_info:
        arbol_vacio.eliminar_persona(persona_id_inexistente)

    assert f"Persona con ID {persona_id_inexistente} no encontrada" in str(exc_info.value)


def test_eliminar_persona_desvincula_pareja(arbol_con_datos: ArbolGenealogico):
    """
    Test: Eliminar persona desvincula su pareja

    Verifica que al eliminar una persona, su pareja queda sin pareja.
    """
    # ARRANGE
    padre = arbol_con_datos.get_persona(1)  # Padre
    madre = arbol_con_datos.get_persona(2)  # Madre (pareja de Padre)
    assert padre.pareja == madre
    assert madre.pareja == padre

    # ACT
    arbol_con_datos.eliminar_persona(padre.id, confirmar_rotura=True)

    # ASSERT
    assert madre.pareja is None
    assert padre.id not in arbol_con_datos.personas


def test_eliminar_persona_desvincula_padres(arbol_con_datos: ArbolGenealogico):
    """
    Test: Eliminar persona desvincula de sus padres

    Verifica que al eliminar una persona, se elimina de la lista de hijos de sus padres.
    """
    # ARRANGE
    padre = arbol_con_datos.get_persona(1)  # Padre
    hijo = arbol_con_datos.get_persona(3)  # Hijo
    assert hijo in padre.hijos

    # ACT
    arbol_con_datos.eliminar_persona(hijo.id)

    # ASSERT
    assert hijo not in padre.hijos
    assert hijo.id not in arbol_con_datos.personas


def test_eliminar_persona_desvincula_hijos(arbol_con_datos: ArbolGenealogico):
    """
    Test: Eliminar persona desvincula a sus hijos

    Verifica que al eliminar una persona, sus hijos quedan sin ese padre.
    """
    # ARRANGE
    padre = arbol_con_datos.get_persona(1)  # Padre
    hijo = arbol_con_datos.get_persona(3)  # Hijo
    assert padre in hijo.padres

    # ACT
    arbol_con_datos.eliminar_persona(padre.id, confirmar_rotura=True)

    # ASSERT
    # El hijo debería tener None en el slot donde estaba el padre
    assert padre not in hijo.padres
    # Verificar que el hijo aún existe pero sin ese padre
    assert hijo.id in arbol_con_datos.personas
    assert padre not in hijo.padres


def test_eliminar_persona_desvincula_hijos_primer_padre(arbol_vacio: ArbolGenealogico):
    """
    Test: Eliminar persona desvincula correctamente cuando hay dos padres

    Verifica que al eliminar un padre, solo se elimina de su slot específico.
    """
    # ARRANGE
    padre1 = arbol_vacio.registrar_persona("Padre 1")
    padre2 = arbol_vacio.registrar_persona("Padre 2")
    hijo = arbol_vacio.registrar_persona("Hijo")

    arbol_vacio.add_hijo(padre1, hijo)
    arbol_vacio.add_hijo(padre2, hijo)

    assert hijo.padres[0] == padre1
    assert hijo.padres[1] == padre2

    # ACT
    arbol_vacio.eliminar_persona(padre1.id, confirmar_rotura=True)

    # ASSERT
    assert hijo.padres[0] is None
    assert hijo.padres[1] == padre2  # El segundo padre se mantiene


def test_eliminar_persona_desvincula_hijos_segundo_padre(arbol_vacio: ArbolGenealogico):
    """
    Test: Eliminar persona desvincula correctamente cuando hay dos padres

    Verifica que al eliminar un padre, solo se elimina de su slot específico.
    """
    # ARRANGE
    padre1 = arbol_vacio.registrar_persona("Padre 1")
    padre2 = arbol_vacio.registrar_persona("Padre 2")
    hijo = arbol_vacio.registrar_persona("Hijo")

    arbol_vacio.add_hijo(padre1, hijo)
    arbol_vacio.add_hijo(padre2, hijo)

    assert hijo.padres[0] == padre1
    assert hijo.padres[1] == padre2
    assert hijo.padres[1].id == padre2.id  # type: ignore

    # ACT
    arbol_vacio.eliminar_persona(padre2.id, confirmar_rotura=True)

    # ASSERT
    assert hijo.padres[0] == padre1  # El primer padre se mantiene
    assert hijo.padres[0].id == padre1.id  # type: ignore
    assert hijo.padres[1] is None

    # Verificar que el hijo aún existe y tiene la relación correcta
    assert hijo in padre1.hijos
    assert padre2 not in hijo.padres


def test_eliminar_persona_lanza_error_si_tiene_hijos(arbol_con_datos: ArbolGenealogico):
    """
    Test: Eliminar persona con hijos sin confirmación

    Verifica que eliminar_persona() lanza error si tiene hijos y no se confirma.
    """
    # ARRANGE
    padre = arbol_con_datos.get_persona(1)  # Padre tiene un hijo
    assert len(padre.hijos) > 0

    # ACT & ASSERT
    with pytest.raises(ValueError) as exc_info:
        arbol_con_datos.eliminar_persona(padre.id, confirmar_rotura=False)

    assert "tiene descendientes" in str(exc_info.value)


def test_eliminar_persona_con_confirmacion(arbol_con_datos: ArbolGenealogico):
    """
    Test: Eliminar persona con hijos y confirmación

    Verifica que eliminar_persona() funciona cuando se confirma la eliminación.
    """
    # ARRANGE
    padre = arbol_con_datos.get_persona(1)  # Padre tiene un hijo
    assert len(padre.hijos) > 0

    # ACT
    arbol_con_datos.eliminar_persona(padre.id, confirmar_rotura=True)

    # ASSERT
    assert padre.id not in arbol_con_datos.personas
    # El hijo debería quedar sin ese padre
    hijo = arbol_con_datos.get_persona(3)
    assert padre not in hijo.padres


def test_eliminar_persona_sin_hijos_no_requiere_confirmacion(
    arbol_con_persona_simple: ArbolGenealogico,
):
    """
    Test: Eliminar persona sin hijos no requiere confirmación

    Verifica que se puede eliminar una persona sin hijos sin confirmación.
    """
    # ARRANGE
    persona_id = 1

    # ACT
    arbol_con_persona_simple.eliminar_persona(persona_id, confirmar_rotura=False)

    # ASSERT
    assert persona_id not in arbol_con_persona_simple.personas
