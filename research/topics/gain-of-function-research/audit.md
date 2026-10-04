# Audit: Engineered Pandemics
2026-09-30 — verdict: ready (re-audit)

The one issue raised in the previous packet is fixed: the local action now links to the
NIH Guidelines themselves (osp.od.nih.gov/wp-content/uploads/NIH_Guidelines.pdf), which
check_links resolves and which carries the card’s claim about community members on
institutional biosafety committees; the Federal Register URL that redirected to an EPA
hydrofluorocarbon notice is gone from the file and from the rendered page. The fix broke
nothing around it — the Actions grid still reads ten cards in two columns at 1440 and one
at 390, and the card’s kind label, title and body are unchanged. Three items the previous
packet listed only as notes were also addressed: the BSL-4 arithmetic now reconciles (all
but two of the 57 BSL-3+ labs are operating, so 55 plus 51 gives 106), the 1918-pandemic
tile headlines the full range 0.11–0.89 rather than its top end, and the dated Anthropic
sentence with no followable source has been removed from the AI question. Read again end
to end, the page still tells one story: a July 2026 US policy, the two chokepoints it
raises, seven questions posed without presupposing their answers, five camps named by what
they want and matched in length and energy, and a crux about where the burden of proof
sits that follows from them. Nothing on the page would mislead or confuse a reader.

## Issues for editorial
none

## Issues for icons
none

## Needs research (stops the run)
none

## Notes for the human
- Template, carried forward: the crux lead renders a space before the punctuation that
  follows the highlighted span — “both sides , where should the burden of proof sit ?” —
  on desktop and mobile. The string in topic.json is clean and the share cards render it
  correctly. Views now logs no template defect, so this one is only visible on the page.
- Layout, carried forward from the views stage: the range value “0.11–0.89” fills the
  narrow one-third tile at 1440 and pushes its unit “% a year” onto a second line. Nothing
  clipped; mobile is unaffected.
- Questions, “Who should decide whether a risky experiment goes ahead?”: the
  independent-body paragraph still runs about twice the length of the experts-in-the-field
  paragraph and names three advocates against one. Both arguments are stated fairly; the
  six other questions are balanced to within a dozen words.
- Repetition, carried forward: the gene synthesis industry having asked Congress to
  regulate it appears in the 1918-fragments stat detail, question four and the
  mandatory-screening steelman; the order-split-across-providers gap likewise. Each
  appearance does work where it sits, but a reader going deep meets both points three times.
- check_topic_text raises one warning: why_now_source_url repeats why_now_source_label.
  Benign — the whitehouse.gov filename is the policy’s title.
- check_links: three 403s (Oxford Academic, CSET twice) are bot blocking, not dead links;
  the Harvard redirect is a trailing slash. The new NIH Guidelines PDF answers 200 to the
  checker and 403 to a bare curl, which is the same Cloudflare behavior.
