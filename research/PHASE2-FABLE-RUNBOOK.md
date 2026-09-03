# FASE 2 — RUNBOOK OPERATIVO PARA FABLE

Entradas que FABLE lee: `research/SCOPE-LOCK.md`, este runbook, `research/SCORING.md`,
`research/schemas/*.json`, y `research/ledger.jsonl` (solo el índice de claves).
**No leer `AI-AGENT-RESEARCH.md`.** **No leer fichas de bloques anteriores.**

---

## 0. Regla de oro del gasto
> Ningún candidato consume tokens de nivel N+1 hasta que sobrevive al nivel N.
> El coste de matar un candidato malo debe ser ~0.

---

## 1. El embudo (5 puertas)

| Puerta | Nombre | Entrada esperada | Salida esperada | Coste/candidato | Artefacto |
|---|---|---|---|---|---|
| G0 | Semillas y mapa | — | 25–40 fuentes meta | ~1k c/u | `ecosystem-map.json` |
| G1 | Descubrimiento | — | 350–500 URLs únicas | ~30 tok | `ledger.jsonl` |
| G2 | Triage por metadatos | 350–500 | 80–110 vivos | ≤300 tok | `triage.jsonl` |
| G3 | Evidencia superficial | 80–110 | 28–36 finalistas | ≤2.5k tok | `shallow.jsonl` |
| G4 | Evidencia profunda | 28–36 | 28–36 fichas | ≤12k tok | `cards/*.json` |
| G5 | Clusters y complementariedad | fichas | 8–14 clusters | ~15k total | `clusters.json` |

**Sin excepciones al aforo de G4.** Si aparece un candidato mejor que un finalista ya procesado,
se sustituye (se marca el desplazado `PARKED`), no se amplía el cupo.

---

## 2. G0 — Semillas y mapa del ecosistema (bloque B1, se ejecuta PRIMERO)

Objetivo: obtener las fuentes que **generan** candidatos, no candidatos sueltos.

Tipos de fuente a localizar (mínimo 2 de cada, máximo 5):
1. Listas curadas (`awesome-*`) de: computer-use / GUI agents / AI agents / MCP / agent memory / agent security.
2. Registros y directorios de servidores MCP.
3. Leaderboards y suites de benchmark de agentes GUI/OS/web.
4. Colecciones paper→código (índices de arXiv por categoría, agregadores de implementaciones).
5. Organizaciones de laboratorio/empresa que publican agentes (buscar por `org:` una vez identificadas).
6. Hubs de modelos: colecciones/leaderboards de VLM y de modelos de *GUI grounding*.

Para cada fuente meta registrar en `ecosystem-map.json`:
`{url, tipo, items_estimados, curada|volcado, ultima_actualizacion, criterio_de_inclusion_declarado, solapamiento_con[]}`

**Test de curación (obligatorio):** una lista es *curada* si (a) tiene criterio de inclusión escrito,
(b) ha eliminado entradas alguna vez (verificar en el historial de commits), (c) fue actualizada en <180 días.
Si no cumple ≥2 de 3 → `volcado`, y se usa solo como fuente de URLs, nunca como señal de calidad.

**Mapa del ecosistema:** producir una taxonomía de 8–12 categorías con las fronteras entre ellas
descritas en una frase cada una. Es descriptivo, no valorativo.

---

## 3. G1 — Descubrimiento (multi-señal, por bloque)

### 3.1 Presupuesto de consultas
Máximo **12 consultas de búsqueda por bloque**. Antes de ejecutar una consulta nueva, comprobar
`queries.jsonl`: si el top-20 esperado solapa >80% con una consulta ya ejecutada, **no se ejecuta**.

### 3.2 Vectores obligatorios por bloque (usar los 6)
1. **Topics + rango de estrellas alto** — descubre lo obvio (necesario para el análisis de hype).
   `topic:<t> stars:>1000 pushed:>{hoy-180d}`
2. **Rango de estrellas BAJO + reciente** — cantera de hidden gems.
   `topic:<t> stars:10..400 pushed:>{hoy-90d}`
3. **Búsqueda en código, no en descripción** — encuentra implementaciones reales, filtra marketing.
   Ej. B2/B3: ficheros que importan APIs de UI Automation, captura de pantalla o inyección de input.
4. **Grafo de dependientes** — de cada meta-proyecto y de cada finalista: quién lo usa y qué usa él.
5. **Grafo de personas** — autores de los 3 mejores repos del bloque → sus otros repositorios y sus orgs.
6. **Fuentes externas** (ver §7): papers, leaderboards, foros técnicos, registros de paquetes.

