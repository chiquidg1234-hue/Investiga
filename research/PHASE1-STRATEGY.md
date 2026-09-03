# FASE 1 — ESTRATEGIA DE INVESTIGACIÓN (OPUS)
Diseño operativo para ejecutar `AI-AGENT-RESEARCH.md` con dos modelos: OPUS y FABLE.
No contiene investigación. Contiene el plan que la hace ejecutable, barata y auditable.

---

## 1. ESTRATEGIA GENERAL

### 1.1 El problema real
El documento fuente pide 33 secciones de investigación. Ejecutado de forma ingenua es un trabajo
divergente: miles de repositorios, evidencia irrepetible y un informe imposible de auditar.
El riesgo dominante **no** es encontrar pocos proyectos: es producir un informe que **suene** bien
y no sea verificable. El documento lo dice explícitamente ("no quiero un recopilador de listas").

### 1.2 Las cuatro apuestas de diseño
1. **Separar hechos de juicios.** FABLE solo produce *hechos con fuente* y *puntuaciones con rúbrica*.
   OPUS produce *decisiones*. Ningún juicio arquitectónico se delega. Esto es lo que hace auditable la FASE 3.
2. **Embudo con puertas de coste creciente.** Cinco puertas (G0–G5). Un candidato malo debe morir
   costando ~300 tokens, no 12.000. El 80% del presupuesto se gasta en el 6% de los candidatos.
3. **Evidencia tipada (E0–E4) como moneda única.** Toda afirmación lleva clase de evidencia, URL, SHA y fecha.
   Esto convierte "detectar hype" de una intuición a una **resta**: claims declaradas − claims verificadas.
4. **Anti-duplicación por ledger, no por memoria.** El estado vive en disco (`ledger.jsonl`), no en el contexto.
   FABLE puede reiniciar contexto en cada bloque sin repetir trabajo. Es el mayor ahorro de tokens del plan.

### 1.3 Decisiones estructurales tomadas en esta fase
- **Windows 11 es un filtro, no un criterio.** Un proyecto W6 (no viable en Windows) en las categorías de
  computer use / automatización se mata en G3, no se puntúa y se descarta. WSL/Docker no controlan el
  escritorio host: eso es una limitación funcional, no un detalle de instalación.
- **La seguridad es un capado, no un sumando.** Un veto (V1–V8) limita la puntuación final por encima del
  peso de 15 puntos. Se cumple así la regla absoluta del documento.
- **Dos puntuaciones, no una.** `score_global` (pesos fijos del documento) para comparar todo;
  `score_track` (renormalizado sin el eje Computer Use) para rankear dentro de categorías donde
  ese eje no aplica. Sin esto, una librería de memoria excelente parece peor que un agente GUI mediocre.
- **Las combinaciones se calculan, no se imaginan.** Cada ficha declara `provides[]` y `consumes[]`.
  La complementariedad sale de una intersección de conjuntos; OPUS solo compone sobre esa matriz.
- **El hardware es un techo duro.** 2 GB de VRAM. FABLE **mide** requisitos y clasifica L0–L4;
  la decisión local vs cloud es exclusivamente de OPUS.

### 1.4 Lo que esta estrategia decide NO hacer
- No perseguir cobertura exhaustiva del ecosistema: se persigue **cobertura de arquetipos** (matriz de slots).
  Es la diferencia entre 500 fichas inútiles y 32 fichas que cubren todas las formas de resolver el problema.
- No evaluar SaaS cerrados como componentes (van a una lista aparte, solo como referencia de coste).
- No leer el documento original en FASE 2: se sustituye por `SCOPE-LOCK.md` (~150 líneas). Ahorro directo
  de ~25k tokens por sesión de FABLE, multiplicado por 11 bloques.

---

## 2. DIVISIÓN EXACTA OPUS / FABLE

### Principio de reparto
> **FABLE** hace todo lo que puede **contrastarse contra una fuente** (existe / no existe, cuándo, cuánto, dónde en el código).
> **OPUS** hace todo lo que exige **elegir entre alternativas cuyo valor depende del resto del sistema**.

