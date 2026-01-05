from .data_loader import DemoDataLoader
from .repository import ArbolGenealogico
from .ui import DinastiaUI


def main():
    arbol = ArbolGenealogico()
    DemoDataLoader.cargar_datos(arbol)
    # Aquí puedes registrar los datos iniciales de los Targaryen
    ui = DinastiaUI(arbol)
    ui.mostrar_menu_principal()


if __name__ == "__main__":
    main()