### 3.3 Vectores adicionales para hidden gems (aplicar al menos 3 por bloque)
- **Intersección de listas:** proyectos presentes en ≥2 listas curadas independientes pero con <1.000 estrellas.
- **Forks divergentes:** forks con commits más recientes que el padre y ≥20 commits propios (proyecto resucitado).
- **Minería de issues/discussions** de los repos líderes: menciones a alternativas, "we switched to X", "X does this better".
- **Papers recientes con enlace a código** en visión-GUI / agentes de SO, publicados en los últimos 12 meses.
- **Fuentes no anglófonas:** laboratorios y comunidades técnicas que publican en chino/japonés/coreano
  (el área de GUI agents tiene producción muy fuerte fuera del inglés). Buscar por nombres de org y por términos traducidos.
- **Paquetes con descargas altas y pocas estrellas** en PyPI/npm (herramienta usada, no promocionada).
- **Repos citados en la documentación oficial** de proveedores de modelos y de MCP.

### 3.4 Matriz de cobertura (anti punto ciego)
Cada bloque define *slots de arquetipo*. Un bloque **no se cierra** hasta tener ≥2 candidatos vivos por slot
o una nota explícita `slot_empty` con las consultas ejecutadas.

- **B2**: (a) modelo/pesos de GUI grounding, (b) harness CU end-to-end, (c) agente CU sobre proveedor cloud,
  (d) comprensión de pantalla/parser de UI, (e) OCR/detector ligero, (f) copiloto visual supervisor (no actúa, guía).
- **B3**: (a) driver Windows UIA/Win32, (b) inyección de mouse/teclado, (c) captura de pantalla multi-monitor/DPI,
  (d) automatización de navegador por DOM/CDP, (e) automatización de aplicaciones de escritorio, (f) scripting PowerShell/AHK.
- **B4**: (a) orquestador de grafo/estado, (b) framework multi-agente por roles, (c) runtime de agente minimalista,
  (d) sistema de handoff/delegación, (e) planificación/descomposición de tareas, (f) checkpoints y reintentos.
- **B5**: (a) deep research end-to-end, (b) agente de navegación web, (c) capa de búsqueda/recuperación,
  (d) verificación y citación de fuentes.
- **B6**: (a) memoria vectorial, (b) grafo de conocimiento, (c) memoria temporal/episódica,
  (d) memoria procedural / workflows aprendidos, (e) compresión y gestión de contexto.
- **B7**: (a) servidores MCP oficiales, (b) MCP de escritorio/entrada, (c) MCP de navegador, (d) MCP de filesystem/terminal,
  (e) gateway/proxy MCP con permisos, (f) cliente/host MCP.
- **B8**: (a) optimizador de prompts con evaluación, (b) gestión de contexto/CLAUDE.md, (c) sistemas de Skills,
  (d) hooks y automatización del entorno, (e) enrutado de modelo/agente, (f) medición de tokens y regresión de calidad.
- **B9**: (a) sandbox/aislamiento de procesos, (b) sistema de permisos y aprobación, (c) defensa frente a prompt injection,
  (d) seguridad de MCP / tool poisoning, (e) gestión de secretos, (f) auditoría de cadena de suministro.
- **B10**: (a) trazado de agentes, (b) contabilidad de coste/tokens, (c) captura de trayectorias y replay,
  (d) suites de evaluación de agentes GUI/web, (e) detección de regresiones.
- **B11**: no son repos: es una tabla de modelos (ver §8).

---

## 4. G2 — Triage por metadatos (≤300 tokens por candidato)

Solo se consulta **metadata de API** (nada de READMEs completos, nada de HTML):
`stars, forks, archived, license, pushed_at, created_at, language, description, topics, open_issues`
más **una** llamada a la lista de commits (últimos 30, campos mínimos).

### Reglas de muerte (aplicar en orden, parar en la primera)
| Código | Condición | Nota |
|---|---|---|
| K8 | La clave ya está en `ledger.jsonl` | coste 0, solo añadir tag |
| K1 | Archivado / read-only | — |
| K2 | Sin commits sustantivos en 24 meses (12 meses si block ∈ {B2,B3,B7,B8}) | "sustantivo" = toca código, no solo docs/CI |
| K3 | Sin fichero de licencia | se registra como riesgo legal, no como candidato |
| K4 | Repo de tutorial/curso/demo/plantilla, o <300 líneas de código propio | — |
| K5 | Wrapper fino de otro candidato sin mecanismo propio | anotar `duplicate_of` |
| K6 | No encaja en ningún slot de arquetipo de ningún bloque | — |
| K7 | Exclusivo de macOS/Linux por diseño **y** el bloque es B2/B3 | W6 |
| K9 | Paper sin código, o código que no implementa lo del paper | va a `papers.jsonl`, no a candidatos |
| K10 | SaaS cerrado sin self-host | va a `commercial.jsonl` (salvo proveedores de modelos, que van a B11) |

