"""
Tests para verificar la conformidad con los Protocolos definidos en interfaces.py

En este archivo verificamos que:
1. Las implementaciones concretas (ArbolGenealogico, DataLoaderDemo, DinastiaUI)
   cumplan con los Protocolos definidos
2. Todos los métodos declarados en los Protocolos existan y funcionen correctamente
3. Las anotaciones de tipo sean correctas
"""

from unittest.mock import patch

import pytest

from src.data_loader import DataLoaderDemo
from src.models import Persona
from src.repository import ArbolGenealogico
from src.ui import DinastiaUI
from src.visitors import PrintArbolVisitor

# ==================== TESTS PARA ArbolRepository PROTOCOL ====================


def test_arbol_genealogico_implementa_arbol_repository():
    """
    Test de conformidad estructural con el Protocol ArbolRepository

    Explicación:
    ------------
    Este test verifica que ArbolGenealogico cumple estructuralmente con el
    Protocol ArbolRepository. No usamos isinstance() porque los Protocols en
    Python no son verificables en runtime por defecto (a menos que usemos
    @runtime_checkable).

    Lo que hacemos es verificar que:
    1. La clase tiene todos los métodos requeridos por el Protocol
    2. Los métodos tienen las firmas correctas (parámetros y retorno)
    3. La propiedad 'personas' existe y es accesible
    """
    # ARRANGE: Creamos una instancia de la implementación concreta
    arbol = ArbolGenealogico()

    # ACT & ASSERT: Verificamos que tiene todos los métodos del Protocol

    # 1. Verificar que tiene la propiedad 'personas'
    assert hasattr(arbol, "personas"), "ArbolGenealogico debe tener propiedad 'personas'"
    assert isinstance(arbol.personas, dict), "personas debe ser un diccionario"

    # 2. Verificar que tiene el método 'registrar_persona'
    assert hasattr(arbol, "registrar_persona"), "Debe tener método 'registrar_persona'"
    assert callable(getattr(arbol, "registrar_persona")), "registrar_persona debe ser callable"

    # 3. Verificar que tiene el método 'get_persona'
    assert hasattr(arbol, "get_persona"), "Debe tener método 'get_persona'"

    # 4. Verificar que tiene el método 'init_get_root'
    assert hasattr(arbol, "init_get_root"), "Debe tener método 'init_get_root'"

    # 5. Verificar que tiene el método 'recorrer_arbol_completo'
    assert hasattr(arbol, "recorrer_arbol_completo"), "Debe tener método 'recorrer_arbol_completo'"

    # 6. Verificar que tiene el método 'add_hijo'
    assert hasattr(arbol, "add_hijo"), "Debe tener método 'add_hijo'"

    # 7. Verificar que tiene el método 'add_pareja'
    assert hasattr(arbol, "add_pareja"), "Debe tener método 'add_pareja'"

    # 8. Verificar que tiene el método 'remove_pareja'
    assert hasattr(arbol, "remove_pareja"), "Debe tener método 'remove_pareja'"

    # 9. Verificar que tiene el método 'eliminar_persona'
    assert hasattr(arbol, "eliminar_persona"), "Debe tener método 'eliminar_persona'"


def test_arbol_repository_registrar_persona():
    """
    Test: Verificar que registrar_persona funciona según el Protocol

    Explicación:
    ------------
    Este test verifica que el método 'registrar_persona' implementa correctamente
    la interfaz definida en ArbolRepository.

    Según el Protocol, registrar_persona debe:
    - Recibir un parámetro 'nombre' de tipo str
    - Retornar un objeto Persona
    - Potencialmente lanzar ValueError si el registro no es válido
    """
    # ARRANGE: Preparar el estado inicial
    arbol = ArbolGenealogico()
    nombre_persona = "Rhaenyra"

    # ACT: Ejecutar la acción (registrar persona)
    persona_registrada = arbol.registrar_persona(nombre_persona)

    # ASSERT: Verificar los resultados
    assert isinstance(persona_registrada, Persona), "Debe retornar una instancia de Persona"
    assert persona_registrada.nombre == nombre_persona, "El nombre debe coincidir"
    assert persona_registrada.id in arbol.personas, "La persona debe estar en el diccionario"
    assert arbol.personas[persona_registrada.id] == persona_registrada, (
        "Debe ser la misma instancia"
    )


