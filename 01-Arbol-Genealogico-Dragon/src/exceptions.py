"""
Módulo de excepciones personalizadas para el sistema de árbol genealógico.

Este módulo define una jerarquía de excepciones que permite un manejo
de errores más específico y expresivo, siguiendo principios SOLID y Clean Code.
"""

from typing import Literal


class ArbolGenealogicoError(Exception):
    """
    Excepción base para todos los errores del sistema de árbol genealógico.

    Esta clase sigue el principio de Open/Closed: es la base para todas las
    excepciones específicas, permitiendo extender el sistema sin modificar
    código existente.

    Attributes:
        message: Mensaje descriptivo del error
    """

    def __init__(self, message: str):
        """
        Inicializa la excepción con un mensaje descriptivo.

        Args:
            message: Mensaje descriptivo del error que ocurrió
        """
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        """Retorna el mensaje de error."""
        return self.message


class PersonaNoEncontradaError(ArbolGenealogicoError):
    """
    Excepción lanzada cuando una persona no se encuentra en el árbol.

    Esta excepción es específica para errores de búsqueda, permitiendo
    un manejo diferenciado de errores de "no encontrado" vs otros errores.

    Example:
        >>> raise PersonaNoEncontradaError(persona_id=42)
        PersonaNoEncontradaError: Persona con ID 42 no encontrada
    """

    def __init__(self, persona_id: int | None = None, message: str | None = None):
        """
        Inicializa la excepción de persona no encontrada.

        Args:
            persona_id: ID de la persona que no se encontró (opcional)
            message: Mensaje personalizado (opcional). Si no se proporciona,
                    se genera automáticamente usando el persona_id
        """
        if message is None:
            if persona_id is not None:
                message = f"Persona con ID {persona_id} no encontrada"
            else:
                message = "Persona no encontrada"

        super().__init__(message)
        self.persona_id = persona_id


class ValidacionError(ArbolGenealogicoError):
    """
    Excepción base para errores de validación.

    Esta clase agrupa todos los errores relacionados con validaciones,
    permitiendo manejar todos los errores de validación de manera uniforme
    si es necesario, o usar las excepciones específicas para casos particulares.

    Example:
        >>> raise ValidacionError("El ID debe ser positivo")
        ValidacionError: El ID debe ser positivo
    """

    pass


class IDInvalidoError(ValidacionError):
    """
    Excepción lanzada cuando un ID es inválido.

    Casos específicos:
    - ID nulo
    - ID no positivo
    - ID duplicado

    Example:
        >>> raise IDInvalidoError("El ID no puede ser nulo")
        IDInvalidoError: El ID no puede ser nulo
    """

    pass


class RelacionInvalidaError(ValidacionError):
    """
    Excepción lanzada cuando se intenta crear una relación inválida.

    Esta excepción cubre varios casos:
    - Relaciones que violan reglas de negocio
    - Relaciones que crearían ciclos
    - Relaciones que violan límites (ej: más de 2 padres)

    Attributes:
        persona1_nombre: Nombre de la primera persona involucrada
        persona2_nombre: Nombre de la segunda persona involucrada
        tipo_relacion: Tipo de relación que se intentó crear
    """

    def __init__(
        self,
        message: str,
        persona1_nombre: str | None = None,
        persona2_nombre: str | None = None,
        tipo_relacion: str | None = None,
    ):
        """
        Inicializa la excepción de relación inválida.

        Args:
            message: Mensaje descriptivo del error
            persona1_nombre: Nombre de la primera persona (opcional)
            persona2_nombre: Nombre de la segunda persona (opcional)
            tipo_relacion: Tipo de relación intentada (opcional)
        """
        super().__init__(message)
        self.persona1_nombre = persona1_nombre
        self.persona2_nombre = persona2_nombre
        self.tipo_relacion = tipo_relacion


class CicloTemporalError(RelacionInvalidaError):
    """
    Excepción lanzada cuando se detecta un ciclo temporal en el árbol.

    Un ciclo temporal ocurre cuando una persona sería ancestro de sí misma
    a través de una cadena de relaciones padre-hijo.

    Example:
        >>> raise CicloTemporalError("Aegon", "Viserys")
        CicloTemporalError: ¡Paradoja temporal! Aegon es ancestro de Viserys
    """

    def __init__(self, hijo_nombre: str, padre_nombre: str):
        """
        Inicializa la excepción de ciclo temporal.

        Args:
            hijo_nombre: Nombre de la persona que sería hijo
            padre_nombre: Nombre de la persona que sería padre
        """
        message = f"¡Paradoja temporal! {hijo_nombre} es ancestro de {padre_nombre}."
        super().__init__(
            message=message,
            persona1_nombre=hijo_nombre,
            persona2_nombre=padre_nombre,
            tipo_relacion="padre-hijo",
        )
        self.hijo_nombre = hijo_nombre
        self.padre_nombre = padre_nombre


