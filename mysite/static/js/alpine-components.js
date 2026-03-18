/**
 * Alpine.js CSP-compatible component registrations.
 *
 * The @alpinejs/csp build forbids inline expressions in directives.
 * All logic must live inside Alpine.data() methods; templates reference
 * property / method names only.
 *
 * Components:
 *   mobileNav     – hamburger menu toggle (base.html)
 *   faqItem       – single FAQ accordion item (all FAQ sections)
 */
document.addEventListener("alpine:init", () => {
  /* ── Mobile Navigation ─────────────────────────── */
  Alpine.data("mobileNav", () => ({
    isOpen: false,

    toggle() {
      this.isOpen = !this.isOpen;
    },

    close() {
      this.isOpen = false;
    },

    /** Computed: true when menu is closed (for hamburger icon). */
    get notOpen() {
      return !this.isOpen;
    },

    /** Computed: "true"/"false" string for aria-expanded. */
    get expandedStr() {
      return String(this.isOpen);
    },
  }));

  /* ── FAQ Accordion Item ────────────────────────── */
  /*
   * Each FAQ item is its own x-data="faqItem" with a data-faq-section
   * attribute on the wrapper.  Items in the same section coordinate
   * via a custom 'faq-close' event dispatched on window so that only
   * one answer is open at a time per section.
   *
   * Template contract:
   *   <div x-data="faqItem"
   *        data-faq-section="unique-section-id"
   *        data-faq-index="0"
   *        @faq-close.window="onClose">
   *       <button @click="toggle" :aria-expanded="expandedStr">
   *           Question
   *           <span x-show="open"  aria-hidden="true">−</span>
   *           <span x-show="notOpen" aria-hidden="true">+</span>
   *       </button>
   *       <div x-show="open" x-collapse>Answer</div>
   *   </div>
   */
  Alpine.data("faqItem", () => ({
    open: false,
    _section: "",
    _index: -1,

    init() {
      this._section = this.$el.dataset.faqSection || "default";
      this._index = parseInt(this.$el.dataset.faqIndex, 10);
    },

    toggle() {
      if (this.open) {
        this.open = false;
      } else {
        // Close every other item in the same section
        this.$dispatch("faq-close", {
          section: this._section,
          except: this._index,
        });
        this.open = true;
      }
    },

    /** Listener for the coordination event. */
    onClose(e) {
      if (
        e.detail &&
        e.detail.section === this._section &&
        e.detail.except !== this._index
      ) {
        this.open = false;
      }
    },

    /** Computed: inverse of open (for the "+" icon). */
    get notOpen() {
      return !this.open;
    },

    /** Computed: "true"/"false" string for aria-expanded. */
    get expandedStr() {
      return String(this.open);
    },
  }));
});
