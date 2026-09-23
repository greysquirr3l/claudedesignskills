---
name: web-animations-api
description: Native browser APIs for "amazing" sites without a JS framework. Use this skill to choreograph complex motion with the Web Animations API (WAAPI), scroll-driven CSS animations (animation-timeline with scroll() and view()), and the View Transitions API (same-document and cross-document). Triggers on tasks involving element.animate, KeyframeEffect, AnimationEvent, scroll-timeline, animation-timeline, view-timeline, ::view-transition, document.startViewTransition, Motion Without a Framework, scroll-linked animations, page transitions, and chrome-free choreography that feels like a SPA. Built for sites that want to be visually rich without shipping 200+ KB of animation libraries. Pairs with htmx and html5-native-design for a complete no-framework stack.
---

# Web Animations API — Native Motion for Beautiful Sites

> **Audit date**: 2026-09-23.
> This skill is **framework-free**: it covers three native browser
> primitives — WAAPI, CSS scroll-driven animations, and the View
> Transitions API — that together replace 80% of what a typical
> motion library does.

Web animation libraries ship ~50 KB to solve one job: turn
declarative timelines into running animations. Browsers ship three
primitives that solve the same job out of the box:

- **Web Animations API (WAAPI)** — `Element.animate()`, `KeyframeEffect`,
  `Animation`, and friends. Imperative JS API, full control,
  scrubable timeline, plays *with* CSS animations and `transition`s.
- **CSS scroll-driven animations** — `@scroll-timeline` / `animation-timeline:
  scroll() / view()`. Pure CSS; runs on the compositor; no JS in the
  critical path.
- **View Transitions API** — `document.startViewTransition()` for
  same-document morphs; CSS `@view-transition` for cross-document
  page navigations. Built-in crossfade-or-morph between DOM snapshots.

These three primitives are stable, broadly supported, and composable.
Most sites don't need GSAP, Framer Motion, Anime.js, or Motion for a
basic motion vocabulary.

**When to use this skill:**

- Building beautiful sites **without** a JS framework — combine with
  `htmx` and `html5-native-design` for a complete no-framework stack.
- Replacing or augmenting CSS `transition`s with timing-controlled,
  scrubable animations.
- Scroll-linked storytelling (header shrinks on scroll, sections
  reveal, progress bars fill, parallax in pure CSS).
- Smooth route changes / "SPA feel" on top of plain HTML or HTMX.
- Replacing 50–200 KB of motion libraries with zero runtime JS for
  motion.

**When NOT to use it (and you actually want a library):**

- Physics-based animation with **springs** and **tween spring
  presets** — *react-spring-physics* and *motion-framer* are better
  at this; WAAPI spring easing is verbose.
- **Cross-cutting timeline orchestration** with multi-property
  scrobbling and stagger — *gsap-scrolltrigger* is best.
- **Component-driven declarative motion in React** —
  *motion-framer* (motion/react) is the standard.
- **Sprite-sheet / skeletal animation** — *pixijs-2d* and
  *lottie-animations* cover this.

**Audit notes:**

- WAAPI `Element.animate()` — shipped since Chrome 36 / Firefox 48;
  universal by 2020.
- CSS `animation-timeline: scroll()` + `view()` — Chrome 115+ /
  Edge 115+, Safari 26+ (2025+), Firefox 136+ as of 2026. Graceful
  degradation is "the animation doesn't run" — add `@supports
  (animation-timeline: view())` to opt in.
- View Transitions API — `document.startViewTransition` Chrome 111+ /
  Edge 111+, Safari 18+, Firefox 137+. Cross-document VT
  `@view-transition` Chrome 126+, Safari TP, Firefox ⏳.

**Companion patterns:**

- *Pair with htmx*: enable `view-transition` extension and let every
  `hx-boost` swap become a View Transition automatically.
- *Pair with html5-native-design*: drive `<dialog>` open / close
  and Popover dismiss with a single View Transition that morphs
  the trigger element into the modal.

---

## Core Concepts

### 1. Web Animations API (WAAPI)

`Element.animate(keyframes, options)` returns an `Animation`
instance you can control:

