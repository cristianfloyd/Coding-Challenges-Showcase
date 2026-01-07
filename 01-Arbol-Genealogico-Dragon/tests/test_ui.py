"""
Tests para el módulo ui.py

Cubre todos los métodos de DinastiaUI:
- pedir_dato (método estático)
- agregar_persona
- buscar_persona
- mostrar_arbol
- agregar_hijo
- agregar_pareja
- eliminar_pareja
- eliminar_persona
"""

from unittest.mock import MagicMock, patch

import pytest

from src.exceptions import (
    ArbolGenealogicoError,
    EliminacionConDescendientesError,
    IDInvalidoError,
)
from src.repository import ArbolGenealogico
from src.ui import DinastiaUI

# ==================== TESTS PARA pedir_dato ====================


class TestPedirDato:
    """Tests para el método estático pedir_dato"""

    @patch("builtins.input", return_value="Juan")
    @patch("src.ui.UIMessages.success")
    @patch("src.ui.UIMessages.error")
    def test_pedir_dato_string_exito(
        self, mock_success: MagicMock, mock_error: MagicMock, mock_input: MagicMock
    ):
        """
        Test: pedir_dato retorna string cuando es_entero=False

        Verifica que pedir_dato() retorna el string ingresado correctamente.
        """
        # ACT
        resultado = DinastiaUI.pedir_dato("Ingrese nombre: ", es_entero=False)

        # ASSERT
        assert resultado == "Juan"
        mock_input.assert_called_once_with("Ingrese nombre: ")
        mock_error.assert_not_called()

    @patch("builtins.input", return_value="123")
    @patch("src.ui.UIMessages.success")
    @patch("src.ui.UIMessages.error")
    def test_pedir_dato_entero_exito(
        self, mock_success: MagicMock, mock_error: MagicMock, mock_input: MagicMock
    ):
        """
        Test: pedir_dato retorna int cuando es_entero=True

        Verifica que pedir_dato() convierte correctamente a entero.
        """
        # ACT
        resultado = DinastiaUI.pedir_dato("Ingrese ID: ", es_entero=True)

        # ASSERT
        assert resultado == 123
        assert isinstance(resultado, int)
        mock_input.assert_called_once_with("Ingrese ID: ")
        mock_error.assert_not_called()

    @patch("builtins.input", side_effect=["", "Juan"])
    @patch("src.ui.UIMessages.error")
    @patch("src.ui.UIMessages.success")
    def test_pedir_dato_string_vacio_reintenta(
        self, mock_success: MagicMock, mock_error: MagicMock, mock_input: MagicMock
    ):
        """
        Test: pedir_dato rechaza valores vacíos y reintenta

        Verifica que pedir_dato() muestra mensaje de error y reintenta cuando
        el input está vacío.
        """
        # ACT
        resultado = DinastiaUI.pedir_dato("Ingrese nombre: ", es_entero=False)

        # ASSERT
        assert resultado == "Juan"
        assert mock_input.call_count == 2
        mock_error.assert_called_once_with("El valor no puede estar vacío. Intente de nuevo.")

        mock_success.assert_not_called()

    @patch("builtins.input", side_effect=["abc", "123"])
    @patch("src.ui.UIMessages.error")
    @patch("src.ui.UIMessages.success")
    def test_pedir_dato_entero_invalido_reintenta(
        self, mock_success: MagicMock, mock_error: MagicMock, mock_input: MagicMock
    ):
        """
        Test: pedir_dato rechaza strings no numéricos y reintenta

        Verifica que pedir_dato() muestra mensaje de error y reintenta cuando
        el input no es un entero válido.
        """
        # ACT
        resultado = DinastiaUI.pedir_dato("Ingrese ID: ", es_entero=True)

        # ASSERT
        assert resultado == 123
        assert mock_input.call_count == 2
        mock_error.assert_called_once_with("El valor debe ser un entero. Intente de nuevo.")

        mock_success.assert_not_called()

    @patch("builtins.input", side_effect=["", "", "Juan"])
    @patch("src.ui.UIMessages.error")
    @patch("src.ui.UIMessages.success")
    def test_pedir_dato_string_multiple_vacio_reintenta(
        self, mock_success: MagicMock, mock_error: MagicMock, mock_input: MagicMock
    ):
        """
        Test: pedir_dato maneja múltiples intentos vacíos

        Verifica que pedir_dato() sigue reintentando hasta recibir un valor válido.
        """
        # ACT
        resultado = DinastiaUI.pedir_dato("Ingrese nombre: ", es_entero=False)

        # ASSERT
        assert resultado == "Juan"
        assert mock_input.call_count == 3
        assert mock_error.call_count == 2  # Dos mensajes de error

        mock_success.assert_not_called()

    @patch("builtins.input", side_effect=["abc", "xyz", "456"])
    @patch("src.ui.UIMessages.error")
    @patch("src.ui.UIMessages.success")
    def test_pedir_dato_entero_multiple_invalido_reintenta(
        self, mock_success: MagicMock, mock_error: MagicMock, mock_input: MagicMock
    ):
        """
        Test: pedir_dato maneja múltiples intentos inválidos

        Verifica que pedir_dato() sigue reintentando hasta recibir un entero válido.
        """
        # ACT
        resultado = DinastiaUI.pedir_dato("Ingrese ID: ", es_entero=True)

        # ASSERT
        assert resultado == 456
        assert mock_input.call_count == 3
        assert mock_error.call_count == 2  # Dos mensajes de error

        mock_success.assert_not_called()


