/* Ideya — Alpine stores + small helpers.
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

    // Vote follow-up modal open state (opened by the "follow-up" event the
    // vote response triggers; its body arrives out of band — see _follow_modal).
    Alpine.store("follow", { open: false });

    // Row-synced expandable grid (positions, basics) — expansion state lives
    // on the grid (keyed by data-xid) so a click opens/closes every card
    // sharing the visual row: the CSS grid stretches row partners anyway, and
    // a stretched-but-empty card reads as a bug. Rows are detected by
    // offsetTop at click time, which stays correct across responsive column
    // counts, wide tiles, and dense grid packing.
    Alpine.data("rowGrid", function () {
      return {
        open: {},
        toggle(card) {
          var next = !this.open[card.dataset.xid];
          var row = Array.prototype.filter.call(
            card.parentElement.querySelectorAll("[data-xid]"),
            function (c) {
              return c.offsetParent !== null && c.offsetTop === card.offsetTop;
            },
          );
          var self = this;
          row.forEach(function (c) {
            self.open[c.dataset.xid] = next;
          });
          if (!next) window.anchorCollapse(card);
        },
      };
    });

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

  // After collapsing a tall box the reader who clicked at its bottom would be
  // left far below where they started: the page reflows but the viewport
  // doesn't. If the collapsed element's top ended up above the viewport,
  // scroll it back to just under the sticky header. setTimeout(0) runs after
  // Alpine's microtask flush (post-collapse layout); the fresh measurement
  // absorbs whatever Chrome's native scroll anchoring already compensated,
  // and "instant" (not the page's smooth default) keeps the correction
  // imperceptible.
  window.anchorCollapse = function (el) {
    setTimeout(function () {
      var top = el.getBoundingClientRect().top;
      if (top < 84) window.scrollBy({ top: top - 84, behavior: "instant" });
    }, 0);
  };

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
