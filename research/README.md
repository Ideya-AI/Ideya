# research/

Source-of-truth artifacts for the content pipeline (versioned in git).

```
research/
  catalog/
    topic-universe.json     # the curated topic universe + proposed taxonomy
                            # (output of the topic-universe workflow, 2026-06-16)
  topics/
    <slug>.json             # per-topic research output + dossier (one per authored topic)
```

- **catalog/topic-universe.json** — `{ proposed_categories, catalog, dropped, missing, notes }`.
  Loaded into the DB (categories + DRAFT topics) by `manage.py load_universe`.
- **topics/<slug>.json** — the research pipeline's full output for one topic (the draft
  content + the dossier of sources). The DB holds the live copy; this file is the
  durable, reviewable, diffable record. Written by the pipeline; loaded by the
  topic loader.

The pipeline design lives in `../RESEARCH_PIPELINE.md`.