# ==================== TESTS PARA agregar_persona ====================


class TestAgregarPersona:
    """Tests para el método agregar_persona"""

    @patch("src.ui.DinastiaUI.pedir_dato", return_value="Rhaenyra")
    @patch("src.ui.UIMessages.error")
    @patch("src.ui.UIMessages.success")
    def test_agregar_persona_exito(
        self,
        mock_success: MagicMock,
        mock_error: MagicMock,
        mock_pedir_dato: MagicMock,
        arbol_vacio: ArbolGenealogico,
    ):
        """
        Test: Agregar persona exitosamente

        Verifica que agregar_persona() registra una persona y muestra mensaje de éxito.
        """
        # ARRANGE
        ui = DinastiaUI(arbol_vacio)

        # ACT
        ui.agregar_persona()

        # ASSERT
        mock_pedir_dato.assert_called_once_with(
            mensaje="Ingrese el nombre de la persona: ", es_entero=False
        )
        assert len(arbol_vacio.personas) == 1
        persona = arbol_vacio.get_persona(1)
        assert persona.nombre == "Rhaenyra"
        # Verificar que se imprimieron los mensajes de éxito
        assert mock_success.call_count == 2
        assert any("Rhaenyra" in str(call) for call in mock_success.call_args_list)
        assert any("registrada exitosamente" in str(call) for call in mock_success.call_args_list)

        mock_error.assert_not_called()

    @patch("src.ui.DinastiaUI.pedir_dato", return_value="")
    @patch("src.ui.UIMessages.success")
    @patch("src.ui.UIMessages.error")
    def test_agregar_persona_error_validacion(
        self,
        mock_error: MagicMock,
        mock_success: MagicMock,
        mock_pedir_dato: MagicMock,
        arbol_vacio: ArbolGenealogico,
    ):
        """Test: Agregar persona con error de validación"""
        # ARRANGE
        ui = DinastiaUI(arbol_vacio)
        error_msg = "Error de validación"

        with patch.object(arbol_vacio, "registrar_persona", side_effect=IDInvalidoError(error_msg)):
            # ACT
            ui.agregar_persona()

            # ASSERT
            mock_error.assert_called_once_with(error_msg)
            mock_success.assert_not_called()


# ==================== TESTS PARA buscar_persona ====================


