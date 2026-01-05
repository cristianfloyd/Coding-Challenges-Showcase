from typing import TYPE_CHECKING

from .models import Persona
from .validators import FamilyValidator

if TYPE_CHECKING:
    from .visitors import ArbolVisitorInterface


class ArbolGenealogico:  # funcionará como repositorio de personas
    """Clase que representa el árbol genealógico"""

    def __init__(self):
        self.personas: dict[int, Persona] = {}
        self._proximo_id: int = 1

    def registrar_persona(self, nombre: str):
        """
        Registra una nueva persona en el arbol.

        Genera un identificador unico para la persona, valida el identificador
        y crea un nuevo objeto persona
        Args:
            nombre (str): El nombre a registrar.

        Raises:
            ValueError: Si el ID generado no es válido o se viola alguna restricción de validación.

        Returns:
            Persona: El objeto persona recién registrado.
        """
        nuevo_id = self._proximo_id
        try:
            validador = FamilyValidator(self.personas)
            validador.validar_id(nuevo_id)
            nueva_persona = Persona(nuevo_id, nombre)
            self.personas[nuevo_id] = nueva_persona
            self._proximo_id += 1
            return nueva_persona
        except ValueError as e:
            raise ValueError(f"Error al registrar persona: {e}")

    def init_get_root(self) -> list["Persona"]:
        """Buscamos en nuestro diccionario de personas aquellas que no tienen padres asignados."""
        return [p for p in self.personas.values() if p.padres[0] is None and p.padres[1] is None]

    def get_persona(self, persona_id: int) -> "Persona":
        """Devuelve la persona con el ID especificado.
        Lanza ValueError si no existe.
        """
        if persona_id not in self.personas:
            raise ValueError(f"Persona con ID {persona_id} no encontrada")
        return self.personas[persona_id]

    def recorrer_arbol_completo(self, visitor: "ArbolVisitorInterface") -> None:
        """Refinamiento: El árbol sabe cómo ser recorrido íntegramente"""
        raices = self.init_get_root()
        for raiz in raices:
            raiz.accept_visitor(visitor)

    def add_hijo(self, padre: "Persona", hijo: "Persona") -> None:
        """Añade un hijo a una persona.

        Args:
            padre: La persona que será padre
            hijo: La persona que será hijo

        Raises:
            ValueError: Si la relación es inválida (ciclos, límite de padres, etc.)

        Example:
            >>> arbol = ArbolGenealogico()
            >>> padre = arbol.registrar_persona("Aenar")
            >>> hijo = arbol.registrar_persona("Gaemon")
            >>> arbol.add_hijo(padre, hijo)
        """
        try:
            validator = FamilyValidator(self.personas)
            validator.validar(padre, hijo, "hijo")
            padre.hijos.append(hijo)

            if hijo.padres[0] is None:
                hijo.padres = (padre, hijo.padres[1])
            elif hijo.padres[1] is None:
                hijo.padres = (hijo.padres[0], padre)

        except ValueError as e:
            raise ValueError(f"Error al añadir hijo: {e}")

    def add_pareja(self, persona1: "Persona", persona2: "Persona") -> None:
        """Añade una pareja a dos personas.
        Lanza ValueError si no es válido.
        """
        try:
            validator = FamilyValidator(self.personas)
            validator.validar(persona1, persona2, "pareja")
            persona1.pareja = persona2
            persona2.pareja = persona1
        except ValueError as e:
            raise ValueError(f"Error al añadir pareja: {e}")

    def remove_pareja(self, persona1: "Persona", persona2: "Persona") -> None:
        """Remueve una pareja de dos personas.
        Lanza ValueError si no es válido.
        """
        try:
            validator = FamilyValidator(self.personas)
            validator.validar(persona1, persona2, "remover_pareja")
            persona1.pareja = None
            persona2.pareja = None
        except ValueError as e:
            raise ValueError(f"Error al remover pareja: {e}")

    def eliminar_persona(self, persona_id: int, confirmar_rotura: bool = False) -> None:
        """Elimina una persona.
        Lanza ValueError si no es válido.
        """
        if persona_id not in self.personas:
            raise ValueError(f"Persona con ID {persona_id} no encontrada")

        persona = self.personas[persona_id]

        # chequear impacto eliminacion
        if persona.hijos and not confirmar_rotura:
            validador = FamilyValidator(self.personas)
            validador.validar_impacto_eliminacion(persona)

        # 1 desvincular la pareja
        if persona.pareja:
            persona.pareja.pareja = None
            persona.pareja = None
        # 2 desvincular los padres
        for p in persona.padres:
            if p:
                p.hijos.remove(persona)

        # 3 desvincular los hijos
        for h in persona.hijos:
            p_lista: list[Persona | None] = list(h.padres)
            if p_lista[0] and p_lista[0].id == persona.id:
                p_lista[0] = None
            if p_lista[1] and p_lista[1].id == persona.id:
                p_lista[1] = None
            h.padres = (p_lista[0], p_lista[1])

        # 4 eliminar la persona
        del self.personas[persona_id]
