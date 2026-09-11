# Democratic Backsliding & the Populism Debate — review packet (2026-08-11)

**Status:** DRAFT loaded as `democratic-backsliding-populism`. Stages: research 3 fix rounds (+3 post-run fact fixes applied by the orchestrator), distribute 1, icon 1 round, views 2 rounds.

## Substance gate (stage 1)

- **neutrality: PASS.** Camp coverage "genuinely complete for the diagnostic fight as actually conducted"; two adjacent schools (deliberative/sortition renewal, epistocracy) noted absent but non-blocking.
- **steelman: PASS.** "Every camp reads as written by a believer"; National Conservative called out as notably strong.
- **fact-source: FAIL → fixed.** 3 blocking defects (a US-specific V-Dem constraints finding presented as global; PopuList chart points not matching the source's published series; an unsourced "stronger predictor" research claim). The workflow's fix loop did not land them, so the critic's exact prescribed corrections were applied to the draft before persisting — annotated in the dossier's verdicts. All other load-bearing claims verified against live sources (V-Dem 2026, Freedom House 2026, PopuList v4.0, TBI, OECD).
- **crux: PASS.** The three-pole lead (disease / immune response / misdiagnosis) maps cleanly onto the camps.

**⚠ Missing planned camp:** the "Technocracy Critic" position agent failed all structured-output retries — the topic ships 5 of 6 planned positions. The neutrality critic judged the absence non-blocking (the technocratic-overreach critique is partially carried by Corrective Populist). **Your call:** accept 5, or order a re-run to add the camp.

28 editorial notes from the critics are preserved in `research/runs/democratic-backsliding-populism/record.json` (verdicts). Highlights worth a look: actions tiering favors the two anti-populist camps' actions at tier 1 (weight doesn't fully explain it); the RepresentUs RCV action is a loose fit for the Corrective Populist camp (the technopopulism essay is the on-voice one); Levitsky & Way year-range slippage (1999–2013 vs 2000–2013).

## Presentation gate (stage 2)

- compact-self-sufficiency: PASS · reading-level-fit: PASS · above-fold-selection: PASS (17 notes).
- Fold above "Go deeper": basics 4/9, questions 4/7, positions 5/5.

## Post-gate content edits (orchestrator, all facts preserved — outside the patch whitelist)

1. Ranked series labels tightened ("Autocratizing (41% of world population)" → "Autocratizing", shares moved into the note); "2026 (most recent elections)" → "2026"; series values de-unitized ("44 countries" → "44"); populist-leaders row glosses moved to the note.
2. Stats reordered so the poster band (first 3) carries one ranked + two radials.
3. Crux subtitle/empirical/values compressed to the house register (247/458/465 → 178/347/325 chars) — they were ~30% longer than any shipped topic and drove the poster overflow.
4. National Conservative steelman shortened to "Reclaiming captured institutions is democracy working, not backsliding."
5. View-critic content fixes: `&amp;` entity literals (3), markdown asterisks, OECD trust detail trimmed 797→440 chars, lean label "Institution-dependent" → "Context-bound" (overflowed at 320px), paragraph breaks inserted into all five position details.

## Icon

Winner: candidate 2 — consistent duotone fills (1 and 3 leave figures/heads unfilled), most compact composition, ballot-box focal point survives 40px. Candidates in `research/icons/candidates/democratic-backsliding-populism/`. Scene: crowd + speech bubble / ballot box mid-slip / columned institution, deliberately verdict-free.

## Views

Desktop / mobile-390 / mobile-320: clean after round-2 fixes (screens re-rendered against final content). OG/sq/pt cards render; poster **fits with 16px slack** (`democratic-backsliding-populism.pdf`).

**⚠ Social cards clip on this topic** — see Engineering issues; the OG/pt overflow is title-length-driven and the sq card is broken independent of content. A verified content-side option: retitle to **"Democratic Backsliding & Populism"** (33 chars → OG overflow exactly 0, portrait +106→+18px). Title is identity — your call, and it doesn't fix sq.

## Engineering issues (for you — pipeline does not touch CSS)

