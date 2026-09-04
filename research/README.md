# research/ — Pipeline de investigación en 3 fases

| Fase | Modelo | Entrada | Salida |
|---|---|---|---|
| 1 — Estrategia | OPUS | `AI-AGENT-RESEARCH.md` | `PHASE1-STRATEGY.md`, `SCOPE-LOCK.md`, `SCORING.md`, `PHASE2-FABLE-RUNBOOK.md`, `HANDOFF-SPEC.md`, `schemas/` |
| 2 — Investigación | FABLE | `SCOPE-LOCK.md` + runbook + rúbrica + esquemas | `ledger.jsonl`, `cards/`, `evidence/`, `clusters.json`, `models.json`, `SUMMARY.jsonl`, `HANDOFF.md` |
| 3 — Auditoría y síntesis | OPUS | `HANDOFF.md` + `SUMMARY.jsonl` (+ fichas puntuales) | Informe final (secciones 1–20 del documento fuente) |

**Orden de lectura para empezar la FASE 2:** `SCOPE-LOCK.md` → `PHASE2-FABLE-RUNBOOK.md` → `SCORING.md` → `schemas/`.
FABLE **no** debe leer `AI-AGENT-RESEARCH.md` ni `PHASE1-STRATEGY.md`.

Regla vigente en las tres fases: **no se instala nada, no se ejecuta nada de terceros, no se modifica el equipo.**

## Estado FASE 2 (2026-09-03)
Artefactos generados: `ledger.jsonl`, `triage.jsonl`, `rejected.md`, `cards/` (41), `evidence/` (41), `clusters.json`, `models.json`, `ecosystem-map.json`, `coverage.json`, `windows-matrix.md`, `contradictions.md`, `open-questions.md`, `papers.jsonl`, `commercial.jsonl`, `queries.jsonl`, `SUMMARY.jsonl`, `HANDOFF.md`.
Regenerables con `python3 research/tools/build_artifacts.py && python3 research/tools/build_meta.py` (sin red). Datos brutos en `raw/`.

Separación pedida por el usuario: ecosystem → `ecosystem-map.json`; candidates → `triage.jsonl`; computer-use/multi-agent/memory/research/MCP/Claude Code → `cards/` por `block` (B2/B4/B6/B5/B7/B8) y `SUMMARY.jsonl`; Windows → `windows-matrix.md`; security → `cards/*.security` + `clusters.json` C3/C6; evaluation → `models.json` + `papers.jsonl`; evidence → `evidence/`; rejected → `rejected.md`.

## Estado FASE 3 (2026-09-03)
`PHASE3-DECISION.md` — auditoría de FABLE, decisión arquitectónica y plan de implementación.
Correcciones de auditoría aplicadas: ficha de `cursortouch/windows-mcp` (permisos reales + telemetría),
campo `audit_opus` en la ficha afectada. Hallazgos F1–F8 documentados en la sección 1.2 de la decisión.