class TestBuscarPersona:
    """Tests para el método buscar_persona"""

    @patch("src.ui.DinastiaUI.pedir_dato", return_value="Padre")
    @patch("src.ui.UIMessages.error")
    @patch("src.ui.UIMessages.success")
    def test_buscar_persona_encontrada(
        self,
        mock_success: MagicMock,
        mock_error: MagicMock,
        mock_pedir_dato: MagicMock,
        arbol_con_datos: ArbolGenealogico,
    ):
        """
        Test: Buscar persona que existe

        Verifica que buscar_persona() encuentra y muestra la persona correctamente.
        """
        # ARRANGE
        ui = DinastiaUI(arbol_con_datos)

        # ACT
        ui.buscar_persona()

        # ASSERT
        mock_pedir_dato.assert_called_once_with(mensaje="Nombre: ", es_entero=False)
        # Verificar que se imprimió "Resultados:" y la persona encontrada
        assert mock_success.call_count == 2
        assert any("Resultados:" in str(call) for call in mock_success.call_args_list)
        assert any("Padre" in str(call) for call in mock_success.call_args_list)
        mock_error.assert_not_called()

    @patch("src.ui.DinastiaUI.pedir_dato", return_value="Inexistente")
    @patch("src.ui.UIMessages.error")
    @patch("src.ui.UIMessages.success")
    def test_buscar_persona_no_encontrada(
        self,
        mock_success: MagicMock,
        mock_error: MagicMock,
        mock_pedir_dato: MagicMock,
        arbol_con_datos: ArbolGenealogico,
    ):
        """
        Test: Buscar persona que no existe

        Verifica que buscar_persona() muestra mensaje cuando no encuentra resultados.
        """
        # ARRANGE
        ui = DinastiaUI(arbol_con_datos)

        # ACT
        ui.buscar_persona()

        # ASSERT
        mock_error.assert_called_once_with("No se encontraron resultados.")
        mock_success.assert_not_called()

    @patch("src.ui.DinastiaUI.pedir_dato", return_value="Padre")
    @patch("src.ui.UIMessages.error")
    @patch("src.ui.UIMessages.success")
    def test_buscar_persona_multiple_resultados(
        self,
        mock_success: MagicMock,
        mock_error: MagicMock,
        mock_pedir_dato: MagicMock,
        arbol_vacio: ArbolGenealogico,
    ):
        """
        Test: Buscar persona con múltiples resultados

        Verifica que buscar_persona() muestra todos los resultados encontrados.
        """
        # ARRANGE
        ui = DinastiaUI(arbol_vacio)
        # Crear dos personas con el mismo nombre
        arbol_vacio.registrar_persona("Padre")
        arbol_vacio.registrar_persona("Padre")

        # ACT
        ui.buscar_persona()

        # ASSERT
        assert mock_success.call_count == 3
        assert any("Resultados:" in str(call) for call in mock_success.call_args_list)
        assert any("Padre" in str(call) for call in mock_success.call_args_list)
        mock_error.assert_not_called()


# ==================== TESTS PARA mostrar_arbol ====================


class TestMostrarArbol:
    """Tests para el método mostrar_arbol"""

    @patch("src.ui.UIMessages.error")
    @patch("src.ui.UIMessages.success")
    def test_mostrar_arbol_con_datos(
        self,
        mock_success: MagicMock,
        mock_error: MagicMock,
        arbol_con_datos: ArbolGenealogico,
    ):
        """
        Test: Mostrar árbol con datos

        Verifica que mostrar_arbol() imprime el árbol correctamente.
        """
        # ARRANGE
        ui = DinastiaUI(arbol_con_datos)

        # ACT
        ui.mostrar_arbol()

        # ASSERT
        mock_success.assert_called_once()
        # Verificar que se imprimió algo (el resultado del visitor)
        call_args = mock_success.call_args[0][0]
        assert "Padre" in call_args or "Madre" in call_args or "Hijo" in call_args
        mock_error.assert_not_called()

    @patch("builtins.print")
    def test_mostrar_arbol_vacio(
        self,
        mock_print: MagicMock,
        arbol_vacio: ArbolGenealogico,
    ):
        """
        Test: Mostrar árbol vacío

        Verifica que mostrar_arbol() maneja árbol vacío correctamente.
        """
        # ARRANGE
        ui = DinastiaUI(arbol_vacio)

        # ACT
        ui.mostrar_arbol()

        # ASSERT
        mock_print.assert_called_once()
        call_args = mock_print.call_args[0][0]
        assert "No hay personajes registrados" in call_args


# ==================== TESTS PARA agregar_hijo ====================


