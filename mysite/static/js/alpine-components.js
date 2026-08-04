/**
 * Alpine.js CSP-compatible component registrations.
 *
 * The @alpinejs/csp build forbids inline expressions in directives.
 * All logic must live inside Alpine.data() methods; templates reference
 * property / method names only.
 *
 * Components:
 *   mobileNav       – hamburger menu with focus containment (base.html)
 *   desktopDropdown – keyboard and pointer-safe global dropdowns (base.html)
 *   mobileQuickActions – keeps fixed actions clear of the hero booking form
 *   faqItem         – single FAQ accordion item (all FAQ sections)
 *   serviceCarousel – ordered photo carousel controls and swipe handling
 *   readingProgress – article reading-progress indicator
 *   blogToc         – article table-of-contents current-section state
 *   backToTop       – article return-to-top control
 *   contactForm     – accessible contact-form validation state
 */
document.addEventListener("alpine:init", () => {
  /* ── Mobile Navigation ─────────────────────────── */
  Alpine.data("mobileNav", () => ({
    isOpen: false,

    toggle() {
      if (this.isOpen) {
        this.close();
        return;
      }
      this.isOpen = true;
      document.body.classList.add("nav-open");
      this.$nextTick(() => {
        const items = this._focusableItems();
        if (items.length) {
          items[0].focus();
        } else if (this.$refs.mobileMenu) {
          this.$refs.mobileMenu.focus();
        }
      });
    },

    close() {
      this.isOpen = false;
      document.body.classList.remove("nav-open");
    },

    closeOnEscape(event) {
      if (!this.isOpen || !event || event.key !== "Escape") return;
      event.preventDefault();
      this.close();
      if (this.$refs.mobileToggle) this.$refs.mobileToggle.focus();
    },

    trapFocus(event) {
      if (!this.isOpen || !event || event.key !== "Tab") return;
      const items = this._focusableItems();
      if (!items.length) return;
      const first = items[0];
      const last = items[items.length - 1];
      if (event.shiftKey && event.target === first) {
        event.preventDefault();
        last.focus();
      } else if (!event.shiftKey && event.target === last) {
        event.preventDefault();
        first.focus();
      }
    },

    _focusableItems() {
      if (!this.$refs.mobileMenu) return [];
      return Array.from(
        this.$refs.mobileMenu.querySelectorAll(
          'a[href], button:not([disabled]), summary, [tabindex]:not([tabindex="-1"])',
        ),
      );
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

  /* ── Desktop Navigation Dropdown ───────────────── */
  Alpine.data("desktopDropdown", () => ({
    isOpen: false,

    toggle() {
      this.isOpen = !this.isOpen;
    },

    openFromPointer() {
      this.isOpen = true;
    },

    closeFromPointer() {
      this.isOpen = false;
    },

    openFromKeyboard(event) {
      if (!event || (event.key !== "Enter" && event.key !== " ")) return;
      event.preventDefault();
      this.isOpen = true;
      this.$nextTick(() => {
        const first = this.$refs.menu
          ? this.$refs.menu.querySelector('[role="menuitem"]')
          : null;
        if (first) first.focus();
      });
    },

    close() {
      this.isOpen = false;
    },

    closeOnEscape(event) {
      if (!this.isOpen || !event || event.key !== "Escape") return;
      event.preventDefault();
      this.close();
      if (this.$refs.trigger) this.$refs.trigger.focus();
    },

    get expandedStr() {
      return String(this.isOpen);
    },
  }));

  /* ── Mobile Quick Actions ──────────────────────── */
  Alpine.data("mobileQuickActions", () => ({
    isVisible: false,
    _observer: null,

    init() {
      const path = window.location?.pathname || "";
      const isContactPage =
        document.body?.classList?.contains("page-contact") ||
        /(^|\/)contact\/?$/.test(path);
      if (isContactPage) {
        this.isVisible = false;
        return;
      }
      const heroBooking = document.querySelector(".booking-widget");
      if (!heroBooking) {
        this.isVisible = true;
        return;
      }

      if (typeof window.IntersectionObserver !== "function") {
        return;
      }

      this._observer = new window.IntersectionObserver(
        (entries) => {
          this.isVisible = !entries.some((entry) => entry.isIntersecting);
        },
        { threshold: 0 },
      );
      this._observer.observe(heroBooking);
    },

    destroy() {
      if (this._observer) this._observer.disconnect();
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

  /* ── Service Photo Carousel ─────────────────────── */
  Alpine.data("serviceCarousel", () => ({
    index: 0,
    count: 0,
    _items: [],
    _pointerStartX: null,
    _suppressScroll: false,
    _scrollTimer: null,

    init() {
      const track = this.$refs.track;
      this._items = track
        ? Array.from(track.querySelectorAll("[data-service-photo-carousel-item]"))
        : [];
      this.count = this._items.length;
      this.index = 0;
    },

    previous() {
      this._goTo(this.index - 1);
    },

    next() {
      this._goTo(this.index + 1);
    },

    onKeydown(event) {
      if (!event) return;
      const actions = {
        ArrowLeft: () => this.previous(),
        ArrowRight: () => this.next(),
        Home: () => this._goTo(0),
        End: () => this._goTo(this.count - 1),
      };
      if (!actions[event.key]) return;
      event.preventDefault();
      actions[event.key]();
    },

    pointerDown(event) {
      this._pointerStartX = event && Number.isFinite(event.clientX)
        ? event.clientX
        : null;
    },

    pointerUp(event) {
      if (
        this._pointerStartX === null ||
        !event ||
        !Number.isFinite(event.clientX)
      ) {
        this._pointerStartX = null;
        return;
      }
      const distance = this._pointerStartX - event.clientX;
      this._pointerStartX = null;
      if (Math.abs(distance) < 40) return;
      if (distance > 0) this.next();
      else this.previous();
    },

    onScroll() {
      const track = this.$refs.track;
      if (!track || !this._items.length || this._suppressScroll) return;
      const maxScroll = (track.scrollWidth || 0) - (track.clientWidth || 0);
      if (maxScroll > 0) {
        const fraction = Math.max(0, Math.min(1, (track.scrollLeft || 0) / maxScroll));
        this.index = Math.round(fraction * (this.count - 1));
        return;
      }
      let closestIndex = 0;
      let closestDistance = Number.POSITIVE_INFINITY;
      this._items.forEach((item, itemIndex) => {
        const distance = Math.abs((item.offsetLeft || 0) - (track.scrollLeft || 0));
        if (distance < closestDistance) {
          closestIndex = itemIndex;
          closestDistance = distance;
        }
      });
      this.index = closestIndex;
    },

    _goTo(nextIndex) {
      if (!this.count) return;
      const bounded = Math.max(0, Math.min(nextIndex, this.count - 1));
      this.index = bounded;
      this._suppressScroll = true;
      if (this._scrollTimer) clearTimeout(this._scrollTimer);
      this._scrollTimer = setTimeout(() => {
        this._suppressScroll = false;
      }, 650);
      const item = this._items[bounded];
      if (!item || typeof item.scrollIntoView !== "function") return;
      const reducedMotion =
        typeof window.matchMedia === "function" &&
        window.matchMedia("(prefers-reduced-motion: reduce)").matches;
      item.scrollIntoView({
        behavior: reducedMotion ? "auto" : "smooth",
        block: "nearest",
        inline: "start",
      });
    },

    get atStart() {
      return this.index <= 0;
    },

    get atEnd() {
      return !this.count || this.index >= this.count - 1;
    },

    get statusText() {
      return this.count ? `Image ${this.index + 1} of ${this.count}` : "";
    },
  }));

  /* ── Blog Reading Progress ──────────────────────── */
  Alpine.data("readingProgress", () => ({
    progress: 0,

    init() {
      this.onScroll();
    },

    onScroll() {
      const article = document.querySelector("[data-blog-article]");
      if (!article) {
        this.progress = 0;
        return;
      }
      const rect = article.getBoundingClientRect();
      const articleTop = window.scrollY + rect.top;
      const root = document.documentElement;
      const pageScrollable = root
        ? Math.max(0, root.scrollHeight - window.innerHeight)
        : 0;
      const articleScrollable = Math.max(0, article.offsetHeight - window.innerHeight);
      const articleEnd = articleTop + articleScrollable;
      const documentEnd = pageScrollable || articleEnd;
      const hasReachableArticleRange =
        articleScrollable > 0 && articleTop < documentEnd;
      const scrollStart = hasReachableArticleRange ? articleTop : 0;
      const scrollEnd = hasReachableArticleRange
        ? Math.min(documentEnd, articleEnd)
        : documentEnd;
      const scrollable = Math.max(0, scrollEnd - scrollStart);
      const rawProgress = scrollable
        ? ((window.scrollY - scrollStart) / scrollable) * 100
        : 0;
      this.progress = Number.isFinite(rawProgress)
        ? Math.max(0, Math.min(100, rawProgress))
        : 0;
    },

    get barStyle() {
      return `width:${this.progress.toFixed(2)}%;`;
    },
  }));

  /* ── Blog Table of Contents ─────────────────────── */
  Alpine.data("blogToc", () => ({
    activeIndex: 0,
    _links: [],
    _observer: null,

    init() {
      this._links = Array.from(this.$el.querySelectorAll("[data-toc-index]"));
      const targets = this._links
        .map((link) => {
          const hash = (link.getAttribute("href") || "").replace(/^#/, "");
          return hash ? document.getElementById(hash) : null;
        })
        .filter(Boolean);
      this._setActive(0);
      if (!targets.length || typeof window.IntersectionObserver !== "function") return;
      this._observer = new window.IntersectionObserver(
        (entries) => {
          const visible = entries.find((entry) => entry.isIntersecting);
          if (!visible) return;
          const nextIndex = targets.indexOf(visible.target);
          if (nextIndex >= 0) this._setActive(nextIndex);
        },
        { rootMargin: "-20% 0px -65% 0px", threshold: 0 },
      );
      targets.forEach((target) => this._observer.observe(target));
    },

    destroy() {
      if (this._observer) this._observer.disconnect();
    },

    _setActive(index) {
      this.activeIndex = index;
      this._links.forEach((link, linkIndex) => {
        const active = linkIndex === index;
        link.classList.toggle("toc-link-active", active);
        link.classList.toggle("toc-link-inactive", !active);
        if (active) link.setAttribute("aria-current", "location");
        else link.removeAttribute("aria-current");
      });
    },
  }));

  /* ── Blog Back-to-Top ───────────────────────────── */
  Alpine.data("backToTop", () => ({
    visible: false,

    init() {
      this.onScroll();
    },

    onScroll() {
      this.visible = window.scrollY > 640;
    },

    scrollUp() {
      const reducedMotion =
        typeof window.matchMedia === "function" &&
        window.matchMedia("(prefers-reduced-motion: reduce)").matches;
      window.scrollTo({ top: 0, behavior: reducedMotion ? "auto" : "smooth" });
    },
  }));

  /* ── Contact Form Validation ────────────────────── */
  Alpine.data("contactForm", () => ({
    onSubmit(event) {
      if (!event) return;
      const form = event.currentTarget || this.$el;
      if (!form || typeof form.checkValidity !== "function" || form.checkValidity()) return;
      event.preventDefault();
      const invalid = form.querySelector(":invalid");
      if (!invalid) return;
      invalid.setAttribute("aria-invalid", "true");
      if (typeof invalid.focus === "function") invalid.focus();
      if (typeof form.reportValidity === "function") form.reportValidity();
    },

    onInvalid(event) {
      if (event && event.target) event.target.setAttribute("aria-invalid", "true");
    },

    onInput(event) {
      const field = event && event.target;
      if (field && field.validity && field.validity.valid) {
        field.removeAttribute("aria-invalid");
      }
    },
  }));
});
