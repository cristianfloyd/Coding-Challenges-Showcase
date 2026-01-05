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
