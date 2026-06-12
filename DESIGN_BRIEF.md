# Infinity — Design Brief

## What this is

A web app that maps hard human issues — existential/global risks, governance, economics, ethics — so that visitors can quickly understand the shape of an issue: what the topic actually is, where the live disagreements sit, who holds which position and why, and how to engage. The product is a **curated, navigable atlas of hard topics**.

## Positioning

**A visual wiki, sitting between encyclopedia and debate platform.** Closer to Our World in Data or a well-designed textbook than to Wikipedia or Reddit. Topic-first, not question-first — readers orient on what something *is* before being asked to take a side.

- Neutral by intention, not by audited performance. Let ideas lead. No bias-balance theater.
- Content is curated. Participation (votes, suggestions) is feedback that improves the content; never a destination of its own.
- Explicitly *not* social media. No feed, friends, follows, profiles.

## Visual feel

- Modern, minimalistic, generous whitespace.
- Mobile-first; desktop is a graceful expansion, not the primary canvas.
- Typography-driven. Inter as the typeface.
- Color used sparingly and meaningfully — color on positions distinguishes them; chrome is restrained.
- Every page must work as a printed/shared static image (see "depth-as-axis" below).

## Three-tier information architecture

Each tier has one job. No overlap.

- **Home** — discovery of everything.
- **Category** — scoped discovery (funnel to topics, not a destination).
- **Topic** — the actual content destination.

---

## Topic page (the main design surface)

A topic is **one structured infographic** rendered at variable depth. Six sections, fixed order, always rendered in this sequence when content exists:

### 1. Overview
What the topic *is*. Title + icon + 1–2 sentence description + scope (what's covered, what isn't) + why it matters now. Category badge(s) and a few "related topics" chips live inside this section. *Visual job: orient the reader in 10 seconds.*

### 2. Basics
The shared empirical landscape — facts most positions agree on. 6–8 stat cards (label / big value / one-line note / source link). May include charts. Low text, high scannable density. *Visual job: ground the reader in numbers before disagreement begins.*

### 3. Questions
The 4–6 open questions that drive disagreement. Each is a question text + 1–2 sentence "why it's contested." Mix of empirical (resolvable with better data) and value (require judgment). Users can vote importance, gradually reordering. *Visual job: surface contested questions cleanly; signal user agency without becoming a forum.*

### 4. Positions
The 3–5 genuine named positions. Each: name + color identifier + one-line steelman + 3–5 sentence description + notable proponents. Color is consistent within a topic (climate pragmatist = green throughout this topic). Positions are non-1:1 with Questions. Users can agree/disagree and vote importance. *Visual job: this is the heart of the page — present sides fairly and distinctively.*

### 5. Crux
1–3 paragraphs. The synthesis: where the real disagreement actually sits, often narrower than the headline positions suggest. Editorially the highest-value section. *Visual job: feel like the centerpiece — high typographic weight, set apart from the surrounding sections.*

### 6. Actions
6–14 real-world engagement options across types: learn-more, political/policy, donate, volunteer, local engagement, submit-personal-view. Each may be aligned with a specific position (so a user sees "for cost skeptics" or "for climate pragmatists" tags). *Visual job: give every reader a path forward without endorsing any.*

---

## Category page (funnel — not a destination)

Just three sections:

1. **Overview** — what this category covers; parent/sibling categories inline.
2. **Basics** — meta-facts about the category itself.
3. **Topics** — a scoped visual showcase of the topics in this category (the main reason someone visits).

No Questions/Positions/Crux/Actions. Categories lead to topics; they don't host their own intellectual content.

---

## Home page (4 sections)

1. **Nav bar** — Logo (left), Search with autofill for topics + categories (center), Menu (right).
2. **Topic Showcase** — the visually ambitious section. A "universe of topics" subtly grouped by category, subtly sized by some signal. Candidate metaphors: galaxy / map / forest. Selecting opens a compact preview + related topics. Must be visually compelling, performant, and mobile-graceful. *This is undesigned — open to exploration.*
3. **Project Purpose + Vision + Basics Carousel** — centered intro text + What/Why/How carousel.
4. **Topic Directory** — categorized list of topics. Smart grouping; less-popular topics collapse into "more."

---

## Depth-as-axis content model

The same topic is rendered at three depths — **not three separate pages**:

- **Condensed** — static, shareable, printable. Postable to socials. Same 6 sections, minimal text, mostly visual.
- **Normal** — same skeleton, text bodies grown out, visuals interactive.
- **Deep** — same skeleton again, with each section's "go further" pocket filled with curated external resources contextual to that section (not a separate Resources page).

Sections persist across all depths. Depth is a property the user controls — globally or per-section.

## Patterns that recur throughout (not standalone sections)

- **Going further** — every section has an outward path (sources, deeper reading) revealed at expanded depth.
- **Citations / sources** — attached inline to claims, facts, and positions.
- **Definitions** — hover/tap-to-define for contested or technical terms.
- **Representative examples** — a person, place, or case that grounds the abstract (especially in Positions).

## What this product is *not*

- Not Wikipedia (we surface contestation; they don't).
- Not Reddit/Kialo (we curate; we don't host argument trees).
- Not a news site (no feed, no recency bias, no events).
- Not an advocacy platform (no house position, no calls-to-action toward one side).

---

## Reference content for sizing (excerpt from the first topic, Nuclear Energy)

**Topic title:** Nuclear Energy
**Summary:** Fission-based electricity generation — among the lowest-carbon and lowest-death-per-TWh sources, but with stubborn Western cost problems and a debate that scrambles partisan lines.
**Category:** Energy & Environment

**Sample Basics card:**
- Label: *Deaths per TWh (lifecycle)*
- Value: **0.03**
- Note: *Coal ~24.6 · Gas ~2.8 · Wind ~0.04 · Solar ~0.03. Nuclear ranks among the safest sources, including Chernobyl and Fukushima.*
- Source: ourworldindata.org

**Sample Question:**
- *Are runaway Western nuclear costs a fixable institutional problem, or a structural feature of the technology?*
- South Korea's APR1400 builds at roughly a quarter the per-kW cost of the EPR or AP1000 in Europe and the U.S. If costs reflect supply-chain atrophy, one-off designs, and regulatory churn, reform could restore competitiveness. If they reflect democratic safety preferences and unavoidable complexity at gigawatt scale, no reform makes new nuclear competitive with solar+storage.

**Sample Position:**
- Name: **Climate Pragmatist** (color #4a9d6c)
- Steelman: *Deep decarbonization on the timeline climate science demands cannot rely on weather-dependent renewables alone; nuclear is the only proven, scaled, firm low-carbon source.*
- Description: 3–5 sentences elaborating the steelman with examples and references to IPCC pathways, the Energiewende, etc.
- Proponents: James Hansen, Stewart Brand, Clean Air Task Force, IPCC AR6 WGIII

**Sample Crux (first paragraph):**
> Once the rhetorical heat is stripped away, most of the nuclear debate collapses onto a narrower disagreement: whether the West can build nuclear plants on budget and on schedule, and whether that question is empirical or values-laden.

**Sample Action:**
- Type: Donate
- Title: *Good Energy Collective*
- Description: *Progressive nuclear policy research. 4-star Charity Navigator; Vox top climate nonprofit 2023–24.*
- Position alignment: *For New-Nuclear Advocate*

---

**Design ask:** Start with the topic page at normal depth (desktop + mobile). Treat the six sections as a vertically sequenced single artifact, not a tabbed app. Find a visual language that feels modern, minimalistic, and information-dense without being noisy. The Positions and Crux sections are the highest-leverage to get right.