**Prohibido matar por pocas estrellas.** Prohibido promover solo por muchas.

### Promoción a G3
`provisional_interest = HIGH` si ocupa un slot con <2 candidatos, o si combina
(actividad sana) + (arquetipo escaso) + (señal de uso externo). Máx 110 promovidos en total.

---

## 5. G3 — Evidencia superficial (≤2.500 tokens por candidato)

Lectura permitida, en este orden y parando en cuanto se pueda decidir:
1. README: **primeras 150 líneas** + secciones de instalación y de limitaciones (por búsqueda de encabezado).
2. Árbol de ficheros de primer nivel + `pyproject.toml`/`package.json`/`Cargo.toml` (dependencias).
3. Fichero de CI (¿hay job `windows-latest`? ¿corre tests o solo lint?).
4. **Sondas por grep**, no lecturas completas. Cada sonda es una búsqueda de código dentro del repo:
   - Windows: importaciones de UI Automation / Win32 / pywin32 / comtypes / captura de pantalla / DPI awareness.
   - Seguridad: ejecución de shell, evaluación dinámica de código, escritura en filesystem, lectura de variables de entorno/credenciales, llamadas de red salientes.
   - Capacidad: presencia real de la función que el README promete (nombre de la función/clase declarada).
   - Tests: existencia y número de ficheros de test que tocan el núcleo.
5. Búsqueda de issues: `is:issue windows` (abiertas vs cerradas) y `is:issue label:bug` recientes.

### Salida obligatoria
Rellenar `candidate.schema.json` en modo `shallow` + crear **entre 3 y 8 evidencias** por candidato.
Extraer las **claims** (máx 10) del README y asignar a cada una su clase de evidencia máxima alcanzada.

### Reglas de muerte en G3
- K11: el README promete la capacidad central y las sondas de código **no** la encuentran (E0 puro sobre la claim principal).
- K12: `risk_tier` R4 sin ningún mecanismo de aprobación **y** existe un candidato del mismo arquetipo con R≤3.
- K13: complejidad de integración `fork_required`/`incompatible` **y** existe alternativa `drop_in` del mismo arquetipo.
- K14: W6 confirmado y el bloque es B2/B3.
- K15: dominado mecánicamente por otro miembro del mismo cluster en **todos** los ejes.

---

## 6. G4 — Evidencia profunda (≤12.000 tokens por finalista)

Solo finalistas. Clonado `--depth 1 --filter=blob:none` permitido; **ejecutar, nunca**.

Secuencia fija (parar si el presupuesto se agota; registrar `truncated_at`):
1. **Anclar SHA**: registrar `commit_sha_reviewed`. Toda evidencia E2 lleva ese SHA.
2. **Arquitectura**: mapear el bucle principal (percepción → decisión → acción → verificación).
   Localizar los 3–5 ficheros del núcleo. Anotar `perception_mechanism`, `actuation_mechanism`, `verification_mechanism`.
3. **Auditoría de permisos**: enumerar la superficie de capacidad de SCORING.md §4 con `path:line` por cada permiso.
   Derivar `risk_tier`. Rellenar `data_exfiltration_paths` (qué sale del PC y hacia dónde).
4. **Windows**: rellenar el bloque completo `windows{}` con evidencia. Asignar nivel W1–W6.
   Si el nivel no puede probarse → `UNVERIFIED`, nunca una suposición.
5. **Madurez**: métricas duras (§9).
6. **Cadena de suministro**: número de dependencias directas, lockfile, scripts de post-instalación,
   método de instalación documentado, releases firmados, advisories conocidos.
7. **Benchmarks**: solo con `name + metric + value + date + self_reported`. Sin fecha → no se registra.
8. **Evidencia externa** (§7): mínimo **1 fuente independiente** (E3) por finalista, o `open_question`.
9. **Interfaces**: `provides[]` / `consumes[]` / runtime / transporte / licencia / esfuerzo de integración.
10. **Impacto**: los 16 ejes, -2..+3.
11. **Puntuación**: aplicar SCORING.md. Cada ancla ≥4 exige ≥2 evidencias E2+.
12. **Contradicciones**: si dos fuentes se contradicen, registrar ambas en `contradictions[]` y **no resolver**.

