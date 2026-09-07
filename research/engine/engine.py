#!/usr/bin/env python
"""The Ideya authoring engine, v2: one command from catalog entry to a loaded
draft and a one-page packet, with nothing run by hand in between.

    .venv/bin/python research/engine/engine.py author <slug> [--start-at STEP] [--concurrency N]
    .venv/bin/python research/engine/engine.py status <slug>

Every step is idempotent and checkpointed in research/runs/<slug>/state.json;
every agent call inside a step is journaled by the harness, so a crash, a kill
or a usage limit resumes from the last call, not the last stage. The stage
scripts (research_topic.js, distribute_topic.js) run UNCHANGED through
research/engine/harness.py on the user's subscription. Stage 5 ends at a loaded
DRAFT and a packet; publishing is the human's, always.
"""

import argparse
import asyncio
import datetime as dt
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "research" / "workflows"))
from research.engine.harness import Harness  # noqa: E402
import bake  # noqa: E402  (catalog_entry, skeleton, load_prior, PHASE_NEEDS, PHASE_STOP)

PY = str(REPO / ".venv" / "bin" / "python")
WF = REPO / "research" / "workflows"
BASE_URL = os.environ.get("ENGINE_BASE_URL", "http://127.0.0.1:8641")
DJ = {**os.environ, "DJANGO_DEBUG": "true"}
AGENTS = REPO / ".claude" / "agents"

STEPS = [
    "s1.plan", "s1.research", "s1.verify", "s1.gate",
    "s2.distribute", "s2.lint", "s2.load", "s2.fit",
    "s3.brief", "s3.generate", "s3.select", "s3.postprocess",
    "s4.render", "s4.links", "s4.views",
    "s5.pm", "s5.packet",
]


def now():
    return dt.datetime.now().isoformat(timespec="seconds")


def sh(cmd, env=None, check=True, timeout=1800):
    r = subprocess.run(cmd, cwd=REPO, env=env or os.environ, capture_output=True, text=True, timeout=timeout)
    if check and r.returncode:
        raise RuntimeError(f"{' '.join(str(c) for c in cmd[:4])} failed ({r.returncode}):\n{(r.stdout + r.stderr)[-1500:]}")
    return r