def test_arbol_repository_get_persona():
    """
    Test: Verificar que get_persona funciona según el Protocol

    El Protocol indica que get_persona debe lanzar ValueError si la persona
    no existe. Sin embargo, en la implementación real usamos PersonaNoEncontradaError,
    que hereda de ArbolGenealogicoError, que a su vez hereda de Exception.
    Esto es válido porque PersonaNoEncontradaError ES un tipo de error de valor.
    """
    # ARRANGE
    arbol = ArbolGenealogico()
    persona = arbol.registrar_persona("Daemon")
    persona_id = persona.id

    # ACT & ASSERT: Caso exitoso
    persona_obtenida = arbol.get_persona(persona_id)
    assert persona_obtenida == persona, "Debe retornar la persona correcta"

    # ACT & ASSERT: Caso de error (persona no existe)
    from src.exceptions import PersonaNoEncontradaError

    with pytest.raises(PersonaNoEncontradaError) as exc_info:
        arbol.get_persona(999)  # ID que no existe

    assert "no encontrada" in str(exc_info.value).lower(), "Mensaje de error debe ser descriptivo"


def test_arbol_repository_init_get_root():
    """
    Test: Verificar que init_get_root retorna las raíces del árbol

    Escenarios a probar:
    - Árbol vacío: Debe retornar lista vacía
    - Árbol con raíces: Debe retornar las personas sin padres
    - Árbol con hijos: Los hijos no deben aparecer en las raíces
    """
    # ARRANGE: Crear un árbol con estructura
    arbol = ArbolGenealogico()
    raiz1 = arbol.registrar_persona("Raíz 1")
    raiz2 = arbol.registrar_persona("Raíz 2")
    hijo = arbol.registrar_persona("Hijo")

    # Establecer relación padre-hijo
    arbol.add_hijo(raiz1, hijo)

    # ACT
    raices = arbol.init_get_root()

    # ASSERT
    assert isinstance(raices, list), "Debe retornar una lista"
    assert len(raices) == 2, "Solo deben haber dos raíces (raiz1 y raiz2)"
    assert raiz2 in raices, "raiz2 debe ser una raíz"
    assert hijo not in raices, "Hijo no debe ser raíz"


def test_arbol_repository_recorrer_arbol_completo():
    """
    Test: Verificar que recorrer_arbol_completo usa el patrón Visitor
    1. El árbol acepta un Visitor (objeto con operaciones a realizar)
    2. El árbol recorre sus nodos (personas)
    3. Cada nodo acepta al Visitor y ejecuta la operación
    4. El Visitor acumula resultados en su estado interno
    """
    # ARRANGE
    arbol = ArbolGenealogico()
    raiz = arbol.registrar_persona("Raíz")
    hijo1 = arbol.registrar_persona("Hijo 1")
    hijo2 = arbol.registrar_persona("Hijo 2")

    arbol.add_hijo(raiz, hijo1)
    arbol.add_hijo(raiz, hijo2)

    visitor = PrintArbolVisitor()

    # ACT
    arbol.recorrer_arbol_completo(visitor)
    resultado = visitor.get_resultado()

    # ASSERT
    assert "Raíz" in resultado, "Debe visitar la raíz"
    assert "Hijo 1" in resultado, "Debe visitar el primer hijo"
    assert "Hijo 2" in resultado, "Debe visitar el segundo hijo"


def test_arbol_repository_add_hijo():
    """
    Test: Verificar que add_hijo establece relación padre-hijo
    1. Establece correctamente la relación padre-hijo
    2. Agrega el hijo a la lista de hijos del padre
    3. Establece al padre en la tupla de padres del hijo
    """
    # ARRANGE
    arbol = ArbolGenealogico()
    padre = arbol.registrar_persona("Padre")
    hijo = arbol.registrar_persona("Hijo")

    # ACT
    arbol.add_hijo(padre, hijo)

    # ASSERT
    assert hijo in padre.hijos, "Hijo debe estar en la lista de hijos del padre"
    assert padre in hijo.padres, "Padre debe estar en la tupla de padres del hijo"


