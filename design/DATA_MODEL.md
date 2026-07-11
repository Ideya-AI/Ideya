# Infinity — Data Model

The canonical content schema. Every page and component renders some slice of a `Topic`.

## Schema (`types.d.ts`)

```ts
/**
 * Infinity — core data model.
 *
 * The shape of a Topic and its parts. This is the source of truth for the
 * content schema: every page mock and component renders some slice of a `Topic`.
 * Hand this file to engineering as the canonical type contract.
 */

/** A stable hex or CSS custom-property reference, e.g. "var(--pos-green)". */
export type ColorToken = string;

/** Phosphor icon name without weight prefix, e.g. "atom", "leaf". Rendered duotone. */
export type IconName = string;

/** Reading depth. Every section degrades to `condensed` for sharing/print. */
export type Depth = "condensed" | "normal" | "deep";

/** Top-level category. Color is used ONLY in discovery tiers, never on a topic page. */
export interface Category {
  id: string;
  name: string;
  icon: IconName;
  /** One of the --cat-* tokens. */
  color: ColorToken;
  description: string;
  /** Sibling/parent categories this one connects to (ids). */
  connectsTo?: string[];
  topicCount: number;
}

/**
 * A named position in a topic's debate — the "heart".
 * Positions are NON-1:1 with questions (one may span several). Written in the
 * side's own voice. Color is assigned per-topic and carries no fixed meaning.
 */
export interface Position {
  id: string;
  name: string;
  /** One of the --pos-* tokens, unique within the topic. */
  color: ColorToken;
  /** The strongest one-line case, in the side's own voice. Always shown. */
  steelman: string;
  /** 3–5 sentences of reasoning. Revealed at normal/deep. */
  description: string;
  /** A person/org/case that grounds the position — its "face". */
  representative?: { name: string; note: string };
  /** Names of notable proponents. */
  proponents: string[];
  /** Aggregated importance signal. Never reorders the sides. */
  importance: number;
}

/** An open question. Kind drives its tag color; importance reorders the list. */
export interface Question {
  id: string;
  text: string;
  kind: "empirical" | "value";
  /** Why the question is genuinely contested (revealed at normal/deep). */
  why: string;
  votes: number;
}

/** Maps a fact's *shape* to its fixed visualization (the chart vocabulary). */
export type VizKind = "ranked" | "radial" | "range" | "bar" | "sparkline";

/** One Basics figure. Title is the metric, not a sentence. */
export interface Stat {
  id: string;
  /** The metric name, e.g. "Deaths per TWh". */
  label: string;
  viz: VizKind;
  /** Headline value for bar/radial/range/sparkline vizzes. */
  value?: string;
  /** Series for ranked/sparkline. `highlight` marks the subject row. */
  series?: { label: string; value: number; highlight?: boolean }[];
  /** Endpoints for a range marker. */
  range?: { min: string; max: string; at: number };
  note?: string;
  source?: string;
}

/** A way to engage. Balanced across the position landscape; never weighted/ranked. */
export interface Action {
  id: string;
  kind:
    | "Learn more"
    | "Donate"
    | "Volunteer"
    | "Policy"
    | "Local engagement"
    | "Submit personal view";
  title: string;
  description: string;
  url: string;
  /** Optional position alignment (id). Unaligned actions belong to no side. */
  forPosition?: string;
}

/** The synthesis: where the real disagreement narrows. The one dark section. */
export interface Crux {
  /** The narrowing, set in display type. */
  lead: string;
  /** The framing — usually an empirical-vs-values split. */
  subtitle: string;
  empirical: string;
  values: string;
}

/** A complete topic — one structured infographic, six sections, fixed order. */
export interface Topic {
  id: string;
  name: string;
  icon: IconName;
  categoryId: string;
  /** 1–2 sentence, jargon-free. */
  summary: string;
  scope: { covered: string; excluded: string };
  whyNow: string;
  relatedTopicIds: string[];
  basics: Stat[];
  questions: Question[];
  positions: Position[];
  crux: Crux;
  actions: Action[];
}
```

## Worked example (`nuclear-energy.example.ts`)

A fully-populated fixture to build and test against.

