# Stage 1, run 1: nuclear-energy, 2026-09-15

The first topic through the v2 pipeline's stage 1, built and run the same day.
Archived whole under `research/runs/nuclear-energy/run1/` (topic.json,
evidence.json, every unit journal, every fetched source, a readable dump of
the draft). Run 2 started 2026-09-16 02:48 from an index-only topic with the
corrections below applied.

## What ran

Phase A once. Phase B once, with the stat writers rerun once for a sidecar.
Phase C three times: the first pass was abandoned after a repairer turned the
240-character crux lead into three paragraphs; the second completed with a
verdict but 25 of its 48 cuts were caused by a verifier-matching bug; the
third, after that fix, blocked on a single lint hit. The draft from the second
pass is what the archive holds.

Wall clock about 19 hours, of which about 9 were the process sleeping through
two five-hour usage resets, and about 3 were model time.

## Cost

Journals survive for Phase A, Phase B and the third Phase C pass. The two
discarded Phase C passes and the preview-era scouts were deleted with their
journals and are estimated.

| | calls | cache write | cache read | output | total input | $ notional | model min |
|---|---|---|---|---|---|---|---|
| A, the map | 12 | 684k | 2,637k | 168k | 3,321k | 8.69 | 33 |
| B, the sections | 22 | 686k | 459k | 176k | 1,144k | 9.28 | 30 |
| C, ledger and checks | 131 | 1,650k | 712k | 408k | 2,362k | 15.23 | 62 |
| one clean run | 165 | 3,019k | 3,808k | 752k | 6,828k | 33.21 | 124 |
| discarded passes, estimated | ~270 | | | | ~5,500k | ~32 | ~110 |

By model: Sonnet 100 calls, 5.9M tokens, $17; Opus 65 calls, 1.0M tokens,
$16. The three heaviest unit kinds: scouts (3.2M, mostly cache reads of
fetched pages), repairs (52 Opus calls, $5.79), verifiers (68 calls, $5.27).
A clean run is about one and a half five-hour windows on the subscription.
The design's "tens of millions of tokens" was high by a factor of two or
three; the sixty-call estimate for the stage was low by a factor of three,
because Phase C's per-source and per-field fan-out is larger than sketched.

## Wins

**The map.** The single best artifact. Eight camps named by what they want,
every camp with two or more adherents on distinct fetched sources and at
least one institution, 35 agreed facts with quotes in their sources, 13
controversial statements, 7 of 10 gaps filled by the gap round. The
cartographer found the frame rejection and the hybrid position the design
asks for. Ranking put the two big camps first without being told what they
were.

**The harvest was real research.** 83 fetched pages across five classes,
about 300 claimants and facts, and after the quote check by code only 8 were
dropped. The scouts' quotes were in their sources 95% of the time on the
first pass, once the tool-result preview bug was fixed.

**Positions are in voice and grounded.** Each position writer returned 10 to
20 sidecar claims paired to source passages. The verifier passed 92% of the
model-checked claims. The prose reads as the camp's own case, and lint found
no self-rebuttal in any of the eight. The ideological Turing test held for
the five main camps on a read.

**The crux converged with v1 independently.** Cost as a property of the
technology versus of how it has been built, with every camp placed on a
branch. Subtraction and root divergence worked as designed.

**Every hard claim was checked.** 275 ledger claims, every one traced to a
fetched page by normalized quote match before a model judged it, and every
URL resolved when written. A hallucinated source was structurally impossible
and none appeared.

**The machinery held.** Sixty-odd resumable units, three phases that skip
what is done, a pause that sleeps through a usage reset and resumes, a
blocked marker that a rerun clears. Two window resets passed with no human
action. Every defect below was found by reading a journal, which is what the
journals are for.

## Losses

### Defects found and fixed during the run

1. **Tool results reached agents as 2KB previews.** Claude Code persists a
   large tool result to a file and shows a preview. Scouts were quoting from
   memory. `ToolAnnotations(maxResultSizeChars=…)` on the fetch tool; now a
   §11 finding in PIPELINE.md.
2. **Scout and gap quotes not in their sources** reached the cartographer.
   Code now quote-checks both harvests before any cartographer sees them, and
   drops an unverifiable agreed fact with a record.
3. **PDF artifacts broke the quote match.** A page number or a footnote date
   spliced into a sentence. Near-match now accepts 60% of six-word shingles
   or a contiguous twelve-word prefix.
4. **Stale utilization after a sleep** looped the orchestrator on one-minute
   naps. The reading is cleared after a sleep-through.
5. **The basics sidecar was filed on the wrong field** and stat writers
   returned no sidecar, so 48 basics claims were unsourced. Stat writers now
   return a sidecar over note and detail.