class TestAgregarHijo:
    """Tests para el método agregar_hijo"""

    @patch("src.ui.DinastiaUI.pedir_dato", side_effect=[1, 2])
    @patch("src.ui.UIMessages.error")
    @patch("src.ui.UIMessages.success")
    def test_agregar_hijo_exito(
        self,
        mock_success: MagicMock,
        mock_error: MagicMock,
        mock_pedir_dato: MagicMock,
        arbol_vacio: ArbolGenealogico,
    ):
        """
        Test: Agregar hijo exitosamente

        Verifica que agregar_hijo() establece la relación padre-hijo correctamente.
        """
        # ARRANGE
        ui = DinastiaUI(arbol_vacio)
        padre = arbol_vacio.registrar_persona("Padre")
        hijo = arbol_vacio.registrar_persona("Hijo")

        # ACT
        ui.agregar_hijo()

        # ASSERT
        assert mock_pedir_dato.call_count == 2
        assert hijo in padre.hijos
        mock_success.assert_called_once_with(f"Ahora {padre.nombre} es padre de {hijo.nombre}")
        mock_error.assert_not_called()

    @patch("src.ui.DinastiaUI.pedir_dato", side_effect=[1, 999])
    @patch("src.ui.UIMessages.error")
    @patch("src.ui.UIMessages.success")
    def test_agregar_hijo_error_persona_no_existe(
        self,
        mock_success: MagicMock,
        mock_error: MagicMock,
        mock_pedir_dato: MagicMock,
        arbol_vacio: ArbolGenealogico,
    ):
        """
        Test: Agregar hijo con error (persona no existe)

        Verifica que agregar_hijo() maneja errores cuando la persona no existe.
        """
        # ARRANGE
        ui = DinastiaUI(arbol_vacio)
        arbol_vacio.registrar_persona("Padre")

        # ACT
        ui.agregar_hijo()

        # ASSERT
        mock_error.assert_called_once()
        mock_success.assert_not_called()


# ==================== TESTS PARA agregar_pareja ====================


class TestAgregarPareja:
    """Tests para el método agregar_pareja"""

    @patch("src.ui.DinastiaUI.pedir_dato", side_effect=[1, 2])
    @patch("src.ui.UIMessages.error")
    @patch("src.ui.UIMessages.success")
    def test_agregar_pareja_exito(
        self,
        mock_success: MagicMock,
        mock_error: MagicMock,
        mock_pedir_dato: MagicMock,
        arbol_vacio: ArbolGenealogico,
    ):
        """
        Test: Agregar pareja exitosamente

        Verifica que agregar_pareja() establece la relación correctamente.
        """
        # ARRANGE
        ui = DinastiaUI(arbol_vacio)
        persona1 = arbol_vacio.registrar_persona("Persona 1")
        persona2 = arbol_vacio.registrar_persona("Persona 2")

        # ACT
        ui.agregar_pareja()

        # ASSERT
        assert mock_pedir_dato.call_count == 2
        assert persona1.pareja == persona2
        assert persona2.pareja == persona1
        mock_success.assert_called_once_with(
            f"Ahora {persona1.nombre} es pareja de {persona2.nombre}"
        )
        mock_error.assert_not_called()

    @patch("src.ui.DinastiaUI.pedir_dato", side_effect=[1, 1])
    @patch("src.ui.UIMessages.error")
    @patch("src.ui.UIMessages.success")
    def test_agregar_pareja_error_validacion(
        self,
        mock_success: MagicMock,
        mock_error: MagicMock,
        mock_pedir_dato: MagicMock,
        arbol_vacio: ArbolGenealogico,
    ):
        """
        Test: Agregar pareja con error de validación

        Verifica que agregar_pareja() maneja errores de validación.
        """
        # ARRANGE
        ui = DinastiaUI(arbol_vacio)
        arbol_vacio.registrar_persona("Persona")

        # ACT
        ui.agregar_pareja()

        # ASSERT
        mock_error.assert_called_once()
        mock_success.assert_not_called()

    @patch("src.ui.DinastiaUI.pedir_dato", side_effect=[1, 999])
    @patch("src.ui.UIMessages.error")
    @patch("src.ui.UIMessages.success")
    def test_agregar_pareja_error_persona_no_existe(
        self,
        mock_success: MagicMock,
        mock_error: MagicMock,
        mock_pedir_dato: MagicMock,
        arbol_vacio: ArbolGenealogico,
    ):
        """
        Test: Agregar pareja con error (persona no existe)

        Verifica que agregar_pareja() maneja errores cuando la persona no existe.
        """
        # ARRANGE
        ui = DinastiaUI(arbol_vacio)
        arbol_vacio.registrar_persona("Persona 1")

        # ACT
        ui.agregar_pareja()

        # ASSERT
        mock_error.assert_called_once()
        assert "999" in str(mock_error.call_args[0][0])
        assert "no encontrada" in str(mock_error.call_args[0][0])
        mock_success.assert_not_called()


