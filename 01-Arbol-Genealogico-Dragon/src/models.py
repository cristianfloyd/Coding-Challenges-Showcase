from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .visitors import ArbolVisitorInterface


class Persona:
    """
    Representa a una persona dentro del árbol genealógico.

    Esta clase gestiona la información básica de una persona,
    incluyendo su identificador único, nombre, su pareja, sus hijos
    y sus padres (biológicos o reconocidos).

    Atributos:
        id (int): Identificador único de la persona.
        nombre (str): Nombre completo de la persona.
        pareja (Optional[Persona]): Referencia a la pareja actual de la persona, si existe.
        hijos (list[Persona]): Lista de objetos Persona que representan los hijos de esta persona.
        padres (tuple[Optional[Persona], Optional[Persona]]): Tupla de longitud 2
        con las referencias a los padres biológicos o reconocidos
        (pueden ser None si no están definidos).
    """

    def __init__(
        self,
        person_id: int,
        nombre: str,
        pareja: Optional["Persona"] = None,
        hijos: Optional[list["Persona"]] = None,
    ):
        """
        Inicializa una instancia de Persona.

        Args:
            person_id (int): Identificador único de la persona.
            nombre (str): Nombre de la persona.
            pareja (Optional[Persona], opcional): Pareja de la persona. Por defecto es None.
            hijos (Optional[list[Persona]], opcional): Lista de hijos de la persona.
                Si no se proporciona, se inicializa como una lista vacía.
        """
        self.id = person_id
        self.nombre: str = nombre
        self.pareja: Optional["Persona"] = pareja or None
        self.hijos: list["Persona"] = hijos or []
        self.padres: tuple[Optional["Persona"], Optional["Persona"]] = (None, None)

    def accept_visitor(self, visitor: "ArbolVisitorInterface") -> None:
        """
        Acepta un visitante que implementa la interfaz ArbolVisitorInterface y permite
        que el visitante realice una operación sobre esta instancia de Persona.

        Args:
            visitor (ArbolVisitorInterface): El visitante que realizará una acción
            sobre la persona actual.
        """
        visitor.visitar(self)

    def __str__(self):
        """
        Devuelve una representación en cadena de la persona, mostrando su nombre y su id.
        Returns:
            str: Representación legible de la persona.
        """
        return f"{self.nombre} ({self.id})"

    def __repr__(self):
        """
        Devuelve una representación informal de la persona, igual al método __str__.

        Returns:
            str: Representación legible de la persona.
        """
        return self.__str__()
