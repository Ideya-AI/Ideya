# Ideya — Component Source

The six reusable components, authored as React. Each has a typed props contract (`.d.ts`) and an implementation (`.jsx`). Recreate these in the target framework; preserve the prop contracts and the depth-awareness.


---

## TopicNode

### Props (`TopicNode.d.ts`)

```ts
import * as React from "react";

export interface TopicNodeProps {
  /** Topic title (Jakarta 800). */
  name: string;
  /** Phosphor icon name (duotone), e.g. "atom". */
  icon: string;
  /** Category color token — tints the icon chip. Discovery-tier color. */
  categoryColor: string;
  /** One-line topic summary. */
  description?: string;
  /** Position color tokens — the "debate signature" dots. */
  positionColors: string[];
  /** Link target. Omit + set `stub` for an in-progress placeholder. */
  href?: string;
  /** Render as a dashed in-progress stub (no dots, "In progress" badge). */
  stub?: boolean;
}

/**
 * TopicNode — the canonical topic card used across discovery tiers
 * (Home directory, Spotlight bench, Category grid, search rows).
 * Icon tinted by category; position colors preview the debate.
 */
export declare const TopicNode: React.FC<TopicNodeProps>;
```

### Implementation (`TopicNode.jsx`)

```jsx
const { useState } = React;

export function TopicNode({ name, icon, categoryColor = "var(--cat-energy)", description, positionColors = [], href, stub = false }) {
  const [hover, setHover] = useState(false);
  const tint = `color-mix(in srgb, ${categoryColor} 13%, #fff)`;
  return (
    <a
      href={href || undefined}
      onMouseEnter={() => setHover(true)}
      onMouseLeave={() => setHover(false)}
      style={{
        position: "relative", display: "flex", flexDirection: "column",
        background: stub ? "var(--ink-50)" : "#fff",
        border: `1px solid ${hover && !stub ? `color-mix(in srgb, ${categoryColor} 40%, var(--ink-100))` : "var(--ink-100)"}`,
        borderStyle: stub ? "dashed" : "solid",
        borderRadius: 18, padding: "22px 22px 20px", textDecoration: "none", color: "inherit",
        transform: hover && !stub ? "translateY(-3px)" : "none",
        boxShadow: hover && !stub ? "0 16px 32px -18px rgba(20,22,15,.22)" : "none",
        transition: "border-color .18s, transform .18s, box-shadow .18s",
      }}
    >
      <div style={{ display: "flex", alignItems: "center", gap: 13 }}>
        <span style={{ flex: "none", width: 52, height: 52, borderRadius: 14, background: stub ? "#fff" : tint, color: categoryColor, display: "flex", alignItems: "center", justifyContent: "center" }}>
          <i className={`ph-duotone ph-${icon}`} style={{ fontSize: 28 }} />
        </span>
        <span style={{ fontFamily: "var(--font-display)", fontWeight: 800, fontSize: 21, letterSpacing: "-.02em", lineHeight: 1.05, minWidth: 0, overflowWrap: "anywhere" }}>{name}</span>
      </div>
      {description && (
        <p style={{ margin: "15px 0 0", fontSize: 14, lineHeight: 1.5, color: "var(--ink-600)", textWrap: "pretty" }}>{description}</p>
      )}
      <div style={{ marginTop: "auto", paddingTop: 18, display: "flex", alignItems: "center", gap: 10 }}>
        {stub ? (
          <span style={{ fontSize: 11, fontWeight: 700, textTransform: "uppercase", letterSpacing: ".04em", color: "var(--ink-400)" }}>In progress</span>
        ) : (
          <>
            <span style={{ display: "flex", gap: 5 }}>
              {positionColors.map((c, i) => (
                <span key={i} style={{ width: 9, height: 9, borderRadius: 9999, background: c }} />
              ))}
            </span>
            <span style={{ fontSize: 12, color: "var(--ink-400)", fontWeight: 600 }}>{positionColors.length} positions</span>
            <span style={{ marginLeft: "auto", width: 30, height: 30, borderRadius: 9999, background: hover ? categoryColor : "var(--ink-50)", color: hover ? "#fff" : "var(--ink-400)", display: "flex", alignItems: "center", justifyContent: "center", transition: ".18s" }}>
              <i className="ph-duotone ph-arrow-right" style={{ fontSize: 15 }} />
            </span>
          </>
        )}
      </div>
    </a>
  );
}
```

---

## PositionCard

### Props (`PositionCard.d.ts`)

```ts
import * as React from "react";
import type { Position, Depth } from "./types";

