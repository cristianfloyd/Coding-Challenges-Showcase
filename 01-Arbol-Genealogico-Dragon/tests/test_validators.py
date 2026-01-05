from unittest.mock import Mock

import pytest

from src.validators import FamilyValidator


@pytest.fixture
def validador_vacio() -> FamilyValidator:
    """
    Fixture: Validador Vacio
    Retorna un validador con un diccionario vacío.
    """
    return FamilyValidator({})


@pytest.fixture
def validador_con_persona() -> FamilyValidator:
    """
    Fixture: Validador con una Persona
    Retorna un validador con un diccionario con una persona.
    """
    return FamilyValidator({1: Mock(id=1, nombre="Persona 1", pareja=None, padres=[None, None])})


# ================= validar_pareja start =================
def test_validar_pareja_exito(validador_vacio: FamilyValidator):
    """
    Test: Validación exitosa de relación de pareja.

    Verifica que validar() no lance error cuando:
    - Ambas personas tienen IDs diferentes
    - Ninguna tiene pareja asignada
    - No existe relación padre-hijo entre ellas

    Expected: No se lanza excepción.
    """
    # ═══════════════════════════════════════════════════
    # ARRANGE (Preparar)
    # ═══════════════════════════════════════════════════
    validator = validador_vacio

    mock_persona1 = Mock(id=1, nombre="Persona 1", pareja=None, padres=[None, None])
    mock_persona2 = Mock(id=2, nombre="Persona 2", pareja=None, padres=[None, None])

    # ═══════════════════════════════════════════════════
    # ACT (Actuar)
    # ═══════════════════════════════════════════════════
    validator.validar(mock_persona1, mock_persona2, "pareja")

    # ═══════════════════════════════════════════════════
    # ASSERT (Verificar)
    # ═══════════════════════════════════════════════════
    # si no lanza error, es porque esta bien


def test_validar_pareja_fallido(validador_vacio: FamilyValidator):
    """
    Test: Negativo
    Que validar_pareja() lance error cuando le pasamos una persona que no puede ser pareja.
    """
    # ═══════════════════════════════════════════════════
    # ARRANGE (Preparar)
    # ═══════════════════════════════════════════════════
    validator = validador_vacio

    mock_persona1 = Mock(id=1, nombre="Persona 1", pareja=None)

    # ═══════════════════════════════════════════════════
    # ACT (Actuar)
    # ═══════════════════════════════════════════════════
    with pytest.raises(ValueError) as e:
        validator.validar(mock_persona1, mock_persona1, "pareja")

    # ═══════════════════════════════════════════════════
    # ASSERT (Verificar)
    # ═══════════════════════════════════════════════════
    assert str(e.value) == "Persona 1 no puede ser su propia pareja"


# test para persona1 tiene pareja y persona2 no tiene pareja
def test_validar_pareja_falla_si_persona1_tiene_pareja(
    validador_con_persona: FamilyValidator,
):
    """
    Test: Negativo
    Que validar_pareja() lance error cuando le pasamos una persona que ya tiene pareja.
    """
    # ═══════════════════════════════════════════════════
    # ARRANGE (Preparar)
    # ═══════════════════════════════════════════════════
    validator = validador_con_persona

    mock_persona2 = Mock(id=2, nombre="Persona 2", pareja=None)
    mock_persona1 = Mock(id=1, nombre="Persona 1", pareja=mock_persona2)

    # ═══════════════════════════════════════════════════
    # ACT (Actuar)
    # ═══════════════════════════════════════════════════
    with pytest.raises(ValueError) as e:
        validator.validar(mock_persona1, mock_persona2, "pareja")

    # ═══════════════════════════════════════════════════
    # ASSERT (Verificar)
    # ═══════════════════════════════════════════════════
    assert (
        str(e.value)
        == f"{mock_persona1.nombre} ya tiene una pareja: {mock_persona1.pareja.nombre}."
    )


