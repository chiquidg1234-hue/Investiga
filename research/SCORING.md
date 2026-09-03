# SISTEMA DE PUNTUACIÓN 0–100 (v1)

## 1. Principios
- Cada eje se puntúa **0–5 con anclas objetivas** (no impresiones), luego se pondera.
- `score_axis_points = (anchor / 5) * weight`
- Un eje sin evidencia suficiente se puntúa **como máximo 2** y se marca `low_confidence: true`.
- Se publican **dos puntuaciones**: `score_global` (pesos fijos del documento, comparable entre todo)
  y `score_track` (renormalizado dentro de su categoría, para rankings por categoría).
- Ninguna puntuación puede ocultar un problema de seguridad → ver §5 (capado duro).

## 2. Ejes y pesos (fijados por el documento)
| # | Eje | Peso |
|---|---|---|
| A1 | Capacidad funcional | 15 |
| A2 | Calidad técnica | 15 |
| A3 | Computer Use | 15 |
| A4 | Seguridad | 15 |
| A5 | Mantenimiento | 10 |
| A6 | Compatibilidad / integración (incluye Windows 11) | 10 |
| A7 | Evidencia / benchmarks | 10 |
| A8 | Documentación | 5 |
| A9 | Comunidad / adopción | 3 |
| A10 | Coste / eficiencia | 2 |

## 3. Anclas por eje

### A1 — Capacidad funcional (15)
- 0: solo demo/README; no hay implementación del núcleo.
- 2: resuelve un caso estrecho; falta la mitad de lo que promete.
- 3: hace lo que promete en su dominio, con límites documentados.
- 4: cubre el dominio completo + casos borde + manejo de errores.
- 5: cubre el dominio y además ofrece extensibilidad probada por terceros (plugins/integraciones reales).

### A2 — Calidad técnica (15)
Señales medibles: tests presentes y ejecutados en CI, tipado, separación de capas, gestión de errores,
tamaño y acoplamiento del núcleo, ausencia de "God file", `TODO/FIXME` densidad, dependencias fijadas.
- 0: sin tests, sin CI, un solo fichero monolítico, dependencias sin fijar.
- 2: tests testimoniales (<10% cobertura aparente) o CI que solo hace lint.
- 3: CI con tests reales, estructura modular clara.
- 4: 3 + tests de integración + tipado + release process reproducible.
- 5: 4 + tests del comportamiento crítico (grounding/ejecución/permisos) + lockfile + versionado semántico respetado.

### A3 — Computer Use (15)
Para proyectos de B2/B3 se mide capacidad directa. Para el resto se mide **contribución al stack de computer use**.
- 0: ninguna relación con controlar/observar un ordenador.
- 1: contribución indirecta (p. ej. logging genérico).
- 2: habilitador claro (memoria/orquestación que un agente CU necesitaría).
- 3: percibe **o** actúa (solo una mitad del bucle), o actúa sin verificación.
- 4: bucle completo percibir→razonar→actuar con verificación del resultado, demostrado.
- 5: 4 + medido en benchmark público de GUI/CU con número y fecha, + funciona en escritorio Windows.

### A4 — Seguridad (15)
Ver §4 (superficie de capacidad) y §5 (vetos). Anclas:
- 0: ejecución arbitraria sin ningún control + instalación por `curl|bash` + sin licencia.
- 1: privilegios altos, cero mecanismos de contención, telemetría no documentada.
- 2: privilegios altos con un único mecanismo débil (p. ej. confirmación en consola).
- 3: modelo de permisos explícito (allowlist/denylist) documentado y aplicado en el código.
- 4: 3 + aislamiento real (proceso/contenedor/VM) + gestión de secretos separada + defensa documentada frente a prompt injection.
- 5: 4 + auditoría externa, política de vulnerabilidades, releases firmados, dependencias fijadas y escaneadas.

### A5 — Mantenimiento (10)
Métricas duras (ver detección en RUNBOOK §Actividad):
- 0: archivado, o >24 meses sin commits.
- 1: >12 meses sin commits sustantivos, issues sin respuesta.
- 2: actividad esporádica, un único mantenedor, backlog creciente sin triage.
- 3: commits sustantivos en los últimos 90 días, issues triadas, releases en los últimos 12 meses.
- 4: 3 + ≥3 contribuidores humanos activos en 90 días + releases regulares.
- 5: 4 + bus factor ≥3 (nadie supera el 60% de commits) + respuesta mediana a issues <7 días + roadmap público.

### A6 — Compatibilidad / integración (10)
Combina la escalera Windows y la facilidad de integración.
- 0: W6 (no recomendable en Windows).
- 1: W5/W4 sin ruta nativa; o requiere reescribir el núcleo para integrarlo.
- 2: W3 (WSL) funcional pero sin control del escritorio host.
- 3: W2 nativo con PowerShell, API/librería importable, sin lock-in de framework.
- 4: W1 nativo + interfaz limpia (librería, CLI o servidor MCP) + sin exigir adoptar todo su framework.
- 5: 4 + probado en CI sobre `windows-latest` + soporta múltiples monitores/DPI + integración documentada con otros componentes del stack.

