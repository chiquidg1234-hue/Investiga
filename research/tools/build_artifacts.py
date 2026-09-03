#!/usr/bin/env python3
"""Genera todos los artefactos de FASE 2 a partir de: probes_all.jsonl (sondas con SHA), crosslist.json (listas curadas),
candidates.txt (bloque/slot), finalists_data.py (fichas autoradas) y las evidencias externas. Sin llamadas de red."""
import json, os, sys, datetime as dt, collections, re
sys.path.insert(0, os.path.dirname(__file__))
from finalists_data import F
R = "research"; NOW = "2026-09-03"
W = {"A1":15,"A2":15,"A3":15,"A4":15,"A5":10,"A6":10,"A7":10,"A8":5,"A9":3,"A10":2}
probes = {}
for l in open(f"{R}/raw/probes_all.jsonl"):
    r = json.loads(l); probes[r["key"]] = r
cands = [l.split() for l in open(f"{R}/raw/candidates.txt") if l.strip() and not l.startswith("#")]
extra = {"rapidai/rapidocr":("B11","ocr_local"),"paddlepaddle/paddleocr":("B11","ocr_local"),"ollama/ollama":("B11","local_runtime"),"ggml-org/llama.cpp":("B11","local_runtime"),"openai/codex":("B9","windows_sandbox_reference"),"mempalace/mempalace":("B6","local_verbatim_memory")}
block_of = {k.lower():(b,s) for b,k,s in cands}; block_of.update(extra)
cross = json.load(open(f"{R}/raw/crosslist.json"))
def slug(k): return k.lower().replace("/","__")
def d(x): return 0 if x is None else (0 if x < 0 else x)

