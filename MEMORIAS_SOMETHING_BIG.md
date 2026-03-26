# 📚 MEMORIAS: SOMETHING BIG (Tool Implementation)
**Resumen extractado de las guías oficiales para cumplimiento del linter y auditoría.**

---

## ⚡ REGLA DE ORO: Implementación Agnóstica
- El prompt debe decir **QUÉ** debe hacer la solución, **NUNCA CÓMO**.
- **EVITAR:** Mencionar pasos lógicos internos, nombres de variables privadas, métodos de ayuda (`helper functions`), o algoritmos específicos (a menos que el prompt lo exija explícitamente).
- **INCLUIR:** Solo el "contrato" externo (inputs, outputs, comportamiento esperado).

## 🐋 DOCKER & AUDIT (Crítico)
- **PROHIBIDO:** Usar el comando `COPY` en el `Dockerfile` para archivos del proyecto.
- Los archivos deben llegar vía `RUN` o montaje de volúmenes en el comando `docker run`.
- **AUDIT.SH:** Es obligatorio ejecutar el script de auditoría **DENTRO** del contenedor. Fallar en esto resulta en offboarding.
- **Dockerfile check:** El linter busca creación de archivos que no sean de dependencias (Cargo.toml, package.json, requirements.txt, etc.).

## 🎯 ESTRUCTURA DEL PROMPT
1. **Objective:** Meta de alto nivel.
2. **Strategy:** Enfoque técnico (ej: "Use a sliding window algorithm").
3. **Constraints:** Limitaciones (ej: "Ensure memory safety", "Use asyncio").
4. **Expected Interface (MANDATORIO):**
   - **Path:** Ruta exacta.
   - **Name:** Clase/Método/Función.
   - **Type:** class/function/interface.
   - **Input/Output:** Tipos explícitos.
   - **Description:** Qué hace la interfaz (no cómo).

## 🧪 TESTS & COVERAGE
- Solo se permiten **Unit Tests**.
- Los tests deben ser agnósticos: alimentar la interfaz pública con inputs (incluso inválidos) y verificar el resultado o errores (ValueError, etc.).
- El coverage debe ser total sobre la implementación a través de la interfaz pública.

## 📏 RÚBRICAS
- Mínimo **10 criterios**.
- Pesos permitidos: **1, 3 o 5** (NUNCA 2 o 4).
- Dimensiones: Instruction Following, Code Correctness, Quality, Clarity, Efficiency.
- Deben ser **Atómicas** (una sola cosa por rúbrica) y **Positivas**.

---
*Documento preparado para la misión: oobabooga/text-generation-webui*
