# FASE 3 — AUDITORÍA, DECISIÓN TÉCNICA Y PLAN DE IMPLEMENTACIÓN

Auditor: OPUS. Entradas: `AI-AGENT-RESEARCH.md`, FASE 1 (`PHASE1-STRATEGY.md`), FASE 2 (41 fichas + evidencia).
Esta fase **no instala nada**. Termina en una decisión y un plan.

---

## 0. VEREDICTO EN UNA PÁGINA

**Sí se puede construir hoy un agente personal útil para tu PC. No se puede construir el agente autónomo del documento.**

Lo que es viable ahora, con evidencia:
- Un agente que **ve tu pantalla, entiende qué app usas, actúa sobre ella y verifica el resultado**, en Windows 11 nativo, usando el árbol de accesibilidad (UIA) como canal principal y visión como respaldo.
- Un agente que **investiga en internet, trabaja con tu código, recuerda procedimientos y pide permiso antes de actuar**.
- Todo ello **sin instalar un framework de agentes nuevo**: Claude Code ya es el harness.

Lo que **no** es viable hoy y no debes intentar (§3):
- Autonomía larga sin supervisión. OSWorld 2.0 (tareas de ~1,6 h) sigue en **31,4 % de completitud binaria** con el mejor sistema del mundo y ~2–4 k USD por ejecución.
- Grounding visual local en tu GPU. Los modelos que caben en 2 GB rinden **28–36 %** en ScreenSpot-Pro frente al 87,9 % de Claude Opus 4.8 en cloud.
- Aislar de verdad al agente del escritorio. **Ningún sandbox encontrado lo consigue**; es un límite estructural de Windows, no una carencia de herramientas.

**La decisión central:** el agente es **Claude Code + tres MCP locales + una capa de permisos por hooks**. Cinco componentes en el núcleo, no quince. Todo lo demás que FABLE encontró es o redundante, o inmaduro, o resuelve un problema que tú no tienes.

---

## 1. AUDITORÍA DE FABLE

### 1.1 Lo que resiste la auditoría
| Comprobación | Resultado |
|---|---|
| Recálculo de los 41 `score_global` desde las anclas A1–A10 y los capados V* | **0 inconsistencias** |
| Regla "ancla ≥4 exige ≥2 evidencias E2+" | **0 violaciones** |
| Sesgo de popularidad (top-10 por score vs top-10 por stars) | **2/10 de solapamiento** — no hay sesgo |
| Vetos de seguridad aplicados | 6 proyectos capados, todos con evidencia E3 externa |
| Trazabilidad | 557 evidencias con SHA y ruta; artefactos regenerables sin red |

FABLE hizo un trabajo honesto: marcó `UNVERIFIED` donde no pudo verificar, registró contradicciones sin resolverlas y no infló nada a su favor.

### 1.2 Fallos encontrados (y corregidos aquí)

**F1 — La evidencia E2 es mecánica, no leída.** Las 501 evidencias "E2" son *grep* + métricas de git, no lectura de código. FABLE nunca confirmó leyendo que un componente hace lo que promete. Lo he hecho yo para los candidatos del núcleo, y ha aparecido F2.

**F2 — La ficha de Windows-MCP subestima gravemente su superficie.** FABLE describió "estado de UI por UIA, captura, clic/tecleo, PowerShell, apps" y le asignó los permisos `exec_shell, fs_read, fs_write, screen_capture, input_injection, clipboard`. La lectura del código (`src/windows_mcp/tools/`, 21 tools) muestra además:
- **`registry_tool` con modos `set` y `delete` sobre HKCU y HKLM** — modificación del sistema, no listada en la ficha.
- **`PowerShell`** cuya propia descripción dice *"full access to the underlying operating system capabilities"*, con `destructiveHint=True` y **sin allowlist**.
- `filesystem`, `notification`, `process`, `scrape`, `vdm` (escritorios virtuales).

**F3 — Telemetría no detectada en Windows-MCP.** `infrastructure/analytics.py` trae una **clave PostHog embebida** (`phc_uxdCItyVTjXNU0sMPr97dq3tcz39scQNt3qjTYw5vLV`, host `us.i.posthog.com`) y el README confirma `ANONYMIZED_TELEMETRY=true` **por defecto**. FABLE contó 7 hits de la sonda y no lo interpretó. Es opt-out y el README afirma que no recoge argumentos ni salidas, pero **debe desactivarse explícitamente**.
→ *Corrección de ficha:* permisos += `system_modify`, `telemetry`; A4 se mantiene en 2 (ya era bajo) pero la ficha pasa a exigir configuración defensiva obligatoria.