### A7 — Evidencia / benchmarks (10)
Clase de evidencia máxima alcanzada (ver RUNBOOK §Evidencia E0–E4):
- 0: solo afirmaciones de README (E0).
- 1: documentación que describe el mecanismo (E1).
- 2: código verificado que implementa la afirmación principal (E2).
- 3: E2 + verificación independiente (issue de tercero, paper, review externa) (E3).
- 4: E3 + resultado de benchmark público con número, harness y fecha (E4).
- 5: E4 + resultados reproducibles/replicados por terceros, o posición en leaderboard mantenido.

### A8 — Documentación (5)
- 0: solo README corto. 2: README completo + ejemplos. 3: sitio de docs con guía de instalación por SO.
- 4: 3 + referencia de API + guía de seguridad/permisos. 5: 4 + troubleshooting Windows + arquitectura explicada.

### A9 — Comunidad / adopción (3)
**Nunca por stars solas.** Señales: dependientes reales, forks con divergencia, discusiones técnicas activas,
integraciones de terceros, paquetes publicados con descargas.
- 0: sin señal externa. 2: usado por ≥3 proyectos independientes. 3: ecosistema de terceros con integraciones mantenidas.
- 5: estándar de facto en su nicho con múltiples implementaciones independientes.

### A10 — Coste / eficiencia (2)
- 0: obliga a modelos caros por acción y no permite alternativas. 3: modelo-agnóstico, permite modelos baratos/locales.
- 5: 3 + optimizaciones medidas (caching, compresión de contexto, batching) con números publicados.

## 4. Superficie de capacidad (obligatoria antes de puntuar A4)
Marcar cada permiso que el proyecto necesita, con evidencia E2 (fichero:línea):
`exec_shell, exec_code, fs_read, fs_write, fs_delete, net_out, net_listen, screen_capture,
input_injection, clipboard, credentials, env_vars, browser_profile, elevated_admin, autostart, telemetry`

`risk_tier` se deriva mecánicamente:
- R0: ninguno de los anteriores salvo `net_out`.
- R1: `fs_read` + `net_out`.
- R2: `screen_capture` **o** `input_injection` **o** `fs_write`.
- R3: `exec_shell`/`exec_code` **o** `credentials` **o** `browser_profile`.
- R4: `elevated_admin` **o** (`exec_shell` + `net_out` sin ningún control de aprobación).

## 5. Vetos y capados duros (regla absoluta del documento)
Si se cumple cualquier condición, se aplica el capado y se marca `veto_reason`:

| Condición (verificada con evidencia) | Efecto |
|---|---|
| V1 — Única vía de instalación documentada es `curl \| bash` / script remoto sin verificación | cap 60 |
| V2 — Sin licencia, o licencia que impide uso personal | cap 50 + `AVOID` |
| V3 — Ejecución arbitraria (`exec_shell`) sin ningún punto de aprobación ni aislamiento | cap 55 |
| V4 — R3/R4 **y** sin commits sustantivos en 12 meses | cap 45 + `AVOID` |
| V5 — Envía screenshots/ficheros/telemetría fuera del equipo por defecto y sin opt-in documentado | cap 50 |
| V6 — CVE/advisory abierto sin parche, o dependencia con advisory crítico sin fijar | cap 40 + `AVOID` |
| V7 — Ejecuta contenido no confiable (web/pantalla) como instrucciones sin ninguna defensa | cap 60 + flag `prompt_injection_surface` |
| V8 — Mantenedor desconocido + binarios precompilados sin build reproducible | cap 45 |

`score_final = min(score_ponderado, min(caps_aplicados))`.
**Un veto siempre aparece en el informe, aunque el proyecto sea excelente técnicamente.**

## 6. Índice de hype (se publica aparte, no se mezcla)
- `claims_total` = afirmaciones de capacidad extraídas del README/landing (máx. 10, las más relevantes).
- `claims_verified` = las que alcanzan evidencia **E2 o superior**.
- `hype_index = 1 - claims_verified / claims_total` (0 = todo verificado, 1 = todo humo).

Etiquetas automáticas:
- `HYPE_FLAG` si `hype_index >= 0.5` **y** `stars >= 5000`.
- `HIDDEN_GEM` si `hype_index <= 0.25` **y** `stars <= 1500` **y** A5 ≥ 3.
- `PAPER_ONLY` si existe paper pero el código no implementa la afirmación principal (E1 sin E2).

## 7. Normalización por track
- `score_global`: pesos de §2 sin cambios (usa A3 como "contribución al computer use").
- `score_track`: para bloques que no son B2/B3, se **excluye A3** y se renormaliza sobre 85 → ×(100/85).
  Se usa **solo** para el ranking interno de la categoría. Ambos números se reportan siempre.

## 8. Reproducibilidad
Toda ancla asignada debe llevar `evidence_ids[]` que la justifiquen. Un eje con ancla ≥4 y menos de
2 evidencias E2+ es inválido: se baja a 3 automáticamente. OPUS audita esta regla en FASE 3.