6. **Extractors quoted fragments and skipped repeated figures.** Coverage is
   now per item, and the extractor is asked for whole sentences.
7. **Proponents were cut as unsourced claims.** A camp's proponents are the
   map's adherents; code checks them against the map and cuts unknown names.
8. **An unbounded repairer** rewrote the crux lead as an essay. Repairs are
   bounded by the loader caps and 1.3 times the original length; an oversize
   repair is rejected.
9. **Action descriptions were extracted as claims.** Actions are lint-only;
   the URL check is their proof.
10. **Verifier verdicts keyed by ledger id** did not survive renumbering
    between rounds, so reused returns matched nothing and 25 good claims were
    cut. Verdicts are keyed by position within the unit.
11. **UK spellings went to Opus repairers.** Lowercase forms are fixed by
    code; capitalized ones are left as proper nouns.
12. **Phase C unit names were keyed by section or source**, so a changed
    draft could reuse a stale return. Names are content-addressed.

### Quality losses in the output

- **Basics leaned on the wrong sources.** Six of 18 tiles from Wikipedia,
  four from one critic's op-ed. The cartographer picked the stat list without
  preferring reference or official sources, and the attribution rule then
  turned two notes into "Ramana argues", which is not a stat note.
- **Basics missed the staples.** No capacity factor, waste volume, reactor
  age, top producers or uranium reserves; coverage tilted to the cost fight.
- **Two weak tiles**, operator training months and a trade group's demand
  forecast, whose details drifted into editorial commentary.
- **One ranked series mixed gigawatts with reactor counts.**
- **Wikipedia's published date came through as the page creation date.**
- **Questions were open and well-shaped but long and academic**, up to 230
  characters, with four of nine on cost and finance.
- **Three of eight camps were sub-issues** (ratepayer risk, repositories,
  host-community consent) rather than answers to the headline question, and
  one camp listed the EIA, the IPCC and Lazard as adherents.
- **Length discipline failed in Phase B.** The crux's empirical branch ran to
  about 6,000 characters, five times the render budget; one position detail
  passed 3,000 in one paragraph.
- **The crux lead lost its snap** when attribution was forced on it. Stage 2
  owns the lead, but the repair should not have been needed.
- **The draft is US-heavy** because the harvest was.
- **Bot walls starved the camp class.** 57 of 71 failed fetches were HTTP
  403, hitting advocacy sites hardest; the camp class saturated at 5 pages.
- **Writers wrote figures from memory.** Most repair cost came from numbers a
  position or question writer could not pair with a passage.

### Design-level lessons

- **Weak upstream criteria become Opus repairs.** Every unsourced number a
  writer produced cost an Opus call downstream. The exit-criteria principle
  (§9) applied to the writer means: no passage in hand, no number.
- **Presentation fields need the map, not the ledger.** Proponents and the
  representative are who holds the view; the map is their check. Fields whose
  proof is elsewhere must be exempt from extraction or the ledger cuts them.
- **Every repair needs a bound.** A model asked to rewrite a field will write
  the field it thinks the topic deserves.
- **Reused returns must be keyed by what they were handed.** Any name keyed by
  a position in a run rather than by content will eventually serve a stale
  answer.
- **The scout's claim is only as good as the extractor's text.** PDF and
  sidebar artifacts are common enough that quote matching must tolerate them.

## Corrections applied before run 2

Prompts: writers told that a figure without a passage in hand is not written;
the cartographer told that a camp answers the topic's own question, that most
topics have three to six, and what a stat tile is (one measured quantity with
a unit from a reference or official source, the quantities a reader needs to
picture the subject first); question text about 120 characters and never over
200, detail at most 1,200; crux subtitle 500, branches 1,800 each, stated as
ceilings; position description opens with the case, not the camp's history;
ranked series share one unit.

Code: lint defects are handed to the forced-cut round; the ledger and a
summary are saved to `evidence.json` even on a criteria failure; Phase B
checks the ceilings and reruns a breaching unit once, recording what stays
over; second-round scouts run in parallel; the stat list drops camp- and
critique-sourced tiles when the rest meet a floor of ten; a 401, 403, 429 or
503 is retried through the Wayback Machine; Wikipedia gets no published date.

## What run 2 must show

- Cuts under 20 on a ledger of a similar size, with none caused by a check.
- No field over its ceiling after Phase B, and no repair over its bound.
- Basics drawn from reference and official sources, with the staples present.
- Three to six camps, each an answer to the headline question.
- Question text under 200 characters.
- Fewer bot-wall failures and a saturated camp class.
- One clean Phase C pass to a verdict, under 7M tokens.