**F4 — Confusión entre "puntuación alta" y "encaje en el stack".** FABLE coronó **LangGraph (78,6)** como número 1 global. Es correcto según la rúbrica y **equivocado como decisión**: su valor marginal dado que ya usas Claude Code es negativo (§2.1). Es el fallo previsible de puntuar componentes en aislamiento; la rúbrica lo pedía así, y por eso el reparto de FASE 1 reservaba esta decisión para OPUS.

**F5 — `tokens_spent: 9000` es un valor inventado.** Idéntico en las 41 fichas. No es medición, es relleno. Viola la regla anti-invención del propio runbook. Sin impacto en las conclusiones, pero es una mentira en el artefacto y queda anotado.

**F6 — Nueve `HYPE_FLAG` mal calibrados.** La regla mecánica marca como hype cualquier benchmark auto-reportado sin verificación de terceros. Eso mete en el mismo saco a `sandbox-runtime` de Anthropic y a `claude-flow`. **No son comparables**: los primeros son cifras auto-reportadas verificables, el segundo generaba resultados con `random.uniform`. Reclasifico: hype real = claude-flow y OpenClaw; el resto es "benchmark no replicado", que es otra cosa.

**F7 — Infravalorados.** `uia-agent` (59,6) es el diseño más limpio del bloque —bucle con verificación explícita, R2, sin shell ni filesystem— y su puntuación baja viene casi toda de A9 (comunidad = 1 estrella), que pesa 3 puntos pero arrastra también A7. Como *patrón de referencia* vale más que su nota. `sandboxrs-windows` (67,0) igual: resuelve el problema exacto de Windows 11 Home sin admin.

**F8 — Sobrevalorados para este caso.** `OmniParser` (56,6) sigue apareciendo como fallback de percepción: 44 días sin commits, 2 humanos, licencia CC-BY-4.0 sobre código y pesos YOLOv8 de linaje AGPL sin aclarar, y superado por los VLM modernos. **Fuera.** `OSWorld` (74,8) es el 5.º mejor puntuado y es **inejecutable en tu máquina** (requiere VMs): es una fuente de verdad para leer, no un componente.

### 1.3 Información que quedó sin verificar y que asumo como riesgo
Stars de 24 de los 41 finalistas; lockfiles y advisories (sin acceso a OSV desde el entorno); latencia real de cualquier modelo local en tu hardware; comportamiento multi-monitor/DPI. Ninguna de estas lagunas cambia la decisión, porque la arquitectura elegida **no depende de modelos locales ni de repos de una estrella en el camino crítico**.

---

## 2. LA DECISIÓN, COMPONENTE A COMPONENTE

### 2.1 El orquestador: **Claude Code**. No LangGraph, no un framework nuevo.

| Pregunta | Respuesta |
|---|---|
| ¿Lo necesitamos? | Sí, algo tiene que ser el bucle. |
| ¿Por qué Claude Code y no LangGraph (78,6, el mejor puntuado)? | Porque ya tienes resuelto en él lo que LangGraph aportaría: **subagentes** con `model`, `tools`, `permissionMode`, `hooks` y `mcpServers` propios; **hooks con bloqueo** (`PreToolUse` → `permissionDecision: deny`, funcionan en Windows vía PowerShell); **skills con carga perezosa** (el cuerpo solo entra en contexto al usarse); permisos por herramienta; cliente MCP. Todo verificado en documentación oficial (E3). |
| ¿Qué perdemos? | Checkpoints durables y *time-travel*. Un agente personal no reanuda workflows de horas: no los tiene. |
| ¿Qué añadiría LangGraph? | Un segundo bucle, un segundo modelo de permisos que no se coordina con el de Claude Code, +dependencias Python, +mantenimiento. **Valor marginal negativo.** |

**Decisión firme: Claude Code es el harness. Ningún framework de agentes se instala.**

### 2.2 La percepción: **UIA primero, visión como respaldo**. No al revés.

Es la decisión técnica más importante del sistema y la evidencia es concluyente:

1. **Coste.** Un árbol UIA podado son ~3–6 k tokens de texto por paso. Un screenshot 1920×1080 son ~2,8 k tokens *de imagen*, y además obliga al modelo a resolver coordenadas. Con visión pura cada paso cuesta 3–4× más.
2. **Determinismo.** UIA invoca patrones reales (`Invoke`, `Value`, `SelectionItem`); la visión clica coordenadas y falla con cualquier cambio de escala o DPI.
3. **Tu hardware no admite la alternativa local.** Modelos de grounding que caben en 2 GB VRAM: 28–36 % en ScreenSpot-Pro. Inservible.
4. **La visión sigue siendo necesaria** donde UIA no llega: Roblox Studio, juegos, apps Electron con canvas, instaladores. Ahí se manda un screenshot a Claude (87,9 % ScreenSpot-Pro con Opus 4.8), pero **solo cuando el árbol UIA no devuelve nodos accionables**.

