# Preguntas abiertas / no verificado

## Transversales

- Stars solo verificadas para 17 finalistas (WebFetch); el resto 'UNVERIFIED' (la API de GitHub estaba bloqueada por el proxy de la sesión).
- Lockfiles, releases firmados y advisories por repo: NO auditados (sin acceso a OSV/GitHub Advisory desde el entorno). Solo se registran hits de postinstall y curl|bash.
- Latencia real de cualquier modelo local en i7-1065G7 + MX330: NO medida (prohibido instalar). Las VRAM de models.json son estimaciones mecánicas int4.
- Multi-monitor/DPI en Windows-MCP, Windows-Use, UFO, uia-agent: NO verificado.
- Embeddings locales: slot no investigado por presupuesto.
- Fuentes no anglófonas: solo uia-agent (README chino) y laboratorios CN vía papers; no se hizo búsqueda dedicada en Zhihu/CSDN.
- letta-ai/letta-code (código real de Letta) no sondeado; Letta queda como PARKED.
- nice-mee/WindowsAgentArena (fork vivo usado por UFO) no sondeado.

## Por ficha

- **anthropic-experimental/sandbox-runtime** — Compatibilidad con Windows 11 Home (no requiere Windows Sandbox: OK).
- **assafelovic/gpt-researcher** — Telemetría por defecto.
- **browser-use/browser-use** — Qué campos exactos envía la telemetría.
- **cursortouch/windows-mcp** — Comportamiento con DPI/multi-monitor no verificado.
- **invariantlabs-ai/mcp-scan** — Modo local puro.
- **jeomon/windows-use** — Tasa de éxito real: sin benchmark.
- **kingsahil/blinky** — Latencia real del bucle en hardware i7-1065G7/MX330.
- **maksym-mishchenko/mcpgate** — Stars y adopción (no verificadas).
- **mediar-ai/screenpipe** — Términos exactos de la licencia; telemetría por defecto.
- **mem0ai/mem0** — Configuración exacta de los reruns independientes.
- **mempalace/mempalace** — ¿Telemetría por defecto?
- **mempalace/mempalace** — Verificación independiente del 96.6%.
- **microsoft/omniparser** — Licencia efectiva de los pesos YOLOv8 afinados (Ultralytics es AGPL-3.0).
- **microsoft/ufo** — Cifras actuales de éxito en WAA para UFO³ (README enlaza a fork nice-mee/WindowsAgentArena; no verificado el número).
- **nousresearch/hermes-agent** — ¿Existe vía de instalación sin script remoto?
- **nousresearch/hermes-agent** — ¿Aprobación de acciones por defecto?
- **openai/openai-agents-python** — Destino por defecto del tracing.
- **openclaw/openclaw** — Estado de parches en la versión actual.
- **promptfoo/promptfoo** — Telemetría por defecto.
- **ruvnet/claude-flow** — Estado real de las remediaciones en la versión estable.
- **simular-ai/agent-s** — Reproducción independiente del 72.6%.
- **supermarioyl/uia-agent** — BENCHMARK.md declara que el 83% es un target no medido: confirmar si ya hay medición real.
- **tarunkurella/sandboxrs-windows** — Compatibilidad con apps GUI dentro del AppContainer.
- **theuser99-spec/phylax** — Auditoría externa.
- **trycua/cua** — Stars no verificadas; comportamiento del driver Windows 'background' con apps DirectX.
- **wonderwhy-er/desktopcommandermcp** — Qué hace el postinstall.
