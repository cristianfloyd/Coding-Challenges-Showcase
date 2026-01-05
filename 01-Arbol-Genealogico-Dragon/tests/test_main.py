"""
Tests para el módulo main.py

Verifica la orquestación principal de la aplicación:
- Inicialización del árbol
- Carga de datos
- Inicialización de la UI
- Ejecución del menú principal
"""

from unittest.mock import MagicMock, patch

from src.main import main


@patch("src.main.DinastiaUI")
@patch("src.main.DemoDataLoader")
@patch("src.main.ArbolGenealogico")
def test_main_flujo_completo(
    mock_arbol_cls: MagicMock, mock_data_loader: MagicMock, mock_ui_cls: MagicMock
):
    """
    Test: Flujo principal de la aplicación

    Verifica que main() orquesta correctamente los componentes:
    1. Crea el árbol
    2. Carga los datos
    3. Inicializa la UI
    4. Muestra el menú
    """
    # ARRANGE
    # Configurar los mocks
    mock_arbol_instance = mock_arbol_cls.return_value
    mock_ui_instance = mock_ui_cls.return_value

    # ACT
    main()

    # ASSERT
    # 1. Verificar que se instanció el árbol
    mock_arbol_cls.assert_called_once()

    # 2. Verificar que se cargaron los datos usando la instancia del árbol
    mock_data_loader.cargar_datos.assert_called_once_with(mock_arbol_instance)

    # 3. Verificar que se instanció la UI con el árbol cargado
    mock_ui_cls.assert_called_once_with(mock_arbol_instance)

    # 4. Verificar que se inició el menú principal
    mock_ui_instance.mostrar_menu_principal.assert_called_once()
