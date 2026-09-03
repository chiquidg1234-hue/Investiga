#!/usr/bin/env python3
"""Herramientas de investigación FASE 2 (solo lectura; nunca ejecuta código de terceros).
  NOTA: en este entorno la API de GitHub está bloqueada por el proxy (solo repo propio). Se usa:
  git clone superficial (permitido, nunca se ejecuta nada) + raw.githubusercontent + pypi.org.
  gh.py awesome owner/repo[/path/README.md] ... -> extrae enlaces github de listas awesome (descubrimiento)
  gh.py probe   owner/repo ...  -> clon --depth 60 temporal: métricas de actividad + sondas grep, luego borra el clon
"""
import json, os, re, subprocess, sys, time, urllib.request, urllib.parse, shutil, datetime as dt
TOK = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
API = "https://api.github.com"
NOW = dt.datetime(2026, 9, 3, tzinfo=dt.timezone.utc)
SCRATCH = "/tmp/claude-0/-home-user-Investiga/8069057e-37b1-5f57-b9a2-d4eae203c938/scratchpad/clones"

def get(path, params=None, raw=False):
    url = API + path + (("?" + urllib.parse.urlencode(params)) if params else "")
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {TOK}", "Accept": "application/vnd.github+json", "User-Agent": "research"})
    for i in range(4):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read().decode() if raw else json.load(r)
        except urllib.error.HTTPError as e:
            if e.code in (403, 429) and i < 3:
                time.sleep(15 * (i + 1)); continue
            if e.code == 404: return None
            raise
    return None

def days(s):
    if not s: return None
    return (NOW - dt.datetime.fromisoformat(s.replace("Z", "+00:00"))).days

def search(q, n=30):
    out = []
    per = min(n, 100)
    d = get("/search/repositories", {"q": q, "per_page": per, "sort": "updated", "order": "desc"}) or {}
    for r in d.get("items", []):
        out.append({"key": r["full_name"].lower(), "stars": r["stargazers_count"], "pushed_d": days(r["pushed_at"]),
                    "age_d": days(r["created_at"]), "lic": (r.get("license") or {}).get("spdx_id"),
                    "arch": r["archived"], "lang": r.get("language"), "desc": (r.get("description") or "")[:110],
                    "topics": r.get("topics", [])[:6]})
    return out

BOT = re.compile(r"\[bot\]|dependabot|renovate|github-actions|copilot|pre-commit", re.I)
DOCS = re.compile(r"^(README|docs/|\.github/|LICENSE|CHANGELOG|CONTRIBUTING|.*\.md$|.*\.rst$|.*\.txt$)", re.I)

def triage(key):
    r = get(f"/repos/{key}")
    if not r: return {"key": key, "verdict": "KILL", "kill_code": "K6", "kill_note": "404/no existe"}
    commits = get(f"/repos/{key}/commits", {"per_page": 30}) or []
    humans90, subst_days, docs_only, total = set(), None, 0, 0
    for c in commits:
        d = days(c["commit"]["author"]["date"]); total += 1
        login = (c.get("author") or {}).get("login") or c["commit"]["author"]["name"]
        if d is not None and d <= 90 and not BOT.search(login or ""): humans90.add(login)
        if subst_days is None:
            det = get(f"/repos/{key}/commits/{c['sha']}") if total <= 8 else None
            if det:
                files = [f["filename"] for f in det.get("files", [])]
                if files and all(DOCS.match(f) for f in files): docs_only += 1
                else: subst_days = d
    rel = get(f"/repos/{key}/releases", {"per_page": 30}) or []
    rel365 = sum(1 for x in rel if days(x["published_at"] or x["created_at"]) <= 365)
    return {"key": key, "stars": r["stargazers_count"], "forks": r["forks_count"], "arch": r["archived"],
            "lic": (r.get("license") or {}).get("spdx_id"), "lang": r.get("language"), "pushed_d": days(r["pushed_at"]),
            "age_d": days(r["created_at"]), "open_issues": r["open_issues_count"], "desc": (r.get("description") or "")[:120],
            "homepage": r.get("homepage"), "topics": r.get("topics", [])[:8], "default_branch": r["default_branch"],
            "subst_commit_d": subst_days if subst_days is not None else (days(commits[0]["commit"]["author"]["date"]) if commits else None),
            "humans90": len(humans90), "docs_only_top8": docs_only, "rel365": rel365, "size_kb": r["size"]}

