# Audit: AI Alignment
2026-09-23 — **ready**

The page tells one story and keeps to it: alignment methods exist, several of them work
measurably, and the argument is over whether anyone can confirm from the outside that they
worked. Every section feeds that thread. Basics is unusually disciplined — sixteen stats, each
with the caveat its own authors gave it, and eight of them are results the labs published
against their own interest. The six camps are named by what they want rather than by posture,
they run 220–308 words apiece, each one is allowed to answer the objection made against it, and
each one has an action pointing at it. The crux follows from the questions above it and the
share cards carry it faithfully. Two mechanical checks pass clean: `check_topic_text` reports
0 errors, `check_links` 25 OK and 1 redirect. Renders (02:34–02:35) are newer than `topic.json`
(02:31) and current. Nothing on the page would mislead a reader.

## Issues for editorial
none

## Issues for icons
none

## Needs research (stops the run)
none

## Notes for the human

- **Template defect, Actions tile, 1440 and 390.** In an action tile that carries a position
  label, the "Learn more" kicker wraps to two lines ("Learn / more") while unlabeled tiles keep
  it on one — the label text crowds the row. Visible on Anthropic Alignment Science blog and
  Transformer Circuits Thread at 1440, and on those two plus Redwood Research at 390. `views.md`
  logged it for desktop and marked mobile pass; it is present at both widths. Recurs on every
  topic whose action links to a position. A `white-space: nowrap` on the kicker, or moving the
  position label to its own row, fixes it. The pipeline does not edit templates.

- **Position 1 re-spends two Basics tiles.** "Align models through empirical training and
  evaluation" opens by citing 13.0 → 0.4 percent, 86 → 4.4 percent, 3,000 hours of red teaming
  and ~1 percent extra compute — all four already in stats 1 and 7 with the same wording. A
  reader who expanded Basics meets them twice in a row. Position 6 ("Halt frontier scaling")
  recaps four stats too but does it in prose without a single number, which reads as a camp
  marshaling evidence rather than a reprint; position 1 could do the same. Symmetric across both
  wings, so it is not an unevenness problem, only a minimalism one.

- **Position 1 splices two versions of one result.** The stat tile is careful: 3,000 hours and
  4.4 percent belong to the first classifier, the ~1 percent overhead to the January 2026
  successor, and that successor's 1,700 further hours turned up one high-risk vulnerability. The
  steelman runs the three facts together as properties of one system. It is the camp's voice and
  the honest version sits directly above it in Basics, so no reader is misled, but it is the one
  place where a steelman leans on the tile it came from.

- **"The number went the wrong way" (stat 2, GPT-6 Astra).** The tile's headline number is
  57 percent *fewer* misalignment flags; the detail's "the number went the wrong way" means the
  monitorability score, and the colon that follows says so. One beat of ambiguity at the tile
  where the reader is most likely to skim.

- **Crux subtitle asserts something one camp on the page denies.** "Nearly every dispute in this
  field resolves into that one question" — but "Treat alignment as ordinary engineering
  reliability" argues that the inner-goals framing is an import from thought experiments and not
  the relevant question at all. The lead question itself is broad enough to hold them (it says
  "disposed to do," and the empirical pane lists hostile testing and ordinary-use monitoring
  alongside internals), and the values pane gives that camp its side. It is the one sentence
  where the page's own voice picks a frame. Worth a second look, not a defect.

- **Glance layer of Basics tilts toward failure.** Across all sixteen the split is roughly six
  results that work, eight that concern, two neutral — balanced. But the seven shown before
  Go deeper run two positive, four negative, one mixed. The negative findings genuinely are the
  news of the last two years and position 1 concedes them by name, so this is defensible; it is
  the tilt a reader meets if they never expand.

- **The foundational stat sits fourteenth.** "Human feedback against raw model size" is the tile
  that explains what alignment training *is* — and it is behind Go deeper, after thirteen
  frontier results that assume the reader knows what covert actions, episodes, chain-of-thought
  and behavioral audits are. Most of the notes are self-explaining, so a newcomer can follow, but
  the order gives them the frontier before the foothold.

- **Missing camp, judgment call.** The "alignment discourse is itself the problem — it serves the
  labs and distracts from present-day harm and power concentration" position has no tile of its
  own. The declared scope ("Methods, not policy") excludes it, and position 4's closing sentence
  carries its sharpest point (safety theater, needless refusals, concentration in a few firms).
  Flagging only because a reader who follows the field will look for it.

- **ControlAI action redirects.** `https://controlai.com/` → `https://controlai.org/`. Resolves;
  worth updating the URL when convenient.

- **Portrait share card** has a tall empty band between "Explore the full debate" and the dark
  block. The og and square cards are tight. Cosmetic.

- **Source-label oddity, stat 3.** "Anthropic, Reasoning models don't always say what they think,
  3 April 2025 (arXiv:2505.05410)" pairs an April date with a May arXiv identifier. The URL is
  the blog post and resolves; the arXiv record would settle whether both belong.