From `view-findings-social.md` (measured, with UBI as control):
- **share.html `.sq` card cannot fit its CTA at any title length** — already ships broken on published UBI's square card. `.sq .dk` flex:none/533px vs `.lt` needs ≥594px.
- **OG card bottom-clips summary+CTA when the title is long** (`justify-content:safe center` falls back to top-align); ~40% of catalog titles (40+ chars) will hit this. Durable fix: stack art above title on OG, or scale title size by line count.
- **Portrait card has ~0.2px of fit margin** even when it fits; CTA hides behind the dark band at 3+ line titles.
- False invariant comment at `templates/topics/share.html:59-60`.

From the screens critic:
- **Lean-chip overflow at 320px** (real-user bug): `.lean .lt .lp` nowrap + no min-width — fixed for this topic by the shorter label, but the CSS should wrap/ellipsize (`static/css/ideya.css:326`).
- **Ranked-tile label column at mobile widths**: labels can collide with bar tracks; cap the label column or stack label-above-bar under ~400px.
- **?expanded=1 capture CSS breaks mobile**: `#main .q-xtra { display:grid !important }` reinstates the desktop grid at 320/390 (capture harness only, live page fine) — scope the overrides per breakpoint; also mobile expanded captures truncate at 22,000px so mobile depth layers of Positions/Crux/Actions went unreviewed.
- **Position dot mis-aligns on wrapped names** at 320px.
- **Scope card "Not" needs a colon** (`detail.html:137`) — reads as a typo on every topic.

## Check in 5 minutes

1. The missing Technocracy Critic camp — accept 5 positions or order the re-run.
2. The retitle question ("Democratic Backsliding & Populism") for the social cards.
3. Actions tiering asymmetry + the RepresentUs action's camp fit.
4. Skim the two ranked tiles and the crux band on `desktop-1440.png` — the most-edited areas.

## To publish

```
.venv/bin/python manage.py load_topic_draft --file research/topics/democratic-backsliding-populism.json \
  --slug democratic-backsliding-populism --title "Democratic Backsliding & the Populism Debate" \
  --category governance --status published --image-brief research/icons/democratic-backsliding-populism.md
```
→ `manage.py load_universe` (wires the 5 related-topic edges) → set `reviewed_at` → `check_links --topic democratic-backsliding-populism` (expect 0 dead / 0 placeholder) → commit dossier, topic JSON, icon assets, review packet.

## Link check (2026-08-11, pre-publish)

16 links: 14 ok after inlining 2 renamed-URL redirects (IDEA GSoD, RepresentUs) · 2 "blocked" are bot-refusals (fetchable in a browser) · 0 dead · 0 placeholder.

## Stage-5 resolution (2026-08-12 — decisions delegated to the agent by the human)

1. **5 positions accepted** (no Technocracy Critic re-run): the neutrality gate judged coverage complete; the camp's core claim — technocratic closure provoked the revolt — is carried by Corrective Populist and named in the crux subtitle. Revisit if reader participation exposes the gap.
2. **Retitled to "Democratic Backsliding & Populism"** (DB + draft JSON + catalog): fixes the OG social card outright, improves portrait, and matches the house register (no "…Debate" suffixes elsewhere). Side-effect: the shorter title crossed into the poster's 80pt `title-sm` bucket and re-broke the fit; the bucket boundary was moved (>32 chars → `title-xs`, poster.html) — all five topics' posters re-checked (wildfires' 42px overflow pre-dates this and is logged for its own review pass).
3. **Actions tiering balanced**: National Conservatism Statement of Principles promoted to tier 1 (tier 1 now: V-Dem report / Measuring Backsliding / GSoD (untagged) / NatCon). **RepresentUs untagged** from Corrective Populist — RCV is a good-government reform, not a populist project; the technopopulism essay remains the camp's on-voice action.
4. **Levitsky & Way window** corrected to 1999–2013 in the Measurement Skeptic description.

Published locally 2026-08-12 (authoring DB; live site is down pending launch): status=published, reviewed_at set, 5 related edges live, search index rebuilt. Note: `check_links`'s two "blocked" results are bot-refusals, verified reachable.
