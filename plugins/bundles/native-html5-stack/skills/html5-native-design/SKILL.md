---
name: html5-native-design
description: Modern HTML5 elements and CSS features for beautiful sites without a JS framework. Use this skill to design with the Popover API, the `dialog` element, the `details` and `summary` elements, container queries, `:has()`, subgrid, `color-mix()`, Web Components, Fetch + streaming, modern HTML form attributes, and other stable native APIs. Triggers on tasks involving modern HTML5 UI elements, advanced CSS, container queries, the Popover API, `dialog` modal, native form UX, declarative Shadow DOM, attribute change observation, modern form pattern. Anywhere a site needs visually rich UI without a UI framework, pair with htmx for server-rendered composition and with web-animations-api for native motion.
---

# HTML5 Native Design — Beautiful Sites Without a Framework

> **Audit date**: 2026-09-23.
> This skill is **framework-free**. It is the third leg of the
> no-framework stack alongside `htmx` (server-driven interactivity)
> and `web-animations-api` (native motion).

Browsers ship more UI primitives every year. In 2026 a site can be
fully interactive using only HTML elements, CSS, and small amounts of
JS — no React, no Vue, no Shadow-DOM-only UI library. This skill
collects the 30-or-so native primitives worth using on a real site.

**When to use this skill:**

- Building beautiful interactive sites **without** a UI framework.
- Replacing modal/drawer/popover libraries with `<dialog>` and the
  Popover API.
- Replacing `useState` / `useEffect` micro-state with declarative
  CSS (`:has()`, `:checked`, `:focus-within`, container queries).
- Building accessible forms using modern HTML attributes
  (`autocomplete`, `inputmode`, `enterkeyhint`, `datalist`).
- Composing reusable UI bits as **Web Components** instead of pulling
  in Lit, Stencil, or framework-specific component libraries.

**When NOT to use it:**

- Heavy client-side state graphs, real-time collaborative editors,
  virtualisation libraries — reach for React/Solid/Svelte.
- Heavy data-grid / table needs (>100k rows) — specialised libs do
  this better.
- Truly build-pipeline-heavy workflows (Tailwind v4,
  PostCSS-only-on-build setups) — pick a framework.

**Companion skills:**

- `htmx` — server-rendered partial updates that pair beautifully
  with native HTML5 elements.
- `web-animations-api` — `<dialog>` open animation, Popover morph,
  scroll-bound timelines.
- `modern-web-design` — accessibility rules (INP, contrast, touch
  targets) above this.
- `gsap-scrolltrigger` — only when scroll orchestration grows too
  complex for CSS scroll-driven animations.

---

## Core Concepts

### 1. The principles

Three principles guide every "amazing native" site:

1. **HTML is the state machine.** If you can express your
   interactive state in `checked`, `open`, `popover`, `value`,
   `:has()`, `:focus-within`, you don't need JavaScript.
2. **CSS owns the presentation.** Variables + container queries +
   `:has()` + `@supports` give you most of what preprocessors and
   JS-driven libraries provide.
3. **JS is the imperative glue.** It's reserved for the things HTML
   and CSS can't express, like `IntersectionObserver` glue or
   `MutationObserver` reactions.

### 2. The 30 primitives worth using

Grouped by what they replace.

**Modals, popovers, drawers:**

- `<dialog>` (`showModal()`, `close()`)
- `popover` attribute (`showPopover()`, `hidePopover()`)
- `popovertarget` (declarative button → popover)
- `::backdrop` (CSS pseudo-element)
- `command` / `commandfor` (1.x declarative buttons — 2026+)

**Disclosure / collapse:**

- `<details>` / `<summary>` — now animated via CSS
  `transition-behavior: allow-discrete`
- `:focus-within` — open on focus
- `:has()` — open on child state

**Modern CSS layout:**