export interface PositionCardProps {
  position: Position;
  /** How much to reveal. condensed = name + steelman only. Default "normal". */
  depth?: Depth;
  /** Reader's current stance; tints the agree/disagree control. */
  stance?: "agree" | "disagree" | null;
  onStanceChange?: (s: "agree" | "disagree" | null) => void;
  /** Click handler (e.g. open detail sheet on mobile). */
  onOpen?: () => void;
}

/**
 * PositionCard — the heart of a topic. Color rail + dot + Jakarta-800 name,
 * italic steelman (always shown), description + representative + proponents
 * revealed with depth, and the agree/disagree + importance signals.
 * Equal-weight by design: never larger or first-by-rank.
 */
export declare const PositionCard: React.FC<PositionCardProps>;
```

### Implementation (`PositionCard.jsx`)

```jsx
const { useState } = React;

export function PositionCard({ position, depth = "normal", stance = null, onStanceChange, onOpen }) {
  const [s, setS] = useState(stance);
  const c = position.color;
  const show = (min) => ({ condensed: 0, normal: 1, deep: 2 }[depth] >= min);
  const setStance = (v) => { const nv = s === v ? null : v; setS(nv); onStanceChange && onStanceChange(nv); };
  return (
    <div onClick={onOpen} style={{ position: "relative", background: "#fff", border: "1px solid var(--ink-100)", borderRadius: 16, padding: "20px 22px 18px 24px", overflow: "hidden", cursor: onOpen ? "pointer" : "default" }}>
      <span style={{ position: "absolute", left: 0, top: 0, bottom: 0, width: 5, background: c }} />
      <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
        <span style={{ width: 11, height: 11, borderRadius: 9999, background: c, flex: "none" }} />
        <span style={{ fontFamily: "var(--font-display)", fontWeight: 800, fontSize: 21, letterSpacing: "-.015em", lineHeight: 1 }}>{position.name}</span>
      </div>
      <p style={{ margin: "11px 0 0", fontSize: 15.5, fontStyle: "italic", fontWeight: 500, lineHeight: 1.45, color: "var(--ink-800)" }}>{position.steelman}</p>
      {show(1) && (
        <p style={{ margin: "12px 0 0", fontSize: 13.5, lineHeight: 1.6, color: "var(--ink-600)" }}>{position.description}</p>
      )}
      {show(2) && position.representative && (
        <div style={{ margin: "13px 0 0", display: "flex", alignItems: "center", gap: 9, padding: "9px 11px", background: "var(--ink-50)", borderRadius: 10 }}>
          <i className="ph-duotone ph-user-focus" style={{ color: "var(--green-700)", fontSize: 18 }} />
          <span style={{ fontSize: 12, color: "var(--ink-600)", lineHeight: 1.4 }}>
            <b style={{ color: "var(--ink-900)", fontWeight: 600 }}>{position.representative.name}</b> — {position.representative.note}
          </span>
        </div>
      )}
      {show(1) && position.proponents?.length > 0 && (
        <p style={{ margin: "12px 0 0", fontSize: 12, color: "var(--ink-400)", lineHeight: 1.45 }}>
          <b style={{ color: "var(--ink-600)", fontWeight: 600 }}>Proponents:</b> {position.proponents.join(" · ")}
        </p>
      )}
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", gap: 12, marginTop: 15, paddingTop: 13, borderTop: "1px solid var(--ink-100)" }}>
        <div style={{ display: "flex", gap: 7 }} onClick={(e) => e.stopPropagation()}>
          {["agree", "disagree"].map((v) => {
            const on = s === v;
            return (
              <button key={v} type="button" onClick={() => setStance(v)} style={{ all: "unset", cursor: "pointer", fontSize: 12, fontWeight: 600, padding: "6px 13px", borderRadius: 9999, border: `1px solid ${on ? c : "var(--ink-200)"}`, color: on ? c : "var(--ink-600)", background: on ? `color-mix(in srgb, ${c} 9%, #fff)` : "transparent", textTransform: "capitalize" }}>{v}</button>
            );
          })}
        </div>
        <span style={{ display: "inline-flex", alignItems: "center", gap: 4, fontSize: 11, color: "var(--ink-400)" }}>
          <i className="ph-duotone ph-caret-up" style={{ fontSize: 15, color: "var(--ink-300)" }} />
          <b style={{ color: "var(--ink-700)", fontVariantNumeric: "tabular-nums" }}>{position.importance}</b>
        </span>
      </div>
    </div>
  );
}
```

---

## QuestionCard

### Props (`QuestionCard.d.ts`)

```ts
import * as React from "react";
import type { Question } from "./types";

