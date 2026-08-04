/**
 * ZIP Code Service Area Checker (Dark Theme)
 *
 * Intercepts all booking links and forms ([data-booking]) to validate
 * the user's ZIP code against the service area before redirecting to
 * the booking site. Pre-fills the ZIP on the booking site via ?zip= param.
 *
 * Two modes:
 *   1. Hero form (has zip input) — inline validation, blocks submit if invalid
 *   2. All other booking links — shows a modal to collect & validate zip
 */
(function () {
  "use strict";

  // Compatibility fallback for pages rendered without the target coverage payload.
  // Normal operation reads target-owned ZIP codes from base.html.
  var LEGACY_ZIP_CODES = [
    "91706",
    "92316",
    "92821",
    "91708",
    "91710",
    "91709",
    "91714",
    "91715",
    "91716",
    "91744",
    "91746",
    "91749",
    "91711",
    "92324",
    "92877",
    "92878",
    "92879",
    "92881",
    "92882",
    "92883",
    "91722",
    "91723",
    "91724",
    "91765",
    "92880",
    "91732",
    "92331",
    "92334",
    "92335",
    "92336",
    "92337",
    "91740",
    "91741",
    "92313",
    "91745",
    "92346",
    "92548",
    "91752",
    "92509",
    "92519",
    "91750",
    "92530",
    "92531",
    "92532",
    "92318",
    "92350",
    "92354",
    "92357",
    "92584",
    "92585",
    "92586",
    "91763",
    "92551",
    "92552",
    "92553",
    "92554",
    "92555",
    "92556",
    "92557",
    "92562",
    "92563",
    "92564",
    "92860",
    "91743",
    "91758",
    "91761",
    "91762",
    "91764",
    "92570",
    "92571",
    "92572",
    "91766",
    "91767",
    "91768",
    "91769",
    "91701",
    "91730",
    "91739",
    "92373",
    "92374",
    "92375",
    "92377",
    "92501",
    "92502",
    "92503",
    "92504",
    "92505",
    "92506",
    "92507",
    "92508",
    "92513",
    "92514",
    "92515",
    "92516",
    "92517",
    "91748",
    "92401",
    "92402",
    "92403",
    "92404",
    "92405",
    "92406",
    "92407",
    "92408",
    "92409",
    "92410",
    "92411",
    "92412",
    "92413",
    "92423",
    "92427",
    "91773",
    "92589",
    "92590",
    "92591",
    "92592",
    "92593",
    "91784",
    "91785",
    "91786",
    "91788",
    "91789",
    "91790",
    "91791",
    "91792",
    "91793",
    "92595",
    "92885",
    "92886",
    "92887",
    "92223",
    "92587",
  ];

  function readServiceZipCodes(doc) {
    var element = doc && doc.getElementById
      ? doc.getElementById("service-zip-codes")
      : null;
    if (!element) return LEGACY_ZIP_CODES.slice();
    try {
      var parsed = JSON.parse(element.textContent || "[]");
      if (!Array.isArray(parsed)) return LEGACY_ZIP_CODES.slice();
      var seen = {};
      return parsed
        .map(function (value) {
          return String(value || "").trim();
        })
        .filter(function (value) {
          if (!/^\d{5}$/.test(value) || seen[value]) return false;
          seen[value] = true;
          return true;
        });
    } catch (error) {
      return LEGACY_ZIP_CODES.slice();
    }
  }

  function isValidZip(zip, zipCodes) {
    var coverage = zipCodes || ZIP_CODES;
    return /^\d{5}$/.test(zip) && coverage.indexOf(zip) !== -1;
  }

  function buildBookingUrl(bookingUrl, zip, fields) {
    var url = new URL(bookingUrl, window.location.href);
    url.searchParams.set("zip", zip);
    var values = fields || {};
    Object.keys(values).forEach(function (key) {
      if (values[key] !== null && values[key] !== undefined && values[key] !== "") {
        url.searchParams.set(key, String(values[key]));
      }
    });
    return url.toString();
  }

  var ZIP_CODES = readServiceZipCodes(document);

  if (typeof module !== "undefined" && module.exports) {
    module.exports = {
      readServiceZipCodes: readServiceZipCodes,
      isValidZip: isValidZip,
      buildBookingUrl: buildBookingUrl,
    };
  }

  // ─── Modal HTML (injected once) ──────────────────────────────────
  var MODAL_ID = "zip-check-modal";

  // Read translations injected by Django template (falls back to English)
  var i18n = window.__ZIP_CHECK_I18N || {};
  var t = function (key, fallback) {
    return i18n[key] || fallback;
  };

  function getOrCreateModal() {
    var existing = document.getElementById(MODAL_ID);
    if (existing) return existing;

    var overlay = document.createElement("div");
    overlay.id = MODAL_ID;
    overlay.setAttribute("role", "dialog");
    overlay.setAttribute("aria-modal", "true");
    overlay.setAttribute(
      "aria-label",
      t("checkAvailability", "Check service availability"),
    );
    overlay.style.cssText =
      "display:none;position:fixed;inset:0;z-index:9999;" +
      "background:rgba(0,0,0,0.7);backdrop-filter:blur(8px);" +
      "align-items:center;justify-content:center;padding:1rem;";

    overlay.innerHTML =
      '<div style="background:#25262C;border:1px solid rgba(255,255,255,0.1);border-radius:24px;max-width:420px;width:90%;padding:3rem;box-shadow:0 25px 50px rgba(0,0,0,0.5);position:relative;animation:zipModalIn 400ms cubic-bezier(0.34,1.56,0.64,1)">' +
      '<button type="button" id="zip-modal-close" aria-label="' +
      t("close", "Close") +
      '" ' +
      'style="position:absolute;top:0.75rem;right:0.75rem;width:44px;height:44px;' +
      "border:none;background:transparent;cursor:pointer;font-size:1.25rem;" +
      'color:#A0A0A5;display:flex;align-items:center;justify-content:center;border-radius:8px"' +
      " onmouseover=\"this.style.background='rgba(255,255,255,0.05)'\" onmouseout=\"this.style.background='transparent'\">&times;</button>" +
      '<div style="text-align:center;margin-bottom:1.5rem">' +
      '<div style="width:48px;height:48px;background:rgba(255,213,4,0.1);border-radius:50%;display:flex;align-items:center;justify-content:center;margin:0 auto 1rem;color:#FFD504;font-size:1.25rem" aria-hidden="true">' +
      '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>' +
      "</div>" +
      '<h2 style="font-family:Montserrat,sans-serif;font-size:1.25rem;font-weight:800;color:#fff;margin:0 0 0.25rem;text-transform:uppercase;letter-spacing:-0.02em">' +
      t("checkArea", "Check Your Area") +
      "</h2>" +
      '<p style="font-size:0.875rem;color:#A0A0A5;margin:0">' +
      t("checkAreaDesc", "Enter your ZIP code to verify we service your area") +
      "</p>" +
      "</div>" +
      '<div style="margin-bottom:1rem">' +
      '<label for="zip-modal-input" class="sr-only">' +
      t("zipCode", "ZIP Code") +
      "</label>" +
      '<input type="text" id="zip-modal-input" maxlength="5" inputmode="numeric" aria-describedby="zip-modal-helper" aria-invalid="false" placeholder="' +
      t("enterZip", "Enter ZIP code") +
      '" ' +
      'style="width:100%;box-sizing:border-box;padding:0.875rem 1rem;border:1px solid rgba(255,255,255,0.1);border-radius:8px;' +
      "background:rgba(255,255,255,0.05);font-size:1.125rem;font-weight:600;text-align:center;letter-spacing:0.15em;" +
      'color:#fff;outline:none;transition:border-color 300ms,box-shadow 300ms" />' +
      '<p id="zip-modal-helper" role="status" aria-live="polite" aria-atomic="true" style="margin:0.5rem 0 0;font-size:0.8125rem;text-align:center;min-height:1.25rem;transition:color 150ms;color:#A0A0A5"></p>' +
      "</div>" +
      '<button type="button" id="zip-modal-submit" disabled ' +
      'style="width:100%;padding:0.875rem;border:none;border-radius:50px;' +
      "font-family:Montserrat,sans-serif;font-size:0.9375rem;font-weight:700;color:#121212;cursor:pointer;" +
      'background:#fff;opacity:0.5;transition:opacity 150ms,transform 100ms;text-transform:uppercase;letter-spacing:0.05em">' +
      t("continueBooking", "Continue to Booking") +
      "</button>" +
      "</div>";

    // Keyframe animation
    var style = document.createElement("style");
    style.textContent =
      "@keyframes zipModalIn{from{opacity:0;transform:scale(0.8)}to{opacity:1;transform:scale(1)}}";
    document.head.appendChild(style);

    document.body.appendChild(overlay);
    return overlay;
  }

  // ─── Modal Logic ─────────────────────────────────────────────────
  var pendingBookingUrl = null;
  var lastTrigger = null;

  function openModal(bookingUrl, trigger) {
    pendingBookingUrl = bookingUrl;
    lastTrigger = trigger || document.activeElement;
    var modal = getOrCreateModal();
    var input = document.getElementById("zip-modal-input");
    var helper = document.getElementById("zip-modal-helper");
    var submitBtn = document.getElementById("zip-modal-submit");

    // Reset state
    input.value = "";
    input.style.borderColor = "rgba(255,255,255,0.1)";
    input.style.boxShadow = "none";
    input.setAttribute("aria-invalid", "false");
    helper.textContent = "";
    helper.style.color = "#A0A0A5";
    submitBtn.disabled = true;
    submitBtn.style.opacity = "0.5";
    submitBtn.style.background = "#fff";

    modal.style.display = "flex";
    document.body.style.overflow = "hidden";
    if (typeof window.inlandTrack === "function") {
      window.inlandTrack("zip_modal_open", { source: "booking_link" });
    }

    // Focus the input after animation
    setTimeout(function () {
      input.focus();
    }, 100);
  }

  function closeModal() {
    var modal = document.getElementById(MODAL_ID);
    if (modal) {
      modal.style.display = "none";
      document.body.style.overflow = "";
    }
    pendingBookingUrl = null;
    if (lastTrigger && typeof lastTrigger.focus === "function") {
      lastTrigger.focus();
    }
    lastTrigger = null;
  }

  function navigateToBooking(zip) {
    if (!pendingBookingUrl) return;
    var url = buildBookingUrl(pendingBookingUrl, zip);
    if (typeof window.inlandTrack === "function") {
      window.inlandTrack("zip_check", { in_service_area: true });
    }
    window.open(url, "_blank", "noopener,noreferrer");
    closeModal();
  }

  // ─── Wire up modal events (once DOM is ready) ───────────────────
  function initModal() {
    var modal = getOrCreateModal();
    var input = document.getElementById("zip-modal-input");
    var helper = document.getElementById("zip-modal-helper");
    var submitBtn = document.getElementById("zip-modal-submit");
    var closeBtn = document.getElementById("zip-modal-close");

    // Close on overlay click
    modal.addEventListener("click", function (e) {
      if (e.target === modal) closeModal();
    });

    // Close button
    closeBtn.addEventListener("click", closeModal);

    // Escape key
    document.addEventListener("keydown", function (e) {
      if (modal.style.display !== "flex") return;
      if (e.key === "Escape") {
        e.preventDefault();
        closeModal();
        return;
      }
      if (e.key !== "Tab") return;
      var focusable = modal.querySelectorAll(
        'button:not([disabled]), input:not([disabled]), a[href], [tabindex]:not([tabindex="-1"])',
      );
      if (!focusable.length) return;
      var first = focusable[0];
      var last = focusable[focusable.length - 1];
      if (e.shiftKey && document.activeElement === first) {
        e.preventDefault();
        last.focus();
      } else if (!e.shiftKey && document.activeElement === last) {
        e.preventDefault();
        first.focus();
      }
    });

    // Input: strip non-digits, validate at 5 chars
    input.addEventListener("input", function () {
      var val = input.value.replace(/\D/g, "").slice(0, 5);
      input.value = val;

      if (val.length < 5) {
        input.style.borderColor = "rgba(255,255,255,0.1)";
        input.style.boxShadow = "none";
        var remaining = 5 - val.length;
        helper.textContent =
          val.length > 0
            ? remaining +
              " " +
              (remaining !== 1
                ? t("moreDigits", "more digits")
                : t("moreDigit", "more digit"))
            : "";
        helper.style.color = "#A0A0A5";
        submitBtn.disabled = true;
        submitBtn.style.opacity = "0.5";
        submitBtn.style.background = "#fff";
        input.setAttribute("aria-invalid", "false");
        return;
      }

      if (isValidZip(val)) {
        input.style.borderColor = "#22c55e";
        input.style.boxShadow = "0 0 0 1px #22c55e";
        helper.textContent = t("weServiceArea", "We service your area!");
        helper.style.color = "#22c55e";
        submitBtn.disabled = false;
        submitBtn.style.opacity = "1";
        submitBtn.style.background = "#FFD504";
        input.setAttribute("aria-invalid", "false");
      } else {
        input.style.borderColor = "#f87171";
        input.style.boxShadow = "0 0 0 1px #f87171";
        helper.textContent = t(
          "noServiceArea",
          "Sorry, we don't service this area yet",
        );
        helper.style.color = "#f87171";
        submitBtn.disabled = true;
        submitBtn.style.opacity = "0.5";
        submitBtn.style.background = "#fff";
        input.setAttribute("aria-invalid", "true");
        if (typeof window.inlandTrack === "function") {
          window.inlandTrack("zip_check", { in_service_area: false });
        }
      }
    });

    // Enter key submits if valid
    input.addEventListener("keydown", function (e) {
      if (e.key === "Enter" && !submitBtn.disabled) {
        navigateToBooking(input.value);
      }
    });

    // Submit button
    submitBtn.addEventListener("click", function () {
      if (!submitBtn.disabled) {
        navigateToBooking(input.value);
      }
    });

    // Hover effect on enabled button
    submitBtn.addEventListener("mouseenter", function () {
      if (!submitBtn.disabled) submitBtn.style.opacity = "0.9";
    });
    submitBtn.addEventListener("mouseleave", function () {
      if (!submitBtn.disabled) submitBtn.style.opacity = "1";
    });
  }

  // ─── Hero form: inline ZIP validation ────────────────────────────
  function initHeroForm() {
    var heroForm = document.querySelector("form[data-booking]");
    if (!heroForm) return;

    var zipInput = heroForm.querySelector('input[name="zip"]');
    if (!zipInput) return;

    // Make the zip column position:relative so helper can be absolute
    var zipWrapper = zipInput.parentNode;
    zipWrapper.style.position = "relative";

    // Create helper text element
    var helperEl = document.createElement("p");
    helperEl.id = "hero-zip-helper";
    helperEl.setAttribute("role", "status");
    helperEl.setAttribute("aria-live", "polite");
    helperEl.setAttribute("aria-atomic", "true");
    zipInput.setAttribute("aria-describedby", "hero-zip-helper");
    helperEl.style.cssText =
      "position:absolute;left:0;top:100%;margin:0.25rem 0 0;font-size:0.75rem;" +
      "white-space:nowrap;transition:color 150ms";
    helperEl.textContent = "";
    zipWrapper.appendChild(helperEl);

    // Real-time validation on the hero zip input
    zipInput.addEventListener("input", function () {
      var val = zipInput.value.replace(/\D/g, "").slice(0, 5);
      zipInput.value = val;

      if (val.length < 5) {
        zipInput.style.borderColor = "";
        zipInput.style.boxShadow = "";
        helperEl.textContent = "";
        return;
      }

      if (isValidZip(val)) {
        zipInput.style.borderColor = "#22c55e";
        zipInput.style.boxShadow = "0 0 0 1px #22c55e";
        helperEl.textContent = t("weServiceArea", "We service your area!");
        helperEl.style.color = "#22c55e";
        zipInput.setAttribute("aria-invalid", "false");
      } else {
        zipInput.style.borderColor = "#f87171";
        zipInput.style.boxShadow = "0 0 0 1px #f87171";
        helperEl.textContent = t(
          "noServiceArea",
          "Sorry, we don't service this area yet",
        );
        helperEl.style.color = "#f87171";
        zipInput.setAttribute("aria-invalid", "true");
      }
    });

    // Block form submit if zip is invalid
    heroForm.addEventListener("submit", function (e) {
      var val = (zipInput.value || "").replace(/\D/g, "");
      if (!isValidZip(val)) {
        e.preventDefault();
        if (val.length < 5) {
          helperEl.textContent = t(
            "enterZipCode",
            "Please enter your ZIP code",
          );
          helperEl.style.color = "#f87171";
        }
        zipInput.focus();
        zipInput.style.borderColor = "#f87171";
        zipInput.style.boxShadow = "0 0 0 1px #f87171";
        zipInput.setAttribute("aria-invalid", "true");
        return;
      }
      // Valid zip — let the form submit naturally
    });
  }

  // ─── Intercept all non-form booking links ────────────────────────
  function initLinkInterception() {
    document.addEventListener("click", function (e) {
      var target = e.target.closest("a[data-booking]");
      if (!target) return;

      e.preventDefault();
      openModal(target.href, target);
    });
  }

  // ─── Initialize ──────────────────────────────────────────────────
  function init() {
    initModal();
    initHeroForm();
    initLinkInterception();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