# ==================== TESTS PARA eliminar_pareja ====================


class TestEliminarPareja:
    """Tests para el método eliminar_pareja"""

    @patch("src.ui.DinastiaUI.pedir_dato", side_effect=[1, 2])
    @patch("src.ui.UIMessages.error")
    @patch("src.ui.UIMessages.success")
    def test_eliminar_pareja_exito(
        self,
        mock_success: MagicMock,
        mock_error: MagicMock,
        mock_pedir_dato: MagicMock,
        arbol_vacio: ArbolGenealogico,
    ):
        """
        Test: Eliminar pareja exitosamente

        Verifica que eliminar_pareja() elimina la relación correctamente.
        """
        # ARRANGE
        ui = DinastiaUI(arbol_vacio)
        persona1 = arbol_vacio.registrar_persona("Persona 1")
        persona2 = arbol_vacio.registrar_persona("Persona 2")
        arbol_vacio.add_pareja(persona1, persona2)

        # ACT
        ui.eliminar_pareja()

        # ASSERT
        assert mock_pedir_dato.call_count == 2
        assert persona1.pareja is None
        assert persona2.pareja is None
        mock_success.assert_called_once_with(
            f"Ahora {persona1.nombre} no es pareja de {persona2.nombre}"
        )
        mock_error.assert_not_called()

    @patch("src.ui.DinastiaUI.pedir_dato", side_effect=[1, 2])
    @patch("src.ui.UIMessages.error")
    @patch("src.ui.UIMessages.success")
    def test_eliminar_pareja_error_no_son_parejas(
        self,
        mock_success: MagicMock,
        mock_error: MagicMock,
        mock_pedir_dato: MagicMock,
        arbol_vacio: ArbolGenealogico,
    ):
        """
        Test: Eliminar pareja con error (no son parejas)

        Verifica que eliminar_pareja() maneja errores cuando no son parejas.
        """
        # ARRANGE
        ui = DinastiaUI(arbol_vacio)
        arbol_vacio.registrar_persona("Persona 1")
        arbol_vacio.registrar_persona("Persona 2")

        # ACT
        ui.eliminar_pareja()

        # ASSERT
        mock_error.assert_called_once()
        assert "no tiene pareja" in str(mock_error.call_args[0][0])
        mock_success.assert_not_called()

    @patch("src.ui.DinastiaUI.pedir_dato", side_effect=[999, 1])
    @patch("src.ui.UIMessages.error")
    @patch("src.ui.UIMessages.success")
    def test_eliminar_pareja_error_persona_no_existe(
        self,
        mock_success: MagicMock,
        mock_error: MagicMock,
        mock_pedir_dato: MagicMock,
        arbol_vacio: ArbolGenealogico,
    ):
        """
        Test: Eliminar pareja con error (persona no existe)

        Verifica que eliminar_pareja() maneja errores cuando la persona no existe.
        """
        # ARRANGE
        ui = DinastiaUI(arbol_vacio)
        arbol_vacio.registrar_persona("Persona 1")

        # ACT
        ui.eliminar_pareja()

        # ASSERT
        mock_error.assert_called_once()
        assert "999" in str(mock_error.call_args[0][0])
        mock_success.assert_not_called()


# ==================== TESTS PARA eliminar_persona ====================


