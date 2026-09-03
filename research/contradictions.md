# Contradicciones no resueltas (para OPUS)

Formato: proyecto — contradicción. FABLE no resuelve; registra ambas fuentes (ver evidence/*.jsonl).

- **Leaderboards OSWorld-Verified** — Steel.dev (2026-05-28): Mythos Preview 85.4%, Fable 5 85.0%, Opus 4.8 83.4%; gentic.news (jun 2026): Mythos Preview 79.6%, Opus 4.8 83.4%; BenchLM (2026-09-02): Qwen3.8 Max 86.1% > Fable 5 85%. Difieren por harness, fecha y política de submisión. Ninguna fuente primaria (os-world.github.io) fue descargada.
- **Benchmarks de memoria** — Mem0 91.6-92.5% LoCoMo (vendor) vs 58-66% (independiente) vs 32-49% OSS en LongMemEval; Zep 84% → 58.44% (autocorrección) → 75.14% (réplica). Además: un modelo de contexto largo supera a todas las memorias en 30+ puntos en esos benchmarks (dreaming.press). Conclusión operativa para OPUS: la memoria se compra por coste/latencia/privacidad, no por precisión.
- **AppContainer como sandbox** — sandboxrs-windows/convira lo adoptan; OpenAI documenta por qué lo descartó para Codex (rompe workflows de desarrollador) y usa restricted tokens + usuarios locales con firewall (requiere admin). sandbox-runtime de Anthropic usa un enfoque similar al de OpenAI (usuario dedicado + WFP).
- **claude-flow/ruflo** — auditorías (issues #1425, #1482, #1660, AgentSeal) vs respuestas del mantenedor (v3.5.69-3.7.0-alpha): 5 de 6 gaps declarados remediados; AgentSeal corrigió su propio falso positivo (terminal_execute era un stub). Persisten: execSync con interpolación, --dangerously-skip-permissions hardcodeado, descripciones de tools.
- **Agent S** — README S3: 72.6% OSWorld (100 pasos + Best-of-N) vs Steel: S2+Claude 3.7 34.5% (50 pasos). No comparables.
- **OmniParser** — HF: 39.6 ScreenSpot-Pro; README: 39.5.
- **Blinky** — badge MIT en README; sin fichero LICENSE en el clon.
- **Phylax** — README 'zero telemetry'; sonda halla 15 ficheros con 'telemetry' (probablemente docs de compliance): UNVERIFIED.

## Por ficha

- **getzep/graphiti** — Zep 84% → 58.44% tras corrección; Mem0 replicó 58.44%; Zep rebate 75.14%.
- **kingsahil/blinky** — README muestra badge MIT pero el clon no contiene fichero LICENSE (license_file=None).
- **mem0ai/mem0** — Vendor: 91.6-92.5% LoCoMo; independientes: 58-66%; OSS en LongMemEval 32-49% vs 93.4% plataforma.
- **mempalace/mempalace** — Blogs citan 54.1k y 58.8k stars y v3.4.0/v3.9.0: crecimiento muy rápido en semanas.
- **microsoft/omniparser** — HF card dice 39.6 ScreenSpot-Pro; README dice 39.5.
- **ruvnet/claude-flow** — Auditoría AlphaSignal (v3.6.30) vs respuesta del mantenedor (v3.7.0-alpha): 5 de 6 gaps 'remediados'; tool descriptions siguen abiertas.
- **simular-ai/agent-s** — Leaderboard Steel.dev lista 'Agent S2 + Claude 3.7' en 34.5% (50 pasos) mientras README de S3 declara 72.6% (100 pasos, BoN): no comparables por configuración.
- **tarunkurella/sandboxrs-windows** — OpenAI (Codex) descartó AppContainer por incompatibilidad con workflows de desarrollador; sandboxrs lo adopta como mecanismo principal.
- **theuser99-spec/phylax** — README: 'zero telemetry'; sonda encontró 15 hits de 'telemetry' (probablemente docs/compliance): UNVERIFIED.
- **xlang-ai/osworld** — Steel.dev: Mythos Preview 85.4% (mayo 2026); gentic.news: 79.6% (junio 2026); BenchLM: Qwen3.8 Max 86.1% (sept 2026) — harness/versiones distintas.