# test para persona2 tiene pareja
def test_validar_pareja_falla_si_persona2_tiene_pareja(
    validador_con_persona: FamilyValidator,
):
    """
    Test: Negativo
    Que validar_pareja() lance error cuando le pasamos una persona que ya tiene pareja.
    """
    validator = validador_con_persona
    mock_persona1 = Mock(id=1, nombre="Persona 1", pareja=None)
    mock_persona2 = Mock(id=2, nombre="Persona 2", pareja=mock_persona1)

    with pytest.raises(ValueError) as e:
        validator.validar(mock_persona1, mock_persona2, "pareja")

    assert (
        str(e.value)
        == f"{mock_persona2.nombre} ya tiene una pareja: {mock_persona2.pareja.nombre}."
    )


def test_validar_pareja_bloquea_incesto_padre_hijo(validador_vacio: FamilyValidator):
    """
    Test: Prevención de incesto - Padre intenta ser pareja de hijo

    Escenario:
    Juan es padre de María
    Intentamos: Juan <-> María
    Resultado: ERROR (incesto)
    """
    # ARRANGE
    # María es hija de Juan
    juan = Mock(id=1, nombre="Juan", padres=[None, None], pareja=None)
    maria = Mock(id=2, nombre="María", padres=[juan, None], pareja=None)

    # ACT & ASSERT
    with pytest.raises(ValueError) as e:
        validador_vacio.validar(juan, maria, "pareja")
    # Verificar si persona2 es padre/madre de persona1
    with pytest.raises(ValueError) as e:
        validador_vacio.validar(maria, juan, "pareja")

    assert "es padre/madre de" in str(e.value)
    assert f"{juan.nombre} es padre/madre de {maria.nombre}. " in str(e.value)


# ═══════════════════════════════════════════════════


# ================= validar_id start =================
def test_validar_id_acepta_id_valido(validador_vacio: FamilyValidator):
    """
    Test: ¿Qué estamos probando?
    Que validar_id() NO lance error cuando le pasamos un ID válido.
    """
    # ═══════════════════════════════════════════════════
    # ARRANGE (Preparar)
    # ═══════════════════════════════════════════════════
    validator = validador_vacio
    id_nuevo = 2  # Un ID válido (positivo, no existe)

    # ═══════════════════════════════════════════════════
    # ACT (Actuar)
    # ═══════════════════════════════════════════════════
    validator.validar_id(id_nuevo)

    # ═══════════════════════════════════════════════════
    # ASSERT (Verificar)
    # ═══════════════════════════════════════════════════
    # El éxito es que NO lanzó excepción.
    # pytest considera que el test pasó si no hubo excepciones.


@pytest.mark.parametrize(
    "id_input, error_esperado_match",
    [
        (None, "no puede ser nulo"),  # Caso 1: None
        (-1, "entero positivo"),  # Caso 2: Negativo
        (1, "ya pertenece a otra persona"),  # Caso 3: Duplicado
    ],
)
def test_validar_id_casos_error(
    id_input: int, error_esperado_match: str, validador_con_persona: FamilyValidator
):
    """
    Test: Parametrizado: Prueba multiples escenarios
    Que validar_id() lance error cuando le pasamos un id nulo.
    """
    # ARRANGE
    validator = validador_con_persona

    # ACT
    with pytest.raises(ValueError) as e:
        validator.validar_id(id_input)

    # ASSERT
    assert error_esperado_match in str(e.value)


# ================= validar_id end =================


# ================= validar_remover_pareja start =================
def test_validar_remover_pareja_exito(validador_con_persona: FamilyValidator):
    """
    Test: Positivo
    Que validar_remover_pareja() no lance error cuando le pasamos una persona que tiene una pareja.
    """
    validator = validador_con_persona
    mock_persona1 = Mock(id=1, nombre="Persona 1")
    mock_persona2 = Mock(id=2, nombre="Persona 2", pareja=mock_persona1)
    mock_persona1.pareja = mock_persona2

    validator.validar(mock_persona1, mock_persona2, "remover_pareja")


def test_validar_remover_pareja_fallido(validador_vacio: FamilyValidator):
    """
    Test: Negativo
    Que validar_remover_pareja() lance error cuando le pasamos una persona que no tiene una pareja.
    """
    validator = validador_vacio
    mock_persona1 = Mock(id=1, nombre="Persona 1")
    mock_persona2 = Mock(id=2, nombre="Persona 2")
    nombre1 = mock_persona1.nombre
    nombre2 = mock_persona2.nombre

    with pytest.raises(ValueError) as e:
        validator.validar(mock_persona1, mock_persona2, "remover_pareja")

    assert str(e.value) == f"Error al validar remover pareja: {nombre1} y {nombre2} no son pareja"


