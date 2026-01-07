# 🐉 Árbol Genealógico - Casa del Dragón

[![CI/CD](https://github.com/cristianfloyd/Coding-Challenges-Showcase/actions/workflows/ci-01-dragon.yml/badge.svg)](https://github.com/cristianfloyd/Coding-Challenges-Showcase/actions/workflows/ci-01-dragon.yml)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Tests](https://img.shields.io/badge/Tests-103%20passed-success.svg)](https://github.com)
[![Coverage](https://img.shields.io/badge/Coverage-94%25-brightgreen.svg)](https://github.com)
[![Code Style](https://img.shields.io/badge/Code%20Style-Ruff-black.svg)](https://github.com/astral-sh/ruff)
[![Type Check](https://img.shields.io/badge/Type%20Check-Pyright%20Strict-blue.svg)](https://github.com/microsoft/pyright)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Architecture](https://img.shields.io/badge/Architecture-SOLID-orange.svg)](https://github.com)

> Sistema de gestión de árboles genealógicos con validaciones complejas, implementado siguiendo principios **SOLID**, **Clean Code** y **Design Patterns**. Proyecto que demuestra competencia en arquitectura de software, testing exhaustivo y buenas prácticas de desarrollo.

## 🎯 Highlights

### Logros Técnicos

| Métrica | Valor | Significado |
|---------|-------|-------------|
| **Cobertura de Tests** | **94%** | Testing exhaustivo y profesional |
| **Total de Tests** | **103** | Unitarios + Integración |
| **Módulos con 100%** | **6 de 7** | Calidad de código excepcional |
| **Líneas de Código** | **~540** | Proyecto de tamaño medio-complejo |
| **Design Patterns** | **3** | Visitor, Repository, Factory |

### Habilidades Demostradas

✅ **Arquitectura de Software**: Separación de responsabilidades, capas bien definidas
✅ **Principios SOLID**: Aplicación práctica en todos los módulos
✅ **Design Patterns**: Visitor, Repository, Factory implementados correctamente
✅ **Testing Profesional**: 103 tests con fixtures reutilizables y mocks
✅ **Clean Code**: Refactorización, nombres descriptivos, funciones pequeñas
✅ **Type Hints**: Código completamente tipado
✅ **CI/CD**: Pipeline automatizado configurado
✅ **Estructuras de Datos**: Árboles, grafos, algoritmos de recorrido

## 📋 Tabla de Contenidos

- [Resumen del Proyecto](#-resumen-del-proyecto)
- [Habilidades Técnicas](#-habilidades-técnicas)
- [Arquitectura y Diseño](#-arquitectura-y-diseño)
- [Calidad del Código](#-calidad-del-código)
- [Instalación y Uso](#-instalación-y-uso)
- [Estructura del Proyecto](#-estructura-del-proyecto)

## 📖 Resumen del Proyecto

Sistema completo de gestión de árboles genealógicos que permite:

- **Gestión de relaciones familiares**: Padres, hijos, parejas con validaciones complejas
- **Validaciones robustas**: Previene incesto, ciclos temporales, relaciones inválidas
- **Patrón Visitor**: Recorridos flexibles (búsqueda, impresión, conteo)
- **Interfaz CLI**: Menú interactivo completo
- **Datos demo**: Árbol genealógico completo de la Casa Targaryen

### Desafíos Técnicos Resueltos

1. **Detección de ciclos temporales**: Algoritmo recursivo para validar ancestros
2. **Validación de reglas de negocio complejas**: Múltiples restricciones simultáneas
3. **Refactorización de código legacy**: Transformación de 300 líneas monolíticas a arquitectura modular
4. **Testing de UI interactiva**: Mocks avanzados para `input()` y métodos estáticos

## 🛠️ Habilidades Técnicas

### Stack Tecnológico

| Categoría | Tecnologías |
|-----------|-------------|
| **Lenguaje** | Python 3.10+ (Type Hints completos) |
| **Testing** | pytest, pytest-cov, unittest.mock |
| **Code Quality** | Ruff (linter), Coverage analysis |
| **Arquitectura** | Modular, SOLID, Design Patterns |
| **CI/CD** | GitHub Actions |

### Principios y Patrones Aplicados

#### ✅ SOLID Principles (Aplicación Práctica)

- **Single Responsibility**: Cada módulo tiene una única responsabilidad clara
- **Open/Closed**: Extensible mediante Visitor Pattern sin modificar código existente
- **Liskov Substitution**: Interfaces bien definidas y respetadas
- **Interface Segregation**: Interfaces específicas y pequeñas
- **Dependency Inversion**: Inyección de dependencias, no acoplamiento directo

#### 🎯 Design Patterns Implementados

1. **Visitor Pattern**: Recorridos flexibles del árbol sin modificar la estructura
2. **Repository Pattern**: Abstracción de acceso a datos
3. **Factory Pattern**: Creación de objetos en tests (fixtures)

#### 📝 Clean Code Practices

- Nombres descriptivos y expresivos
- Funciones pequeñas y enfocadas (< 30 líneas)
- Separación de concerns (UI, lógica, datos)
- Documentación completa (docstrings)
- Type hints en 100% del código

## 🏗️ Arquitectura y Diseño

### Arquitectura en Capas

```
┌─────────────────┐
│   main.py       │  ← Orquestación (Dependency Injection)
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
┌───▼───┐ ┌──▼──────┐
│  UI   │ │ Data    │  ← Presentación y Datos
│ Layer │ │ Loader  │
└───┬───┘ └─────────┘
    │
┌───▼──────────┐
│  Repository   │  ← Persistencia (Repository Pattern)
└───┬───────────┘
    │
┌───▼──────────┐
│  Validators  │  ← Lógica de Negocio
└──────────────┘
    │
┌───▼──────────┐
│   Models     │  ← Entidades del Dominio
└──────────────┘
```

### Componentes y Cobertura

| Módulo | Responsabilidad | Cobertura | Estado |
|--------|----------------|-----------|--------|
| `models.py` | Entidades del dominio | **100%** ✅ | Perfecto |
| `repository.py` | Gestión de datos | **100%** ✅ | Perfecto |
| `validators.py` | Reglas de negocio | **100%** ✅ | Perfecto |
| `visitors.py` | Patrón Visitor | **100%** ✅ | Perfecto |
| `data_loader.py` | Carga de datos | **100%** ✅ | Perfecto |
| `main.py` | Orquestación | **100%** ✅ | Perfecto |
| `ui.py` | Interfaz de usuario | **76%** ⚠️ | Bueno |

### Decisiones de Diseño Clave

1. **Separación UI/Lógica**: La UI solo orquesta, la lógica está en validators
2. **Visitor Pattern**: Permite agregar nuevos algoritmos sin modificar Persona
3. **Repository Pattern**: Abstrae el acceso a datos, facilita testing
4. **Refactorización**: Código monolítico → arquitectura modular (300 → 7 módulos)

## 🧪 Calidad del Código

### Testing Exhaustivo

```bash
# Ejecutar todos los tests
pytest --cov=src --cov-report=term-missing
```

## 📋 Sistema de Logging

Este proyecto implementa un sistema de logging estructurado siguiendo mejores prácticas de la industria.

### Configuración

El sistema de logging está centralizado en `src/utils/logger.py` y se inicializa automáticamente al iniciar la aplicación.

**Ubicación del archivo de logs:**

- logs/arbol_genealogico.log


### Niveles de Log

| Nivel | Uso | Ejemplo |
|-------|-----|---------|
| **DEBUG** | Información detallada para debugging | "Buscando persona con ID: 42" |
| **INFO** | Eventos importantes de la aplicación | "Persona registrada exitosamente: Daenerys (ID: 5)" |
| **WARNING** | Situaciones que requieren atención pero no son errores | "Límite de padres excedido para persona X" |
| **ERROR** | Errores que requieren atención inmediata | "Error al registrar persona: ID ya existe" |

### Separación de Concerns

El proyecto mantiene una separación clara entre:

- **Logging técnico** (`logging`): Para debugging, auditoría y monitoreo
  - Se guarda en archivo y consola (solo errores)
  - Usa el módulo estándar `logging` de Python
  - Formato estructurado con timestamp, módulo, nivel y mensaje

- **Output de usuario** (`print()`): Para la interfaz interactiva CLI
  - Mensajes amigables para el usuario
  - No debe reemplazarse con logging

### Ejemplos de Uso

#### En código nuevo:


```python
from src.utils.logger import get_logger

logger = get_logger(__name__)
def mi_funcion():
    logger.debug("Iniciando operación compleja")
    try:
        # ... código ...
        logger.info("Operación completada exitosamente")
    except Exception as e:
        logger.error(f"Error en operación: {e}")
        raise
```

#### Configuración personalizada:

```python
from src.utils.logger import LoggerConfig
from pathlib import Path

logger = LoggerConfig.setup_logger(
    name="mi_modulo",
    level=logging.DEBUG,  # Nivel personalizado
    log_file=Path("logs/mi_log.log")  # Archivo personalizado
)

```

**Resultados:**
- ✅ **103 tests** pasando
- ✅ **94% cobertura** total
- ✅ **6 módulos** con 100% de cobertura
- ✅ **13 fixtures** reutilizables
- ✅ **Tests unitarios** + **Tests de integración**

### Tipos de Tests Implementados

| Tipo | Cantidad | Ejemplos |
|------|----------|----------|
| **Unit Tests** | 90+ | Validaciones, modelos, repositorio |
| **Integration Tests** | 10+ | Carga de datos, flujos completos |
| **UI Tests** | 30+ | Mocks de input/output, casos edge |

### Ejemplo de Test Profesional

```python
@patch("src.ui.UIMessages.success")
@patch("src.ui.UIMessages.error")
def test_agregar_persona_exito(mock_error, mock_success, arbol_vacio):
    """Test: Agregar persona exitosamente"""
    ui = DinastiaUI(arbol_vacio)
    ui.agregar_persona()

    assert len(arbol_vacio.personas) == 1
    mock_success.assert_called()
    mock_error.assert_not_called()
```

### Validaciones Implementadas

- ✅ Prevención de incesto (padre-hijo como pareja)
- ✅ Detección de ciclos temporales (algoritmo recursivo)
- ✅ Límite de 2 padres por persona
- ✅ Validación de IDs únicos
- ✅ Verificación de relaciones bidireccionales
- ✅ Manejo de errores robusto

## 📦 Instalación y Uso

### Instalación Rápida

```bash
# Clonar repositorio
git clone https://github.com/cristianfloyd/arbol-genealogico-dragon.git
cd arbol-genealogico-dragon

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar dependencias
pip install -e ".[dev]"
```

### Ejecutar

```bash
python -m src.main
```

### Menú Interactivo

```
Menu Principal
1. Agregar persona
2. Eliminar persona
3. Buscar persona
4. Mostrar arbol
5. Agregar hijo
6. Agregar pareja
7. Eliminar pareja
8. Salir
```

## 📁 Estructura del Proyecto

```
01-Arbol-Genealogico-Dragon/
├── src/
│   ├── models.py            # Entidades del dominio
│   ├── repository.py        # Repositorio (Repository Pattern)
│   ├── validators.py        # Lógica de validación
│   ├── visitors.py          # Visitor Pattern
│   ├── ui.py                # Interfaz de usuario
│   ├── data_loader.py       # Carga de datos
│   └── main.py              # Orquestación
├── tests/
│   ├── conftest.py          # Fixtures compartidos (13 fixtures)
│   ├── test_models.py       # Tests del modelo
│   ├── test_validators.py   # Tests de validación (24 tests)
│   ├── test_repository.py   # Tests del repositorio (30 tests)
│   ├── test_visitors.py     # Tests del Visitor (10 tests)
│   ├── test_ui.py           # Tests de UI (30 tests)
│   ├── test_data_loader.py  # Tests de integración (5 tests)
│   └── test_main.py         # Tests de orquestación
├── .github/workflows/
│   └── ci.yml               # CI/CD pipeline
└── pyproject.toml           # Configuración del proyecto
```

## 📊 Métricas del Proyecto

- **Líneas de código**: ~540 (sin tests)
- **Tests**: 103 (unitarios + integración)
- **Cobertura**: 94%
- **Módulos**: 7
- **Clases**: 8
- **Funciones/Métodos**: 50+
- **Design Patterns**: 3 (Visitor, Repository, Factory)
- **Principios SOLID**: Todos aplicados

## 🎓 Aprendizajes y Desafíos

### Desafíos Técnicos Superados

1. **Refactorización de código monolítico**: Transformación de 300 líneas en arquitectura modular
2. **Testing de UI interactiva**: Implementación de mocks complejos para `input()` y métodos estáticos
3. **Algoritmos de validación**: Detección de ciclos temporales en grafos dirigidos
4. **Cobertura del 100%**: Logro de cobertura completa en 6 de 7 módulos

### Mejores Prácticas Aplicadas

- ✅ Type hints en todo el código
- ✅ Docstrings completos
- ✅ Separación de concerns
- ✅ Inyección de dependencias
- ✅ Testing exhaustivo con fixtures
- ✅ CI/CD configurado

## 👤 Autor

**Cristian Arenas**

- 🔗 GitHub: [@cristianfloyd](https://github.com/cristianfloyd)
- 💼 LinkedIn: [Tu perfil](https://linkedin.com/in/tu-perfil)
- 📧 Email: ccristianfloyd@gmail.com

---

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo `LICENSE` para más detalles.

---

⭐ **¿Interesado en este proyecto?** Considera darle una estrella en GitHub o contactarme para más detalles sobre la implementación.
