# refresh-topic — reference

Longer detail for [`SKILL.md`](SKILL.md): the file schema, the verdict shape, the
editorial rules to enforce, the staging→publish mechanics, and the human-gate
snippets. Authority for the content model is `RESEARCH_PIPELINE.md` and `topics/models.py`;
the hand-built `research/topics/nuclear-energy.gold.json` is the **content** quality bar.

> **Shape caveat.** `nuclear-energy.gold.json` is in **export shape**
> (`{title, summary, scope_*, why_now, sections:[…]}`, what `export_topic` emits) —
> read it for the writing/quality standard, but **do not feed it to `load_topic_draft`**;
> the loader wants `{draft:{overview,basics,…}}` and would silently load an empty topic
> from it. For a *loadable-shape* example, see `research/topics/nuclear-energy-pipeline.json`
> (or any `-calibration`/`-refresh` file the pipeline emits).

## The file: `research/topics/<slug>.json`
The loader (`topics/management/commands/load_topic_draft.py`) reads
`{ draft, verdicts, plan_positions }` (a bare `draft` object also works). `verdicts`
is stored on `Topic.research_dossier` for the reviewer; `plan_positions` is carried
for provenance but not consumed. Fields below are what the loader actually maps — the
models hold more (e.g. Stat `series`/`wide`/`range_*`), so `ranked` / `sparkline` /
`range` viz need either those fields plus a loader extension or a fall back to
`bar`/`radial`. The loader also (re)seeds the topic's 3 Add-your-view prompts on
every load, and warns on placeholder action URLs and truncated stat units/notes.

```jsonc
{
  "draft": {
    "overview": { "summary", "scope_covered", "scope_excluded", "why_now" },
    "basics": {
      "intro": "lead-in copy",
      "stats": [{
        "label", "value",
        "unit",                                        // DISPLAY TOKEN <= 12 chars ('%', '$B/yr')
        "viz": "bar|ranked|radial|range|sparkline",   // default bar
        "fill_pct": 0-100,
        "note",                                        // one tight sentence (visible layer)
        "detail",                                      // deeper analysis shown on tile expand
        "tier": 1..n,                                  // 1 = leading; new tier at a natural drop-off
        "source_label", "source_url",
        "source_published": "2025 | Q1 2025",          // when the data is from
        "source_accessed": "YYYY-MM-DD",               // when you verified it
        "reveal": "condensed|normal|deep"              // reading depth, default condensed
      }]
    },
    "questions": [{ "text", "kind": "empirical|value",
      "why",                                           // 1-2 tight sentences (visible layer)
      "detail",                                        // deeper analysis shown on expand
      "tier": 1..n, "reveal" }],
    "positions": [{
      "name", "steelman",                              // one-line, in the side's own voice
      "description",
      "detail",                                        // deeper in-voice background on card expand
      "tier": 1..n,                                    // drives the Go-deeper split
      "proponents": "comma, separated, names",
      "representative_name", "representative_note",
      "prevalence_weight": 0-100,                       // seeds default order (mainstream leads)
      "spectrum_position": -n..n                        // optional axis metadata, not the order
    }],                                                 // colour is auto-assigned by index
    "crux": { "lead", "lead_highlight", "subtitle", "empirical", "values" },
    "actions": [{
      "kind": "learn_more|donate|volunteer|policy|local|submit_view",
      "title", "description", "url",
      "for_position": "<a position name>",              // maps the action to that Position
      "tier": 1..n,
      "reveal": "condensed|normal|deep"
    }]
  },
  "verdicts": [{ "pass": true, "issues": ["..."], "fixes": ["..."] }],
  "plan_positions": []
}
```

**Verdicts** are the adversarial gate's output — one per element checked, mirroring the
authoring pipeline's critics (neutrality / steelman / fact-source / crux). `issues`
names what's wrong (tilt, misattributed fact, dead link, stale number, asymmetric
sourcing); `fixes` are the concrete corrections. Carry them in the file so the diff in
SKILL.md stage 3 traces back to a verdict, and so the dossier records *why* each change
was made.