**Decisión firme: percepción UIA-first con fallback a screenshot bajo condición explícita, nunca por defecto.**

### 2.3 La capa de escritorio: **Windows-MCP, recortado**

Es el componente Windows más activo que existe (16 committers humanos en 90 días, CI en `windows-latest` con tests, 6,9 k estrellas) y encaja como servidor MCP en Claude Code sin escribir código.

Pero mi auditoría (F2, F3) obliga a condiciones **no negociables**:
- `ANONYMIZED_TELEMETRY=false` en la configuración MCP. Sin esto, hay una clave PostHog embebida activa.
- **Denegar `registry_tool` y `PowerShell`** desde los permisos de Claude Code. El registro no lo necesita un asistente de escritorio, y para shell ya tienes `Bash` nativo con hooks encima. Dos rutas de ejecución sin controlar es una de más.
- Permitir solo: `snapshot` (árbol UIA), `input`, `app`, `display`, `clipboard`, `scrape`.

*Alternativa considerada:* `uia-agent` — más limpio (R2, sin shell ni filesystem, verificación explícita, 4 k LOC). **Descartado del núcleo** por 1 estrella, 3 contribuidores y un benchmark que el propio README declara "valor objetivo, no medido". Queda como **plan B** y como fuente del patrón de poda del árbol.

### 2.4 El navegador: **Playwright MCP**. No browser-use.

Oficial de Microsoft, 36,8 k estrellas, **1 issue abierta**, CI Windows, Apache-2.0, sin telemetría detectada. Opera por árbol de accesibilidad del navegador: barato en tokens y determinista — el mismo argumento que en 2.2.
`browser-use` (112 k estrellas) es un **agente** completo: duplicaría el bucle de razonamiento que ya tiene Claude Code, trae telemetría PostHog activada por defecto y empuja hacia su nube. Para investigación autónoma, Claude Code razona y Playwright MCP ejecuta.

### 2.5 La memoria: **ficheros, no base de datos vectorial**

La evidencia externa es demoledora y va contra la intuición del documento original:
> En LoCoMo y LongMemEval **un modelo de contexto largo supera a la mejor capa de memoria por 35,2 y 33,4 puntos**. El valor real de una capa de memoria es coste y latencia a escala (7 k tokens vs 25 k+ por consulta), no precisión.

Tú eres un usuario, no una plataforma con millones de conversaciones. **No tienes el problema que resuelve mem0.** Añadirlo aporta: telemetría por defecto, features clave tras plan de pago de 249 USD/mes, benchmarks que nadie reproduce (91,6 % del vendedor vs 32–66 % independiente) y un servicio más que mantener.

**Decisión: la memoria son `CLAUDE.md` + skills + un directorio de notas en Markdown.** Si más adelante hace falta consulta semántica, **Basic Memory** (Markdown + MCP, W1, CI Windows, 601 tests) es el único candidato aceptable, porque lo que guarda **lo puedes leer y corregir tú**. Mem0, Zep, MemPalace, Letta: fuera.

### 2.6 La seguridad: **primitivas del SO + hooks**, no herramientas de seguridad de IA

**El hallazgo más importante de toda la investigación:** *ningún sandbox aísla el escritorio*. `sandbox-runtime`, AppContainer, Phylax y los gateways MCP protegen ficheros, red o protocolo — **ninguno impide que un proceso con acceso a UIA lea o controle cualquier ventana abierta**. Aislar de verdad exige una VM, y en una VM el agente ya no ve *tu* pantalla. Esto no tiene solución con las herramientas de 2026: se gestiona, no se elimina.

Lo que sí se hace, en orden de coste/beneficio:
1. **Hooks `PreToolUse`** como puerta de aprobación. Ya existen, funcionan en Windows, bloquean con `deny`, cuestan cero dependencias. Cubren el 80 % del problema.
2. **Cuenta de usuario Windows dedicada** para el agente, sin acceso a tu perfil ni a tus credenciales. Es el patrón que usan tanto OpenAI (Codex) como Anthropic (`sandbox-runtime`), verificado en ambas fuentes.
3. **Regla de higiene:** nunca ejecutar el agente con sesiones bancarias, gestores de contraseñas o el correo abiertos. Con UIA, "abierto en pantalla" equivale a "legible".