### Prohibiciones en G4
- No leer ficheros >300 líneas completos: usar búsqueda dirigida y leer ±30 líneas alrededor del hallazgo.
- No leer `node_modules`, `vendor`, `dist`, `docs/` completo, ni ficheros de test salvo para contarlos.
- No leer más de 12 ficheros por repositorio.
- No redactar recomendaciones. `verdict_factual` es descriptivo: "hace X (E2), no hace Y, medido en Z".

---

## 7. Investigación fuera de GitHub (cuándo y cómo)

**Disparadores** (solo entonces se gasta en fuentes externas):
- T1: el proyecto afirma una capacidad de computer-use y no hay benchmark en el repo → buscar leaderboard/paper.
- T2: hay señal de hype (muchas estrellas, pocas evidencias) → buscar críticas técnicas independientes.
- T3: dos candidatos del mismo cluster empatan → buscar comparativas o migraciones documentadas.
- T4: hay duda de compatibilidad Windows → buscar issues, foros y notas de release.
- T5: hay duda de seguridad → buscar advisories y bases de vulnerabilidades.
- T6: se necesita dato de coste/latencia de un modelo → documentación oficial del proveedor.

**Jerarquía de fuentes (usar en este orden, parar al confirmar):**
1. Documentación oficial del proyecto o del proveedor del modelo.
2. Paper (con su sección de limitaciones — es donde está la verdad) y su leaderboard.
3. Bases de vulnerabilidades y advisories; puntuaciones de salud de proyecto open source.
4. Registros de paquetes (descargas reales) y grafos de dependencias.
5. Discusión técnica de desarrolladores (foros de agregación de noticias técnicas, subreddits técnicos,
   hilos largos con detalle reproducible). **Solo se cita si aporta un hecho verificable**, no una opinión.
6. Vídeo/redes: **nunca** como evidencia. Solo como pista para volver al código.

**Regla de citación:** toda fuente externa se guarda como evidencia con `source_url + fetched_at + quote` (≤400 chars).
Una opinión sin hecho comprobable no es evidencia: va a `contradictions[]` o se descarta.

**Presupuesto:** máx. 3 fuentes externas por finalista, máx. 2 por disparador.

---

## 8. B11 — Modelos (no son repositorios)

Producir `models.json`, una fila por modelo, con columnas fijas:
`nombre, proveedor, abierto|cerrado, modalidad, contexto, tool_calling, computer_use_nativo,
benchmark_relevante(+valor+fecha), coste_entrada, coste_salida, latencia_tipica,
VRAM_min_cuantizado, RAM_min_CPU, requiere_CUDA, licencia, fuente`

Categorías a cubrir: razonamiento, computer use / GUI grounding, visión general, coding, research, OCR, embeddings.
Mínimo 3 candidatos por categoría, con al menos 1 abierto y 1 cerrado.

**Clasificación de viabilidad local (mecánica, sin opinión):**
- `L0` corre en CPU con <4 GB RAM; `L1` CPU 4–10 GB RAM; `L2` GPU ≤2 GB VRAM (cuantizado);
- `L3` GPU 4–8 GB VRAM; `L4` >8 GB VRAM → **cloud-only en este hardware**.
FABLE asigna L0–L4 a partir de los requisitos publicados. La decisión local/cloud es de OPUS.

---

## 9. Verificación de actividad real (definiciones exactas)

- **Commit sustantivo**: toca ≥1 fichero de código fuera de `docs/`, `README`, `.github/`, ficheros de licencia.
- `days_since_substantive_commit`: días desde el último commit sustantivo en la rama por defecto.
- `human_committers_90d`: autores distintos en 90 días excluyendo cuentas con sufijo de bot.
- `docs_only_commit_ratio_90d`: proporción de commits no sustantivos → **>0.7 = "teatro de actividad"**, marcar flag.
- `bus_factor_top_share`: proporción de commits del autor principal en 12 meses. **>0.9 = riesgo de abandono**.
- `median_issue_first_response_days`: sobre las últimas 20 issues cerradas.
- `open_issue_growth_90d`: (abiertas hoy − abiertas hace 90 días) / abiertas hace 90 días.
- `releases_365d`: releases publicadas en 12 meses.

---

## 10. Detección de hype (procedimiento, no intuición)

1. Extraer del README/landing las **claims** de capacidad (máx 10, las que justifican usarlo).
2. Para cada claim, buscar la evidencia de mayor clase alcanzable con **≤2 sondas de código**.
3. Calcular `hype_index` (SCORING.md §6).
4. Contrastar popularidad con evidencia: registrar `stars`, `hype_index`, `A7`, `A2`.
5. Marcar `HYPE_FLAG` según la regla automática. **La etiqueta va acompañada siempre de las claims fallidas concretas.**
6. Registrar también el caso inverso (`HIDDEN_GEM`): baja popularidad, alta verificación.

