"use strict";

const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const test = require("node:test");
const vm = require("node:vm");

const JS_DIR = path.resolve(__dirname, "..");

function loadAlpineComponents() {
  const components = {};
  const classNames = new Set();
  const heroBooking = { name: "hero-booking" };
  const observers = [];
  const document = {
    body: {
      classList: {
        add(name) {
          classNames.add(name);
        },
        remove(name) {
          classNames.delete(name);
        },
        contains(name) {
          return classNames.has(name);
        },
      },
    },
    addEventListener(name, callback) {
      if (name === "alpine:init") callback();
    },
    querySelector(selector) {
      return selector === ".booking-widget" ? heroBooking : null;
    },
  };
  class IntersectionObserver {
    constructor(callback, options) {
      this.callback = callback;
      this.options = options;
      this.observed = [];
      this.disconnected = false;
      observers.push(this);
    }
    observe(target) {
      this.observed.push(target);
    }
    disconnect() {
      this.disconnected = true;
    }
  }
  const Alpine = {
    data(name, factory) {
      components[name] = factory;
    },
  };
  vm.runInNewContext(
    fs.readFileSync(path.join(JS_DIR, "alpine-components.js"), "utf8"),
    { Alpine, document, window: { IntersectionObserver }, console, setTimeout, clearTimeout },
    { filename: "alpine-components.js" },
  );
  return { components, document, heroBooking, observers };
}

function focusable(name) {
  return {
    name,
    focusCount: 0,
    focus() {
      this.focusCount += 1;
    },
  };
}

test("mobile navigation moves focus, traps Tab, and returns focus on Escape", () => {
  const { components, document } = loadAlpineComponents();
  assert.equal(typeof components.mobileNav, "function");

  const toggle = focusable("toggle");
  const first = focusable("first");
  const last = focusable("last");
  const menu = {
    querySelectorAll() {
      return [first, last];
    },
  };
  const component = components.mobileNav.call({ $refs: { mobileToggle: toggle, mobileMenu: menu } });
  component.$refs = { mobileToggle: toggle, mobileMenu: menu };
  component.$nextTick = (callback) => callback();

  component.toggle();
  assert.equal(component.isOpen, true);
  assert.equal(first.focusCount, 1);
  assert.equal(document.body.classList.contains("nav-open"), true);
  assert.equal(typeof component.trapFocus, "function");

  let prevented = false;
  component.trapFocus({
    key: "Tab",
    shiftKey: false,
    target: last,
    preventDefault() {
      prevented = true;
    },
  });
  assert.equal(prevented, true);
  assert.equal(first.focusCount, 2);

  component.closeOnEscape({
    key: "Escape",
    preventDefault() {},
  });
  assert.equal(component.isOpen, false);
  assert.equal(toggle.focusCount, 1);
  assert.equal(document.body.classList.contains("nav-open"), false);
});

test("desktop dropdown supports Enter, Space, click-away, and Escape focus return", () => {
  const { components } = loadAlpineComponents();
  assert.equal(typeof components.desktopDropdown, "function");

  const trigger = focusable("trigger");
  const first = focusable("menuitem");
  const menu = {
    querySelector() {
      return first;
    },
  };
  const component = components.desktopDropdown.call({ $refs: { trigger, menu } });
  component.$refs = { trigger, menu };
  component.$nextTick = (callback) => callback();

  let prevented = false;
  component.openFromKeyboard({
    key: "Enter",
    preventDefault() {
      prevented = true;
    },
  });
  assert.equal(prevented, true);
  assert.equal(component.isOpen, true);
  assert.equal(first.focusCount, 1);
  assert.equal(component.expandedStr, "true");

  component.close();
  component.openFromKeyboard({ key: " ", preventDefault() {} });
  assert.equal(component.isOpen, true);
  component.closeOnEscape({ key: "Escape", preventDefault() {} });
  assert.equal(component.isOpen, false);
  assert.equal(trigger.focusCount, 1);
});

test("mobile quick actions stay clear of the hero booking form", () => {
  const { components, heroBooking, observers } = loadAlpineComponents();
  assert.equal(typeof components.mobileQuickActions, "function");

  const component = components.mobileQuickActions();
  component.init();
  assert.equal(observers.length, 1);
  assert.deepEqual(observers[0].observed, [heroBooking]);

  observers[0].callback([{ isIntersecting: true }]);
  assert.equal(component.isVisible, false);
  observers[0].callback([{ isIntersecting: false }]);
  assert.equal(component.isVisible, true);

  component.destroy();
  assert.equal(observers[0].disconnected, true);
});

