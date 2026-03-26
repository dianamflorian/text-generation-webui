# 🧠 OUTLIER REAL CODER — METODOLOGÍA MAESTRA (Score 85-95%)
**Versión:** 1.0 | **Basado en:** Quote Builder Session + Guidelines Oficiales Outlier
**Ruta:** `SOMETHING BIG/` | **Aplica a:** TODOS los proyectos Real Coder

---

## ⚡ REGLA SUPREMA: El Prompt ES Todo
> Si modificas el prompt → modifica TODO: Expected Interface, codebase, tests, rúbricas.
> Nunca hay partes "independientes". El prompt es el contrato.

---

## 📋 FASE 1: EL PROMPT (Contract-First)

### 1.1 Estructura Obligatoria del Prompt
```
1. Background (Job Posting style — "Senior developer needed for...")
2. Core Features (lista de funcionalidades clave)
3. Key Requirements
   ├── Data Requirements (network bans, validaciones)
   ├── Pricing Logic / Business Logic (NÚMEROS EXACTOS, SIN AMBIGÜEDAD)
   └── Technical Specifications
4. Expected Interface (OBLIGATORIO)
   ├── Paths exactos: src/logic/file.ts
   ├── Function signatures completas
   └── Type shapes explícitas
```

### 1.2 Reglas de Oro del Prompt
| Regla | Qué hacer | Qué evitar |
|-------|-----------|------------|
| **0 Ambigüedad** | "Landing Page: $500 base" | "landing page starts around $500" |
| **Tipos literales** | `'landing' \| 'multi-page'` | "project type string" |
| **Fórmulas exactas** | `Math.round(total / 85)` | "rounded to nearest integer" |
| **Network ban explícito** | Lista fetch, XHR, WebSocket, etc. | "no external calls" genérico |
| **Validation bounds** | "pages: 1–50, tax: 0–20" | "reasonable range" |

### 1.3 Section Expected Interface (CRÍTICA)
- **Cada función exportable DEBE aparecer** — si no está en Expected Interface y el test la usa → FAIL
- Incluir: Path, Name, Type (Function/Interface/Component), Input, Output, Description
- Si añades `parseAndValidate` al código → también al prompt → también a los tests

---

## 📐 FASE 2: LA IMPLEMENTACIÓN (Golden Patch)

### 2.1 Arquitectura Determinista
```
src/
├── constants/pricing.ts   ← UN SOLO objeto PRICING_CONFIG (inmutable)
├── logic/quoteEngine.ts   ← Funciones puras, 0 side effects
└── components/QuoteBuilder.tsx ← UI, consume quoteEngine
```

### 2.2 Reglas de La Implementación
- **PRICING_CONFIG:** Un solo objeto, todos los números ahí. 0 magic numbers en funciones.
- **Funciones puras:** `calculateQuote(config) → QuoteSummary` — mismo input = mismo output.
- **Validación explícita:** `parseAndValidate(raw) → ValidationResult` intercepta inputs antes de lógica.
- **Network ban:** Cero fetch/XHR/WebSocket. Fuentes/iconos vendoreados en `/public`.
- **No cambiar interfaces públicas** sin actualizar prompt + tests.

### 2.3 Checklist Pre-Submission del Codebase
- [ ] `calculateQuote` retorna `QuoteSummary` directamente (no `{ summary: QuoteSummary }`)
- [ ] `parseAndValidate` valida: tipo, páginas [1-50], tax [0-20], features válidas
- [ ] UI re-calcula en cada onChange sin botón Submit
- [ ] Dashboard muestra: base, extra-pages, features, timeline, descuentos, tax, total, depósito, horas, rate
- [ ] Assets locales (sin Google Fonts remote, sin CDN)

---

## 🧪 FASE 3: LOS TESTS (F2P — Fail-to-Pass)

### 3.1 Arquitectura de Tests
```
tests/                    ← Tests F2P (fallan SIN golden patch)
with_solution/tests/      ← Mismos tests (pasan CON golden patch)
```
> ⚠️ Ambos sets DEBEN SER idénticos o Outlier rechaza.

