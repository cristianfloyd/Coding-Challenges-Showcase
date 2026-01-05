from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .visitors import ArbolVisitorInterface


class Persona:
    def __init__(
        self,
        person_id: int,
        nombre: str,
        pareja: Optional["Persona"] = None,
        hijos: Optional[list["Persona"]] = None,
    ):
        self.id = person_id
        self.nombre: str = nombre
        self.pareja: Optional["Persona"] = pareja or None
        self.hijos: list["Persona"] = hijos or []
        self.padres: tuple[Optional["Persona"], Optional["Persona"]] = (None, None)

    def accept_visitor(self, visitor: "ArbolVisitorInterface") -> None:
        visitor.visitar(self)

    def __str__(self):
        return f"{self.nombre} ({self.id})"

    def __repr__(self):
        return self.__str__()
