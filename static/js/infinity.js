/* Infinity — Alpine stores + small helpers.
   Loaded (deferred) BEFORE Alpine so alpine:init listeners are registered. */
(function () {
  document.addEventListener("alpine:init", function () {
    // Reading depth — persisted, drives every section's reveal via body[data-depth].
    Alpine.store("ui", {
      depth: localStorage.getItem("infinity:depth") || "normal",
      setDepth(d) {
        this.depth = d;
        localStorage.setItem("infinity:depth", d);
      },
    });

    // Global search overlay open/close state (the dropdown lives in _search.html).
    Alpine.store("search", {
      open: false,
      toggle() {
        this.open = !this.open;
      },
    });

    // Submit-your-view modal open state.
    Alpine.store("submit", { open: false });

    // The 3-step submit flow: align → stance/importance/reasoning → identity.
    Alpine.data("submitFlow", () => ({
      step: 1,
      position: "",
      stance: "",
      importance: 3,
      reasoning: "",
      email: "",
      anon: true,
      launch() {
        this.reset();
        Alpine.store("submit").open = true;
      },
      reset() {
        this.step = 1;
        this.position = "";
        this.stance = "";
        this.importance = 3;
        this.reasoning = "";
        this.email = "";
        this.anon = true;
      },
      get canContinue() {
        if (this.step === 1) return !!this.position;
        if (this.step === 2) return !!this.stance;
        return true;
      },
      next() {
        if (this.canContinue && this.step < 3) this.step++;
      },
      back() {
        if (this.step > 1) this.step--;
      },
    }));
  });

  // Keyboard: "/" focuses search, Esc closes overlays. Registered once.
  document.addEventListener("keydown", function (e) {
    if (
      e.key === "/" &&
      !/^(INPUT|TEXTAREA)$/.test(document.activeElement.tagName)
    ) {
      e.preventDefault();
      if (window.Alpine) Alpine.store("search").open = true;
    }
  });
})();