class TestEliminarPersona:
    """Tests para el método eliminar_persona"""

    @patch("src.ui.DinastiaUI.pedir_dato", return_value=1)
    @patch("src.ui.UIMessages.error")
    @patch("src.ui.UIMessages.success")
    def test_eliminar_persona_exito(
        self,
        mock_success: MagicMock,
        mock_error: MagicMock,
        mock_pedir_dato: MagicMock,
        arbol_con_persona_simple: ArbolGenealogico,
    ):
        """
        Test: Eliminar persona sin hijos exitosamente

        Verifica que eliminar_persona() elimina la persona correctamente.
        """
        # ARRANGE
        ui = DinastiaUI(arbol_con_persona_simple)
        persona_id = 1

        # ACT
        ui.eliminar_persona()

        # ASSERT
        mock_pedir_dato.assert_called_once_with("Ingrese el ID de la persona a eliminar: ", True)
        assert persona_id not in arbol_con_persona_simple.personas
        mock_success.assert_called_once_with("Persona Persona 1 eliminada exitosamente.")
        mock_error.assert_not_called()

    @patch("src.ui.DinastiaUI.pedir_dato", return_value=1)
    @patch("builtins.input", return_value="s")
    @patch("src.ui.UIMessages.error")
    @patch("src.ui.UIMessages.success")
    def test_eliminar_persona_con_hijos_confirma(
        self,
        mock_success: MagicMock,
        mock_error: MagicMock,
        mock_input: MagicMock,
        mock_pedir_dato: MagicMock,
        arbol_con_datos: ArbolGenealogico,
    ):
        """
        Test: Eliminar persona con hijos y confirmación

        Verifica que eliminar_persona() solicita confirmación y elimina si se confirma.
        """
        # ARRANGE
        ui = DinastiaUI(arbol_con_datos)
        persona = arbol_con_datos.get_persona(1)  # Padre que tiene hijos

        # ACT
        ui.eliminar_persona()

        # ASSERT
        mock_pedir_dato.assert_called_once_with("Ingrese el ID de la persona a eliminar: ", True)
        mock_input.assert_called_once_with("Desea continuar? (s/n): ")
        assert persona.id not in arbol_con_datos.personas
        # Verificar que se imprimió el mensaje de eliminación exitosa
        assert mock_success.call_count == 1
        mock_success.assert_called_once_with(f"Persona {persona.nombre} eliminada exitosamente.")

        assert mock_error.call_count == 1
        # Verificar que el mensaje contiene información sobre descendientes
        error_message = mock_error.call_args[0][0]
        assert "tiene descendientes" in error_message or "ADVERTENCIA" in error_message

    @patch("src.ui.DinastiaUI.pedir_dato", return_value=1)
    @patch("builtins.input", return_value="n")
    @patch("src.ui.UIMessages.error")
    @patch("src.ui.UIMessages.success")
    def test_eliminar_persona_con_hijos_cancela(
        self,
        mock_success: MagicMock,
        mock_error: MagicMock,
        mock_input: MagicMock,
        mock_pedir_dato: MagicMock,
        arbol_con_datos: ArbolGenealogico,
    ):
        """
        Test: Eliminar persona con hijos y cancelación

        Verifica que eliminar_persona() cancela la operación si el usuario no confirma.
        """
        # ARRANGE
        ui = DinastiaUI(arbol_con_datos)
        persona_id = 1  # Padre que tiene hijos

        # ACT
        ui.eliminar_persona()

        # ASSERT
        mock_pedir_dato.assert_called_once_with("Ingrese el ID de la persona a eliminar: ", True)
        mock_input.assert_called_once_with("Desea continuar? (s/n): ")
        # La persona NO debería ser eliminada
        assert persona_id in arbol_con_datos.personas
        mock_error.assert_any_call("Operación cancelada.")
        mock_success.assert_not_called()

    @patch("src.ui.DinastiaUI.pedir_dato", return_value=999)
    @patch("builtins.print")
    def test_eliminar_persona_error_no_existe(
        self,
        mock_print: MagicMock,
        mock_pedir_dato: MagicMock,
        arbol_vacio: ArbolGenealogico,
    ):
        """
        Test: Eliminar persona que no existe

        Verifica que eliminar_persona() maneja errores cuando la persona no existe.
        """
        # ARRANGE
        ui = DinastiaUI(arbol_vacio)

        # ACT
        ui.eliminar_persona()

        # ASSERT
        mock_print.assert_called_once()
        assert "Error:" in str(mock_print.call_args[0][0])

    @patch("src.ui.DinastiaUI.pedir_dato", return_value=1)
    @patch("builtins.input", return_value="s")
    @patch("builtins.print")
    def test_eliminar_persona_con_advertencia(
        self,
        mock_print: MagicMock,
        mock_input: MagicMock,
        mock_pedir_dato: MagicMock,
        arbol_vacio: ArbolGenealogico,
    ):
        """
        Test: Eliminar persona con mensaje de ADVERTENCIA

        Verifica que eliminar_persona() maneja correctamente mensajes con "ADVERTENCIA".
        """
        # ARRANGE
        ui = DinastiaUI(arbol_vacio)
        padre = arbol_vacio.registrar_persona("Padre")
        hijo = arbol_vacio.registrar_persona("Hijo")
        arbol_vacio.add_hijo(padre, hijo)

        # Simular que el validador lanza error con "ADVERTENCIA"
        with patch.object(
            arbol_vacio,
            "eliminar_persona",
            side_effect=[
                EliminacionConDescendientesError("Persona 1", 2),
                None,  # Segunda llamada (con confirmación) no lanza error
            ],
        ):
            # ACT
            ui.eliminar_persona()

            # ASSERT
            mock_input.assert_called_once_with("Desea continuar? (s/n): ")
            # Verificar que se mostró la advertencia
            assert any("ADVERTENCIA" in str(call) for call in mock_print.call_args_list)

    @patch("src.ui.DinastiaUI.pedir_dato", return_value=1)
    @patch("builtins.input", return_value="S")  # Mayúscula
    @patch("builtins.print")
    def test_eliminar_persona_confirma_con_mayuscula(
        self,
        mock_print: MagicMock,
        mock_input: MagicMock,
        mock_pedir_dato: MagicMock,
        arbol_con_datos: ArbolGenealogico,
    ):
        """
        Test: Eliminar persona acepta confirmación con mayúscula

        Verifica que eliminar_persona() acepta "S" mayúscula como confirmación.
        """
        # ARRANGE
        ui = DinastiaUI(arbol_con_datos)

        # Simular error con ADVERTENCIA
        with patch.object(
            arbol_con_datos,
            "eliminar_persona",
            side_effect=[
                EliminacionConDescendientesError("Persona 1", 1),
                None,
            ],
        ):
            # ACT
            ui.eliminar_persona()

            # ASSERT
            # El .strip().lower() debería convertir "S" a "s"
            mock_input.assert_called_once_with("Desea continuar? (s/n): ")
            assert any("eliminada exitosamente" in str(call) for call in mock_print.call_args_list)

    @patch("src.ui.DinastiaUI.pedir_dato", return_value=1)
    @patch("builtins.input", return_value="  s  ")  # Con espacios
    @patch("builtins.print")
    def test_eliminar_persona_confirma_con_espacios(
        self,
        mock_print: MagicMock,
        mock_input: MagicMock,
        mock_pedir_dato: MagicMock,
        arbol_con_datos: ArbolGenealogico,
    ):
        """
        Test: Eliminar persona acepta confirmación con espacios

        Verifica que eliminar_persona() maneja espacios en la confirmación.
        """
        # ARRANGE
        ui = DinastiaUI(arbol_con_datos)

        # Simular error con ADVERTENCIA
        with patch.object(
            arbol_con_datos,
            "eliminar_persona",
            side_effect=[
                EliminacionConDescendientesError("Persona 1", 1),
                None,
            ],
        ):
            # ACT
            ui.eliminar_persona()

            # ASSERT
            # El .strip().lower() debería limpiar los espacios
            assert any("eliminada exitosamente" in str(call) for call in mock_print.call_args_list)

    @patch("src.ui.DinastiaUI.pedir_dato", return_value=1)
    @patch("builtins.print")
    def test_eliminar_persona_error_sin_advertencia(
        self,
        mock_print: MagicMock,
        mock_pedir_dato: MagicMock,
        arbol_vacio: ArbolGenealogico,
    ):
        """
        Test: Eliminar persona con error sin ADVERTENCIA

        Verifica que eliminar_persona() maneja errores que no contienen "ADVERTENCIA".
        """
        # ARRANGE
        ui = DinastiaUI(arbol_vacio)
        arbol_vacio.registrar_persona("Persona")

        # Simular error sin ADVERTENCIA
        with patch.object(
            arbol_vacio, "eliminar_persona", side_effect=ArbolGenealogicoError("Error genérico")
        ):
            # ACT
            ui.eliminar_persona()

            # ASSERT
            # No debería pedir confirmación, solo mostrar el error
            assert any("Error:" in str(call) for call in mock_print.call_args_list)
            assert any("Error genérico" in str(call) for call in mock_print.call_args_list)

    @patch("src.ui.DinastiaUI.pedir_dato", return_value=1)
    @patch("src.ui.UIMessages.error")
    def test_eliminar_persona_error_critico_repositorio(
        self,
        mock_error: MagicMock,
        mock_pedir_dato: MagicMock,
        arbol_vacio: ArbolGenealogico,
    ):
        """Cubre líneas 289-292 (except ArbolGenealogicoError en eliminar_persona)"""
        ui = DinastiaUI(arbol_vacio)
        with patch.object(
            arbol_vacio, "get_persona", side_effect=ArbolGenealogicoError("Error crítico")
        ):
            ui.eliminar_persona()
            mock_error.assert_called_with("Error crítico")


