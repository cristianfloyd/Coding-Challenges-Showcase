from typing import TYPE_CHECKING, Literal, overload

from .repository import ArbolGenealogico
from .utils.ui_logger import create_ui_logger
from .visitors import PrintArbolVisitor, SearchArbolVisitor

if TYPE_CHECKING:
    pass

# Inicializar logger de UI al nivel del módulo
# Esto sigue el patrón Singleton: una sola instancia para todo el módulo
_ui_logger = create_ui_logger("src.ui")


class DinastiaUI:
    def __init__(self, arbol_gen: "ArbolGenealogico") -> None:
        self.arbol = arbol_gen
        # Log de inicialización
        _ui_logger.info(
            f"UI inicializada con árbol que contiene {len(arbol_gen.personas)} personas"
        )

    def mostrar_menu_principal(self):
        """
        Muestra el menú principal de la aplicación de árbol genealógico e inicia el bucle
        principal de interacción con el usuario. Permite agregar, eliminar y buscar personas,
        gestionar hijos y parejas, mostrar el árbol y salir del programa.

        No recibe ni retorna ningún parámetro. Las acciones se efectúan en base
        a la opción elegida por el usuario en consola.
        """
        UIMessages.success("Bienvenido al sistema de árbol genealógico")
        _ui_logger.info("Sistema iniciado - Menú principal activo")

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

            _ui_logger.info(f"Usuario seleccionó opción: {opcion}")

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
                    _ui_logger.info("Usuario salió del sistema")
                    break
                case _:
                    print("Opción invalida. Intente de nuevo.")
                    _ui_logger.warning(f"Opción inválida ingresada: {opcion}")

    def agregar_persona(self):
        """
        Solicita un nombre de persona al usuario y registra una nueva persona en el árbol.
        Maneja errores de validación y muestra mensajes de éxito o error.
        """
        try:
            nombre = self.pedir_dato(mensaje="Ingrese el nombre de la persona: ", es_entero=False)
            _ui_logger.info(f"Intentando registrar persona: {nombre}")

            nuevo_registro = self.arbol.registrar_persona(nombre)

            UIMessages.success(f"Persona {nuevo_registro.nombre} registrada exitosamente.")
            UIMessages.success(f"\nID: {nuevo_registro.id}")
            _ui_logger.success(
                f"Persona registrada: {nuevo_registro.nombre} (ID: {nuevo_registro.id})"
            )
        except ValueError as e:
            UIMessages.error(str(e))
            _ui_logger.error(f"Error al registrar persona: {e}")

    def buscar_persona(self):
        """
        Busca una persona en el árbol genealógico por su nombre y muestra los resultados.
        Maneja errores de validación y muestra mensajes de éxito o error.
        """
        try:
            print("Ingrese el nombre de la persona a buscar:")
            nombre = self.pedir_dato(mensaje="Nombre: ", es_entero=False)
            _ui_logger.info(f"Buscando persona con nombre: {nombre}")

            visitor = SearchArbolVisitor(nombre)
            self.arbol.recorrer_arbol_completo(visitor)
            resultados = visitor.obtener_resultado()

            if not resultados:
                UIMessages.error("No se encontraron resultados.")
                _ui_logger.info(f"Búsqueda sin resultados para: {nombre}")
            else:
                UIMessages.success("Resultados:")
                _ui_logger.info(f"Búsqueda exitosa: {len(resultados)} resultado(s) encontrado(s)")
                for r in resultados:
                    UIMessages.success(f"- {r.nombre} ({r.id})")
                    _ui_logger.debug(f"Resultado encontrado: {r.nombre} (ID: {r.id})")
        except ValueError as e:
            UIMessages.error(str(e))
            _ui_logger.error(f"Error en búsqueda: {e}")

    def mostrar_arbol(self):
        """
        Muestra el árbol genealógico completo mediante un visitante.
        Maneja el caso en que el árbol esté vacío y muestra un mensaje de error.
        """
        try:
            _ui_logger.info("Mostrando árbol genealógico completo")
            visitor = PrintArbolVisitor()
            self.arbol.recorrer_arbol_completo(visitor)
            resultado = visitor.get_resultado()
            UIMessages.success(resultado)
            _ui_logger.info("Árbol mostrado exitosamente")
        except ValueError as e:
            UIMessages.error(str(e))
            _ui_logger.error(f"Error al mostrar árbol: {e}")

    def agregar_hijo(self):
        """
        Solicita IDs de padre e hijo y establece la relación.

        Imprime mensaje de éxito o error según el resultado.
        Los errores de validación se capturan y muestran al usuario.
        """
        try:
            padre_id = self.pedir_dato("Ingrese el ID del padre: ", True)
            hijo_id = self.pedir_dato("Ingrese el ID del hijo: ", True)
            _ui_logger.info(f"Intentando agregar relación padre-hijo: {padre_id} -> {hijo_id}")

            padre = self.arbol.get_persona(padre_id)
            hijo = self.arbol.get_persona(hijo_id)

            self.arbol.add_hijo(padre, hijo)
            UIMessages.success(f"Ahora {padre.nombre} es padre de {hijo.nombre}")
            _ui_logger.success(f"Relación padre-hijo creada: {padre.nombre} -> {hijo.nombre}")
        except ValueError as e:
            UIMessages.error(str(e))
            _ui_logger.error(f"Error al agregar hijo: {e}")

    def agregar_pareja(self):
        try:
            persona1_id = self.pedir_dato(
                mensaje="Ingrese el ID de la primera persona: ", es_entero=True
            )
            persona2_id = self.pedir_dato(
                mensaje="Ingrese el ID de la segunda persona: ", es_entero=True
            )
            _ui_logger.info(
                f"Intentando agregar relación de pareja: {persona1_id} <-> {persona2_id}"
            )

            persona1 = self.arbol.get_persona(persona1_id)
            persona2 = self.arbol.get_persona(persona2_id)
            self.arbol.add_pareja(persona1, persona2)
            UIMessages.success(f"Ahora {persona1.nombre} es pareja de {persona2.nombre}")
            _ui_logger.success(
                f"Relación de pareja creada: {persona1.nombre} <-> {persona2.nombre}"
            )
        except ValueError as e:
            UIMessages.error(str(e))
            _ui_logger.error(f"Error al agregar pareja: {e}")

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
            _ui_logger.info(
                f"Intentando eliminar relación de pareja: {persona1_id} <-> {persona2_id}"
            )

            persona1 = self.arbol.get_persona(persona1_id)
            persona2 = self.arbol.get_persona(persona2_id)
            self.arbol.remove_pareja(persona1, persona2)
            UIMessages.success(f"Ahora {persona1.nombre} no es pareja de {persona2.nombre}")
            _ui_logger.success(
                f"Relación de pareja eliminada: {persona1.nombre} <-> {persona2.nombre}"
            )
        except ValueError as e:
            UIMessages.error(str(e))
            _ui_logger.error(f"Error al eliminar pareja: {e}")

    def eliminar_persona(self):
        """
        Solicita un ID de persona y elimina la persona del árbol.
        Maneja errores de validación y muestra mensajes de éxito o error.
        """
        try:
            id_persona = self.pedir_dato("Ingrese el ID de la persona a eliminar: ", True)
            _ui_logger.info(f"Intentando eliminar persona con ID: {id_persona}")

            persona = self.arbol.get_persona(id_persona)
            try:
                self.arbol.eliminar_persona(id_persona)
                UIMessages.success(f"Persona {persona.nombre} eliminada exitosamente.")
                _ui_logger.success(f"Persona eliminada: {persona.nombre} (ID: {id_persona})")
            except ValueError as e:
                mensaje_error = str(e)
                if "ADVERTENCIA" in mensaje_error:
                    UIMessages.error(f"\n{mensaje_error}")
                    _ui_logger.warning(
                        f"Advertencia al eliminar persona {persona.nombre}: {mensaje_error}"
                    )
                    confirma = input("Desea continuar? (s/n): ").strip().lower()
                    if confirma == "s":
                        confirma = True
                        self.arbol.eliminar_persona(id_persona, confirma)
                        UIMessages.success(f"Persona {persona.nombre} eliminada exitosamente.")
                        _ui_logger.success(
                            f"Persona eliminada con confirmación: {persona.nombre} (ID: {id_persona})"
                        )
                    else:
                        UIMessages.error("Operación cancelada.")
                        _ui_logger.info(
                            f"Eliminación de persona {persona.nombre} cancelada por el usuario"
                        )
                else:
                    UIMessages.error(str(e))
                    _ui_logger.error(f"Error al eliminar persona: {e}")

        except ValueError as e:
            UIMessages.error(str(e))
            _ui_logger.error(f"Error al obtener persona para eliminar: {e}")


