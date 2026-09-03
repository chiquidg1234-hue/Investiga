# HANDOFF FASE 2 → FASE 3 (2026-09-03)

Modelo ejecutor: claude-fable-5-1 (sesión configurada como claude-opus-5). Todo dato factual lleva evidence_id; lo no verificable está marcado UNVERIFIED.

## 1. Embudo
- Descubiertas: 572 claves en ledger (2.876 únicas en 45 listas awesome; 341 en ≥2 listas, 126 en ≥3) + Exa/WebFetch.
- Triadas con sonda de clon (G2+G3 fusionados por bloqueo de la API GitHub): 155 · KILL 47 · PARKED 67 · FINALISTAS 41 (cupo ampliado de 32 a 41 para no vaciar slots).
- Códigos de muerte más usados: K13 (aparcado por cupo/redundancia), K2 (inactividad), K4 (demo/tutorial), K5 (dominado), K9 (paper/pesos), K11 (claim sin implementación).
## 2. Cobertura
- Slots cubiertos en B2, B3, B4, B5, B7, B9, B10. Débiles/vacíos: B6.context_compression (cubierto por features nativas de API/Claude Code, no por repos), B6.procedural (sin sistema de 'workflows aprendidos' con evidencia), B8.context_claudemd (solo SKILL.md sin evaluación), B8.routing (nada con evidencia; subagentes nativos permiten `model:` por agente), B9.supply_chain (solo mcp-scan). Detalle: coverage.json.
## 3. Presupuesto
- Coste reportado por la sesión al momento del build: ≈ USD 2.92 (cache_read 860k, cache_write 123k, output 50k) de los 25 autorizados. Cifra final en el checkpoint.
## 4. Diez hechos verificados (con evidencia)
1. Dos vías reales de percepción en Windows: árbol UIA (UFO, Windows-MCP, Windows-Use, uia-agent: deps uiautomation/pywinauto en clon) y visión (OmniParser, VLMs). Solo UFO combina ambas en código. [E2 sondas]
2. OSWorld-Verified está saturándose para modelos frontier (85-86%) y OSWorld 2.0 (tareas de ~1.6 h) sigue en 31% binario con ~USD 2-4k por run: la autonomía larga no es fiable hoy. [E3 Steel/Snorkel]
3. En grounding puro (ScreenSpot-Pro) los modelos ≤4B viables en 2 GB VRAM rinden 28-36% frente a 85-88% de los frontier cloud; el techo de VRAM hace el grounding local de baja calidad. [E3 papers/BenchLM]
4. Ningún sandbox encontrado aísla el escritorio (UIA/input); solo VMs. sandbox-runtime (Windows alpha, requiere admin) y AppContainer (sin admin, rompe herramientas) cubren FS/red. [E1/E2]
5. OpenClaw acumula en 2026: cadena de 4 CVEs con escape de sandbox (CVSS 9.6), 341 skills maliciosas en su marketplace, RCE en instalación de plugins. [E3 CSA/GHSA]
6. claude-flow/ruflo: auditorías independientes documentan features simuladas, benchmarks generados con random.uniform y --dangerously-skip-permissions hardcodeado; el mantenedor ha corregido parte. [E3]
7. Los benchmarks de memoria no son comparables entre vendors y el contexto largo los supera en 30+ puntos; Mem0 y Zep ponen sus mejores features tras pago; mem0 y browser-use envían telemetría por defecto (opt-out por env). [E2 telemetry.py, E3]
8. Claude Code ofrece nativamente hooks con bloqueo (PreToolUse deny, funcionan en Windows), subagentes con modelo/tools/permisos propios y skills con carga perezosa: gran parte de B8 ya existe sin terceros. [E3 docs]
9. Los gateways MCP con política/aprobación (mcpgate, mcp-doorman, mcpproxy, mcpfw) son todos de un solo autor; el único con equipo (toolhive) exige Docker en Windows. [E2 sondas]
10. Windows-MCP (6.9k stars, 16 committers/90d, CI Windows) es el componente Windows más activo; uia-agent (1 star) es el diseño más limpio (verify + MCP, R2) pero sin benchmark medido. [E2/E3]
## 5. Vetos aplicados
- jeomon/windows-use: V3
- kingsahil/blinky: V2
- nousresearch/hermes-agent: V1
- openclaw/openclaw: V3, V6
- wonderwhy-er/desktopcommandermcp: V3
- ruvnet/claude-flow: V3, V8
## 6. HYPE_FLAG (regla mecánica: hype_index ≥ 0.5 con ≥5k stars; incluye casos donde la claim fallida es un benchmark auto-reportado)
- microsoft/ufo: claims sin E2+: ['Resultados en Windows Agent Arena y OSWorld-Windows', 'Hasta 51% menos consultas LLM por bundling']
- microsoft/omniparser: claims sin E2+: ['Mejor rendimiento en Windows Agent Arena (2024)', '0.6 s/frame en A100, 0.8 s en 4090']
- simular-ai/agent-s: claims sin E2+: ['56.6% Windows Agent Arena', 'Soporta Windows']
- openclaw/openclaw: claims sin E2+: ['Sandbox OpenShell aísla al agente', 'Marketplace de skills seguro']
- mem0ai/mem0: claims sin E2+: ['SOTA en LoCoMo (~91-92%)']
- getzep/graphiti: claims sin E2+: ['~84% LoCoMo']
- mempalace/mempalace: claims sin E2+: ['96.6% R@5 LongMemEval sin API']
- ruvnet/claude-flow: claims sin E2+: ['84.8% SWE-bench', '30-50% ahorro de tokens', 'Orquesta agentes reales']
- anthropic-experimental/sandbox-runtime: claims sin E2+: ['Filtro WFP bloquea conexiones aunque el proceso ignore el proxy']
## 7. Hidden gems (juicio de FABLE, no flag mecánico: stars desconocidas o claims auto-declaradas)
- SuperMarioYL/uia-agent (B2): 4k LOC, verify explícito, MCP, R2, activo; 1 star; benchmark no medido.
- maksym-mishchenko/mcpgate (B7): deny-by-default fail-closed con aprobación y auditoría; activo hoy; 1 autor.
- Sushank05/mcp-doorman (B7, PARKED): policy + redacción de secretos + pinning + elicitación MCP; 0 stars, 56 d.
- TarunKurella/sandboxrs-windows (B9): sandbox sin admin verificado en CI como usuario estándar; 22 d, 1 autor.
- KingSahil/Blinky (B2): único supervisor visual Windows-nativo y local activo; hackathon, sin LICENSE.
- lessenings-prog/OpenGUI (B2, PARKED): servicio .NET con bucle O-P-E-V-R y verificación; 0 stars, 6 tests.
## 8. Clusters escalados a OPUS (sin ganador mecánico)
- C1 escritorio Windows: UFO vs Windows-MCP vs uia-agent (Windows-Use eliminado por dominancia).
- C3 gateway MCP: mcpgate vs mcp-doorman vs toolhive(Docker).
- C4 memoria: mem0 vs graphiti vs MemPalace vs basic-memory (evidencia E3: precisión no es el criterio).
- C5 orquestación: LangGraph vs OpenAI Agents vs Pydantic AI vs Claude Agent SDK.
- C6 sandbox Windows: sandbox-runtime vs sandboxrs vs Phylax.
- C7 navegador: playwright-mcp vs browser-use.
- Ganador mecánico: C2 supervisor visual → Blinky (los otros 3 inactivos).
## 9. Contradicciones abiertas
- Ver contradictions.md (leaderboards OSWorld, benchmarks de memoria, AppContainer, claude-flow, Agent S, OmniParser, Blinky, Phylax).
## 10. Lo que NO se investigó y por qué
- Stars/issues de 24 finalistas (API bloqueada; WebFetch limitado a 17). Advisories/lockfiles (sin OSV). Latencia local real (prohibido instalar). Embeddings (presupuesto). letta-code, nice-mee/WindowsAgentArena, openlit, AgentBench, owl (cupo/timeout). Búsqueda dedicada en fuentes CN/JP/KR. Vídeo/redes: excluidos por diseño.
## Protocolo de auditoría sugerido (HANDOFF-SPEC §4)
- Muestrear 15 evidence_ids E2/E3 de evidence/*.jsonl; las E2 'clone:' se re-verifican clonando el SHA indicado; las E3 por URL.
- Recalcular score_global desde A1..A10 (pesos 15/15/15/15/10/10/10/5/3/2) y comprobar caps V*.
- Fichas con tokens_spent=9000 son estimaciones uniformes (no medidas por ficha).