## Editorial rules to enforce (stage 2)
From `RESEARCH_PIPELINE.md` §2 + §8 — the same bar published content must meet:
- **Neutral by intention** — no house position, no section tilts.
- **Genuine steelman per position** — each side's strongest case *in its own voice*,
  such that a real proponent would endorse it. Not strawmen, not balance theatre.
- **Honest non-balance** — include every genuine position, each steelmanned; never
  force 50/50. Asymmetry is carried honestly by Basics (shared facts), each position's
  real prevalence, and the Crux — never a house verdict. No false balance; no
  fringe-exclusion-by-omission.
- **Crux must narrow** — to where disagreement *actually* sits, plus the
  if-empirical / if-values split. No new facts. Not "both sides have a point."
- **Accurate + sourced + dated** — every Stat verified, with `source_published` and
  `source_accessed`.
- **Recency pass** — never trust first-pass recollection; fetch genuinely-current data
  for time-sensitive figures (the "good-but-slightly-stale baked in" failure).
- **Durable by default** — prefer structural / long-run figures that age well; isolate
  + date the genuinely perishable ones; minimize perishable surface area.
- **Source tiers** — primary/official + peer-reviewed > reputable journalism/research >
  advocacy/opinion. Basics prefers cross-accepted sources; Positions are attributed to
  real proponents (the proponent *is* the idea's source).
- **Depth = distill down** — condensed (headline + one line) / normal (explanatory
  body) / deep (caveats, representative, proponents, sources). Same six-section
  skeleton at every depth; more room adds evidence + nuance, never new sections.

## Why a staging slug (stage 4)
`load_topic_draft` does `update_or_create(slug=...)` and then **deletes and rebuilds
that topic's sections** inside one transaction. So loading the refresh onto the *live*
slug with `--status draft` would flip the published topic to draft (invisible to the
public — drafts render only to staff) and replace its current content. That both takes
the page offline and removes the live version you wanted to diff against.

Loading to `<slug>-draft` keeps the live topic untouched and lets a reviewer preview
both as staff. The loader's own docstring endorses this ("Use a distinct --slug to keep
a gold standard intact while comparing"). On approval you publish by re-running the
loader onto the canonical slug — it's `@transaction.atomic`, so the in-place rebuild of
the live topic is all-or-nothing (no half-rendered page).

## Publish + reset the clock (stage 5)
Publish the approved content in place, then clean up staging:
```
python manage.py load_topic_draft --file research/topics/<slug>.json \
  --slug <slug> --title '<Title>' --category <cat-slug> --status published

python manage.py shell -c "from topics.models import Topic; \
  Topic.objects.filter(slug='<slug>-draft').delete()"
```
Set human-approval time (the loader sets `researched_at`, not `reviewed_at`):
```
python manage.py shell -c "from django.utils import timezone; from topics.models import Topic; \
  Topic.objects.filter(slug='<slug>').update(reviewed_at=timezone.now())"
```
`reviewed_at` resets the cadence clock (`last_touched = reviewed_at or researched_at`,
read by `topics_due`) and feeds the reader "Last reviewed: \<month year\>" badge.

**Admin path (light changes):** `TopicAdmin` lists `status` and `researched_at`, has
**Publish selected topics** / **Unpublish** actions, and exposes `reviewed_at` as an
editable field (Research provenance fieldset; `researched_at` + `research_dossier` are
read-only there). The bulk Publish action sets status only — still set `reviewed_at`
yourself.

Finally `git add research/topics/<slug>.json` and commit — the JSON diff is the
durable content history.

## Companion commands
In-tree today: `topics_due` and `load_topic_draft`. `check_links` (per-topic link
audit) and `export_topic` (dump the live topic back to its JSON) are companion
freshness commands this workflow drives — confirm with `python manage.py help` and read
each command's `--help`. If one isn't available yet: read "is it due" from
`topics_due --json`, and treat the committed `research/topics/<slug>.json` as the
durable current copy to diff against. `topics_due` reports the queue globally (no
`--topic` flag) — filter its `--json` output by slug when you need one row.

## Related
- `RESEARCH_PIPELINE.md` — the authoring pipeline this upkeep loop mirrors.
- `research/README.md` — what lives under `research/` and why.
- `deep-research` skill — the fan-out + adversarial-verification harness for stage 2.
- `schedule` skill — for the weekly link sweep / cadence backstop runs.
