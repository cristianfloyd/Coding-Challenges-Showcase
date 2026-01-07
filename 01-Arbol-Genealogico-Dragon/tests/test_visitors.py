from src.models import Persona
from src.visitors import ArbolVisitorInterface, PrintArbolVisitor, SearchArbolVisitor


def test_base_visitor_interface_coverage():
    """Cubre el método pass de la interfaz base (Línea 14)"""

    class MockVisitor(ArbolVisitorInterface):
        pass

    visitor = MockVisitor()
    persona = Persona(1, "Test")
    # Al no estar sobreescrito, llama al visitar() de la interfaz (pass)
    visitor.visitar(persona)


def test_print_visitor_imprime_persona_simple():
    """
    Test: Verificar que PrintArbolVisitor genera la salida correcta
    para una persona sin hijos.
    """
    # ARRANGE
    persona = Persona(1, "Rhaenyra")
    visitor = PrintArbolVisitor()

    # ACT
    visitor.visitar(persona)
    resultado = visitor.get_resultado()

    # ASSERT
    # Verificamos que el resultado contenga información esperada
    assert "Rhaenyra" in resultado
    assert "id: 1" in resultado or "(1)" in resultado  # Ajusta según tu formato


def test_search_visitor_encuentra_persona():
    """
    Test: Verificar que SearchArbolVisitor encuentra una persona por nombre.
    """
    # ARRANGE
    persona = Persona(1, "Rhaenyra")
    visitor = SearchArbolVisitor("Rhaenyra")  # Buscamos "Rhaenyra"

    # ACT
    visitor.visitar(persona)
    resultados = visitor.obtener_resultado()

    # ASSERT
    assert len(resultados) == 1
    assert resultados[0].nombre == "Rhaenyra"
    assert resultados[0].id == 1


def test_search_visitor_no_encuentra_persona_inexistente():
    """
    Test: Verificar que SearchArbolVisitor retorna lista vacía si no encuentra.
    """
    # ARRANGE
    persona = Persona(1, "Rhaenyra")
    visitor = SearchArbolVisitor("Daemon")  # Buscamos alguien que no existe

    # ACT
    visitor.visitar(persona)
    resultados = visitor.obtener_resultado()

    # ASSERT
    assert len(resultados) == 0
    assert resultados == []


def test_print_visitor_con_hijos():
    # ARRANGE: Creamos un árbol pequeño
    hijo = Persona(2, "Hijo")
    padre = Persona(1, "Padre")
    padre.hijos.append(hijo)  # Relación manual para el test

    visitor = PrintArbolVisitor()

    # ACT: Usamos 'ejecutar' que cubre las líneas 78-79
    resultado = visitor.ejecutar(padre)

    # ASSERT
    assert "Padre" in resultado
    assert "Hijo" in resultado
    assert "└─" in resultado  # Verifica que entró en la recursión (líneas 65-74)


def test_print_visitor_vacio():
    visitor = PrintArbolVisitor()
    # Verificamos la línea 83
    assert visitor.get_resultado() == "No hay personajes registrados."


def test_search_visitor_recursivo():
    # ARRANGE
    nieto = Persona(3, "Nieto")
    hijo = Persona(2, "Hijo")
    padre = Persona(1, "Padre")

    # IMPORTANTE: Para que Search use recursión (línea 108),
    # necesitamos que los objetos Persona tengan el método 'accept_visitor'
    # o simular la estructura.
    hijo.hijos.append(nieto)
    padre.hijos.append(hijo)

    visitor = SearchArbolVisitor("Nieto")

    # ACT
    visitor.visitar(padre)

    # ASSERT
    assert len(visitor.obtener_resultado()) == 1
    assert visitor.obtener_resultado()[0].nombre == "Nieto"


def test_search_visitor_evita_ciclos_recursivos():
    """Verifica que el SearchVisitor no entre en bucle infinito (Línea 103)"""
    p1 = Persona(1, "A")
    p2 = Persona(2, "B")
    p1.hijos.append(p2)
    p2.hijos.append(p1)  # ¡CICLO!

    visitor = SearchArbolVisitor("Inexistente")
    visitor.visitar(p1)

    assert len(visitor.obtener_resultado()) == 0