# ==================== TESTS PARA mostrar_menu_principal ====================


class TestMenuPrincipal:
    """Tests para el bucle principal del menú"""

    @patch("builtins.input", side_effect=["8"])
    @patch("src.ui.UIMessages.success")
    def test_mostrar_menu_principal_salir(
        self, mock_success: MagicMock, mock_input: MagicMock, arbol_vacio: ArbolGenealogico
    ):
        """Cubre líneas 37-41, 50-54, 69-71"""
        ui = DinastiaUI(arbol_vacio)
        ui.mostrar_menu_principal()
        mock_success.assert_any_call("Bienvenido al sistema de árbol genealógico")

    @patch("builtins.input", side_effect=["invalid", "8"])
    @patch("builtins.print")
    def test_mostrar_menu_principal_opcion_invalida(
        self, mock_print: MagicMock, mock_input: MagicMock, arbol_vacio: ArbolGenealogico
    ):
        """Cubre líneas 72-74"""
        ui = DinastiaUI(arbol_vacio)
        ui.mostrar_menu_principal()
        mock_print.assert_any_call("Opción invalida. Intente de nuevo.")

    @pytest.mark.parametrize(
        "opcion,metodo_mock",
        [
            ("1", "agregar_persona"),
            ("2", "eliminar_persona"),
            ("3", "buscar_persona"),
            ("4", "mostrar_arbol"),
            ("5", "agregar_hijo"),
            ("6", "agregar_pareja"),
            ("7", "eliminar_pareja"),
        ],
    )
    def test_mostrar_menu_principal_opciones(
        self, opcion: str, metodo_mock: str, arbol_vacio: ArbolGenealogico
    ):
        """Cubre todas las opciones del match en mostrar_menu_principal (líneas 56-68)"""
        ui = DinastiaUI(arbol_vacio)
        with patch.object(ui, metodo_mock) as mock_metodo:
            with patch("builtins.input", side_effect=[opcion, "8"]):
                ui.mostrar_menu_principal()
                mock_metodo.assert_called_once()


