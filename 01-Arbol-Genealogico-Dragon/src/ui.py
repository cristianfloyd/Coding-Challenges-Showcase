from typing import TYPE_CHECKING, Literal, overload

from .repository import ArbolGenealogico
from .visitors import PrintArbolVisitor, SearchArbolVisitor

if TYPE_CHECKING:
    pass


class DinastiaUI:
    def __init__(self, arbol_gen: "ArbolGenealogico") -> None:
        self.arbol = arbol_gen

    def mostrar_menu_principal(self):
        """
        Muestra el menú principal de la aplicación de árbol genealógico e inicia el bucle
        principal de interacción con el usuario. Permite agregar, eliminar y buscar personas,
        gestionar hijos y parejas, mostrar el árbol y salir del programa.

        No recibe ni retorna ningún parámetro. Las acciones se efectúan en base
        a la opción elegida por el usuario en consola.
        """

        UIMessages.success("Bienvenido al sistema de árbol genealógico")
        while True:
            print("\nMenu Principal")
            print("1. Agregar persona")
            print("2. Eliminar persona")
            print("3. Buscar persona")
            print("4. Mostrar arbol")
            print("5. Agregar hijo")
            print("6. Agregar pareja")
            print("7. Eliminar pareja")
            print("8. Salir")
            opcion = input("Ingrese una opción: ").strip().lower()

            match opcion:
                case "1":
                    self.agregar_persona()
                case "2":
                    self.eliminar_persona()
                case "3":
                    self.buscar_persona()
                case "4":
                    self.mostrar_arbol()
                case "5":
                    self.agregar_hijo()
                case "6":
                    self.agregar_pareja()
                case "7":
                    self.eliminar_pareja()
                case "8":
                    break
                case _:
                    print("Opción invalida. Intente de nuevo.")

    def agregar_persona(self):
        """
        Solicita un nombre de persona al usuario y registra una nueva persona en el árbol.
        Maneja errores de validación y muestra mensajes de éxito o error.
        """
        try:
            nombre = self.pedir_dato(mensaje="Ingrese el nombre de la persona: ", es_entero=False)
            nuevo_registro = self.arbol.registrar_persona(nombre)
            UIMessages.success(f"Persona {nuevo_registro.nombre} registrada exitosamente.")
            UIMessages.success(f"\nID: {nuevo_registro.id}")
        except ValueError as e:
            UIMessages.error(str(e))

    def buscar_persona(self):
        """
        Busca una persona en el árbol genealógico por su nombre y muestra los resultados.
        Maneja errores de validación y muestra mensajes de éxito o error.
        """
        try:
            print("Ingrese el nombre de la persona a buscar:")
            nombre = self.pedir_dato(mensaje="Nombre: ", es_entero=False)
            visitor = SearchArbolVisitor(nombre)
            self.arbol.recorrer_arbol_completo(visitor)
            resultados = visitor.obtener_resultado()
            if not resultados:
                UIMessages.error("No se encontraron resultados.")
            else:
                UIMessages.success("Resultados:")
                for r in resultados:
                    UIMessages.success(f"- {r.nombre} ({r.id})")
        except ValueError as e:
            UIMessages.error(str(e))

    def mostrar_arbol(self):
        """
        Muestra el árbol genealógico completo mediante un visitante.
        Maneja el caso en que el árbol esté vacío y muestra un mensaje de error.
        """
        try:
            visitor = PrintArbolVisitor()
            self.arbol.recorrer_arbol_completo(visitor)
            resultado = visitor.get_resultado()
            UIMessages.success(resultado)
        except ValueError as e:
            UIMessages.error(str(e))

    def agregar_hijo(self):
        """
        Solicita IDs de padre e hijo y establece la relación.

        Imprime mensaje de éxito o error según el resultado.
        Los errores de validación se capturan y muestran al usuario.
        """
        try:
            padre_id = self.pedir_dato("Ingrese el ID del padre: ", True)
            hijo_id = self.pedir_dato("Ingrese el ID del hijo: ", True)

            padre = self.arbol.get_persona(padre_id)
            hijo = self.arbol.get_persona(hijo_id)

            self.arbol.add_hijo(padre, hijo)
            UIMessages.success(f"Ahora {padre.nombre} es padre de {hijo.nombre}")
        except ValueError as e:
            UIMessages.error(str(e))

    def agregar_pareja(self):
        try:
            persona1_id = self.pedir_dato(
                mensaje="Ingrese el ID de la primera persona: ", es_entero=True
            )
            persona2_id = self.pedir_dato(
                mensaje="Ingrese el ID de la segunda persona: ", es_entero=True
            )

            persona1 = self.arbol.get_persona(persona1_id)
            persona2 = self.arbol.get_persona(persona2_id)
            self.arbol.add_pareja(persona1, persona2)
            UIMessages.success(f"Ahora {persona1.nombre} es pareja de {persona2.nombre}")
        except ValueError as e:
            UIMessages.error(str(e))

    @overload
    @staticmethod
    def pedir_dato(mensaje: str, es_entero: Literal[True]) -> int: ...

    @overload
    @staticmethod
    def pedir_dato(mensaje: str, es_entero: Literal[False]) -> str: ...

    @staticmethod
    def pedir_dato(mensaje: str, es_entero: bool = False) -> None | str | int:
        """
        Pide un dato al usuario.
        Args:
            mensaje (str): El mensaje a mostrar al usuario.
            es_entero (bool): Indica si el dato debe ser un entero.
        Returns:
            None | str | int: El dato ingresado por el usuario.
        """
        while True:
            dato = input(mensaje).strip()
            if not dato:
                UIMessages.error("El valor no puede estar vacío. Intente de nuevo.")
                continue
            if es_entero:
                try:
                    return int(dato)
                except ValueError:
                    UIMessages.error("El valor debe ser un entero. Intente de nuevo.")
                    continue
            return dato

    def eliminar_pareja(self):
        """
        Solicita IDs de dos personas y elimina la relación de pareja entre ellas.
        Maneja errores de validación y muestra mensajes de éxito o error.
        """
        try:
            persona1_id = self.pedir_dato("Ingrese el ID de la primera persona: ", True)
            persona2_id = self.pedir_dato("Ingrese el ID de la segunda persona: ", True)
            persona1 = self.arbol.get_persona(persona1_id)
            persona2 = self.arbol.get_persona(persona2_id)
            self.arbol.remove_pareja(persona1, persona2)
            UIMessages.success(f"Ahora {persona1.nombre} no es pareja de {persona2.nombre}")
        except ValueError as e:
            UIMessages.error(str(e))

    def eliminar_persona(self):
        """
        Solicita un ID de persona y elimina la persona del árbol.
        Maneja errores de validación y muestra mensajes de éxito o error.
        """
        try:
            id_persona = self.pedir_dato("Ingrese el ID de la persona a eliminar: ", True)
            persona = self.arbol.get_persona(id_persona)
            try:
                self.arbol.eliminar_persona(id_persona)
                UIMessages.success(f"Persona {persona.nombre} eliminada exitosamente.")
            except ValueError as e:
                mensaje_error = str(e)
                if "ADVERTENCIA" in mensaje_error:
                    UIMessages.error(f"\n{mensaje_error}")
                    confirma = input("Desea continuar? (s/n): ").strip().lower()
                    if confirma == "s":
                        confirma = True
                        self.arbol.eliminar_persona(id_persona, confirma)
                        UIMessages.success(f"Persona {persona.nombre} eliminada exitosamente.")
                    else:
                        UIMessages.error("Operación cancelada.")
                else:
                    UIMessages.error(str(e))

        except ValueError as e:
            UIMessages.error(str(e))


class UIMessages:
    @staticmethod
    def error(message: str) -> None:
        """Imprime un mensaje de error formateado."""
        print(f"Error: {message}")

    @staticmethod
    def success(message: str) -> None:
        """Imprime un mensaje de éxito formateado."""
        print(f"✅ {message}")