| # | Tarea | Dueño | Por qué |
|---|---|---|---|
| 1 | Compilar `SCOPE-LOCK`, rúbrica, esquemas y runbook | OPUS (FASE 1) | Define el marco; es la fuente de la reproducibilidad |
| 2 | Descubrir fuentes meta y construir la taxonomía del ecosistema | FABLE | Recopilación verificable |
| 3 | Ejecutar consultas y generar el pool de candidatos | FABLE | Trabajo masivo, sin juicio |
| 4 | Aplicar reglas de muerte K1–K15 | FABLE | Reglas mecánicas, sin criterio |
| 5 | Extraer claims y asignar clases de evidencia E0–E4 | FABLE | Contrastable contra código/documentación |
| 6 | Medir actividad, madurez, bus factor, cadena de suministro | FABLE | Métricas duras |
| 7 | Determinar nivel Windows W1–W6 | FABLE | Detección por dependencias, CI, issues |
| 8 | Enumerar superficie de permisos y derivar `risk_tier` | FABLE | Búsqueda de código con `path:line` |
| 9 | Aplicar vetos V1–V8 | FABLE | Condiciones booleanas |
| 10 | Puntuar A1–A10 con anclas | FABLE | Rúbrica anclada; OPUS re-audita |
| 11 | Clasificar viabilidad local L0–L4 de modelos | FABLE | Comparar requisitos publicados con el hardware |
| 12 | Rellenar `provides[]/consumes[]` | FABLE | Lectura de interfaces |
| 13 | Construir clusters y tablas cabeza a cabeza | FABLE | Agrupar y tabular |
| 14 | **Elegir ganador de un cluster no dominado** | **OPUS** | Depende del stack objetivo |
| 15 | **Resolver contradicciones entre fuentes** | **OPUS** | Requiere juicio sobre credibilidad |
| 16 | **Decidir qué es hype con consecuencias** (lista "no recomendados") | **OPUS** | FABLE aporta el índice; OPUS lo interpreta |
| 17 | **Decidir local vs cloud por componente** | **OPUS** | Trade-off coste/privacidad/latencia/calidad |
| 18 | **Decidir mecanismo de percepción/acción del agente** (visión vs UIA vs DOM vs híbrido) | **OPUS** | Es la decisión arquitectónica central |
| 19 | **Componer los stacks (CORE / HIGH VALUE / OPTIONAL / EXPERIMENTAL / AVOID)** | **OPUS** | Depende de complementariedad y de redundancia |
| 20 | **Calcular impacto MARGINAL de cada componente dado el resto** | **OPUS** | FABLE mide impacto aislado; el marginal es contextual |
| 21 | **Arquitectura recomendada / mínima / avanzada** | **OPUS** | Diseño |
| 22 | **Plan de implementación fases 0–7, matriz de riesgo, coste, hardware** | **OPUS** | Decisión y planificación |
| 23 | **Auditar a FABLE por muestreo y rechazar lotes** | **OPUS (FASE 3)** | Control de calidad independiente |

### Prohibiciones cruzadas
- FABLE **no** escribe recomendaciones, ni rankings globales, ni arquitectura, ni resuelve contradicciones.
- OPUS **no** vuelve a hacer descubrimiento masivo en FASE 3: si falta cobertura, devuelve el bloque a FABLE.

---

## 3. PIPELINE DE INVESTIGACIÓN

### 3.1 Orden de ejecución de los 11 bloques (no arbitrario)
```
B1  Meta / ecosistema        ← primero: genera semillas para todos los demás
 ├─ B2  Computer Use / GUI agents      ← categoría crítica, máximo presupuesto
 ├─ B3  Substrato de automatización     ← define lo que B2 puede o no hacer en Windows
 ├─ B7  MCP y tool use                  ← capa de integración transversal
 ├─ B11 Modelos + local/cloud           ← condiciona la viabilidad de B2 en este hardware
 ├─ B4  Frameworks y orquestación
 ├─ B6  Memoria y contexto
 ├─ B5  Research agents
 ├─ B8  Claude Code / prompting
 ├─ B9  Seguridad, permisos, HITL
 └─ B10 Observabilidad y evaluación
                 ↓
        SEC-PASS  (pasada transversal de seguridad sobre TODOS los finalistas)
                 ↓
        G5  Clusters + complementariedad
                 ↓
        HANDOFF  →  FASE 3 (OPUS)
```
Razones del orden: B1 alimenta a todos; B2/B3 determinan si el objetivo central es siquiera posible;
B7 y B11 son transversales y cambian cómo se evalúa todo lo demás; B9 se descubre tarde pero se **aplica**
a todo mediante SEC-PASS, porque la seguridad se juzga sobre finalistas reales, no sobre candidatos muertos.