# ==================== TESTS DE ERRORES ADICIONALES ====================


class TestUIDataErrors:
    """Tests para capturar errores de ArbolGenealogicoError en UI"""

    @patch("src.ui.SearchArbolVisitor")
    @patch("src.ui.DinastiaUI.pedir_dato", return_value="Test")
    @patch("src.ui.UIMessages.error")
    def test_buscar_persona_error_generico(
        self,
        mock_error: MagicMock,
        mock_pedir: MagicMock,
        mock_visitor: MagicMock,
        arbol_vacio: ArbolGenealogico,
    ):
        """Cubre líneas 119-121"""
        ui = DinastiaUI(arbol_vacio)
        # Forzar error al recorrer
        with patch.object(
            arbol_vacio,
            "recorrer_arbol_completo",
            side_effect=ArbolGenealogicoError("Error search"),
        ):
            ui.buscar_persona()
            mock_error.assert_called_with("Error search")

    @patch("src.ui.PrintArbolVisitor")
    @patch("src.ui.UIMessages.error")
    def test_mostrar_arbol_error_generico(
        self, mock_error: MagicMock, mock_visitor: MagicMock, arbol_vacio: ArbolGenealogico
    ):
        """Cubre líneas 135-137"""
        ui = DinastiaUI(arbol_vacio)
        with patch.object(
            arbol_vacio, "recorrer_arbol_completo", side_effect=ArbolGenealogicoError("Error print")
        ):
            ui.mostrar_arbol()
            mock_error.assert_called_with("Error print")
