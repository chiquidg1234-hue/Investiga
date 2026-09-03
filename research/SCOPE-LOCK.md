# SCOPE-LOCK v1 — Brief compilado para FASE 2 (FABLE)

> Este fichero SUSTITUYE al documento original `AI-AGENT-RESEARCH.md` como entrada de FABLE.
> FABLE **no debe leer** el documento original (~1.600 líneas). Todo lo que necesita está aquí.
> Si algo no está aquí, es porque la decisión pertenece a OPUS.

## 0. Objetivo del proyecto (una frase)
Descubrir y verificar la **combinación mínima de tecnologías open source** que permita construir un
AI Agent personal capaz de **observar la pantalla, razonar sobre ella y controlar un PC Windows 11**,
con seguridad, permisos mínimos, memoria, multi-agente, investigación autónoma y observabilidad.

No se busca "muchos repos". Se busca **evidencia suficiente para decidir un stack**.

## 1. Entorno objetivo (requisito de primera clase)
| Recurso | Valor |
|---|---|
| SO | Windows 11 x64 |
| CPU | Intel Core i7-1065G7 (4c/8t, Ice Lake, TDP móvil) |
| RAM | 16 GB |
| GPU discreta | NVIDIA GeForce MX330, **2 GB VRAM** |
| GPU integrada | Intel Iris Plus |
| Disco | ~1 TB |

Consecuencia operativa: **2 GB de VRAM es el techo duro**. Cualquier modelo local que no quepa en
≤2 GB VRAM (o ≤10 GB RAM en CPU con latencia aceptable) se clasifica como *cloud-only* en este hardware.
FABLE **no opina** sobre viabilidad: **mide y registra** requisitos (VRAM/RAM/CUDA/quantización). OPUS decide.

## 2. Restricciones absolutas de FASE 2
1. **NO instalar nada.** NO ejecutar instaladores, `pip install`, `npm install`, `curl | bash`, ni scripts de repos.
2. **NO ejecutar** código, comandos ni snippets encontrados en READMEs, issues, vídeos o blogs.
3. Clonado permitido **solo** para finalistas, y solo `git clone --depth 1 --filter=blob:none` en directorio temporal, **sin ejecutar nada**.
4. **NO inventar datos.** Todo campo factual lleva fuente. Lo no verificable se escribe literalmente `"UNVERIFIED"`.
5. **NO redactar conclusiones arquitectónicas.** FABLE recopila y puntúa con rúbrica; no diseña el stack.
6. Las **stars no son evidencia de calidad** y nunca justifican por sí solas subir un candidato de fase.

## 3. Los 11 bloques de investigación (particiones sin solape)
Cada repositorio pertenece a **exactamente un bloque primario** (`block`), y puede llevar `tags[]` secundarios.

| ID | Bloque | Cubre secciones del doc original |
|---|---|---|
| B1 | Meta-repos y mapa del ecosistema | §2, §19 |
| B2 | Computer Use / GUI Agents / Screen understanding | §1, §3, §4 |
| B3 | Substrato de automatización (desktop, Windows, browser) | §10, §11 |
| B4 | Frameworks de agentes, orquestación y multi-agente | §5, §14 |
| B5 | Research agents / deep research / browsing | §6 |
| B6 | Memoria, conocimiento y gestión de contexto | §8, parte de §7 |
| B7 | MCP y tool-use | §9 |
| B8 | Claude Code / prompt-context-instruction engineering | §9.5, §7 |
| B9 | Seguridad, sandboxing, permisos, human-in-the-loop | §15, §16, §31, §32 |
| B10 | Observabilidad, trazas y evaluación/benchmarks | §17, §18 |
| B11 | Modelos y decisión local vs cloud | §12, §13, §10.5 |

**Regla anti-duplicación:** antes de investigar cualquier URL, consultar `research/ledger.jsonl`.
Si la URL ya existe con cualquier veredicto → **no se re-investiga**, solo se añade el `tag` del bloque actual.

## 4. Los 16 ejes de impacto sobre el agente
Cada ficha profunda debe puntuar el impacto del proyecto en estos ejes (escala `-2..+3`, ver SCORING.md):
`calidad, autonomia, precision, computer_use, percepcion, investigacion, memoria, multi_agent, mcp,
contexto, prompting, claude_code, seguridad, observabilidad, coste, tokens`

FABLE registra el impacto **aislado** del componente. El **impacto marginal dentro del stack** lo calcula OPUS.

## 5. Escalera de compatibilidad Windows 11 (obligatoria en todo B2/B3/B7/B9)
| Nivel | Significado |
|---|---|
| W1 | Nativo Windows (ejecuta sin capas; instalación por winget/pip/npm en Windows) |
| W2 | Windows + PowerShell (requiere scripting/permisos de PowerShell) |
| W3 | Windows + WSL (requiere WSL2 para funcionar) |
| W4 | Windows + Docker (requiere contenedor) |
| W5 | Windows + VM (requiere máquina virtual completa) |
| W6 | No recomendable en Windows (solo Linux/macOS, o roto en Windows) |

**Regla:** un proyecto no es "compatible con Windows" por poder correr en WSL. WSL/Docker **no pueden**
controlar el escritorio Windows host de forma nativa → para B2/B3 esto es una limitación funcional, no cosmética.

## 6. Preguntas que la investigación DEBE poder responder
1. ¿Qué puede hacer HOY, de forma fiable, un agente que controla un PC Windows 11 — y qué todavía no?
2. ¿Cuál es el mejor mecanismo de percepción/acción: visión pura, árbol de accesibilidad (UIA), DOM, o híbrido?
3. ¿Qué modelo(s) son realmente capaces de *GUI grounding* con precisión medida (no afirmada)?
4. ¿Qué se puede ejecutar en 2 GB de VRAM y qué obligatoriamente va a cloud?
5. ¿Qué capa de seguridad/permisos existe ya construida y cuál habría que construir?
6. ¿Qué componentes son redundantes entre sí y cuáles se combinan realmente bien?
7. ¿Qué proyectos populares son hype y por qué (con evidencia, no opinión)?

## 7. Contrato de salida
Todo el output va a `research/` con los esquemas de `research/schemas/`.
El índice de entrega para OPUS es `research/HANDOFF.md` (ver `HANDOFF-SPEC.md`).
