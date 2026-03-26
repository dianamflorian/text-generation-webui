# 📊 RÚBRICAS DE EVALUACIÓN: SOMETHING BIG
**Estándares de calidad para aprobación de tareas (Dimensiones y Criterios).**

---

## 1. El Prompt (Agnosticismo y Claridad)
- **Claridad:** Debe ser entendible sin ambigüedades. Detalles mayores no pueden ser omitidos.
- **Self-Containment (Tool Implementation):** La herramienta no debe depender del repo original. Debe ser repo-independiente.
- **Interfaces:** Obligatorio documentar puntos de entrada, inputs/outputs con tipos y descripción.
  - **Fallo:** Si >10% de las interfaces son inválidas o faltan.
  - **Fallo:** Si el prompt es "Implementation-Specific" (prescribe el CÓMO).

## 2. Golden Patch (Calidad del Código)
- **Fulfillment:** Todas las instrucciones del prompt deben ser *intentadas*.
- **Correctitud:** No debe tener errores de compilación o ejecución.
- **Diseño:** Debe ser modular y abstracto (fácil de mantener).
- **Performance:** Evitar algoritmos ineficientes (ej. O(n²) cuando es posible O(n log n)).
- **Readability:** Nombres de variables significativos y formato consistente.

## 3. Pruebas (Tests y F2P)
- **Coverage:** Los tests F2P deben cubrir TODOS los requerimientos del prompt.
- **Relevancia:** Los tests deben verificar comportamiento de la interfaz, no detalles internos.
  - **Fallo:** >10% de tests irrelevantes o >20% débilmente relevantes.
- **After JSON:** **TODOS** los tests F2P deben estar en `PASSED`.

## 4. Archivos Críticos (Checklist de Entrega)
- [ ] **Before/After JSON:** Salidas directas de la auditoría.
- [ ] **Run/Parsing Scripts:** Para la automatización del proceso.
- [ ] **Dockerfile:** Construcción limpia con `--platform linux/amd64`.
- [ ] **Golden Patch:** El código de la solución.

## 5. Rúbricas (Evaluación Hecha por el Colaborador)
- **Atomicidad:** Cada criterio evalúa UNA sola cosa.
- **Framing:** Deben ser redactadas en **POSITIVO** (un buen resultado es "Sí/Verdadero").
- **Self-Contained:** El auditor debe poder evaluar la rúbrica sin mirar el prompt (incluir el valor esperado).
- **Pesos:** Solo usar 1 (bajo), 3 (medio) o 5 (crítico). **Nunca 2 o 4.**

---

### ⚠️ Principales Causas de Rechazo (Fallo Inmediato)
1.  **Failing Tests:** Un test F2P que falle en el `after.json`.
2.  **Unsafe Code:** Inyecciones SQL, malware o exposición de datos sensibles.
3.  **Missing Critical Files:** Falta de parches o logs de JSON.
4.  **Bad Rubric Quality:** >10% de errores mayores en las rúbricas generadas.

*Documento preparado para cumplimiento de estándares de Outlier/Master Real Coder.*