- `display: grid; grid-template-columns: subgrid;`
- `gap`, `grid-template-rows/columns: masonry`
- `:has()`, `:where()`, `:is()`, `:not()` logical selectors
- `container-type: inline-size` + `@container`
- `css-nesting` (`section { & h2 { ... } }`)
- `color-mix(in srgb, …, …)` (and oklch)
- `@layer` cascade layers
- `clamp()`, `min()`, `max()` (already common)

**Modern forms:**

- `autocomplete`, `inputmode`, `enterkeyhint`, `pattern`, `min`,
  `max`, `step`, `required`, `readonly`
- `<datalist>`, `<output>`, `<meter>`, `<progress>`
- Custom validation via constraint validation API
- `<selectmenu>` (progressive — coming to all engines)

**Visibility / accessibility:**

- `popover="auto"` (light dismiss) vs `popover="manual"`
- `inert` attribute (disable subtree)
- `aria-live`, `aria-expanded`, `role="dialog"`
- `details[name=…]` exclusive accordions (Chrome 120+)

**State-bridging:**

- `:has(:target)` — anchor link styling
- `:has(:checked)` — toggle-driven layout
- `:has(:focus)` — focus-driven theming
- `:has(:placeholder-shown)` — empty-input theming
- `:has(:user-invalid)` — form-error styling

**Web platform APIs:**

- `Element.animate(...)` and `getAnimations()`
- `document.startViewTransition(...)` — same-doc DOM swaps
- `ResizeObserver`, `IntersectionObserver`, `MutationObserver`,
  `PerformanceObserver`
- `AbortController` for fetch
- `PopoverInvokerElement` (Popover API)
- Custom Elements / Shadow DOM / Declarative Shadow DOM
- Web Audio (procedural background sound, only when requested)

### 3. Browser support policy

2026 timeline for each primitive:

| Feature | Chrome | Edge | Firefox | Safari |
|---|---|---|---|---|
| Container queries | 105+ | 105+ | 117+ | 16+ |
| `:has()` | 105+ | 105+ | 121+ | 15.4+ |
| `color-mix()` | 111+ | 111+ | 113+ | 16.2+ |
| `<dialog>` | 37+ | 79+ | 98+ | 15.4+ |
| Popover API | 114+ | 114+ | 125+ | 17+ |
| `<selectmenu>` | 121+ | 121+ | — | — |
| `details[name=…]` | 120+ | 120+ | 123+ | 17.2+ |
| Subgrid | 117+ | 117+ | 71+ | 16+ |
| View Transitions (same-doc) | 111+ | 111+ | 137+ | 18+ |
| `css-nesting` | 112+ | 112+ | 117+ | 16.5+ |
| `transition-behavior: allow-discrete` | 117+ | 117+ | 129+ | 17.4+ |
| `popovertarget` declarative | 114+ | 114+ | 125+ | 17+ |
| `inert` | 102+ | 102+ | 112+ | 15.5+ |
| `@layer` | 99+ | 99+ | 97+ | 15.4+ |
| `clamp()` / `min()` / `max()` | 79+ | 79+ | 75+ | 13.1+ |

Use `@supports` to gate modern features on capable browsers; older
browsers get a simpler fallback from the same HTML.

---

## Common Patterns — Beautiful, Native, Reusable

### 1. Modal with `<dialog>`

```html
<dialog id="confirm" class="modal">
  <article>
    <h2>Confirm order</h2>
    <p>You're about to place a $42 order.</p>
    <form method="dialog" class="actions">
      <button value="cancel">Cancel</button>
      <button value="confirm" autofocus>Confirm</button>
    </form>
  </article>
</dialog>
<button onclick="confirm.showModal()">Place order</button>
```

