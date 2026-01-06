from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from .data_loader import DataLoaderDemo
    from .interfaces import ArbolRepository, DataLoaderProtocol, UIProtocol
    from .repository import ArbolGenealogico
    from .ui import DinastiaUI

from .data_loader import DataLoaderDemo
from .repository import ArbolGenealogico
from .ui import DinastiaUI


class ContainerProtocol(Protocol):
    """
    Protocolo de interfaz para el contenedor de dependencias.

    Define la interfaz que debe cumplir cualquier contenedor,
    siguiendo el principio de Dependency Inversion (SOLID).
    """

    def get_arbol(self) -> "ArbolRepository":
        """
        Obtiene una instancia del repositorio de árbol genealógico.

        Returns:
            ArbolRepository: Instancia del repositorio.
        """
        ...

    def get_ui(self) -> "UIProtocol":
        """
        Obtiene una instancia de la interfaz de usuario.

        Returns:
            UI: Instancia de la interfaz de usuario.
        """
        ...

    def get_data_loader(self) -> "DataLoaderProtocol":
        """
        Obtiene una instancia del cargador de datos.

        Returns:
            DataLoader: Instancia del cargador de datos.
        """
        ...


class ApplicationContainer:
    """
    Contenedor de dependencias siguiendo Dependency Injection.

    Implementa el patrón Service Locator con lazy initialization
    para gestionar el ciclo de vida de las dependencias.
    """

    def __init__(self):
        self._arbol: ArbolGenealogico | None = None
        self._ui: DinastiaUI | None = None

    def get_arbol(self) -> ArbolGenealogico:
        """
        Obtiene una instancia de ArbolGenealogico (singleton).

        Si no existe, crea una nueva y la almacena para futuras llamadas.

        Returns:
            ArbolGenealogico: Instancia única del repositorio.
        """
        if self._arbol is None:
            self._arbol = ArbolGenealogico()
        return self._arbol

    def get_ui(self) -> DinastiaUI:
        """
        Obtiene una instancia de DinastiaUI (singleton).

        Si no existe, crea una nueva con las dependencias necesarias
        y la almacena para futuras llamadas.

        Returns:
            DinastiaUI: Instancia única de la interfaz de usuario.
        """
        if self._ui is None:
            self._ui = DinastiaUI(self.get_arbol())
        return self._ui

    def get_data_loader(self) -> "DataLoaderProtocol":
        """
        Obtiene una nueva instancia de DataLoaderDemo (transient).

        Retorna una nueva instancia en cada llamada, ya que
        DataLoaderDemo es stateless.

        Returns:
            DataLoaderProtocol: Nueva instancia del cargador de datos.
        """
        return DataLoaderDemo()
