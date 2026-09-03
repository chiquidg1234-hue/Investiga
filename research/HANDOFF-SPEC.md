# CONTRATO DE ENTREGA FASE 2 → FASE 3 (auditoría por OPUS)

## 1. Estructura de ficheros exacta
```
research/
  SCOPE-LOCK.md                  (entrada, no se modifica)
  SCORING.md                     (entrada, no se modifica)
  PHASE2-FABLE-RUNBOOK.md        (entrada, no se modifica)
  schemas/*.json                 (entrada, no se modifica)
  ledger.jsonl                   toda URL vista + veredicto + kill_code + tokens
  queries.jsonl                  toda consulta ejecutada + nº resultados + hash top-20
  ecosystem-map.json             taxonomía + fuentes meta + test de curación
  triage.jsonl                   salida G2
  shallow.jsonl                  salida G3
  cards/<slug>.json              salida G4, una por finalista (≤8 KB)
  evidence/<slug>.jsonl          evidencias del finalista (E0–E4)
  clusters.json                  duplicados, dominancia y complementariedad
  models.json                    tabla de modelos (B11)
  papers.jsonl                   papers sin código utilizable
  commercial.jsonl               opciones SaaS cerradas (contexto de coste)
  coverage.json                  slots de arquetipo cubiertos/vacíos por bloque
  contradictions.md              contradicciones no resueltas (para OPUS)
  open-questions.md              lo que no se pudo verificar y por qué
  SUMMARY.jsonl                  ÍNDICE: una línea por finalista, ≤400 tokens
  HANDOFF.md                     portada de entrega (≤2 páginas)
```

## 2. `SUMMARY.jsonl` — el fichero que OPUS lee primero
Una línea por finalista, y **solo** estos campos (permite a OPUS ver los ~32 finalistas por ~13k tokens):
```json
{"key":"", "block":"", "archetype":"", "one_liner":"", "score_global":0, "score_track":0,
 "risk_tier":"", "vetoes":[], "windows_level":"", "hype_index":0, "flags":[],
 "perception":"", "actuation":"", "provides":[], "consumes":[],
 "top_evidence":["E-id","E-id"], "cluster_id":"", "open_questions_count":0, "tokens_spent":0}
```
OPUS abre `cards/<slug>.json` **solo** para los que vaya a rankear o auditar.

## 3. `HANDOFF.md` — portada obligatoria (≤2 páginas)
Debe contener, en este orden:
1. **Números de embudo**: descubiertos / triados / superficiales / finalistas / muertos por código de muerte.
2. **Tabla de cobertura**: por bloque, slots cubiertos vs vacíos, con las consultas ejecutadas para los vacíos.
3. **Presupuesto**: tokens gastados por etapa vs presupuestado; bloques con `budget_exhausted`.
4. **Top 10 hallazgos factuales** (hechos verificados, no recomendaciones), cada uno con su `evidence_id`.
5. **Lista de vetos** aplicados (V1–V8) con el proyecto afectado.
6. **Lista de `HYPE_FLAG`** con la claim concreta no verificada de cada uno.
7. **Lista de `HIDDEN_GEM`**.
8. **Clusters escalados a OPUS** (los que no tienen ganador mecánico) con su `tradeoff_summary`.
9. **Contradicciones abiertas** (enlace a `contradictions.md`).
10. **Lo que NO se investigó y por qué** (honestidad de cobertura).

**Prohibido en `HANDOFF.md`:** recomendaciones, arquitectura propuesta, rankings globales opinados,
lenguaje evaluativo sin evidencia. FABLE entrega hechos puntuados; OPUS decide.

## 4. Protocolo de auditoría de FASE 3 (cómo OPUS verifica sin releer todo)
1. **Muestreo aleatorio de evidencia:** OPUS elige 15 `evidence_id` al azar del conjunto E2/E3/E4 y los re-verifica
   contra la fuente. **>1 fallo ⇒ el lote del bloque se rechaza** y FABLE lo repite.
2. **Coherencia de rúbrica:** recalcular `score_global` desde las anclas A1–A10 y comprobar que coincide;
   comprobar la regla "ancla ≥4 exige ≥2 evidencias E2+".
3. **Detección de fichas huecas:** cualquier ficha con `tokens_spent` < 3.000 y `score_global` > 70 se re-audita.
4. **Detección de invención:** buscar campos factuales sin `evidence_ids` ni `"UNVERIFIED"` → error de protocolo.
5. **Auditoría de puntos ciegos:** revisar `coverage.json`; todo slot vacío exige justificación con consultas ejecutadas.
6. **Sesgo de popularidad:** comprobar que la correlación entre `stars` y `score_global` no es la que manda;
   si los 10 primeros son los 10 más populares, exigir a FABLE una ronda extra de hidden gems.
7. **Consistencia de vetos:** todo `risk_tier` R3/R4 debe tener `permissions` con evidencia E2 `path:line`.

## 5. Qué produce OPUS en FASE 3 (fuera del alcance de FABLE)
Las secciones 1–20 del informe final del documento original, en particular:
mapa del ecosistema comentado, TOP 25 global, rankings por categoría, los 10 componentes de mayor impacto,
proyectos no recomendados, arquitectura recomendada / mínima / avanzada, plan de implementación fases 0–7,
matriz de riesgo, coste estimado local vs híbrido vs cloud, hardware necesario, y fuentes.
