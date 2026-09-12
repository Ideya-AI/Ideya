# Stage 1 — meta-research findings

Raw material for designing stage 1 of the authoring pipeline. Gathered
2026-09-12 by five parallel research agents plus their sub-researchers,
against the question: how do people do this well, and what is known about how
machines do it badly.

**This file reports findings. It does not draw conclusions, and nothing here is
a decision.** Where sources disagree, both are recorded (§11). Where an agent
flagged a claim as unverified, the flag is kept. Design decisions live in
`PIPELINE.md`.

---

## 1. Provenance and confidence

| Agent | Scope | Confidence notes |
|---|---|---|
| position-mapping | Enumerating camps, establishing prevalence | Primary methodology docs, fetched |
| research-methods | Human research traditions | Its six sub-researchers' reports never reached it; about half is from model knowledge, tagged by the agent as needing spot-check |
| artifact-analysis | Reverse-engineering published explainers; audited our own files | Read raw HTML/PDF; quotes verbatim; claims about our topic files independently verified |
| automated-research | STORM, deep-research systems, measured LLM failure modes | Papers with numbers |
| claude-practices | Anthropic docs and the installed SDK | Probes against this install; corrected four of its own doc-derived claims |
| (sub) forecasting | Metaculus, Tetlock, FRI, rationalist norms | Primary, some via text-render proxy |
| (sub) evidence synthesis | Cochrane, GRADE, IPCC, PRISMA, saturation | Primary |
| (sub) deliberative briefing | Stanford DDL, citizens' assemblies, Oregon CIR, Kettering, OECD | Primary |
| (sub) Wikipedia + SEP | NPOV machinery, SEP editorial process | Primary |
| (sub) BBC ×2 | Due impartiality, Jones review, Reuters, AP | Primary; the two duplicated, one corrected the other's section numbering |
| (sub) argument mapping | IBIS, Toulmin, pragma-dialectics, Walton, ACH, adversarial collaboration | Primary |
| (sub) explainer formats | Economist, FT, Vox, ProPublica, UNESCO | Summary only reached us; full report went to a peer |

Known access failures: Kialo is login-walled, Britannica/ProCon blocked (read via
Wayback), Economist and FT paywalled, AP's deep pages Cloudflare-blocked. AP's
false-balance rule lives in the paywalled Stylebook and is **quoted only from
hostile secondary sources — flagged unverified.**

---

## 2. Enumerating positions

### The inversion

Multiple traditions converge on not asking what the positions are.

- **Q methodology** builds a **concourse** first: "the infinite set of possible
  expressions that refer to a topic of concern, from all different points of
  view," sampled into 40–60 opinion statements drawn from "existing literature
  and research, interviews with subject-matter experts, open-ended surveys."
  Safeguard: "factor interpretation should be grounded in statement loadings,
  not researcher projection."
- Position-mapping's formulation: never ask "what are the positions on X?" —
  that is the generative mode. Ask "who has publicly said what about X, and
  where?" Enumeration becomes retrieval over claimants.
- **Stakeholder analysis** calls this bottom-up *reconstructive* categorization
  (stakeholders define themselves) versus top-down *analytical* categorization
  (the analyst sorts them). [Reed et al. 2009]
- **Kettering/NIF** harvests ~150 raw concerns in 2–3 hours, then clusters. "Most
  contentious issues are framed in expert terms by political and technical
  elites. People find such framings alien."

### The highest-yield single operation

