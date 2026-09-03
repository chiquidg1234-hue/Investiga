# Matriz Windows 11 (finalistas)

Niveles: W1 nativo · W2 +PowerShell/admin · W3 WSL · W4 Docker · W5 VM · W6 no recomendable. Fuente: fichas (windows.notes) + sondas (ci_windows, deps).

| key | nivel | CI windows-latest | deps nativas detectadas | nota |
|---|---|---|---|---|
| langchain-ai/langgraph | W1 | False | win32 | Python puro. |
| pydantic/pydantic-ai | W1 | False | win32,screenshot | Python puro. |
| openai/openai-agents-python | W1 | True | win32,input | CI windows-latest con tests. |
| microsoft/playwright-mcp | W1 | True | - | Node; CI windows-latest con tests; Docker opcional. |
| xlang-ai/osworld | W5 | False | win_uia,win32,screenshot,input | Requiere VMs (VMware/Docker); tareas Ubuntu; variante Windows en WAA (muerto: 651 días). |
| promptfoo/promptfoo | W1 | True | input | CI windows-latest. |
| anthropic-experimental/sandbox-runtime | W2 | True | win32 | Windows alpha: requiere instalación elevada (crea usuario srt-sandbox y filtros WFP); CI windows-latest con tests. |
| stanfordnlp/dspy | W1 | False | win32 | Python. |
| microsoft/ufo | W1 | False | win_uia,win32,screenshot,input | Deps con marcador sys_platform=='win32': pywin32, pywinauto, uiautomation, pyautogui. Sin job windows-latest en CI (ci=1, sin tests en CI). |
| jlowin/fastmcp | W1 | True | win_uia,win32,input | CI windows-latest. |
| browser-use/browser-use | W1 | True | input | CI windows-latest con tests. |
| anthropics/claude-agent-sdk-python | W1 | True | - | CI windows-latest con tests; requiere Claude Code CLI (Node). |
| modelcontextprotocol/servers | W1 | False | win32 | Node/Python. |
| langfuse/langfuse | W4 | False | - | Self-host = Docker Compose; SDK Python/JS nativo. |
| cursortouch/windows-mcp | W1 | True | win_uia,win32,screenshot,input | 189 menciones Windows en README; CI windows-latest con tests; deps uiautomation/pywin32. |
| stacklok/toolhive | W4 | False | screenshot | Contenedores → Docker Desktop en Windows; no aísla MCPs que necesitan el escritorio (Windows-MCP). |
| tarunkurella/sandboxrs-windows | W1 | True | - | Windows 11 / Server 2025; CI windows-latest con tests como usuario estándar. |
| trycua/cua | W2 | True | win_uia,win32,screenshot,input | Driver Windows nativo (win32: 35 hits, UIA: 19) + CI windows-latest; el sandbox completo requiere Docker/VM (W4/W5). 12 hits de curl/bash en |
| mempalace/mempalace | W1 | True | win32 | CI windows-latest con tests; Docker opcional. |
| yinkaisheng/python-uiautomation-for-windows | W1 | False | win_uia,win32,screenshot,input | Solo Windows. |
| ethz-spylab/agentdojo | W1 | False | win32 | Python. |
| ryoppippi/ccusage | W1 | True | - | Node; CI windows-latest. |
| mem0ai/mem0 | W1 | False | win32 | Python; vector store local (Qdrant/Chroma) posible. |
| getzep/graphiti | W2 | False | win32 | Requiere base de grafos (Neo4j Desktop en Windows o Docker). |
| invariantlabs-ai/mcp-scan | W1 | True | win32 | CI windows-latest. |
| maksym-mishchenko/mcpgate | W1 | False | - | Binario Go; sin CI Windows (no crítico). |
| assafelovic/gpt-researcher | W1 | False | screenshot | Python; Docker solo opcional (12 menciones). |
| supermarioyl/uia-agent | W1 | True | win_uia | Solo Windows por diseño; sesión interactiva; CI windows-latest con tests (12 tests). |
| basicmachines-co/basic-memory | W1 | True | win32 | CI windows-latest con tests. |
| simular-ai/agent-s | W2 | False | win_uia,win32,input | README: soporta Windows; usa pyautogui; requiere tesseract; sin CI Windows; solo 1 test. |
| mediar-ai/screenpipe | W1 | True | win_uia,win32,screenshot,input | Rust nativo, CI windows-latest, UIA/win32 hits; instalador Windows. |
| microsoft/omniparser | W4 | False | win_uia,input | OmniTool controla una VM Windows 11 (Docker/VM); el parser en sí corre nativo (PyTorch) en cualquier SO. Latencia publicada 0.8 s/frame en R |
| jeomon/windows-use | W1 | True | win_uia,win32,screenshot,input | Windows 10 build 17763+ / 11; CI windows-latest con tests. |
| wonderwhy-er/desktopcommandermcp | W1 | False | - | Node; 13 menciones Windows. |
| nousresearch/hermes-agent | W2 | True | win32,screenshot,input | CI windows-latest; 15 menciones Windows; 35 hits curl/bash (instalador). |
| bytedance/deer-flow | W3 | False | win32,input | Guías Docker/WSL; sin CI Windows. |
| obra/superpowers | W1 | False | - | Markdown/scripts. |
| kingsahil/blinky | W1 | False | win_uia,win32,screenshot,input | Windows-first (WinRT OCR, dxcam, pywinauto); Docker solo para SearXNG opcional. |
| theuser99-spec/phylax | W1 | True | win32,screenshot | Windows-first; CI windows-latest. |
| openclaw/openclaw | W2 | True | screenshot,input | CI windows-latest; postinstall script en package.json; 6 instaladores. |
| ruvnet/claude-flow | W2 | True | - | CI windows-latest. |

**Hallazgo transversal:** ningún sandbox encontrado (sandbox-runtime, AppContainer, ACL) aísla el escritorio: UIA e inyección de input siguen disponibles para el proceso del agente. El aislamiento del escritorio solo existe vía VM (OSWorld/WAA/cua) = W5.