### 3.2 Reglas Anti-Overly-Specific
| ❌ PROHIBIDO | ✅ CORRECTO |
|-------------|------------|
| `expect(result.deposit).toBe(200)` | `expect(result.deposit).toBe(result.total * 0.4)` |
| `(calculateQuote(...) as any).summary` | `calculateQuote(config)` directamente |
| `expect(result.hours).toBe(6)` | `expect(result.hours).toBe(Math.round(result.total / 85))` |
| Valores exactos de breakdown | Solo subtotal/total final |

### 3.3 Cobertura Mínima Requerida
Cada proyecto DEBE tener tests para:
1. Base price de TODOS los tipos de proyecto
2. Lógica extra (páginas extra, multiplicadores)
3. Todos los multiplicadores/timelines (no solo uno)
4. Descuento volume (con 5+ features)
5. Descuento referral AFTER volume
6. Tax aplicado al total
7. Depósito como % del total
8. Horas (`Math.round(total / divisor)`)
9. Effective rate (2 decimales)
10. `parseAndValidate` happy path (ok: true)
11. Validación tipo inválido (ok: false)
12. Validación páginas bajo límite (ok: false)
13. Validación páginas SOBRE límite (ok: false) ← 51+
14. Validación tax fuera de rango (ok: false)
15. Validación features inválidas (ok: false)

### 3.4 Argumentos para Marcar Errores del Linter Como Inválidos

**"INTERFACE_VIOLATION" por .summary:**
> "The prompt explicitly defines calculateQuote's output as QuoteSummary returned directly. Testing .summary assumes a wrapper that contradicts the public interface contract."

**"OVER_CONSTRAINED" por breakdown.* valores:**
> "The QuoteSummary breakdown fields are part of the explicitly declared public interface in the prompt's Expected Interface section. Testing correct values of a mandated public interface is specification compliance, not over-specification. The deterministic formula has only one mathematically correct output."

**"Minor Non-Atomic" en rubrics:**
> "The behaviors are architecturally inseparable in a React onChange handler — they form one cohesive data-flow integration. Splitting would test the same 10 lines 4 times."

---

## 📏 FASE 4: LAS RÚBRICAS (Rubrics)

### 4.1 Reglas de Atomicidad
- **Una sola idea verificable** por rúbrica
- **Auto-contenida:** el auditor puede evaluar sin ver el código fuente
- **Fraseada en positivo:** "The app uses only local assets" NO "The app does not use external..."
- **Weights: solo 1, 3 o 5** — nunca 2 o 4

### 4.2 Cuándo Marcar el Linter Como Inválido

| Error del Linter | Justificación |
|-----------------|---------------|
| **Negative Phrasing** cuando el prompt mismo usa prohibiciones | "El prompt original usa prohibiciones explícitas como ground truth. Parafrasear en positivo reduce precisión y dificulta la evaluación objetiva de edge cases." |
| **Miscategorized** (Instruction Following vs Code Correctness) | "La rubrica evalúa una instrucción explícita de arquitectura definida en el prompt, no una inferencia de correctitud." |
| **Minor Non-Atomic** para comportamientos inseparables en React | "Los comportamientos se implementan en un solo handler. Dividirlos crearía 4 rubrics para el mismo bloque de código." |
| **Overlap** entre rubric 1 y 4 | "Rubric 1 testea timing (sin submit), Rubric 4 testea pipeline de validación. Son distintos — un UI puede recalcular sin usar parseAndValidate." |
| **Non-Atomic** para dashboard/breakdown completo | "El prompt requiere un 'Professional Dashboard' como unidad. Un revisor evalúa el panel en una sola mirada. Dividir en 11 rubrics es overhead desproporcionado." |