**Descartado del núcleo: los gateways MCP** (mcpgate, mcp-doorman, mcpproxy, mcpfw). Todos de un solo autor, sin adopción, y los hooks de Claude Code hacen su trabajo principal sin añadir un proceso intermedio. Solo se justifican cuando conectes varios MCP de terceros sin auditar.

### 2.7 El supervisor visual (§4 del documento): **se construye, no se instala**

Tu caso de uso más concreto —"estoy en Roblox Studio, dime si lo estoy haciendo mal"— no tiene ninguna solución madura. El único candidato Windows-nativo y local es **Blinky**: 12 estrellas, proyecto de hackathon, **badge MIT sin fichero LICENSE**, tres runtimes (Python + Bun + Rust), sin CI.

Pero la capacidad es simple: capturar pantalla (o leer el árbol UIA), mandarla a Claude con la pregunta correcta, y mostrar la respuesta. **Son ~200 líneas de una skill de Claude Code**, sin dependencias nuevas y sin heredar el riesgo de un prototipo ajeno. Blinky se usa como **referencia de diseño** —su clasificador previo de intención, que evita capturar pantalla cuando no hace falta, es una buena idea— no como dependencia.

### 2.8 Observabilidad y coste: **ccusage + logs propios**. Langfuse no todavía.

`ccusage` lee los logs locales de Claude Code y da coste por sesión: R0, local, cero riesgo. Langfuse es excelente (34 k estrellas, 642 tests) pero su servidor **exige Docker** en un portátil de 16 GB, para responder preguntas que en fase 1 responden los logs. Entra en fase 5 o cuando haya varios agentes concurrentes.

---

## 3. LO QUE NO SE PUEDE HACER HOY (y no hay que fingir que sí)

| Capacidad pedida | Estado real | Evidencia |
|---|---|---|
| Agente autónomo que ejecuta tareas largas sin supervisión | **No.** 31,4 % de completitud en tareas de ~1,6 h, con el mejor sistema existente y ~2–4 k USD por ejecución | OSWorld 2.0 (Snorkel, 2026-06) |
| Modelo de visión/grounding local en tu GPU | **No.** 2 GB VRAM solo admite modelos ≤3B, que rinden 28–36 % en ScreenSpot-Pro | ZonUI-3B (WACV 2026), BenchLM |
| Aislar al agente del resto del escritorio | **No.** Ningún sandbox cubre UIA ni inyección de input | Auditoría propia de los 5 candidatos de sandbox |
| Supervisión visual continua en tiempo real | **Técnicamente sí, económicamente no.** Cada frame es una imagen facturada; un bucle continuo cuesta decenas de USD/día | Cálculo §7 |
| Sistema de "workflows aprendidos" que se reutilizan solos | **No existe con evidencia.** Slot vacío en toda la investigación; lo más cercano son skills escritas a mano | `coverage.json` (B6.procedural) |

---

## 4. ARQUITECTURA FINAL

### CORE — el sistema mínimo que ya hace algo útil (5 componentes)

| # | Componente | Rol | Windows | Riesgo | Por qué es indispensable |
|---|---|---|---|---|---|
| 1 | **Claude Code** (suscripción) | Orquestador, subagentes, skills, permisos, cliente MCP | Nativo | R3 | Es el bucle. Sin él no hay agente |
| 2 | **Windows-MCP** *(recortado, telemetría off)* | Percepción UIA + acción (ratón/teclado/apps/captura) | Nativo (W1) | R3 | Único canal maduro de escritorio Windows |
| 3 | **Playwright MCP** | Navegador por accesibilidad | Nativo (W1) | R3 | Investigación y tareas web, barato en tokens |
| 4 | **Hooks `PreToolUse` propios** *(código tuyo, ~150 líneas)* | Puerta de aprobación y denylist | Nativo | R0 | Es toda la capa de seguridad de fase 1 |
| 5 | **`CLAUDE.md` + skills + notas Markdown** | Memoria, procedimientos, contexto | Nativo | R0 | Memoria suficiente, auditable, coste cero |

### HIGH VALUE — se añaden cuando el CORE funcione

| Componente | Aporta | Condición de entrada |
|---|---|---|
| **Skill "supervisor visual"** (tuya) | El caso de uso §4: observar, diagnosticar, guiar | Cuando el CORE sea estable |
| **Subagentes especializados** (research / computer / reviewer) | Aislamiento de contexto y modelo barato por rol | Cuando una sola sesión empiece a saturarse |
| **`ccusage`** | Coste real por sesión | Desde el primer día si quieres medir |
| **Cuenta Windows dedicada** | Contención real del daño | Antes de dar acceso a ficheros personales |
| **`promptfoo`** o evals propios | Demostrar que los cambios mejoran | Antes de añadir el 3.er componente |