def test_validar_remover_pareja_fallido_uno_no_tiene_pareja(
    validador_vacio: FamilyValidator,
):
    """
    Test: Negativo
    Que validar_remover_pareja() lance error cuando le pasamos una persona que no tiene una pareja.
    """
    validator = validador_vacio
    mock_persona1 = Mock(id=1, nombre="Persona 1", pareja=None)
    mock_persona2 = Mock(id=2, nombre="Persona 2", pareja=mock_persona1)
    nombre1 = mock_persona1.nombre
    nombre2 = mock_persona2.nombre
    with pytest.raises(ValueError) as e:
        validator.validar(mock_persona1, mock_persona2, "remover_pareja")

    assert str(e.value) == f"Error al validar remover pareja: {nombre1} o {nombre2} no tiene pareja"


# ================= validar_hijo start =================
def test_validar_hijo_exito(validador_vacio: FamilyValidator):
    """
    Test: Positivo
    Escenario:
    - Juan no tiene hijos
    - María no tiene padres
    - No son pareja
    - No hay ciclos

    Resultado: Asignación exitosa
    """
    juan = Mock(id=1, nombre="Juan", padres=[None, None], pareja=None)
    maria = Mock(id=2, nombre="María", padres=[None, None], pareja=None)

    # No debería lanzar error
    validador_vacio.validar(juan, maria, "hijo")


def test_validar_hijo_permite_segundo_padre(validador_vacio: FamilyValidator):
    """
    Test Positivo: Permite agregar segundo padre cuando solo hay uno

    Escenario:
    - María tiene 1 padre (Juan)
    - Intentamos agregar a Ana como segunda madre

    Resultado: Éxito (se permite)
    """
    juan = Mock(id=1, nombre="Juan", padres=[None, None], pareja=None)
    maria = Mock(id=2, nombre="María", padres=[juan, None], pareja=None)
    ana = Mock(id=3, nombre="Ana", padres=[None, None], pareja=None)

    # No debería lanzar error
    validador_vacio.validar(ana, maria, "hijo")


def test_validar_hijo_permite_hermanos(validador_vacio: FamilyValidator):
    """
    Test Positivo: Permite que dos personas tengan el mismo padre (hermanos)

    Escenario:
    Juan -> Padre de María
    Juan -> Padre de Pedro
    Resultado: Éxito (hermanos válidos)
    """
    juan = Mock(id=1, nombre="Juan", padres=[None, None], pareja=None)
    maria = Mock(id=2, nombre="María", padres=[None, None], pareja=None)
    pedro = Mock(id=3, nombre="Pedro", padres=[None, None], pareja=None)

    # No debería lanzar error
    validador_vacio.validar(juan, maria, "hijo")
    validador_vacio.validar(juan, pedro, "hijo")


def test_validar_hijo_detecta_ciclo_simple(validador_vacio: FamilyValidator):
    """
    A -> B
    Intentamos que B sea padre de A (ciclo simple)
    """
    abuelo = Mock(id=1, nombre="Abuelo", padres=[None, None])
    padre = Mock(id=2, nombre="Padre", padres=[abuelo, None])

    with pytest.raises(ValueError) as e:
        validador_vacio.validar(padre, abuelo, "hijo")

    assert "Paradoja temporal" in str(e.value)


def test_validar_hijo_no_puede_ser_su_propio_padre(validador_vacio: FamilyValidator):
    """
    A -> A
    Intentamos que A sea padre de A (ciclo)
    """
    persona = Mock(id=1, nombre="Persona", padres=[None, None])

    with pytest.raises(ValueError) as e:
        validador_vacio.validar(persona, persona, "hijo")

    assert f"{persona.nombre} no puede ser su propio padre" in str(e.value)


def test_validar_hijo_maximo_2_padres(validador_vacio: FamilyValidator):
    """
    A - B -> D
    C -> D
    Intentamos que A, B y C sean padres de D
    """
    madre = Mock(id=1, nombre="Madre", padres=[None, None])
    padre = Mock(id=2, nombre="Padre", padres=[None, None])
    persona = Mock(id=3, nombre="Persona", padres=[None, None])
    hijo = Mock(id=4, nombre="hijo", padres=[padre, madre])

    with pytest.raises(ValueError) as e:
        validador_vacio.validar(persona, hijo, "hijo")

    assert "La persona ya tiene 2 padres" in str(e.value)