```css
.modal {
  border: 1px solid #ddd;
  border-radius: .75rem;
  background: var(--surface);
  color: var(--fg);
  padding: 0;                       /* card handles padding */
  inset: 0; margin: auto;            /* center */
  max-width: min(90vw, 480px);
  /* Open/close animation */
  opacity: 0; transform: translateY(8px) scale(.985);
  transition: opacity 220ms ease-out,
              transform 280ms cubic-bezier(.2,.8,.2,1),
              overlay 280ms allow-discrete;
}
.modal[open] { opacity: 1; transform: none; }
@starting-style { .modal[open] { opacity: 0; transform: translateY(8px) scale(.985); } }
.modal::backdrop { background: transparent; transition: background 220ms ease-out; }
.modal[open]::backdrop { background: rgba(0,0,0,.4); }

@supports not (transition-behavior: allow-discrete) {
  .modal { transition: none; }
}
```

`<form method="dialog">` returns a close + value; the submitting
button's `value` attribute is what `dialog.returnValue` reads.

### 2. Hover-triggered popover (CSS-only, no JS)

```html
<button popovertarget="user-info" popovertargetaction="toggle"
        style="anchor-name:--user-btn">@ada</button>

<div id="user-info" popover="manual"
     style="position-anchor:--user-btn; inset:auto; margin:0;">
  <p>Ada Lovelace</p>
  <p>First programmer</p>
</div>
```

CSS Anchor Positioning (Chrome 125+) lets the popover attach to a
button anchor without JS measurement.

### 3. Exclusive accordion (one open at a time)

```html
<details name="acc">
  <summary>Section A</summary>
  <p>…</p>
</details>
<details name="acc">
  <summary>Section B</summary>
  <p>…</p>
</details>
```

`details[name=…]` makes `<details>` mutually exclusive within a
name group — opening one closes the others. No JS.

### 4. Animated `<details>` (the "smooth accordion")

```css
details {
  border: 1px solid #ddd;
  border-radius: .5rem;
  padding: 1rem;
}
details::details-content {
  /* csswg proposal — not yet shipped; use wrapper as fallback */
}
details > :not(summary) {
  opacity: 0;
  height: 0;
  overflow: hidden;
  /* Smooth height transitions are tricky in 2026 because
     height: auto can't be transitioned. Two options: */
}
/* Option A: line-clamp (only animates text, not raw HTML) */
/* details[open] > :not(summary) { height: auto; opacity: 1; } */

/* Option B: WAAPI to set max-height on close,auto on open */
details > :not(summary) {
  display: grid;
  grid-template-rows: 0fr;
  opacity: 0;
  transition: grid-template-rows 240ms cubic-bezier(.2,.8,.2,1),
              opacity 240ms;
}
details[open] > :not(summary) {
  grid-template-rows: 1fr;
  opacity: 1;
}
```

The grid-template-rows trick (`0fr → 1fr`) is the modern way to
animate to `height: auto` without measuring the content.

### 5. Container queries — the layout primitive

```css
.card-grid > .card {
  /* Component decides its own layout based on its size,
     not the viewport size. */
  container-type: inline-size;
  container-name: card;
}
@container card (min-width: 480px) {
  .card .meta { display: grid; grid-template-columns: 1fr 1fr; }
}
@container card (max-width: 479px) {
  .card .meta { display: block; }
  .card .image { display: none; }
}
```

Inside `@container`, the `container-type: inline-size` parent is the
viewport-equivalent. Works in shadow DOM too.

### 6. `:has()`-driven theming

```css
/* Form: if any field is :user-invalid, dim the rest of the page. */
:root:has(form :user-invalid) main { opacity: .8; }

/* Article: if the article contains an image, lay it out specially. */
.article:has(> figure) { grid-template-columns: 1fr 320px; }

/* Theme: if the system is dark, default. */
:root:has(.theme-light) { /* override */ }
@container card (min-width: 700px) {
  .card:has(.image) { display: grid; grid-template-columns: 240px 1fr; }
}
```

`:has()` is the relational sibling selector — it picks up state from
any descendant.

### 7. Modern form UX

