# Audit: Nuclear Energy
2026-09-22 — verdict: ready

The page tells one story and tells it in the right order. Cost opens Basics, cost is
the first question, cost is the crux, and the crux's two halves are visibly the two
halves of the argument the rest of the page has been having: an empirical half that
building would settle and a values half that it would not. The five camps are
distinct — build big with public money, phase out, run the fleet and stop, build
small, procure an attribute rather than a technology — each is named by what it
wants rather than by a posture, each is written at comparable length and with
comparable force, and each answers the objection a reader would raise. The stat
notes state values and let the details carry the argument on both sides; where
sources disagree (fleet counts, the Chernobyl toll, Russia's enrichment share, the
COP28 baseline) the page says so instead of picking. The why-now is two weeks old,
belongs to this topic, and carries its own caveat that no restart has generated yet.
Mechanical checks are clean: 0 errors, 0 warnings; 30 links, 26 ok, 4 blocked by
403 (NRC, two IEA reports, the NEA Red Book), 0 dead or placeholder. Renders are
newer than topic.json and current.

## Issues for editorial
- none

## Issues for icons
- none

## Needs research (stops the run)
- none

## Notes for the human
- Related-topic chips render alphabetically by slug (Critical Minerals, Renewables
  vs. Firm Power, Fossil Fuel Phase-Out, Net-Zero Pace), not in the `related` order
  in topic.json (firm-power, net-zero, critical-minerals, fossil-fuel). Order is
  supposed to be the mechanism for weight; this is a template or loader behavior,
  not a content defect, and it applies to every topic.
- `chernobyl-and-fukushima-death-tolls`: the green highlight falls on "Fukushima,
  evacuation 2,313". Everywhere else on the page the highlight marks nuclear, so
  here it reads as the page underlining the evacuation-not-the-radiation point,
  which is one camp's framing. It is defensible as "the focal number" (the usage in
  UBI and wildfires), and the note and detail are even-handed, so I left it. Worth a
  second look if you want the convention to be strictly "the subject row".
- Expanded Basics at 1440 leaves a tall blank in the left column whenever a narrow
  right-hand tile's detail runs long (clearest under the first tile, roughly 350px).
  Rows still align and nothing is hidden; it is the two-column grid meeting a long
  detail in a one-third-width tile. Mobile is unaffected.
- Last Actions card at 1440: "Set clean firm targets and let technologies compete"
  is the longest position name and wraps its chip to two lines, pushing "Learn more"
  onto two lines beside it. Cosmetic.
- The og share card lists four of the five positions; the square and portrait cards
  do the same. The camp dropped is the last in file order, so the loss follows
  weight, but a sharer sees four camps where the page has five.
- Scope says "Not: weapons and proliferation as a security question in its own
  right" and question eight asks whether civilian power raises proliferation risk.
  The qualifier makes it consistent, but the two sit close enough that a reader may
  notice the tension before resolving it.
- Vogtle's $35 billion appears in the page's own voice twice, in its own stat tile
  and in question one's "why". The second use is load-bearing — it is the premise
  both camps in that question share — but it is the one figure a reader meets twice.
  The Fukushima evacuation is likewise the example in the accident stat and again in
  question four, and Finland's Onkalo against Yucca Mountain appears in the waste
  stat and again in question seven, each time doing different work.
- No camp argues for new build through licensing reform and private capital rather
  than public money; question three's "Let markets decide" lean and position three
  cover the ground indirectly. Five camps already span the space, so this is a
  judgment call, not a gap.
- Poster (static/posters/nuclear-energy.pdf) and all three social cards regenerated
  2026-09-22 16:20, after the last topic.json write at 16:16.