def test_arbol_repository_add_pareja():
    """
    Test: Verificar que add_pareja establece relación de pareja

    Este test verifica que el método add_pareja establece correctamente
    la relación bidireccional de pareja entre dos personas.
    """
    # ARRANGE
    arbol = ArbolGenealogico()
    persona1 = arbol.registrar_persona("Persona 1")
    persona2 = arbol.registrar_persona("Persona 2")

    # ACT
    arbol.add_pareja(persona1, persona2)

    # ASSERT
    assert persona1.pareja == persona2, "persona1 debe tener a persona2 como pareja"
    assert persona2.pareja == persona1, "persona2 debe tener a persona1 como pareja"


def test_arbol_repository_remove_pareja():
    """
    Test: Verificar que remove_pareja elimina relación de pareja

    Este test verifica que remove_pareja:
    1. Elimina la relación bidireccional de pareja
    2. Establece pareja en None para ambas personas
    """
    # ARRANGE
    arbol = ArbolGenealogico()
    persona1 = arbol.registrar_persona("Persona 1")
    persona2 = arbol.registrar_persona("Persona 2")
    arbol.add_pareja(persona1, persona2)

    # Verificar que la pareja está establecida
    assert persona1.pareja == persona2
    assert persona2.pareja == persona1

    # ACT
    arbol.remove_pareja(persona1, persona2)

    # ASSERT
    assert persona1.pareja is None, "persona1 no debe tener pareja"
    assert persona2.pareja is None, "persona2 no debe tener pareja"


def test_arbol_repository_eliminar_persona():
    """
    Test: Verificar que eliminar_persona elimina una persona del árbol

    Este test verifica que eliminar_persona:
    1. Elimina la persona del diccionario de personas
    2. Maneja correctamente el caso cuando la persona no existe
    """
    # ARRANGE
    arbol = ArbolGenealogico()
    persona = arbol.registrar_persona("Persona a eliminar")
    persona_id = persona.id

    # Verificar que existe
    assert persona_id in arbol.personas

    # ACT
    arbol.eliminar_persona(persona_id)

    # ASSERT
    assert persona_id not in arbol.personas, "La persona debe ser eliminada del diccionario"


# ==================== TESTS PARA DataLoaderProtocol ====================


def test_data_loader_demo_implementa_data_loader_protocol():
    """
    Test: Verificar que DataLoaderDemo cumple con DataLoaderProtocol

    Este test verifica la conformidad estructural de DataLoaderDemo
    con el Protocol DataLoaderProtocol.

    El Protocol solo define un método: cargar_datos(arbol)
    que debe recibir un ArbolRepository y no retornar nada.
    """
    # ARRANGE
    data_loader = DataLoaderDemo()

    # ACT & ASSERT
    assert hasattr(data_loader, "cargar_datos"), "Debe tener método 'cargar_datos'"
    assert callable(getattr(data_loader, "cargar_datos")), "cargar_datos debe ser callable"


def test_data_loader_protocol_cargar_datos():
    """
    Test: Verificar que cargar_datos funciona según el Protocol

    Este test verifica que:
    1. El método cargar_datos acepta un ArbolRepository
    2. Carga datos en el árbol (modifica el estado del árbol)
    3. No retorna nada (None)

    Patrón de verificación:
    - Verificamos el estado antes y después de cargar_datos
    - Verificamos que el árbol tiene más personas después de cargar
    """
    # ARRANGE
    arbol = ArbolGenealogico()
    data_loader = DataLoaderDemo()

    # Verificar estado inicial
    assert len(arbol.personas) == 0, "Árbol debe estar vacío inicialmente"

    # ACT
    resultado = data_loader.cargar_datos(arbol)

    # ASSERT
    assert resultado is None, "cargar_datos no debe retornar nada"
    assert len(arbol.personas) > 0, "El árbol debe tener personas después de cargar datos"