class UIMessages:
    """
    Clase para mensajes de UI con logging integrado.

    Mantiene la interfaz pública existente pero ahora usa logging
    en lugar de solo print(), mejorando trazabilidad y control.

    Esta clase sigue el principio de Single Responsibility: solo maneja
    la presentación de mensajes al usuario, delegando el logging técnico
    a UILogger.
    """

    @staticmethod
    def error(message: str) -> None:
        """
        Muestra un mensaje de error al usuario y lo registra en logs.

        Mantiene compatibilidad con código existente: sigue mostrando
        el mensaje en consola, pero ahora también lo registra para
        trazabilidad.

        Args:
            message: Mensaje de error a mostrar y registrar
        """
        error_msg = f"Error: {message}"
        print(error_msg)  # Mantener para UI interactiva
        _ui_logger.error(message)  # Logging para trazabilidad

    @staticmethod
    def success(message: str) -> None:
        """
        Muestra un mensaje de éxito al usuario y lo registra en logs.

        Mantiene compatibilidad con código existente: sigue mostrando
        el mensaje en consola, pero ahora también lo registra para
        trazabilidad.

        Args:
            message: Mensaje de éxito a mostrar y registrar
        """
        success_msg = f"✅ {message}"
        print(success_msg)  # Mantener para UI interactiva
        _ui_logger.success(message)  # Logging para trazabilidad