### OPTIONAL — solo ante un problema concreto

`Basic Memory` (si las notas Markdown se quedan cortas) · `gpt-researcher` (si el research de Claude Code no basta) · `Langfuse` (si hay varios agentes y Docker deja de molestar) · `mcpgate`/`mcp-doorman` (si conectas MCP de terceros sin auditar) · `DSPy` (si optimizas prompts contra un eval real).

### EXPERIMENTAL — prometedor, no listo

`sandbox-runtime` (Windows **alpha**, exige admin; verificado en CI `windows-latest` y `windows-11-arm` — vigilar hasta que salga de alpha) · `sandboxrs-windows` (sandbox sin admin, honesto sobre sus límites, 1 autor, 22 días de vida) · `uia-agent` (mejor diseño del bloque, sin comunidad) · Modelos de grounding ≤4B (esperar a que quepan y rindan).

### AVOID — y por qué

| Proyecto | Motivo |
|---|---|
| **OpenClaw** | Cadena de 4 CVEs con escape de sandbox (CVSS 9,6), **341 skills maliciosas** en su marketplace (12 % de 2.857 auditadas), RCE en instalación de plugins. No importa lo activo que esté |
| **claude-flow / ruflo** | Benchmarks generados con `random.uniform`, features que devolvían éxito sin ejecutar nada, `--dangerously-skip-permissions` en 5 sitios, preinstall ofuscado retirado. El mantenedor corrige, pero la confianza está rota |
| **Dex** | Vendoriza OpenClaw + UFO² + browser-use: hereda todos los CVEs de OpenClaw |
| **DesktopCommanderMCP** | Shell + filesystem sin límites, postinstall script, telemetría — y redundante con las tools nativas de Claude Code |
| **mem0 / Zep / MemPalace** | Resuelven un problema de escala que no tienes; benchmarks irreproducibles; telemetría y funciones de pago |
| **LangGraph / CrewAI / AutoGen / Agno** | Duplican el harness. AutoGen además: 160 días sin commit sustantivo |
| **OmniParser** | Mantenimiento débil, licencia de pesos sin aclarar, superado por los VLM actuales |
| **mcp-shield / mcpkernel** | Prometen firewall/eBPF/Sigstore sin implementación ni actividad |
| **UFO²** | *No es un rechazo técnico* — es el mejor harness Windows que existe. Pero es un **agente completo** que compite con Claude Code por el bucle, con 137 k LOC y sin sandbox. Si algún día abandonas Claude Code, es la primera alternativa |

### Flujo de información

```
                    ┌──────────────────────────┐
                    │   TÚ  (Windows 11)       │
                    └────────────┬─────────────┘
                                 │ instrucción en lenguaje natural
                                 ▼
              ┌────────────────────────────────────────┐
              │  CLAUDE CODE  (orquestador + memoria)  │
              │  CLAUDE.md · skills · subagentes       │
              └───┬──────────────┬──────────────┬──────┘
                  │              │              │
      ┌───────────▼───┐   ┌──────▼──────┐  ┌────▼─────────┐
      │ HOOK PreTool  │   │  subagente  │  │  subagente   │
      │ ¿permitido?   │   │  research   │  │  computer    │
      │ deny / ask    │   └──────┬──────┘  └────┬─────────┘
      └───────┬───────┘          │              │
              │ allow            ▼              ▼
              │          ┌──────────────┐  ┌──────────────────┐
              ├─────────►│ Playwright   │  │  Windows-MCP     │
              │          │ MCP (web)    │  │  (recortado)     │
              │          └──────────────┘  └───┬──────────┬───┘
              │                                │          │
              │                       árbol UIA│          │ si UIA
              │                       (barato) │          │ no da nodos
              │                                ▼          ▼
              │                          acción      screenshot →
              │                          + verify    Claude (visión)
              ▼
      ┌────────────────┐        ┌──────────────────────┐
      │ Bash nativo    │        │ notas .md + ccusage  │
      │ (con hooks)    │        │ memoria + coste      │
      └────────────────┘        └──────────────────────┘
```

Regla del flujo: **toda acción que modifique algo pasa por el hook antes de ejecutarse.** La percepción (leer árbol, capturar pantalla) no pide permiso; la acción (clicar, escribir, ejecutar, borrar) sí.

---

