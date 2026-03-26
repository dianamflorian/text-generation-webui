# 💡 EJEMPLOS DE PROMPT: SOMETHING BIG
**Catálogo de ejemplos de referencia para estructura y agnosticismo.**

---

## 1. PyMC: Soporte para Marimo Notebook
- **Objetivo:** Refactorizar el sistema de barras de progreso para soportar rendering HTML en Marimo, manteniendo compatibilidad con terminal/Jupyter.
- **Patrón:** Factory pattern (`create_simple_progress`) y modularización en subpaquetes.
- **Interfaces clave:** `ProgressBackend` (Protocol), `ProgressBarManager`, `create_simple_progress`.
- **Lección:** Cómo definir una arquitectura modular (backends separados) sin prescribir la lógica interna de cálculo.

## 2. Voila: Widget Manager Decoupling
- **Objetivo:** Desacoplar el gestor de widgets para soportar ipywidgets 7 y 8 simultáneamente mediante extensiones federadas.
- **Interfaces clave:** `get_voila_labextensions_path`, `maybe_inject_widgets_manager_extension`.
- **Lección:** Especificación técnica detallada de dependencias y rutas de archivos (`{PREFIX}/share/...`) manteniendo el prompt agnóstico a la lógica de inyección exacta.

## 3. Polygon Triangulation (earcut.hpp)
- **Objetivo:** Librería C++ header-only para triangulación de polígonos con huecos.
- **Interfaces clave:** `mapbox::earcut` (Public API), `mapbox::detail::Earcut` (Internal).
- **Lección:** Cómo documentar estructuras de datos internas (`Node`) y algoritmos complejos (ear-cutting, z-order curve) sin dictar cada línea de código, enfocándose en la firmas de funciones y el comportamiento observable.

---

### 📝 Notas sobre "Expected Interface" (Formato Mandatorio)
Todos los ejemplos siguen estrictamente este bloque por cada componente:
- **Path:** Ruta exacta del archivo.
- **Name:** Nombre de la clase o función.
- **Type:** Tipo de objeto.
- **Input/Output:** Parámetros y retornos con tipos.
- **Description:** Descripción del QUÉ hace.

*Documento preparado como material de apoyo para la misión: oobabooga/text-generation-webui*