```html
<form class="contact" novalidate>
  <label>Email
    <input type="email" name="email"
           autocomplete="email"
           inputmode="email"
           enterkeyhint="next"
           required>
  </label>
  <label>Country
    <input name="country" list="cc" autocomplete="country"
           inputmode="text">
  </label>
  <datalist id="cc">
    <option>United States</option>
    <option>United Kingdom</option>
    <option>Australia</option>
  </datalist>
  <label>Code
    <input name="code" inputmode="numeric"
           pattern="[0-9]{3}"
           maxlength="3"
           required>
  </label>
  <button type="submit">Send</button>
</form>
```

```css
input:user-invalid { border-color: #dc2626; }
input:user-invalid:focus { outline-color: #dc2626; }

@supports (field-sizing: content) {
  textarea, input { field-sizing: content; }
}
```

`field-sizing: content` lets a text input/textarea size to its
content rather than its width attribute (Chrome 123+).

### 8. Accessible submit-feedback with `aria-live`

```html
<form id="contact" hx-post="/api/contact" hx-swap="innerHTML"
      hx-target="#status">
  <input name="email" type="email" required>
  <button>Send</button>
</form>
<div id="status" aria-live="polite"></div>
```

Pair with HTMX (or a `submit` event handler) — the response lands
inside the live region and a screen reader announces it.

### 9. Scroll-driven "smooth accordion" with `view()` timeline

```css
details > :not(summary) {
  animation: close linear both;
  animation-timeline: view();
  animation-range: exit 0% exit 100%;
}
details[open] > :not(summary) {
  animation: open linear both;
  animation-timeline: view();
  animation-range: entry 0% entry 50%;
}
```

(Use CSS scroll-driven animations from `web-animations-api` for the
two state phases — entry and exit. Browser support
[scoped to modern engines].)

### 10. Web Component — encapsulated reuse

```javascript
class ImageFigure extends HTMLElement {
  static observedAttributes = ['src', 'caption']
  // Mark up the declarative Shadow DOM with the static HTML attribute below.

  connectedCallback() {
    if (this.shadowRoot) return  // declarative shadow root takes over
    const root = this.attachShadow({ mode: 'open' })
    root.innerHTML = `
      <style>
        figure { margin: 0; }
        figcaption { font: 14px/1.5 system-ui; opacity: .7; }
      </style>
      <figure>
        <img part="img" alt="">
        <figcaption><slot></slot></figcaption>
      </figure>
    `
    this.img = root.querySelector('img')
    this.update()
  }

  attributeChangedCallback() { this.update?.() }

  update() {
    if (this.img) {
      this.img.src = this.getAttribute('src') ?? ''
      this.img.alt = this.getAttribute('caption') ?? ''
    }
  }
}
customElements.define('image-figure', ImageFigure)
```

```html
<template id="image-figure-tpl">
  <style>
    :host { display: block; }
    ::part(img) { width: 100%; height: auto; display: block; border-radius: .5rem; }
    ::part(caption) { font: 14px/1.5 system-ui; opacity: .7; }
  </style>
</template>

<image-figure src="cat.jpg" caption="Mona, the office cat">
  Slot content: arbitrary author fallback text.
</image-figure>
```

Declarative Shadow DOM (Chrome 90+/Edge 90+/Safari 16.4+) renders the
shadow tree from HTML on first paint — server-rendered components
work without the JS having executed yet.

### 11. Form validation: declarative + custom

```javascript
const input = document.querySelector('input[name=email]')

input.addEventListener('invalid', (e) => {
  if (input.validity.typeMismatch) {
    input.setCustomValidity('Please enter a valid email address.')
  }
  if (input.validity.valueMissing) {
    input.setCustomValidity('This field is required.')
  }
})

input.addEventListener('input', () => input.setCustomValidity(''))
```

The browser does the rest — `:user-invalid` styling, the error
message in the constraint-violation popover, and form submission
blocking are all native.

### 12. Smooth `<details>` content animation (full pattern)