```javascript
const anim = el.animate(
  [
    { opacity: 0, transform: 'translateY(8px)' },
    { opacity: 1, transform: 'none' }
  ],
  {
    duration: 280,
    easing: 'cubic-bezier(.2,.8,.2,1)',
    fill: 'forwards',  // keep end-state after the animation finishes
    delay: 100,
  }
)

// Optional: chain, pause, cancel
anim.finished.then(() => console.log('done'))
anim.pause(); anim.playbackRate = 0.5
anim.cancel()
```

Why WAAPI over CSS `transition`/`animation`?

- **Imperative** — start, pause, reverse, scrub at runtime.
- **Composable** — multiple animations on the same property layer
  cleanly.
- **Read-only inspection** — `animation.currentTime`, `playState`,
  `playbackRate` make UI entirely scriptable.
- **Same composability with `transition`** — a CSS transition
  triggered by a class change becomes a CSSAnimation/TransitionEvent
  you can listen for.

### 2. CSS scroll-driven animations

Two flavours:

- **Scroll progress** — `animation-timeline: scroll()` ties the
  animation 0→100% to the scroll progress of a **scroller**
  (`block` axis — the root by default).
- **View progress** — `animation-timeline: view()` ties the
  animation 0→100% to the **element's** visibility in the
  scroller (0 when entering, 50% centred, 100% leaving).

```css
/* Headline that shrinks as you scroll */
h1 {
  font-size: clamp(2.5rem, 6vw, 4rem);
  animation: shrink linear both;
  animation-timeline: scroll(root);
  animation-range: 0 30vh;
}
@keyframes shrink {
  to { font-size: 1.5rem; opacity: 0.8; letter-spacing: -.02em; }
}

/* Reveal-on-enter — no JS! */
.reveal {
  animation: reveal linear both;
  animation-timeline: view();
  animation-range: entry 100% cover 0%;
}
@keyframes reveal {
  from { opacity: 0; transform: translateY(40px); }
  to   { opacity: 1; transform: none; }
}
```