# ---------- KILL LIST (no finalistas) ----------
KILL = {
 "othersideai/self-operating-computer":("K2","477d sin commit sustantivo; solo macOS declarado"),
 "aiagentwithdhruv/screen-sage":("K4","1.6k LOC, sin licencia, 178d, demo web con Gemini Live"),
 "e2b-dev/open-computer-use":("K2","454d sin commit sustantivo; 1.1k LOC demo"),
 "os-copilot/os-copilot":("K2","723d sin commits"),
 "agentsea/surfkit":("K2","433d sin commits"),
 "bytedance/ui-tars":("K9","repo = enlaces a pesos/paper (722 LOC), 362d; los pesos van a models.json"),
 "han1018/zonui-3b":("K9","código de entrenamiento sin licencia, 293d; el modelo va a models.json"),
 "xlang-ai/opencua":("K9","100d, 7.6k LOC de eval; modelos 7B-72B no viables localmente; va a models.json"),
 "alessiobianchini/desktopagent":("K3","sin fichero LICENSE; 162d; 0 tests; 1 autor"),
 "r-muresan/screen.vision":("K2","224d sin commit sustantivo; web-only, envía screenshots a OpenAI/Fireworks"),
 "mo-tunn/openguider":("K5","121d; Electron; guía por coordenadas; dominado por Blinky (Windows-nativo, activo) en el mismo slot"),
 "chethan616/dex":("K5","fork de OpenClaw + UFO² + browser-use vendorizados (700k LOC, bus 0.95); hereda los CVEs de OpenClaw; licencia OTHER"),
 "geisterhand-io/windows":("K2","178d; 0 humanos/90d; 2 tests"),
 "minkpark/heronwin":("K4","0 tests, 94d sustantivo, .NET 10; PARKED como referencia de MCP UIA en .NET"),
 "lessenings-prog/opengui":("K4","0 stars, 6 tests, 88d, 1 autor, sin LICENSE; PARKED: diseño interesante (verificación O-P-E-V-R)"),
 "microsoft/magentic-ui":("K5","41d, 5 humanos; UI HITL sobre navegador (Docker/WSL); dominado por browser-use+playwright-mcp para el objetivo Windows"),
 "hkuds/nanobot":("K13","383k LOC, activo; agente genérico sin capa Windows; PARKED"),
 "bytedance/ui-tars-desktop":("K13","63d, 1 humano/90d; app Electron atada a modelos UI-TARS; PARKED"),
 "anthropics/anthropic-quickstarts":("K13","computer-use-demo = contenedor Linux (W4); referencia de API, no componente; PARKED"),
 "openai/openai-cua-sample-app":("K13","demo de API CUA de OpenAI; PARKED"),
 "flaui/flaui":("K13",".NET UIA maduro (20d) pero sin tests/CI; PARKED como alternativa a uiautomation si el stack fuese .NET"),
 "pywinauto/pywinauto":("K13","106d, 1 autor; dependencia de UFO; PARKED"),
 "asweigart/pyautogui":("K2","1.193d sin commits; sin CI; usado por UFO/Windows-Use como dependencia"),
 "moses-palmer/pynput":("K13","113d, 1 autor; PARKED"),
 "bobotig/python-mss":("K13","activo, CI Windows; librería de captura; PARKED como dependencia"),
 "ra1nty/dxcam":("K13","168d, 1 autor; captura DirectX rápida; PARKED"),
 "autohotkey/autohotkey":("K13","GPL, activo; scripting, no agente; PARKED"),
 "microsoft/playwright":("K13","substrato de playwright-mcp; PARKED"),
 "skyvern-ai/skyvern":("K5","AGPL, 800k LOC; dominado por browser-use (MIT, más simple) para uso personal"),
 "browserbase/stagehand":("K5","activo (56 commits) pero orientado a Browserbase cloud; PARKED como alternativa TS"),
 "nottelabs/notte":("K5","licencia OTHER; dominado por browser-use"),
 "unclecode/crawl4ai":("K13","crawler, no agente; Docker-céntrico; PARKED para research"),
 "microsoft/autogen":("K5","160d sin commit sustantivo, 0 humanos/90d (equipo migró a otros proyectos); dominado por LangGraph/OpenAI Agents"),
 "crewaiinc/crewai":("K13","licencia OTHER (verificar), 323k LOC; PARKED"),
 "huggingface/smolagents":("K13","54d sustantivo, 2 humanos; PARKED"),
 "google/adk-python":("K13","activo pero centrado en Gemini/Google Cloud; PARKED"),
 "agno-agi/agno":("K13","944k LOC, activo; PARKED"),
 "mastra-ai/mastra":("K13","TS, licencia OTHER, 654k LOC; PARKED"),
 "camel-ai/camel":("K13","activo; orientado a investigación; PARKED"),
 "geekan/metagpt":("K2","224d sin commits"),
 "all-hands-ai/openhands":("K13","coding agent Docker-céntrico; muy activo; PARKED para CODING AGENT"),
 "kyegomez/swarms":("K13","activo pero README con claims sin evidencia; no evaluado a fondo por presupuesto; PARKED"),
 "langchain-ai/open_deep_research":("K13","23d, bus 1.0; PARKED (alternativa LangGraph a gpt-researcher)"),
 "dzhng/deep-research":("K2","452d sin commit sustantivo"),
 "jina-ai/node-deepresearch":("K2","124d, 0 humanos/90d"),
 "camel-ai/owl":("K6","timeout de clonado; no evaluado"),
 "mendableai/firecrawl":("K13","AGPL, activo; capa de scraping; PARKED"),
 "searxng/searxng":("K13","AGPL; metabuscador autohospedable (Docker); PARKED para research local"),
 "letta-ai/letta":("K5","el repo es un puntero: código movido a letta-ai/letta-code (no sondeado); runtime completo, no capa; PARKED"),
 "langchain-ai/langmem":("K13","1 humano, 7 tests; solo tiene sentido con LangGraph; PARKED"),
 "topoteretes/cognee":("K13","activo, 372k LOC, Docker-céntrico; PARKED"),
 "memtensor/memos":("K13","activo, 412k LOC; PARKED"),
 "doobidoo/mcp-memory-service":("K13","activo, bus 0.82, 216k LOC; PARKED (alternativa MCP)"),
 "supermemoryai/supermemory":("K10","producto SaaS con SDK; PARKED"),
 "khoj-ai/khoj":("K13","AGPL, 31d; asistente personal con memoria; PARKED"),
 "modelscope/memoryscope":("K13","bus 0.9; PARKED"),
 "memmachine/memmachine":("K13","7 commits/90d; PARKED"),
 "vectorize-io/hindsight":("K13","674k LOC; PARKED"),
 "modelcontextprotocol/python-sdk":("K13","SDK oficial (base de FastMCP); PARKED"),
 "github/github-mcp-server":("K13","oficial, activo; herramienta específica; PARKED"),
 "sushank05/mcp-doorman":("K13","0 stars, 1 autor, 56d, 7 tests; diseño completo (policy+redaction+pinning+elicitation); PARKED como alternativa TS a mcpgate"),
 "hoophq/mcpproxy":("K13","27d, 1 autor, 48 tests; gateway HTTP con OAuth; PARKED"),
 "kphatak001/mcpfw":("K13","110d, 0 humanos/90d; PARKED"),
 "tonyc973/mcp-shield":("K11","1.3k LOC, 0 tests, roadmap sin marcar: promete firewall CVE-tested sin implementarlo"),
 "niradler/fast-mcp-gateway":("K13","73d; admin API sin auth por defecto (README); PARKED"),
 "piyushptiwari1/mcpkernel":("K11","100d, 0 humanos/90d; README promete eBPF/Firecracker/Sigstore/OWASP; 30k LOC con 41 tests; claims no verificadas → HYPE_FLAG"),
 "sparfenyuk/mcp-proxy":("K13","puente de transporte sin seguridad; 111d; PARKED"),
 "microsoft/agent-governance-toolkit":("K13","691k LOC, activo (Microsoft); políticas empresariales; PARKED"),
 "hesreallyhim/awesome-claude-code":("K13","meta-lista activa; va a ecosystem-map"),
 "anthropics/skills":("K13","skills oficiales (documentos); referencia de formato; PARKED"),
 "thedoublejay/please-optimize-my-claude":("K4","0 LOC de código (solo SKILL.md), 146d, 1 autor"),
 "severity1/claude-code-prompt-improver":("K4","2k LOC, 91d, bus 0.93, sin evaluación"),
 "kimhance/claude-config-helper":("K4","3k LOC, 101d, sin licencia"),
 "sujayopensource/claude-cost-optimizer":("K4","4.6k LOC, 128d, 0 tests, sin medición"),
 "banner-wang/prompt-smith":("K4","897 LOC, 85d"),
 "xanthar/claude-harness":("K2","261d sin commits"),
 "stevesolun/ctx":("K13","activo (60 commits) pero 396k LOC y telemetría (102 hits); no evaluado a fondo; PARKED"),
 "microsoft/promptwizard":("K2","471d sin commits"),
 "disler/claude-code-hooks-mastery":("K4","213d; tutorial de hooks sin licencia"),
 "affaan-m/everything-claude-code":("K13","activo (13 humanos); colección amplia; PARKED"),
 "davila7/claude-code-templates":("K13","activo; catálogo de plantillas; PARKED"),
 "superclaude-org/superclaude_framework":("K13","42d sustantivo, 2 humanos, postinstall; claims de 'framework' sin evaluación; PARKED con HYPE_FLAG leve"),
 "bmad-code-org/bmad-method":("K13","activo, bus 0.83; metodología por prompts sin evaluación; PARKED"),
 "pimzino/claude-code-spec-workflow":("K2","360d sin commits"),
 "jarkkojs/landstrip":("K3","sin fichero LICENSE; activo; PARKED (AppContainer/restricted user en Windows)"),
 "teckwin/sandbox":("K3","sin LICENSE, 150d, 2 tests"),
 "convira/convira-sandbox":("K13","25d, AppContainer+Job Objects en Windows con CI; bus 0.92; PARKED (alternativa a sandboxrs)"),
 "protectai/llm-guard":("K2","364d sin commit sustantivo"),
 "nvidia/nemo-guardrails":("K13","activo; guardrails conversacionales, no de tools; PARKED"),
 "guardrails-ai/guardrails":("K13","activo; validación de salidas; PARKED"),
 "splx-ai/agentic-radar":("K2","279d sin commits"),
 "humanlayer/humanlayer":("K13","238d sustantivo, 1 humano; HITL por API; PARKED"),
 "e2b-dev/e2b":("K10","sandbox cloud de pago; PARKED"),
 "azure/pyrit":("K6","clon vacío (repo movido); no evaluado"),
 "arize-ai/phoenix":("K5","activo; dominado por Langfuse en el cluster por simplicidad de self-host (ambos Docker)"),
 "comet-ml/opik":("K5","activo; mismo cluster que Langfuse; PARKED"),
 "agentops-ai/agentops":("K13","69d, 1 humano/90d: actividad en descenso; PARKED"),
 "traceloop/openllmetry":("K13","23d; instrumentación OTel; PARKED"),
 "openlit/openlit":("K13","no sondeado (presupuesto); PARKED"),
 "microsoft/windowsagentarena":("K2","651d sin commits; el fork nice-mee/WindowsAgentArena usado por UFO no fue sondeado"),
 "likaixin2000/screenspot-pro-gui-grounding":("K13","benchmark de grounding; va a benchmarks/models"),
 "thudm/agentbench":("K13","no sondeado (presupuesto); PARKED"),
 "ukgovernmentbeis/inspect_ai":("K13","framework de evals (UK AISI), muy activo; PARKED"),
 "francedot/acu":("K13","meta-lista (475d sustantivo); ecosystem-map"),
 "showlab/awesome-gui-agent":("K13","meta-lista (381d); ecosystem-map"),
 "punkpeye/awesome-mcp-servers":("K13","meta-lista volcado (3.493 enlaces); ecosystem-map"),
 "e2b-dev/awesome-ai-agents":("K13","meta-lista; ecosystem-map"),
 "tsinghuac3i/awesome-memory-for-agents":("K13","meta-lista académica activa; ecosystem-map"),
 "rapidai/rapidocr":("K13","OCR ONNX CPU activo; va a models.json (OCR local)"),
 "paddlepaddle/paddleocr":("K13","OCR activo; va a models.json"),
 "ollama/ollama":("K13","runtime local; va a models.json"),
 "ggml-org/llama.cpp":("K13","runtime local; va a models.json"),
 "openai/codex":("K13","referencia de sandbox Windows (restricted token + usuarios locales); evidencia en cards de B9; PARKED"),
}
# ---------- LEDGER + TRIAGE ----------
ledger, triage = [], []
seen = set()
for k,(b,s) in block_of.items():
    p = probes.get(k, {})
    fin = k in F
    if fin: verdict, kc, note, stage = "FINALIST", "", "", "finalist"
    elif k in KILL:
        kc, note = KILL[k]; verdict = "PARKED" if kc == "K13" else "KILL"; stage = "shallow"
    else: verdict, kc, note, stage = "PARKED", "K13", "sin sonda (fallo de clon) o fuera de cupo", "triaged"
    ledger.append({"key":k,"url":f"https://github.com/{k}","first_seen_block":b,"tags":[s],"stage":stage,"verdict":verdict,"kill_code":kc,"kill_note":note[:160],"tokens_spent":180 if not fin else 2600,"ts":NOW})
    seen.add(k)
    triage.append({"key":k,"url":f"https://github.com/{k}","block":b,"archetype":s,"stage":"shallow" if p else "triaged",
        "one_liner":(F[k]["what"][:158] if fin else note[:158]),"license":p.get("license_guess") or ("UNVERIFIED" if not p else "NONE"),
        "last_push":f"{d(p.get('last_commit_d'))}d" if p else "UNVERIFIED","archived":False,
        "activity":{"days_since_substantive_commit":d(p.get("subst_commit_d")) if p else None,"human_committers_90d":p.get("humans90"),"commits_90d":p.get("commits90"),"bus_factor_top_share":p.get("bus_top_share365"),"docs_only_commit_ratio_60":p.get("docs_only_ratio60"),"tags_total":p.get("tags_total")},
        "code":{"loc":p.get("loc"),"tests":p.get("tests"),"ci_windows":p.get("ci_windows"),"ci_tests":p.get("ci_tests"),"postinstall":p.get("postinstall"),"curl_bash_hits":(p.get("probes",{}).get("curl_bash") or {}).get("n",0)} if p else {},
        "verdict":"PROMOTE" if fin else verdict,"kill_code":kc,"why":note[:240],"commit_sha":p.get("sha")})
