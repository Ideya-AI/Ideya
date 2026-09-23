# Audit: AI Alignment
2026-09-23, verdict: ready

The page tells one story. Basics runs from what current methods achieve (covert actions cut by deliberative alignment) through how they are failing or losing their instruments (monitorability, faithfulness, agentic tampering, alignment faking, evaluation awareness) to how the field is resourced. The seven questions (generalization, scheming, chain-of-thought legibility, values against containment, whose values, automated research, helpfulness) each carry two readings of similar length. The six camps each want something distinct and are named by what they want. Detail lengths run 220 to 308 words, and every camp gets a "we are told" rebuttal. The crux (can anyone check from the outside what a system is disposed to do) grows out of the questions, and the halt camp's resumption criterion and the containment camp's premise both point at it. The why-now event, OpenAI's September 16, 2026 misalignment disclosures, belongs here. Both mechanical checks pass: 0 text errors, 27 of 27 links ok. The renders are newer than topic.json (04:19 to 04:21 against 04:17). The live page at 1440 matches them, and its Go deeper buttons toggle to "Show less" as they should. The three issues from the previous audit are resolved. The sabotage scenario now says it covered twelve of fourteen models, and the automated-research lean labels now answer the question asked. The repeated rules-against-reasons argument remains, and it is now a note. Nothing left on the page would mislead a reader. What remains is for the human's judgment.

## Issues for editorial
none

## Issues for icons
none

## Needs research (stops the run)
none

## Notes for the human
- Repeated argument (carried from the last audit). The argument that reasons generalize and rules do not still appears in four places: the covert-actions detail ("a written rule can change conduct in situations its authors did not anticipate"), the 84-pages detail, the optimistic paragraph of the first question, and the first position. A reader meets it four times.
- Other points the reader meets repeatedly. Evaluation awareness appears in the covert-actions note, its own stat, question two, positions one and six, and the crux subtitle. Astra's lost monitorability appears in its stat, question three, and positions one and six. Positions citing the evidence is expected, but the page leans hard on the same handful of results.
- chain-of-thought-faithfulness detail. In the page's voice it calls faithfulness "the load-bearing assumption under every attempt to supervise a model by reading what it writes." Question three's durability side argues that a monitor needs only the incriminating step, and that hard tasks force it into the scratchpad. The stat does not mention that reply, although the cost-to-strip stat gives both readings of its number. The 25 to 39 percent figure therefore reads as weighing against durability.
- Stat 2 against question three. The Astra detail calls reading the scratchpad "the cheapest way anyone has found" to catch misbehavior. Question three's why calls it "the most effective misbehavior detector anyone has." These are different claims, one of them strong, and both are in the page's voice.
- cost-to-strip-safety-training-from label. The label says "open weights", but one of the note's three examples is GPT-3.5 Turbo stripped through a closed fine-tuning API. A reader could take GPT-3.5 for an open-weight model. The source field names two works (Qi et al.; Volkov) but links only one.
- Scope. The scope line excludes "regulation and licensing". Yet the sixth camp calls for halting frontier scaling, and its action (ControlAI) lobbies for binding limits on training runs. The camp's claim is about the state of alignment, so including it is defensible, but a reader may notice the tension.
- Sourcing concentration. Eight of the sixteen stats come from Anthropic, including the agentic-tampering test in which Anthropic's own models score best. The page states that caveat, and most of the Anthropic stats report failures. This is not a neutrality defect, but the evidence base is narrower than the camp list.
- Proponent overlap. Google DeepMind is listed under both the first and second positions, and Anthropic appears in both (as Anthropic, Anthropic Interpretability and Dario Amodei). The camps differ in what they want, but the overlap may make a reader wonder whether they are one camp.
- Glance order. Four of six camps show before Go deeper, and so do the actions for camps one to three. The reliability, guarantees and halt camps' actions sit behind Go deeper, and the share cards list only the first four camps. That follows file order by design. The consequence is that every shared card omits the guarantees and halt camps.
- Crux values box. It ends "Underneath sits who decides." That is too terse to land. A reader cannot tell who the candidates are.
- Template/CSS: ranked charts do not render the unit. The control chart shows bare 92 and 79 where the unit is "% safe", and the covert-actions chart shows 13.0 and 0.4 without "%". At 390 the ranked-chart bar track is about 45px wide, so 13.0 against 8.7, or 85 against 95, is hard to read from the bars.
- Template: the expanded-section renders still show "Go deeper" and "See how it resolves" at the section foot. The live page toggles correctly to "Show less", so this is a render-capture artifact, not a page defect.
- Desktop 1440 expanded: the last Basics row holds two tiles and leaves the third column empty, because 16 stats do not divide by three. It is cosmetic.