## 5. WINDOWS 11 Y TU HARDWARE

| Componente | Clasificación | Nota para tu equipo |
|---|---|---|
| Claude Code | **Native Windows** | Sin problema |
| Windows-MCP | **Native Windows** | Python 3.13; CI en `windows-latest`; requiere sesión interactiva |
| Playwright MCP | **Native Windows** | Node; descarga navegadores (~500 MB de disco) |
| Hooks | **PowerShell** | Documentado y verificado en Windows |
| ccusage | **Native Windows** | Node, R0 |
| Basic Memory | **Native Windows** | CI Windows con 601 tests |
| sandbox-runtime | **PowerShell + admin** | Alpha; crea usuario local y filtros WFP; **no en fase 1** |
| Langfuse (servidor) | **Docker** | 16 GB de RAM lo aguantan, pero es peso muerto al principio |
| OSWorld / WAA | **VM** | Inejecutable aquí. Se lee, no se corre |
| UFO², Agent-S | Native / PowerShell | Descartados por arquitectura, no por Windows |

**Tu hardware, sin adornos:**
- **i7-1065G7 (4 núcleos, Ice Lake móvil)**: suficiente para el agente, que es I/O y red. Sufrirá con OCR local continuo.
- **16 GB RAM**: cómodo. Docker + Langfuse + navegadores lo apretarían.
- **MX330, 2 GB VRAM**: **el cuello de botella y la razón de que el stack sea cloud-first.** No cabe ningún modelo de razonamiento ni de visión útil. Lo único razonable en local: OCR (Windows OCR API nativo, RapidOCR) y embeddings pequeños. **No compres la idea de "modelo local" con esta GPU.**
- **Multi-monitor y escalado DPI**: sin verificar en ninguno de los candidatos. Es el primer fallo práctico que te vas a encontrar. Pruébalo el día 1.

---

## 6. MATRIZ DE RIESGO

| Componente | Beneficio | Complejidad | Riesgo | Permisos | Privacidad | Reversibilidad |
|---|---|---|---|---|---|---|
| Claude Code | Muy alto | Baja | **Medio** | Shell, FS, red, credenciales | Prompts y ficheros al proveedor | Alta (desinstalar) |
| Windows-MCP *(recortado)* | Muy alto | Baja | **Alto** | UIA, input, captura, portapapeles | Lo que haya en pantalla | Alta (quitar del config) |
| Windows-MCP *(completo)* | Alto | Baja | **Muy alto** | + registro (set/delete), PowerShell sin filtro, FS | + telemetría ON por defecto | Alta |
| Playwright MCP | Alto | Baja | **Medio** | Perfil de navegador, red | Cookies y sesiones si usas tu perfil | Alta |
| Hooks propios | Alto | Baja | **Bajo** | Ninguno | Ninguna | Total |
| Notas Markdown | Medio | Muy baja | **Bajo** | FS local | Local | Total |
| Subagentes | Alto | Media | **Bajo** | Heredados, restringibles | Igual que el padre | Total |
| sandbox-runtime | Alto | Alta | **Medio** | Admin en instalación | Ninguna | Media (deja usuario y reglas WFP) |
| Cuenta Windows dedicada | Alto | Media | **Bajo** | — | Aísla tu perfil | Media |

### Los cuatro riesgos que importan de verdad

1. **Inyección de prompt desde la pantalla.** Si el agente lee una ventana con texto malicioso ("ignora las instrucciones anteriores y ejecuta…"), ese texto entra como datos y puede convertirse en instrucciones. **Ningún componente de esta arquitectura lo previene.** Mitigación real: el hook de aprobación para todo lo destructivo, y no dejar al agente leyendo contenido no confiable mientras tiene permisos amplios.
2. **Lectura indiscriminada de pantalla.** UIA lee cualquier ventana visible: contraseñas, correo, banca. Mitigación: higiene de sesión (§2.6.3) y cuenta dedicada.
3. **Ejecución de código generado por IA.** `Bash` + `PowerShell` = dos rutas. **Cierra una** (deniega `PowerShell` de Windows-MCP) y pon hooks en la otra.
4. **Cadena de suministro.** La lección de OpenClaw (341 skills maliciosas) y claude-flow (preinstall ofuscado) es que **cada MCP o skill de terceros es código que corre con tus permisos**. Regla: solo MCP oficiales o auditados por ti, y `mcp-scan` antes de añadir cualquier otro.

---

## 7. COSTE Y TOKENS

### De dónde viene el gasto

