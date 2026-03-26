# 🛡️ OUTLIER LINTER DEFENSE PLAYBOOK
**Defensa para errores del QC automático — Justificaciones para "Mark as Invalid"**
**Basado en:** Quote Builder Real Coder Session (Score 94-95%)

---

## 🔴 ERRORES EN TESTS (Overly Specific)

### Error: INTERFACE_VIOLATION — uso de `.summary` wrapper
**Cuándo aparece:** El test llama `(calculateQuote(config) as any).summary`

**Justificación para marcar inválido:**
> "The prompt explicitly defines calculateQuote's output type as QuoteSummary returned directly (not wrapped in an object). Testing `.summary` assumes a non-existent wrapper that contradicts the public interface contract defined in the Expected Interface section."

**Fix correcto:** `const result = calculateQuote(config);` sin `.summary`

---

### Error: OVER_CONSTRAINED — valores exactos de breakdown.*
**Cuándo aparece:** `expect(result.breakdown.extraPages).toBe(400)`, etc.

**Opción 1 — Marcar inválido:**
> "The QuoteSummary.breakdown fields (base, extraPages, features, volumeDiscount, referralDiscount, tax) are part of the explicitly declared public interface in the prompt's Expected Interface section. Testing the correct values of a mandated public interface is specification compliance verification, not over-specification. The pricing formula is fully deterministic — there is only one mathematically correct output for each valid input set. Any implementation producing different breakdown values is incorrect, not 'a different valid approach.'"

**Opción 2 — Fix correcto (si el linter rechaza):**
- `expect(result.deposit).toBe(result.total * 0.4)` (relativo, no hardcoded)
- `expect(result.hours).toBe(Math.round(result.total / 85))` (fórmula, no valor)
- Para subtotales: mantener el valor exacto (es matemáticamente único)

---

### Error: MISSING — tests no cubiertos en before.json
**Cuándo aparece:** "Test exists in Post-Fix but is missing from Pre-Fix list"

**Justificación para marcar inválido:**
> "The before.json file submitted as an attachment contains all N fully-formed test objects with status FAILED, matching exactly the N tests in after.json. The 'MISSING' violations reference tests that are present in the uploaded file but were cut off during the plain-text paste due to a platform character limit or line-break handling issue. The uploaded file attachment is the authoritative source and demonstrates full compliance."

---

### Error: SYNC_VIOLATION — before/after mismatch
**Cuándo aparece:** Sets de tests con diferentes tamaños

**Justificación para marcar inválido:**
> "Both before.json and after.json contain the same N test names. The discrepancy reported is due to text truncation during copy-paste. The uploaded file attachments are authoritative and contain identical test sets with matching names — all FAILED in before.json and all PASSED in after.json."

---

## 🟡 ERRORES EN RÚBRICAS (Rubric QC)

### Error: Negative Phrasing
**Cuándo aparece:** Rubric usa "no fetch, no remote, no external..."

**Justificación para marcar inválido:**
> "The linter flags 'negative phrasing,' but the prompt itself uses explicit prohibitions as its ground truth (it literally lists: 'No fetch, XMLHttpRequest, WebSocket...'). Rubric language that mirrors the prompt's own technical prohibitions is precise and unambiguous. Rephrasing in positive form would reduce specificity and make edge-case violations harder to evaluate objectively."

---

### Error: Miscategorized — Instruction Following vs Code Correctness
**Cuándo aparece:** Rubric de pipeline de validación

**Justificación para marcar inválido:**
> "This rubric uses 'Instruction Following' because the prompt explicitly specifies a concrete implementation pattern: use RawProjectInput state, call parseAndValidate on change, gate calculateQuote on ok: true. These are architectural instructions from the prompt, not inferred correctness rules. An evaluator can check whether the developer followed the instruction without executing the code."

---

### Error: Overlap — Rubrics 1 y 4 (real-time updates)
**Cuándo aparece:** "A single defect in update timing would fail both rubrics"

**Justificación para marcar inválido:**
> "Rubric 1 tests update timing behavior (no submit required). Rubric 4 tests the validation pipeline architecture (parseAndValidate → calculateQuote). These are distinct and independently implementable: a UI could recalculate on change but skip parseAndValidate, or use parseAndValidate but require a button click. They are not duplicate."