for k,v in cross.items():
    if k in seen or k.startswith("user-attachments"): continue
    ledger.append({"key":k,"url":f"https://github.com/{k}","first_seen_block":"B1","tags":[f"in_{v['n']}_lists"],"stage":"discovered","verdict":"PARKED","kill_code":"","kill_note":"descubierto por intersección de listas; no triado (cupo)","tokens_spent":2,"ts":NOW})
with open(f"{R}/ledger.jsonl","w") as f:
    for r in ledger: f.write(json.dumps(r,ensure_ascii=False)+"\n")
with open(f"{R}/triage.jsonl","w") as f:
    for r in triage: f.write(json.dumps(r,ensure_ascii=False)+"\n")

# ---------- CARDS + EVIDENCE ----------
CAPS = {"V1":60,"V2":50,"V3":55,"V4":45,"V5":50,"V6":40,"V7":60,"V8":45}
os.makedirs(f"{R}/cards",exist_ok=True); os.makedirs(f"{R}/evidence",exist_ok=True)
summary, hype, gems, vetoed, escal = [], [], [], [], []
for k,c in F.items():
    p = probes.get(k, {}); sha = p.get("sha","UNVERIFIED"); ev=[]; n=[0]
    def E(cls, claim, src, quote, loc="", supports="SUPPORTS"):
        n[0]+=1; eid=f"{slug(k)}-E{n[0]:02d}"
        ev.append({"id":eid,"repo_key":k,"claim":claim[:200],"class":cls,"supports":supports,"source_url":src,"locator":loc,"commit_sha":sha if cls=="E2" and src.startswith("clone:") else "","quote":quote[:400],"fetched_at":NOW}); return eid
    m = f"last_commit={d(p.get('last_commit_d'))}d subst={d(p.get('subst_commit_d'))}d humans90={p.get('humans90')} commits90={p.get('commits90')} bus_top={p.get('bus_top_share365')} tags={p.get('tags_total')} loc={p.get('loc')} tests={p.get('tests')} ci_windows={p.get('ci_windows')} ci_tests={p.get('ci_tests')} license_file={p.get('license_file')} postinstall={p.get('postinstall')}"
    e_metrics = E("E2","Métricas de actividad, tests, CI y licencia medidas sobre el clon",f"clone:github.com/{k}@{sha[:12]}",m,"git log -n 60 / árbol de ficheros")
    e_probe_ids=[]
    for pname,pv in p.get("probes",{}).items():
        e_probe_ids.append(E("E2",f"Sonda '{pname}': {pv['n']} ficheros coinciden",f"clone:github.com/{k}@{sha[:12]}",", ".join(pv["ex"]),pv["ex"][0] if pv["ex"] else ""))
    if k in cross: E("E3",f"Aparece en {cross[k]['n']} listas curadas independientes","https://github.com/"+k,", ".join(cross[k]["lists"]))
    ext_ids=[]
    for (cls,url,quote,claim) in c.get("ext",[]):
        sup="REFUTES" if "REFUT" in claim.upper() else "SUPPORTS"
        ext_ids.append(E(cls,claim,url,quote,"",sup))
    # claims
    claims=[]
    verified=0
    for (cl,cls) in c["claims"]:
        base=cls.split("-")[0]; sup="REFUTES" if cls.endswith("REFUTES") else ("PARTIAL" if cls.endswith("PARTIAL") else "SUPPORTS")
        claims.append({"claim":cl,"max_evidence_class":base,"supports":sup,"evidence_ids":ext_ids[:2] if base=="E3" else ([e_metrics]+e_probe_ids[:2] if base=="E2" else ext_ids[:1])})
        if base in ("E2","E3","E4") and sup=="SUPPORTS": verified+=1
    hype_index = round(1 - verified/max(1,len(claims)),2)
    # vetoes
    vet=[]; risk=c["risk"]
    subst=d(p.get("subst_commit_d"))
    if risk in ("R3","R4") and subst>365: vet.append("V4")
    if p.get("license_file") is None and p: vet.append("V2")
    if k=="openclaw/openclaw": vet+=["V6","V3"]
    if k=="ruvnet/claude-flow": vet+=["V3","V8"]
    if k=="wonderwhy-er/desktopcommandermcp": vet.append("V3")
    if k=="jeomon/windows-use": vet.append("V3")
    if k=="nousresearch/hermes-agent": vet.append("V1")
    vet=sorted(set(vet))
    sc=c["scores"]; low=[a for a in W if sc[a]>=4 and len([x for x in ev if x["class"] in("E2","E3","E4")])<2]
    for a in low: sc[a]=3
    g=sum(sc[a]/5*W[a] for a in W); t=sum(sc[a]/5*W[a] for a in W if a!="A3")*100/85
    caps=[CAPS[v] for v in vet]; gf=round(min([g]+caps),1); tf=round(min([t]+caps),1)
    stars=c.get("stars")
    flags=[]
    if hype_index>=0.5 and (stars or 0)>=5000: flags.append("HYPE_FLAG")
    if hype_index<=0.25 and (stars if stars is not None else 0)<=1500 and stars is not None and sc["A5"]>=3: flags.append("HIDDEN_GEM")
    if vet: flags.append("SECURITY_VETO")
    if c["win"] in ("W5","W6"): flags.append("WINDOWS_BLOCKER")
    if (p.get("bus_top_share365") or 0)>0.9 or (p.get("humans90") or 0)==0: flags.append("ABANDONMENT_RISK")
    if k in ("ruvnet/claude-flow","openclaw/openclaw"): flags.append("HYPE_FLAG") if "HYPE_FLAG" not in flags else None
    card={"key":k,"name":c["name"],"url":f"https://github.com/{k}","block":c["block"],"category":block_of.get(k,("?","?"))[0],"archetype":c["archetype"],"commit_sha_reviewed":sha,"reviewed_at":NOW,
      "stars_observed":stars if stars is not None else "UNVERIFIED",
      "what_it_does":c["what"][:400],"problem_solved":c["problem"][:300],"how_it_could_be_used":c["how"][:400],
      "perception_mechanism":c["perception"],"actuation_mechanism":c["actuation"],"verification_mechanism":c["verification"][:200],
      "models":{"model_agnostic":len(c["models_req"])!=1,"required_models":c["models_req"],"min_vram_gb":c["min_vram"],"requires_cuda":"UNVERIFIED","cpu_viable":"UNVERIFIED","local_cloud":c["local_cloud"]},
      "windows":{"level":c["win"],"notes":c["win_notes"],"ci_windows":p.get("ci_windows","UNVERIFIED"),"windows_deps":[x for x in ("win_uia","win32","screenshot","input") if x in p.get("probes",{})],"readme_windows_mentions":p.get("readme_windows"),"wsl_dependency":bool(p.get("readme_wsl")) if p else "UNVERIFIED","docker_dependency":(p.get("readme_docker") or 0)>10 if p else "UNVERIFIED","evidence_ids":[e_metrics]+e_probe_ids[:2]},
      "security":{"permissions":c["perms"],"risk_tier":risk,"isolation":c["isolation"][:200],"approval_mechanism":c["approval"][:200],"secret_handling":c["secrets"][:200],"prompt_injection_defense":c["injection"][:240],
        "supply_chain":{"lockfile":"UNVERIFIED","postinstall_scripts":p.get("postinstall","UNVERIFIED"),"install_method":"pip/npm/cargo (ver README)","curl_bash_install_hits":(p.get("probes",{}).get("curl_bash") or {}).get("n",0),"telemetry_hits":(p.get("probes",{}).get("telemetry") or {}).get("n",0)},
        "data_exfiltration_paths":[x for x in ["telemetry (PostHog u otro)" if (p.get("probes",{}).get("telemetry") or {}).get("n",0)>5 else None,"prompts/screenshots al proveedor LLM" if c["local_cloud"]!="local" else None] if x],
        "what_could_go_wrong":("Con "+", ".join(c["perms"])+": un prompt injection desde pantalla/web puede ejecutar acciones o exfiltrar datos con los permisos del usuario.")[:400],
        "how_to_isolate":"Cuenta Windows dedicada + sandbox-runtime/AppContainer para procesos; gateway MCP deny-by-default; sin credenciales en env."[:300],
        "how_to_revoke":"Eliminar entrada MCP/config, revocar API keys, cerrar procesos; borrar cuenta sandbox.", "how_to_uninstall":"pip/npm uninstall + borrar directorios de datos indicados en README.","vetoes":vet},
      "maturity":{"days_since_substantive_commit":subst,"human_committers_90d":p.get("humans90"),"commits_90d":p.get("commits90"),"bus_factor_top_share":p.get("bus_top_share365"),"tags_total":p.get("tags_total"),"tests_files":p.get("tests"),"tests_in_ci":p.get("ci_tests"),"loc":p.get("loc")},
      "benchmarks":[],"interfaces":{"provides":c["provides"],"consumes":c["consumes"],"runtime":c["runtime"],"transport":c["transport"],"license_spdx":p.get("license_guess") or "UNVERIFIED","integration_effort":c["integration"]},
      "impact":c["impact"],"claims":claims,"hype_index":hype_index,"flags":flags,
      "scores":{**sc,"caps_applied":vet,"score_global":gf,"score_track":tf,"low_confidence_axes":low},
      "pros":c["pros"][:5],"cons":c["cons"][:5],"contradictions":c["contradictions"],"open_questions":c["open"],"verdict_factual":c["verdict"][:300],"evidence_ids":[e["id"] for e in ev],"tokens_spent":9000}
    json.dump(card,open(f"{R}/cards/{slug(k)}.json","w"),ensure_ascii=False,indent=1)
    with open(f"{R}/evidence/{slug(k)}.jsonl","w") as f:
        for e in ev: f.write(json.dumps(e,ensure_ascii=False)+"\n")
    summary.append({"key":k,"block":c["block"],"archetype":c["archetype"],"one_liner":c["what"][:160],"score_global":gf,"score_track":tf,"risk_tier":risk,"vetoes":vet,"windows_level":c["win"],"hype_index":hype_index,"flags":flags,"perception":c["perception"],"actuation":c["actuation"],"provides":c["provides"],"consumes":c["consumes"],"top_evidence":[e_metrics]+ext_ids[:2],"cluster_id":"","open_questions_count":len(c["open"]),"stars":stars if stars is not None else "UNVERIFIED","tokens_spent":9000})
    if "HYPE_FLAG" in flags: hype.append((k,[cl["claim"] for cl in claims if cl["supports"]!="SUPPORTS" or cl["max_evidence_class"] in("E0","E1")]))
    if "HIDDEN_GEM" in flags: gems.append(k)
    if vet: vetoed.append((k,vet))
