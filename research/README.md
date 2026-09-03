# research/ — Pipeline de investigación en 3 fases

| Fase | Modelo | Entrada | Salida |
|---|---|---|---|
| 1 — Estrategia | OPUS | `AI-AGENT-RESEARCH.md` | `PHASE1-STRATEGY.md`, `SCOPE-LOCK.md`, `SCORING.md`, `PHASE2-FABLE-RUNBOOK.md`, `HANDOFF-SPEC.md`, `schemas/` |
| 2 — Investigación | FABLE | `SCOPE-LOCK.md` + runbook + rúbrica + esquemas | `ledger.jsonl`, `cards/`, `evidence/`, `clusters.json`, `models.json`, `SUMMARY.jsonl`, `HANDOFF.md` |
| 3 — Auditoría y síntesis | OPUS | `HANDOFF.md` + `SUMMARY.jsonl` (+ fichas puntuales) | Informe final (secciones 1–20 del documento fuente) |

**Orden de lectura para empezar la FASE 2:** `SCOPE-LOCK.md` → `PHASE2-FABLE-RUNBOOK.md` → `SCORING.md` → `schemas/`.
FABLE **no** debe leer `AI-AGENT-RESEARCH.md` ni `PHASE1-STRATEGY.md`.

Regla vigente en las tres fases: **no se instala nada, no se ejecuta nada de terceros, no se modifica el equipo.**