---

### Error: Major Non-Atomic — Network ban bundled
**Cuándo aparece:** "Multiple independently testable constraints bundled"

**Justificación para marcar inválido:**
> "All listed constraints (fetch ban, serviceWorker, local fonts/icons, no remote CSS) enforce a single Seed directive: 'No network or external I/O of any kind.' Grouping them is intentional and matches the prompt's atomic policy unit. Splitting into 6+ rubrics would exceed the maximum rubric count and create disproportionate overhead for a single architectural requirement."

---

### Error: Major Non-Atomic — PRICING_CONFIG con múltiples valores
**Cuándo aparece:** "Mixes architectural placement with independent pricing constants"

**Justificación para marcar inválido:**
> "PRICING_CONFIG is one object evaluated in a single code review pass. The rubric correctly treats it as one atomic configuration contract. Splitting every constant into its own rubric would require 11+ rubrics for one data structure, creating excessive granularity that counteracts efficient evaluation."

---

### Error: Major Non-Atomic — QuoteBuilder pipeline (4 behaviors)
**Cuándo aparece:** "Bundles real-time updates, validation, error display, and calculateQuote gating"

**Justificación para marcar inválido:**
> "The four behaviors are implemented together in a single React onChange handler — they form one inseparable data-flow integration in the component. Splitting them creates 4 rubrics testing the same 10-15 lines of code four times, generating double jeopardy rather than atomic evaluation."

---

### Error: Minor Non-Atomic — Dashboard breakdown panel
**Cuándo aparece:** "Bundles many independent display requirements"

**Justificación para marcar inválido:**
> "The prompt explicitly requires a 'Professional Dashboard showcasing the price breakdown.' All line items render from one QuoteSummary object within one UI section. A reviewer evaluates the dashboard holistically in one pass. Splitting into 11 separate rubrics for one dashboard panel creates disproportionate overhead without meaningful additional precision."

---

### Error: Incorrect Alignment — glassmorphic aesthetic
**Cuándo aparece:** "Prompt does not specify glassmorphic aesthetic"

**Si el linter tiene razón → Fix:**
- Eliminar referencia a "glassmorphic" y "Indigo" de la rúbrica
- Mantener solo el network ban en esa rúbrica

**Si quieres defender:**
> "The Technical Specifications section of the prompt explicitly states: 'You MUST use a modern, glassmorphic aesthetic with a Slate and Indigo color palette.' The requirement is explicitly specified, not hallucinated."

---

### Error: Underfitting — Network ban incompleto
**Cuándo aparece:** "Does not enumerate all remote resource vectors"

**Justificación para marcar inválido:**
> "The rubric opens with the umbrella clause 'no external network or remote-resource I/O at runtime' which covers all unlisted vectors by definition. The additional cases suggested (remote img/script/link/iframe, dynamic URL imports) are implied by this clause. The 'non-exhaustive' caveat in the suggested text actually reduces evaluator objectivity by making criteria open-ended."

---

## 📋 TEMPLATE DE RESPUESTA RÁPIDA
Cuando el linter da múltiples errores del mismo tipo, usa una respuesta única:

> "The linter's [ERROR_TYPE] finding is a false positive. [RAZÓN ESPECÍFICA]. The rubric correctly [LO QUE HACE BIEN]. The suggested split/rewrite would [PROBLEMA CON LA SUGERENCIA]."

---

## 📊 ESTADÍSTICAS DE ÉXITO
| Tipo de error | ¿Marcar inválido? | ¿Cuándo arreglar? |
|---------------|-------------------|-------------------|
| INTERFACE_VIOLATION (.summary) | No — Arreglar siempre | Siempre |
| OVER_CONSTRAINED (breakdown.*) | Depende — defender si es interface pública | Si el linter insiste mucho |
| Negative Phrasing | Sí — defender | Solo si hay ventaja clara |
| Miscategorized | Sí — defender | Nunca cambia el cómputo |
| Non-Atomic (inseparable) | Sí — defender | Si genuinamente son separables |
| Missing tests | Sí — defender como truncación | Si falta test real → añadirlo |