### 3.2 Las cinco puertas
| Puerta | Qué hace | Coste/candidato | Supervivencia |
|---|---|---|---|
| G0 | Fuentes meta + taxonomía | ~1k por fuente | 25–40 fuentes |
| G1 | Descubrimiento multi-señal (6 vectores obligatorios) | ~30 tok | 350–500 URLs |
| G2 | Triage solo con metadatos de API (K1–K10) | ≤300 tok | 80–110 |
| G3 | Evidencia superficial: README parcial + sondas grep + CI + issues (K11–K15) | ≤2.5k tok | 28–36 |
| G4 | Evidencia profunda: arquitectura, permisos, Windows, madurez, benchmarks, externo | ≤12k tok | 28–36 fichas |
| G5 | Clusters, dominancia, complementariedad | ~15k total | 8–14 clusters |

Detalle completo, consultas por bloque, sondas, reglas de muerte y matriz de cobertura:
**`research/PHASE2-FABLE-RUNBOOK.md`**.

### 3.3 Mecanismo anti-punto-ciego
Cada bloque tiene **slots de arquetipo** (RUNBOOK §3.4). Un bloque no se cierra sin ≥2 candidatos vivos
por slot, o una nota `slot_empty` con las consultas ejecutadas. Esto evita el fallo típico de
"encontré 40 frameworks de agentes y ningún driver de UI Automation para Windows".

---

## 4. CRITERIOS DE EVALUACIÓN

Todos los criterios son **detectables mecánicamente**. Definiciones exactas en RUNBOOK y SCORING.

| Criterio | Cómo se determina objetivamente |
|---|---|
| **Descubrir repositorios** | 6 vectores obligatorios: topics alto/bajo rango de estrellas, búsqueda **en código**, grafo de dependientes, grafo de autores, fuentes externas. Máx 12 consultas/bloque con deduplicación por hash del top-20 |
| **Filtrar candidatos** | K1–K10 en G2 (metadatos), K11–K15 en G3 (evidencia). Prohibido matar por pocas estrellas o promover por muchas |
| **Detectar hype** | `hype_index = 1 − claims_verificadas(E2+)/claims_totales`. `HYPE_FLAG` si ≥0.5 con ≥5.000 estrellas. **Siempre acompañado de la claim concreta que falló** |
| **Verificar actividad real** | Commit *sustantivo* (toca código, no docs/CI); `days_since_substantive_commit`; committers humanos en 90d; `docs_only_commit_ratio > 0.7` = teatro de actividad; `bus_factor_top_share > 0.9` = riesgo de abandono |
| **Compatibilidad Windows 11** | Escalera W1–W6. Señales: dependencias nativas (UIA/Win32/pywin32/comtypes), job `windows-latest` en CI, instrucciones PowerShell, dependencia de WSL/Docker/VM, ratio de issues abiertas que mencionan Windows, soporte multi-monitor y DPI. **WSL ≠ compatible** para control del escritorio |
| **Seguridad** | Superficie de 16 permisos con evidencia `path:line` → `risk_tier` R0–R4; aislamiento; mecanismo de aprobación; gestión de secretos; defensa frente a prompt injection; cadena de suministro (lockfile, post-install, `curl\|bash`, releases firmados, advisories); rutas de exfiltración de datos |
| **Permisos** | Enumeración explícita + qué puede ver, qué puede modificar, qué podría salir mal, cómo aislarlo, cómo revocarlo, cómo desinstalarlo (§31 del documento fuente) |
| **Arquitectura** | Mapa del bucle percepción→decisión→acción→**verificación**. Un sistema que actúa sin verificar el resultado no pasa de A3=3. Acoplamiento, modularidad, si exige adoptar todo el framework |
| **Madurez** | Edad, releases/año, frecuencia de cambios rompientes, tests reales en CI (no solo lint), tipado, estabilidad de la API pública |
| **Mantenimiento** | Committers humanos 90d, bus factor, mediana de primera respuesta a issues, crecimiento del backlog, releases 12 meses, roadmap público |
| **Coste** | Modelo-agnóstico o no; llamadas de modelo por acción; posibilidad de modelos baratos/locales; optimizaciones medidas (caché, compresión, batching) |
| **Valor real para el agente** | 16 ejes de impacto (−2..+3) medidos **en aislamiento** por FABLE; el **impacto marginal dado el resto del stack** lo calcula OPUS |

