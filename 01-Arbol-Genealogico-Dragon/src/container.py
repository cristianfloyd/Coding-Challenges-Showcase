from .data_loader import DemoDataLoader
from .repository import ArbolGenealogico
from .ui import DinastiaUI


class ApplicationContainer:
    """Contenedor de dependencias siguiendo Dependency Injection"""

    def __init__(self):
        self._arbol: ArbolGenealogico | None = None
        self._ui: DinastiaUI | None = None

    def get_arbol(self) -> ArbolGenealogico:
        """
        Obtiene una instancia de ArbolGenealogico.
        Si no existe, crea una nueva.
        """
        if self._arbol is None:
            self._arbol = ArbolGenealogico()
        return self._arbol

    def get_ui(self) -> DinastiaUI:
        """
        Obtiene una instancia de DinastiaUI.
        Si no existe, crea una nueva.
        """
        if self._ui is None:
            self._ui = DinastiaUI(self.get_arbol())
        return self._ui

    def get_data_loader(self) -> DemoDataLoader:
        """
        Obtiene una instancia de DemoDataLoader.
        """
        return DemoDataLoader()
