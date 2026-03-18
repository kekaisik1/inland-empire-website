/**
 * UTM Parameter Forwarding
 *
 * Captures UTM parameters from the landing URL and appends them
 * to all booking links AND forms so the booking system receives
 * full attribution from Google Ads and other campaigns.
 *
 * Tracked params: utm_source, utm_medium, utm_campaign, utm_content,
 *                 utm_term, gclid, gad_source, gad_campaignid
 *
 * Works with:
 *   - <a data-booking> links  (rewrites href)
 *   - <form data-booking> forms (injects hidden inputs)
 */
(function () {
  "use strict";

  var UTM_KEYS = [
    "utm_source",
    "utm_medium",
    "utm_campaign",
    "utm_content",
    "utm_term",
    "gclid",
    "gad_source",
    "gad_campaignid",
  ];
  var STORAGE_KEY = "lowl_utm";

  function getUtmFromUrl() {
    var params = {};
    var search = window.location.search;
    if (!search) return params;

    var pairs = search.substring(1).split("&");
    for (var i = 0; i < pairs.length; i++) {
      var parts = pairs[i].split("=");
      var key = decodeURIComponent(parts[0]);
      if (UTM_KEYS.indexOf(key) !== -1 && parts[1]) {
        params[key] = decodeURIComponent(parts[1]);
      }
    }
    return params;
  }

  function save(params) {
    if (Object.keys(params).length === 0) return;
    try {
      sessionStorage.setItem(STORAGE_KEY, JSON.stringify(params));
    } catch (e) {
      /* storage unavailable */
    }
  }

  function load() {
    try {
      var stored = sessionStorage.getItem(STORAGE_KEY);
      return stored ? JSON.parse(stored) : {};
    } catch (e) {
      return {};
    }
  }

  function appendToUrl(href, utmParams) {
    var keys = Object.keys(utmParams);
    if (keys.length === 0) return href;

    var sep = href.indexOf("?") !== -1 ? "&" : "?";
    var qs = keys
      .map(function (k) {
        return encodeURIComponent(k) + "=" + encodeURIComponent(utmParams[k]);
      })
      .join("&");

    return href + sep + qs;
  }

  function getBookingSource() {
    return window.__BOOKING_SOURCE || "lowl";
  }

  function updateBookingLinks(utmParams) {
    // Always include source identifier
    var paramsWithSource = {};
    paramsWithSource.source = getBookingSource();
    var keys = Object.keys(utmParams);
    for (var i = 0; i < keys.length; i++) {
      paramsWithSource[keys[i]] = utmParams[keys[i]];
    }

    // Rewrite <a data-booking> hrefs
    var links = document.querySelectorAll("a[data-booking]");
    for (var i = 0; i < links.length; i++) {
      links[i].href = appendToUrl(links[i].href, paramsWithSource);
    }

    // Inject hidden inputs into <form data-booking> elements
    var forms = document.querySelectorAll("form[data-booking]");
    for (var f = 0; f < forms.length; f++) {
      var form = forms[f];
      var allKeys = Object.keys(paramsWithSource);
      for (var j = 0; j < allKeys.length; j++) {
        // Skip if a field with this name already exists
        if (form.querySelector('input[name="' + allKeys[j] + '"]')) continue;
        var input = document.createElement("input");
        input.type = "hidden";
        input.name = allKeys[j];
        input.value = paramsWithSource[allKeys[j]];
        form.appendChild(input);
      }
    }
  }

  // Also inject UTM params as hidden fields in the contact form
  // so contact inquiries can be attributed to campaigns
  function updateContactForm(utmParams) {
    var contactForm = document.querySelector('form[action*="contact"]');
    if (!contactForm) return;

    var keys = Object.keys(utmParams);
    for (var i = 0; i < keys.length; i++) {
      if (contactForm.querySelector('input[name="' + keys[i] + '"]')) continue;
      var input = document.createElement("input");
      input.type = "hidden";
      input.name = keys[i];
      input.value = utmParams[keys[i]];
      contactForm.appendChild(input);
    }
  }

  // Capture on landing, persist, rewrite
  var fresh = getUtmFromUrl();
  if (Object.keys(fresh).length > 0) save(fresh);

  var utm = Object.keys(fresh).length > 0 ? fresh : load();

  function init() {
    updateBookingLinks(utm);
    updateContactForm(utm);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