export interface QuestionCardProps {
  question: Question;
  /** "condensed" hides the "why contested" body. Default "normal". */
  depth?: "condensed" | "normal" | "deep";
  onVote?: (vote: "up" | "down" | null) => void;
}

/**
 * QuestionCard — one open question. Empirical/value tag drives the accent;
 * importance vote (which reorders the list in product); "why it's contested"
 * revealed at normal/deep.
 */
export declare const QuestionCard: React.FC<QuestionCardProps>;
```

### Implementation (`QuestionCard.jsx`)

```jsx
const { useState } = React;

export function QuestionCard({ question, depth = "normal", onVote }) {
  const [vote, setVote] = useState(null);
  const isEmp = question.kind === "empirical";
  const tagColor = isEmp ? "var(--pos-blue)" : "var(--pos-amber)";
  const n = question.votes + (vote === "up" ? 1 : 0) - (vote === "down" ? 1 : 0);
  const set = (v) => { const nv = vote === v ? null : v; setVote(nv); onVote && onVote(nv); };
  return (
    <div style={{ border: "1px solid var(--ink-100)", borderRadius: 13, padding: 16, background: "#fff" }}>
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 9 }}>
        <span style={{ display: "inline-flex", alignItems: "center", gap: 5, fontSize: 10, fontWeight: 700, textTransform: "uppercase", letterSpacing: ".05em", padding: "3px 9px", borderRadius: 9999, color: tagColor, background: `color-mix(in srgb, ${tagColor} 12%, #fff)` }}>
          <i className={isEmp ? "ph-duotone ph-flask" : "ph-duotone ph-heart"} style={{ fontSize: 12 }} />
          {isEmp ? "Empirical" : "Value"}
        </span>
        <span style={{ display: "inline-flex", alignItems: "center", gap: 6, border: "1px solid var(--ink-100)", borderRadius: 9999, padding: "3px 9px" }}>
          <button type="button" onClick={() => set("up")} style={{ all: "unset", cursor: "pointer", display: "flex" }}>
            <i className={vote === "up" ? "ph-fill ph-caret-up" : "ph-duotone ph-caret-up"} style={{ fontSize: 13, color: vote === "up" ? "var(--green-600)" : "var(--ink-300)" }} />
          </button>
          <span style={{ fontSize: 11, fontWeight: 700, color: "var(--ink-900)", fontVariantNumeric: "tabular-nums" }}>{n}</span>
          <button type="button" onClick={() => set("down")} style={{ all: "unset", cursor: "pointer", display: "flex" }}>
            <i className={vote === "down" ? "ph-fill ph-caret-down" : "ph-duotone ph-caret-down"} style={{ fontSize: 13, color: vote === "down" ? "var(--pos-rust)" : "var(--ink-300)" }} />
          </button>
        </span>
      </div>
      <div style={{ fontFamily: "var(--font-display)", fontWeight: 800, fontSize: 16, lineHeight: 1.3, letterSpacing: "-.01em", color: "var(--ink-900)" }}>{question.text}</div>
      {depth !== "condensed" && question.why && (
        <p style={{ margin: "9px 0 0", fontSize: 12.5, lineHeight: 1.5, color: "var(--ink-600)" }}>
          <b style={{ color: "var(--ink-900)", fontWeight: 600 }}>Why contested:</b> {question.why}
        </p>
      )}
    </div>
  );
}
```

---

## StatTile

### Props (`StatTile.d.ts`)

```ts
import * as React from "react";
import type { Stat } from "./types";

export interface StatTileProps {
  stat: Stat;
  /** "condensed" shows viz + value only; normal/deep add note + source. */
  depth?: "condensed" | "normal" | "deep";
}

/**
 * StatTile — one Basics figure. Implements the chart vocabulary: each fact's
 * shape maps to ONE fixed viz (ranked / radial / range / bar / sparkline).
 * Charts are ink + a single green; the subject is the only green element.
 */
export declare const StatTile: React.FC<StatTileProps>;
```

### Implementation (`StatTile.jsx`)

```jsx
function Ranked({ series = [] }) {
  const max = Math.max(...series.map((s) => s.value));
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 6 }}>
      {series.map((r, i) => (
        <div key={i} style={{ display: "grid", gridTemplateColumns: "64px 1fr 40px", alignItems: "center", gap: 8 }}>
          <span style={{ fontSize: 11, color: r.highlight ? "var(--ink-900)" : "var(--ink-500)", fontWeight: r.highlight ? 700 : 400 }}>{r.label}</span>
          <span style={{ height: 7, borderRadius: 9999, background: "var(--ink-100)", overflow: "hidden" }}>
            <span style={{ display: "block", height: "100%", borderRadius: 9999, width: `${Math.max(3, (r.value / max) * 100)}%`, background: r.highlight ? "var(--green-500)" : "var(--ink-300)" }} />
          </span>
          <span style={{ fontSize: 11, textAlign: "right", fontVariantNumeric: "tabular-nums", color: r.highlight ? "var(--green-700)" : "var(--ink-400)", fontWeight: r.highlight ? 700 : 400 }}>{r.value}</span>
        </div>
      ))}
    </div>
  );
}