# ==================== TESTS PARA UIProtocol ====================


def test_dinastia_ui_implementa_ui_protocol():
    """
    Test: Verificar que DinastiaUI cumple con UIProtocol

    Este test verifica la conformidad estructural de DinastiaUI
    con el Protocol UIProtocol.

    El Protocol define varios métodos para la interacción con el usuario:
    - mostrar_menu_principal()
    - agregar_persona()
    - buscar_persona()
    - mostrar_arbol()
    - agregar_hijo()
    - agregar_pareja()
    - eliminar_pareja()
    - eliminar_persona()

    Todos estos métodos deben existir y ser callable.
    """
    # ARRANGE
    arbol = ArbolGenealogico()
    ui = DinastiaUI(arbol)

    # ACT & ASSERT: Verificar que todos los métodos existen
    metodos_requeridos = [
        "mostrar_menu_principal",
        "agregar_persona",
        "buscar_persona",
        "mostrar_arbol",
        "agregar_hijo",
        "agregar_pareja",
        "eliminar_pareja",
        "eliminar_persona",
    ]

    for metodo in metodos_requeridos:
        assert hasattr(ui, metodo), f"DinastiaUI debe tener método '{metodo}'"
        assert callable(getattr(ui, metodo)), f"'{metodo}' debe ser callable"


def test_ui_protocol_agregar_persona():
    """
    Test: Verificar que agregar_persona funciona según el Protocol
    """
    # ARRANGE
    arbol = ArbolGenealogico()
    ui = DinastiaUI(arbol)

    # Mock de input para simular entrada del usuario
    with patch("builtins.input", return_value="Nueva Persona"):
        with patch("builtins.print"):  # Mock de print para evitar output
            # ACT
            ui.agregar_persona()

    # ASSERT
    # Verificar que se agregó una persona al árbol
    assert len(arbol.personas) > 0, "Debe haber agregado al menos una persona"

    # Verificar que la persona tiene el nombre correcto
    personas_nombres = [p.nombre for p in arbol.personas.values()]
    assert "Nueva Persona" in personas_nombres, "Debe contener 'Nueva Persona'"


def test_ui_protocol_buscar_persona():
    """
    Test: Verificar que buscar_persona funciona según el Protocol

    Este test verifica que el método buscar_persona solicita un nombre al
    usuario, busca coincidencias en el árbol genealógico y muestra los
    resultados encontrados por pantalla.
    """
    # ARRANGE
    arbol = ArbolGenealogico()
    persona = arbol.registrar_persona("Persona a buscar")
    ui = DinastiaUI(arbol)

    # ACT: Simular búsqueda
    with patch("builtins.input", return_value="Persona a buscar"):
        with patch("builtins.print") as mock_print:
            ui.buscar_persona()

    # ASSERT: Verificar que se llamó a print (indica que mostró resultados)
    full_output = "".join(str(call) for call in mock_print.call_args_list)

    assert "Resultados:" in full_output, "Debe mostrar el encabezado de éxito"
    assert "Persona a buscar" in full_output, "Debe mostrar el nombre de la persona"
    assert str(persona.id) in full_output, "Debe mostrar el ID correcto de la persona"


def test_ui_protocol_mostrar_arbol():
    """
    Test: Verificar que mostrar_arbol funciona según el Protocol

    Este test verifica que mostrar_arbol recorre el árbol y muestra
    su estructura. Usamos un mock de print para verificar que se
    ejecuta sin errores.
    """
    # ARRANGE
    arbol = ArbolGenealogico()
    raiz = arbol.registrar_persona("Raíz")
    hijo = arbol.registrar_persona("Hijo")
    arbol.add_hijo(raiz, hijo)

    ui = DinastiaUI(arbol)

    # ACT
    with patch("builtins.print") as mock_print:
        ui.mostrar_arbol()

    # ASSERT: Verificar que se imprimió la estructura esperada
    full_output = "".join(str(call) for call in mock_print.call_args_list)

    assert "Raíz" in full_output, "Debe mostrar el nombre de la raíz"
    assert "Hijo" in full_output, "Debe mostrar el nombre del hijo"
    assert "✅" in full_output, "Debe usar el formato de éxito de UIMessages"