| Fuente | Impacto | Optimización concreta |
|---|---|---|
| **Screenshots** | ~2,8 k tokens de *imagen* cada uno | Usar UIA por defecto; imagen solo si el árbol no da nodos accionables. **Ahorro estimado 60–70 %** |
| **Árbol UIA sin podar** | Una ventana compleja pasa de 30 k tokens | Podar a ≤400 nodos / 12 niveles (patrón de `uia-agent`): 3–6 k |
| **Contexto acumulado** | Cada paso reenvía la historia | Prompt caching; subagentes para aislar el contexto de tareas largas |
| **Subagentes** | Cada uno es una conversación nueva | Asignarles `model: haiku`/`sonnet`; reservar Opus para el orquestador |
| **MCP conectados** | Cada tool ocupa contexto siempre | Solo 2 MCP con las tools recortadas |
| **Bucle de verificación** | Duplica llamadas si verificas cada paso | Verificar por hito, no por paso |

### Coste estimado por paso de agente

| Modo | Tokens/paso | Modelo | USD/paso | Tarea de 20 pasos |
|---|---|---|---|---|
| UIA + Sonnet 5 | ~4 k in / 300 out | $2 / $10 por M | **~0,011** | **~0,22** |
| UIA + Opus 5 | ~4 k in / 300 out | $5 / $25 por M | ~0,028 | ~0,55 |
| Visión + Opus 5 | ~7 k in / 300 out | $5 / $25 por M | ~0,043 | ~0,85 |

**Recomendación de facturación: usa la suscripción de Claude Code para el bucle principal, no la API.** Un uso realista (20–30 tareas cortas al día) se iría a ~30–60 USD/mes por API; la suscripción lo acota. Reserva la API para subagentes en lote y evals.

**Presupuesto de arranque: 0 USD adicionales.** Todo el CORE es open source o ya lo pagas.

---

## 8. CÓMO DEMOSTRAR QUE CADA COMPONENTE MEJORA EL AGENTE

Sin esto, en tres meses tendrás quince herramientas y ninguna prueba de que alguna sirva.

**Banco de pruebas: 20 tareas reales tuyas**, escritas antes de instalar nada, con criterio de éxito verificable por ti. Ejemplos: "abre VS Code y crea un archivo con este contenido", "busca X en la web y resume 3 fuentes", "dime qué está mal en esta escena de Roblox Studio", "renombra estos 5 ficheros según este patrón".

**Métricas, medidas antes y después de cada componente:**

| Métrica | Cómo se mide | Umbral para conservar el componente |
|---|---|---|
| Task completion | % de las 20 tareas completadas sin intervención | **+10 puntos** o se retira |
| Accuracy | % de acciones correctas al primer intento | +5 puntos |
| Tool calls | Media por tarea | No debe subir >20 % |
| Tokens | `ccusage` por tarea | No debe subir >30 % sin ganar completitud |
| Coste | USD por tarea completada | Coste **por tarea completada**, no por llamada |
| Latencia | Segundos hasta el resultado | No debe duplicarse |
| Errores | Acciones que hubo que deshacer | Debe bajar |
| Intervención humana | Nº de veces que tuviste que corregir | Debe bajar |
| Alucinaciones | Afirmaciones sobre la pantalla que eran falsas | **Debe ser 0 en acciones destructivas** |
| Seguridad | Acciones destructivas ejecutadas sin aprobación | **Debe ser 0. Sin excepciones** |
| Estabilidad | Fallos por cada 20 tareas | Debe bajar |

**Regla de retirada:** un componente que en dos rondas no mejora ninguna métrica por encima de su umbral **se desinstala**. Esto aplica a todo lo de HIGH VALUE y OPTIONAL, sin discusión.

---

## 9. PLAN DE IMPLEMENTACIÓN

| Fase | Objetivo | Qué se instala | Qué validar antes de seguir | Rollback |
|---|---|---|---|---|
| **0 — Línea base** *(sin instalar nada)* | Escribir las 20 tareas y medir Claude Code solo | Nada | Tienes números de partida | — |
| **1 — Seguridad primero** | Hooks de aprobación + `CLAUDE.md` | Código tuyo | Un `rm -rf` de prueba **se bloquea** | Borrar el hook |
| **2 — Ojos y manos** | Windows-MCP recortado, telemetría off | 1 MCP | El agente lee el árbol de VS Code, abre apps, escribe texto. **Prueba multi-monitor y DPI** | Quitar del config |
| **3 — Verificación** | El agente comprueba su propia acción | Skill tuya | Detecta que una acción falló, en ≥80 % de los casos | Borrar la skill |
| **4 — Web** | Playwright MCP + subagente de research | 1 MCP | Investigación con fuentes citadas y sin tocar tu perfil de navegador | Quitar del config |
| **5 — Supervisor visual** | El caso de uso §4 | Skill tuya | Diagnostica correctamente en Roblox Studio / VS Code | Borrar la skill |
| **6 — Multi-agente** | Subagentes con modelo barato por rol | Configuración | Baja el coste por tarea sin bajar completitud | Volver a agente único |
| **7 — Endurecer** | Cuenta dedicada y, si sale de alpha, sandbox-runtime | Cuenta Windows | Nada se rompe con permisos reducidos | Volver a tu cuenta |

