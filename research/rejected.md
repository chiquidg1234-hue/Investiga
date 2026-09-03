# Candidatos descartados y aparcados (G2/G3)

| key | bloque | veredicto | código | razón |
|---|---|---|---|---|
| arize-ai/phoenix | B10 | KILL | K5 | activo; dominado por Langfuse en el cluster por simplicidad de self-host (ambos Docker) |
| comet-ml/opik | B10 | KILL | K5 | activo; mismo cluster que Langfuse; PARKED |
| microsoft/windowsagentarena | B10 | KILL | K2 | 651d sin commits; el fork nice-mee/WindowsAgentArena usado por UFO no fue sondeado |
| agentsea/surfkit | B2 | KILL | K2 | 433d sin commits |
| aiagentwithdhruv/screen-sage | B2 | KILL | K4 | 1.6k LOC, sin licencia, 178d, demo web con Gemini Live |
| alessiobianchini/desktopagent | B2 | KILL | K3 | sin fichero LICENSE; 162d; 0 tests; 1 autor |
| bytedance/ui-tars | B2 | KILL | K9 | repo = enlaces a pesos/paper (722 LOC), 362d; los pesos van a models.json |
| chethan616/dex | B2 | KILL | K5 | fork de OpenClaw + UFO² + browser-use vendorizados (700k LOC, bus 0.95); hereda los CVEs de OpenClaw; licencia OTHER |
| e2b-dev/open-computer-use | B2 | KILL | K2 | 454d sin commit sustantivo; 1.1k LOC demo |
| geisterhand-io/windows | B2 | KILL | K2 | 178d; 0 humanos/90d; 2 tests |
| han1018/zonui-3b | B2 | KILL | K9 | código de entrenamiento sin licencia, 293d; el modelo va a models.json |
| lessenings-prog/opengui | B2 | KILL | K4 | 0 stars, 6 tests, 88d, 1 autor, sin LICENSE; PARKED: diseño interesante (verificación O-P-E-V-R) |
| microsoft/magentic-ui | B2 | KILL | K5 | 41d, 5 humanos; UI HITL sobre navegador (Docker/WSL); dominado por browser-use+playwright-mcp para el objetivo Windows |
| minkpark/heronwin | B2 | KILL | K4 | 0 tests, 94d sustantivo, .NET 10; PARKED como referencia de MCP UIA en .NET |
| mo-tunn/openguider | B2 | KILL | K5 | 121d; Electron; guía por coordenadas; dominado por Blinky (Windows-nativo, activo) en el mismo slot |
| os-copilot/os-copilot | B2 | KILL | K2 | 723d sin commits |
| othersideai/self-operating-computer | B2 | KILL | K2 | 477d sin commit sustantivo; solo macOS declarado |
| r-muresan/screen.vision | B2 | KILL | K2 | 224d sin commit sustantivo; web-only, envía screenshots a OpenAI/Fireworks |
| xlang-ai/opencua | B2 | KILL | K9 | 100d, 7.6k LOC de eval; modelos 7B-72B no viables localmente; va a models.json |
| asweigart/pyautogui | B3 | KILL | K2 | 1.193d sin commits; sin CI; usado por UFO/Windows-Use como dependencia |
| browserbase/stagehand | B3 | KILL | K5 | activo (56 commits) pero orientado a Browserbase cloud; PARKED como alternativa TS |
| nottelabs/notte | B3 | KILL | K5 | licencia OTHER; dominado por browser-use |
| skyvern-ai/skyvern | B3 | KILL | K5 | AGPL, 800k LOC; dominado por browser-use (MIT, más simple) para uso personal |
| geekan/metagpt | B4 | KILL | K2 | 224d sin commits |
| microsoft/autogen | B4 | KILL | K5 | 160d sin commit sustantivo, 0 humanos/90d (equipo migró a otros proyectos); dominado por LangGraph/OpenAI Agents |
| camel-ai/owl | B5 | KILL | K6 | timeout de clonado; no evaluado |
| dzhng/deep-research | B5 | KILL | K2 | 452d sin commit sustantivo |
| jina-ai/node-deepresearch | B5 | KILL | K2 | 124d, 0 humanos/90d |
| letta-ai/letta | B6 | KILL | K5 | el repo es un puntero: código movido a letta-ai/letta-code (no sondeado); runtime completo, no capa; PARKED |
| supermemoryai/supermemory | B6 | KILL | K10 | producto SaaS con SDK; PARKED |
| piyushptiwari1/mcpkernel | B7 | KILL | K11 | 100d, 0 humanos/90d; README promete eBPF/Firecracker/Sigstore/OWASP; 30k LOC con 41 tests; claims no verificadas → HYPE_FLAG |
| tonyc973/mcp-shield | B7 | KILL | K11 | 1.3k LOC, 0 tests, roadmap sin marcar: promete firewall CVE-tested sin implementarlo |
| banner-wang/prompt-smith | B8 | KILL | K4 | 897 LOC, 85d |
| disler/claude-code-hooks-mastery | B8 | KILL | K4 | 213d; tutorial de hooks sin licencia |
| kimhance/claude-config-helper | B8 | KILL | K4 | 3k LOC, 101d, sin licencia |
| microsoft/promptwizard | B8 | KILL | K2 | 471d sin commits |
| pimzino/claude-code-spec-workflow | B8 | KILL | K2 | 360d sin commits |
| severity1/claude-code-prompt-improver | B8 | KILL | K4 | 2k LOC, 91d, bus 0.93, sin evaluación |
| sujayopensource/claude-cost-optimizer | B8 | KILL | K4 | 4.6k LOC, 128d, 0 tests, sin medición |
| thedoublejay/please-optimize-my-claude | B8 | KILL | K4 | 0 LOC de código (solo SKILL.md), 146d, 1 autor |
| xanthar/claude-harness | B8 | KILL | K2 | 261d sin commits |
| azure/pyrit | B9 | KILL | K6 | clon vacío (repo movido); no evaluado |
| e2b-dev/e2b | B9 | KILL | K10 | sandbox cloud de pago; PARKED |
| jarkkojs/landstrip | B9 | KILL | K3 | sin fichero LICENSE; activo; PARKED (AppContainer/restricted user en Windows) |
| protectai/llm-guard | B9 | KILL | K2 | 364d sin commit sustantivo |
| splx-ai/agentic-radar | B9 | KILL | K2 | 279d sin commits |
| teckwin/sandbox | B9 | KILL | K3 | sin LICENSE, 150d, 2 tests |
| e2b-dev/awesome-ai-agents | B1 | PARKED | K13 | meta-lista; ecosystem-map |
| francedot/acu | B1 | PARKED | K13 | meta-lista (475d sustantivo); ecosystem-map |
| punkpeye/awesome-mcp-servers | B1 | PARKED | K13 | meta-lista volcado (3.493 enlaces); ecosystem-map |
| showlab/awesome-gui-agent | B1 | PARKED | K13 | meta-lista (381d); ecosystem-map |
| tsinghuac3i/awesome-memory-for-agents | B1 | PARKED | K13 | meta-lista académica activa; ecosystem-map |
| agentops-ai/agentops | B10 | PARKED | K13 | 69d, 1 humano/90d: actividad en descenso; PARKED |
| likaixin2000/screenspot-pro-gui-grounding | B10 | PARKED | K13 | benchmark de grounding; va a benchmarks/models |
| openlit/openlit | B10 | PARKED | K13 | no sondeado (presupuesto); PARKED |
| thudm/agentbench | B10 | PARKED | K13 | no sondeado (presupuesto); PARKED |
| traceloop/openllmetry | B10 | PARKED | K13 | 23d; instrumentación OTel; PARKED |
| ukgovernmentbeis/inspect_ai | B10 | PARKED | K13 | framework de evals (UK AISI), muy activo; PARKED |
| ggml-org/llama.cpp | B11 | PARKED | K13 | runtime local; va a models.json |
| ollama/ollama | B11 | PARKED | K13 | runtime local; va a models.json |
| paddlepaddle/paddleocr | B11 | PARKED | K13 | OCR activo; va a models.json |
| rapidai/rapidocr | B11 | PARKED | K13 | OCR ONNX CPU activo; va a models.json (OCR local) |
| anthropics/anthropic-quickstarts | B2 | PARKED | K13 | computer-use-demo = contenedor Linux (W4); referencia de API, no componente; PARKED |
| bytedance/ui-tars-desktop | B2 | PARKED | K13 | 63d, 1 humano/90d; app Electron atada a modelos UI-TARS; PARKED |
| hkuds/nanobot | B2 | PARKED | K13 | 383k LOC, activo; agente genérico sin capa Windows; PARKED |
| openai/openai-cua-sample-app | B2 | PARKED | K13 | demo de API CUA de OpenAI; PARKED |
| showlab/showui | B2 | PARKED | K13 | sin sonda (fallo de clon) o fuera de cupo |
| autohotkey/autohotkey | B3 | PARKED | K13 | GPL, activo; scripting, no agente; PARKED |
| bobotig/python-mss | B3 | PARKED | K13 | activo, CI Windows; librería de captura; PARKED como dependencia |
| flaui/flaui | B3 | PARKED | K13 | .NET UIA maduro (20d) pero sin tests/CI; PARKED como alternativa a uiautomation si el stack fuese .NET |
| microsoft/playwright | B3 | PARKED | K13 | substrato de playwright-mcp; PARKED |
| moses-palmer/pynput | B3 | PARKED | K13 | 113d, 1 autor; PARKED |
| pywinauto/pywinauto | B3 | PARKED | K13 | 106d, 1 autor; dependencia de UFO; PARKED |
| ra1nty/dxcam | B3 | PARKED | K13 | 168d, 1 autor; captura DirectX rápida; PARKED |
| unclecode/crawl4ai | B3 | PARKED | K13 | crawler, no agente; Docker-céntrico; PARKED para research |
| agno-agi/agno | B4 | PARKED | K13 | 944k LOC, activo; PARKED |
| all-hands-ai/openhands | B4 | PARKED | K13 | coding agent Docker-céntrico; muy activo; PARKED para CODING AGENT |
| camel-ai/camel | B4 | PARKED | K13 | activo; orientado a investigación; PARKED |
| crewaiinc/crewai | B4 | PARKED | K13 | licencia OTHER (verificar), 323k LOC; PARKED |
| google/adk-python | B4 | PARKED | K13 | activo pero centrado en Gemini/Google Cloud; PARKED |
| huggingface/smolagents | B4 | PARKED | K13 | 54d sustantivo, 2 humanos; PARKED |
| kyegomez/swarms | B4 | PARKED | K13 | activo pero README con claims sin evidencia; no evaluado a fondo por presupuesto; PARKED |
| mastra-ai/mastra | B4 | PARKED | K13 | TS, licencia OTHER, 654k LOC; PARKED |
| langchain-ai/open_deep_research | B5 | PARKED | K13 | 23d, bus 1.0; PARKED (alternativa LangGraph a gpt-researcher) |
| mendableai/firecrawl | B5 | PARKED | K13 | AGPL, activo; capa de scraping; PARKED |
| searxng/searxng | B5 | PARKED | K13 | AGPL; metabuscador autohospedable (Docker); PARKED para research local |
| doobidoo/mcp-memory-service | B6 | PARKED | K13 | activo, bus 0.82, 216k LOC; PARKED (alternativa MCP) |
| khoj-ai/khoj | B6 | PARKED | K13 | AGPL, 31d; asistente personal con memoria; PARKED |
| langchain-ai/langmem | B6 | PARKED | K13 | 1 humano, 7 tests; solo tiene sentido con LangGraph; PARKED |
| memmachine/memmachine | B6 | PARKED | K13 | 7 commits/90d; PARKED |
| memtensor/memos | B6 | PARKED | K13 | activo, 412k LOC; PARKED |
| modelscope/memoryscope | B6 | PARKED | K13 | bus 0.9; PARKED |
| topoteretes/cognee | B6 | PARKED | K13 | activo, 372k LOC, Docker-céntrico; PARKED |
| vectorize-io/hindsight | B6 | PARKED | K13 | 674k LOC; PARKED |
| github/github-mcp-server | B7 | PARKED | K13 | oficial, activo; herramienta específica; PARKED |
| hoophq/mcpproxy | B7 | PARKED | K13 | 27d, 1 autor, 48 tests; gateway HTTP con OAuth; PARKED |
| kphatak001/mcpfw | B7 | PARKED | K13 | 110d, 0 humanos/90d; PARKED |
| microsoft/agent-governance-toolkit | B7 | PARKED | K13 | 691k LOC, activo (Microsoft); políticas empresariales; PARKED |
| modelcontextprotocol/python-sdk | B7 | PARKED | K13 | SDK oficial (base de FastMCP); PARKED |
| niradler/fast-mcp-gateway | B7 | PARKED | K13 | 73d; admin API sin auth por defecto (README); PARKED |
| sparfenyuk/mcp-proxy | B7 | PARKED | K13 | puente de transporte sin seguridad; 111d; PARKED |
| sushank05/mcp-doorman | B7 | PARKED | K13 | 0 stars, 1 autor, 56d, 7 tests; diseño completo (policy+redaction+pinning+elicitation); PARKED como alternativa TS a mcpgate |
| affaan-m/everything-claude-code | B8 | PARKED | K13 | activo (13 humanos); colección amplia; PARKED |
| anthropics/skills | B8 | PARKED | K13 | skills oficiales (documentos); referencia de formato; PARKED |
| bmad-code-org/bmad-method | B8 | PARKED | K13 | activo, bus 0.83; metodología por prompts sin evaluación; PARKED |
| davila7/claude-code-templates | B8 | PARKED | K13 | activo; catálogo de plantillas; PARKED |
| hesreallyhim/awesome-claude-code | B8 | PARKED | K13 | meta-lista activa; va a ecosystem-map |
| stevesolun/ctx | B8 | PARKED | K13 | activo (60 commits) pero 396k LOC y telemetría (102 hits); no evaluado a fondo; PARKED |
| superclaude-org/superclaude_framework | B8 | PARKED | K13 | 42d sustantivo, 2 humanos, postinstall; claims de 'framework' sin evaluación; PARKED con HYPE_FLAG leve |
| convira/convira-sandbox | B9 | PARKED | K13 | 25d, AppContainer+Job Objects en Windows con CI; bus 0.92; PARKED (alternativa a sandboxrs) |
| guardrails-ai/guardrails | B9 | PARKED | K13 | activo; validación de salidas; PARKED |
| humanlayer/humanlayer | B9 | PARKED | K13 | 238d sustantivo, 1 humano; HITL por API; PARKED |
| nvidia/nemo-guardrails | B9 | PARKED | K13 | activo; guardrails conversacionales, no de tools; PARKED |
| openai/codex | B9 | PARKED | K13 | referencia de sandbox Windows (restricted token + usuarios locales); evidencia en cards de B9; PARKED |