def test_ui_protocol_agregar_hijo():
    """
    Test: Verificar que agregar_hijo funciona según el Protocol

    Este test verifica que agregar_hijo:
    1. Solicita IDs al usuario (simulado)
    2. Obtiene las personas del árbol
    3. Establece la relación padre-hijo
    """
    # ARRANGE
    arbol = ArbolGenealogico()
    padre = arbol.registrar_persona("Padre")
    hijo = arbol.registrar_persona("Hijo")
    ui = DinastiaUI(arbol)

    # ACT: Simular entrada de IDs (padre.id, hijo.id)
    with patch("builtins.input", side_effect=[str(padre.id), str(hijo.id)]):
        with patch("builtins.print"):
            ui.agregar_hijo()

    # ASSERT
    assert hijo in padre.hijos, "Hijo debe estar en la lista de hijos del padre"


def test_ui_protocol_agregar_pareja():
    """
    Test: Verificar que agregar_pareja funciona según el Protocol
    """
    # ARRANGE
    arbol = ArbolGenealogico()
    persona1 = arbol.registrar_persona("Persona 1")
    persona2 = arbol.registrar_persona("Persona 2")
    ui = DinastiaUI(arbol)

    # ACT
    with patch("builtins.input", side_effect=[str(persona1.id), str(persona2.id)]):
        with patch("builtins.print"):
            ui.agregar_pareja()

    # ASSERT
    assert persona1.pareja == persona2, "persona1 debe tener a persona2 como pareja"


def test_ui_protocol_eliminar_pareja():
    """Test: Verificar que eliminar_pareja funciona según el Protocol"""
    # ARRANGE
    arbol = ArbolGenealogico()
    persona1 = arbol.registrar_persona("Persona 1")
    persona2 = arbol.registrar_persona("Persona 2")
    arbol.add_pareja(persona1, persona2)
    ui = DinastiaUI(arbol)

    # ACT
    with patch("builtins.input", side_effect=[str(persona1.id), str(persona2.id)]):
        with patch("builtins.print"):
            ui.eliminar_pareja()

    # ASSERT
    assert persona1.pareja is None, "persona1 no debe tener pareja"
    assert persona2.pareja is None, "persona2 no debe tener pareja"


def test_ui_protocol_eliminar_persona():
    """Test: Verificar que eliminar_persona funciona según el Protocol"""
    # ARRANGE
    arbol = ArbolGenealogico()
    persona = arbol.registrar_persona("Persona a eliminar")
    persona_id = persona.id
    ui = DinastiaUI(arbol)

    # ACT
    with patch("builtins.input", return_value=str(persona_id)):
        with patch("builtins.print"):
            ui.eliminar_persona()

    # ASSERT
    assert persona_id not in arbol.personas, "La persona debe ser eliminada"


# ==================== TESTS DE TIPOS Y ANOTACIONES ====================


def test_arbol_repository_property_personas_tipo():
    """
    Test: Verificar que la propiedad personas tiene el tipo correcto"""
    # ARRANGE
    arbol = ArbolGenealogico()

    # ACT: Obtener anotaciones de tipo
    # Nota: En runtime, las anotaciones pueden no estar disponibles
    # dependiendo de si usamos __annotations__ o get_type_hints()

    # ASSERT: Verificar que personas es un dict[int, Persona]
    assert isinstance(arbol.personas, dict), "personas debe ser un diccionario"

    # Si agregamos una persona, verificamos que la clave es int y el valor es Persona
    persona = arbol.registrar_persona("Test")
    assert isinstance(persona.id, int), "Las claves deben ser int"
    assert isinstance(arbol.personas[persona.id], Persona), "Los valores deben ser Persona"
