from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from .models import Persona
    from .visitors import ArbolVisitorInterface


class ArbolRepository(Protocol):
    """
    Protocolo para el repositorio de árbol genealógico.

    Define la interfaz que debe cumplir cualquier implementación
    de repositorio de árbol genealógico, siguiendo el principio
    de Dependency Inversion (SOLID).
    """

    # Propiedad para acceder a las personas
    @property
    def personas(self) -> dict[int, "Persona"]: ...  # pragma: no cover

    def registrar_persona(self, nombre: str) -> "Persona":
        """
        Registra una nueva persona en el árbol.

        Args:
            nombre: Nombre de la persona a registrar.

        Returns:
            Persona: La persona recién registrada.

        Raises:
            ValueError: Si el registro no es válido.
        """
        ...  # pragma: no cover

    def get_persona(self, persona_id: int) -> "Persona":
        """
        Obtiene una persona por su ID.

        Args:
            persona_id: ID de la persona a buscar.

        Returns:
            Persona: La persona encontrada.

        Raises:
            ValueError: Si la persona no existe.
        """
        ...  # pragma: no cover

    def init_get_root(self) -> list["Persona"]:
        """
        Obtiene las raíces del árbol (personas sin padres).

        Returns:
            Lista de personas que son raíces del árbol.
        """
        ...  # pragma: no cover

    def recorrer_arbol_completo(self, visitor: "ArbolVisitorInterface") -> None:
        """
        Recorre el árbol completo usando el patrón Visitor.

        Args:
            visitor: Visitante que procesará cada persona del árbol.
        """
        ...  # pragma: no cover

    def add_hijo(self, padre: "Persona", hijo: "Persona") -> None:
        """
        Establece una relación padre-hijo entre dos personas.

        Args:
            padre: Persona que será el padre.
            hijo: Persona que será el hijo.

        Raises:
            ValueError: Si la relación no es válida.
        """
        ...  # pragma: no cover

    def add_pareja(self, persona1: "Persona", persona2: "Persona") -> None:
        """
        Establece una relación de pareja entre dos personas.

        Args:
            persona1: Primera persona de la pareja.
            persona2: Segunda persona de la pareja.

        Raises:
            ValueError: Si la relación no es válida.
        """
        ...  # pragma: no cover

    def remove_pareja(self, persona1: "Persona", persona2: "Persona") -> None:
        """
        Elimina la relación de pareja entre dos personas.

        Args:
            persona1: Primera persona de la pareja.
            persona2: Segunda persona de la pareja.

        Raises:
            ValueError: Si la relación no existe o no es válida.
        """
        ...  # pragma: no cover

    def eliminar_persona(self, persona_id: int, confirmar_rotura: bool = False) -> None:
        """
        Elimina una persona del árbol.

        Args:
            persona_id: ID de la persona a eliminar.
            confirmar_rotura: Si True, permite eliminar aunque tenga descendientes.

        Raises:
            ValueError: Si la persona no existe o no se puede eliminar.
        """
        ...  # pragma: no cover


class DataLoaderProtocol(Protocol):
    """
    Protocolo para cargadores de datos.

    Define la interfaz para cualquier implementación que cargue
    datos iniciales en el árbol genealógico.
    """

    def cargar_datos(self, arbol: "ArbolRepository") -> None:
        """
        Carga datos en el árbol genealógico.

        Args:
            arbol: Repositorio donde se cargarán los datos.
        """
        ...  # pragma: no cover


class UIProtocol(Protocol):
    """
    Protocolo para la interfaz de usuario.

    Define la interfaz que debe cumplir cualquier implementación
    de interfaz de usuario para el árbol genealógico.
    """

    def mostrar_menu_principal(self) -> None:
        """
        Muestra el menú principal y gestiona la interacción con el usuario.
        """
        ...  # pragma: no cover

    def agregar_persona(self) -> None:
        """
        Solicita datos al usuario y agrega una nueva persona al árbol.
        """
        ...  # pragma: no cover

    def buscar_persona(self) -> None:
        """
        Solicita un nombre al usuario y busca personas en el árbol.
        """
        ...  # pragma: no cover

    def mostrar_arbol(self) -> None:
        """
        Muestra el árbol genealógico completo.
        """
        ...  # pragma: no cover

    def agregar_hijo(self) -> None:
        """
        Solicita IDs al usuario y establece una relación padre-hijo.
        """
        ...  # pragma: no cover

    def agregar_pareja(self) -> None:
        """
        Solicita IDs al usuario y establece una relación de pareja.
        """
        ...  # pragma: no cover

    def eliminar_pareja(self) -> None:
        """
        Solicita IDs al usuario y elimina una relación de pareja.
        """
        ...  # pragma: no cover

    def eliminar_persona(self) -> None:
        """
        Solicita un ID al usuario y elimina una persona del árbol.
        """
        ...  # pragma: no cover