### Clases de evidencia (moneda común)
`E0` afirmación de README · `E1` documentación del mecanismo · `E2` código verificado (`path:line` + SHA)
· `E3` verificación independiente (paper, tercero, issue de no-mantenedor, auditoría) · `E4` resultado medido con harness y fecha.

### Comparación de repositorios que resuelven el mismo problema
Cluster (mismo arquetipo + ≥60% de `provides[]` comunes) → tabla de 9 ejes con **una evidencia
discriminante por celda** → si un miembro gana o empata en los 9 y gana estricto en ≥3, FABLE lo declara
ganador mecánico y elimina al resto con razón; **en cualquier otro caso escala a OPUS** con un
`tradeoff_summary` de una frase por miembro ("A gana si X, B gana si Y").

### Detección de herramientas complementarias
`match = provides[A] ∩ consumes[B]` no vacío **y** `role_overlap ≤ 0.3`
(`role_overlap = |provides A ∩ provides B| / |provides A ∪ provides B|`; >0.6 significa redundancia, no sinergia),
más compatibilidad de runtime, de transporte y de licencia, más `evidence_of_joint_use` si existe integración
documentada real. Máx 25 pares reportados. **OPUS compone los stacks sobre esta matriz.**

---

## 5. SISTEMA DE SCORING

Definición completa y anclas por eje: **`research/SCORING.md`**. Resumen:

- 10 ejes con los pesos exactos del documento (15/15/15/15/10/10/10/5/3/2).
- Cada eje se puntúa **0–5 con anclas objetivas**; `puntos = (ancla/5) × peso`.
- **Regla de sustento:** un ancla ≥4 exige ≥2 evidencias E2 o superiores; si no, baja automáticamente a 3.
- **Regla de confianza:** un eje sin evidencia suficiente se limita a 2 y se marca `low_confidence`.
- **Doble puntuación:** `score_global` (pesos fijos, comparable entre todo) y `score_track`
  (excluye el eje Computer Use y renormaliza ×100/85, para rankings dentro de categorías donde no aplica).
- **Capados de seguridad (regla absoluta):** V1 `curl|bash` único → 60 · V2 sin licencia → 50 + AVOID ·
  V3 ejecución arbitraria sin aprobación → 55 · V4 riesgo alto + abandonado → 45 + AVOID ·
  V5 exfiltración por defecto → 50 · V6 CVE sin parche → 40 + AVOID · V7 superficie de prompt injection
  sin defensa → 60 · V8 binarios opacos → 45. `score_final = min(ponderado, min(capados))`.
- **Índice de hype publicado aparte**, nunca mezclado en la puntuación, con las claims fallidas listadas.
- Etiquetas automáticas: `HYPE_FLAG`, `HIDDEN_GEM`, `PAPER_ONLY`, `ABANDONMENT_RISK`, `WINDOWS_BLOCKER`, `SECURITY_VETO`.

---

## 6. ESTRUCTURA DE ARTEFACTOS

Esquemas JSON en `research/schemas/`, estructura completa en `research/HANDOFF-SPEC.md`.

| Artefacto | Contenido | Consumidor |
|---|---|---|
| `ledger.jsonl` | Toda URL vista + veredicto + `kill_code` + tokens. Caché negativa y anti-duplicado | FABLE (entre bloques), OPUS (auditoría) |
| `queries.jsonl` | Consultas ejecutadas + hash del top-20 (deduplicación) | OPUS (auditar cobertura) |
| `ecosystem-map.json` | Taxonomía 8–12 categorías + fuentes meta + test de curación | OPUS (sección "mapa del ecosistema") |
| `triage.jsonl` / `shallow.jsonl` | Salidas de G2 / G3 | OPUS (auditar filtrado) |
| `cards/<slug>.json` | Ficha profunda ≤8 KB: la §23 del documento + permisos + Windows + interfaces + impacto + puntuación | OPUS (ranking y arquitectura) |
| `evidence/<slug>.jsonl` | Evidencias E0–E4 con URL, SHA, `path:line`, cita, fecha | OPUS (auditoría por muestreo) |
| `clusters.json` | Duplicados, dominancia mecánica, escalados y matriz de complementariedad | OPUS (elegir ganadores y componer stacks) |
| `models.json` | Tabla de modelos con coste, contexto, benchmark, VRAM/RAM, clase L0–L4 | OPUS (decisión local vs cloud) |
| `papers.jsonl` / `commercial.jsonl` | Papers sin código utilizable / SaaS cerrados (referencia de coste) | OPUS |
| `coverage.json` | Slots de arquetipo cubiertos vs vacíos por bloque | OPUS (detectar puntos ciegos) |
| `contradictions.md` | Contradicciones sin resolver, con ambas fuentes | OPUS (resolver) |
| `open-questions.md` | Lo no verificable y por qué | OPUS (declarar límites en el informe) |
| **`SUMMARY.jsonl`** | **Índice: 1 línea por finalista, ≤400 tokens. Es lo primero que lee OPUS** | OPUS |
| **`HANDOFF.md`** | Portada ≤2 páginas: embudo, cobertura, presupuesto, 10 hechos clave, vetos, hype, gems, clusters escalados, contradicciones, lo no investigado | OPUS |