def jload(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def jdump(p, o):
    Path(p).parent.mkdir(parents=True, exist_ok=True)
    tmp = Path(str(p) + ".tmp")
    tmp.write_text(json.dumps(o, ensure_ascii=False, indent=1), encoding="utf-8")
    tmp.replace(p)


class Run:
    def __init__(self, slug, concurrency=None, log=print):
        self.slug = slug
        self.entry = bake.catalog_entry(slug)
        self.title = self.entry["title"]
        self.dir = REPO / "research" / "runs" / slug
        self.dir.mkdir(parents=True, exist_ok=True)
        self.state_path = self.dir / "state.json"
        self.state = jload(self.state_path) if self.state_path.exists() else {"slug": slug, "title": self.title, "started": now(), "steps": {}}
        self.concurrency = concurrency
        self.log = log
        self.dossier_path = REPO / "research" / "dossiers" / f"{slug}.json"
        self.topic_path = REPO / "research" / "topics" / f"{slug}.json"
        self.review_dir = REPO / "research" / "reviews" / slug
        self.review_dir.mkdir(parents=True, exist_ok=True)
        self.today = dt.date.today().isoformat()

    # ---- state -----------------------------------------------------------
    def save(self):
        jdump(self.state_path, self.state)

    def mark(self, step, status, note=""):
        s = self.state["steps"].setdefault(step, {})
        s["status"] = status
        s[status] = now()
        if note:
            s["note"] = note
        self.save()

    def done(self, step):
        return self.state["steps"].get(step, {}).get("status") in ("done", "skipped")

    # ---- agents ----------------------------------------------------------
    def harness(self, step):
        return Harness(self.dir / step, self.concurrency, log=self.log)

    async def script(self, step, script, args):
        return await self.harness(step).run(WF / script, args)

    async def agent(self, step, prompt, **opts):
        return await self.harness(step).agent(prompt, opts)

    # ---- stage 1 ---------------------------------------------------------
    async def s1_phase(self, phase):
        step = f"s1.{phase}"
        args = bake.skeleton(self.entry, self.today)
        args["prior"] = bake.load_prior(self.dossier_path, bake.PHASE_NEEDS[phase], self.slug) if bake.PHASE_NEEDS[phase] else {}
        args["stop_after"] = bake.PHASE_STOP[phase]
        r = await self.script(step, "research_topic.js", args)
        if not isinstance(r, dict):
            raise RuntimeError(f"{step}: script returned {type(r).__name__}")
        d = jload(self.dossier_path) if self.dossier_path.exists() else {"dossier_version": 1, "slug": self.slug, "input": self.entry}
        d.update({k: v for k, v in r.items()})
        d["generated"] = now()
        d["phase_done"] = phase
        d.setdefault("runs", {})[step] = str(self.dir / step)
        if phase == "gate":
            vs = r.get("verdicts") or []
            passes = sum(1 for v in vs if v.get("pass"))
            blocks = sum(len(v.get("blocking") or []) for v in vs)
            d["gate_status"] = "pass" if passes == len(vs) and not r.get("shape_notes") else f"{passes}/{len(vs)} pass, {blocks} blocking open"
        jdump(self.dossier_path, d)
        return d.get("gate_status", f"{phase} persisted")

    # ---- stage 2 ---------------------------------------------------------
    def s2_args(self, fix_only=None):
        d = jload(self.dossier_path)
        a = {"slug": self.slug, "title": self.title, "today": self.today,
             "dossier": {"draft": d["draft"], "verdicts": d.get("verdicts", []), "plan_positions": d.get("plan_positions", []),
                         "plan": d["plan"], "claim_ledger": d["claim_ledger"]}}
        if fix_only is not None:
            t = jload(self.topic_path)
            a["dossier"]["draft"] = t["draft"]
            a["dossier"]["verdicts"] = t.get("verdicts", [])
            a["dossier"]["plan_positions"] = t.get("plan_positions", [])
            a["fix_only"] = fix_only
        return a

    def persist_topic(self, r, tag):
        t = jload(self.topic_path) if self.topic_path.exists() else {}
        d = jload(self.dossier_path)
        t.update({"draft": r["draft"], "verdicts": r["verdicts"], "plan_positions": r.get("plan_positions", []), "claim_ledger": d["claim_ledger"], "fold": r.get("fold", t.get("fold"))})
        t.setdefault("runs", {})[tag] = now()
        jdump(self.topic_path, t)

    async def s2_distribute(self):
        r = await self.script("s2.distribute", "distribute_topic.js", self.s2_args())
        self.persist_topic(r, "s2.distribute")
        vs = [v for v in r["verdicts"] if v.get("stage") == "presentation"]
        return f"presentation {sum(1 for v in vs if v.get('pass'))}/{len(vs)}"

    async def fix_only(self, step, findings):
        r = await self.script(step, "distribute_topic.js", self.s2_args(fix_only=findings))
        self.persist_topic(r, step)
        return r

    def lint(self):
        sh([PY, str(WF / "lint_draft.py"), str(self.topic_path), "--fix"], check=False)
        r = sh([PY, str(WF / "lint_draft.py"), str(self.topic_path), "--json"], check=False)
        try:
            return json.loads(r.stdout or "[]")
        except json.JSONDecodeError:
            return []

    async def s2_lint(self):
        for i in range(3):
            findings = self.lint()
            if not findings:
                return f"lint 0 after {i} fix pass(es)"
            self.log(f"  lint: {len(findings)} judgment finding(s) → fix_only")
            await self.fix_only(f"s2.lint.fix{i + 1}", findings)
        raise RuntimeError("lint still failing after 2 fix_only passes")

    def load(self):
        r = sh([PY, "manage.py", "load_topic_draft", "--file", str(self.topic_path), "--slug", self.slug, "--title", self.title,
                "--category", self.entry["primary_category_slug"], "--status", "draft"], env=DJ)
        warn = [l for l in (r.stdout + r.stderr).splitlines() if "warn" in l.lower() or "EXHAUSTED" in l]
        self.state.setdefault("loader_warnings", warn)
        return (r.stdout.strip().splitlines() or [""])[-1]

    def ensure_server(self):
        try:
            import urllib.request
            urllib.request.urlopen(BASE_URL + "/", timeout=5)
            return
        except Exception:
            pass
        self.log(f"  starting dev server on {BASE_URL}")
        subprocess.Popen([PY, "manage.py", "runserver", BASE_URL.split("//")[1], "--noreload"], cwd=REPO, env=DJ,
                         stdout=open(self.dir / "devserver.log", "a"), stderr=subprocess.STDOUT)
        time.sleep(6)

    async def s2_fit(self):
        self.ensure_server()
        for i in range(3):
            out = self.dir / f"fit{i}.json"
            r = sh([PY, str(WF / "fit_check.py"), "--slug", self.slug, "--base-url", BASE_URL, "--json", str(out)], check=False)
            if r.returncode == 0:
                return (r.stdout.strip().splitlines() or ["fits"])[-1]
            if not out.exists():
                raise RuntimeError("fit_check failed: " + (r.stdout + r.stderr)[-800:])
            self.log("  poster over → fix_only with measured trims")
            await self.fix_only(f"s2.fit.fix{i + 1}", jload(out))
            if self.lint():
                await self.fix_only(f"s2.fit.lint{i + 1}", self.lint())
            self.load()
        raise RuntimeError("poster still overflows after 2 measured trims")

    # ---- stage 3 ---------------------------------------------------------
    async def s3_brief(self):
        brief_path = REPO / "research" / "icons" / f"{self.slug}.md"
        if brief_path.exists() and "## Generation prompt" in brief_path.read_text(encoding="utf-8"):
            return "brief already present"
        schema = {"type": "object", "additionalProperties": False, "required": ["brief_markdown", "concept"],
                  "properties": {"brief_markdown": {"type": "string"}, "concept": {"type": "string"}}}
        d = jload(self.dossier_path)
        prompt = (f"Write the icon brief for the Ideya topic below. Return it as `brief_markdown` (the complete file content for research/icons/{self.slug}.md, matching the headings of the existing briefs exactly, with a complete self-contained `## Generation prompt` blockquote) and one line in `concept` naming the visual concept and why it survives at 40px.\n\n"
                  f"slug: {self.slug}\ntitle: {self.title}\nprimary category: {self.entry['primary_category_slug']} (secondary: {', '.join(self.entry.get('secondary_category_slugs') or [])})\n"
                  f"summary: {self.entry.get('summary', '')}\noverview line: {d['draft']['overview'].get('summary', '')}\nstage-1 Phosphor icon hint: {d['draft']['overview'].get('icon', '')} (a hint only)\n\n"
                  "Ground yourself first by reading research/ICONOGRAPHY.md, research/icons/categories.md and two or three existing briefs in research/icons/*.md as exemplars.")
        r = await self.agent("s3.brief", prompt, schema=schema, label="icon-brief", agentType="icon-briefer", model="opus", effort="high")
        if not r or not r.get("brief_markdown"):
            raise RuntimeError("icon brief agent returned nothing")
        brief_path.write_text(r["brief_markdown"].rstrip() + "\n", encoding="utf-8")
        return r["concept"][:200]

    def s3_generate(self):
        cdir = REPO / "research" / "icons" / "candidates" / self.slug
        if cdir.exists() and len(list(cdir.glob("*.jpg"))) >= 4:
            return f"{len(list(cdir.glob('*.jpg')))} candidates already present"
        r = sh([PY, str(REPO / "research" / "icons" / "generate_icons.py"), "--slug", self.slug, "--n", "4"], timeout=900)
        return (r.stdout.strip().splitlines() or [""])[-1]

    async def s3_select(self):
        cdir = REPO / "research" / "icons" / "candidates" / self.slug
        brief_path = REPO / "research" / "icons" / f"{self.slug}.md"
        if "## Selection" in brief_path.read_text(encoding="utf-8"):
            return "selection already recorded"
        cands = sorted(p for p in cdir.glob("*.jpg") if ".40px" not in p.name)
        neighbors = [p for p in (REPO / "static" / "img" / "topics").glob("*.png") if p.stem != self.slug][:3]
        schema = {"type": "object", "additionalProperties": False, "required": ["winner", "rationale", "rejects"],
                  "properties": {"winner": {"type": "integer", "description": "1-based index into the candidate list"}, "rationale": {"type": "string"},
                                 "rejects": {"type": "array", "items": {"type": "string"}}}}
        prompt = ("Judge these icon candidates for the Ideya topic below against the checklist in research/ICONOGRAPHY.md: uniform monoline stroke, same-hue ~16–18% duotone fill on EVERY major element, the category color, 2.5–3.5× scene complexity, white ground, no text or frame, and legibility at 40px. Judge family fit too: read the neighbor icons and pick the candidate that reads as the same hand. Read every image with the Read tool.\n\n"
                  f"topic: {self.title} ({self.slug})\nbrief: research/icons/{self.slug}.md\n\nCANDIDATES (1-based):\n" + "\n".join(f"{i + 1}. {p}" for i, p in enumerate(cands)) +
                  "\n\nNEIGHBORS (existing winners):\n" + "\n".join(str(p) for p in neighbors) +
                  "\n\nReturn the winner's index, a two-sentence rationale, and one line per rejected candidate.")
        r = await self.agent("s3.select", prompt, schema=schema, label="icon-select", agentType="view-critic", model="opus", effort="high")
        if not r:
            raise RuntimeError("icon selection agent returned nothing")
        w = cands[max(0, min(len(cands) - 1, int(r["winner"]) - 1))]
        brief_path = REPO / "research" / "icons" / f"{self.slug}.md"
        with brief_path.open("a", encoding="utf-8") as f:
            f.write(f"\n## Selection\n\n{self.today}: candidate {int(r['winner'])} of {len(cands)} (`{w.name}`). {r['rationale']}\n" + "".join(f"- {x}\n" for x in r.get("rejects", [])))
        self.state["icon_winner"] = str(w)
        return f"candidate {int(r['winner'])} of {len(cands)}"

    def s3_postprocess(self):
        icon = REPO / "static" / "img" / "topics" / f"{self.slug}.png"
        if icon.exists():
            return "icon already present"
        w = self.state.get("icon_winner")
        r = sh([PY, str(REPO / "research" / "icons" / "postprocess_icon.py"), "--slug", self.slug, "--src", w])
        return (r.stdout.strip().splitlines() or [""])[0]

    # ---- stage 4 ---------------------------------------------------------
    def s4_render(self):
        self.ensure_server()
        m = [PY, "manage.py"]
        sh(m + ["render_screens", "--slug", self.slug, "--base-url", BASE_URL, "--sections"], env=DJ, timeout=1200)
        sh(m + ["render_screens", "--slug", self.slug, "--base-url", BASE_URL, "--sections", "--expanded"], env=DJ, timeout=1200)
        sh(m + ["render_social", "--slug", self.slug, "--formats", "og", "--base-url", BASE_URL], env=DJ)
        sh(m + ["render_social", "--slug", self.slug, "--formats", "sq,pt", "--base-url", BASE_URL, "--out", str(self.review_dir)], env=DJ)
        r = sh(m + ["render_poster", "--slug", self.slug, "--base-url", BASE_URL, "--out", str(self.review_dir)], env=DJ, check=False)
        if r.returncode:
            raise RuntimeError("poster overflowed at stage 4 after fit_check passed: " + r.stdout[-300:])
        return "6 screens + sections, og, sq, pt, poster"

    def s4_links(self):
        r = sh([PY, "manage.py", "check_links", "--topic", self.slug], env=DJ, check=False, timeout=1200)
        summary = [l for l in r.stdout.splitlines() if l.startswith("Summary")]
        dead = [l for l in r.stdout.splitlines() if l.strip().startswith("DEAD")]
        self.state["links"] = (summary or [""])[0]
        if dead:
            raise RuntimeError("dead links: " + " | ".join(dead[:5]))
        return self.state["links"]

    async def s4_views(self):
        sec = self.review_dir / "sections"
        common = ("Judge ONLY on-system vs off-system against design/DESIGN_SYSTEM.md and design/RESPONSIVE.md, with research/reviews/UI_DEFECTS.md in hand: cite an OPEN entry rather than re-reporting it; a FIXED entry recurring is a REGRESSION, say so; a new site-wide defect gets the template/CSS location if you can name it. Read every image with the Read tool. Do not comment on content quality.\n"
                  f"Topic: {self.title} ({self.slug}), category {self.entry['primary_category_slug']}.\n")
        schema = {"type": "object", "additionalProperties": False, "required": ["findings", "blocking", "notes"],
                  "properties": {"findings": {"type": "array", "items": {"type": "object", "additionalProperties": False, "required": ["where", "what", "on_system", "register", "severity"],
                                 "properties": {"where": {"type": "string"}, "what": {"type": "string"}, "on_system": {"type": "boolean"}, "register": {"type": "string"}, "severity": {"type": "string", "enum": ["blocking", "note"]}}}},
                                 "blocking": {"type": "integer"}, "notes": {"type": "integer"}}}
        jobs = {
            "desktop": [p for p in sorted(sec.glob("desktop-1440/*.png"))] + [p for p in sorted(sec.glob("desktop-1440-expanded/*.png"))],
            "mobile": [p for p in sorted(sec.glob("mobile-390/*.png"))] + [p for p in sorted(sec.glob("mobile-320/*.png"))],
            "cards": [self.review_dir / f"{self.slug}.pdf", REPO / "static" / "img" / "social" / f"{self.slug}.png", self.review_dir / f"{self.slug}-sq.png", self.review_dir / f"{self.slug}-pt.png", REPO / "static" / "img" / "topics" / f"{self.slug}.png"],
        }
        async def one(name, files):
            prompt = common + f"Surface set: {name}. Files (in page order):\n" + "\n".join(str(f) for f in files) + "\n\nReturn every finding with where, what, on_system, register match (OPEN/FIXED/new), severity."
            return name, await self.agent("s4.views", prompt, schema=schema, label=f"views:{name}", agentType="view-critic", model="opus", effort="high")
        results = dict(await asyncio.gather(*(one(n, f) for n, f in jobs.items())))
        jdump(self.review_dir / "views.json", results)
        blocking = sum((r or {}).get("blocking", 0) for r in results.values())
        return f"views: {blocking} blocking, {sum((r or {}).get('notes', 0) for r in results.values())} notes"

    # ---- stage 5 ---------------------------------------------------------
    def checks(self):
        from PIL import Image
        Image.MAX_IMAGE_PIXELS = None
        t = jload(self.topic_path)
        lint = self.lint()
        icon = REPO / "static" / "img" / "topics" / f"{self.slug}.png"
        og = REPO / "static" / "img" / "social" / f"{self.slug}.png"
        renders = [self.review_dir / f"{a}-{w}{s}.png" for a, w in (("desktop", 1440), ("mobile", 390), ("mobile", 320)) for s in ("", "-expanded")]
        sys.path.insert(0, str(REPO / "topics" / "management" / "commands"))
        cap = 80000
        try:
            import render_screens as rs
            cap = rs.CAPTURE_HEIGHT_EXPANDED
        except Exception:
            pass
        heights = [Image.open(p).size[1] if p.exists() else None for p in renders]
        sub = [v for v in t["verdicts"] if v.get("stage") == "substance"]
        pres = [v for v in t["verdicts"] if v.get("stage") == "presentation"]
        fid = next((v for v in pres if v.get("key") == "claim-fidelity"), None)
        lines = [
            f"CHECK 1 lint            {'PASS' if not lint else 'FAIL'}  {len(lint)} findings",
            f"CHECK 2 links           {'PASS' if 'dead' in self.state.get('links', '') and ' 0 dead' in self.state.get('links', '') else 'FAIL'}  {self.state.get('links', 'not run')}",
            f"CHECK 3 primary art     {'PASS' if icon.exists() and Image.open(icon).size == (1035, 690) else 'FAIL'}  {Image.open(icon).size if icon.exists() else 'missing'}",
            f"CHECK 4 og card         {'PASS' if og.exists() else 'FAIL'}  {og.relative_to(REPO) if og.exists() else 'missing'}",
            f"CHECK 5 cards + poster  {'PASS' if all((self.review_dir / n).exists() for n in (f'{self.slug}-sq.png', f'{self.slug}-pt.png', f'{self.slug}.pdf')) else 'FAIL'}  sq/pt/pdf",
            f"CHECK 6 renders         {'PASS' if all(h and h < cap - 200 for h in heights) else 'FAIL'}  {sum(1 for h in heights if h)} of 6; cap {cap}; tallest {max(h or 0 for h in heights)}",
            f"CHECK 7 gates ran       {'PASS' if len(sub) == 5 and len(pres) == 4 and fid and 'no claim_ledger' not in json.dumps(fid) and 'claim_ledger' in t else 'FAIL'}  substance {sum(1 for v in sub if v.get('pass'))}/{len(sub)}, presentation {sum(1 for v in pres if v.get('pass'))}/{len(pres)}, fidelity {'ran' if fid else 'missing'}",
        ]
        return lines

    async def s5_pm(self):
        checks = self.checks()
        t = jload(self.topic_path)
        d = jload(self.dossier_path)
        from collections import Counter
        led = Counter(r.get("status") for r in d["claim_ledger"]["results"])
        views = jload(self.review_dir / "views.json") if (self.review_dir / "views.json").exists() else {}
        schema = {"type": "object", "additionalProperties": False, "required": ["routing", "packet_markdown"],
                  "properties": {"routing": {"type": "array", "items": {"type": "object", "additionalProperties": False, "required": ["finding", "stage", "closes_when"],
                                 "properties": {"finding": {"type": "string"}, "stage": {"type": "string", "enum": ["1", "2", "3", "4", "register"]}, "closes_when": {"type": "string"}}}},
                                 "packet_markdown": {"type": "string"}}}
        counts = {k: len(t["draft"].get(k) or (t["draft"].get("basics", {}).get("stats") if k == "stats" else [])) for k in ("questions", "positions", "actions")}
        counts["stats"] = len(t["draft"]["basics"]["stats"])
        prompt = (f"Stage 4.5 PM gate for the Ideya topic \"{self.title}\" (slug {self.slug}, category {self.entry['primary_category_slug']}), loaded as DRAFT at {BASE_URL}/{self.slug}/ (and ?expanded=1). Today is {self.today}.\n\n"
                  f"Counts: {counts['stats']} stats · {counts['questions']} questions · {counts['positions']} positions · {counts['actions']} actions. Fold: {json.dumps(t.get('fold'))}.\n\n"
                  "The deterministic pass was run by the engine; its lines are below — report them as given, and verify any you doubt by reading the files (you may Read, not run):\n" + "\n".join(checks) + "\n\n"
                  f"Run: substance verdicts {[(v.get('key'), v.get('pass'), len(v.get('blocking') or [])) for v in t['verdicts'] if v.get('stage') == 'substance']}; presentation verdicts {[(v.get('key'), v.get('pass'), len(v.get('blocking') or [])) for v in t['verdicts'] if v.get('stage') == 'presentation']}; ledger {dict(led)} of {len(d['claim_ledger']['claims'])}; prescribed fixes on file: {len(d.get('prescribed_fixes') or [])} (stage 1) + {len(t.get('prescribed_fixes') or [])} (stage 2); loader warnings: {self.state.get('loader_warnings')}; links: {self.state.get('links')}.\n\n"
                  f"Stage-4 view-critic findings (design conformance): {json.dumps(views)[:6000]}\n\n"
                  f"Renders to read: research/reviews/{self.slug}/sections/<set>/*.png (per-section, in page order; sets desktop-1440, desktop-1440-expanded, mobile-390, mobile-320, mobile-390-expanded, mobile-320-expanded), the poster research/reviews/{self.slug}/{self.slug}.pdf, cards research/reviews/{self.slug}/{self.slug}-sq.png and -pt.png, og static/img/social/{self.slug}.png. Topic JSON: research/topics/{self.slug}.json. Do not read the dossier.\n\n"
                  "Return `routing` (empty on a healthy run) and `packet_markdown` — the one-page packet per research/ENGINE.md §12 (links first; Run; Decided for you; Check in 5 minutes with at most three items; Engineering; Publish).")
        r = await self.agent("s5.pm", prompt, schema=schema, label="pm", agentType="topic-pm", model="fable", effort="max")
        if not r:
            raise RuntimeError("PM returned nothing")
        jdump(self.dir / "pm.json", r)
        (self.review_dir / "REVIEW.md").write_text(r["packet_markdown"].rstrip() + "\n", encoding="utf-8")
        if r["routing"] and not self.state.get("pm_rerouted"):
            self.state["pm_rerouted"] = True
            self.save()
            changed = await self.route(r["routing"])
            if changed:
                if self.lint():
                    await self.fix_only("s5.reroute.lint", self.lint())
                self.load()
                self.s4_render()
            self.log("  routes handled — re-running the PM once")
            return await self.s5_pm()
        return f"PM: {len(r['routing'])} routed" + (" (second read; left for the human)" if r["routing"] else "")

    async def route(self, routing):
        """Close what the PM routed, by the engine's own rules. Returns True if
        the draft changed (so it must be re-linted, re-loaded, re-rendered)."""
        changed = False
        s2, s1, reg = [], [], []
        for x in routing:
            (s2 if x["stage"] == "2" else s1 if x["stage"] == "1" else reg if x["stage"] == "register" else []).append(x)
        for x in reg:
            self.register_row(x)
        for x in s1:
            changed |= await self.verify_routed_claim(x)
        if s2:
            await self.fix_only("s5.reroute", [{"issue": x["finding"], "fix": x["closes_when"], "quote": x["finding"][:200]} for x in s2])
            changed = True
        for x in routing:
            if x["stage"] in ("3", "4"):
                self.log(f"  route to stage {x['stage']} left for the human: {x['finding'][:120]}")
        return changed

    def register_row(self, x):
        reg = REPO / "research" / "reviews" / "UI_DEFECTS.md"
        text = reg.read_text(encoding="utf-8")
        anchor = "## By design"
        i = text.index(anchor)
        cell = lambda t: t.replace("|", "／").replace("\n", " ").strip()
        row = f"| {cell(x['finding'])} | see finding | {self.slug} ({self.today}, stage-4.5 PM) | {cell(x['closes_when'])} |\n\n"
        head = text[:i].rstrip("\n") + "\n"
        reg.write_text(head + row + text[i:], encoding="utf-8")
        self.log(f"  register: appended — {x['finding'][:100]}")

    async def verify_routed_claim(self, x):
        """A fact the PM found asserted without a ledger result: verify it blind
        (claim-verifier), append the verdict to the ledger, and if it is not
        supported, soften it through one stage-2 fix_only (cut / soften /
        attribute in-voice — the same three outcomes every claim gets)."""
        import re as _re
        q = _re.search(r'"([^"]{20,})"', x["finding"]) or _re.search(r"“([^”]{20,})”", x["finding"])
        quote = q.group(1) if q else x["finding"][:300]
        schema = {"type": "object", "additionalProperties": False, "required": ["status", "source_url", "source_quote", "note"],
                  "properties": {"status": {"type": "string", "enum": ["supported", "contradicted", "unverifiable"]}, "source_url": {"type": "string"}, "source_quote": {"type": "string"}, "note": {"type": "string"}}}
        prompt = (f"Verify this claim in isolation against real sources. A verdict with no verbatim source_quote from a page you read is unverifiable. Never answer from memory.\n\nCLAIM: {quote}\n\nContext from the reviewer (not evidence): {x['finding'][:600]}")
        v = await self.agent("s5.route", prompt, schema=schema, label="verify:routed", agentType="claim-verifier", model="sonnet", effort="high")
        if not v:
            v = {"status": "unverifiable", "source_url": "", "source_quote": "", "note": "verifier returned nothing"}
        if not v.get("source_quote"):
            v["status"] = "unverifiable"
        cid = f"r{sum(1 for c in jload(self.dossier_path)['claim_ledger']['claims'] if str(c.get('id', '')).startswith('r')) + 1}"
        for path in (self.dossier_path, self.topic_path):
            d = jload(path)
            d["claim_ledger"]["claims"].append({"id": cid, "claim": quote, "quote": quote, "section": "routed", "item": "", "kind": "fact", "source_url": v.get("source_url", "")})
            d["claim_ledger"]["results"].append({"id": cid, **v, "note": f"PM-routed, verified blind at stage 5: {v.get('note', '')}"})
            jdump(path, d)
        self.log(f"  routed claim {cid}: {v['status']}")
        if v["status"] == "supported":
            return False
        await self.fix_only("s5.route.fix", [{"issue": f"A claim on the page is {v['status']} (blind verifier at stage 5): {quote}", "fix": "Cut it, soften it to exactly what a source supports, or attribute it in-voice to whoever asserts it — presentation edit on the description/detail that carries it; never assert a figure you cannot source.", "quote": quote}])
        return True

    def s5_packet(self):
        usage = {}
        for step_dir in sorted(p for p in self.dir.iterdir() if p.is_dir()):
            j = step_dir / "journal"
            if not j.exists():
                continue
            u = {"calls": 0, "cached": 0, "input": 0, "output": 0, "cache_read": 0, "cache_write": 0}
            for f in j.glob("*.json"):
                e = jload(f)
                us = e.get("usage") or {}
                u["calls"] += 1
                u["input"] += int(us.get("input_tokens") or 0)
                u["output"] += int(us.get("output_tokens") or 0)
                u["cache_read"] += int(us.get("cache_read_input_tokens") or 0)
                u["cache_write"] += int(us.get("cache_creation_input_tokens") or 0)
            usage[step_dir.name] = u
        tot = {k: sum(v.get(k, 0) for v in usage.values()) for k in ("calls", "cached", "input", "output", "cache_read", "cache_write")}
        lines = [f"# {self.slug} — token record", "", f"Authoring run {self.state['started'][:10]} → {now()[:16]} (engine v2, subscription; per-call journal under research/runs/{self.slug}/).", "",
                 "| step | calls | cached | input | output | cache read | cache write |", "|---|---|---|---|---|---|---|"]
        for k, v in usage.items():
            lines.append(f"| {k} | {v.get('calls', 0)} | {v.get('cached', 0)} | {v.get('input', 0):,} | {v.get('output', 0):,} | {v.get('cache_read', 0):,} | {v.get('cache_write', 0):,} |")
        lines.append(f"| **total** | {tot['calls']} | {tot['cached']} | {tot['input']:,} | {tot['output']:,} | {tot['cache_read']:,} | {tot['cache_write']:,} |")
        lines += ["", "Stage 3 image generation: 4 Gemini candidates × 1 round (not in any Anthropic tally)."]
        (self.review_dir / "tokens.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
        return f"packet + tokens written to {self.review_dir.relative_to(REPO)}"

    # ---- driver ----------------------------------------------------------
    def step_fn(self, step):
        return {
            "s1.plan": lambda: self.s1_phase("plan"), "s1.research": lambda: self.s1_phase("research"),
            "s1.verify": lambda: self.s1_phase("verify"), "s1.gate": lambda: self.s1_phase("gate"),
            "s2.distribute": self.s2_distribute, "s2.lint": self.s2_lint, "s2.load": self.load, "s2.fit": self.s2_fit,
            "s3.brief": self.s3_brief, "s3.generate": self.s3_generate, "s3.select": self.s3_select, "s3.postprocess": self.s3_postprocess,
            "s4.render": self.s4_render, "s4.links": self.s4_links, "s4.views": self.s4_views,
            "s5.pm": self.s5_pm, "s5.packet": self.s5_packet,
        }[step]

    async def run_one(self, step):
        """Run exactly one step now, regardless of its recorded status (the
        manual walkthrough and the way to redo a step after a fix)."""
        self.mark(step, "running")
        t0 = time.time()
        try:
            note = self.step_fn(step)()
            if asyncio.iscoroutine(note):
                note = await note
        except Exception as e:
            self.mark(step, "failed", str(e)[:500])
            self.log(f"[{step}] FAILED after {time.time() - t0:.0f}s: {str(e)[:500]}")
            raise
        self.mark(step, "done", str(note)[:300])
        self.log(f"[{step}] done in {time.time() - t0:.0f}s — {note}")

    def reset(self, step):
        """Forget a step (and everything after it) so `author` re-runs them.
        Journals are kept: identical agent calls replay for free."""
        for s in STEPS[STEPS.index(step):]:
            self.state["steps"].pop(s, None)
        self.state.pop("pm_rerouted", None)
        self.save()

    async def run(self, start_at=None):
        if start_at:
            for s in STEPS[: STEPS.index(start_at)]:
                if not self.done(s):
                    self.mark(s, "skipped", "start-at")
        for step in STEPS:
            if self.done(step):
                self.log(f"[{step}] {self.state['steps'][step]['status']} — {self.state['steps'][step].get('note', '')}")
                continue
            self.mark(step, "running")
            self.log(f"[{step}] running")
            t0 = time.time()
            try:
                note = self.step_fn(step)()
                if asyncio.iscoroutine(note):
                    note = await note
            except Exception as e:
                self.mark(step, "failed", str(e)[:500])
                self.log(f"[{step}] FAILED after {time.time() - t0:.0f}s: {str(e)[:500]}")
                raise
            self.mark(step, "done", str(note)[:300])
            self.log(f"[{step}] done in {time.time() - t0:.0f}s — {note}")
        self.log(f"DONE: {self.slug} is loaded as a draft; packet at research/reviews/{self.slug}/REVIEW.md. Stage 5 is yours: publish_topic --slug {self.slug} --dry-run")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("cmd", choices=["author", "status", "step", "reset"])
    ap.add_argument("slug")
    ap.add_argument("step", nargs="?", choices=STEPS, help="for `step` (run one) and `reset` (forget it and everything after)")
    ap.add_argument("--start-at", choices=STEPS, help="author: mark earlier steps skipped (artifacts must already exist)")
    ap.add_argument("--concurrency", type=int)
    a = ap.parse_args()
    run = Run(a.slug, a.concurrency)
    if a.cmd == "status":
        for s in STEPS:
            st = run.state["steps"].get(s, {})
            print(f"{s:16} {st.get('status', 'pending'):8} {st.get('note', '')[:100]}")
        return
    if a.cmd == "reset":
        if not a.step:
            ap.error("reset needs a step")
        run.reset(a.step)
        print(f"reset {a.step} and everything after it")
        return
    log_path = run.dir / "engine.log"

    def log(m):
        line = f"{now()} {m}"
        print(line, flush=True)
        with log_path.open("a", encoding="utf-8") as f:
            f.write(line + "\n")

    run.log = log
    if a.cmd == "step":
        if not a.step:
            ap.error("step needs a step name")
        asyncio.run(run.run_one(a.step))
        return
    asyncio.run(run.run(a.start_at))


if __name__ == "__main__":
    main()
