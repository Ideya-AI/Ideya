# Content Moderation & Online Speech — review packet (2026-08-12)

**Status:** DRAFT loaded as `content-moderation-free-speech` — NOT published. Stages: research 3 fix rounds (+4 post-run fact fixes), distribute 1 (failed once on a structured-output cap, recovered via cached resume; +2 whitelist-rejected reading-level fixes applied by orchestrator), icon 1 round, views 2 rounds.

## Substance gate (stage 1)

- **neutrality / steelman / crux: PASS.** Six camps (plan's five + a Harm-Accountability Advocate the fix loop added): Duty-of-Care Reformer, Speech Maximalist, Due-Process Reformer, Common-Carrier Regulator, Jawboning Hawk, Harm-Accountability Advocate.
- **fact-source: FAIL → fixed** per prescriptions: (1) why_now legal overstatement — the March 2026 Meta verdicts *routed around* Section 230 on a product-defect theory; no court "cracked the shield" (rewritten to the accurate holding); (2) the DSA 6% fine cap re-sourced to EUR-Lex Art. 74 (the cited page didn't contain the figure); (3) two perishable roster counts dropped (designated-VLOP count was stale-wrong; reviewer-body count outdated); (4) a spliced Brandeis quotation unspliced to the genuine "more speech, not enforced silence" sentence.

22 editorial notes in the dossier verdicts.

## Presentation gate (stage 2)

- compact-self-sufficiency / above-fold-selection: PASS. **reading-level-fit: FAIL → fixed** (whitelist correctly refused both): "jawboning" glossed as "government pressure on platforms" at its first compact appearance; the NCLA action de-acronymed. Fold: basics 4/7, questions 4/7, positions 6/6.

## Post-gate content edits (orchestrator, facts preserved)

Poster required real restructuring (501px over → fits 14px slack): this topic's survey items and case holdings made sentence-length ranked rows — the Pew tile became a radial (83%) with all three figures in its note, SCOTUS rows became bare case names (context in the note), band labels/notes tightened. Plus the screens critique: deterministic smart-quote pass, US-spelling normalization, en-dashed vote splits, quoted book title, all 7 question details paragraph-broken, DSA unit → "%". Jawboning Hawk pinned to slate (teal reserved for the digital category chip).

## Icon

Winner: candidate 3 of 4, first batch — three speech bubbles through an open gateway, level scale on the lintel; verdict-free by construction; 40px thumb reads.

## Views

Desktop/mobile/expanded: clean after fixes; links 0 dead / 0 placeholder (2 redirects to inline at publish); poster fits (14px). Social: OG/sq/pt clean — sq shows a by-design clamp ellipsis landing on "shoul…" (cosmetic; reword the summary if it bothers you).

## Engineering fixed this round (all topics)

- **OG t-mid/t-long clamp never stepped down** (systemic since the rebuild — measured near-clipping on UBI): now steps 4→3; DBP's committed OG regenerated.
- Mobile ranked rows: real label-column floor + bar minimum (names no longer shatter at 320).
- **Capture harness now raises the reveal layers** — mobile expanded captures were silently omitting every section's normal/deep items (live page unaffected; Actions made it visible).

## Open decisions for you

1. **Doc-vs-implementation conflict:** DESIGN_SYSTEM.md says category colors are discovery-tier only, "never on a Topic page" — but topic pages render colored category chips, and on this topic the governance-purple chip exactly matches a position dot. The critics recommend neutral-ink chips on topic pages (system-wide change). Your call.
2. Token collisions (cat-tech=pos-blue, cat-econ=pos-amber, focus-ring=pos-blue) — still open from prior packets; per-topic palette pinning is the current insurance.
3. The sq card's "shoul…" ellipsis word-break cosmetics.

## Check in 5 minutes

1. The four corrected facts (especially the why_now legal rewrite — it's the topic's hook).
2. The sixth camp (Harm-Accountability Advocate) — fix-loop addition; steelman quality.
3. The Pew radial restructure (was a 3-row ranked; all figures preserved in the note).

## To publish (after your review)

```
.venv/bin/python manage.py load_topic_draft --file research/topics/content-moderation-free-speech.json \
  --slug content-moderation-free-speech --title "Content Moderation & Online Speech" \
  --category digital --status published --image-brief research/icons/content-moderation-free-speech.md
```
→ `load_universe` (4 related edges) → reviewed_at → `check_links` → inline the 2 redirects.
