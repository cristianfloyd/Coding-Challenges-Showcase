import json


def get_coverage_percentage():
    """Lee el porcentaje de cobertura del reporte JSON ya generado."""
    try:
        # Leemos el coverage.json que ya debería existir (generado por pytest)
        with open("coverage.json", "r") as f:
            data = json.load(f)
            # El formato de coverage.json tiene "totals": {"percent_covered": ...}
            return data["totals"]["percent_covered"]
    except FileNotFoundError:
        print("Error: coverage.json no encontrado. Asegúrate de ejecutar pytest --cov primero.")
        return 0
    except Exception as e:
        print(f"Error leyendo cobertura: {e}")
        return 0


def generate_badge(percentage: float):
    """Genera un archivo SVG con el porcentaje."""
    # Colores según el porcentaje
    if percentage >= 95:
        color = "#4c1"  # Verde brillante (Success)
    elif percentage >= 90:
        color = "#97c40f"  # Verde claro
    elif percentage >= 75:
        color = "#a4a61d"  # Amarillo oscuro
    elif percentage >= 60:
        color = "#dfb317"  # Amarillo
    else:
        color = "#e05d44"  # Rojo (Failure)

    # Redondeamos a 2 decimales o entero
    per_str = f"{round(percentage)}%"

    # Plantilla SVG minimalista (estilo shields.io)
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="90" height="20">
    <linearGradient id="b" x2="0" y2="100%">
        <stop offset="0" stop-color="#bbb" stop-opacity=".1"/>
        <stop offset="1" stop-opacity=".1"/>
    </linearGradient>
    <mask id="a">
        <rect width="90" height="20" rx="3" fill="#fff"/>
    </mask>
    <g mask="url(#a)">
        <path fill="#555" d="M0 0h55v20H0z"/>
        <path fill="{color}" d="M55 0h35v20H55z"/>
        <path fill="url(#b)" d="M0 0h90v20H0z"/>
    </g>
    <g fill="#fff" text-anchor="middle" font-family="DejaVu Sans,Verdana,Geneva,sans-serif"
       font-size="11">
        <text x="27.5" y="15" fill="#010101" fill-opacity=".3">coverage</text>
        <text x="27.5" y="14">coverage</text>
        <text x="71.5" y="15" fill="#010101" fill-opacity=".3">{per_str}</text>
        <text x="71.5" y="14">{per_str}</text>
    </g>
</svg>"""

    with open("coverage_badge.svg", "w") as f:
        f.write(svg)

    print(f"Badge generado: coverage_badge.svg con {per_str}")


if __name__ == "__main__":
    print("Calculando cobertura y generando badge...")
    cov = get_coverage_percentage()
    generate_badge(cov)