```html
<style>
  details { border: 1px solid #eee; border-radius: .5rem; overflow: hidden; }
  summary { padding: 1rem; cursor: pointer; font-weight: 600;
            background: #fafafa; }
  details .panel {
    display: grid;
    grid-template-rows: 0fr;
    transition: grid-template-rows 280ms cubic-bezier(.2,.8,.2,1),
                padding 280ms;
    overflow: hidden;
    padding: 0 1rem;
  }
  details[open] .panel { grid-template-rows: 1fr; padding: 1rem; }
  .panel > div { min-height: 0; }
</style>

<details>
  <summary>Section A</summary>
  <div class="panel"><div>
    <p>Animatable content goes here. Open/close smoothly.</p>
  </div></div>
</details>
```

### 13. Native modal stack with Popover API + View Transition

```html
<button popovertarget="m1" popovertargetaction="show">Open modal</button>

<div id="m1" popover="auto"
     style="view-transition-name: modal-1;
            border: 0; border-radius: .75rem; padding: 0;
            max-width: 480px;">
  <header><h3>Modal 1</h3></header>
  <p>Body — opens with a View Transition morph from the trigger button.</p>
  <button popovertarget="m1" popovertargetaction="hide">Close</button>
</div>
```

```css
button[popovertarget="m1"] { view-transition-name: modal-1; }

::view-transition-old(modal-1),
::view-transition-new(modal-1) {
  animation-duration: 240ms;
  animation-timing-function: cubic-bezier(.2,.8,.2,1);
}
```

Pairs with the `web-animations-api` skill — triggers → modal morph
via View Transitions.

### 14. Reading progress with `<progress>` and CSS

```html
<progress id="read" max="100" value="0"
          style="position:fixed;top:0;left:0;right:0;height:4px;border:0"></progress>

<article>…</article>

<script>
  const progress = document.getElementById('read')
  const article = document.querySelector('article')
  new ResizeObserver(check).observe(article)
  window.addEventListener('scroll', check, { passive: true })
  function check() {
    const rect = article.getBoundingClientRect()
    const total = article.offsetHeight - window.innerHeight
    const scrolled = -rect.top
    progress.value = Math.max(0, Math.min(100, scrolled / total * 100))
  }
</script>
```

### 15. Tab UI with full keyboard support, no JS

```html
<style>
  .tabs > input[type=radio] { position: absolute; opacity: 0; }
  .tabs > input + label { padding: 1rem 2rem; cursor: pointer; }
  .tabs > div { display: none; padding: 2rem; }
  .tabs > input:checked + label { color: var(--accent); }
  .tabs > input:checked + label + div { display: block; }
</style>

<div class="tabs">
  <input id="t1" type="radio" name="t" checked>
  <label for="t1">Tab 1</label>
  <div>Tab 1 content</div>

  <input id="t2" type="radio" name="t">
  <label for="t2">Tab 2</label>
  <div>Tab 2 content</div>
</div>
```

Uses radio buttons as the state, checked siblings as the reveal.
Native keyboard support; no JS required.

---

## Integration Patterns

### 1. With HTMX — a beautiful, no-framework site

The canonical "no-framework" stack:

```html
<link rel="stylesheet" href="/styles.css">
<script src="https://cdn.jsdelivr.net/npm/htmx.org@2.0.4/dist/htmx.min.js"
        defer></script>
<script type="module" src="/app.js"></script>

<body hx-boost="true" hx-ext="view-transition"
      hx-target="#main" hx-swap="innerHTML show:window:top">

  <header><h1>The Site</h1></header>

  <main id="main" hx-get="/pages/home" hx-trigger="load"
        hx-swap="innerHTML">
    <!-- initial server-rendered fragment -->
  </main>

  <footer>…</footer>
</body>
```

CSS handles layout, transitions, responsive design; HTMX handles
navigation; `<dialog>` and Popover handle modals; WAAPI handles
motion.

### 2. With Web Animations API

Drive `<dialog>` and Popover open/close with WAAPI (or pair with
View Transitions for snap morph):

