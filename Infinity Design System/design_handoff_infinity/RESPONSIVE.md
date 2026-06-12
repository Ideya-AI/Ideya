# Responsive intent

How each surface adapts across breakpoints. The Topic page has full desktop +
mobile designs; the others are specified here so engineering doesn't guess.

**Breakpoints:** `mobile` < 640 · `tablet` 640–1024 · `desktop` > 1024.
Design widths in the mocks: desktop 1180 content max; mobile 390.

---

## Cross-cutting rules
- **Single column under 640.** Every multi-column grid collapses to one column.
- **Sticky chrome stays sticky;** side rails (section nav) become a **horizontal
  scroller** pinned under the nav (see the mobile Topic page).
- **Reading-depth control** moves from the left rail into the sticky controls bar;
  stays a segmented pill.
- **Hover-only affordances** (node arrows, row arrows) render always-on at touch sizes.
- **Hit targets ≥ 44px** on touch.
- **Modals → bottom sheets** under 640 (the Submit flow and position detail both).

---

## Home  *(desktop built; mobile spec below)*
- **Nav** — logo + search + menu; under 640 the search collapses to an icon that
  opens a full-width search overlay.
- **Spotlight** — the light/dark hero **stacks**: "what it is" panel on top, the dark
  "the debate" panel below it. The 3-card bench becomes a **horizontal snap-scroller**.
- **Purpose** — `What / Why / How` 3-up grid → single column; the rotating indicator
  becomes a real swipe carousel.
- **Directory** — the 3-column masonry → **one column**; categories become collapsible
  accordions (collapsed by default past the first two) so the page isn't a giant list.

## Category page  *(desktop built)*
- Section rail → horizontal scroller under nav.
- **Meta-Basics** 4-up → 2-up on tablet, 1-up on mobile.
- **Topics grid** 3-col → 2-col tablet → 1-col mobile. "Show more" stays.

## Search  *(desktop built)*
- The dropdown is already near-full-width; on mobile it becomes a **full-screen
  search view** (input pinned top, results fill the screen, "cancel" returns).
- Result rows keep the icon + name + meta; debate dots may hide under 360px.

## Submit your view  *(desktop built)*
- The centered modal becomes a **bottom sheet** that can expand to full height.
- Stepper, position options, stance/importance, and identity all stack naturally —
  they're already single-column inside the modal. Footer (Back / Continue) pins to
  the bottom of the sheet.

---

## Topic page  *(both built — reference implementation)*
- **Desktop:** `Desktop Topic - Nuclear Energy.html` — left section rail + depth toggle,
  side-by-side section layouts.
- **Mobile:** `Mobile Topic - Nuclear Energy.html` — stacked accordions, sticky
  section-jump scroller, compact depth control, **bottom-sheet** position detail.
  This pair is the canonical model for how every other surface should reflow.