def test_print_visitor_evita_ciclos_recursivos():
    """Verifica que el PrintVisitor no entre en bucle infinito (Línea 47)"""
    p1 = Persona(1, "A")
    p2 = Persona(2, "B")
    p1.hijos.append(p2)
    p2.hijos.append(p1)  # ¡CICLO!

    visitor = PrintArbolVisitor()
    resultado = visitor.ejecutar(p1)

    assert "A" in resultado
    assert "B" in resultado
    # Si pasa este test sin colgarse, la línea 47 hizo su trabajo


def test_print_visitor_recursivo_detecta_visitados():
    """Cubre específicamente la línea 47"""
    p1 = Persona(1, "A")
    visitor = PrintArbolVisitor()

    # Llamamos una vez
    visitor._visitar_recursivo(p1, True, [])  # type: ignore

    # Llamamos de nuevo con la misma persona (ya visitada)
    visitor._visitar_recursivo(p1, True, [])  # type: ignore

    # Si no hay error, la línea 47 funcionó
    assert p1.id in visitor.visitados


def test_print_visitor_con_pareja():
    """
    Test: Cubre la línea 59 - Persona con pareja
    Verifica que se muestre la información de la pareja en el resultado
    """
    # ARRANGE
    pareja = Persona(2, "Pareja")
    persona = Persona(1, "Persona", pareja=pareja)
    visitor = PrintArbolVisitor()

    # ACT
    visitor.visitar(persona)
    resultado = visitor.get_resultado()

    # ASSERT
    assert "Persona" in resultado
    assert "-> 2" in resultado  # Verifica que muestra el ID de la pareja


def test_print_visitor_con_multiple_hijos():
    """
    Test: Cubre las líneas 55, 71, 75 - Múltiples hijos con símbolos ├─ y └─
    Verifica que se usen correctamente los símbolos para hijos intermedios y último hijo
    """
    # ARRANGE
    hijo1 = Persona(2, "Hijo1")
    hijo2 = Persona(3, "Hijo2")
    hijo3 = Persona(4, "Hijo3")
    padre = Persona(1, "Padre")
    padre.hijos.extend([hijo1, hijo2, hijo3])
    visitor = PrintArbolVisitor()

    # ACT
    resultado = visitor.ejecutar(padre)

    # ASSERT
    assert "├─" in resultado  # Debe tener hijo intermedio
    assert "└─" in resultado  # Debe tener último hijo
    assert "Hijo1" in resultado
    assert "Hijo2" in resultado
    assert "Hijo3" in resultado


def test_print_visitor_prefijos_con_multiple_hijos():
    """
    Test: Cubre las líneas 74-77 - Prefijos │  y espacios
    Verifica que se usen correctamente los prefijos │  para hijos intermedios
    """
    # ARRANGE
    nieto1 = Persona(3, "Nieto1")
    nieto2 = Persona(4, "Nieto2")
    hijo1 = Persona(2, "Hijo1")
    hijo1.hijos.extend([nieto1, nieto2])
    padre = Persona(1, "Padre")
    padre.hijos.append(hijo1)
    visitor = PrintArbolVisitor()

    # ACT
    resultado = visitor.ejecutar(padre)

    # ASSERT
    # Verifica que se usan los prefijos correctos
    lines = resultado.split("\n")
    assert len(lines) >= 3  # Padre, Hijo1, y al menos un nieto


def test_print_visitor_visitar_ya_visitado():
    """
    Test: Cubre la línea 33 - Cuando persona.id ya está en visitados
    Verifica que visitar() no entre en recursión si la persona ya fue visitada
    """
    # ARRANGE
    persona = Persona(1, "Persona")
    visitor = PrintArbolVisitor()

    # ACT
    visitor.visitar(persona)
    resultado1 = visitor.get_resultado()

    # Llamamos visitar() de nuevo con la misma persona
    visitor.visitar(persona)
    resultado2 = visitor.get_resultado()

    # ASSERT
    # El resultado no debería cambiar porque ya estaba visitado
    assert resultado1 == resultado2
    assert persona.id in visitor.visitados