```javascript
const dlg = document.getElementById('m1')
dlg.addEventListener('open', () => {
  dlg.animate(
    [{ opacity: 0, transform: 'translateY(40px) scale(.97)' },
     { opacity: 1, transform: 'none' }],
    { duration: 240, easing: 'cubic-bezier(.2,.8,.2,1)', fill: 'backwards' }
  )
})
dlg.addEventListener('close', () => {
  dlg.animate(
    [{ transform: 'none' }, { opacity: 0, transform: 'translateY(20px) scale(.97)' }],
    { duration: 160, fill: 'forwards' }
  )
})
```

### 3. State machines from CSS

CSS-only component state without JavaScript:

```css
/* Toggle via .list :checked */
.list { display: grid; gap: 1rem; padding: 0; }
.list > li { list-style: none; }

/* The "open" state — pair with <details> or :checked */
.list[data-open] > li[hidden] { display: list-item; }

.list { container-type: inline-size; }
@container (min-width: 600px) {
  .list { grid-template-columns: 1fr 1fr; }
}
@container (min-width: 900px) {
  .list { grid-template-columns: repeat(3, 1fr); }
}
```

### 4. Cards / layouts

```html
<style>
  .grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(min(320px, 100%), 1fr));
    gap: clamp(1rem, 2vw, 1.5rem);
  }
  .card {
    container-type: inline-size;
    border: 1px solid #eee;
    border-radius: .75rem;
    padding: clamp(1rem, 2vw, 2rem);
    background: var(--surface);
  }
</style>
<div class="grid">
  <div class="card">…</div>
</div>
```

The card itself uses container queries for its internal layout;
the grid auto-fits to its parent's width.

### 5. Forms with progressive enhancement

```html
<form action="/api/contact" method="post"
      hx-post="/api/contact" hx-swap="innerHTML" hx-target="#status"
      novalidate>
  …fields…
  <button>Send</button>
</form>
<div id="status" aria-live="polite"></div>
```

The browser hits the URL even if HTMX isn't loaded — the form
gracefully degrades. `aria-live="polite"` announces the response.

### 6. Theme tokens

```css
:root {
  --bg: light-dark(#fafafa, #0b0f12);
  --fg: light-dark(#1a1a1a, #f1f1f1);
  --accent: light-dark(#06b6d4, #22d3ee);
  --surface: light-dark(#fff, #131a20);
  --line: light-dark(#eee, #1f2630);
  --radius: .5rem;
  --shadow: light-dark(0 1px 2px rgba(0,0,0,.05), 0 1px 2px rgba(0,0,0,.4));
}

@layer base {
  body { background: var(--bg); color: var(--fg); }
}

@layer components {
  button { border-radius: var(--radius); }
  .card { box-shadow: var(--shadow); }
}
```

Use `@layer` to manage cascade layers; use `light-dark(...)` to
cleanly express light/dark pairs (Chrome 123+).

---

## Configuration Knobs Worth Knowing

### 1. `<dialog>` attributes

| Attribute | Effect |
|---|---|
| `open` | Open on initial render |
| `closedby="closerequest"` (Chrome 130+) | Browser handles ESC + click-outside close |
| `closedby="any" \| "none"` | Other behaviours |

### 2. Popover API attributes

| Attribute | Effect |
|---|---|
| `popover="auto"` | Light-dismiss (click outside / ESC) |
| `popover="manual"` | Must call `hidePopover()` to close |
| `popovertarget="<id>"` | Declarative button → popover target |
| `popovertargetaction="show\|hide\|toggle"` | Behavior |
| `popover` (browser-default style) | `inset: 0; margin: auto; …` (overridable) |

### 3. `inert` and `disable`

```html
<div inert aria-hidden="true">…</div>
<form disabled>…</form>
<fieldset disabled>
  <legend>Section</legend>
  <input> <input> <input>
</fieldset>
```

`inert` removes a subtree from tab order and accessibility tree —
perfect for modals and off-canvas menus.

### 4. `tabindex` reachability

