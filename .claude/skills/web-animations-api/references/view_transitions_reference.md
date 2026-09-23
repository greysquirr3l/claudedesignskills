# View Transitions API Reference

The View Transitions API gives every site the morph-between-DOM-
snapshots animation that used to require a heavyweight framework.

## Same-document — `document.startViewTransition`

```typescript
const transition = document.startViewTransition(
  (() => void) | (() => Promise<void> | void)
)

transition.ready     // Promise — snapshots taken, swap in flight
transition.finished  // Promise — animations done
transition.updateCallbackDone  // Promise — your callback finished
transition.skipTransition()
```

The callback updates the DOM. The browser snapshots the current and
new state, names matched elements stay in place, the old snapshots
shrink and fade out, the new ones bloom in.

```javascript
// Synchronous updates
document.startViewTransition(() => {
  document.querySelector('#card').classList.toggle('expanded')
})

// Async updates
const t = document.startViewTransition(async () => {
  const html = await fetch('/api/page').then(r => r.text())
  document.querySelector('main').innerHTML = html
})

await t.finished
console.log('transition complete')
```

## Cross-document — `@view-transition { navigation: auto }`

CSS-only page-to-page transitions:

```css
@view-transition {
  navigation: auto;
}
::view-transition-old(root), ::view-transition-new(root) {
  animation-duration: 280ms;
  animation-timing-function: cubic-bezier(.2, .8, .2, 1);
}
```

Per-element morphs use `view-transition-name`:

```html
<!-- index -->
<article style="view-transition-name: post-42">…</article>

<!-- detail page -->
<article style="view-transition-name: post-42">…</article>
```

For both views, the browser morphs the snapshot from index layout
to detail layout automatically.

> **Browser support** as of 2026-09-23:
> - **Same-document** `startViewTransition` — Chrome 111+, Edge 111+,
>   Firefox 137+, Safari 18+. Universal in 2026.
> - **Cross-document** `@view-transition { navigation: auto }` —
>   Chrome 126+, Edge 126+, Safari 26+, Firefox ⏳ in progress.
>   Feature-detect / opt-in.

## Pseudo-elements

| Pseudo | Purpose |
|---|---|
| `::view-transition-group(*)` | The full snapshot pair wrapper |
| `::view-transition-image-pair(*)` | Holds both snapshots until animation finishes |
| `::view-transition-old(*)` | The old snapshot — fades / morphs out |
| `::view-transition-new(*)` | The new snapshot — fades / morphs in |

`*` accepts both a literal name and a wildcard. Use specific names
when you have only one morph element; use the wildcard for a global
transition policy.

```css
::view-transition-old(root), ::view-transition-new(root) {
  animation-duration: 280ms;
  animation-timing-function: cubic-bezier(.2, .8, .2, 1);
}

/* Card-name morph — keep the easing slower on the card specifically */
::view-transition-old(post-42), ::view-transition-new(post-42) {
  animation-duration: 360ms;
  animation-timing-function: cubic-bezier(.16, 1, .3, 1);
}
```

## Composing with other primitives

### With WAAPI for animating the snapshot

```javascript
document.startViewTransition(() => {
  popover.showPopover()
})

// WAAPI-driven choreography of one specific snapshot
const styleEl = popover.style
styleEl.viewTransitionName = 'confirm-modal'
```

### With CSS scroll-driven animations

CSS scroll-driven animations don't pause during VT, but the
snapshot interferes with `view-transition-name`. Don't re-use the
same name for two animations active at once.

### With WAAPI scrubable timeline

```javascript
const t = document.startViewTransition(() => {})
await t.ready
const all = document.getAnimations()
// Each pseudo-element's CSS animation is now in `all`.
```

## Reducing motion

```css
@media (prefers-reduced-motion: reduce) {
  ::view-transition-old(*),
  ::view-transition-new(*) {
    animation: none !important;
  }
}
```

And in JS:

```javascript
function transition(updateDOM) {
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches
  if (reduced) return { ready: Promise.resolve(), finished: Promise.resolve() }
  return document.startViewTransition(updateDOM)
}
```

## Patterns

### "Tile into full-screen modal"

```html
<img src="…" id="thumb" style="view-transition-name: thumb-1">
<div id="overlay" style="view-transition-name: thumb-1; display: none">
  <img src="…">
</div>
```

```javascript
document.getElementById('thumb').addEventListener('click', () => {
  document.startViewTransition(() => {
    document.getElementById('overlay').style.display = 'grid'
  })
})
```

### "Scroll to top on route change"

```javascript
const t = document.startViewTransition(() => {
  // update DOM...
})
await t.ready
window.scrollTo({ top: 0, behavior: 'instant' })
```

### "Skip the transition for trivial changes"

```javascript
document.startViewTransition(() => markAllAsRead())
// vs
markAllAsRead()  // no transition
```

### "Reverse popover close"

```javascript
popover.addEventListener('toggle', async (e) => {
  if (e.newState === 'open') return
  if (!document.startViewTransition) return
  const t = document.startViewTransition(() => {})
  await t.ready
  // close is happening now; let the browser snapshot first
  popover.hidePopover()
})
```

## Pitfalls

| Pitfall | Fix |
|---|---|
| `document.startViewTransition` undefined | Feature-detect; fall back to instant DOM update |
| Snapshot name collision | Two elements with the same `view-transition-name` morph into one snapshot. Avoid duplicates. |
| `<dialog>::backdrop` doesn't morph | Style backdrop separately — it isn't auto-snapshotted |
| Cross-doc VT breaks in Firefox | Conditional CSS; fall back to HTML refresh |
| Async callback throws | `transition.updateCallbackDone` rejects; DOM update is "applied" anyway. Catch + rollback. |
| Popover/dialog open during VT | Open the popover *outside* the callback — browser snapshots the *current* state |
| Excessive `view-transition-name` count | Each name adds an extra snapshot layer; use sparingly for "wow" elements |
| Reduced motion not respected | Always gate CSS pseudo-element animations and JS calls |

## Cross-references

- [MDN — View Transitions API](https://developer.mozilla.org/en-US/docs/Web/API/View_Transitions_API)
- [Chrome for Developers — Smooth transitions with the View Transitions API](https://developer.chrome.com/docs/web-platform/view-transitions)
- [CSSWG specification](https://drafts.csswg.org/css-view-transitions-1/)
- [web.dev — Shared element transitions](https://developer.chrome.com/docs/web-platform/shared-element-transitions)
