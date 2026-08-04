/**
 * Consent-gated, cookie-free first-party event tracking for Inland Empire.
 *
 * The collector accepts only a small allowlist of event names and properties.
 * This client mirrors that contract, stores a UUID in sessionStorage, strips
 * URL query strings, and stays inert when DNT/GPC or required consent applies.
 */
(function () {
  "use strict";

  var config = window.__INLAND_TRACK || {};
  var endpoint = String(config.endpoint || "");
  var sessionKey = String(config.storageKey || "inland_tracking_sid");
  var utmStorageKey = String(config.utmStorageKey || "inland_utm");
  var bookingDomain = String(config.bookingDomain || "").toLowerCase();
  var consentRequired = config.consentRequired !== false;
  var consentKey = "inland_tracking_consent";
  var queue = [];
  var active = false;
  var initialized = false;
  var sessionId = "";
  var startedAt = typeof performance !== "undefined" ? performance.now() : 0;
  var scrollMilestones = {};

  function storageGet(key) {
    try {
      return sessionStorage.getItem(key);
    } catch (error) {
      return null;
    }
  }

  function storageSet(key, value) {
    try {
      sessionStorage.setItem(key, value);
      return true;
    } catch (error) {
      return false;
    }
  }

  function storageRemove(key) {
    try {
      sessionStorage.removeItem(key);
    } catch (error) {
      /* Storage is optional. */
    }
  }

  function privacyOptOut() {
    var dnt = String(navigator.doNotTrack || window.doNotTrack || "").toLowerCase();
    return navigator.globalPrivacyControl === true || dnt === "1" || dnt === "yes";
  }

  function consentGranted() {
    if (!consentRequired) return true;
    return (
      window.__INLAND_TRACKING_CONSENT === true ||
      storageGet(consentKey) === "granted"
    );
  }

  function createSessionId() {
    if (typeof crypto !== "undefined" && typeof crypto.randomUUID === "function") {
      return crypto.randomUUID();
    }
    return "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, function (char) {
      var random = Math.floor(Math.random() * 16);
      var value = char === "x" ? random : (random & 3) | 8;
      return value.toString(16);
    });
  }

  function cleanUrl(value, sameOriginOnly) {
    if (!value) return "";
    try {
      var url = new URL(value, window.location.origin);
      if (sameOriginOnly && url.origin !== window.location.origin) return "";
      return url.origin + url.pathname;
    } catch (error) {
      return "";
    }
  }

  function loadUtm() {
    try {
      var parsed = JSON.parse(storageGet(utmStorageKey) || "{}");
      return parsed && typeof parsed === "object" ? parsed : {};
    } catch (error) {
      return {};
    }
  }

  function sessionMeta() {
    var utm = loadUtm();
    return {
      landing_url: cleanUrl(window.location.href, true),
      referrer: cleanUrl(document.referrer, false),
      utm_source: String(utm.utm_source || ""),
      utm_medium: String(utm.utm_medium || ""),
      utm_campaign: String(utm.utm_campaign || ""),
      utm_content: String(utm.utm_content || ""),
      utm_term: String(utm.utm_term || ""),
      gclid: String(utm.gclid || ""),
      screen_width: window.screen ? window.screen.width : null,
      language: String(navigator.language || "").slice(0, 10),
    };
  }

  function track(name, properties) {
    if (!active) return;
    queue.push({
      name: String(name || "").slice(0, 50),
      properties: properties && typeof properties === "object" ? properties : {},
      ts: Date.now(),
    });
    if (queue.length >= 10) flush();
  }

  window.inlandTrack = track;

  function payload(events) {
    return JSON.stringify({
      session_id: sessionId,
      consent: consentGranted(),
      session_meta: sessionMeta(),
      events: events,
    });
  }

  function flush() {
    if (!active || !endpoint || !queue.length) return;
    var pending = queue.splice(0, 50);
    var body = payload(pending);
    if (navigator.sendBeacon) {
      var sent = navigator.sendBeacon(
        endpoint,
        new Blob([body], { type: "application/json" }),
      );
      if (sent) return;
    }
    if (typeof fetch === "function") {
      fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: body,
        credentials: "same-origin",
        keepalive: true,
      }).catch(function () {
        /* Tracking must never interrupt the user journey. */
      });
    }
  }

  function appendSessionToBookingTargets() {
    var links = document.querySelectorAll("a[data-booking]");
    for (var i = 0; i < links.length; i++) {
      try {
        var url = new URL(links[i].href, window.location.href);
        if (!bookingDomain || url.hostname.toLowerCase() === bookingDomain) {
          url.searchParams.set("tracking_session_id", sessionId);
          links[i].href = url.toString();
        }
      } catch (error) {
        /* Ignore malformed or placeholder links. */
      }
    }

    var forms = document.querySelectorAll("form[data-booking]");
    for (var f = 0; f < forms.length; f++) {
      var form = forms[f];
      if (form.querySelector('input[name="tracking_session_id"]')) continue;
      var input = document.createElement("input");
      input.type = "hidden";
      input.name = "tracking_session_id";
      input.value = sessionId;
      form.appendChild(input);
    }
  }

  function clickTarget(event, selector) {
    if (!event.target || typeof event.target.closest !== "function") return null;
    return event.target.closest(selector);
  }

  function bindClickTracking() {
    document.addEventListener("click", function (event) {
      var phoneLink = clickTarget(event, 'a[href^="tel:"]');
      if (phoneLink) {
        track("phone_click", {
          location: String(phoneLink.dataset.trackingLocation || "site"),
        });
        return;
      }

      var bookingLink = clickTarget(event, "a[data-booking]");
      if (bookingLink) {
        track("booking_click", {
          source: String(bookingLink.dataset.bookingSource || "site_cta"),
        });
        return;
      }

      var faqButton = clickTarget(event, "[data-faq-section] button");
      if (faqButton) {
        track("faq_expand", {
          question: String(faqButton.textContent || "").trim().slice(0, 300),
        });
        return;
      }

      var navItem = clickTarget(event, "[data-nav-key]");
      if (navItem) {
        track("nav_click", { label: String(navItem.dataset.navKey || "") });
        return;
      }

      var outbound = clickTarget(event, "a[href]");
      if (outbound) {
        try {
          var outboundUrl = new URL(outbound.href, window.location.href);
          if (outboundUrl.origin !== window.location.origin) {
            track("outbound_click", { target: outboundUrl.hostname });
          }
        } catch (error) {
          /* Ignore malformed links. */
        }
      }
    });

    document.addEventListener("submit", function (event) {
      var form = clickTarget(event, "form[data-booking]");
      if (!form) return;
      var service = form.querySelector('[name="service"]');
      track("booking_form_submit", {
        service: service ? String(service.value || "") : "",
      });
    });
  }

  function bindScrollTracking() {
    window.addEventListener(
      "scroll",
      function () {
        var documentHeight = Math.max(
          document.documentElement ? document.documentElement.scrollHeight : 0,
          document.body ? document.body.scrollHeight : 0,
        );
        var viewport = window.innerHeight || 0;
        var maximum = Math.max(documentHeight - viewport, 1);
        var depth = Math.min(100, Math.round(((window.scrollY || 0) / maximum) * 100));
        [25, 50, 75, 100].forEach(function (milestone) {
          if (depth >= milestone && !scrollMilestones[milestone]) {
            scrollMilestones[milestone] = true;
            track("scroll_depth", { depth: milestone });
          }
        });
      },
      { passive: true },
    );
  }

  function bindImpressions() {
    if (typeof IntersectionObserver !== "function") return;
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        var label = entry.target.dataset.bookingSource || entry.target.textContent || "cta";
        track("cta_impression", { cta: String(label).trim().slice(0, 100) });
        observer.unobserve(entry.target);
      });
    });
    var targets = document.querySelectorAll("a[data-booking], form[data-booking]");
    for (var i = 0; i < targets.length; i++) observer.observe(targets[i]);
  }

  function bindLifecycle() {
    window.addEventListener("pagehide", function () {
      var seconds = startedAt
        ? Math.max(0, Math.round((performance.now() - startedAt) / 1000))
        : 0;
      track("time_on_page", { seconds: seconds });
      flush();
    });
    document.addEventListener("visibilitychange", function () {
      if (document.visibilityState === "hidden") flush();
    });
    setInterval(flush, 5000);
  }

  function initialize() {
    if (initialized || privacyOptOut() || !endpoint || !consentGranted()) return;
    initialized = true;
    active = true;
    sessionId = storageGet(sessionKey) || createSessionId();
    storageSet(sessionKey, sessionId);
    appendSessionToBookingTargets();
    bindClickTracking();
    bindScrollTracking();
    bindImpressions();
    bindLifecycle();
    track("page_view", {
      title: String(document.title || "").slice(0, 300),
      path: String(window.location.pathname || "/").slice(0, 500),
    });
  }

  function handleConsent(event) {
    var granted = Boolean(event && event.detail && event.detail.granted === true);
    if (!granted) {
      storageRemove(consentKey);
      storageRemove(sessionKey);
      queue = [];
      active = false;
      return;
    }
    storageSet(consentKey, "granted");
    window.__INLAND_TRACKING_CONSENT = true;
    initialize();
  }

  window.addEventListener("inland:tracking-consent", handleConsent);
  window.inlandTrackingConsent = function (granted) {
    if (typeof window.dispatchEvent !== "function" || typeof CustomEvent !== "function") {
      handleConsent({ detail: { granted: granted === true } });
      return;
    }
    window.dispatchEvent(
      new CustomEvent("inland:tracking-consent", {
        detail: { granted: granted === true },
      }),
    );
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initialize);
  } else {
    initialize();
  }
})();