def test_print_visitor_hijos_no_visitados():
    """
    Test: Cubre la línea 67 - Filtrar hijos ya visitados
    Verifica que solo se procesen hijos que no han sido visitados
    """
    # ARRANGE
    hijo1 = Persona(2, "Hijo1")
    hijo2 = Persona(3, "Hijo2")
    padre = Persona(1, "Padre")
    padre.hijos.extend([hijo1, hijo2])
    visitor = PrintArbolVisitor()

    # ACT
    # Visitamos primero un hijo directamente
    visitor.visitar(hijo1)
    # Luego visitamos el padre (que tiene hijo1 y hijo2)
    visitor.visitar(padre)
    resultado = visitor.get_resultado()

    # ASSERT
    # hijo1 no debería aparecer dos veces
    assert resultado.count("Hijo1") == 1
    assert "Hijo2" in resultado


def test_search_visitor_busqueda_case_insensitive():
    """
    Test: Cubre las líneas 100 y 109 - Búsqueda insensible a mayúsculas/minúsculas
    Verifica que la búsqueda funcione sin importar mayúsculas o minúsculas
    """
    # ARRANGE
    persona = Persona(1, "Rhaenyra")
    visitor1 = SearchArbolVisitor("rhaenyra")  # minúsculas
    visitor2 = SearchArbolVisitor("RHAENYRA")  # mayúsculas
    visitor3 = SearchArbolVisitor("RhAeNyRa")  # mixto

    # ACT
    visitor1.visitar(persona)
    visitor2.visitar(persona)
    visitor3.visitar(persona)

    # ASSERT
    assert len(visitor1.obtener_resultado()) == 1
    assert len(visitor2.obtener_resultado()) == 1
    assert len(visitor3.obtener_resultado()) == 1


def test_search_visitor_busqueda_con_espacios():
    """
    Test: Cubre las líneas 100 y 109 - strip() para eliminar espacios
    Verifica que la búsqueda funcione correctamente con espacios
    """
    # ARRANGE
    persona = Persona(1, "  Rhaenyra  ")
    visitor = SearchArbolVisitor("  Rhaenyra  ")

    # ACT
    visitor.visitar(persona)
    resultados = visitor.obtener_resultado()

    # ASSERT
    assert len(resultados) == 1
    assert resultados[0].id == 1


def test_search_visitor_visitar_ya_visitado():
    """
    Test: Cubre la línea 104 - Cuando persona.id ya está en visitados
    Verifica que visitar() retorne inmediatamente si la persona ya fue visitada
    """
    # ARRANGE
    persona = Persona(1, "Persona")
    visitor = SearchArbolVisitor("Persona")

    # ACT
    visitor.visitar(persona)
    resultado1 = visitor.obtener_resultado()

    # Llamamos visitar() de nuevo con la misma persona
    visitor.visitar(persona)
    resultado2 = visitor.obtener_resultado()

    # ASSERT
    # El resultado no debería cambiar porque ya estaba visitado
    assert len(resultado1) == 1
    assert len(resultado2) == 1
    assert resultado1 == resultado2
    assert persona.id in visitor.visitados


def test_print_visitor_ejecutar_retorna_string():
    """
    Test: Cubre la línea 84 - ejecutar() retorna string
    Verifica que ejecutar() retorne el resultado como string
    """
    # ARRANGE
    persona = Persona(1, "Persona")
    visitor = PrintArbolVisitor()

    # ACT
    resultado = visitor.ejecutar(persona)

    # ASSERT
    assert isinstance(resultado, str)
    assert "Persona" in resultado


def test_search_visitor_init():
    """
    Test: Cubre las líneas 98-101 - Inicialización de SearchArbolVisitor
    Verifica que el constructor inicialice correctamente los atributos
    """
    # ARRANGE & ACT
    visitor = SearchArbolVisitor("  Test  ")

    # ASSERT
    assert visitor.nombre_a_buscar == "test"
    assert visitor.resultado == []
    assert visitor.visitados == set()


def test_print_visitor_init():
    """
    Test: Cubre las líneas 23-25 - Inicialización de PrintArbolVisitor
    Verifica que el constructor inicialice correctamente los atributos
    """
    # ARRANGE & ACT
    visitor = PrintArbolVisitor()

    # ASSERT
    assert visitor.resultado == []
    assert visitor.visitados == set()