```html
<div aria-hidden="true" tabindex="-1">…</div>
<input tabindex="0">
```

`tabindex="-1"` is non-tabbable but JS-focusable; `tabindex="0"`
makes a non-focusable element focusable.

### 5. Popover and `<dialog>` interaction

A `<dialog popover>` (Chrome 124+) combines the two: it gets the
light-dismiss and stacking of Popover with the modal/top-layer
behaviour of `<dialog>`.

### 6. `:focus-visible` everywhere

```css
button:focus { outline: 0; }    /* a11y faux pas */
button:focus-visible {          /* only on keyboard focus */
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}
```

---

## Performance & UX

1. **Use `<datalist>` for combobox** — replaces light JS autocomplete
   while staying progressive.
2. **Build pure-CSS layouts first; container queries make it easy.**
   Reach for JS only when you can't help it.
3. **Use `popover` for transient UI** — it's free top-layer
   stacking, focus management, and light-dismiss.
4. **Drive Web Animations API** for `<dialog>` and Popover
   lifecycle — animations can call `cancel()` on close for a
   smooth reverse.
5. **`view-transition-name` is the snapshot key** — name your
   elements deliberately; don't reuse names for distinct morphs.
6. **`<details>` with `name=` attribute** — exclusive accordions
   without a JS container.
7. **Use `:has()` for relational selectors** — replaces most
   `.parent--has-child-X` style hooks.
8. **`container-type: inline-size`** on every reusable component —
   gives component-level responsiveness for free.
9. **`field-sizing: content`** on text inputs — saves dozens of
   layout classes.
10. **Custom validation via `setCustomValidity`** — keep form errors
    declarative; never branch in JS to "validate this".

---

## Common Pitfalls

1. **`<dialog>` `closedby` escapes closedby attribute** — older
   browsers ignore; manually bind `keydown` + click-outside.
2. **Popover inside `<dialog>`** — `:top-layer` placement behaves
   inconsistently; verify in target browsers.
3. **`:has()` blowing up specificity** — wrap in `:where()` to keep
   it at zero specificity.
4. **CSS scroll-driven animations not animating** — `@supports
   (animation-timeline: view())` is missing or scoped wrong.
5. **Container query ancestors** — every `@container` ancestor must
   have `container-type` declared; without it, `:has()` falls back
   to viewport queries.
6. **`<details>` open transition** — height: auto can't transition.
   Use the `grid-template-rows: 0fr / 1fr` trick or
   `transition-behavior: allow-discrete`.
7. **`popover` not closing** — light-dismiss requires a click
   *outside* the popover. `popovertargetaction="hide"` is for
   buttons; click-outside is the popup's own behaviour.
8. **`<input type=file>` security** — never pre-populate `.value`.
9. **`<select>` styled with `appearance: none`** — screen readers
   sometimes miss the role. Don't strip the role; only style the
   chrome.
10. **Shadow DOM event retargeting** — events from inside a shadow
    root surface as if they came from the custom element. Use
    `e.composedPath()` for the original source.

---

## Quick Recipes

### "Submit a form and show a toast with no JS"

```html
<form action="/api/echo" method="post"
      hx-post="/api/echo" hx-swap="innerHTML" hx-target="#status">
  <input name="msg" required>
  <button>Send</button>
</form>

<dialog id="toast" popover="auto" class="toast"
        style="border:0;border-radius:.5rem;padding:1rem;color:white;background:#22c55e;inset:auto 0 1rem auto;max-width:300px">
  Sent!
</dialog>
```

After a 200 response, fire `document.getElementById('toast')
.showPopover()` in `hx-on::after-request`.

### "Tab strip with native keyboard"

See the `[input[type=radio] + label + div]` pattern earlier — full
keyboard support with arrow keys, no JS.

### "Modal with customisable animation"

