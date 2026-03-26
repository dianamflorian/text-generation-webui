# 📚 CASO DE ESTUDIO: QUOTE BUILDER (Real Coder — Expert)
**Fecha:** Marzo 2026 | **Dificultad:** Expert | **Score:** ~94-95% (PASS)
**Tecnología:** React (Vite) + TypeScript + Tailwind CSS + Lucide-React

---

## 📋 Resumen del Proyecto
Herramienta de cotización para desarrolladores freelance. Calcula precios en tiempo real según tipo de proyecto, features seleccionadas, timeline, descuentos y taxes.

## ✅ Qué Funcionó Bien
- **Arquitectura determinista**: `PRICING_CONFIG` → `parseAndValidate` → `calculateQuote` → UI
- **Expected Interface completo**: Todos los tipos y funciones explícitos en el prompt
- **Network ban explícito**: Lista exhaustiva de APIs prohibidas en el prompt
- **0 Ambigüedad en fórmulas**: `Math.round(total / 85)`, `total * 0.40`, etc.

## ❌ Errores Que Ocurrieron (Lecciones)
1. **Tests con `.summary` wrapper** → Corregido a `calculateQuote(config)` directo
2. **Faltaba test de Rush timeline** → Añadido después del coverage check
3. **Faltaba test de páginas > 50** → Añadido (upper bound)
4. **Faltaba test de features inválidas** → Añadido + corregido `parseAndValidate`
5. **before.json truncado al pegar** → Usar archivo adjunto como fuente autoritativa
6. **parsing.py generaba 9 tests pero había 21** → Actualizado número

## 📁 Estructura Final de Archivos
```
review_task/
├── app/
│   ├── codebase.zip      ← Golden patch (sin carpeta raíz)
│   ├── tests.zip         ← Solo tests/
│   ├── Dockerfile        ← Solo package.json COPY
│   ├── parsing.py        ← Genera after.json (21 tests PASSED)
│   ├── run.sh            ← npm install + npm test
│   ├── before.json       ← 21 tests FAILED
│   └── after.json        ← 21 tests PASSED
├── src/
│   ├── constants/pricing.ts    ← PRICING_CONFIG
│   ├── logic/quoteEngine.ts    ← parseAndValidate + calculateQuote
│   └── components/QuoteBuilder.tsx
├── tests/
│   └── quoteEngine.test.ts    ← 21 tests F2P
└── with_solution/
    └── tests/quoteEngine.test.ts  ← Mismos 21 tests

```

## 🎯 Las 5 Rúbricas Finales (Aprobadas)
1. Real-time recalculation without submit (Weight 5)
2. Local-only assets, no network I/O (Weight 5)
3. PRICING_CONFIG con valores correctos (Weight 5)
4. QuoteBuilder validation pipeline (Weight 5)
5. Dashboard breakdown completo (Weight 3)

## 🧪 Los 21 Tests F2P Finales
1. Landing Page base price ($500)
2. Multi-page extra pages (3pgs = $900)
3. E-commerce at threshold (5pgs = $2000)
4. E-commerce extra pages (7pgs = $2300)
5. Web App extra pages (5pgs = $3600)
6. Feature percentages to base (auth 20% = $600)
7. Fast timeline multiplier (1.25x = $625)
8. Rush timeline multiplier (1.5x = $750)
9. Volume discount 8% for 5+ features ($828)
10. NO volume discount for < 5 features
11. Referral 10% after volume ($745.2)
12. NO referral when code is empty
13. Hours = Math.round(total / 85)
14. Effective rate = 2 decimales
15. Tax applied to total (10% = $550)
16. parseAndValidate: valid input → ok: true
17. parseAndValidate: invalid type → ok: false
18. parseAndValidate: pages < 1 → ok: false
19. parseAndValidate: pages > 50 → ok: false
20. parseAndValidate: tax > 20 → ok: false
21. parseAndValidate: invalid features → ok: false

## 📊 Dimensiones de Score
| Dimensión | Score | Notas |
|-----------|-------|-------|
| Instruction Following | 5/5 | Todo el prompt cubierto |
| Code Correctness | 5/5 | Lógica determinista verificada |
| Expected Interfaces | 5/5 | Todos declarados en prompt |
| F2P Methodology | 5/5 | 21 fail antes, 21 pass después |
| Code Quality | 4-5/5 | PRICING_CONFIG limpio |
