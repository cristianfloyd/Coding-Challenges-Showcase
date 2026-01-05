from typing import TYPE_CHECKING

from .models import Persona
from .utils.logger import get_logger
from .validators import FamilyValidator

if TYPE_CHECKING:
    from .visitors import ArbolVisitorInterface

# Inicializar logger para este módulo
logger = get_logger(__name__)


class ArbolGenealogico:  # funcionará como repositorio de personas
    """Clase que representa el árbol genealógico"""

    def __init__(self):
        self.personas: dict[int, Persona] = {}
        self._proximo_id: int = 1
        logger.debug("Árbol genealógico inicializado (vacío)")

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
        logger.debug(f"Intentando registrar persona: {nombre} (ID asignado: {nuevo_id})")

        try:
            validador = FamilyValidator(self.personas)
            validador.validar_id(nuevo_id)
            nueva_persona = Persona(nuevo_id, nombre)
            self.personas[nuevo_id] = nueva_persona
            self._proximo_id += 1

            logger.info(f"Persona registrada exitosamente: {nueva_persona.nombre} (ID: {nuevo_id})")
            logger.debug(f"Total de personas en árbol: {len(self.personas)}")

            return nueva_persona
        except ValueError as e:
            logger.warning(f"Error al registrar persona '{nombre}': {e}")
            raise ValueError(f"Error al registrar persona: {e}")

    def init_get_root(self) -> list["Persona"]:
        """Buscamos en nuestro diccionario de personas aquellas que no tienen padres asignados."""
        raices = [p for p in self.personas.values() if p.padres[0] is None and p.padres[1] is None]
        logger.debug(f"Buscando raíces del árbol: {len(raices)} raíz(ces) encontrada(s)")
        return raices

    def get_persona(self, persona_id: int) -> "Persona":
        """Devuelve la persona con el ID especificado.
        Lanza ValueError si no existe.
        """
        logger.debug(f"Buscando persona con ID: {persona_id}")

        if persona_id not in self.personas:
            logger.warning(
                f"Persona con ID {persona_id} no encontrada (total personas: {len(self.personas)})"
            )
            raise ValueError(f"Persona con ID {persona_id} no encontrada")

        persona = self.personas[persona_id]
        logger.debug(f"Persona encontrada: {persona.nombre} (ID: {persona_id})")
        return persona

    def recorrer_arbol_completo(self, visitor: "ArbolVisitorInterface") -> None:
        """Refinamiento: El árbol sabe cómo ser recorrido íntegramente"""
        logger.debug(f"Recorriendo árbol completo con visitor: {type(visitor).__name__}")
        raices = self.init_get_root()

        for raiz in raices:
            logger.debug(f"Procesando raíz: {raiz.nombre}")
            raiz.accept_visitor(visitor)

        logger.debug("Recorrido del árbol completado")

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
        logger.debug(
            f"Intentando agregar relación padre-hijo: {padre.nombre} (ID: {padre.id}) -> {hijo.nombre} (ID: {hijo.id})"  # noqa: E501
        )

        try:
            validator = FamilyValidator(self.personas)
            validator.validar(padre, hijo, "hijo")

            padre.hijos.append(hijo)

            if hijo.padres[0] is None:
                hijo.padres = (padre, hijo.padres[1])
            elif hijo.padres[1] is None:
                hijo.padres = (hijo.padres[0], padre)

            logger.info(f"Relación padre-hijo creada exitosamente: {padre.nombre} -> {hijo.nombre}")
            logger.debug(
                f"Hijo ahora tiene {len([p for p in hijo.padres if p is not None])} padre(s)"
            )

        except ValueError as e:
            logger.warning(
                f"Error al añadir relación padre-hijo ({padre.nombre} -> {hijo.nombre}): {e}"
            )
            raise ValueError(f"Error al añadir hijo: {e}")

    def add_pareja(self, persona1: "Persona", persona2: "Persona") -> None:
        """Añade una pareja a dos personas.
        Lanza ValueError si no es válido.
        """
        logger.debug(
            f"Intentando agregar relación de pareja: {persona1.nombre} (ID: {persona1.id}) <-> {persona2.nombre} (ID: {persona2.id})"  # noqa: E501
        )

        try:
            validator = FamilyValidator(self.personas)
            validator.validar(persona1, persona2, "pareja")

            persona1.pareja = persona2
            persona2.pareja = persona1

            logger.info(
                f"Relación de pareja creada exitosamente: {persona1.nombre} <-> {persona2.nombre}"
            )

        except ValueError as e:
            logger.warning(
                f"Error al añadir relación de pareja ({persona1.nombre} <-> {persona2.nombre}): {e}"
            )
            raise ValueError(f"Error al añadir pareja: {e}")

    def remove_pareja(self, persona1: "Persona", persona2: "Persona") -> None:
        """Remueve una pareja de dos personas.
        Lanza ValueError si no es válido.
        """
        logger.debug(
            f"Intentando remover relación de pareja: {persona1.nombre} (ID: {persona1.id}) <-> {persona2.nombre} (ID: {persona2.id})"  # noqa: E501
        )

        try:
            validator = FamilyValidator(self.personas)
            validator.validar(persona1, persona2, "remover_pareja")

            persona1.pareja = None
            persona2.pareja = None

            logger.info(
                f"Relación de pareja removida exitosamente: {persona1.nombre} <-> {persona2.nombre}"
            )

        except ValueError as e:
            logger.warning(
                f"Error al remover relación de pareja ({persona1.nombre} <-> {persona2.nombre}): {e}"  # noqa: E501
            )
            raise ValueError(f"Error al remover pareja: {e}")

    def eliminar_persona(self, persona_id: int, confirmar_rotura: bool = False) -> None:
        """Elimina una persona.
        Lanza ValueError si no es válido.
        """
        logger.debug(
            f"Intentando eliminar persona con ID: {persona_id} (confirmar_rotura: {confirmar_rotura})"  # noqa: E501
        )

        if persona_id not in self.personas:
            logger.warning(f"Intento de eliminar persona inexistente (ID: {persona_id})")
            raise ValueError(f"Persona con ID {persona_id} no encontrada")

        persona = self.personas[persona_id]
        logger.debug(
            f"Persona a eliminar: {persona.nombre} (tiene {len(persona.hijos)} hijo(s), pareja: {persona.pareja is not None})"  # noqa: E501
        )

        # chequear impacto eliminacion
        if persona.hijos and not confirmar_rotura:
            logger.debug(f"Persona {persona.nombre} tiene descendientes, validando impacto")
            validador = FamilyValidator(self.personas)
            validador.validar_impacto_eliminacion(persona)

        # 1 desvincular la pareja
        if persona.pareja:
            logger.debug(f"Desvinculando pareja: {persona.nombre} <-> {persona.pareja.nombre}")
            persona.pareja.pareja = None
            persona.pareja = None

        # 2 desvincular los padres
        padres_desvinculados = 0
        for p in persona.padres:
            if p:
                p.hijos.remove(persona)
                padres_desvinculados += 1
        if padres_desvinculados > 0:
            logger.debug(f"Desvinculados {padres_desvinculados} padre(s) de {persona.nombre}")

        # 3 desvincular los hijos
        hijos_desvinculados = len(persona.hijos)
        for h in persona.hijos:
            p_lista: list[Persona | None] = list(h.padres)
            if p_lista[0] and p_lista[0].id == persona.id:
                p_lista[0] = None
            if p_lista[1] and p_lista[1].id == persona.id:
                p_lista[1] = None
            h.padres = (p_lista[0], p_lista[1])
        if hijos_desvinculados > 0:
            logger.debug(f"Desvinculados {hijos_desvinculados} hijo(s) de {persona.nombre}")

        # 4 eliminar la persona
        del self.personas[persona_id]
        logger.info(f"Persona eliminada exitosamente: {persona.nombre} (ID: {persona_id})")
        logger.debug(f"Total de personas restantes en árbol: {len(self.personas)}")
