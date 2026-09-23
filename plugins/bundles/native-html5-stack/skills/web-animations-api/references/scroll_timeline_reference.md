# CSS Scroll-Driven Animations Reference

Two timeline flavours in CSS — `scroll()` (scroll progress) and
`view()` (element visibility).

## animation-timeline

### Scroll progress — `scroll()`

```css
.progress-bar {
  animation: fill linear both;
  animation-timeline: scroll(root);    /* or scroll() for default scroller */
}

@keyframes fill {
  from { transform: scaleX(0); }
  to   { transform: scaleX(1); }
}
```

| Argument | Notes |
|---|---|
| `scroll()` | Default scroller (= nearest scrollable ancestor) |
| `scroll(root)` | Document / `<html>` scroll |
| `scroll(block nearest)` | Block axis, nearest scroller |
| `scroll(inline self)` | Inline axis, the element itself |

### View progress — `view()`

```css
.reveal {
  animation: rise linear both;
  animation-timeline: view();
  animation-range: entry 0% cover 30%;
}

@keyframes rise {
  from { opacity: 0; transform: translateY(80px); }
  to   { opacity: 1; transform: none; }
}
```

| Argument | Notes |
|---|---|
| `view()` | Default — element vs. nearest scroller |
| `view(block)` | Block axis |
| `view(inline)` | Inline axis |
| `view(none)` | No scroller — uses the document viewport |
| `view(--my-scroller)` | Named scroll container (`scroll-timeline-name`) |

## animation-range

Three "phases" of an element's lifecycle in the scroller's
visibility:

- **Entry**: from first contact with the scroller to fully inside.
- **Cover**: the element is fully inside the scroller.
- **Exit**: from start of leaving to fully gone.

The default range is the full timeline; you can pin any phase with
keyframes:

| Range | Meaning |
|---|---|
| `0% 100%` | The entire timeline (default) |
| `entry 0% cover 100%` | From element starts entering to fully covered |
| `cover 0% exit 100%` | From covered to leaving |
| `entry 0% cover 50%` | First half of the entry phase |
| `entry 100% cover 100%` | The moment of "fully inside" only |
| `cover 0% cover 100%` | The whole cover phase |

```css
/* Play once, when element is 0–50% covered */
.once-once {
  animation: rise linear both;
  animation-timeline: view();
  animation-range: entry 0% cover 50%;
}

/* Sticky parallax: stays "alive" through entry AND exit */
.parallax {
  animation: shift linear both;
  animation-timeline: view();
  animation-range: cover 0% cover 100%;
}
```

## The deprecated `@scroll-timeline` syntax

Older CSS (pre-2024) used `@scroll-timeline` + named timelines:

```css
@scroll-timeline --my-scroll {
  source: scroll(root);
  orientation: block;
}
@view-timeline --my-entry {
  source: auto;
  orientation: block;
}

.something {
  animation: fill linear both;
  animation-timeline: --my-scroll;
}
```

This is now consolidated into `animation-timeline: scroll()` /
`animation-timeline: view()` (the function-valued keywords). The
`@scroll-timeline` / `@view-timeline` at-rule syntax still works in
Chrome/Edge but is being phased out. **Prefer the newer syntax on
new code.**

## Common idioms

### "Parallax without JS"

```css
.parallax-img {
  animation: shift linear both;
  animation-timeline: scroll(root);
}
@keyframes shift {
  from { transform: translateY(-15%); }
  to   { transform: translateY(15%); }
}
```

### "Reading progress bar"

```css
progress { position: fixed; top: 0; left: 0; right: 0; height: 4px;
           border: 0;
           animation: fill linear both;
           animation-timeline: scroll(root);
           animation-range: 0 100%; }
@keyframes fill { from { transform: scaleX(0); } to { transform: scaleX(1); } }
```

### "Hero shrink-pin"

```css
.hero {
  height: 100vh;
  position: sticky;
  top: 0;
}
.hero h1 {
  font-size: clamp(3rem, 12vw, 8rem);
  animation: shrink linear both;
  animation-timeline: scroll(root);
  animation-range: 0 50vh;
}
@keyframes shrink { to { font-size: clamp(1.5rem, 4vw, 2.5rem); } }
```

Pair `position: sticky; top: 0;` with a scroll-bound transform —
the section appears pinned while the page scrolls past.

### "Section-reveal one-by-one on scroll"

```css
.reveal {
  animation: reveal linear both;
  animation-timeline: view();
  animation-range: entry 0% cover 50%;
}
@keyframes reveal {
  from { opacity: 0; transform: translateY(60px); }
  to   { opacity: 1; transform: none; }
}
```

### "Sticky tab indicator"

```css
.tabs::after {
  content: '';
  position: absolute;
  bottom: 0; left: 0;
  height: 2px; width: 100%;
  background: var(--accent);
  transform: scaleX(0);
  transform-origin: left;
  animation: fill linear both;
  animation-timeline: view();
  animation-range: contain 0% contain 100%;
}
```

## Feature-detection

```css
@supports (animation-timeline: view()) {
  .reveal { animation: rise linear both;
            animation-timeline: view(); }
}
@supports not (animation-timeline: view()) {
  /* classic IntersectionObserver fallback */
  .reveal { opacity: 0; }
  .reveal.is-in { opacity: 1; transition: opacity 320ms; }
}
```

```javascript
if (CSS.supports('animation-timeline', 'view()')) {
  // great
} else {
  // set up IntersectionObserver fallback
}
```

## Reduced motion

```css
@media (prefers-reduced-motion: reduce) {
  .reveal, .parallax-img, .hero h1, .progress-bar {
    animation: none;
  }
}
```

Cancel any in-flight WAAPI animations:

```javascript
if (matchMedia('(prefers-reduced-motion: reduce)').matches) {
  document.getAnimations().forEach((a) => a.cancel())
}
```

## Browser support

| Browser | `scroll()` | `view()` |
|---|---|---|
| Chrome / Edge | 115+ ✅ | 115+ ✅ |
| Firefox | 136+ (2026) | 136+ (2026) |
| Safari | 26+ (2025) | 26+ (2025) |

As of audit (2026-09-23), all three major engines ship
`animation-timeline: scroll()` and `: view()`. Older versions need
the `@supports` fallback.

## Cross-references

- [MDN — CSS scroll-driven animations](https://developer.mozilla.org/en-US/docs/Web/CSS/animation-timeline)
- [CSSWG specification](https://drafts.csswg.org/scroll-animations-1/)
- [web.dev: scroll-driven animations](https://web.dev/articles/scroll-driven-animations)