function Bar({ value }) {
  const pct = parseFloat(value) || 0;
  return (
    <div style={{ height: 7, borderRadius: 9999, background: "var(--ink-100)", overflow: "hidden" }}>
      <span style={{ display: "block", height: "100%", borderRadius: 9999, width: `${Math.min(100, pct)}%`, background: "var(--green-500)" }} />
    </div>
  );
}

function Radial({ value }) {
  const pct = parseFloat(value) || 0;
  const r = 28, circ = 2 * Math.PI * r;
  return (
    <svg width="58" height="58" viewBox="0 0 72 72">
      <circle cx="36" cy="36" r={r} fill="none" stroke="var(--ink-100)" strokeWidth="9" />
      <circle cx="36" cy="36" r={r} fill="none" stroke="var(--green-500)" strokeWidth="9" strokeLinecap="round" strokeDasharray={`${(pct / 100) * circ} ${circ}`} transform="rotate(-90 36 36)" />
    </svg>
  );
}

function Range({ range }) {
  return (
    <div>
      <div style={{ position: "relative", height: 7, borderRadius: 9999, background: "linear-gradient(90deg, var(--green-tint-strong), var(--ink-100))" }}>
        <span style={{ position: "absolute", top: "50%", left: `${range.at}%`, width: 13, height: 13, borderRadius: 9999, background: "var(--green-500)", border: "2.5px solid #fff", transform: "translate(-50%,-50%)", boxShadow: "0 0 0 1px var(--green-600)" }} />
      </div>
      <div style={{ display: "flex", justifyContent: "space-between", fontSize: 9, color: "var(--ink-400)", marginTop: 5 }}>
        <span>{range.min}</span><span>{range.max}</span>
      </div>
    </div>
  );
}