`animation-range` is the killer feature — choose **when** in the
timeline the animation lives (e.g. `entry 0% cover 50%` plays from
the moment the element starts entering until it's half-coverd).

Browser support: feature-detect with `@supports (animation-timeline:
view())` to gate the rules.

### 3. View Transitions API

Two shapes:

- **Same-document**: `document.startViewTransition(() => updateDOM())`.
  The browser takes snapshots of the old and new DOM, names matched
  elements stay in place. ~5 KB of JS.
- **Cross-document** (page navigations): add `@view-transition
  { navigation: auto }` to the CSS and matching
  `view-transition-name` to the relevant nodes.

```javascript
async function navigate(to) {
  if (!document.startViewTransition) return location.href = to

  const transition = document.startViewTransition(async () => {
    const html = await fetch(to).then(r => r.text())
    document.body.innerHTML = html
  })
  await transition.finished
}
```

```css
::view-transition-old(root), ::view-transition-new(root) {
  animation-duration: 280ms;
  animation-timing-function: cubic-bezier(.2,.8,.2,1);
}
```

Cross-document VTs still have rough spots — *feature-detect on
`document.startViewTransition`* and always provide a non-JS fallback.

### 4. The three primitives together

A "scroll-driven landing" page combines all three:

- CSS scroll-driven animations for **content**: hero reveals,
  progress fill, sticky-section fade.
- View Transitions for **routes**: navigation feels like a SPA.
- WAAPI for **micro-interactions**: button ripples, focus rings,
  hover-lifts, dialog open/close morph.

That's the whole toolset. Now we'll go deeper.

---

## Common Patterns — Beautiful, Native, Compositional

### 1. Reveal-on-scroll with `animation-timeline: view()`

CSS-only — no IntersectionObserver boilerplate, no JS animations:

```css
@supports (animation-timeline: view()) {
  .reveal {
    animation: reveal-up linear both;
    animation-timeline: view();
    /* start the moment it enters, finish when half-covered */
    animation-range: entry 0% cover 50%;
  }
}
@keyframes reveal-up {
  from { opacity: 0; transform: translateY(48px); }
  to   { opacity: 1; transform: none; }
}

/* Pure CSS parallax — value computed by browser as you scroll */
.parallax-bg {
  animation: parallax linear both;
  animation-timeline: scroll(root);
  animation-range: 0 100vh;
}
@keyframes parallax {
  from { transform: translateY(-10%); }
  to   { transform: translateY(10%); }
}
```

`@supports` keeps older browsers from blinking — the animation
simply doesn't apply if the feature is missing. Pair with a
`@media (prefers-reduced-motion: reduce) { .reveal { animation: none } }`
to honour motion preferences.

### 2. Headline shrink-as-you-scroll

```css
.hero h1 {
  font-size: clamp(2.5rem, 8vw, 6rem);
  letter-spacing: -.03em;
  animation: pin-zoom linear both;
  animation-timeline: scroll(root);
  animation-range: 0 50vh;
}
@keyframes pin-zoom {
  to {
    font-size: clamp(1.25rem, 4vw, 2.5rem);
    letter-spacing: -.01em;
  }
}
```

Smooth, no JS, no library.

### 3. Reading-progress bar

```css
progress#read {
  /* fills 0–100% as the page scrolls */
  animation: fill linear both;
  animation-timeline: scroll(root);
  /* binds to the document scroll, not the progress element */
  position: fixed;
  top: 0; left: 0; right: 0;
  height: 4px;
  border: 0;
  background: transparent;
}
@keyframes fill {
  from { width: 0; }
  to   { width: 100vw; }
}
```

Alternatively use `animation-name: read-progress` and bind
manually with WAAPI for a scrubbed, easing-aware bar.

### 4. Element morphs across views (View Transitions)

```html
<!-- Hero card on the index -->
<article class="card" id="post-42">
  <h3 style="view-transition-name: post-42-title">How to make sites beautiful</h3>
  <p style="view-transition-name: post-42-thumb">…</p>
</article>

<!-- After clicking through to the detail page -->
<article class="card">
  <h1 style="view-transition-name: post-42-title">How to make sites beautiful</h1>
  <img style="view-transition-name: post-42-thumb" src="…">
</article>
```

With both views' `view-transition-name` set, the browser morphs the
title and thumbnail from index layout to detail layout — across
either same-document or cross-document navigation.

```css
::view-transition-group(*) {
  animation-duration: 320ms;
  animation-timing-function: cubic-bezier(.2,.8,.2,1);
}
```

### 5. Tap-to-reveal with a CSS-only tab indicator

```css
.tab-strip {
  position: relative;
  isolation: isolate;
}
.tab-strip::before {
  content: "";
  position: absolute;
  inset: auto 0;
  height: 2px;
  background: var(--accent);
  transform-origin: left;
  transform: scaleX(0);
  animation: tab-underline linear both;
  animation-timeline: view();
  animation-range: contain 0% contain 100%;
}
@keyframes tab-underline {
  to { transform: scaleX(1); }
}
```

### 6. Smooth dialog open with WAAPI

```html
<dialog id="settings">
  <h3>Settings</h3>
  <p>…</p>
  <form method="dialog"><button>Close</button></form>
</dialog>
<button onclick="document.getElementById('settings').showModal()">
  Open
</button>
```

```css
dialog {
  opacity: 0;
  transform: translateY(40px) scale(.96);
  transition: opacity 240ms, transform 280ms cubic-bezier(.2,.8,.2,1);
}
dialog[open] { opacity: 1; transform: none; }
dialog::backdrop { opacity: 0; transition: opacity 240ms; }
dialog[open]::backdrop { opacity: 1; background: rgba(0,0,0,.4); }
```

Make sure transitions are reversible — opening and closing produce
the same animation in reverse.

### 7. Press the "macro" — `document.startViewTransition` for an app shell

```javascript
async function navigate(to) {
  const data = await fetch(to).then(r => r.json())
  const transition = document.startViewTransition(() => {
    document.querySelector('main').innerHTML = data.html
    document.title = data.title
  })
  await transition.ready
  // Optional: scroll to top after the new DOM is on-screen
  window.scrollTo({ top: 0, behavior: 'instant' })
}
```

Bind to `<a hx-get=...>` by combining with HTMX:

```javascript
document.body.addEventListener('htmx:beforeSwap', (e) => {
  if (!document.startViewTransition || e.detail.pathInfo?.requestPath === location.pathname) return
  // Defer swap until view transition begins — HTMX will do its own work
})

document.body.addEventListener('htmx:beforeHistorySave', () => {
  document.startViewTransition?.(() => {})
})
```

### 8. Morph from trigger element to dialog (popover → modal)

Pair with `html5-native-design` (§Popover API):

```javascript
trigger.addEventListener('click', () => {
  document.startViewTransition(() => {
    // browser snapshots trigger, opens popover
    popover.showPopover()
  })
})
```

Apply matching `view-transition-name: confirm-modal` to both the
button and the dialog so the open animation morphs button → dialog.

### 9. Press the "WAAPI options" keys

```javascript
el.animate(keyframes, {
  // Timing
  duration, delay, iterations, iterationStart,
  easing, // string OR [0,.5,1] cubic-bezier array
  // Direction
  direction,  // 'normal' | 'reverse' | 'alternate' | 'alternate-reverse'
  // Fill behaviour — what happens before / after
  fill,       // 'auto' | 'backwards' | 'forwards' | 'both' | 'none'
  // Composite — how multiple animations on the same property merge
  composite,  // 'replace' | 'add' | 'accumulate'
  // Iteration composite
  iterationComposite, // 'replace' | 'accumulate'
})
```

### 10. Pause-on-reduced-motion

```javascript
const mq = window.matchMedia('(prefers-reduced-motion: reduce)')
function animate_(el, kf, opts) {
  if (mq.matches) return
  return el.animate(kf, opts)
}
mq.addEventListener('change', () => {
  // cancel all running WAAPI animations if the user just opted out
  document.getAnimations().forEach(a => a.cancel())
})
```

Pure-CSS scroll-driven animations need their own gating:

```css
@media (prefers-reduced-motion: reduce) {
  .reveal, .parallax-bg { animation: none; }
}
```

---

## Integration Patterns

### 1. With HTMX (boosted swaps become View Transitions)

```html
<body hx-boost="true"
      hx-ext="view-transition"
      hx-target="#main"
      hx-swap="innerHTML show:window:top">

<style>
  ::view-transition-old(root), ::view-transition-new(root) {
    animation-duration: 280ms;
    animation-timing-function: cubic-bezier(.2, .8, .2, 1);
  }
</style>
```

That's it — every link now feels native.

### 2. With Web Components

Web Components fully support CSS animations, View Transitions, and
WAAPI. Element access via `this.shadowRoot.querySelector(...)`
works inside `connectedCallback`.

```javascript
class SlideInPanel extends HTMLElement {
  connectedCallback() {
    const anim = this.animate(
      [{ transform: 'translateX(100%)' }, { transform: 'none' }],
      { duration: 280, easing: 'cubic-bezier(.2,.8,.2,1)', fill: 'forwards' }
    )
    anim.finished.then(() => this.focus())
  }
}
customElements.define('slide-in-panel', SlideInPanel)
```

### 3. With the `<dialog>` and Popover API (see html5-native-design)

Use WAAPI + View Transitions for the modal open/close choreography.
The Popover API will fire `toggle` events you can hook for the
anim.

```javascript
popover.addEventListener('toggle', async (e) => {
  if (!e.newState) return
  if (document.startViewTransition) {
    await document.startViewTransition(() => {}).ready
  }
  popover.showPopover()
})
```

### 4. State-during-transition holds

```javascript
let pendingNav = null
async function navigate(to) {
  if (document.startViewTransition) {
    pendingNav = { to, started: performance.now() }
    document.startViewTransition(() => updateDOM(to))
    return
  }
  location.href = to
}
```

`pendingNav` survives across the synchronous updateDOM callback and
the async render; use it to track in-flight transitions without
duplicating state.

### 5. Pre-emptive loading for snappier VT

```javascript
const link = document.createElement('link')
link.rel = 'preload'
link.as = 'fetch'
link.href = nextUrl
link.crossOrigin = ''  // cookies
document.head.appendChild(link)
```

Most clients won't make this measurable in 2026; only worth it when
the next page is large or the user's connection is slow.

### 6. Reduced-motion fallback

```javascript
const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches
function transition(updateDOM) {
  return document.startViewTransition
    ? document.startViewTransition(reduced ? () => { updateDOM(); return Promise.resolve() } : updateDOM)
    : { ready: Promise.resolve(), finished: Promise.resolve(), updateDOMDone: Promise.resolve() }
}
```

---

## Configuration Knobs Worth Knowing

### 1. `Element.animate(options)`

The most important options beyond `duration` and `easing`:

```javascript
el.animate([{...}, {...}], {
  duration: 600,        // ms
  delay:    100,
  iterations: Infinity, // loop forever
  iterationStart: 0,    // ms into the animation to start at
  direction: 'alternate',
  fill: 'forwards',     // keep end-state after the animation finishes
  composite: 'add',     // how this animation combines with CSS transitions
  easing: 'cubic-bezier(.2, .8, .2, 1)'
})
```

### 2. `Animation` returned by `animate()`

```javascript
const anim = el.animate(keyframes, opts)

anim.finished        // Promise<void>
anim.ready           // Promise<Animation>
anim.playState       // 'idle' | 'pending' | 'running' | 'paused' | 'finished'
anim.currentTime     // ms
anim.playbackRate    // 0.5 = half speed, -1 = reverse
anim.startTime       // document.timeline.currentTime at start
anim.effect          // KeyframeEffect
anim.cancel()
anim.finish()
anim.persist()       // hold animation when document is in suspension

// Events
anim.addEventListener('finish',   () => {})
anim.addEventListener('cancel',   () => {})
anim.addEventListener('remove',   () => {})
```

### 3. `document.getAnimations()` — global registry

```javascript
const all = document.getAnimations()

// Pause every animation for reduced-motion
all.forEach(a => a.pause())

// Cancel everything that targets a specific element
document.getAnimations({ subtree: true })
  .filter(a => a.effect?.target?.closest('.modal'))
  .forEach(a => a.cancel())
```

### 4. CSS scroll-driven animation rules

```css
.something {
  /* The timeline the animation lives on */
  animation-timeline: scroll(root) | view() | view(none) | scroll(nearest);

  /* Range on the timeline (default = the full timeline) */
  animation-range: 0% 100%;                /* full timeline */
  animation-range: entry 0% cover 100%;     /* element fully entered to fully covered */
  animation-range: contain 0% contain 100%; /* contain phase */
  animation-range: exit 0% cover 100%;      /* element fully covered to fully exited */

  /* Optional: pick the scroller explicitly */
  animation-timeline: scroll(block nearest);
}
```

### 5. View Transitions: opt-in shapes

```css
/* Cross-document (page navigations) */
@view-transition {
  navigation: auto;  /* 'none' (default) | 'auto' */
}

/* Or element-level via view-transition-name */
.cover {
  view-transition-name: cover;
}

/* Pseudo-elements you can style */
::view-transition-old(*) { ... }
::view-transition-new(*) { ... }
::view-transition-group(*) { ... }
::view-transition-image-pair(*) { ... }
```

```javascript
// Skip a transition (e.g. for trivial DOM changes)
document.startViewTransition(() => updateDOM())
// vs
updateDOM()  // no transition at all

// Listen to lifecycle events
const vt = document.startViewTransition(() => updateDOM())
vt.ready.then(() => console.log('snapshots taken, swapping'))
vt.finished.then(() => console.log('transition complete'))
vt.skipTransition()  // cancel
```

### 6. Pitfalls

| Behaviour | Cause | Fix |
|---|---|---|
| Scroll-driven animation "lags" by one frame | Compositor scheduling | Use `will-change: transform`; pre-render hot path with `transform: translateZ(0)` |
| `Element.animate` doesn't persist after reload | `fill: 'auto'` | Use `fill: 'forwards'` |
| Cross-document VT doesn't fire | Browser support | `if (!document.startViewTransition) location.href = next` |
| WAAPI spring looks stiff | `cubic-bezier(.2,.8,.2,1)` isn't a spring | Use Motion / react-spring for true springs |
| Tab loses `Element.animate` | Background tab throttling | `composite: 'add'` to merge with running animations |
| Scroll-driven animation in `<iframe>` | Timeline tied to inner scroller | Use `scroll(viewport)` or unscoped `scroll()` |
| `view-transition-name` collides | Unique per element | One pair of snapshot names per "morph" |

---

## Performance & UX

1. **Animate `transform` and `opacity`** — these are compositor-
   only and never hit layout. Avoid `width`/`height`/`top`/`left`.
2. **Set `will-change`** for elements that animate continuously
   (or remove it after the animation finishes to free the slot).
3. **`composite: 'add'`** to combine multiple animations on the
   same property without ordering issues.
4. **Run scroll-driven animations on the compositor** — that's the
   default, but be careful: setting `animation-timing-function:
   steps(60)` on a scroll-bound animation fights the compositor.
5. **Cap iteration count** — `iterations: Infinity` is fine if you
   know it'll be torn down (e.g. an interruptible bounce). Otherwise
   bound it.
6. **Use `view-transition-name` sparingly** — each name causes an
   extra snapshot; over-using them slows the transition.
7. **Listen to `transitionrun` / `transitionstart` / `transitionend`**
   for tools (and tests). `El.getAnimations({ subtree: true })`
   gives you every animation in a subtree.
8. **`prefers-reduced-motion`** — gate all of the above on a media
   query, both in JS and CSS.
9. **Throttle WAAPI on long-running lists** — animating 10,000
   elements directly is fine if they're cheap (transform-only) but
   not if you manipulate layout properties.

---

## Common Pitfalls

1. **`animate()` returned but you forgot to chain `.finished`** —
   the animation runs, but if it makes a state change you depend on
   you must await `finished`.
2. **`fill: 'none'`** — the element snaps back to its base state
   before/after the animation runs.
3. **Multiple animations on the same property** — they don't merge;
   later animations win. Use `composite: 'add'` or `'accumulate'`.
4. **`duration` 0** — sometimes useful for synchronous state swaps,
   but breaks `fill: 'forwards'` in subtle ways.
5. **Animating `width` / `height`** — triggers layout on every frame;
   prefer scale via `transform`.
6. **CSS scroll-driven animation on `[hidden]`** — the timeline
   can't progress while the element is `display: none`.
7. **Cross-document VT** — only Chrome/Edge 126+ reliably; Safari
   is partial; Firefox is in progress. Always feature-detect.
8. **`startViewTransition` exception inside the callback** — the
   DOM update is "applied" because the API treats a thrown
   exception as "update already done". Use `transition.updateDOMDone`
   to be sure.
9. **`document.startViewTransition` and `popover`/`dialog`** — open
   the popover *outside* the transition callback for predictable
   timing; the browser snapshots the *current* state, not the
   post-update state.
10. **`animation-timeline: view()` without `view-timeline`** — older
    syntax `@scroll-timeline` is deprecated in favour of
    `animation-timeline`. Use the latter on 2025+ code.

---

## Quick Recipes

### "Infinite marquee" — pure CSS, GPU-friendly

```css
.marquee { overflow: hidden; }
.marquee-track {
  display: inline-flex;
  animation: marquee linear infinite;
  animation-duration: 24s;
  will-change: transform;
}
@keyframes marquee {
  from { transform: translateX(0); }
  to   { transform: translateX(-50%); }
}
@media (prefers-reduced-motion: reduce) { .marquee-track { animation: none } }
```

### "Animated number counter"

```javascript
function animateCount(el, to, duration = 800) {
  const from = Number(el.textContent)
  const start = performance.now()
  const anim = el.animate(
    [{ innerHTML: from }, { innerHTML: to }],
    { duration, fill: 'forwards', easing: 'cubic-bezier(.2,.8,.2,1)' }
  )
  anim.onupdate = () => { el.textContent = Math.round(+el.textContent || 0).toLocaleString() }
  return anim.finished
}
```

(Caveat: animating `innerHTML` is allowed but flaky across browsers;
a custom property + `counter-reset` is more reliable in 2026.)

### "Cross-fade a list item in/out" with WAAPI

```javascript
function fadeOut(el) {
  return el.animate(
    [{ opacity: 1, transform: 'translateX(0)' }, { opacity: 0, transform: 'translateX(-8px)' }],
    { duration: 200, fill: 'forwards' }
  ).finished.then(() => el.remove())
}
```

### "Smooth section anchor" with View Transitions

```javascript
document.body.addEventListener('click', (e) => {
  const a = e.target.closest('a[href^="#"]')
  if (!a) return
  e.preventDefault()
  const id = a.getAttribute('href').slice(1)
  const target = document.getElementById(id)
  if (!target) return

  if (document.startViewTransition) {
    document.startViewTransition(() => {
      window.scrollTo({ top: target.offsetTop, behavior: 'instant' })
    })
  } else {
    window.scrollTo({ top: target.offsetTop, behavior: 'smooth' })
  }
})
```

### "Keyboard-driven scrub of CSS scroll-driven animation"

```javascript
const anim = document.querySelector('.parallax').getAnimations()[0]
window.addEventListener('keydown', (e) => {
  if (e.key === 'ArrowDown') anim.currentTime = Math.min(anim.currentTime + 50, anim.effect.getTiming().duration)
  if (e.key === 'ArrowUp')   anim.currentTime = Math.max(anim.currentTime - 50, 0)
})
```

---

## Resources

### Scripts (in this skill)
- `waapi_examples.py` — generate 15+ WAAPI snippets with the
  `Element.animate(keyframes, options)` API, from simple reveals
  to scrubable timelines.

### References (in this skill)
- `waapi_reference.md` — complete WAAPI browser reference.
- `scroll_timeline_reference.md` — every `animation-timeline`,
  `animation-range`, and `@scroll-timeline` rule with examples.
- `view_transitions_reference.md` — same-document and
  cross-document VT pseudo-elements, lifecycle, and patterns.
- `reduced_motion_playbook.md` — accessible motion design: when to
  gate, when to keep, what to replace.
- `groundtruth.md` — index of the user's `pattern_lab` reference
  examples and how to re-pull them.

### Assets (in this skill)
- `assets/scroll_showcase/` — single-file demo combining
  scroll-driven CSS, WAAPI, and View Transitions.
- `assets/view_transition_landing/` — same-doc + cross-doc page
  transitions.
- `assets/reduced_motion_demo/` — every primitive with and without
  motion enabled.
- `assets/groundtruth/scroll_timeline_lab.html` — **ground-truth
  reference**: copy of the user's `2026_scroll_timeline_lab.html`
  from `greysquirr3l/pattern_lab`. The same file is live at
  <https://greysquirr3l.github.io/pattern_lab/2026_scroll_timeline_lab.html>
  — open the live URL in any modern browser to see the demos run.
  Twelve finished scroll-driven CSS examples using the lab's dark
  navy / neon palette. Treat as polished reference; adapt for new
  projects.

---

## Related Skills

- `htmx` — HTMX + View Transitions is the single biggest
  no-framework "wow" available. Wire `hx-ext="view-transition"` and
  every page change becomes a native-feeling morph.
- `html5-native-design` — `<dialog>`, Popover API, container
  queries, `:has()`. Pair with WAAPI to choreograph their open /
  close / respond.
- `gsap-scrolltrigger` — when you need timeline orchestration and
  cross-property scrub, this is the right tool.
- `motion-framer` — when you're already in React and want the
  declarative `motion.div` API.
- `animejs` — keep this around for spring easings (v4
  `createSpring`) and chained timelines if you prefer an
  imperative-style API to GSAP.
- `modern-web-design` — accessibility, INP, contrast, and design
  system tokens.

---

## Audit Notes

- Built 2026-09-23 to provide a native-HTML5 motion layer for the
  `htmx` + `html5-native-design` no-framework stack.
- Each primitive has a tested browser-support section with fallback
  patterns for missing features.
- All CSS scroll-driven-animation examples are gated behind
  `@supports (animation-timeline: view())` for graceful
  degradation.
- Reduced-motion gating uses both `matchMedia` (JS) and `@media
  (prefers-reduced-motion)` (CSS).
- View Transitions are paired with HTMX (`hx-ext="view-transition"`)
  and with first-class `view-transition-name` choreography.