From each document, harvest **everyone it argues against by name.** Critics have
an incentive to find every opponent, so critiques routinely name camps a
from-scratch enumeration misses. (Snowball sampling, per Reed: "people who know
other people.")

### Structuring the space rather than listing

- **SEP** names the *dimensions of variation before naming any position*:
  "Distributive principles vary in numerous dimensions. They vary in what is
  considered relevant…; in the nature of the recipients…; and on what basis the
  distribution should be made." Position-mapping's gloss: you cannot detect a
  missing camp by staring at a list; you can detect an **empty cell**.
- SEP's fidelity disclaimer ships with it: the categories "necessarily involve
  over-simplification, particularly with respect to the criticisms of each of
  the groups of principles."
- **Morphological analysis / multiple hypotheses generator** (intelligence
  tradecraft): decompose the framing into dimensions, take the cross-product,
  "discard any permutation that simply makes no sense" (expect ~90% eliminated),
  score survivors 1–5, restate as hypotheses. Stated purpose: greater confidence
  "that a critical alternative or an outlier has not been overlooked."
- **Quadrant crunching** — "a Key Assumptions Check on steroids" — flips each
  assumption of the conventional framing and crosses the contraries.

### Reserved slots

- SEP's *Legal Punishment* taxonomy always carries a **Mixed/hybrid** bucket and
  an **Abolition / reject-the-question** bucket.
- Position-mapping's **frame-rejection test**: is there a camp whose position is
  "the question is wrong"? Systematically missed because the page title
  presupposes a frame.
- **Kunz & Rittel (IBIS, 1970)** require a per-issue flag: "To each issue a
  **logically closed set** of possible positions or an **open list** of possible
  positions may be assigned."

### Cardinality

Everyone converges on 3–7.

| Source | Count | Basis |
|---|---|---|
| Pew typology | 9 | clustering on 27 value items across the whole spectrum |
| Hidden Tribes | 7 | 58 items |
| Q studies | 3–6 factors | Kaiser-Guttman, scree, Humphrey's rule, ≥2 loading sorts, "the magic number seven" |
| Kettering | start 5–7, converge to 3–4 | "In what ways are some of these subsets of others?" |
| ACH | ≤7 | "More than seven hypotheses may be unmanageable" |
| SEP Immigration | 9 restrictionist / 5 open-borders | deliberately asymmetric |

Pew's retention test, verbatim: solutions were evaluated for producing "cohesive
groups that were sufficiently distinct from one another and large enough in size
to be analytically practical and substantively meaningful." Their candour:
"different solutions are possible using the same data depending on the algorithm
used, the ways in which the variables are coded, and even the order in which
respondents are sorted."

### Is this camp real?

- **Wikipedia's three-way test** (paraphrasing Wales, 2003): majority ⇒ "easy to
  substantiate it with references to commonly accepted reference texts";
  significant minority ⇒ "easy to name **prominent** adherents"; extremely small
  minority ⇒ "does not belong… regardless of whether it is true."
- Position-mapping's **adherence bar**: ≥2 independent, named, citable adherents,
  at least one institutional, asserting the camp's claim in their own published
  words, dated. **The gate is on adherence, not coherence** — a language model
  can always construct a defensible position.
- **Four named LLM confabulation modes**: *symmetry completion* (manufacturing
  the fourth cell of an implied 2×2); *interpolation* (the reasonable-sounding
  moderate between two real camps that nobody occupies — flagged as the most
  dangerous because most plausible); *literature import* (a labelled option in an
  academic literature with no adherents in the live debate); *coalition
  splitting* (promoting a secondary-aspect difference to a camp).
- **Walton's scheme-matching rejection rule**: "If a required premise of the
  scheme is not found in the argument in the discourse, we need to look and see
  if there is evidence that it is an implicit premise. If there is no such
  evidence we need to conclude that the given argument is not an instance of
  this particular scheme."
- **SEP's anti-invention rule**, the most-cited sentence across agents:
  > "Authors should not use their SEP entry to raise, or respond to, objections
  > if those objections and responses aren't already in the published literature."
- **Heuer's unproven ≠ disproved rule**: "Early rejection of unproven, but not
  disproved, hypotheses biases the subsequent analysis… Unproven hypotheses
  should be kept alive until they can be disproved."
- **Heuer's expectation test**: before writing "there is no evidence that…", ask
  "If this hypothesis is true, can I realistically expect to see evidence of it?"

Position-mapping recommends **decoy calibration**: generate plausible-but-
fabricated camps, mix them in, require the verification pass to reject all of
them. "If it 'verifies' a decoy, the gate is broken and the run is void."

### Granularity — when are two views one camp?

- **ACF tier test**: differ in *policy core* (causal diagnosis, shape of the
  acceptable response) ⇒ distinct camps. Differ only in *secondary aspects*
  (instrument, magnitude, sequencing, funding) ⇒ one camp with recorded internal
  variation.
- **Distinguishing-statement test** (from Q's factor interpretation): two camps
  are distinct only if you can write at least one proposition A affirms and B
  denies — "not merely emphasizes differently."
- **Coalition tiebreak**: would they coalition together against a common
  opponent? ACF requires "a nontrivial degree of coordinated activity over time."
- **Kettering's sacrifice test**: two options requiring the same sacrifice are
  the same option.
- **Argdown's equivalence classes**: two reconstructions resolving to the same
  title are one camp.
- **ACH merge gate**: "If there is little or no evidence that helps distinguish
  between two hypotheses, should they be combined into one?"
- **Asymmetric splitting hazard** (position-mapping): you will split the camps
  you know most about and lump the ones you know least about, producing a page
  fine-grained on the domestic mainstream and coarse elsewhere. Guard: check that
  split-depth does not correlate with source volume.

### Completeness tests

No source offers a completeness proof. What exists:

1. **Source saturation**, made numeric (Guest/Namey/Chen, PLOS ONE 2020): base
   size (default **4**), run length (**2 or 3** consecutive units), new-
   information threshold (**≤5%** or **0%**), explicitly analogized to a p-value.
   Formula: (new themes in run) ÷ (unique themes in base) ≤ threshold. Bootstrapped
   result: "saturation was indicated at **6+2 interviews**," ≈78–82% coverage.
   Published critique: saturation measures when new themes stopped appearing *in
   your sample*, conditional on sampling diversity.
2. **Orphan-argument test**: for each camp, take its strongest published critique
   and check who the critic names as opponents.
3. **Axis test**: if all camps order on one axis, the orthogonal ones are
   probably missing. Warrant from cleavage theory — Lipset & Rokkan's structure
   repeatedly needed added dimensions.
4. **Affected-interests test**: enumerate the populations materially affected,
   check each has a position represented. Deliberative practice lets participants
   "request additional experts or stakeholders if they feel information is
   missing."
5. **Frame-rejection test** (above).
6. **Kettering's explicit missing-camp pass**: "once it seems that all the
   concerns have been aired, push ahead and ask specifically about those not in
   the room… Imagine specific kinds of people (the elderly, new immigrants, the
   poor), and imagine what they actually might say."
7. **Hunter's whole-document opener**: "Is it biased, or fair? Does it feel as if
   something is missing? Who, or what, might be able to present a different
   picture?"

### The audit trail

- **PRISMA 2020 item 16b**: "Cite studies that might appear to meet the inclusion
  criteria, but which were excluded" — near-misses published, with reasons.
- **Cochrane rapid reviews**: a second reviewer screens **all excluded** records.
  Rationale as the agent put it: a wrongly included item gets caught downstream;
  a wrongly excluded one is invisible forever.
- **Saunders et al.** on reporting saturation: "document the initial plan, the
  evidence gathered during analysis, the stopping criterion used, and the
  rationale for concluding that saturation was achieved."
- **BBC 2.4.4**: "There is no view on any subject which must be excluded as a
  matter of principle; content producers should make reasoned decisions."

### Naming camps

Three documented failure modes:

| Mode | Example |
|---|---|
| The camp's own marketing | "pro-life"/"pro-choice" — each frames itself in inherently positive terms, forcing the other's name into a negation. Also "right to work," "election integrity" |
| Opponents' caricature | "death tax," "abortionist" (AP: "connotes a person who performs clandestine abortions"), "climate denier," "AI doomer," "NIMBY" |
| False-neutral euphemism that loses the position | AP's 2015 "climate doubters." AP's own reporter conceded the accurate phrase was "those who reject mainstream climate science" and that "doubters" was chosen because the precise phrase doesn't fit a headline |

Rules found:

- **SEP**: entries should be "idea-driven" rather than "person-driven," and
  "section and subsection titles should avoid invoking the names of philosophers."
- **AP's label rule**: "'illegal' should describe only an action," not a person.
  They rejected "undocumented" too "because it is not precise." Generalized:
  "while labels may be more facile, they are not accurate." And: be as specific
  as possible; "in many cases we find the most effective word is simply 'people'."
- **Symmetry of register**: all camps named in the same grammatical form. Mixed
  registers editorialize through form alone.
- **Coined names must be declared as coined** — Pew and More in Common both do
  this openly.
- **Two-sided acceptance test**: a name passes iff the camp's strongest advocate
  *and* its strongest critic would both call it **accurate** — not "would both
  like it."
- **Wikipedia's sourceable-label rule**: characterizations are allowed "provided
  the source is accurately labeled in neutral terms and the label is sourceable."

### What not to build on

Argument mining and stance detection: SOTA models show "limited cross-domain
generalizability" and "primarily learn dataset-specific characteristics… rather
than… fundamental principles about argumentation structure." Stance corpora are
English-centric and Global-North-skewed.

### Boundary cases (position-mapping)

- **Fringe with real adherents** → include and label. Wikipedia: "clearly
  described as such," with "an explanation of how experts in the relevant field
  have reacted."
- **Once-dominant, now abandoned** → test "does anyone defend it in print, now?"
  Note that "abandoned" is usually a claim made by the winners.
- **Held mainly outside the page's country** → include; score prevalence
  in-scope; state the elsewhere. Wikipedia's Anglo-American systemic bias is
  formally recognized and attributed to "the availability of sources and
  disproportionate global media coverage."
- **Large-but-inarticulate positions** — Converse's nonattitudes: the most
  populous stance on a low-salience question is often "no stance," which has no
  op-eds and fails any adherent gate.
- **Adherents but no institutions** — fails an institution-requiring gate for
  reasons of resource distribution, not reality.

---

## 3. Prevalence and weight

### The structural finding

Position-mapping: **enumeration and prevalence are two problems with two disjoint
evidence bases, and essentially no published method does both.**

| Instrument | Enumerates | Measures prevalence |
|---|---|---|
| Q methodology | purpose-built | "can only be used to identify points of view in a population, but not by how many people these points of view are shared" |
| Survey typologies | only what the questionnaire contained | precisely |
| Wikipedia due weight | no | yes, but of *sources* |

### Whose prevalence?

Wikipedia is explicit: "in determining proper weight, we consider a viewpoint's
prevalence in **reliable sources**, not its prevalence among Wikipedia editors or
the general public."

Public and expert prevalence diverge enormously and the sign is unstable
(Pew/AAAS 2015): GM food safety **88% of scientists vs 37% of public** (51
points); nuclear power **reverses** (65% vs 45%); 8 of 13 science issues exceeded
a 20-point gap.

### Source types and their biases

| Source | Measures | Failure mode |
|---|---|---|
| Mass survey | the public, as worded | wording manufactures part of the result; nonattitudes on low-salience issues |
| Expert survey | a defined expert population | the target population *is* the bias; option set is the surveyor's enumeration |
| Elite/party positions | organized political supply | worst at small and extreme parties |
| Legislative record | institutional outcomes | filtered by feasibility and agenda control |
| Funding/capacity | institutional power | measures resources, not belief. "Do not label this prevalence" |
| Media share | source prominence | Boykoff & Boykoff: decoupled by an order of magnitude from expert prevalence |
| Academic citation | literature activity | a settled consensus can be under-cited *because* settled |

**PhilPapers** is cited as the best available model of a defensible instrument:
~2,000 philosophers, 100 multiple-choice questions, declared population, published
per-position percentages with decade-over-decade change.

**IGM / Kent Clark Center** is the cheapest copyable model: fixed panel,
agree/disagree/uncertain on a 5-point scale plus No Opinion and Did Not Answer,
each panellist self-rating **confidence 1–10**, published both unweighted (so
non-response is visible) and confidence-weighted.

### Conventions for expressing weight

- **IPCC**: evidence (*limited/medium/robust*) and agreement (*low/medium/high*)
  as **two separate axes**, read off a 3×3 grid. Routing rule: high agreement AND
  robust evidence ⇒ state a confidence level; one but not both ⇒ confidence if
  possible, else report both summary terms; **low agreement AND limited evidence
  ⇒ report both coordinates, never a composite.** The guidance forbids attaching
  a number when the basis for one doesn't exist.
- **GRADE**: four ordinal levels with the reasons for downgrading recorded, and
  certainty of evidence kept separate from strength of recommendation.
- **Wikipedia**: weight expressed structurally, never numerically. And the
  warning that "undue weight can be given in several ways, including… **depth of
  detail, quantity of text, prominence of placement, juxtaposition of statements,
  and use of imagery**."
- **BBC 2.2.7**: "There is no requirement to give all views equal weight – false
  equivalence does not achieve impartiality and should be avoided. Minority views
  or those less supported by evidence, do not need to be given similar prominence
  or weight to those with more support, to the prevailing consensus, or to those
  better evidenced." And 2.1: "Impartiality will always rest on good judgement,
  rather than any mathematical formula."
- **Citizens' Assembly on Brexit** took the *opposite* approach and said so —
  see §11.
- **AP's weight-signalling sentence template**: "Though some public officials and
  laymen and only a few climate scientists disagree, the world's scientific
  organizations say that the world's climate is changing… This is supported by
  more than 90 percent of the peer-reviewed scientific literature."
- **Oregon CIR**: a tally ("may include a tally of how many panelists agreed"),
  and a mandated null — **"No panelist took this position."**
- **Metaculus**: central estimate, interquartile range and N together, never a
  bare point estimate.
- **ICD 203 probability lexicon**: *almost no chance 01–05% / very unlikely 05–20%
  / unlikely 20–45% / roughly even chance 45–55% / likely 55–80% / very likely
  80–95% / almost certain 95–99%*, with hard rules against mixing rows and against
  combining a confidence level with a likelihood in one sentence.

### The false-balance evidence

- **Boykoff & Boykoff 2004**: 52.65% of US prestige-press climate articles gave
  balanced treatment to a view held by a small minority of scientists.
- **Dixon & Clarke 2013**: readers of falsely balanced autism-vaccine coverage
  "were less certain that vaccines did not cause autism and more likely to
  believe experts were divided," with reduced vaccination intent — and the effect
  was **mediated by the belief that medical experts are divided.**
- **Kohl et al. 2016**: the established fix is weight-of-evidence reporting —
  presenting the minority view *with* an explicit statement of how much support
  each has — not exclusion.
- **No published numeric threshold** below which a view should be omitted. The
  literature declines to set one.
- Counter-literature: consensus-first framing "may silence legitimate dissent"
  and "convey a distorted image of science as a body that speaks unanimously";
  an evidence-resistant minority shifts opinion whether or not you cover it.

### What the silicon-sampling literature says about model-estimated prevalence

LLM-generated opinion distributions are "far too homogeneous" relative to human
data; GPT-3.5 silicon samples **inflated partisan and racial affective
polarization by ~7×**; models **under-represent minority views** and default to
higher-education, higher-SES respondents; a documented **"harmlessness bias"**
pushes toward socially desirable answers, worst on socially sensitive topics.

Expected error direction: minority camps under-weighted, gaps between polarized
camps exaggerated.

**Framing effects**: Grace et al.'s AI survey put the 50% HLMI date 34 years out
under fixed-year framing vs 17 under fixed-probability. Authors' caution:
"aggregate answers to any particular question are not an accurate guide."

### Structured elicitation, and why an LLM estimate is not it

Cooke's classical model weights experts by calibration measured on **seed
questions with known answers**; IDEA adds structured discussion between two
rounds of private estimates; SHELF ends in a facilitated consensus distribution;
Delphi supplies anonymity, iteration, controlled feedback, statistical group
response. Position-mapping's note: every one derives legitimacy from multiple
independent experts plus empirical calibration. "A single model producing a
number has neither."

**Bayesian Truth Serum** scores answers "more common than collectively predicted"
— the surprisingly-popular criterion — and its stated property is that it
"removes all bias in favor of consensus."

**ProPublica's data rule**: "If you are ranking data, take the margin of error
into account because it could change rankings."

**EKLIPSE's vote-counting warning**: weight by considered assessment, never by
how many sources you happened to find, because source counts track publication
volume and your own search shortcuts.

### The argument against having the field at all

Position-mapping, stated at full strength on request:

1. **Category error** — no single population over which "how widely held" is
   well-defined; a scalar collapses incommensurable measurements into a number
   true of no population.
2. **Fabrication by interface** — a required numeric field will be filled; there
   is no "unavailable" that survives a sort function; on the page a sourced
   number and an invented one are visually identical. And the fabrication is
   systematically biased toward media share.
3. **Editorializing in the costume of data** — ordering by an unsourced number
   takes a side while claiming the ordering is not a judgment.
4. **Precision theatre** — 0.34 vs 0.31 implies a resolution no source supports.

Its recommended replacement: keep the mechanism, change the type to a band with a
declared population, a required `basis` (source, url, date, method, question
wording), evidence and agreement levels, and an optional `divergence` block.
Rules: no band without a basis; ordering derived only from banded camps;
**bands never normalize to 100%** (Converse); four bands, not ten.

**Its stated kill condition**: "if, after running the procedure on a real sample
of topics, the modal value is `unranked`… A field whose modal value is fiction
should not exist."

---

## 4. Steelmanning and voice

### The critique of "steelman," from the community that coined it

- **Ozy, *Against Steelmanning***: where worldviews differ deeply, "Alice doesn't
  actually understand Bob's argument at all," and the practice "is actively
  harmful to epistemic charity and to careful thought. **Instead of understanding
  that people believe things differently from you, you're transforming everyone
  into stupider versions of yourself.**" Alternative: "Seek out intelligent and
  well-informed advocates of viewpoints you disagree with. **You don't have to
  make up what your opponents believe!**"
- ***Dangers of steelmanning*** names four: worldview entrenchment; **false
  consensus** (the steelman makes your frame look more widely shared than it is);
  overvaluing arguments nobody advances; poor models of what people believe.
  Guards: distinguish clarifying from improving; **do not attribute a constructed
  argument back to a real group.**
- ***Steelmanning as an especially insidious form of strawmanning***: the
  steelman is "the best argument the interlocutor can generate on the spot," so
  it substitutes the author's reachable argument for the holder's actual
  load-bearing one, "while wearing the costume of good faith."
- **Bensinger**: the goal is to "understand the substance of someone's view well
  enough to be able to correctly describe their beliefs and reasoning"; "charity"
  is rejected because "it equivocates between 'be friendly' norms and 'have
  accurate beliefs about others' norms"; the recommended pair is **pass their ITT
  + identify cruxes**.
- **Gelman**: bending over backward for one view implicitly dismisses the others.

Wikipedia's own essay names the identity: "**Writing for the opponent**, also
known as **steelmanning**… and also giving it proper weight in the article
relative to its significance." Its success test is external: "The point is to
satisfy the proponents of a perspective that you understand their arguments."
And: "it is possible to explain why certain individuals did terrible things,
without either endorsing them or adding one's own proofs that they were evil or
wrong… the ability to communicate another viewpoint **without any elaboration**."
Plus: "**To leave out one side amounts to promoting the other side's point of
view.**"

### Charity, defined precisely

Shields' four criteria: an interpretation is maximally charitable iff it is
(i) accurate in translation "**to be recognizable by A as A's argument in B's own
words**," (ii) fair to A's intentions in context, (iii) plausible to both,
(iv) preserves and improves the logical features. Shields flags (iv)'s tension:
improving risks "an argument that is not hers, because it's better than Alice's
original."

Pragma-dialectical **Rule 5** forbids the same thing: "A party may not falsely
present something as a premise that has been left unexpressed by the other party."

### Reconstruction rules

- **IAT annotation manual**: "**Do as much reconstruction as necessary** so that
  you end up with a full sentence which will be understandable without any
  context… At the same time, **do as little reconstruction of implicit material
  as possible**." Tested by the **Standalone Test**: "Will a third party be able
  to understand this sentence standalone from any context?"
- The same manual's anti-straw-man clause: "we allow arguers to express not just
  good arguments, but poor, weak, incoherent and fallacious arguments… **We are
  never trying to analyse the ways in which propositions might be connected**…
  **We are aiming to capture the arguments that were made by the original
  interlocutors.**"
- **Hahn/Madsen/Reed**: "we felt it was important at all times to stick with the
  original text, rather than paraphrase… **The only tool we decided to allow with
  respect to length and detail was ellipsis, represented clearly with '…'**"
- **Theoretical adversarial collaboration template**: "The critic formulates in
  their own terms the strongest possible version of T… The advocate supervises
  both formulation and defense to ensure accuracy and completeness," and answers
  objections "**in terms of conceptual resources in existing publications of T**."
- **UNESCO story-based inquiry**, the fact-checker's target: "challenges in
  particular the **author's interpretation of the target's motives, goals or
  thoughts. In general, this material should be cut.**"
- **Wikipedia depth cap**: "if the only references to a particular subject are in
  news sources, then a level of detail which is greater than that which appears
  in these news sources is inappropriate."

### Validation gates

- **Ideological Turing test** (Caplan): "the ability to pass ideological Turing
  tests — **to state opposing views as clearly and persuasively as their
  proponents** — is a genuine symptom of objectivity." Failure diagnostic is
  caricature by tone: sneers, over-claiming, getting the *emotional* drivers
  wrong.
- **FRI's comprehension gate**: "each side must demonstrate it more fully grasps
  each major argument of the other side before offering rebuttals."
- **Penn ACP**: articulate each other's positions "so that each side feels fairly
  characterized, **not caricatured**."
- **Oregon CIR right-of-reply**: the camp's designated advocate reviews *its own*
  statement and the shared key findings, but not other camps' statements; the
  panel "may adjust" and retains final authority.
- **Persuasion delta** (from XPT's rationale-prize mechanic): have a naive reader
  state a view before and after reading a position. A position that moves nobody
  is decoration; one that moves everyone the same direction is advocacy.

### Sourcing the advocates

- **Irish Citizens' Assembly** selection criteria: demonstrated expertise; "good
  communicators"; "**people who are not seen primarily as advocates on one side
  or another**"; and "in the case of issues where expert views are contested… both
  sides of the argument will be represented." Two tracks: non-advocate experts
  supply facts, advocacy groups supply positions.
- **Oregon CIR fallback duty**: chief petitioners select two representatives; if
  they fail to, "the commission may designate two persons who support the
  measure"; for the other side "the commission **shall** designate two persons
  who oppose."
- **newDemocracy's withdrawal rule**: when industry speakers withdrew at the
  eleventh hour, "a library of comprehensive information had to be assembled and
  the pro-CDL experts were told to stay away so that balanced information could be
  provided via that library." Symmetry preserved by demoting both sides.
- **Celebrity capture guard**: ask a celebrity expert to "nominate another speaker
  who shares their position." Position continuity, not person continuity.
- **Enumerate categories of voice before naming individuals.**

### Voice and register

- **BBC YESPOV**: "assert facts, including facts about opinions — but do not
  assert the opinions themselves"; "**The only bias that should be evident is the
  bias attributed to the source.**"
- **BBC IMPARTIAL**: "**Try not to quote directly from participants engaged in a
  heated dispute**; instead, summarize and present the arguments in an impartial,
  formal tone." (Noted by artifact-analysis as a rule our in-voice design
  deliberately breaks.)
- **Red Team convention**: "The analysis is often in a 'first person' format…
  Red Team analysis **avoids the use of caveats or qualifications**." Paired with
  Devil's Advocacy's labelling guard: products must be "identified as an
  explicitly 'Devil's Advocate' project; otherwise, the reader can become confused
  as to the current official view."
- **NIF's voice marker**: each option opens "**THIS OPTION SAYS THAT…**"
- **Kettering's tone rule**: "each one should be persuasive and an argument
  against the others. It should make its own strongest case," and "The narrative
  voice needs to make an argument, but at the same time needs to do so in a way
  that it admits doubt. **It must be persuasive without being strident.**"
- **SEP**: no first person, even to indicate what the author intends to discuss;
  self-citation capped and policed; biography must be critical, not
  hagiographical.
- **Reuters' lexical blacklist**: "Words like 'claimed' or 'according to' can
  suggest we doubt what is being said. Words like 'fears' or 'hopes' might suggest
  we are taking sides. Verbs like rebut or refute… or like fail… are best
  avoided." Plus hype words: "A 'flood' of immigrants… may in reality be a
  relatively small number." Plus: "To write… that someone hinted, implied,
  indicated, suggested, or signaled is to **editorialize**."
- **Vague-attribution blacklist** (Reuters): no "sources," "observers,"
  "informed sources," "reliable sources" — "Would we quote an uninformed or
  unreliable source?" — and "Do not quote 'analysts'. Specify their area of
  expertise."
- **WP:WEASEL / SUBSTANTIATE**: replace an unsourceable opinion with the factual
  claim underneath it — "John Doe had the highest batting average in the major
  leagues from 2003 through 2006."
- **The Economist's style guide**: "Those who disagree with you are not
  necessarily stupid or insane… **When you express opinions, do not simply make
  assertions**… Go easy on the oughts and shoulds."

### The blandness failure, diagnosed

- **Jay Rosen, "View from Nowhere"**: "a bid for trust that advertises the
  viewlessness of the news producer," which "frequently places the journalist
  between polarized extremes, and calls that neither-nor position 'impartial'."
  Worst consequence: "criticism from both sides is a sign that you're doing
  something right, when you could be doing everything wrong."
- **Pielke's honest broker** test: the honest broker "makes an effort to expand
  (or at least clarify) the scope of choice for decision-making," where the issue
  advocate narrows it.
- **Jones (BBC science review)**: "In most areas of endeavour, the famous 'wagon
  wheel' involves the presentation of divergent opinions; but science deals, most
  of the time, with **opposed evidence**. To confuse the two can destroy the whole
  basis of impartiality." And: "**It must accept that it is impossible to produce
  a balance between fact and opinion.**" And on format: "to present it in 'debate'
  format was to set up a false balance; to return to the seesaw."
- **BBC 2.4.26, the reverse failure**: where a consensus exists and seeking
  opposition isn't warranted, "reporting should not use language and tone which
  appear to accept consensus or received wisdom as fact or self-evident."
- **Seesaw to Wagon Wheel #4**: "Impartiality involves breadth of view, and can
  be breached by omission. It is not necessarily to be found on the centre
  ground… **Reporting from the centre ground is often the wrong place to be.**…
  all of them **subject to equal scrutiny**."
- **Anthropic's own prompt guidance**: "the prompt's register becomes the
  output's register: **an anxious prompt produces a cautious, hedging model**,"
  and "a prohibition against a failure the model wasn't going to make can
  **anchor it toward** that failure."
- **Measured hedging rates** across 7 models × 4,738 prompts: 2.4% (Claude
  Sonnet 4) to 28.6% (Gemini 2.5 Pro), near-zero on consensus topics and highest
  on genuinely contested ones.
- **Models take a stance when used as judges or debaters** even when they give
  nuanced answers as open-ended generators. Implication recorded by the agent:
  never route "which camp is right" or "is this balanced" to a judge-shaped call.
- **Counter-pressure**: one (blog-only, not peer-reviewed) test found LLM judges
  scored balanced answers 0.74 points lower than confident one-sided ones.
- **Verbalized Sampling**: asking a model to verbalize a distribution over
  candidate responses with probabilities restored ~66.8% of lost diversity.
- **Anthropic's Constitution**: "epistemic cowardice" — "giving deliberately
  vague or noncommittal answers to avoid controversy or to placate people" — is
  named as an honesty violation; Claude should be "**diplomatically honest rather
  than dishonestly diplomatic**."

### The homogenization risk

- **claude-practices**: Anthropic's guidance says both "provide the best case for
  most viewpoints" and "adopt neutral terminology over politically-loaded
  terminology." Those conflict here, because a camp's own vocabulary *is* loaded.
  Unresolved, the model resolves toward neutral and flattens every camp into one
  register — named **strawman-by-homogenization**, "a worse failure than advocacy
  because it's invisible."
- **The Economist's "A note on editing"** names the parallel failure: "The risk is
  that the newspaper will turn into a collection of 70 or 80 articles which **read
  as though they have been written by no more than half a dozen hands.**"

---

## 5. Questions and the empirical/value split

### Taxonomies found

- **Kunz & Rittel (IBIS §7)**, four-way with canonical interrogative forms:
  > "• **factual issues**: 'Is X the case?' • **deontic issues**: 'Shall X become
  > the case?' • **explanatory issues**: 'Is X the reason for Y?' •
  > **instrumental issues**: 'Is X the appropriate means to accomplish Y in this
  > situation?'"
- **FT / IPSO 1.4**: "must distinguish clearly between **comment, conjecture and
  fact**."
- **artifact-analysis** proposes empirical / value / **feasibility**, evidenced
  from our own file (§12).
- **Truong, Puranam & Koçak** use a MECE five-type premise taxonomy: factual
  (current), factual (forecast), causal, moral/evaluative, definitional.
- **BBC 2.4.6**'s sixth factor: "the distinction between matters grounded in fact
  and those which are a matter of opinion."

### Mechanical extraction

- **Toulmin warrants**: the challenge script is "What do you have to go on?"
  (grounds) → "How do you get there?" (warrant) → justification (backing). The
  warrant is "a **general rule which licenses or permits a step**… It is implicit
  in the arguments people put forward." The operational test where you cannot ask
  the arguer: "**'How might you get there?' And then: 'Is one of the ways you
  might get there a reliable route?'**"
- Hitchcock's feasibility measurement: of 50 randomly sampled arguments, "For 49
  of the arguments, I had no difficulty in singling out an applicable
  'inference-licensing covering generalization'."
- **Procedural constraint**: "In general, then, the warrant is **not part of the
  analysis** of an argument… **Identification of the warrant is part of the
  evaluation**." The agent's note: warranting is an editorial act, so excavated
  warrants belong wherever the page speaks in its own voice, not inside a camp's.
- **Conklin's Rule 3c**: "Often the justification (e.g. 'because it is cheaper')
  masks a hidden understanding of the problem (e.g. 'costs must be minimized')."
- **Rabbit Rule** (argument mapping): "Every significant word, phrase or concept
  appearing in the contention of a simple argument must also appear in one of the
  premises." **Holding Hands**: "Every significant word… appearing in a premise
  but not in the contention must also appear in some other premise." Stated
  limit: "it doesn't mechanically determine the outcome."
- **The Taboo pass**: ban the contested handle and "describe outward observables
  and interior mechanisms." If the disagreement survives, it is empirical; if it
  evaporates, it was definitional.

### Question-writing rules

**Conklin's five IBIS rules**, each with a worked repair:

| Rule | Content |
|---|---|
| Simplicity | "should be simple and concise. It should not contain possible answers. It should avoid the words 'and', 'or', or 'not'." |
| Open Question | "avoid 'Yes/No' Questions, and Questions that follow the pattern 'Should we do X or Y?'… **this benefit is eliminated if the Question is not asked in an open-ended way.**" Diagnostic: yes/no questions "begin with either 'should' or some form of 'be' or 'does'." |
| Embedded Solution | "If 'S' is an element of the Solution… avoid Questions such as 'Should we do S?'… Instead, abstract out the Problem to be solved and ask 'How to solve P?'" |
| "Other" | "should not contain the word 'other'… A Question asking 'What other solution is there?' is usually redundant" — a diagnostic that an earlier question violated Rule 3 |
| No Benefits | "should not ask for the benefits or disadvantages… IBIS provides a specific place for pros and cons — in Arguments." |

Conklin names the pathology these exist to prevent — the **Answer Reflex**: "the
original question is quickly overwhelmed by a flurry of countermanding ideas… A
well-functioning Answer Reflex assures that no one asks, 'What is the question
here?'"

**Metaculus's Clairvoyance Test**: a question must be "unambiguously resolvable,
with a community reading the question terms able to agree, before and after the
event has occurred, whether the outcome satisfies the question's terms." Their
eight requirements include a named authoritative public source plus a fallback,
pre-decided edge cases, and a title that does not "make a stronger/weaker claim
than the resolution criteria." Failure taxonomy: **ambiguous** (reality unclear)
vs **annulled** ("a key assumption of the question was overturned"), plus
**misaligned** (letter vs spirit) from Rethink Priorities.

**Kunz & Rittel's provenance test**: "**The origins of issues are controversial
statements.**" A sub-question earns its place only if the controversial statement
it came from can be named.

**Walton's critical questions**, e.g. for *argument from expert opinion*:
expertise, field, opinion, trustworthiness, consistency, backup evidence. For
*practical reasoning*, CQ2 is a generative instruction: "**What alternative
actions to my bringing about A that would also bring about G should be
considered?**" For *analogy*, CQ3: "Is there some other case C3 that is also
similar to C1, but in which some conclusion other than A should be drawn?"

**Petticrew & Roberts' question typology** — effectiveness, process, **salience**,
safety, **acceptability**, cost-effectiveness, **appropriateness**, satisfaction —
with the note that the evidence hierarchy "depends on the question asked" and "in
certain circumstances the hierarchy may even be **inverted**."

---

## 6. The crux

### Named methods

- **Double crux**: B is a crux for A if "if it turned out that B was **not** true,
  that would be sufficient to make you think A was false, too." Algorithm:
  operationalize first ("The very first step… should **always** be to
  operationalize and clarify terms"), each party lists cruxes independently, then
  intersect. Terminal condition: "until you end up with something you can research
  or run an experiment on." Dissolution counts as success.
  Critique (*Contra Double Crux*): single cruxes are "the exception rather than the
  rule"; cruxes are frequently **asymmetric**; validity check **P(C) ≥ P(B)**.
  Even the canonical source concedes the multi-crux case.
- **FRI's crux funnel**, the only fully operationalized version found: cruxes are
  "short-term indicators, usually resolving by 2030, that would cause the largest
  updates in expectation"; ~250 candidates; 10-minute flash forecasts; survivors
  promoted to ~1-hour questions; elicit P(Crux) and P(headline | Crux) *per camp*;
  rank by expected update.
- **ACH diagnosticity**: "**Evidence is diagnostic when it influences your
  judgment on the relative likelihood of the various hypotheses.** If an item of
  evidence seems consistent with all the hypotheses, it may have no diagnostic
  value." Heuer's *linchpin assumption* is the crux by another name, and his
  observation: analysts "often realize that their judgments are actually based on
  **very few factors**."
- **Jadad discordance walk**: when two credible reviews disagree — same PICO? same
  primary studies? quality weighting? eligibility boundary? time window? Replication
  study found it non-reproducible as a *selection* tool (62% disagreement), so the
  agent recorded it as a locator, not an adjudicator.
- **SEP's subtraction**: the *Immigration* conclusion locates the disagreement by
  naming what nobody holds — "**no one defends the status quo**", "**everyone
  acknowledges** that the current situation… is utterly indefensible", "no one
  defends all the measures that existing states currently employ."
- **SEP's premise location**: "This objection shows that the argument from a right
  to life has (at least) one controversial assumption: either premise 1 or premise
  2 is controversial."
- **IBIS direct-successor edges**: "Issue I₂ is a **direct successor** of issue I₁:
  I₂ challenges a statement made in support of one of the positions maintained in
  view of I₁." Three exits per issue: settled, further evidence required, or "the
  significance of Iᵣ can be denied and substitute issues may be introduced."
- **NIF's give-up test**: "Which trade-offs are we willing to make to move in a
  shared direction? Which are we unwilling to make?"
- **IPCC evidence×agreement as a diagnostic**: robust evidence + low agreement ⇒
  the disagreement is not empirical; limited evidence + high agreement ⇒ consensus
  outrunning data; limited + low ⇒ genuinely open.
- **Scott Alexander's ladder**: the top rungs are **operationalizing** and
  **high-level generators of disagreement**, which appear "when everyone
  understands exactly what's being argued, and agrees on what all the evidence
  says."

### The measured result that constrains all of them

**FRI's adversarial collaboration**: n=22, 8 weeks, medians of 80 vs 31 hours of
deliberation. Skeptic median 0.10% → 0.12%; concerned 25% → 20%. The best crux
moved the median pair from 22.7pp apart to 21.48pp — **~5% of the gap.**
Engagement and comprehension were explicitly ruled out as explanations: both sides
could summarize each other correctly and still disagreed.

What the disagreement rested on instead, in four layers: differing **priors on how
the world changes** ("Skeptics were somewhat anchored on the assumption that the
world usually changes slowly"); differing **evidentiary standards** (skeptics
wanted real-world demonstrations, the concerned group "more willing to place
weight on theoretical arguments with multiple steps of logic") — described as a
**meta-crux about admissible evidence that no empirical question can settle**;
**social/epistemic deference**; and timeline scale (median year AI displaces
humans: **2045 vs 2450**).

XPT's parallel finding: "**Few minds were changed** during the XPT, even among the
most active participants, despite monetary incentives," with within-group spread
up to ~11 orders of magnitude.

Isch, Tetlock & Clark's 13-project meta-study: ~34% updated, 24% didn't, ~41% "it
was complicated." Kahneman: "Even successful collaborations will end with few
minds changing."

### Root divergence, measured

Truong, Puranam & Koçak, 1,072 disagreeing argument pairs. "Root divergence" is
"the **earliest point** in the reasoning chains where their beliefs conflict…
the point of disagreement that **does not logically depend on any earlier
conflict**."

| Premise type | Root divergence | Base rate | Ratio |
|---|---|---|---|
| causal | 36.85% | 27.95% | 1.3× |
| forecast | 26.68% | 15.11% | 1.8× |
| factual (current) | 18.84% | 38.13% | 0.5× |
| **definitional** | **17.26%** | **3.68%** | **4.7×** |
| **moral/evaluative** | **1.23%** | **15.13%** | **0.08×** |

χ²(4)=921.59, p<.001. The agent's reading: camps state moral premises constantly
but rarely *diverge* there first; they diverge on definitions, causal mechanisms
and forecasts.

### Publication conventions

- **XPT stage-3 team wiki**: "the strongest argument for the team's median
  forecast, along with rationales for lower- and higher-end forecasts that they
  considered plausible… **describe key areas of disagreement and uncertainty**."
  Appendix 7 publishes, per question, **Sources of agreement / Sources of
  disagreement / Sources of uncertainty**, each footnoted to a numbered
  participant's own words.
- **Kahneman Rule 5**: arbiter writes the introduction, results and agreed
  conclusions; "If significant disagreements remain, the participants should write
  individual discussions. The length of these discussions should be determined in
  advance."
- **Kahneman Rule 2**: each side records in advance what would change its mind
  **and** how it would interpret a disconfirming outcome — "recorded by the
  arbiter to prevent future disagreements about remembered interpretations."
- **Team A/Team B** requires each team to "**identify missing information that
  would buttress their hypotheses**."
- **ICD 203 Standard 3**: "**Assumptions are defined as suppositions used to frame
  or support an argument**… **Judgments are defined as conclusions based on
  underlying intelligence information, analysis, and assumptions.** Products should
  state assumptions explicitly when they serve as the linchpin of an argument."
- **Reuters SCENARIO**: the only convention found that attaches probabilities —
  "give some guidance on the probability of each scenario."
- **Sciencewise**: a delivery criterion is "**Capturing agreement, disagreement
  and uncertainty**," plus "**missed or unresolved areas of discussion**."
- **Pragma-dialectics' opening stage**, where parties "agree on procedural and
  substantive starting points," is identified by the agent as a section most
  products lack.

---

## 7. Sourcing and citation

### Measured citation density

artifact-analysis counted inline markers per 100 words of body prose:

| Artifact | Per 100 words | Claim type |
|---|---|---|
| SEP, *Ethics of Abortion* | 0.35 | normative argument |
| SEP, *Moral Status of Animals* | 0.57 | normative + empirical |
| Our World in Data | ~0.5–0.75 | empirical, plus 1,729 words of endnotes against 2,413 of body |
| CRS R49032 | 0.74 | law + administrative fact |
| CRS R44306 | 0.90 | same |
| Wikipedia, *Nuclear power debate* | 1.66 (lead: 5.39) | mixed |
| ProCon, *Vaccines* | 2.62 | empirical claims marshalled as argument |
| ProCon, *Animal Testing* | 3.62 | same |

Its stated pattern: "density tracks *claim type*, not *topic heat*." SEP's topics
are the most contested and have the lowest density "because their sentences are
arguments, and an argument is cited for provenance, not for permission."

### Standards

- **Reuters**: "**You must source every statement in every story unless it is an
  established fact or is information clearly in the public domain.**" /
  "You must source a contentious statement **each time it appears**." /
  "**There is no need to source statements of the obvious.**"
- **AP**: "**Anything in the AP news report that could reasonably be disputed
  should be attributed.**" With an escape valve: "For lengthy stories, attribution
  can be contained in an extended editor's note detailing interviews, research and
  methodology."
- **BBC 3.4.4**: "Content producers should be reluctant to rely on a single
  source." **3.4.6**: "If content producers have been unable to verify material,
  they should usually say so and attribute the information."
- **SEP**: Bibliography "is reserved for refereed publications"; non-refereed web
  material goes in Other Internet Resources. Citations are inline parentheticals
  "(Author Year, page)" and "**they should not be used solely for citations**" in
  footnotes — footnotes are for substance.
- **Wikipedia PARITY**: "the lack of peer-reviewed criticism of creation science
  should not be used as a justification for marginalizing… scientific criticism of
  creation science, since creation science itself is not published in peer-reviewed
  journals." The source-quality bar for a critique is set by what it critiques.
- **Wikipedia FRIND**: the best sources "are… **outside the sourcing ecosystem** of
  the fringe theory itself."
- **Wikipedia SOURCEBIAS**: "biased sources are not inherently disallowed based on
  bias alone."
- **MEDRS**: "**Cite reviews, don't write them**," and per-claim source tiers —
  only biomedical claims need MEDRS.
- **IPCC**: "Priority should be given to peer-reviewed" literature; grey sources
  permitted if **retrievable and archived**.
- **Kettering, the anti-footnote position**: "**Footnotes are rarely helpful, as
  they tend to alienate people**, but a list of sources to double-check facts
  before publication is very important." Also advises against think-tank data and
  against quoting polarizing figures.
- **Cochrane's layered stack**: full review (every judgement footnoted) → Summary
  of Findings table (≤7 outcomes) → abstract → Plain Language Summary (400–850
  words, **no statistics, no confidence intervals, no certainty jargon, no
  recommendations**). The PLS restrictions are justified by reader testing:
  "Readers have indicated in feedback to us that they do not find these terms easy
  to understand."
- **PLS selection rule**: "**Focus on the comparison(s) that have the most clinical
  importance for decision makers, not the ones with the most data or the best
  results.**"
- **PLS funding disclosure**, as one neutral sentence: "Pharmaceutical companies
  funded 24 of the studies."
- **BBC 2.4.17 disclosure test**: "**The key test is to consider whether the
  audience would be misled if such information was not made available.**"
- **ICD 206**: an endnote "each time a source is directly cited… or a specific
  aspect of analysis… depends on a source," always to "the most original source,"
  plus a **source summary statement** covering "strengths and weaknesses of the
  source base, which sources are most important to key judgments, what sources are
  meaningfully corroborative or conflicting."
- **ProPublica**: span-level progressive disclosure, plus a methodology-note genre
  that always includes **what was withheld or unavailable**.
- **Wire-service de-duplication** (Wikipedia): "Multiple sources should not be
  asserted for any wire service article. Such sources are essentially a single
  source."

### Statistics handling (BBC Section 11)

| Clause | Rule |
|---|---|
| 11.4.1 | figures get "**no more and no less weight than the evidence supports**" |
| 11.4.3 | the source "is not as important as the quality of the data"; a source unwilling to show its methods "should be treated with caution" |
| 11.4.6 | peer review "is an indication of reliability but does not guarantee it" |
| 11.4.8 | percentage vs percentage points; "an unusual type of crime might have jumped by 300% but remain relatively low… from three to twelve" |
| 11.4.9 | projections give "the most likely number, rather than the most extreme value"; flags "up to", "as much as", "could rise to" |
| 11.4.10 | handle uncertainty "by rounding ('roughly 200,000' as opposed to '203,400')… and by reporting ranges" |
| 11.4.11 | "causation should not be implied without a high threshold of proof" |

**IPCC ¶4 framing symmetry**: "a 10% chance of dying is interpreted more
negatively than a 90% chance of surviving… **Consider reciprocal statements to
avoid value-laden interpretations.**"

**IPCC ¶5, against over-hedging**: "in some cases, it may be appropriate to
describe findings for which evidence and understanding are overwhelming **as
statements of fact without using uncertainty qualifiers**."

**IPCC conditional findings**: "the degree of certainty in findings that are
conditional on other findings should be evaluated and **reported separately**."
The agent's note: this is the fix for "if X then Y, and Y is catastrophic"
receiving one confidence label.

### Calibrated wording

**GRADE guidelines 26** — wording as a function of certainty × effect size:

| | High | Moderate | Low | Very low |
|---|---|---|---|---|
| Large | "X results in a large reduction in Y" | "X **probably** results in…" | "X **may** result in…" / "**The evidence suggests**…" | "**The evidence is very uncertain about** the effect of X on Y" |
| Moderate | "X reduces Y" | "X probably reduces Y" | "X may reduce Y" | same |
| Small | "X reduces Y **slightly**" | "probably… slightly" | "may… slightly" | same |
| Trivial/none | "**little to no difference**" | "probably… little to no difference" | "may… little to no difference" | same |

Derived empirically: workshops with 80 attendees plus 110 surveyed users,
"revising the wording of those that were unacceptable to ≥40% of participants."
For a genuinely two-sided estimate, the sanctioned phrasing is "**It is unclear
if** intervention has an effect on outcome."

**Cochrane PLS certainty translation**: High → "We are confident that…";
Moderate → "We are moderately confident in the evidence because…"; Low → "We have
little confidence in the evidence because…"; Very low → "We are not confident in
the evidence because…" With the style instruction: "**Do not refer to evidence
being 'downgraded', just explain why you are less than confident.**"

**IPCC traceable account**: "a description in the chapter text of your evaluation
of the type, amount, quality, and consistency of evidence and the degree of
agreement, which together form the basis for a given key finding."

---

## 8. Stopping rules

**automated-research's verdict on the LLM literature**: "Every published system
uses a fixed budget or the model's own 'is this enough' judgment. **There is no
principled or evaluated stopping rule anywhere in the literature**," and "unaware
of termination conditions" is 12.4% of measured multi-agent failures.

What exists elsewhere:

| Family | Rule |
|---|---|
| **Pre-specification** | Cochrane: grouping and eligibility "made independent of knowing which studies will be included." Post-hoc changes legal, **silent** ones not: "document all post hoc changes" |
| **Fixed source list** | "Always search Cochrane CENTRAL, MEDLINE… and Embase"; specialized databases "restricted to 1-2 additional sources, or omitted if time and resources are limited" |
| **Citation-chasing as a terminal audit** | reference lists screened "**AFTER** screening of the abstracts and full texts," to detect what searches missed |
| **Numeric saturation** | base 4, run 2, threshold ≤5% (§2) |
| **Agreement-gated shortcuts** | dual-screen 20%, proceed single-pass only when "reviewer agreement is high (**at least 80%**)" |
| **Effort-bounded** | "only including the top N results"; or stop at consecutive non-relevant records reaching "1% of the total found papers (with a minimum of 25)" |
| **External gate** | the advisory committee signs off; the subject editor accepts; CRS's four-tier review chain ending in the front office |
| **Structural ceilings** | Oregon CIR 250 words per statement; POSTnote 4 pages; Reuters Factbox "maximum of five key facts", Explainer 200–600 words, chronology ≤10 dates; SEP ~12,000 words with a consultation trigger |
| **Wicked-problem rule** | Conklin #2: "Wicked problems have no stopping rule… The problem solving process ends when you run out of resources, such as time, money, or energy, not when some optimal or 'final and correct' solution emerges" |
| **Triage before research** | Tetlock commandment 1: skip clocklike questions (answerable by a rule of thumb) and cloudlike ones (no method resolves them) |
| **Convergence stop** | do not keep researching hoping disagreement dissolves — FRI burned 25–100 hours per participant to move 0.10%→0.12% |

Honest statements about the limit:

- Computer-assisted screening review: when all relevant records have been found
  "is **unknowable** because we do not know a priori the total number of relevant
  documents," so a review "needs methods that effectively **manage the risk** of
  missing more studies than would be acceptable."
- Hunter's anti-perfectionism rule: "a part of you still wants to believe it isn't
  so, **which leads you to think you'll never have enough data**… **Stay within
  the limits of what you have found**, but show respect for your own work, and
  get it out."
- Reuters' publish test: "**It's better to be late than wrong. Before pushing the
  button, think how you would withstand a challenge or a denial.**"
- Walton on critical questions: "Closure to asking of critical questions thus
  depends on the stage a dialogue is in."
- Kettering's stopping rule is a **test forum**, not saturation: "if people in
  multiple conversations all tend to gravitate to one option, it may mean that
  the others are not argued strongly enough."

### The rapid-review tradition's exit

- Named shortcuts are legitimate **iff declared**: "Methods are documented
  transparently and **shortcuts are clear to see**."
- The one shortcut that changes what the product may be used for is dropping
  quality appraisal — recommended only for "**general** understanding… and to
  inform general policy direction," not "directly for specific policy
  decision-making."
- "you may conclude that a rapid review **is not worth it**."
- Rapid reviews are "less effective where research questions do not easily map on
  to the existing body of evidence," and social-policy questions of the "why did
  this work / under what circumstances / is it acceptable" kind "are harder to
  answer."
- The **named-landmark failure**: a 2021 UK POST rapid review on water
  fluoridation needed a seminal 1970s study — "**Without including this influential
  study, the review would have been seriously flawed.**"

---

## 9. Measured LLM failure modes

### Citations

| Measure | Range across 14 frontier models |
|---|---|
| link works | 80.8–100% (frontier >94%) |
| content topically relevant | 60.6–95.7% (frontier >80%) |
| **fact actually supported by the source** | **24.4–76.8%** |

Authors' warning: high link validity and topical relevance "may create a false
sense of trust."

DeepResearch Bench FACT scores: Perplexity 90.24%, Grok 83.59%, Gemini 2.5 Pro
81.44%, OpenAI Deep Research 77.96%.

Pre-agentic baseline (Liu et al.): only **51.5% of generated sentences fully
supported** by their citations; only 74.5% of citations support the sentence they
are attached to.

**URL hallucination** (53,090 citation URLs, ten models): "**3–13% of citation
URLs are hallucinated**—they have no record in the Wayback Machine and likely
never existed—while 5–18% are non-resolving overall. Deep research agents generate
substantially more citations per query than search-augmented LLMs but hallucinate
URLs at higher rates." Agents self-correcting with a resolution tool cut
non-resolving URLs "by 6–79× to under 1%."

**Fabrication without grounding**: 636 citations across 42 topics — **18% of GPT-4
citations entirely fabricated, 24% of the real ones containing substantive
errors**. GPT-4o in mental-health literature reviews: 19.9% fabricated, 45.4% of
apparently-real ones carrying bibliographic errors. **Fabrication tracks topic
obscurity**: 28–29% for body dysmorphic disorder vs 6% for major depressive
disorder.

**Citation laundering**: a source topically related but **under-warranting the
force of the claim** — "linked to" cited as "causes."

### Poisoned sources

"Introducing **one** misleading document increases the mean false-conclusion
adoption rate from 0% in the no-injection control to **54.7%**… Pre- and
post-research defenses reduce FCAR but do not eliminate adoption."

### Cheap checking

**MiniCheck**: a 770M Flan-T5 scores **74.7% balanced accuracy on LLM-AggreFact
vs GPT-4's 75.3%** (Claude-3 Opus 74.1%, prior SOTA AlignScore 70.4%) at **>400×
lower cost** — $0.24 vs $107 for the full test set.

**VeriFastScore**: 6.6× wall-clock speedup, r=0.80 claim-level and r=0.94
system-level correlation with full VeriScore.

**Full verification costs**: VeriScore per response ≈ 60 LLM/API calls (14
extraction, 23 search, 23 verification), ~104 seconds, ~$0.017 in search fees.
SAFE agrees with human annotators on 72% of individual facts, wins 76% of sampled
disagreements, 20× cheaper than human annotation.

**Counter-caveat**: on BIONLI-300, atomic decomposition + web search beat
sentence-level MiniCheck by +6.0 factual F1 and +7.35 balanced accuracy — so
decomposition adds real signal where claims are compound.

**Claimify** is cited as the right extraction pattern: extract a claim only when
the source text has one high-confidence interpretation, carrying forward enough
context to make the claim self-contained.

### Self-correction and refinement

- **Huang et al., "LLMs Cannot Self-Correct Reasoning Yet"**: without external
  feedback, self-correction fails and **performance often degrades**.
- **Stechly et al., "GPT-4 Doesn't Know It's Wrong"**: on graph colouring, GPT-4
  is no better at verifying than producing, and "**the correctness and content of
  criticisms… seems largely irrelevant to the performance of iterative
  prompting**." Apparent gains came from the right answer appearing in the
  sampled completions and being selected by an *external* verifier.
- **Multi-agent debate underperforms plain self-consistency** at equal agent
  count, and can overturn correct single-agent answers.
- **TTD-DR** (retrieval-grounded revision) shows the opposite: win rate 39.4% →
  60.9% (self-evolution) → **69.1%** (denoising with retrieval). Retrieval-grounded
  revision at step 9 beat 20 steps of self-evolution by 4.2%. "Denoising with
  retrieval at step 9 incorporates 51.2% of final report information."
- **ALCE**: reranking over sampled generations by citation recall raised ASQA
  citation recall from 73.6% to 84.8% — generate-N-and-select against an external
  metric, not critique-and-repair.

### Judges

- **SycEval**: sycophantic capitulation in **58.19%** of cases (Gemini 62.47%,
  ChatGPT 56.71%), with **78.5% persistence** once triggered.
- **Self-preference** correlates linearly with self-recognition; a 2025 EMNLP
  paper finds it "largely disappears once output quality and judge severity are
  controlled." What is robust: **disclosed authorship labels shift judgments
  symmetrically.**
- **Position bias** runs 10–15 points, with reports of judges picking the first
  option in **68%** of comparisons. Calibration prompting moves 68% → 58%; **swap
  augmentation** (evaluate both orders, accept only consistent verdicts) is the
  structural fix.
- **Cross-family verifiers beat self-verification**, because self-consistent
  errors are largely model-specific. Documented asymmetry: strong generators
  produce internally coherent wrong answers that verifiers find *harder* to reject.
- **Context blindness** cuts the other way: context generally *helps* verification
  accuracy, via recall at some precision cost.
- Anthropic's eval guidance: **one** LLM judge, one call, one prompt, 0.0–1.0 plus
  pass/fail "was the most consistent"; "grade each dimension with an isolated
  LLM-as-judge"; give the judge an escape hatch to return "Unknown"; calibration
  bar "**well below ~90% on clear-cut cases means the judge prompt needs another
  iteration**"; negative controls (empty string, "I don't know", a confident answer
  to the wrong question). And: "**An LLM judge being gamed looks exactly like a
  breakthrough until you check.**"
- Anthropic's Agent SDK blog: LLM-as-judge is "generally not a very robust method,
  and can have heavy latency tradeoffs" — prefer rules-based feedback first.

### Other measured modes

- **Context rot** (18 frontier models): performance degrades with input length
  non-uniformly and well before the window fills; degradation is **steeper when
  needle-question semantic similarity is low**; a single distractor measurably
  hurts; shuffled haystacks outperformed logically coherent ones.
- **Search-induced bias**: retrievers optimizing semantic similarity to a loaded
  query act as an echo chamber; dense retrievers carry brevity, position,
  literal-matching and repetition biases. Deep-research reports "over-depend on a
  few sources, recycling them across sections with only phrasing changes."
- **Over-association of unrelated facts** — named in STORM's expert study as
  distinct from hallucination: every fact sourced and true, the connection
  invented. Per-claim checking is blind to it by construction. **No measured
  mitigation found.**
- **Source bias transfer** — STORM's generated text inherited non-neutral tone
  from sources; "significant" appeared 17 times in one article.
- **MAST** (150 traces, κ=0.88, 1,600+ annotated): multi-agent failure rates
  **41–86.7%**; causes distributed as system design 44.2% / inter-agent
  misalignment 32.3% / task verification 23.5%. Top modes: step repetition 15.7%,
  reasoning-action mismatch 13.2%, unaware of termination 12.4%. Tactical fixes
  bought only +9.4% to +15.6%.
- **Eval awareness**: unintended-solution rate **0.24% single-agent vs 0.87%
  multi-agent — 3.7×**.
- **LLMs over-apply NPOV**: ~64% accuracy detecting biased edits; "extraneous
  non-NPOV changes beyond neutralization"; removed 79% of the words editors
  removed but rewrote more broadly. **Crowdworkers rated the AI rewrites *more*
  neutral and fluent.**
- **WMF caution**: "Exercise caution assuming that LLMs are effective at
  evaluating NPOV… Wikipedia content is a near-ubiquitous source of training data."
- **Generated critical questions** fail as "(a) the introduction of new concepts
  or topics… (b) bad reasoning, namely, **questions critical towards positions or
  claims the speaker does not hold**; or (c) non-specific critical questions."
  With a bare prompt, "**over 10% of the generated questions ask about claims the
  speaker does not hold**."

---

## 10. Research architecture

### STORM's ablation

| Config | Outline soft recall | Unique refs |
|---|---|---|
| STORM | 86.26% | 99.83 |
| w/o perspective | 84.49% | 54.36 |
| w/o conversation | 77.97% | 39.56 |
| Direct generation | 80.23% | — |
| outline-driven RAG | 73.59% | — |

automated-research's reading: removing perspectives costs ~1.8 points of outline
quality but nearly halves the evidence base; removing **multi-turn conversation**
collapses to RAG-baseline quality. "Perspectives buy source breadth; iterative
multi-round retrieval buys quality."

STORM's own stated limitation: output "may still be biased towards dominant
sources on the Internet."

**Co-STORM** adds a **Moderator** that asks questions derived from
retrieved-but-unused information.

### Parallelism

- **LangChain Open Deep Research** built parallel section-writing agents and
  abandoned them: "the reports were disjoint because the section-writing agents
  were not well coordinated." Current design confines parallelism to research and
  writes sequentially in one pass. Sub-agents get isolated context and **prune
  findings before returning**.
- **Under matched thinking-token budgets**, single-agent beat or tied five
  multi-agent architectures on FRAMES and MuSiQue. Multi-agent became competitive
  "only under context degradation."
- **Anthropic's multi-agent post** reports 90.2% improvement over single-agent
  Opus 4 on an internal eval, ~15× token multiplier, and caveats that are often
  dropped: "some domains that require **all agents to share the same context** or
  involve **many dependencies between agents** are not a good fit"; "LLM agents
  are not yet great at coordinating and delegating to other agents in real time";
  observed early failures included spawning 50 subagents for simple queries.
  automated-research notes these figures are from June 2025 and predate several
  model generations.
- **Deduplication across parallel workers**: "**This is the weakest-evidenced area
  in the whole survey.** There is no paper with measured dedup numbers." Published
  practice is design-level only.
- Convergent open-source architecture: *decompose → fan out with isolated context
  → compress each worker's findings → single synthesis*. Worker return contract:
  key findings, evidence with citations, confidence, what it could not find.

### Evidence-synthesis automation

What transferred: screening/triage with human supervision. RobotReviewer LIVE hit
**100% recall at 55% precision**. An LLM living-review engine reproduced a
published meta-analysis's conclusion in **32 minutes for $1.95 vs an estimated 58
hours and $2,900–5,800**.

What did not: **structured data extraction** — exact agreement on mortality event
counts for only **4 of 7** studies (57%). Adoption is near-nil: ~5% of
Cochrane/Campbell reviews explicitly reported using ML.

Design rule the agent drew from it: recall-first in search/triage, precision-first
in extraction.

**IPPO's position on automation**: "The best approach is **semi-automation**: using
machine learning to expedite tasks, rather than complete them"; "**Full automation
is not yet a realistic alternative** for rapid reviews."

### Cognitive overhead

Buckingham Shum et al., on 15 years of argumentation-support systems, decompose
the work into four interleaving tasks: **unbundling**, **classification**,
**naming**, **structuring**. Conclusion: "DR that yields insight into the complex
ideas and arguments that may lie behind a decision does not come 'for free'."
Historical failure: "it was relatively easy for an IBIS discussion to overwhelm
any manual system."

Sprawl is measured: a Diablo Canyon debate map "could not be rendered all on
screen at once."

---

## 11. Where sources disagree

**1. Equal space versus proportional prominence.**
The **Citizens' Assembly on Brexit** named the choice and took the first option:
> "One view of balance says that each perspective should receive equal attention
> and credit. This is, broadly, the approach that the BBC takes to referendums…
> Another view of balance says that each perspective should receive attention in
> proportion to the number and credibility of its adherents. This is the approach
> that the BBC now takes to discussions of climate change… The approach to balance
> that we adopted… was close to the first of these options. **At the same time, we
> also indicated to Members where there was an imbalance in the numbers of
> adherents.**"

**BBC 2.2.7** takes the second: minority views "do not need to be given similar
prominence or weight."

Both are the BBC, applied to different question types. Unresolved here.

**2. Wikipedia forbids what our design does.**
WP:IMPARTIAL: "Try not to quote directly from participants engaged in a heated
dispute; instead, summarize and present the arguments in an impartial, formal
tone." artifact-analysis recorded its own disagreement: "I think Wikipedia is
wrong here and our design is better… but the price of in-voice is that voice
boundaries must be enforced mechanically."

**3. Wikipedia forbids per-position pages; SEP maintains them.**
WP:NPOVFORK bans a dedicated page per viewpoint. SEP maintains `compatibilism`
and `incompatibilism-theories` alongside `freewill`, "often written by advocates
of that position," held together by a parent survey and a routing table.

**4. Blind verification.**
Anthropic documents that "separate fresh-context verifier sub-agents tend to
outperform self-critique," and its verification guidance is always **grounded** —
"find a direct quote from the documents that supports it." automated-research
found evidence that context *helps* verification accuracy. claude-practices
recommends splitting the blindfold: blind to authorship and provenance, not to
sources.

**5. Stopping rules.**
automated-research: "no principled stopping rule anywhere in the literature."
Evidence-synthesis: a numeric saturation rule exists and is published (base 4, run
2, ≤5%). Not in conflict — different literatures — but the first agent's claim is
too strong as stated.

**6. Does structure help?**
ACH is the best-measured structured technique and it does **not** improve
accuracy: 50 practising analysts, randomized — hypothesis enumeration no benefit
(92% vs 100%, p=.149); evidence completeness benefit (92% vs 68%); diagnosticity
benefit (80% vs 32%); **base-rate use got worse** (12% vs 52%, p=.002); **scoring
consistency got worse** (4% vs 44%, p=.003); **80% of the ACH group produced tied
ranks vs 19% of controls**. What predicted accuracy in both groups was internal
consistency (80% vs 31%, OR 8.89). Chang et al.'s diagnosis: ACH "does not provide
detailed guidance on how 'consistency' should be defined," and students disagree
on 20–30% of cells. Their general warning:
> "**SATs may serve only as a vehicle transporting subjectivity from one end of
> the process to the other. The SAT process becomes an end in itself, dressing up
> subjective judgments in a cloak of objectivity.**"

---

## 12. Audit of our shipped content (artifact-analysis, verified)

**Camp names leak valence.** `nuclear-energy` runs *Climate Pragmatist / Cost
Skeptic / New-Nuclear Advocate / Risk-First Skeptic* — the two pro camps get
Pragmatist and Advocate, both anti camps get Skeptic. "Nobody self-describes as
the non-pragmatist," and in energy discourse "skeptic" carries a denial echo. The
agent's rule: name camps by what they want, never by how they reason. *Skeptic,
Realist, Pragmatist, Alarmist, Denier, Purist* are posture labels.

`vaccine-mandates` is cited as the counter-example done right: *Herd Immunity
Guardian / Conscience Exemption Broadener / Institutional Risk Owner / Schedule
Minimalist / Medical Freedom Campaigner / Vaccine Confidence Builder.*

**Self-names abandoned.** `housing` has *Supply Liberalizer* with no YIMBY
anywhere. Analyst coinages flagged as failing recognition: *Membership by
Presence, Cohesion Communitarian, Tenant Decommodifier, Hassle Factor Architect,
Deployment Witness.*

**Two nuclear "camps" have empty `representative_name` and `proponents`** —
verified. They are also a different taxonomy: *Go all-in: a fast, standardised
build-out* and *Keep existing plants, bet new money on renewables* are
prescriptions, not camps, mixed into the same list.

**Positions carry no source fields.** Unattributed numeric claims in position
prose: nuclear-energy **13 in 1,133 words**, vaccine-mandates 14, housing 14,
ai-alignment 12. Examples running unsourced: "France still draws about 69% of its
electricity from nuclear"; "about $21 billion over budget at a total cost near $35
billion"; "roughly £48 billion in today's money."

**Basics sourcing is uneven** — verified: nuclear-energy has 12 stats, **9 with
`source_url`, 7 with `source_published`**. Other topics are at 100%.

**Steelmen rebut themselves.** From `New-Nuclear Advocate.detail`: "But the model's
fragility is real too: NuScale's flagship US project in Idaho collapsed in 2023…"
From another: "Critics counter that deep decarbonisation eventually needs firm
low-carbon power…"

**Hedge inventory in the same file**: "the argument goes", "From this view", "on
this view", "the skeptic notes", "the skeptic reads that as", "Advocates argue",
"Proponents argue", "The case here is about."

**UK spellings** in nuclear-energy against the US-spelling invariant:
decarbonisation, standardised, programme, labour.

**A question is mistyped, and its own field says so** — verified. "Is the waste
problem solved in principle, but unsolved in practice?" is tagged `kind: value`;
its `why` explains "the gap is political, not technical."

**The crux orphans a camp.** Nuclear's crux is a single axis (cost as fixable vs
chosen); `Risk-First Skeptic`, a tier-1 camp, sits on a different axis
(irreversible tail risk).

**Scale.** Immigration carries **twelve** positions across three tiers;
ai-alignment ten with 4,990 words of position prose. SEP, with no length limit,
presents six.

**What it rated positively.** "**Crux is our best section and it has no peer in the
corpus.** Nothing in ProCon, Wikipedia, CRS, or Full Fact attempts it." Quoted
approvingly: "Grant that an animal can suffer, and the argument has barely
started." / "Every camp has an alignment method; none can say what would count as
proof it worked." Also praised: `scope_covered`/`scope_excluded` as "the single
most under-imitated good practice in the field," and the Basics `note`/`detail`
split.

**Sections it questioned.** *Actions*: "Not one of the strong artifacts has this
section… on a genuinely contested question, any concrete action list encodes a
conclusion about which side is right." The methods agent reached the same
conclusion independently via the honest-broker standard. *Agreed facts*: currently
buried in `crux.subtitle`; both agents propose promoting it. *Missing position
fields*: what this camp grants to the others, and what would change its mind.
*Missing page metadata*: a vintage stamp and a reading-time/layer signal.

---

## 13. Named gaps and unverified items

- **AP's false-balance rule** is quoted only from hostile secondary sources.
- **Kialo** could not be read (login-walled, unarchived), so the argument-tree
  question is unanswered.
- **The Economist** publishes no primary account of briefing commissioning, word
  budget, or red-lining; circulating word counts are unsourced.
- **Reuters has no documented "Explainer:" convention** — only ANALYSIS, FEATURE,
  FACTBOX, SCENARIO.
- **research-methods' six sub-researchers' reports never reached it**; roughly
  half that report is from model knowledge, self-tagged.
- **No measured mitigation exists** for over-association of unrelated facts.
- **No measured deduplication numbers** for parallel research agents.
- **No Anthropic guidance** on effort levels for generative writing versus
  adversarial checking, or on waiting out subscription rate-limit windows.
- **`TASK_MAX_OUTPUT_LENGTH` default** is unresolvable from the minified bundle.
- **The "balance penalty"** in LLM judges is from a blog post, not peer-reviewed.
- **Self-preference bias magnitude** is contested once quality and judge severity
  are controlled; the **label** effect is the robust part.
- **No published anti-brigading policy** for Kialo-style crowd voting.
- Two claims worth holding beside a one-day budget. Kettering, on the
  concern-clustering step: "There is no easy way to perform this work. **It cannot
  be automated.** It requires judgment." And the BBC's 2012 follow-up: "in a wide
  range of areas (for example, badger culling, stem cell research, genetically
  modified food or **nuclear energy**) **it is harder to delineate where the
  scientific consensus might lie**" — resolved by spending "many months gathering
  guidance and information from a range of distinguished experts."