```html
<dialog id="m1">
  <h3>Title</h3>
  <p>…</p>
  <form method="dialog"><button>Close</button></form>
</dialog>

<style>
  @starting-style {
    dialog[open] { opacity: 0; transform: scale(.97); }
  }
  dialog {
    opacity: 1;
    transform: none;
    transition: opacity 220ms, transform 220ms,
                overlay 220ms allow-discrete;
  }
</style>
```

### "Toggleable settings panel"

```html
<input id="settings-toggle" type="checkbox" class="toggle"
       style="position:absolute;opacity:0">
<label for="settings-toggle"
       style="view-transition-name: settings-panel">⚙</label>
<section class="settings-panel"
         style="view-transition-name: settings-panel"
         hidden>…</section>

<style>
  #settings-toggle:checked + * + .settings-panel { display: block; }
  .toggle:checked + [popovertarget] { /* works for some browsers */ }
</style>
```

Pair with View Transitions for a settings gear → panel morph.

### "Search with native datalist"

```html
<input type="search" name="q" list="browsers"
       hx-get="/api/search" hx-trigger="input delay:200ms"
       hx-target="#results">
<datalist id="browsers">
  <option>Chrome</option>
  <option>Edge</option>
  <option>Firefox</option>
  <option>Safari</option>
</datalist>
```

Combines native autosuggest + HTMX fetch.

### "Inline dropdown using details+summary"

```html
<details class="dropdown">
  <summary>Actions</summary>
  <ul role="menu">
    <li><a hx-get="/api/edit" hx-target="#main">Edit</a></li>
    <li><a hx-get="/api/duplicate" hx-target="#main">Duplicate</a></li>
    <li><a hx-delete="/api/archive" hx-confirm="Archive?">Archive</a></li>
  </ul>
</details>

<style>
  .dropdown[open] > ul { display: block; }
  .dropdown > ul { display: none; padding: .5rem 0; }
</style>
```

The browser handles open/close, keyboard, and outside-click — you
handle the menu.

---

## Resources

### Scripts (in this skill)
- `form_generator.py` — generate accessible input markup that
  pairs with the right `autocomplete` token for the field name.
- `popover_pairs.py` — generate `popovertarget`/`popover` pairs for
  any list of (button text, target id) tuples.

### References (in this skill)
- `popover_api.md` — full Popover API reference with `auto` /
  `manual`, declarative vs imperative, light-dismiss behaviour.
- `dialog_api.md` — full `<dialog>` reference including
  `closedby`, focus-trap, form-mode, returnValue.
- `container_queries.md` — every `container-type`, `container-name`,
  `@container`, `@container-style`, and `container-query-units`
  keyword with examples.
- `css_nesting_layers.md` — `@layer`, nesting `&`, modern CSS
  module structure.

### Assets (in this skill)
- `assets/starter/` — single-file demo of modal + popover +
  details + form + container queries — every primitive in one
  page.
- `assets/components/` — a small Web Component library:
  `<image-figure>`, `<tabs>`, `<theme-toggle>`, `<count-up>`.

---

## Related Skills

- `htmx` — the *server-side* half. Pair every form with `hx-post`
  and every `<dialog>` open with a `hx-get` to render content.
- `web-animations-api` — animate `<dialog>` open/close, Popover
  transitions, and scroll-bound timelines.
- `gsap-scrolltrigger` — when CSS scroll-driven animations aren't
  enough.
- `motion-framer` — when you're in React and want the declarative
  `motion.div` API.
- `modern-web-design` — accessibility rules (INP, contrast, touch
  targets) above this skill.
- `barba-js` — alternative to View Transitions + HTMX for sites
  with heavy page transitions.

---

## Audit Notes

- Built 2026-09-23 as the third leg of the no-framework stack
  (`htmx` + `web-animations-api` + this skill).
- Each primitive has a feature-detection snippet.
- Common pitfalls are tagged by primitive to keep the section
  useful during debugging.
- `starter/index.html` is a one-page demo of every primitive in
  the skill — useful as a smoke test.
- All CSS examples use modern syntax (nesting, container queries,
  `:has()`, color-mix) with fallbacks where needed.
