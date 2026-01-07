# 🐉 Árbol Genealógico - Casa del Dragón

[![CI/CD](https://github.com/cristianfloyd/Coding-Challenges-Showcase/actions/workflows/ci-01-dragon.yml/badge.svg)](https://github.com/cristianfloyd/Coding-Challenges-Showcase/actions/workflows/ci-01-dragon.yml)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Tests](https://img.shields.io/badge/Tests-155%20passed-success.svg)](https://github.com)
[![Coverage](https://img.shields.io/badge/Coverage-94%25-brightgreen.svg)](https://github.com)
[![Code Style](https://img.shields.io/badge/Code%20Style-Ruff-black.svg)](https://github.com/astral-sh/ruff)
[![Type Check](https://img.shields.io/badge/Type%20Check-Pyright%20Strict-blue.svg)](https://github.com/microsoft/pyright)
[![Security](https://img.shields.io/badge/Security-Bandit%20%2B%20Safety-blue.svg)](https://github.com/PyCQA/bandit)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Architecture](https://img.shields.io/badge/Architecture-SOLID-orange.svg)](https://github.com)

> Sistema de gestión de árboles genealógicos con validaciones complejas, implementado siguiendo principios **SOLID**, **Clean Code** y **Design Patterns**. Proyecto que demuestra competencia en arquitectura de software, testing exhaustivo y buenas prácticas de desarrollo.

## 🎯 Highlights

### Logros Técnicos

| Métrica | Valor | Significado |
|---------|-------|-------------|
| **Cobertura de Tests** | **94%** | Testing exhaustivo y profesional |
| **Total de Tests** | **155** | Unitarios + Integración |
| **Módulos con 100%** | **6 de 7** | Calidad de código excepcional |
| **Líneas de Código** | **~540** | Proyecto de tamaño medio-complejo |
| **Design Patterns** | **3+** | Visitor, Repository, Factory, DI Container |
| **Security Scanning** | **Bandit + Safety** | Análisis automático de vulnerabilidades |

### Habilidades Demostradas

✅ **Arquitectura de Software**: Separación de responsabilidades, capas bien definidas
✅ **Principios SOLID**: Aplicación práctica en todos los módulos
✅ **Design Patterns**: Visitor, Repository, Factory, Dependency Injection implementados
✅ **Testing Profesional**: 155 tests con fixtures reutilizables y mocks
✅ **Clean Code**: Refactorización, nombres descriptivos, funciones pequeñas
✅ **Type Hints**: Código completamente tipado con Pyright strict
✅ **CI/CD**: Pipeline automatizado con security scanning
✅ **Security**: Análisis automático con Bandit y Safety
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
| **Code Quality** | Ruff (linter/formatter), Coverage analysis |
| **Type Checking** | Pyright (strict mode) |
| **Security** | Bandit, Safety |
| **Arquitectura** | Modular, SOLID, Design Patterns, Dependency Injection |
| **CI/CD** | GitHub Actions (tests, lint, type-check, security) |

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
4. **Dependency Injection**: Container para gestión de dependencias (Service Locator pattern)
5. **Protocol-based Design**: Structural subtyping para Dependency Inversion

#### 📝 Clean Code Practices

- Nombres descriptivos y expresivos
- Funciones pequeñas y enfocadas (< 30 líneas)
- Separación de concerns (UI, lógica, datos)
- Documentación completa (docstrings)
- Type hints en 100% del código

## 🏗️ Arquitectura y Diseño

### Arquitectura en Capas

```
┌─────────────────────────────────────────┐
│         main.py                         │  ← Orquestación
│  (Dependency Injection Container)       │
└──────────────┬──────────────────────────┘
               │
    ┌──────────┴──────────┐
    │                     │
┌───▼────┐         ┌──────▼─────────┐
│  UI    │         │  Data Loader   │  ← Presentación y Carga
│ Layer  │         │  (Protocol)    │
└───┬────┘         └────────────────┘
    │
┌───▼──────────┐
│  Repository  │  ← Persistencia (Repository Pattern)
│  (Protocol)  │
└───┬──────────┘
    │
┌───▼──────────┐
│  Validators  │  ← Lógica de Negocio
└──────────────┘
    │
┌───▼──────────┐
│   Models     │  ← Entidades del Dominio
└──────────────┘

┌─────────────────────────────────────────┐
│      Dependency Injection Layer         │
│  - Container (Service Locator)          │
│  - Interfaces (Protocols)               │
│  - Configuration (AppConfig)            │
└─────────────────────────────────────────┘
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
4. **Dependency Injection**: Container gestiona dependencias siguiendo Service Locator pattern
5. **Protocol-based Design**: Structural subtyping para Dependency Inversion (sin acoplamiento)
6. **Separación Logging/Output**: Logging técnico vs mensajes de usuario claramente separados
7. **Refactorización**: Código monolítico → arquitectura modular (300 → 12+ módulos)

## 🧪 Calidad del Código

### Testing Exhaustivo

```bash
# Ejecutar todos los tests
pytest --cov=src --cov-report=term-missing

# O usar el Makefile
make test
```

### Security Scanning

El proyecto incluye análisis automático de seguridad:

```bash
# Ejecutar análisis de seguridad
make security-scan

# O individualmente
make bandit    # Análisis de código Python
make safety    # Verificación de vulnerabilidades en dependencias
```

**Herramientas de seguridad:**
- **Bandit**: Detecta vulnerabilidades comunes en código Python
- **Safety**: Verifica vulnerabilidades conocidas en dependencias (no aplica actualmente: `dependencies = []`)

## 🔌 Dependency Injection y Arquitectura

### Dependency Injection Container

El proyecto implementa un **Container** siguiendo el patrón Service Locator para gestionar dependencias:

- **Singleton**: Dependencias con estado (ArbolGenealogico, DinastiaUI)
- **Transient**: Servicios stateless (DataLoader)
- **Protocol-based**: Dependency Inversion mediante structural subtyping

### Separación de Concerns

El código mantiene una clara separación entre:
- **Logging técnico**: Para debugging y auditoría (`logging` module)
- **Output de usuario**: Mensajes interactivos de la CLI (`print()`)
- **Configuración**: Externalizada mediante `AppConfig.from_env()`

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
- ✅ **155 tests** pasando
- ✅ **94% cobertura** total
- ✅ **6 módulos** con 100% de cobertura
- ✅ **13+ fixtures** reutilizables
- ✅ **Tests unitarios** + **Tests de integración**
- ✅ **Security scanning** integrado (Bandit: 0 issues)

### Tipos de Tests Implementados

| Tipo | Cantidad | Ejemplos |
|------|----------|----------|
| **Unit Tests** | 120+ | Validaciones, modelos, repositorio, interfaces, container |
| **Integration Tests** | 10+ | Carga de datos, flujos completos |
| **UI Tests** | 25+ | Mocks de input/output, casos edge, UI logger |

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
git clone https://github.com/cristianfloyd/Coding-Challenges-Showcase.git
cd Coding-Challenges-Showcase/01-Arbol-Genealogico-Dragon

# Crear entorno virtual (opcional, recomendado usar Rye)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar dependencias
make install
# O manualmente:
pip install -e ".[dev]"
```

### Comandos Disponibles (Makefile)

```bash
make install        # Instalar dependencias de desarrollo
make test           # Ejecutar todos los tests
make lint           # Verificar estilo de código con Ruff
make format         # Formatear código con Ruff
make type-check     # Verificar tipos con Pyright
make security-scan  # Ejecutar análisis de seguridad (Bandit + Safety)
make check          # Ejecutar todas las verificaciones (lint + type-check + security + test)
```

### Ejecutar la Aplicación

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
│   ├── main.py              # Orquestación
│   ├── container.py         # Dependency Injection Container
│   ├── interfaces.py        # Protocols para Dependency Inversion
│   ├── config.py            # Configuración de la aplicación
│   ├── exceptions.py        # Jerarquía de excepciones personalizadas
│   └── utils/
│       ├── logger.py        # Sistema de logging estructurado
│       ├── ui_logger.py     # Logger para operaciones de UI
│       └── output.py        # Separación de output de usuario
├── tests/
│   ├── conftest.py          # Fixtures compartidos (13+ fixtures)
│   ├── test_models.py       # Tests del modelo
│   ├── test_validators.py   # Tests de validación
│   ├── test_repository.py   # Tests del repositorio
│   ├── test_visitors.py     # Tests del Visitor
│   ├── test_ui.py           # Tests de UI
│   ├── test_data_loader.py  # Tests de integración
│   ├── test_main.py         # Tests de orquestación
│   ├── test_container.py    # Tests del DI Container
│   ├── test_interfaces.py   # Tests de interfaces/protocols
│   └── test_ui_logger.py    # Tests del UI logger
├── scripts/
│   └── generate_badge.py    # Generación automática de badges
├── .github/workflows/
│   └── ci-01-dragon.yml     # CI/CD pipeline completo
├── Makefile                 # Comandos automatizados
├── pyproject.toml           # Configuración del proyecto
└── README.md                # Documentación completa
```

## 📊 Métricas del Proyecto

- **Líneas de código**: ~540 (sin tests)
- **Tests**: 155 (unitarios + integración)
- **Cobertura**: 94%
- **Módulos**: 12+ (src/ + utils/)
- **Clases**: 10+
- **Funciones/Métodos**: 60+
- **Design Patterns**: 4+ (Visitor, Repository, Factory, DI Container)
- **Principios SOLID**: Todos aplicados completamente
- **Security Issues**: 0 (Bandit scan)

## 🎓 Aprendizajes y Desafíos

### Desafíos Técnicos Superados

1. **Refactorización de código monolítico**: Transformación de 300 líneas en arquitectura modular
2. **Testing de UI interactiva**: Implementación de mocks complejos para `input()` y métodos estáticos
3. **Algoritmos de validación**: Detección de ciclos temporales en grafos dirigidos
4. **Cobertura del 100%**: Logro de cobertura completa en 6 de 7 módulos

### Mejores Prácticas Aplicadas

- ✅ Type hints en todo el código (Pyright strict mode)
- ✅ Docstrings completos
- ✅ Separación de concerns
- ✅ Inyección de dependencias (Container pattern)
- ✅ Testing exhaustivo con fixtures (155 tests)
- ✅ CI/CD configurado (tests, lint, type-check, security)
- ✅ Security scanning automático (Bandit + Safety)
- ✅ Logging estructurado y separado del output de usuario
- ✅ Excepciones personalizadas con jerarquía clara
- ✅ Pre-commit hooks configurados

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