function storageDouble(initial = {}) {
  const values = new Map(Object.entries(initial));
  return {
    getItem(key) {
      return values.has(key) ? values.get(key) : null;
    },
    setItem(key, value) {
      values.set(key, String(value));
    },
    removeItem(key) {
      values.delete(key);
    },
    value(key) {
      return values.get(key);
    },
  };
}

test("UTM forwarding uses Inland identifiers and preserves existing booking fields", () => {
  const storage = storageDouble();
  const anchor = {
    href: "https://booking.inland.test/schedule?service=washer",
  };
  const fields = new Map();
  const form = {
    querySelector(selector) {
      const match = selector.match(/name=\"([^\"]+)\"/);
      return match && fields.has(match[1]) ? fields.get(match[1]) : null;
    },
    appendChild(input) {
      fields.set(input.name, input);
    },
  };
  const document = {
    readyState: "complete",
    createElement() {
      return {};
    },
    querySelectorAll(selector) {
      if (selector === "a[data-booking]") return [anchor];
      if (selector === "form[data-booking]") return [form];
      return [];
    },
    querySelector() {
      return null;
    },
    addEventListener() {},
  };
  const window = {
    __BOOKING_SOURCE: "inland-test",
    location: {
      href: "https://inland.test/?utm_source=google&utm_campaign=summer",
      search: "?utm_source=google&utm_campaign=summer",
    },
  };
  vm.runInNewContext(
    fs.readFileSync(path.join(JS_DIR, "utm.js"), "utf8"),
    {
      URL,
      decodeURIComponent,
      encodeURIComponent,
      document,
      sessionStorage: storage,
      window,
      console,
    },
    { filename: "utm.js" },
  );

  const booking = new URL(anchor.href);
  assert.equal(booking.searchParams.get("service"), "washer");
  assert.equal(booking.searchParams.get("source"), "inland-test");
  assert.equal(booking.searchParams.get("utm_source"), "google");
  assert.equal(booking.searchParams.get("utm_campaign"), "summer");
  assert.equal(booking.searchParams.getAll("source").length, 1);
  assert.equal(storage.value("inland_utm"), '{"utm_source":"google","utm_campaign":"summer"}');
  assert.equal(fields.get("source").value, "inland-test");
  assert.equal(fields.get("utm_source").value, "google");
});

function addListener(store, name, callback) {
  if (!store[name]) store[name] = [];
  store[name].push(callback);
}

test("first-party tracker is consent-gated and emits target API payloads", () => {
  const sourcePath = path.join(JS_DIR, "tracker.js");
  assert.equal(fs.existsSync(sourcePath), true, "tracker.js must exist");

  const storage = storageDouble({
    inland_utm: '{"utm_source":"google","utm_campaign":"summer"}',
  });
  const documentListeners = {};
  const windowListeners = {};
  const beacons = [];
  const document = {
    readyState: "complete",
    referrer: "https://search.example/results?q=private",
    visibilityState: "visible",
    title: "Inland Home",
    addEventListener(name, callback) {
      addListener(documentListeners, name, callback);
    },
    querySelectorAll() {
      return [];
    },
  };
  const window = {
    __INLAND_TRACK: {
      endpoint: "/api/track/collect/",
      bookingDomain: "booking.inland.test",
      storageKey: "phase05_sid",
      utmStorageKey: "inland_utm",
      consentRequired: true,
    },
    location: {
      href: "https://inland.test/?private=query",
      origin: "https://inland.test",
      pathname: "/",
      search: "?private=query",
      hostname: "inland.test",
    },
    screen: { width: 390 },
    addEventListener(name, callback) {
      addListener(windowListeners, name, callback);
    },
  };
  const navigator = {
    doNotTrack: "0",
    globalPrivacyControl: false,
    language: "en-US",
    sendBeacon(endpoint, blob) {
      beacons.push({ endpoint, body: blob.parts.join("") });
      return true;
    },
  };
  class BlobDouble {
    constructor(parts) {
      this.parts = parts;
    }
  }
  class IntersectionObserverDouble {
    observe() {}
    unobserve() {}
  }

  vm.runInNewContext(
    fs.readFileSync(sourcePath, "utf8"),
    {
      Blob: BlobDouble,
      IntersectionObserver: IntersectionObserverDouble,
      URL,
      URLSearchParams,
      clearTimeout,
      console,
      crypto: { randomUUID: () => "123e4567-e89b-42d3-a456-426614174000" },
      document,
      fetch: () => Promise.resolve(),
      navigator,
      performance: { now: () => 1000 },
      sessionStorage: storage,
      setInterval: () => 1,
      setTimeout,
      window,
    },
    { filename: "tracker.js" },
  );

  assert.equal(storage.value("phase05_sid"), undefined);
  assert.equal(beacons.length, 0);
  assert.equal(typeof window.inlandTrack, "function");

  const consentListeners = windowListeners["inland:tracking-consent"] || [];
  assert.equal(consentListeners.length, 1);
  consentListeners[0]({ detail: { granted: true } });
  window.inlandTrack("nav_click", { label: "Services" });
  for (const callback of windowListeners.pagehide || []) callback();

  assert.equal(storage.value("phase05_sid"), "123e4567-e89b-42d3-a456-426614174000");
  assert.equal(beacons.length, 1);
  assert.equal(beacons[0].endpoint, "/api/track/collect/");
  const payload = JSON.parse(beacons[0].body);
  assert.equal(payload.consent, true);
  assert.equal(payload.session_meta.landing_url, "https://inland.test/");
  assert.equal(payload.session_meta.utm_source, "google");
  assert.equal(payload.events.some((event) => event.name === "nav_click"), true);
  assert.equal(payload.events.some((event) => event.properties.label === "Services"), true);
  assert.equal(beacons[0].body.includes("private=query"), false);
});

test("ZIP checker uses target coverage data and preserves booking parameters", () => {
  const moduleDouble = { exports: {} };
  const serviceZipScript = { textContent: '["92879","92880"]' };
  const document = {
    readyState: "loading",
    addEventListener() {},
    getElementById(id) {
      return id === "service-zip-codes" ? serviceZipScript : null;
    },
  };
  const window = {
    __ZIP_CHECK_I18N: {},
    location: { href: "https://inland.test/" },
  };
  vm.runInNewContext(
    fs.readFileSync(path.join(JS_DIR, "zip-check.js"), "utf8"),
    {
      URL,
      console,
      document,
      module: moduleDouble,
      setTimeout,
      window,
    },
    { filename: "zip-check.js" },
  );

  assert.equal(typeof moduleDouble.exports.readServiceZipCodes, "function");
  assert.equal(typeof moduleDouble.exports.isValidZip, "function");
  assert.equal(typeof moduleDouble.exports.buildBookingUrl, "function");
  assert.deepEqual(
    Array.from(moduleDouble.exports.readServiceZipCodes(document)),
    ["92879", "92880"],
  );
  assert.equal(moduleDouble.exports.isValidZip("92879", ["92879", "92880"]), true);
  assert.equal(moduleDouble.exports.isValidZip("91706", ["92879", "92880"]), false);

  const destination = moduleDouble.exports.buildBookingUrl(
    "https://booking.inland.test/schedule?source=inland-test&utm_source=google",
    "92879",
    {
      service: "washer-repair",
      tracking_session_id: "123e4567-e89b-42d3-a456-426614174000",
    },
  );
  const url = new URL(destination);
  assert.equal(url.searchParams.get("zip"), "92879");
  assert.equal(url.searchParams.get("service"), "washer-repair");
  assert.equal(url.searchParams.get("source"), "inland-test");
  assert.equal(url.searchParams.get("utm_source"), "google");
  assert.equal(
    url.searchParams.get("tracking_session_id"),
    "123e4567-e89b-42d3-a456-426614174000",
  );
});

test("ZIP feedback is announced and uses an AA-contrast error color", () => {
  const source = fs.readFileSync(path.join(JS_DIR, "zip-check.js"), "utf8");
  assert.match(source, /aria-live=[\\"']polite[\\"']/);
  assert.match(source, /aria-atomic=[\\"']true[\\"']/);
  assert.match(source, /setAttribute\([\\"']aria-describedby[\\"'], [\\"']hero-zip-helper[\\"']\)/);
  assert.equal(source.includes("#f87171"), true);
  assert.equal(source.includes("#ef4444"), false);
});

test("shared scripts contain no LOWL client identifiers", () => {
  const names = ["alpine-components.js", "utm.js", "zip-check.js", "tracker.js"];
  for (const name of names) {
    assert.equal(fs.existsSync(path.join(JS_DIR, name)), true, `${name} must exist`);
  }
  const combined = names
    .map((name) => fs.readFileSync(path.join(JS_DIR, name), "utf8"))
    .join("\n");
  for (const token of ["lowl_utm", "lowl_sid", "__LOWL_TRACK", "window.lowlTrack"]) {
    assert.equal(combined.includes(token), false, token);
  }
  assert.equal(combined.includes("inland_utm"), true);
  assert.equal(combined.includes("tracking_session_id"), true);
});