**Regla de entrega:** OPUS lee `HANDOFF.md` + `SUMMARY.jsonl` (~15k tokens) y solo abre las fichas completas
de los proyectos que va a rankear o auditar. Sin este diseño, la FASE 3 empezaría gastando 250k tokens en leer.

---

## 7. INSTRUCCIONES OPERATIVAS PARA FASE 2

### 7.1 Arranque de FABLE (una sesión por bloque)
Contexto que se carga al inicio de **cada** sesión, y nada más:
1. `research/SCOPE-LOCK.md`
2. `research/PHASE2-FABLE-RUNBOOK.md`
3. `research/SCORING.md`
4. El esquema JSON del artefacto que va a escribir
5. `research/ledger.jsonl` **solo como lista de claves** (`key|verdict|block`)

Prohibido cargar: el documento original, fichas de bloques anteriores, evidencias de otros bloques.

### 7.2 Bucle por bloque
```
1. Leer slots de arquetipo del bloque (RUNBOOK §3.4)
2. G1: ejecutar hasta 12 consultas (6 vectores obligatorios + ≥3 vectores de hidden gems)
       → escribir cada URL nueva en ledger.jsonl (stage=discovered)
       → parada temprana: 4 consultas seguidas sin candidato nuevo vivo ⇒ bloque saturado
3. G2: por candidato, metadatos de API + últimos 30 commits
       → aplicar K1–K10 en orden, parar en la primera
       → escribir triage.jsonl y actualizar ledger
4. G3: por superviviente, README parcial + dependencias + CI + sondas grep + issues
       → 3–8 evidencias, extraer claims, calcular hype_index preliminar
       → aplicar K11–K15 → escribir shallow.jsonl
5. Comprobar matriz de cobertura: slot con <2 vivos ⇒ una consulta dirigida extra (máx 2 por slot)
6. Escribir a disco, cerrar sesión, reiniciar contexto
```

### 7.3 Sesión G4 (finalistas)
Un finalista por vez, en el orden fijo del RUNBOOK §6 (SHA → arquitectura → permisos → Windows →
madurez → cadena de suministro → benchmarks → evidencia externa → interfaces → impacto → puntuación →
contradicciones). Tope duro de 12k tokens; si se agota, se registra `truncated_at` y se entrega lo obtenido.
Nunca se inventa el resto.

### 7.4 SEC-PASS (transversal, tras G4)
Sobre **todos** los finalistas: verificar que `permissions` tiene evidencia E2 `path:line`, recalcular
`risk_tier`, aplicar V1–V8, rellenar `data_exfiltration_paths`, `how_to_isolate` / `how_to_revoke` /
`how_to_uninstall`. Ningún finalista llega al handoff sin este bloque completo.

### 7.5 G5 (clusters)
Formar clusters, rellenar la tabla de 9 ejes con evidencia discriminante, decidir solo los ganadores por
dominancia mecánica, escalar el resto, y calcular la matriz de complementariedad.

