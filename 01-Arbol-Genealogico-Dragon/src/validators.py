from typing import TYPE_CHECKING, Optional

from .utils.logger import get_logger

if TYPE_CHECKING:
    from .models import Persona

# Inicializar logger para este módulo
logger = get_logger(__name__)


class FamilyValidator:  # funcionará como validador de relaciones
    """Clase que valida las relaciones entre personas.

    Esta clase maneja dos tipos de validaciones:
    - validar_id(): Valida identificadores antes de crear nuevas personas
    - validar(): Dispatcher que valida relaciones entre personas existentes
                 (pareja, hijo, etc.)

    Se mantienen separadas porque son contextos diferentes: una valida
    datos primitivos (ID), la otra valida relaciones complejas entre objetos.
    """

    def __init__(self, personas_existentes: dict[int, "Persona"]):
        self.personas_existentes: dict[int, "Persona"] = personas_existentes
        logger.debug(f"FamilyValidator inicializado con {len(personas_existentes)} personas")

    def validar(self, persona1: "Persona", persona2: "Persona", relacion: str):
        """
        Validar una relación entre dos personas.
        Args:
            persona1: La primera persona
            persona2: La segunda persona
            relacion: La relación a validar
        Raises:
            ValueError: Si la relación es inválida
        """
        logger.debug(
            f"Validando relación '{relacion}': {persona1.nombre} (ID: {persona1.id}) <-> {persona2.nombre} (ID: {persona2.id})" # noqa: E501
        )

        match relacion:
            case "eliminar_persona":
                self.validar_impacto_eliminacion(persona1)
            case "pareja":
                self._validar_pareja(persona1, persona2)
            case "remover_pareja":
                self._validar_remover_pareja(persona1, persona2)
            case "hijo":
                self._validar_hijo(persona1, persona2)
            case _:
                logger.error(f"Tipo de relación inválida: {relacion}")
                raise ValueError("Relacion no valida")

    def _validar_hijo(self, padre: "Persona", hijo: "Persona"):
        """
        Valida que la persona pueda ser hijo de otra persona
        """
        logger.debug(f"Validando relación padre-hijo: {padre.nombre} -> {hijo.nombre}")

        # regla 1: no puede ser su propio padre
        if padre.id == hijo.id:
            logger.warning(
                f"Intento de relación padre-hijo inválida: {padre.nombre} no puede ser su propio padre" # noqa: E501
            )
            raise ValueError(f"{padre.nombre} no puede ser su propio padre")
        # regla 2: maximo 2 padres
        self._limite_padres(hijo)

        # regla 3: no puede ser pareja de su propio padre
        self._no_pareja_descendiente(hijo, padre)

        # regla 4: deteccion de ciclos, ej.:
        # A es hijo de B, B es hijo de C, C es hijo de A.
        # No crear bucles infinitos
        self._deteccion_ciclos(hijo, padre)

        logger.debug(f"Validación padre-hijo exitosa: {padre.nombre} -> {hijo.nombre}")

    def _limite_padres(self, persona: "Persona") -> None:
        """
        Valida que la persona no tenga más de 2 padres.
        Args:
            persona: La persona a validar
        Raises:
            ValueError: Si la persona ya tiene 2 padres
        """
        padres_count = len([p for p in persona.padres if p is not None])
        logger.debug(f"Verificando límite de padres para {persona.nombre}: {padres_count}/2")

        if persona.padres[0] is not None and persona.padres[1] is not None:
            logger.warning(f"Límite de padres excedido para {persona.nombre}: ya tiene 2 padres")
            raise ValueError("La persona ya tiene 2 padres")

    def _no_pareja_descendiente(self, hijo: "Persona", padre: "Persona") -> None:
        """
        Valida que no exista una relación de pareja entre padre e hijo.

        Esta validación es la contrapartida de la verificación padre-hijo
        en _validar_pareja(). Juntas forman una validación bidireccional
        que previene relaciones incestuosas:

        - _validar_pareja(): Bloquea hacer pareja a personas que YA son padre-hijo
        - _no_pareja_descendiente(): Bloquea hacer padre-hijo a personas que YA son pareja

        Ejemplo bloqueado:
            Juan <-> María (son pareja)
            Intentar: Juan -> padre de María
            Resultado: ERROR

        Args:
            hijo: La persona que será hijo
            padre: La persona que será padre
        Raises:
            ValueError: Si existe relación de pareja entre ambos
        """
        logger.debug(f"Validando que {hijo.nombre} y {padre.nombre} no sean pareja")

        if (hijo.pareja is not None) and (hijo.pareja.id == padre.id):
            logger.warning(
                f"Relación inválida detectada: {hijo.nombre} y {padre.nombre} son pareja"
            )

            raise ValueError(f"{hijo.nombre} no puede ser hijo de {padre.nombre} porque son pareja")
        if (padre.pareja is not None) and (padre.pareja.id == hijo.id):
            logger.warning(
                f"Relación inválida detectada: {padre.nombre} y {hijo.nombre} son pareja"
            )

            raise ValueError(f"{hijo.nombre} no puede ser hijo de {padre.nombre} porque son pareja")

    def _deteccion_ciclos(self, hijo: "Persona", padre: "Persona"):
        """
        Funcion recursiva que detecta ciclos en el arbol genealógico
        """
        logger.debug(
            f"Buscando ciclos temporales: {hijo.nombre} podría ser ancestro de {padre.nombre}?"
        )

        if self._es_ancestro_de(hijo, padre):
            logger.error(f"¡Ciclo temporal detectado! {hijo.nombre} es ancestro de {padre.nombre}")
            raise ValueError(f"¡Paradoja temporal! {hijo.nombre} es ancestro de {padre.nombre}.")

        logger.debug(f"No se detectaron ciclos temporales entre {hijo.nombre} y {padre.nombre}")

    def _es_ancestro_de(self, buscar: "Persona", inicio: "Persona") -> bool:
        """
        sube por el arbol desde 'inicio' buscando a 'buscar'
        """
        logger.debug(f"Buscando si {buscar.nombre} es ancestro de {inicio.nombre}")
        # Si no, busca recursivamente en los padres de los padres.
        for p in inicio.padres:
            if p is not None:
                if p.id == buscar.id or self._es_ancestro_de(buscar, p):
                    logger.debug(f"¡Encontrado! {buscar.nombre} es ancestro de {inicio.nombre}")
                    return True
        return False

    def validar_id(self, id_nuevo: Optional[int]):
        """
        Valida un identificador antes de crear una nueva persona.

        Esta validación se mantiene separada de validar() porque:
        - Se ejecuta antes de que la Persona exista
        - Solo requiere validar un dato primitivo (int)
        - No necesita el dispatcher de relaciones

        Args:
            id_nuevo: El ID a validar

        Raises:
            ValueError: Si el ID es inválido, nulo, o ya existe
        """
        logger.debug(f"Validando ID: {id_nuevo}")

        if id_nuevo is None:
            logger.warning("Intento de usar ID nulo")
            raise ValueError("El id no puede ser nulo")

        if id_nuevo <= 0:
            logger.warning(f"ID inválido (debe ser positivo): {id_nuevo}")
            raise ValueError(f"El id {id_nuevo} debe ser un entero positivo")

        if id_nuevo in self.personas_existentes:
            persona_existente = self.personas_existentes[id_nuevo]
            logger.warning(f"ID {id_nuevo} ya existe: pertenece a {persona_existente.nombre}")
            raise ValueError(f"El id {id_nuevo} ya pertenece a otra persona")

        logger.debug(f"ID {id_nuevo} validado exitosamente")

    def _validar_pareja(self, persona1: "Persona", persona2: "Persona") -> None:
        """Valida que persona1 y persona2 puedan ser pareja
        Args: persona1, persona2 (Persona)
        """
        logger.debug(f"Validando relación de pareja: {persona1.nombre} <-> {persona2.nombre}")

        if persona1.id == persona2.id:
            logger.warning(f"Intento de relación de pareja consigo mismo: {persona1.nombre}")
            raise ValueError(f"{persona1.nombre} no puede ser su propia pareja")

        if persona1.pareja is not None:
            logger.warning(f"{persona1.nombre} ya tiene pareja: {persona1.pareja.nombre}")
            raise ValueError(f"{persona1.nombre} ya tiene una pareja: {persona1.pareja.nombre}.")

        if persona2.pareja is not None:
            logger.warning(f"{persona2.nombre} ya tiene pareja: {persona2.pareja.nombre}")
            raise ValueError(f"{persona2.nombre} ya tiene una pareja: {persona2.pareja.nombre}.")

        if persona1.id in [p.id for p in persona2.padres if p is not None]:
            logger.warning(
                f"Relación padre-hijo detectada: {persona1.nombre} es padre de {persona2.nombre}"
            )
            raise ValueError(
                f"{persona1.nombre} es padre/madre de {persona2.nombre}. No pueden ser pareja."
            )

        if persona2.id in [p.id for p in persona1.padres if p is not None]:
            logger.warning(
                f"Relación padre-hijo detectada: {persona2.nombre} es padre de {persona1.nombre}"
            )
            raise ValueError(
                f"{persona2.nombre} es padre/madre de {persona1.nombre}. No pueden ser pareja."
            )

        logger.debug(f"Validación de pareja exitosa: {persona1.nombre} <-> {persona2.nombre}")

    def _validar_remover_pareja(self, persona1: "Persona", persona2: "Persona") -> None:
        """
        Valida que persona1 y persona2 puedan ser removidas de su pareja.
        Args: persona1, persona2 (Persona)
        """
        logger.debug(f"Validando remover pareja: {persona1.nombre} <-> {persona2.nombre}")

        try:
            if persona1.pareja is None or persona2.pareja is None:
                logger.warning(
                    "Intento de remover pareja cuando una persona no tiene pareja asignada"
                )
                raise ValueError(f"{persona1.nombre} o {persona2.nombre} no tiene pareja")

            if (persona1.pareja.id != persona2.id) or (persona2.pareja.id != persona1.id):
                logger.warning(
                    f"{persona1.nombre} y {persona2.nombre} no son pareja según registros"
                )
                raise ValueError(f"{persona1.nombre} y {persona2.nombre} no son pareja")

            logger.debug("Validación para remover pareja exitosa")
        except ValueError as e:
            logger.warning(f"Error al validar remover pareja: {e}")
            raise ValueError(f"Error al validar remover pareja: {e}")

    @staticmethod
    def validar_impacto_eliminacion(persona: "Persona") -> None:
        """
        Valida el impacto de eliminar una persona.
        Args: persona (Persona)
        """
        logger.debug(f"Validando impacto de eliminación para {persona.nombre}")

        if persona.hijos:
            logger.warning(
                f"Intento de eliminar persona con descendientes: {persona.nombre} tiene {len(persona.hijos)} hijo(s)" # noqa: E501
            )
            raise ValueError(
                f"ADVERTENCIA: {persona.nombre} tiene descendientes. "
                "Eliminar este nodo dividirá el árbol en dos y romperá el linaje. "
                "¿Desea continuar?"
            )

        logger.debug(f"Validación de impacto de eliminación exitosa para {persona.nombre}")
