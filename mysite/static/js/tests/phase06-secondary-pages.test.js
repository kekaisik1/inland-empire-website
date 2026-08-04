"use strict";

const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const test = require("node:test");
const vm = require("node:vm");

const JS_PATH = path.resolve(__dirname, "..", "alpine-components.js");

function loadComponents(documentOverrides = {}) {
  const components = {};
  const document = {
    body: { classList: { add() {}, remove() {} } },
    addEventListener(name, callback) {
      if (name === "alpine:init") callback();
    },
    querySelector() {
      return null;
    },
    querySelectorAll() {
      return [];
    },
    ...documentOverrides,
  };
  class IntersectionObserver {
    constructor(callback) {
      this.callback = callback;
      this.targets = [];
    }
    observe(target) {
      this.targets.push(target);
    }
    disconnect() {}
  }
  const window = {
    scrollY: 0,
    innerHeight: 800,
    IntersectionObserver,
    scrollTo() {},
  };
  const Alpine = {
    data(name, factory) {
      components[name] = factory;
    },
  };
  vm.runInNewContext(
    fs.readFileSync(JS_PATH, "utf8"),
    {
      Alpine,
      IntersectionObserver,
      document,
      navigator: { clipboard: { writeText: () => Promise.resolve() } },
      window,
      console,
      setTimeout,
      clearTimeout,
    },
    { filename: "alpine-components.js" },
  );
  return { components, document, window };
}

test("service carousel exposes bounded controls, keyboard navigation, and swipe state", () => {
  const { components } = loadComponents();
  assert.equal(typeof components.serviceCarousel, "function");

  const items = [0, 1, 2].map((index) => ({
    offsetLeft: index * 320,
    scrollCalls: [],
    scrollIntoView(options) {
      this.scrollCalls.push(options);
    },
  }));
  const track = {
    scrollLeft: 0,
    querySelectorAll() {
      return items;
    },
  };
  const component = components.serviceCarousel();
  component.$refs = { track };
  component.init();

  assert.equal(component.count, 3);
  assert.equal(component.index, 0);
  assert.equal(component.atStart, true);
  assert.equal(component.statusText, "Image 1 of 3");

  component.next();
  assert.equal(component.index, 1);
  assert.equal(items[1].scrollCalls.length, 1);

  let prevented = false;
  component.onKeydown({ key: "End", preventDefault() { prevented = true; } });
  assert.equal(prevented, true);
  assert.equal(component.index, 2);
  assert.equal(component.atEnd, true);

  component.pointerDown({ clientX: 160 });
  component.pointerUp({ clientX: 230 });
  assert.equal(component.index, 1);

  component.onKeydown({ key: "Home", preventDefault() {} });
  component.previous();
  assert.equal(component.index, 0, "previous remains bounded at the first image");
});

test("contact form marks invalid fields and moves focus without submitting", () => {
  const { components } = loadComponents();
  assert.equal(typeof components.contactForm, "function");

  const attributes = new Map();
  const invalid = {
    validity: { valid: false },
    focusCount: 0,
    setAttribute(name, value) { attributes.set(name, value); },
    removeAttribute(name) { attributes.delete(name); },
    focus() { this.focusCount += 1; },
  };
  const form = {
    checkValidity() { return false; },
    querySelector(selector) { return selector === ":invalid" ? invalid : null; },
  };
  const component = components.contactForm();
  let prevented = false;
  component.onInvalid({ target: invalid });
  component.onSubmit({
    currentTarget: form,
    preventDefault() { prevented = true; },
  });

  assert.equal(prevented, true);
  assert.equal(attributes.get("aria-invalid"), "true");
  assert.equal(invalid.focusCount, 1);

  invalid.validity.valid = true;
  component.onInput({ target: invalid });
  assert.equal(attributes.has("aria-invalid"), false);
});

test("blog reading progress is registered and clamps article progress", () => {
  const article = {
    offsetHeight: 2000,
    getBoundingClientRect() { return { top: -500 }; },
  };
  const { components, window } = loadComponents({
    querySelector(selector) {
      return selector === "[data-blog-article]" ? article : null;
    },
  });
  assert.equal(typeof components.readingProgress, "function");
  assert.equal(typeof components.blogToc, "function");

  const component = components.readingProgress();
  window.scrollY = 500;
  component.onScroll();
  assert.equal(component.progress > 0, true);
  assert.equal(component.progress <= 100, true);
  assert.match(component.barStyle, /^width:[0-9.]+%;$/);
});

test("blog reading progress advances within the reachable range for a short article", () => {
  let browserWindow;
  const article = {
    offsetHeight: 421,
    getBoundingClientRect() {
      return { top: 624 - browserWindow.scrollY };
    },
  };
  const loaded = loadComponents({
    documentElement: { scrollHeight: 1462 },
    querySelector(selector) {
      return selector === "[data-blog-article]" ? article : null;
    },
  });
  browserWindow = loaded.window;
  browserWindow.innerHeight = 900;
  browserWindow.scrollY = 562;

  const component = loaded.components.readingProgress();
  component.onScroll();

  assert.equal(Number.isFinite(component.progress), true);
  assert.equal(component.progress > 0, true);
  assert.equal(component.progress <= 100, true);
  assert.notEqual(component.barStyle, "width:0.00%;");
});

test("mobile quick actions stay hidden on the contact page", () => {
  const body = {
    classList: {
      add() {},
      remove() {},
      contains(value) {
        return value === "page-contact";
      },
    },
  };
  const { components } = loadComponents({ body });
  const component = components.mobileQuickActions();
  component.$watch = () => {};
  component.init();

  assert.equal(component.isVisible, false);
});