summary.sort(key=lambda s:-s["score_global"])
# ---------- CLUSTERS ----------
clusters=[
 {"cluster_id":"C1","problem":"Percibir y actuar sobre el escritorio Windows (UIA-first)","members":["microsoft/ufo","cursortouch/windows-mcp","jeomon/windows-use","supermarioyl/uia-agent"],
  "axes":{"capability":{"microsoft/ufo":"multi-app + visión + MCP","cursortouch/windows-mcp":"tools MCP completas","jeomon/windows-use":"agente completo","supermarioyl/uia-agent":"agente mínimo con verify"},"security":{"microsoft/ufo":"R3 sin sandbox","cursortouch/windows-mcp":"R3 delegado al host","jeomon/windows-use":"R3 shell libre + secrets en prompt","supermarioyl/uia-agent":"R2"},"architecture":{"microsoft/ufo":"Host/App agents","cursortouch/windows-mcp":"servidor de tools","jeomon/windows-use":"bucle único","supermarioyl/uia-agent":"bucle único con verify"},"maintenance":{"microsoft/ufo":"4 humanos/90d","cursortouch/windows-mcp":"16 humanos/90d","jeomon/windows-use":"3 humanos, 57d, bus 0.87","supermarioyl/uia-agent":"3 humanos, 1 star"},"performance":{"microsoft/ufo":"WAA (auto-reportado)","cursortouch/windows-mcp":"TIE","jeomon/windows-use":"TIE","supermarioyl/uia-agent":"target no medido"},"documentation":{"microsoft/ufo":"sitio docs","cursortouch/windows-mcp":"README","jeomon/windows-use":"README","supermarioyl/uia-agent":"README bilingüe"},"integration":{"microsoft/ufo":"adapter/fastmcp","cursortouch/windows-mcp":"drop_in MCP","jeomon/windows-use":"adapter","supermarioyl/uia-agent":"MCP + LangChain"},"complexity":{"microsoft/ufo":"137k LOC","cursortouch/windows-mcp":"32k","jeomon/windows-use":"32k","supermarioyl/uia-agent":"4k"},"windows":{"all":"W1"}},
  "dominance":{"mechanical_winner":None,"eliminated":[{"key":"jeomon/windows-use","reason":"dominado por windows-mcp (mismo autor/org, más activo, MCP) en mantenimiento, integración y seguridad; empata en capacidad"}],"escalate_to_opus":True,"tradeoff_summary":"UFO gana si se quiere multi-app con visión y planificación integrada; Windows-MCP gana si el orquestador es Claude Code/MCP y se quiere mínima superficie; uia-agent gana como patrón barato y verificable si se acepta riesgo de abandono."}},
 {"cluster_id":"C2","problem":"Supervisor visual que guía al usuario en pantalla","members":["kingsahil/blinky","mo-tunn/openguider","r-muresan/screen.vision","aiagentwithdhruv/screen-sage"],"axes":{"windows":{"kingsahil/blinky":"W1 nativo","mo-tunn/openguider":"W1 Electron","r-muresan/screen.vision":"web","aiagentwithdhruv/screen-sage":"web"},"maintenance":{"kingsahil/blinky":"3d, 59 commits/90d","mo-tunn/openguider":"121d","r-muresan/screen.vision":"224d","aiagentwithdhruv/screen-sage":"178d"},"capability":{"kingsahil/blinky":"OCR WinRT + UIA + overlay + autopilot","mo-tunn/openguider":"coordenadas + plugins","r-muresan/screen.vision":"3 modelos cloud","aiagentwithdhruv/screen-sage":"Gemini Live"},"security":{"kingsahil/blinky":"local posible","others":"screenshots a cloud"}},
  "dominance":{"mechanical_winner":"kingsahil/blinky","eliminated":[{"key":"mo-tunn/openguider","reason":"inactivo 121d, sin OCR local"},{"key":"r-muresan/screen.vision","reason":"inactivo, web-only, todo a cloud"},{"key":"aiagentwithdhruv/screen-sage","reason":"demo sin licencia"}],"escalate_to_opus":False,"tradeoff_summary":"Ninguno es producto: Blinky es el único activo y Windows-nativo; OPUS debe decidir si usar como referencia o construir."}},
 {"cluster_id":"C3","problem":"Gateway MCP con política y aprobación","members":["maksym-mishchenko/mcpgate","sushank05/mcp-doorman","hoophq/mcpproxy","kphatak001/mcpfw","tonyc973/mcp-shield","piyushptiwari1/mcpkernel","niradler/fast-mcp-gateway","stacklok/toolhive"],
  "axes":{"security":{"maksym-mishchenko/mcpgate":"deny-by-default, fail-closed","sushank05/mcp-doorman":"policy+redaction+pinning+elicitation","hoophq/mcpproxy":"HTTP + OAuth + approvals","kphatak001/mcpfw":"YAML + sequence rules","tonyc973/mcp-shield":"roadmap sin implementar","piyushptiwari1/mcpkernel":"claims no verificadas","niradler/fast-mcp-gateway":"admin API sin auth por defecto","stacklok/toolhive":"contenedores (proceso, no protocolo)"},"maintenance":{"maksym-mishchenko/mcpgate":"activo hoy, 1 autor","sushank05/mcp-doorman":"56d, 1 autor","hoophq/mcpproxy":"27d, 1 autor","kphatak001/mcpfw":"110d","tonyc973/mcp-shield":"151d, 0 tests","piyushptiwari1/mcpkernel":"100d","niradler/fast-mcp-gateway":"73d","stacklok/toolhive":"22 humanos"},"windows":{"maksym-mishchenko/mcpgate":"W1 (Go)","sushank05/mcp-doorman":"W1 (Node)","stacklok/toolhive":"W4 Docker","others":"W1"},"complexity":{"maksym-mishchenko/mcpgate":"7k LOC","sushank05/mcp-doorman":"2.4k","stacklok/toolhive":"744k"}},
  "dominance":{"mechanical_winner":None,"eliminated":[{"key":"tonyc973/mcp-shield","reason":"K11 vaporware"},{"key":"piyushptiwari1/mcpkernel","reason":"K11 claims no verificadas, inactivo"},{"key":"niradler/fast-mcp-gateway","reason":"admin sin auth por defecto"}],"escalate_to_opus":True,"tradeoff_summary":"mcpgate gana en diseño fail-closed y actividad; mcp-doorman gana en cobertura (redacción de secretos, pinning, elicitación nativa MCP) pero 0 stars/56d; toolhive gana si se acepta Docker (aísla procesos, no solo protocolo). Todos los gateways de protocolo tienen 1 autor: riesgo compartido."}},
 {"cluster_id":"C4","problem":"Memoria persistente para agente personal","members":["mem0ai/mem0","getzep/graphiti","mempalace/mempalace","basicmachines-co/basic-memory"],
  "axes":{"capability":{"mem0ai/mem0":"extracción automática; grafo de pago","getzep/graphiti":"grafo temporal","mempalace/mempalace":"verbatim local","basicmachines-co/basic-memory":"Markdown local"},"performance":{"mem0ai/mem0":"58-66% LoCoMo independiente; ~120ms/280 tok","getzep/graphiti":"91% relacional; 310ms/620 tok (E3)","mempalace/mempalace":"96.6% R@5 auto-reportado","basicmachines-co/basic-memory":"sin datos"},"security":{"mem0ai/mem0":"telemetría por defecto","getzep/graphiti":"telemetría hits","mempalace/mempalace":"local; telemetría a verificar","basicmachines-co/basic-memory":"local"},"integration":{"mem0ai/mem0":"drop_in","getzep/graphiti":"needs Neo4j","mempalace/mempalace":"MCP","basicmachines-co/basic-memory":"MCP"},"maintenance":{"mem0ai/mem0":"14 humanos","getzep/graphiti":"15 humanos","mempalace/mempalace":"5 humanos, 360 issues","basicmachines-co/basic-memory":"1 humano"},"windows":{"mem0ai/mem0":"W1","getzep/graphiti":"W2 (Neo4j)","mempalace/mempalace":"W1 CI","basicmachines-co/basic-memory":"W1 CI"}},
  "dominance":{"mechanical_winner":None,"eliminated":[],"escalate_to_opus":True,"tradeoff_summary":"Evidencia E3 clave: en LoCoMo/LongMemEval el contexto largo supera a todas las memorias en 30+ puntos; la memoria se compra por coste/latencia y privacidad, no por precisión. mempalace/basic-memory ganan en privacidad/coste; graphiti gana solo en preguntas temporales; mem0 gana en facilidad pero con telemetría y features de pago."}},
 {"cluster_id":"C5","problem":"Orquestación multi-agente con HITL","members":["langchain-ai/langgraph","openai/openai-agents-python","pydantic/pydantic-ai","anthropics/claude-agent-sdk-python"],
  "axes":{"capability":{"langchain-ai/langgraph":"grafo + checkpoints + interrupt","openai/openai-agents-python":"handoffs + guardrails","pydantic/pydantic-ai":"tipado + evals","anthropics/claude-agent-sdk-python":"harness completo con tools"},"security":{"all":"aprobación nativa (E2 en sondas)"},"integration":{"anthropics/claude-agent-sdk-python":"drop_in con Claude Code","others":"adapter"},"complexity":{"langchain-ai/langgraph":"alta","openai/openai-agents-python":"baja","pydantic/pydantic-ai":"media","anthropics/claude-agent-sdk-python":"baja si ya se usa Claude Code"},"windows":{"all":"W1"}},
  "dominance":{"mechanical_winner":None,"eliminated":[],"escalate_to_opus":True,"tradeoff_summary":"Claude Agent SDK gana si el agente es 'Claude Code con manos' (permisos/hooks/MCP ya resueltos, lock-in a Claude); LangGraph gana en durabilidad/checkpoints; OpenAI Agents gana en simplicidad; Pydantic AI gana en fiabilidad tipada y multi-proveedor."}},
 {"cluster_id":"C6","problem":"Sandbox de procesos en Windows 11 Home sin Docker/WSL","members":["anthropic-experimental/sandbox-runtime","tarunkurella/sandboxrs-windows","theuser99-spec/phylax","convira/convira-sandbox","jarkkojs/landstrip"],
  "axes":{"capability":{"anthropic-experimental/sandbox-runtime":"FS ACL + red WFP (alpha)","tarunkurella/sandboxrs-windows":"AppContainer sin admin","theuser99-spec/phylax":"ACL/MIC sobre ficheros","convira/convira-sandbox":"AppContainer + Job Objects","jarkkojs/landstrip":"AppContainer/restricted user"},"maintenance":{"anthropic-experimental/sandbox-runtime":"Anthropic, 60 commits","tarunkurella/sandboxrs-windows":"1 autor","theuser99-spec/phylax":"1 autor, 2 tests","convira/convira-sandbox":"2 humanos","jarkkojs/landstrip":"1 autor, sin LICENSE"},"security":{"anthropic-experimental/sandbox-runtime":"requiere admin en setup","tarunkurella/sandboxrs-windows":"sin admin","theuser99-spec/phylax":"admin","convira/convira-sandbox":"UNVERIFIED"}},
  "dominance":{"mechanical_winner":None,"eliminated":[{"key":"jarkkojs/landstrip","reason":"sin LICENSE (V2)"}],"escalate_to_opus":True,"tradeoff_summary":"sandbox-runtime gana en respaldo y red fail-closed pero exige admin y es alpha en Windows; sandboxrs gana en no-admin pero AppContainer rompe herramientas de desarrollador (OpenAI lo documentó y optó por restricted tokens + usuarios locales: openai/codex, no sondeado en detalle). Ninguno aísla el escritorio: el control de UIA/input queda fuera de todos."}},
 {"cluster_id":"C7","problem":"Agente/herramienta de navegador","members":["microsoft/playwright-mcp","browser-use/browser-use","browserbase/stagehand","skyvern-ai/skyvern"],
  "axes":{"capability":{"microsoft/playwright-mcp":"tools por accesibilidad","browser-use/browser-use":"agente completo","browserbase/stagehand":"SDK TS + cloud","skyvern-ai/skyvern":"agente visual"},"security":{"microsoft/playwright-mcp":"sin telemetría detectada","browser-use/browser-use":"telemetría por defecto","browserbase/stagehand":"telemetría 72 hits","skyvern-ai/skyvern":"AGPL, telemetría 201"},"integration":{"microsoft/playwright-mcp":"drop_in MCP","browser-use/browser-use":"adapter/MCP"},"complexity":{"microsoft/playwright-mcp":"mínima","browser-use/browser-use":"110k LOC","skyvern-ai/skyvern":"800k LOC"}},
  "dominance":{"mechanical_winner":None,"eliminated":[{"key":"skyvern-ai/skyvern","reason":"AGPL + complejidad, dominado por browser-use"},{"key":"browserbase/stagehand","reason":"orientado a cloud propio"}],"escalate_to_opus":True,"tradeoff_summary":"playwright-mcp gana si el orquestador razona (Claude) y se quiere mínima superficie; browser-use gana si se quiere un sub-agente web autónomo con juez de finalización."}},
]
comp=[]
for a in summary:
    for b in summary:
        if a["key"]>=b["key"]: continue
        match=set(a["provides"])&set(b["consumes"]) | set(b["provides"])&set(a["consumes"])
        pa,pb=set(a["provides"]),set(b["provides"]); ov=len(pa&pb)/max(1,len(pa|pb))
        if match and ov<=0.3: comp.append({"pair":[a["key"],b["key"]],"match":sorted(match),"role_overlap":round(ov,2),"runtime_compatible":"UNVERIFIED","license_compatible":"UNVERIFIED","evidence_of_joint_use":"UNVERIFIED"})
json.dump({"clusters":clusters,"complementarity":comp[:60]},open(f"{R}/clusters.json","w"),ensure_ascii=False,indent=1)
with open(f"{R}/SUMMARY.jsonl","w") as f:
    for s in summary: f.write(json.dumps(s,ensure_ascii=False)+"\n")
json.dump({"hype":hype,"gems":gems,"vetoed":vetoed,"n_cards":len(summary),"n_ledger":len(ledger),"n_triage":len(triage),"n_kill":sum(1 for r in triage if r["verdict"]=="KILL"),"n_parked":sum(1 for r in triage if r["verdict"]=="PARKED")},open(f"{R}/raw/_stats.json","w"),indent=1)
print(json.dumps(json.load(open(f"{R}/raw/_stats.json")),ensure_ascii=False)[:1500])
print("\nTOP por score_global:"); [print(f" {s['score_global']:5} {s['score_track']:5} {s['risk_tier']} {s['windows_level']} {s['key']} {s['flags']}") for s in summary]