PROBES = {
  "win_uia": r"uiautomation|comtypes|pywinauto|IUIAutomation|UIAutomationClient|FlaUI|System\.Windows\.Automation",
  "win32": r"pywin32|win32gui|win32api|win32con|ctypes\.windll|user32|SetProcessDpiAware|GetForegroundWindow",
  "screenshot": r"mss\b|ImageGrab|pyscreeze|screencapture|CopyFromScreen|BitBlt|PrintWindow|dxcam|desktopCapturer",
  "input": r"pyautogui|pynput|SendInput|keyboard\.press|mouse\.click|xdotool|robotjs|nut-js|SetCursorPos",
  "exec": r"subprocess\.(run|Popen|call)|os\.system|child_process|exec\(|eval\(|ShellExecute|powershell",
  "fs_write": r"open\([^)]*['\"]w|writeFile|shutil\.(rmtree|move)|os\.remove|fs\.unlink|Path\([^)]*\)\.write",
  "env_cred": r"os\.environ|process\.env|keyring|\.netrc|credential|api_key|API_KEY",
  "net": r"requests\.(get|post)|httpx|aiohttp|fetch\(|axios|urllib\.request",
  "telemetry": r"posthog|sentry|segment\.com|mixpanel|telemetry|analytics\.track",
  "approval": r"confirm|approval|permission|allowlist|allow_list|denylist|human_in_the_loop|require_confirmation|ask_user",
  "sandbox": r"docker|firejail|bubblewrap|seccomp|sandbox|AppContainer|Windows Sandbox|nsjail",
  "mcp": r"modelcontextprotocol|FastMCP|mcp\.server|McpServer|\"mcpServers\"",
  "playwright": r"playwright|puppeteer|CDP|chrome-remote-interface|selenium",
  "vlm": r"gpt-4o|claude-|gemini|qwen2?-?vl|qwen2\.5-vl|ui-tars|omniparser|florence|paligemma|showui|set-of-mark",
  "curl_bash": r"curl[^\n]*\|\s*(ba)?sh|iwr[^\n]*\|\s*iex|irm[^\n]*\|\s*iex",
}
def probe(key):
    os.makedirs(SCRATCH, exist_ok=True)
    dst = os.path.join(SCRATCH, key.replace("/", "__"))
    shutil.rmtree(dst, ignore_errors=True)
    p = subprocess.run(["git", "clone", "-q", "--depth", "60", "--single-branch", f"https://github.com/{key}.git", dst],
                       capture_output=True, text=True, timeout=300)
    if p.returncode != 0: return {"key": key, "error": p.stderr[-200:]}
    sha = subprocess.run(["git", "-C", dst, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    res = {"key": key, "sha": sha}
    log = subprocess.run(["git", "-C", dst, "log", "--format=%H|%an|%ae|%aI", "--name-only", "-n", "60"], capture_output=True, text=True).stdout
    commits, cur = [], None
    for line in log.split("\n"):
        if "|" in line and len(line.split("|")) == 4 and re.match(r"^[0-9a-f]{40}\|", line):
            h, an, ae, ad = line.split("|"); cur = {"a": an, "e": ae, "d": ad, "f": []}; commits.append(cur)
        elif line.strip() and cur is not None: cur["f"].append(line.strip())
    subst_d, humans90, docs_only, n90, authors365 = None, set(), 0, 0, {}
    for c in commits:
        d = days(c["d"]); isbot = bool(BOT.search(c["a"] + c["e"]))
        docs = bool(c["f"]) and all(DOCS.match(f) for f in c["f"])
        if docs: docs_only += 1
        elif subst_d is None: subst_d = d
        if d is not None and d <= 90 and not isbot: humans90.add(c["e"]); n90 += 1
        if d is not None and d <= 365 and not isbot: authors365[c["e"]] = authors365.get(c["e"], 0) + 1
    res["last_commit_d"] = days(commits[0]["d"]) if commits else None
    res["subst_commit_d"] = subst_d
    res["humans90"] = len(humans90); res["commits90"] = n90
    res["docs_only_ratio60"] = round(docs_only / max(1, len(commits)), 2)
    res["bus_top_share365"] = round(max(authors365.values()) / max(1, sum(authors365.values())), 2) if authors365 else None
    res["authors365"] = len(authors365)
    tags = subprocess.run(["git", "-C", dst, "ls-remote", "--tags", "-q", "origin"], capture_output=True, text=True).stdout
    res["tags_total"] = len([l for l in tags.split("\n") if l and not l.endswith("^{}")])
    lic = next((f for f in os.listdir(dst) if f.upper().startswith("LICENSE") or f.upper().startswith("COPYING")), None)
    res["license_file"] = lic
    if lic:
        lt = open(os.path.join(dst, lic), errors="ignore").read(600)
        res["license_guess"] = ("MIT" if "MIT License" in lt else "Apache-2.0" if "Apache License" in lt else "GPL" if "GNU GENERAL PUBLIC" in lt else "AGPL" if "AFFERO" in lt else "BSD" if "BSD" in lt else "MPL" if "Mozilla Public" in lt else "OTHER")
    # files
    files = []
    for root, dirs, fs in os.walk(dst):
        dirs[:] = [d for d in dirs if d not in (".git", "node_modules", "vendor", "dist", "build", ".venv", "third_party")]
        for f in fs: files.append(os.path.relpath(os.path.join(root, f), dst))
    code_ext = (".py", ".ts", ".tsx", ".js", ".rs", ".go", ".cs", ".java", ".kt", ".swift", ".cpp", ".c", ".ps1", ".ahk")
    code = [f for f in files if f.endswith(code_ext)]
    loc = 0
    for f in code[:3000]:
        try:
            with open(os.path.join(dst, f), "rb") as fh: loc += sum(1 for _ in fh)
        except Exception: pass
    res["files"] = len(files); res["code_files"] = len(code); res["loc"] = loc
    res["tests"] = sum(1 for f in code if re.search(r"(^|/)(tests?|__tests__|spec)(/|$)|_test\.|\.test\.|test_", f))
    res["top"] = sorted({f.split("/")[0] for f in files})[:40]
    res["dep_files"] = [f for f in files if f.split("/")[-1] in ("pyproject.toml", "requirements.txt", "package.json", "Cargo.toml", "go.mod", "setup.py", "uv.lock", "poetry.lock", "package-lock.json", "pnpm-lock.yaml", "yarn.lock", "bun.lockb") and f.count("/") == 0]
    ci = [f for f in files if f.startswith(".github/workflows/")]
    res["ci"] = len(ci)
    citext = ""
    for f in ci:
        try: citext += open(os.path.join(dst, f), errors="ignore").read()
        except Exception: pass
    res["ci_windows"] = bool(re.search(r"windows-latest|windows-20", citext))
    res["ci_tests"] = bool(re.search(r"pytest|npm test|cargo test|go test|vitest|jest|dotnet test", citext))
    res["installers"] = [f for f in files if re.search(r"(^|/)(install|setup)[^/]*\.(sh|ps1|bat|cmd)$", f, re.I)][:6]
    res["postinstall"] = False
    pj = os.path.join(dst, "package.json")
    if os.path.exists(pj):
        try: res["postinstall"] = "postinstall" in json.load(open(pj)).get("scripts", {})
        except Exception: pass
    # readme head
    rd = next((f for f in files if f.lower() in ("readme.md", "readme.rst", "readme")), None)
    res["readme_head"] = ""
    if rd:
        txt = open(os.path.join(dst, rd), errors="ignore").read()
        res["readme_len"] = len(txt)
        res["readme_head"] = re.sub(r"\n{2,}", "\n", re.sub(r"<[^>]+>", "", txt))[:1800]
        res["readme_windows"] = len(re.findall(r"windows|win11|win10|powershell", txt, re.I))
        res["readme_wsl"] = len(re.findall(r"\bwsl\b", txt, re.I)); res["readme_docker"] = len(re.findall(r"docker", txt, re.I))
        res["readme_macos_only"] = bool(re.search(r"(only|currently) (supports?|available on|works on) macos", txt, re.I))
    # grep probes over code + readme + docs
    hits = {}
    for name, pat in PROBES.items():
        g = subprocess.run(["grep", "-rIlE", "--exclude-dir=.git", "--exclude-dir=node_modules", "--exclude-dir=dist", pat, dst],
                           capture_output=True, text=True)
        fl = [os.path.relpath(x, dst) for x in g.stdout.split("\n") if x]
        if fl: hits[name] = {"n": len(fl), "ex": fl[:3]}
    res["probes"] = hits
    shutil.rmtree(dst, ignore_errors=True)
    return res

def awesome(spec):
    if "/" in spec and spec.count("/") >= 3: owner, repo, path = spec.split("/", 1)[0], spec.split("/")[1], "/".join(spec.split("/")[2:])
    else: owner, repo, path = spec.split("/")[0], spec.split("/")[1], "README.md"
    txt = None
    for br in ("main", "master"):
        url = f"https://raw.githubusercontent.com/{owner}/{repo}/{br}/{path}"
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "research"}), timeout=30) as r: txt = r.read().decode(errors="ignore"); break
        except Exception: continue
    if txt is None: return {"list": spec, "error": "not found"}
    links = re.findall(r"https?://github\.com/([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)", txt)
    keys = []
    for l in links:
        k = l.lower().rstrip(".")
        if k.split("/")[0] in ("topics", "orgs", "settings", "features", "sponsors", "marketplace", "apps", "about", "site", "search", "collections", "trending", "login", "signup", "explore"): continue
        if k not in keys: keys.append(k)
    return {"list": spec, "chars": len(txt), "n_links": len(keys), "keys": keys}

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "awesome":
        for k in sys.argv[2:]: print(json.dumps(awesome(k), ensure_ascii=False)); sys.stdout.flush()
    elif cmd == "probe":
        for k in sys.argv[2:]: print(json.dumps(probe(k.lower()), ensure_ascii=False)); sys.stdout.flush()
    elif cmd == "brief":  # resumen compacto de probes.jsonl
        for l in open(sys.argv[2]):
            r=json.loads(l)
            if "error" in r: print(f"{r['key']}: ERROR {r['error'][:60]}"); continue
            p=r.get("probes",{}); pk=",".join(f"{k}{v['n']}" for k,v in p.items())
            print(f"{r['key']} | lic={r.get('license_guess')} last={r.get('last_commit_d')}d subst={r.get('subst_commit_d')}d h90={r.get('humans90')} c90={r.get('commits90')} bus={r.get('bus_top_share365')} tags={r.get('tags_total')} | loc={r.get('loc')} tests={r.get('tests')} ci={r.get('ci')} ciwin={int(bool(r.get('ci_windows')))} citest={int(bool(r.get('ci_tests')))} post={int(bool(r.get('postinstall')))} inst={len(r.get('installers',[]))} | rdwin={r.get('readme_windows')} wsl={r.get('readme_wsl')} dock={r.get('readme_docker')} macos_only={int(bool(r.get('readme_macos_only')))} | {pk}")
