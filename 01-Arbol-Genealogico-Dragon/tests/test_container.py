"""
Tests para el módulo container.py

Verifica la correcta implementación del patrón Service Locator y Singleton
en ApplicationContainer.
"""

from src.container import ApplicationContainer
from src.data_loader import DataLoaderDemo
from src.repository import ArbolGenealogico
from src.ui import DinastiaUI


class TestApplicationContainer:
    """Tests para la clase ApplicationContainer"""

    def test_get_arbol_singleton(self):
        """
        Test: get_arbol retorna Singleton

        Verifica que get_arbol():
        1. Retorna una instancia de ArbolGenealogico
        2. Retorna siempre la misma instancia (Singleton de facto)
        """
        container = ApplicationContainer()

        arbol1 = container.get_arbol()
        arbol2 = container.get_arbol()

        assert isinstance(arbol1, ArbolGenealogico)
        assert arbol1 is arbol2

    def test_get_ui_singleton(self):
        """
        Test: get_ui retorna Singleton

        Verifica que get_ui():
        1. Retorna una instancia de DinastiaUI
        2. Retorna siempre la misma instancia
        3. Se inicializa correctamente con el árbol del contenedor
        """
        container = ApplicationContainer()

        ui1 = container.get_ui()
        ui2 = container.get_ui()

        assert isinstance(ui1, DinastiaUI)
        assert ui1 is ui2
        # Verificar que la UI tiene el mismo árbol que el contenedor
        assert ui1.arbol is container.get_arbol()

    def test_get_data_loader_transient(self):
        """
        Test: get_data_loader retorna nueva instancia (Transient)

        Verifica que get_data_loader():
        1. Retorna una instancia de DataLoaderDemo
        2. Retorna una NUEVA instancia cada vez
        """
        container = ApplicationContainer()

        loader1 = container.get_data_loader()
        loader2 = container.get_data_loader()

        assert isinstance(loader1, DataLoaderDemo)
        assert isinstance(loader2, DataLoaderDemo)
        assert loader1 is not loader2
