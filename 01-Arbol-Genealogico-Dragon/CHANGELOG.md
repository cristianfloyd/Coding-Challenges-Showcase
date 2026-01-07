# Changelog

Todos los cambios notables de este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-01-05

### Añadido
- Sistema completo de gestión de árboles genealógicos
- Gestión de relaciones familiares (padres, hijos, parejas)
- Validaciones robustas:
  - Prevención de incesto (padre-hijo como pareja)
  - Detección de ciclos temporales (algoritmo recursivo)
  - Límite de 2 padres por persona
  - Validación de IDs únicos
  - Verificación de relaciones bidireccionales
- Implementación de Design Patterns:
  - Visitor Pattern para recorridos flexibles
  - Repository Pattern para abstracción de datos
  - Factory Pattern en tests
- Sistema de logging estructurado:
  - Logging centralizado con `LoggerConfig`
  - Separación de logging técnico y output de usuario
  - Logging a archivo (`logs/arbol_genealogico.log`)
  - Niveles de log (DEBUG, INFO, WARNING, ERROR)
- Testing exhaustivo:
  - 103 tests (unitarios + integración)
  - 94% de cobertura de código
  - 6 módulos con 100% de cobertura
  - Fixtures reutilizables y mocks avanzados
- Arquitectura Clean Code:
  - Separación de responsabilidades (SOLID)
  - Dependency Injection Container
  - Protocols para Dependency Inversion
  - Type hints completos
- Interfaz CLI interactiva con menú completo
- Datos demo: Árbol genealógico completo de la Casa Targaryen
- CI/CD Pipeline:
  - GitHub Actions para tests y linting
  - Pre-commit hooks (Ruff, Pyright)
  - Coverage badges automáticos
- Documentación técnica completa en README
- Makefile para automatización de tareas

### Cambiado
- Refactorización de código monolítico (300 líneas) a arquitectura modular (7 módulos)
- Separación clara entre UI, lógica de negocio y persistencia

### Seguridad
- Pre-commit hooks para validación de código antes de commits
- Type checking estricto con Pyright

---

## [Unreleased]

### Planificado
- Excepciones personalizadas para mejor manejo de errores
- Security scanning automatizado (Bandit, Safety)
- Matrix testing (múltiples versiones de Python)
- Performance testing y benchmarks
- Dockerización de la aplicación

---

## Formato de Versionado

Este proyecto usa [Semantic Versioning](https://semver.org/):
- **MAJOR** (1.0.0): Cambios incompatibles en la API
- **MINOR** (0.1.0): Funcionalidades nuevas compatibles hacia atrás
- **PATCH** (0.0.1): Correcciones de bugs compatibles hacia atrás

## Categorías de Cambios

- **Añadido**: Nuevas funcionalidades
- **Cambiado**: Cambios en funcionalidades existentes
- **Deprecado**: Funcionalidades que pronto serán eliminadas
- **Eliminado**: Funcionalidades eliminadas
- **Corregido**: Correcciones de bugs
- **Seguridad**: Vulnerabilidades de seguridad corregidas