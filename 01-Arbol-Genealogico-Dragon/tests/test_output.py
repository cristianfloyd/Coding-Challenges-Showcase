"""
Tests para el módulo utils/output.py

Este módulo verifica la implementación de ConsoleOutput y su adherencia
al Protocolo UserOutputInterface.
"""

import pytest

from src.utils.output import ConsoleOutput, UserOutputInterface


class TestConsoleOutput:
    """
    Tests de alta fidelidad para la implementación de salida por consola.
    Utiliza el fixture 'capsys' de pytest para validar el stream real de stdout.
    """

    def test_implementa_protocolo_output(self):
        """
        Test estructural: Verificar que ConsoleOutput cumple con el Protocolo.
        Esto garantiza la compatibilidad para Inyección de Dependencias.
        """
        output = ConsoleOutput()
        assert isinstance(output, UserOutputInterface)

    def test_show_message_imprime_texto_plano(self, capsys: "pytest.CaptureFixture[str]"):
        """
        Verificar que show_message envía el texto correcto a la consola.
        """
        output = ConsoleOutput()
        test_msg = "Mensaje de prueba"
        output.show_message(test_msg)

        captured = capsys.readouterr()
        assert captured.out == f"{test_msg}\n"

    def test_show_error_agrega_prefijo_error(self, capsys: "pytest.CaptureFixture[str]"):
        """
        Verificar que show_error formatea el mensaje con el prefijo 'Error:'.
        """
        output = ConsoleOutput()
        test_error = "Algo salió mal"
        output.show_error(test_error)

        captured = capsys.readouterr()
        assert captured.out == f"Error: {test_error}\n"

    def test_show_success_incluye_emoji_y_formato(self, capsys: "pytest.CaptureFixture[str]"):
        """
        Verificar que show_success incluye el emoji de verificación.
        """
        output = ConsoleOutput()
        test_success = "Operación exitosa"
        output.show_success(test_success)

        captured = capsys.readouterr()
        assert f"✅ {test_success}" in captured.out
        assert captured.out.endswith("\n")
