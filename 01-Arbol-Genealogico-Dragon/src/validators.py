from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .models import Persona


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
                raise ValueError("Relacion no valida")

    def _validar_hijo(self, padre: "Persona", hijo: "Persona"):
        """
        Valida que la persona pueda ser hijo de otra persona
        """
        # regla 1: no puede ser su propio padre
        if padre.id == hijo.id:
            raise ValueError(f"{padre.nombre} no puede ser su propio padre")
        # regla 2: maximo 2 padres
        self._limite_padres(hijo)

        # regla 3: no puede ser pareja de su propio padre
        self._no_pareja_descendiente(hijo, padre)

        # regla 4: deteccion de ciclos, ej.:
        # A es hijo de B, B es hijo de C, C es hijo de A.
        # No crear bucles infinitos
        self._deteccion_ciclos(hijo, padre)

    def _limite_padres(self, persona: "Persona") -> None:
        """
        Valida que la persona no tenga más de 2 padres.
        Args:
            persona: La persona a validar
        Raises:
            ValueError: Si la persona ya tiene 2 padres
        """
        if persona.padres[0] is not None and persona.padres[1] is not None:
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
        if (hijo.pareja is not None) and (hijo.pareja.id == padre.id):
            raise ValueError(f"{hijo.nombre} no puede ser hijo de {padre.nombre} porque son pareja")
        if (padre.pareja is not None) and (padre.pareja.id == hijo.id):
            raise ValueError(f"{hijo.nombre} no puede ser hijo de {padre.nombre} porque son pareja")

    def _deteccion_ciclos(self, hijo: "Persona", padre: "Persona"):
        """
        Funcion recursiva que detecta ciclos en el arbol genealógico
        """
        if self._es_ancestro_de(hijo, padre):
            raise ValueError(f"¡Paradoja temporal! {hijo.nombre} es ancestro de {padre.nombre}.")

    def _es_ancestro_de(self, buscar: "Persona", inicio: "Persona") -> bool:
        """
        sube por el arbol desde 'inicio' buscando a 'buscar'
        """
        # Si no, busca recursivamente en los padres de los padres.
        for p in inicio.padres:
            if p is not None:
                if p.id == buscar.id or self._es_ancestro_de(buscar, p):
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
        if id_nuevo is None:
            raise ValueError("El id no puede ser nulo")

        if id_nuevo <= 0:
            raise ValueError(f"El id {id_nuevo} debe ser un entero positivo")

        if id_nuevo in self.personas_existentes:
            raise ValueError(f"El id {id_nuevo} ya pertenece a otra persona")

    def _validar_pareja(self, persona1: "Persona", persona2: "Persona") -> None:
        """Valida que persona1 y persona2 puedan ser pareja
        Args: persona1, persona2 (Persona)
        """
        if persona1.id == persona2.id:
            raise ValueError(f"{persona1.nombre} no puede ser su propia pareja")

        if persona1.pareja is not None:
            raise ValueError(f"{persona1.nombre} ya tiene una pareja: {persona1.pareja.nombre}.")
        if persona2.pareja is not None:
            raise ValueError(f"{persona2.nombre} ya tiene una pareja: {persona2.pareja.nombre}.")
        if persona1.id in [p.id for p in persona2.padres if p is not None]:
            raise ValueError(
                f"{persona1.nombre} es padre/madre de {persona2.nombre}. No pueden ser pareja."
            )

        # Verificar si persona2 es padre/madre de persona1
        if persona2.id in [p.id for p in persona1.padres if p is not None]:
            raise ValueError(
                f"{persona2.nombre} es padre/madre de {persona1.nombre}. No pueden ser pareja."
            )

    def _validar_remover_pareja(self, persona1: "Persona", persona2: "Persona") -> None:
        try:
            if persona1.pareja is None or persona2.pareja is None:
                raise ValueError(f"{persona1.nombre} o {persona2.nombre} no tiene pareja")
            if (persona1.pareja.id != persona2.id) or (persona2.pareja.id != persona1.id):
                raise ValueError(f"{persona1.nombre} y {persona2.nombre} no son pareja")
        except ValueError as e:
            raise ValueError(f"Error al validar remover pareja: {e}")

    @staticmethod
    def validar_impacto_eliminacion(persona: "Persona") -> None:
        if persona.hijos:
            raise ValueError(
                f"ADVERTENCIA: {persona.nombre} tiene descendientes. "
                "Eliminar este nodo dividirá el árbol en dos y romperá el linaje. "
                "¿Desea continuar?"
            )