### 7.6 Cierre
Generar `coverage.json`, `contradictions.md`, `open-questions.md`, `SUMMARY.jsonl` y `HANDOFF.md`
según `HANDOFF-SPEC.md`. Verificar antes de entregar:
- [ ] Ningún campo factual sin `evidence_ids` ni `"UNVERIFIED"`
- [ ] Toda E2 con `commit_sha` + `path:line`
- [ ] Todo benchmark con fecha y `self_reported`
- [ ] Toda ancla ≥4 con ≥2 evidencias E2+
- [ ] Todo slot vacío justificado con las consultas ejecutadas
- [ ] Cero recomendaciones y cero arquitectura en los artefactos de FABLE

### 7.7 Reglas de conducta permanentes
No instalar. No ejecutar código de terceros. No ejecutar comandos de READMEs/issues/vídeos.
Clonado solo de finalistas, superficial, sin ejecución. No estimar. No resolver contradicciones.
No elegir ganadores fuera de la dominancia mecánica. No escribir prosa fuera de los campos con tope.

---

## 8. ESTRATEGIA DE CONTROL DE TOKENS Y COSTE

### 8.1 Reparto del presupuesto
| Etapa | % | Tope duro | Estimación |
|---|---|---|---|
| G0 semillas | 8% | 12 fuentes meta leídas | ~80k |
| G1 descubrimiento | 12% | 12 consultas/bloque | ~120k |
| G2 triage | 10% | 300 tok × ~450 | ~135k |
| G3 superficial | 25% | 2,5k × ~100 | ~250k |
| G4 profundo | 33% | 12k × ~32 | ~384k |
| G5 + entrega | 12% | — | ~120k |
| **Total FASE 2** | | | **≈1,0–1,3 M tokens** |

FASE 3 (OPUS) queda en ~150–250k tokens gracias a `SUMMARY.jsonl`: lee el índice, audita 15 evidencias
muestreadas y abre solo las fichas que rankea.

### 8.2 Las diez reglas que producen el ahorro
1. **`SCOPE-LOCK` sustituye al documento original** (~25k ahorrados por sesión × 11 bloques ≈ 275k).
2. **Una sesión por bloque, contexto reiniciado.** El corpus vive en disco, nunca en contexto.
3. **Caché negativa.** Un candidato muerto no se vuelve a mirar nunca: `ledger.jsonl` cuesta ~20 tokens por fila.
4. **API antes que HTML.** Nunca renderizar una página si existe un endpoint con los campos necesarios.
5. **Grep antes que lectura.** Nunca abrir un fichero para saber si contiene algo. Máx 12 ficheros por repo,
   nunca >300 líneas seguidas, siempre ±30 líneas alrededor del hallazgo.
6. **Deduplicación de consultas** por hash del top-20: evita re-descubrir el mismo cluster de repos.
7. **Topes de caracteres en todos los campos de texto.** Sin resúmenes narrativos: la prosa es el gasto invisible.
8. **Aforo fijo en G4.** 32 finalistas. Un candidato nuevo mejor **sustituye**, no amplía.
9. **Regla de aborto:** un bloque que supera el 130% de su presupuesto cierra el descubrimiento y termina
   con lo recogido, marcando `budget_exhausted` y los slots vacíos. Nunca se sacrifica G4 por descubrir más.
10. **Parada temprana por saturación:** 4 consultas seguidas sin candidato nuevo vivo ⇒ el bloque se cierra.

### 8.3 Reparto de coste entre modelos
- **FABLE** absorbe ~90% del volumen (descubrimiento, triage, evidencia, métricas, rúbrica).
- **OPUS** consume ~10% del volumen pero concentra el 100% de las decisiones: elección de ganadores,
  resolución de contradicciones, local vs cloud, mecanismo de percepción/acción, composición de stacks,
  arquitectura, plan de fases, matriz de riesgo y auditoría.
- Ese reparto es también el control de calidad: el modelo caro no re-investiga, **verifica por muestreo**
  y rechaza lotes (>1 fallo en 15 evidencias muestreadas ⇒ el bloque se repite).

### 8.4 Señal de alarma de gasto inútil
Si al terminar la FASE 2 se cumple alguna de estas, hubo derroche y debe corregirse antes de la FASE 3:
- Más del 20% de los candidatos triados llegaron a G3 (filtro demasiado permisivo).
- El coste medio por candidato muerto supera 500 tokens (se está leyendo demasiado antes de matar).
- Más del 30% de las fichas profundas tienen `score_global < 45` (mal criterio de promoción en G3).
- Los 10 primeros por `score_global` coinciden con los 10 más populares (sesgo de popularidad: falta
  una ronda de hidden gems).