def test_validar_hijo_bloquea_si_ya_son_pareja(validador_vacio: FamilyValidator):
    """
    Test: Regla 3 - Bloquea hacer padre-hijo a personas que YA son pareja

    Escenario:
    Juan <-> María (son pareja)
    Intentamos: Juan -> Padre de María
    Resultado: ERROR
    """
    juan = Mock(id=1, nombre="Juan", padres=[None, None])
    maria = Mock(id=2, nombre="María", padres=[None, None])
    jose = Mock(id=3, nombre="José", padres=[None, None])
    pepe = Mock(id=4, nombre="Pepe", padres=[None, None])
    # Los configuramos como pareja
    juan.pareja = maria
    maria.pareja = juan
    jose.pareja = pepe
    pepe.pareja = None

    with pytest.raises(ValueError) as e:
        validador_vacio.validar(juan, maria, "hijo")

    with pytest.raises(ValueError) as e:
        validador_vacio.validar(jose, pepe, "hijo")

    assert "no puede ser hijo de" in str(e.value)
    assert f"{pepe.nombre} no puede ser hijo de {jose.nombre} porque son pareja" == str(e.value)


def test_validar_hijo_detecta_ciclo_tres_generaciones(validador_vacio: FamilyValidator):
    """
    Test: Detección de ciclo complejo (3 generaciones)

    Escenario:
    Abuelo -> Padre -> Nieto
    Intentamos: Nieto -> Padre de Abuelo
    Resultado: ERROR (ciclo temporal)
    """
    abuelo = Mock(id=1, nombre="Abuelo", padres=[None, None])
    padre = Mock(id=2, nombre="Padre", padres=[abuelo, None])
    nieto = Mock(id=3, nombre="Nieto", padres=[padre, None])

    # Intentamos cerrar el ciclo: Nieto -> padre de Abuelo
    with pytest.raises(ValueError) as e:
        validador_vacio.validar(nieto, abuelo, "hijo")

    assert "Paradoja temporal" in str(e.value)


# ================= validar_hijo end =================


# ================= validar_impacto_eliminacion start =================
def test_validar_impacto_eliminacion_error_si_tiene_hijos():
    """
    Test: Error al eliminar persona con hijos

    Escenario:
    - Persona tiene hijos
    Resultado: ERROR (tiene hijos)
    """
    # ARRANGE
    # Solo necesitamos una persona que tenga algo en su lista de hijos
    persona_con_hijos = Mock(
        nombre="Rhaenyra", hijos=["Daemon", "Viserys"]
    )  # Mockeamos que tiene hijos

    # ACT & ASSERT
    with pytest.raises(ValueError) as e:
        FamilyValidator.validar_impacto_eliminacion(persona_con_hijos)

    assert "tiene descendientes" in str(e.value)


def test_validar_impacto_eliminacion_exito_si_no_tiene_hijos():
    """
    Test: Éxito al eliminar persona sin hijos

    Escenario:
    - Persona no tiene hijos
    Resultado: Éxito (no tiene hijos)
    """
    # ARRANGE
    persona_sin_hijos = Mock(nombre="Aegon", hijos=[])

    # ACT (No debería lanzar nada)
    FamilyValidator.validar_impacto_eliminacion(persona_sin_hijos)


# ================= validar_impacto_eliminacion end =================
def test_validar_relacion_desconocida(validador_vacio: FamilyValidator):
    """
    Test: Error al validar relacion desconocida

    Escenario:
    - Persona se desconoce la relacion con otra persona
    Resultado: ERROR (relacion desconocida)
    """
    with pytest.raises(ValueError) as e:
        validador_vacio.validar(Mock(), Mock(), "relacion_desconocida")

    assert "Relacion no valida" in str(e.value)


def test_validar_dispatcher_eliminar_persona(validador_vacio: FamilyValidator):
    """Cubre el dispatcher para la eliminación de personas"""
    persona = Mock(nombre="Borrar", hijos=[])
    # Aquí llamamos a validar(), que internamente ejecutará la línea 33
    validador_vacio.validar(persona, Mock(), "eliminar_persona")
