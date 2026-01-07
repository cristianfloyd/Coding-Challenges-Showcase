from typing import Protocol


class UserOutputInterface(Protocol):
    def show_message(self, message: str) -> None:
        ...

    def show_error(self, message: str) -> None:
        ...

    def show_success(self, message: str) -> None:
        ...


class ConsoleOutput:
    """Implementación de salida a consola"""

    def show_message(self, message: str) -> None:
        """Muestra un mensaje al usuario"""
        print(message)

    def show_error(self, message: str) -> None:
        """Muestra un mensaje de error al usuario"""
        print(f"Error: {message}")

    def show_success(self, message: str) -> None:
        """Muestra un mensaje de éxito al usuario"""
        print(f"✅ {message}")
