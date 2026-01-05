from abc import ABC
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .models import Persona


class ArbolVisitorInterface(ABC):  # patron visitor
    """Clase que representa un visitante del árbol genealógico
    - Interfaz
    """

    def visitar(self, persona: "Persona"):
        pass


class PrintArbolVisitor(ArbolVisitorInterface):  # patron visitor concreto
    """Clase que representa un visitante del árbol genealógico que imprimira el árbol
    - Su estado interno es el string que está construyendo
    - Utiliza recursividad para añadir └— y ├—.
    """

    def __init__(self):
        self.resultado: list[str] = []
        self.visitados: set[int] = set()

    def visitar(self, persona: "Persona"):
        """
        Visita una persona y sus hijos de manera recursiva.
        Args:
            persona (Persona): La persona a visitar.
        """
        if persona.id not in self.visitados:
            # inicia el recorrido desde esta persona como raiz.
            self._visitar_recursivo(persona, es_ultimo=True, prefijos=[])

    def _visitar_recursivo(self, persona: "Persona", es_ultimo: bool, prefijos: list[str]):
        """
        Método auxiliar recursivo que realiza la impresión real.

        Args:
            persona (Persona): La persona a visitar.
            es_ultimo (bool): Indica si es el ultimo hijo de su padre.
            prefijos (list[str]): Prefijos para la impresión.
        """
        # Protección contra ciclos y llamadas duplicadas
        # (aunque visitar() ya filtra, este método debe ser seguro por sí mismo)
        if persona.id in self.visitados:  # Defense in Depth
            return

        # construir el prefijo concatenando los prefijos
        prefijo_completo = "".join(prefijos)

        # Elegir símbolo: └─ para último hijo, ├─ para hijos intermedios
        simbolo = "└─" if es_ultimo else "├─"

        # Construir la línea con información de la persona
        persona_id = f" (id: {persona.id})" if persona.id else ""
        pareja_str = f"-> {persona.pareja.id}" if persona.pareja else ""

        self.resultado.append(
            f"{prefijo_completo}{simbolo} {persona.nombre}{persona_id}{pareja_str}"
        )
        self.visitados.add(persona.id)

        # hijos que aún no han sido visitados
        hijos_no_visitados = [h for h in persona.hijos if h.id not in self.visitados]

        # recorrer hijos no visitados
        for i, hijo in enumerate(hijos_no_visitados):
            es_ultimo_hijo = i == len(hijos_no_visitados) - 1

            # crear prefijos para el siguiente nivel
            nuevos_prefijos = prefijos.copy()
            nuevo_prefijo = "│  " if not es_ultimo else "   "

            nuevos_prefijos.append(nuevo_prefijo)

            # llamada recursiva
            self._visitar_recursivo(hijo, es_ultimo_hijo, nuevos_prefijos)

    def ejecutar(self, persona: "Persona"):
        self.visitar(persona)
        return "\n".join(self.resultado)

    def get_resultado(self):
        if not self.resultado:
            return "No hay personajes registrados."
        return "\n".join(self.resultado)


class SearchArbolVisitor(ArbolVisitorInterface):  # patron visitor concreto
    """Clase que representa un visitante del árbol genealógico que buscara una persona
    - Su estado es el resultado de la búsqueda.
    - No imprime nada, solo acumula nodos que cumplan un criterio.
    """

    def __init__(self, nombre_a_buscar: str):
        self.resultado: list["Persona"] = []
        self.nombre_a_buscar: str = nombre_a_buscar.strip().lower()
        self.visitados: set[int] = set()

    def visitar(self, persona: "Persona"):
        if persona.id in self.visitados:
            return

        self.visitados.add(persona.id)

        if persona.nombre.strip().lower() == self.nombre_a_buscar:
            self.resultado.append(persona)

        for hijo in persona.hijos:
            hijo.accept_visitor(self)

    def obtener_resultado(self):
        """
        Returns the result stored in the object.
        Retorna el resultado almacenado en el objeto.

        Este método recupera el valor del resultado almacenado internamente en el
        objeto. No modifica ni altera el valor almacenado y sirve como un simple
        accessor.

        Returns:
            list[Persona]: Lista de personas que cumplen con el criterio de búsqueda.
        """
        return self.resultado