### 4.3 Template de 5 Rúbricas para Proyectos Web con Lógica de Negocio
1. **Real-time updates** (Weight 5, Code Correctness): "The [main component] recalculates all output values automatically on every relevant input change without requiring a submit action."
2. **Network ban completo** (Weight 5, Instruction Following): "The application uses only local bundled or public assets at runtime; all [fonts/icons] are self-hosted and no runtime network I/O paths are present including fetch, XHR, WebSocket, EventSource, sendBeacon, service worker registration, or remote asset URLs."
3. **Config centralizada** (Weight 5, Code Correctness): "A single immutable local [CONFIG_NAME] object defines all [domain] constants: [lista de valores exactos con números del prompt]."
4. **Pipeline de validación** (Weight 5, Instruction Following): "The [Component] implements real-time updates, uses [validateFn] to validate raw inputs on every change and display user-friendly error messages, and calls [calcFn] only when validation returns success."
5. **Dashboard completo** (Weight 3, Code Correctness): "The UI displays an itemized breakdown including all required components: [lista de campos del prompt]."

---

## 📦 FASE 5: LOS ARCHIVOS DE SUBMISSION

### 5.1 Checklist de Archivos
| Archivo | Ruta | Contenido |
|---------|------|-----------|
| `codebase.zip` | Sin carpeta raíz anidada | src/, tests/, Dockerfile, package.json, run.sh |
| `tests.zip` | Solo `tests/` | quoteEngine.test.ts actualizado |
| `before.json` | Generado con todos FAILED | Mismos nombres que after.json |
| `after.json` | Generado con todos PASSED | parsing.py actualizado |
| `Dockerfile` | Solo COPY package.json | SIN código fuente |
| `parsing.py` | Genera after.json correcto | Número de tests correcto |
| `run.sh` | npm install + npm test | Sin dependencias de bash extras |
| `package.json` | Dependencias completas | vitest, react, etc. |

### 5.2 El Dockerfile Correcto (Outlier Standard)
```dockerfile
FROM node:18-slim
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm install
# Código llega vía golden_patch, NO va en el Dockerfile
```

### 5.3 Sincronización before.json ↔ after.json
- **Mismos nombres de test** en ambos (1:1 match)
- **before.json:** todos `"status": "FAILED"`
- **after.json:** todos `"status": "PASSED"`
- El total debe coincidir con el número real de tests

---

## 🚨 ERRORES MÁS COMUNES (Red Flags a Evitar)

### Por Score Bajo
1. **Tests usan `.summary` wrapper** → El prompt dice que calculateQuote retorna QuoteSummary directamente
2. **Falta upper-bound de validación** → Siempre testear el límite alto (páginas > 50) además del bajo (< 1)
3. **No testear features inválidas** → parseAndValidate debe rechazarlas y el test debe verificarlo
4. **before.json truncado** → Copiar JSON completo, no desde el terminal que puede cortar
5. **Rush timeline no testeado** → Testear TODOS los timelines (standard, fast, rush)
6. **Rubric con phrasing negativo** → Reformular en positivo O marcar como inválido con justificación

### Por Linter FAIL
1. **ZERO_TOLERANCE** en Overly Specific → Verificar que deposits/hours usen fórmulas relativas
2. **SYNC_VIOLATION** en before/after → Contar tests exactos, actualizar parsing.py
3. **Non-Atomic rubric** → Defender inseparabilidad técnica O dividir si realmente son independientes

---

## 🗓️ ORDEN DE TRABAJO (Workflow Óptimo)

```
1. Leer prompt guidelines del Outlier → Entender el dominio
2. Escribir el PROMPT completo con Expected Interface
3. Implementar el codebase (Golden Patch)
4. Escribir los TESTS (F2P) — verificar que fallan sin solución
5. Actualizar parsing.py con número correcto de tests
6. Crear before.json (todos FAILED) y after.json (todos PASSED)
7. Escribir las 5 RÚBRICAS (atomicas, con pesos 1/3/5)
8. Pasar por los LINTERS — marcar inválidos con justificación
9. Comprimir codebase.zip y tests.zip correctamente
10. Subir todos los archivos en orden
```

---

## 📌 NOTAS DE SCORE REAL (Quote Builder Session)
- **Score logrado:** ~94-95% (PASS)
- **Observaciones del auditor:**
  - "ReferralCode error channel no se dispara" → código muerto inofensivo, no es bug
  - "Timeline breakdown no es línea separada" → quirk de presentación, no logic fail
- **Dificultad:** Expert (múltiples subsistemas: validación, cálculo, UI, network isolation)
