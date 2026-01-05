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


@patch("src.main.ApplicationContainer")
@patch("src.main.setup_application_logging")
def test_main_flujo_completo(mock_setup_logging: MagicMock, mock_container_cls: MagicMock):
    """
    Test: Flujo principal de la aplicación

    Verifica que main() orquesta correctamente los componentes:
    1. Configura el logging
    2. Crea el contenedor
    3. Obtiene el árbol, data_loader y UI del contenedor
    4. Carga los datos
    5. Muestra el menú principal
    """
    # ARRANGE
    # Configurar los mocks del contenedor
    mock_container_instance = mock_container_cls.return_value
    mock_arbol = MagicMock()
    mock_arbol.personas = {}  # Simular diccionario vacío para len()
    mock_data_loader = MagicMock()
    mock_ui = MagicMock()

    # Configurar los métodos del contenedor
    mock_container_instance.get_arbol.return_value = mock_arbol
    mock_container_instance.get_data_loader.return_value = mock_data_loader
    mock_container_instance.get_ui.return_value = mock_ui

    # ACT
    main()

    # ASSERT
    # 1. Verificar que se configuró el logging
    mock_setup_logging.assert_called_once()

    # 2. Verificar que se creó el contenedor
    mock_container_cls.assert_called_once()

    # 3. Verificar que se obtuvieron las dependencias del contenedor
    mock_container_instance.get_arbol.assert_called_once()
    mock_container_instance.get_data_loader.assert_called_once()
    mock_container_instance.get_ui.assert_called_once()

    # 4. Verificar que se cargaron los datos usando la instancia del árbol
    mock_data_loader.cargar_datos.assert_called_once_with(mock_arbol)

    # 5. Verificar que se inició el menú principal
    mock_ui.mostrar_menu_principal.assert_called_once()