```ts
/**
 * Worked example of the Topic data model (see types.d.ts).
 * One fully-populated topic — the canonical fixture engineering can build against.
 */
import type { Topic } from "./types";

export const nuclearEnergy: Topic = {
  id: "nuclear-energy",
  name: "Nuclear Energy",
  icon: "atom",
  categoryId: "energy",
  summary:
    "Fission-based electricity — among the lowest-carbon, lowest-death sources, in a debate that scrambles partisan lines.",
  scope: {
    covered: "Civilian fission for grid power: cost, safety, waste, the climate case.",
    excluded: "Weapons, fusion, naval propulsion.",
  },
  whyNow:
    "A retiring fleet meets climbing demand from AI and electrification, just as climate targets need firm clean power.",
  relatedTopicIds: ["solar-power", "grid-storage", "ai-existential-risk"],

  basics: [
    {
      id: "deaths",
      label: "Deaths per TWh · lifecycle",
      viz: "ranked",
      series: [
        { label: "Coal", value: 24.6 },
        { label: "Gas", value: 2.8 },
        { label: "Nuclear", value: 0.03, highlight: true },
        { label: "Solar", value: 0.03 },
      ],
      note: "Among the safest sources — including Chernobyl and Fukushima.",
      source: "ourworldindata.org",
    },
    { id: "share", label: "Share of global power", viz: "bar", value: "9%", note: "Down from a ~17% peak in 1996." },
    { id: "capacity", label: "Capacity factor", viz: "radial", value: "92%", note: "Highest of any source — runs around the clock." },
    {
      id: "co2",
      label: "Lifecycle CO₂ · g/kWh",
      viz: "range",
      value: "12 g",
      range: { min: "clean", max: "gas ~490", at: 5 },
      note: "Among the lowest of any source.",
      source: "IPCC AR5",
    },
  ],

  questions: [
    {
      id: "cost",
      text: "Are runaway Western nuclear costs fixable, or structural?",
      kind: "empirical",
      why: "Korea builds at ~¼ the per-kW cost. If costs reflect lost supply chains, reform helps — if safety preferences, it won't.",
      votes: 142,
    },
    {
      id: "waste",
      text: "Is the waste problem solved in principle, but not in practice?",
      kind: "value",
      why: "Disposal is settled science; Finland's Onkalo runs. Yet most countries have no sited repository — the gap is politics, not engineering.",
      votes: 98,
    },
  ],

  positions: [
    {
      id: "pragmatist",
      name: "Climate Pragmatist",
      color: "var(--pos-green)",
      steelman: "The only proven, scaled, firm low-carbon source we have.",
      description:
        "Nuclear is the only dispatchable zero-carbon power that already runs at scale. IPCC 1.5 °C pathways lean on expanding it; Germany's phase-out raised emissions.",
      representative: { name: "James Hansen", note: "climate scientist who broke with much of the green movement to back nuclear." },
      proponents: ["James Hansen", "Stewart Brand", "Clean Air Task Force"],
      importance: 142,
    },
    {
      id: "cost-skeptic",
      name: "Cost Skeptic",
      color: "var(--pos-amber)",
      steelman: "Too slow and costly to be the rational marginal climate dollar.",
      description:
        "Vogtle and Hinkley Point C ran years late and billions over. Renewables keep getting cheaper on a learning curve nuclear has never shown.",
      representative: { name: "Amory Lovins", note: "physicist and advocate of the efficiency-and-renewables path." },
      proponents: ["Amory Lovins", "BNEF analysts", "Mark Z. Jacobson"],
      importance: 74,
    },
    {
      id: "advocate",
      name: "New-Nuclear Advocate",
      color: "var(--pos-blue)",
      steelman: "Advanced reactors and serial builds can fix the cost problem.",
      description:
        "SMRs and Gen-IV designs trade gigawatt megaprojects for factory-built, repeatable units. Learning-by-building drives costs down — the West simply stopped building.",
      representative: { name: "TerraPower", note: "Gen-IV developer betting on factory-built reactors." },
      proponents: ["TerraPower", "NuScale", "Good Energy Collective", "DOE"],
      importance: 61,
    },
    {
      id: "risk-first",
      name: "Risk-First Skeptic",
      color: "var(--pos-rust)",
      steelman: "Catastrophic, intergenerational risks justify deep caution.",
      description:
        "Meltdowns, proliferation pathways, and waste that outlasts institutions are not ordinary risks. A decentralized renewable grid fails gracefully; a reactor does not.",
      representative: { name: "Naomi Oreskes", note: "historian of science writing on risk and trust." },
      proponents: ["Naomi Oreskes", "anti-nuclear NGOs", "parts of the Green movement"],
      importance: 52,
    },
  ],

  crux: {
    lead: "The debate narrows to one question.",
    subtitle:
      "Can the West build reactors on budget and on schedule — and is that an engineering problem or a values problem?",
    empirical: "If overruns are contingent — atrophied supply chains, one-off designs — then better data could settle it.",
    values: "If high costs encode real democratic caution about dread risk, then no data closes it — it's a choice.",
  },

  actions: [
    { id: "owid", kind: "Learn more", title: "Our World in Data — energy", description: "Lifecycle emissions and death rates across every source.", url: "#" },
    { id: "gec", kind: "Donate", title: "Good Energy Collective", description: "Progressive nuclear policy research.", url: "#", forPosition: "advocate" },
    { id: "rmi", kind: "Donate", title: "Rocky Mountain Institute", description: "Renewables-and-efficiency research.", url: "#", forPosition: "cost-skeptic" },
    { id: "nrc", kind: "Policy", title: "Comment on NRC reform", description: "Open dockets on advanced-reactor rules.", url: "#" },
    { id: "submit", kind: "Submit personal view", title: "Add your view to this topic", description: "Your reasoning is aggregated into the position landscape — not posted as a comment.", url: "#" },
  ],
};
```