**Qué probar primero, si solo haces una cosa:** la **fase 2** con una tarea trivial —"abre el Bloc de notas, escribe 'hola', guárdalo en el escritorio"— y mira dos cosas: cuántos tokens consume el árbol UIA, y si funciona con tu escalado de pantalla. Si el árbol UIA de tus aplicaciones reales resulta ser inútil (aplicaciones que se dibujan solas, sin nodos accionables), **toda esta arquitectura cambia** y hay que reconsiderar el camino de visión, asumiendo su coste. Es la única incógnita que puede invalidar la decisión, y se resuelve en una tarde.

---

## 10. FINAL CHECK

| Pregunta | Respuesta |
|---|---|
| ¿Componentes redundantes? | Eliminados: LangGraph (duplica el harness), browser-use (duplica el bucle), mem0 (duplica la memoria de ficheros), gateways MCP (duplican los hooks), Langfuse en fase 1 (duplica ccusage). |
| ¿Evidencia débil? | Sí, y está marcada: el supervisor visual no tiene precedente maduro (se construye); sandbox-runtime en Windows es alpha (queda fuera del núcleo); multi-monitor/DPI sin verificar en ningún candidato. |
| ¿Riesgo desproporcionado? | Windows-MCP completo, sí — por eso va recortado con telemetría desactivada. OpenClaw y claude-flow, sí — por eso están en AVOID. |
| ¿Funciona en Windows 11? | Los 5 componentes del CORE son W1 nativos con CI en `windows-latest`. Cero Docker, cero WSL, cero VM. |
| ¿Gastamos tokens de más? | La decisión UIA-first ahorra un 60–70 % frente a visión por defecto; los subagentes con modelo barato son el segundo ahorro. |
| ¿Se puede quitar algo más? | Sí: Playwright MCP es prescindible en fase 1 si solo quieres control del PC. El mínimo absoluto son 3 piezas: Claude Code + Windows-MCP + hooks. |
| ¿Alternativa más simple? | Solo una: Claude Code sin MCP de escritorio, pidiéndole comandos PowerShell. Funciona para automatización de ficheros, **no** para "ver la pantalla". Si nunca necesitas GUI, es más simple y más segura. |
| ¿Qué se prueba primero? | Fase 2, tarea trivial, midiendo tokens del árbol UIA y comportamiento con tu DPI. |

---

## 11. RESPUESTAS DIRECTAS

**¿Qué debemos construir?** Un agente basado en Claude Code con percepción UIA y una capa de aprobación por hooks. Lo que se construye a mano (hooks, skill de verificación, skill de supervisor visual) son unas 500 líneas en total.

**¿Qué debemos instalar eventualmente?** Windows-MCP (recortado), Playwright MCP, ccusage. Después, según medición: Basic Memory, promptfoo, sandbox-runtime.

**¿Qué NO debemos instalar?** OpenClaw, claude-flow, Dex, DesktopCommanderMCP, mem0/Zep/MemPalace, LangGraph/CrewAI/AutoGen, OmniParser, mcp-shield, mcpkernel. Motivos en §4.

**¿Cuál es la arquitectura recomendada?** §4. Cinco componentes en el núcleo.

**¿Orden de implementación?** §9. Seguridad antes que capacidad — es lo contrario de lo que hace todo el mundo, y es la razón por la que a todo el mundo le acaba pasando algo.

**¿Qué riesgos existen?** Inyección de prompt desde pantalla (sin solución hoy), lectura indiscriminada de pantalla, doble ruta de ejecución de código, cadena de suministro de MCP y skills. §6.

**¿Cuánto costará?** 0 USD de instalación. Operación: entre 0 (suscripción de Claude Code) y ~30–60 USD/mes si vas por API con uso intensivo. §7.

**¿Qué probar primero?** El árbol UIA de tus aplicaciones reales. §9.

**¿Cómo sabremos que mejoró?** Las 20 tareas y las 11 métricas de §8, con umbral de retirada. Si un componente no supera su umbral, se va.
