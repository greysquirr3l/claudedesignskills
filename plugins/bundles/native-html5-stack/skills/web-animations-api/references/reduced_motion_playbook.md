# Reduced Motion Playbook

A practical guide to honouring the user's motion preference across
the three primitives in this skill — without losing the "wow"
factor.

## The first principle

> Reduce motion ≠ remove all motion.
>
> Users with `prefers-reduced-motion: reduce` don't want a static
> page — they want **intentional** motion. Translate 50-pixel
> parallax into 4-pixel translation; replace bouncy springs with
> smooth fades; preserve clarity over surprise.

## What to gate, and how

### CSS scroll-driven animations — gate at the rule level

```css
@supports (animation-timeline: view()) {
  .reveal {
    animation: reveal-up linear both;
    animation-timeline: view();
    animation-range: entry 0% cover 50%;
  }
}

@media (prefers-reduced-motion: reduce) {
  .reveal { animation: none !important; }
}
```

If the user prefers reduced motion, the animation never starts —
the page is just visible. No JS needed.

### View Transitions — gate the pseudo-elements

```css
@media (prefers-reduced-motion: reduce) {
  ::view-transition-old(*),
  ::view-transition-new(*),
  ::view-transition-group(*) {
    animation: none !important;
  }
}
```

Or wrap keyframes in a media query:

```css
::view-transition-old(root), ::view-transition-new(root) {
  /* only define these if motion is OK */
}
@media (prefers-reduced-motion: no-preference) {
  ::view-transition-old(root), ::view-transition-new(root) {
    animation-duration: 280ms;
    animation-timing-function: cubic-bezier(.2, .8, .2, 1);
  }
}
```

### WAAPI — gate inside the JS

```javascript
const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches

function animate_(el, keyframes, opts) {
  if (reduced) {
    const last = keyframes[keyframes.length - 1]
    for (const k in last) el.style[k] = last[k]
    return null
  }
  return el.animate(keyframes, opts)
}

// Optional: react to a user toggling the preference mid-session
matchMedia('(prefers-reduced-motion: reduce)')
  .addEventListener('change', () => {
    document.getAnimations().forEach((a) => a.cancel())
  })
```

## What to keep vs what to remove

| Primitive | Reduced-motion replacement |
|---|---|
| Scroll-driven reveal | Plain opacity transition with `transitionend` IntersectionObserver |
| Spring-easing WAAPI | Linear ease-out (`cubic-bezier(0, 0, .2, 1)`); shorter duration |
| Hover lift `translateY(-8px)` | `translateY(-2px)` or no offset |
| Parallax scroll | Static positioning with `position: relative` |
| Marquee | Static flex layout, no infinite animation |
| WAAPI counter | `requestAnimationFrame` with linear interpolation |
| Cross-document VT | Same `view-transition-name` morphs but at `animation-duration: 0ms` |
| Modal WAAPI open | `transition: opacity 100ms, transform 100ms` with reduced distance |

The table's row-by-row design lets you preserve **clarity** (the
modal still visually becomes open; the counter still moves; the
parallax still exists at zero-amplitude) while removing
**disorientation** (overshoots, large translates, infinite loops).

## When NOT to gate

A few patterns stay even with reduced motion on — mostly because
they communicate state, not decoration:

- **`<details>` open / close** — accessibility-critical, not
  decorative.
- **`prefers-reduced-motion-transparency`** — separate CSS hook
  (not yet broadly supported).
- **Page navigation** — keeping the user oriented through a route
  change is more important than removing the transition; just
  shorten the duration to ~80ms so it's a blink, not a flourish.
- **Loading indicators** — a spinner is motion-as-feedback, not
  decoration.
- **Auto-playing carousel transitions** — actually, do gate these.
  Anything that the user didn't request should respect reduce.

## Accessibility-aware variant library functions

```javascript
// Generic — supports any el + any keyframes
function safeAnimate(el, keyframes, opts = {}) {
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) {
    const last = keyframes[keyframes.length - 1]
    for (const k in last) el.style[k] = last[k]
    return null
  }
  return el.animate(keyframes, opts)
}

function safeViewTransition(updateDOM) {
  if (!document.startViewTransition) return Promise.resolve()
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches
  if (reduced) {
    updateDOM()
    return Promise.resolve()
  }
  return document.startViewTransition(updateDOM).finished
}
```

## Why CSS-level gating is best

CSS `animation: none` is fast (browser skips compositing), `pointer-
events` are not affected (clicks work normally), and `prefers-
reduced-motion` is a fully declarative media query. Reach for the
JS gate only when you need to set inline end states.

## Cursor over movement

If you have spring-like hover lifts, replace them with a cursor
*highlight* the user can see without motion. A subtle shadow change
(`box-shadow: 0 4px 8px rgba(0,0,0,.1)`) reads as a "press" cue
without bouncing.

## Reduced motion also affects other prefs

- `prefers-color-scheme: dark` — give your motion-replaced fallback
  variants a dark variant.
- `prefers-reduced-data: reduce` — drop fancy background videos
  even when motion is allowed.
- `forced-colors: active` — same dark-data variant.

## Useful testing toggles

```javascript
// In dev only — flip reduced motion
window.toggleReduceMotion = () => {
  const mql = matchMedia('(prefers-reduced-motion: reduce)')
  // (The browser API doesn't let you mutate media-query results
  //  — use Chrome DevTools > Rendering > Emulate prefers-reduced-motion)
}
```

In Chrome DevTools: **More Tools → Rendering → Emulate CSS media
feature `prefers-reduced-motion`**.

## Cross-references

- [MDN — prefers-reduced-motion](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion)
- [WCAG 2.1 — Animation from Interactions (2.3.3)](https://www.w3.org/WAI/WCAG21/Understanding/animation-from-interactions.html)
- [Inclusive Components — Heydon Pickering](https://inclusive-components.design/) (chapter on toggletips)
- [web.dev — Accessible motion preferences](https://web.dev/articles/prefers-reduced-motion)