Nunca escribir "es hype" sin listar qué claim concreta no tiene evidencia.

---

## 11. Clusters, duplicados y complementariedad (G5)

### 11.1 Formación de clusters
Dos proyectos van al mismo cluster si comparten `archetype` **y** ≥60% de `provides[]`.
Un cluster tiene entre 2 y 6 miembros.

### 11.2 Comparación cabeza a cabeza
Rellenar `cluster.schema.json` con los 9 ejes. Cada celda necesita **una evidencia discriminante**
(no vale repetir la puntuación global). Si un eje no puede discriminarse, escribir `TIE`.

- **Dominancia mecánica**: un miembro gana o empata en los 9 ejes y gana estrictamente en ≥3 → `mechanical_winner`,
  el resto se elimina con razón. FABLE puede decidir esto solo.
- **Cualquier otro caso** → `escalate_to_opus: true` + `tradeoff_summary` de una frase por miembro
  ("A gana si X; B gana si Y"). FABLE **no elige**.

### 11.3 Complementariedad (herramientas que funcionan mejor juntas)
Para cada par candidato dentro de un bloque o entre bloques adyacentes, calcular mecánicamente:
- `match` = `provides[A] ∩ consumes[B]` (no vacío ⇒ encajan).
- `role_overlap` = |provides[A] ∩ provides[B]| / |provides[A] ∪ provides[B]|. **>0.6 ⇒ redundantes, no complementarios.**
- `runtime_compatible`, `license_compatible`.
- `evidence_of_joint_use`: ¿existe integración documentada real (adaptador, ejemplo, dependencia)? Si no → `UNVERIFIED`.
Solo se reportan los pares con `match` no vacío **y** `role_overlap ≤ 0.3`. Máx. 25 pares.
**OPUS compone los stacks; FABLE solo entrega la matriz.**

---

## 12. Presupuesto de tokens y control de coste

| Etapa | % del presupuesto | Tope duro |
|---|---|---|
| G0 semillas | 8% | 12 fuentes meta leídas |
| G1 descubrimiento | 12% | 12 consultas/bloque |
| G2 triage | 10% | 300 tok/candidato |
| G3 superficial | 25% | 2.5k tok/candidato |
| G4 profundo | 33% | 12k tok/finalista |
| G5 clusters + entrega | 12% | — |

Presupuesto total orientativo de FASE 2: **≈1,0–1,3 M tokens**.
(≈500 triados × 0,3k + ≈100 superficiales × 2,5k + ≈32 profundos × 12k + descubrimiento y síntesis).

### Reglas de higiene de contexto (obligatorias)
1. **Una sesión por bloque.** Al terminar un bloque se escribe a disco y se reinicia el contexto.
2. **Nunca mantener el corpus en contexto.** Se escribe línea a línea en JSONL tras cada candidato.
3. El único estado compartido entre sesiones es `ledger.jsonl` cargado **solo como lista de claves**
   (`key|verdict|block`, ≤20 tokens por fila).
4. **API antes que HTML.** Nunca renderizar una página cuando existe un endpoint con los campos necesarios.
5. **Grep antes que lectura.** Nunca leer un fichero para averiguar si contiene algo.
6. **Sin prosa.** Todos los campos de texto tienen tope de caracteres del esquema. Nada de resúmenes narrativos.
7. **Caché negativa.** Un candidato muerto no se vuelve a mirar jamás; `kill_code` explica por qué en ≤160 chars.
8. **Deduplicación de consultas** en `queries.jsonl` con el hash del top-20.
9. **Regla de aborto:** si un bloque supera el 130% de su presupuesto, se cierra el descubrimiento,
   se termina con lo recogido y se registra `budget_exhausted: true` + los slots vacíos. No se sacrifica G4.
10. **Regla de parada temprana:** si tras 4 consultas de un bloque no aparece ningún candidato nuevo vivo,
    el bloque se da por saturado.

---

## 13. Reglas anti-invención (críticas para la auditoría de FASE 3)
1. Todo campo factual lleva `evidence_ids` o el literal `"UNVERIFIED"`. **Prohibido estimar.**
2. Toda evidencia E2 lleva `commit_sha` + `path:line`. Sin SHA no es E2, es E1.
3. Toda cita literal ≤400 caracteres y textual.
4. Toda métrica de benchmark lleva fecha y `self_reported: true|false`.
5. Si dos fuentes se contradicen, **se registran las dos**. Resolver contradicciones es trabajo de OPUS.
6. `tokens_spent` se registra por candidato: permite a OPUS detectar fichas "demasiado baratas para ser reales".