function Sparkline({ series = [] }) {
  const vals = series.map((s) => s.value);
  const max = Math.max(...vals), min = Math.min(...vals);
  const pts = vals.map((v, i) => `${(i / (vals.length - 1)) * 72},${34 - ((v - min) / (max - min || 1)) * 28}`).join(" ");
  return (
    <svg width="74" height="40" viewBox="0 0 74 40" fill="none">
      <polyline points={pts} stroke="var(--green-500)" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
}

export function StatTile({ stat, depth = "normal" }) {
  const big = stat.viz === "bar" || stat.viz === "radial" || stat.viz === "range";
  return (
    <div style={{ border: "1px solid var(--ink-100)", borderRadius: 14, padding: "16px 16px 15px", display: "flex", flexDirection: "column", gap: 11, background: "#fff" }}>
      <div style={{ fontSize: 11, textTransform: "uppercase", letterSpacing: ".04em", color: "var(--ink-400)", lineHeight: 1.3 }}>{stat.label}</div>
      {big && stat.value && (
        <div style={{ fontFamily: "var(--font-display)", fontWeight: 800, fontSize: 34, fontVariantNumeric: "tabular-nums", letterSpacing: "-.03em", lineHeight: .95 }}>{stat.value}</div>
      )}
      <div style={{ marginTop: "auto" }}>
        {stat.viz === "ranked" && <Ranked series={stat.series} />}
        {stat.viz === "bar" && <Bar value={stat.value} />}
        {stat.viz === "radial" && <Radial value={stat.value} />}
        {stat.viz === "range" && <Range range={stat.range} />}
        {stat.viz === "sparkline" && <Sparkline series={stat.series} />}
      </div>
      {depth !== "condensed" && stat.note && (
        <div style={{ fontSize: 12, color: "var(--ink-600)", lineHeight: 1.45 }}>{stat.note}</div>
      )}
      {depth === "deep" && stat.source && (
        <div style={{ display: "inline-flex", alignItems: "center", gap: 4, fontSize: 11, color: "var(--ink-400)" }}>
          <i className="ph-duotone ph-link-simple" style={{ fontSize: 12 }} />{stat.source}
        </div>
      )}
    </div>
  );
}
```

---

## DepthToggle

### Props (`DepthToggle.d.ts`)

```ts
import * as React from "react";

export interface DepthToggleProps {
  /** Current depth. */
  value: "condensed" | "normal" | "deep";
  /** Called with the new depth on change. */
  onChange?: (depth: "condensed" | "normal" | "deep") => void;
  /** Short labels (Brief/Normal/Deep) vs. full. Default true. */
  compact?: boolean;
}

/**
 * DepthToggle — the reading-depth control. A visual segmented control whose
 * bar-height glyph signals increasing density. First-class, cross-cutting:
 * drives which content each section reveals.
 */
export declare const DepthToggle: React.FC<DepthToggleProps>;
```

### Implementation (`DepthToggle.jsx`)

```jsx
const DEPTHS = [
  { key: "condensed", label: "Brief", bars: 1 },
  { key: "normal", label: "Normal", bars: 2 },
  { key: "deep", label: "Deep", bars: 3 },
];

export function DepthToggle({ value = "normal", onChange, compact = true }) {
  return (
    <div style={{ display: "inline-flex", background: "#fff", border: "1px solid var(--ink-100)", borderRadius: 9999, padding: 3 }}>
      {DEPTHS.map((d) => {
        const on = d.key === value;
        return (
          <button
            key={d.key}
            type="button"
            onClick={() => onChange && onChange(d.key)}
            style={{
              all: "unset", cursor: "pointer", display: "flex", alignItems: "center", gap: 6,
              fontFamily: "var(--font-sans)", fontSize: 12, fontWeight: 600,
              color: on ? "#fff" : "var(--ink-500)", background: on ? "var(--ink-900)" : "transparent",
              padding: "6px 12px", borderRadius: 9999, transition: ".15s",
            }}
          >
            <span style={{ display: "flex", gap: 1.5, alignItems: "flex-end", height: 10 }}>
              {[4, 7, 10].map((h, i) => (
                <span key={i} style={{ width: 2.5, height: h, borderRadius: 1, background: on ? (i < d.bars ? "var(--green-500)" : "rgba(255,255,255,.3)") : (i < d.bars ? "var(--ink-400)" : "var(--ink-200)") }} />
              ))}
            </span>
            {compact ? d.label : `${d.label} reading`}
          </button>
        );
      })}
    </div>
  );
}
```

---

## VoteControl

### Props (`VoteControl.d.ts`)

```ts
import * as React from "react";

export interface VoteControlProps {
  /** Aggregate count shown between the carets. */
  count: number;
  /** Initial vote state. */
  value?: "up" | "down" | null;
  onChange?: (vote: "up" | "down" | null) => void;
  /** Horizontal pill vs. vertical stack. Default "pill". */
  layout?: "pill" | "stack";
}

/**
 * VoteControl — the importance signal used on Questions and Positions.
 * Aggregates a community count; in the product it surfaces salience but
 * never reorders curated content.
 */
export declare const VoteControl: React.FC<VoteControlProps>;
```

### Implementation (`VoteControl.jsx`)

```jsx
const { useState } = React;

export function VoteControl({ count = 0, value = null, onChange, layout = "pill" }) {
  const [vote, setVote] = useState(value);
  const n = count + (vote === "up" ? 1 : 0) - (vote === "down" ? 1 : 0);
  const set = (v) => { const nv = vote === v ? null : v; setVote(nv); onChange && onChange(nv); };
  const vertical = layout === "stack";
  return (
    <span style={{ display: "inline-flex", flexDirection: vertical ? "column" : "row", alignItems: "center", gap: vertical ? 3 : 6, border: "1px solid var(--ink-100)", borderRadius: 9999, padding: vertical ? "6px 5px" : "3px 9px", background: "#fff" }}>
      <button type="button" onClick={() => set("up")} style={{ all: "unset", cursor: "pointer", display: "flex" }}>
        <i className={vote === "up" ? "ph-fill ph-caret-up" : "ph-duotone ph-caret-up"} style={{ fontSize: 14, color: vote === "up" ? "var(--green-600)" : "var(--ink-300)" }} />
      </button>
      <span style={{ fontSize: 12, fontWeight: 700, color: "var(--ink-900)", fontVariantNumeric: "tabular-nums", minWidth: 18, textAlign: "center" }}>{n}</span>
      <button type="button" onClick={() => set("down")} style={{ all: "unset", cursor: "pointer", display: "flex" }}>
        <i className={vote === "down" ? "ph-fill ph-caret-down" : "ph-duotone ph-caret-down"} style={{ fontSize: 14, color: vote === "down" ? "var(--pos-rust)" : "var(--ink-300)" }} />
      </button>
    </span>
  );
}
```
