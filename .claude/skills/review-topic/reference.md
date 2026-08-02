# review-topic — reference

Detail for the [SKILL](SKILL.md): finding shape, packet template, tuning-log contract.

## Finding shape

```
{ severity: "blocking" | "advisory" | "note",
  item:     "<exact stat label / question text / position name / view element>",
  issue:    "<what's wrong>",
  evidence: "<what was checked — quoted source text, image region, computed fold>",
  fix:      "<concrete correction>",
  routing:  "content" | "presentation" | "code-css" | "process" }
```

- `blocking` = would mislead a reader or embarrass the product if published.
- `advisory` = should fix before/at next touch.
- `note` = polish; packet-only, no routing.
- Blocking findings get one quick same-model second look before any fix is applied;
  this replaces the heavyweight per-finding adversarial-verify fleet used in the
  one-off 2026-07-31 housing deep review (kept there as the calibration reference).

## Routing mechanics

- **content, draft topic:** edit `research/topics/<slug>.json` directly, record each
  change in the packet cycle's changelog (old → new + source), then
  `load_topic_draft … --status draft` and re-render affected views. Facts changed here
  must carry a working source, same bar as stage 1.
- **content, published topic:** never touch the live slug — hand the findings to the
  `refresh-topic` skill (its `args.link_report`-style seeding works; format each as one
  line: `SECTION/item: old → new (source URL, date)`), which owns the
  changelog-approval-staging flow.
- **presentation:** bake `args.fix_only: [{issue, fix}, …]` into a `distribute_topic.js`
  run script (recipe in `author-topic/reference.md`), run, persist, reload, re-render.
- **process:** the incremental-vs-transformative rule and the log-entry format live in
  `research/PIPELINE_TUNING_LOG.md` (top of file). When editing a critic prompt, grep
  the other two workflow files for the MIRROR sibling and port the same change or log
  why not.

## Packet cycle template

```
## Cycle <n> — <date> (<dimensions run>)

**Verdict:** <publish-ready | fixes applied, re-render clean | blocked on X>

### Findings (<blocking>/<advisory>/<note>)
- [severity|routing] <item>: <issue> → <fix / what was done>

### Residual audit
- <prior finding>: applied | STILL OPEN (→ re-entered above)

### Changelog (content fixes applied this cycle)
- <SECTION/item>: <old> → <new> (<source>)

### Process lessons
- <applied: one-liner + PIPELINE_TUNING_LOG.md anchor> | <PROPOSED: one-liner — see log + chat>

### Engineering issues (code/CSS — human)
- <finding>

### For the human
- <the few judgment calls / approvals needed>
```

## Cadence

On-demand only (like author-topic and refresh-topic): run after authoring stage 4,
after a refresh applies, or when the human asks. `topics_due` remains content/link
freshness only.