class LimitePadresExcedidoError(RelacionInvalidaError):
    """
    Excepción lanzada cuando se intenta agregar un tercer padre a una persona.

    El sistema permite máximo 2 padres por persona (padre y madre).

    Example:
        >>> raise LimitePadresExcedidoError("Daenerys")
        LimitePadresExcedidoError: La persona Daenerys ya tiene 2 padres
    """

    def __init__(self, persona_nombre: str):
        """
        Inicializa la excepción de límite de padres excedido.

        Args:
            persona_nombre: Nombre de la persona que ya tiene 2 padres
        """
        message = f"La persona {persona_nombre} ya tiene 2 padres"
        super().__init__(
            message=message,
            persona1_nombre=persona_nombre,
            tipo_relacion="padre-hijo",
        )
        self.persona_nombre = persona_nombre


class RelacionIncestuosaError(RelacionInvalidaError):
    """
    Excepción lanzada cuando se intenta crear una relación incestuosa.

    Casos cubiertos:
    - Padre-hijo como pareja
    - Pareja como padre-hijo

    Example:
        >>> raise RelacionIncestuosaError("Aegon", "Rhaenyra", "pareja")
        RelacionIncestuosaError: Aegon y Rhaenyra no pueden ser pareja porque son padre-hijo
    """

    def __init__(
        self,
        persona1_nombre: str,
        persona2_nombre: str,
        tipo_intento: Literal["pareja", "padre-hijo"],
    ):
        """
        Inicializa la excepción de relación incestuosa.

        Args:
            persona1_nombre: Nombre de la primera persona
            persona2_nombre: Nombre de la segunda persona
            tipo_intento: Tipo de relación que se intentó crear ("pareja" o "padre-hijo")
        """
        tipos_validos = ["pareja", "padre-hijo"]

        if tipo_intento not in tipos_validos:
            raise ValueError(
                f"tipo_intento debe ser uno de {tipos_validos}, recibido: {tipo_intento}"
            )

        if tipo_intento == "pareja":
            message = (
                f"{persona1_nombre} y {persona2_nombre} no pueden ser pareja porque son padre-hijo"
            )
        else:  # padre-hijo
            message = (
                f"{persona1_nombre} y {persona2_nombre} no pueden ser padre-hijo porque son pareja"
            )

        super().__init__(
            message=message,
            persona1_nombre=persona1_nombre,
            persona2_nombre=persona2_nombre,
            tipo_relacion=tipo_intento,
        )


class ParejaNoExisteError(RelacionInvalidaError):
    """
    Excepción lanzada cuando se intenta remover una pareja que no existe.

    Casos cubiertos:
    - Una persona no tiene pareja
    - Las dos personas no son pareja entre sí

    Example:
        >>> raise ParejaNoExisteError("Aegon", "Rhaenyra")
        ParejaNoExisteError: Aegon y Rhaenyra no son pareja
    """

    def __init__(self, persona1_nombre: str, persona2_nombre: str, razon: str = "no son pareja"):
        """
        Inicializa la excepción de pareja no existe.

        Args:
            persona1_nombre: Nombre de la primera persona
            persona2_nombre: Nombre de la segunda persona
            razon: Razón por la que no pueden removerse como pareja
        """
        message = f"{persona1_nombre} y {persona2_nombre} {razon}"
        super().__init__(
            message=message,
            persona1_nombre=persona1_nombre,
            persona2_nombre=persona2_nombre,
            tipo_relacion="pareja",
        )


class EliminacionConDescendientesError(ArbolGenealogicoError):
    """
    Excepción lanzada cuando se intenta eliminar una persona con descendientes.

    Esta excepción indica que eliminar la persona dividirá el árbol
    y se requiere confirmación del usuario.

    Attributes:
        persona_nombre: Nombre de la persona a eliminar
        cantidad_hijos: Cantidad de hijos que tiene la persona
    """

    def __init__(self, persona_nombre: str, cantidad_hijos: int):
        """
        Inicializa la excepción de eliminación con descendientes.

        Args:
            persona_nombre: Nombre de la persona a eliminar
            cantidad_hijos: Cantidad de hijos que tiene
        """
        message = (
            f"ADVERTENCIA: {persona_nombre} tiene descendientes. "
            "Eliminar este nodo dividirá el árbol en dos y romperá el linaje. "
            "¿Desea continuar?"
        )
        super().__init__(message)
        self.persona_nombre = persona_nombre
        self.cantidad_hijos = cantidad_hijos
