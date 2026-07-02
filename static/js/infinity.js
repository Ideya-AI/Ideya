/* Infinity — Alpine stores + small helpers.
   Loaded (deferred) BEFORE Alpine so alpine:init listeners are registered. */
(function () {
  document.addEventListener("alpine:init", function () {
    // Global search overlay open/close state (the dropdown lives in _search.html).
    Alpine.store("search", { open: false });

    // Global nav menu — desktop dropdown / mobile sheet (lives in _menu.html).
    Alpine.store("menu", {
      open: false,
      toggle() {
        this.open = !this.open;
      },
    });

    // "Add your view" input modal open state.
    Alpine.store("input", { open: false });

    // Transient confirmation toast — flash(msg) shows it briefly, then auto-hides.
    Alpine.store("toast", {
      show: false,
      msg: "",
      _t: null,
      flash(msg) {
        this.msg = msg;
        this.show = true;
        clearTimeout(this._t);
        this._t = setTimeout(() => {
          this.show = false;
        }, 2400);
      },
    });
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
