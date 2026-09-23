# Popover API Reference

The Popover API (Chrome 114+, Edge 114+, Firefox 125+, Safari 17+)
makes transient UI (popovers, tooltips, dropdowns) first-class
citizens without losing focus management, ESC handling, or
top-layer stacking.

## Element shape

```html
<div popover="auto | manual">…</div>
```

- `popover="auto"` — light-dismiss (click outside / ESC closes),
  stacking (only one auto popover at a time, others hide).
- `popover="manual"` — must call `hidePopover()` to close, no
  stacking rules.

The popover renders in the **top layer** like `<dialog>` —
outside `overflow: hidden` and `<iframe>` boundaries.

## Triggering

### Declarative (HTML only)

```html
<button popovertarget="my-popover"
        popovertargetaction="show | hide | toggle">Open</button>

<div id="my-popover" popover="auto">
  <p>Hello from a popover.</p>
</div>
```

| `popovertargetaction` | Effect |
|---|---|
| `show` | Call `showPopover()` (idempotent) |
| `hide` | Call `hidePopover()` |
| `toggle` | Toggle |

`popovertargetaction="toggle"` is the most common — one button
opens and closes the popover.

### Imperative (JS)

```javascript
const el = document.getElementById('my-popover')

el.showPopover()          // open
el.hidePopover()          // close
el.togglePopover()        // toggle
el.matches(':popover-open') // current state

// State events
el.addEventListener('toggle', (e) => {
  console.log(e.newState)  // 'open' | 'closed'
})

// Open with interactivity (top layer) but no light-dismiss
el.showPopover({ source: trigger })
```

## CSS targeting

```css
/* Default popover styles (override the user-agent defaults) */
[popover] {
  margin: auto;
  inset: 0;
  border: 1px solid light-dark(#ddd, #1f2630);
  border-radius: .5rem;
  padding: 1rem;
  background: light-dark(#fff, #131a20);
  color: light-dark(#1a1a1a, #f1f1f1);
}

/* Open state */
[popover]:popover-open { /* … */ }

/* Animations: open/close apply to display + opacity */
.popover {
  opacity: 0;
  transform: translateY(8px) scale(.985);
  transition: opacity 220ms ease-out,
              transform 280ms cubic-bezier(.2,.8,.2,1),
              overlay 280ms allow-discrete,
              display 280ms allow-discrete;
}
.popover:popover-open {
  opacity: 1;
  transform: none;
}

/* Start-state for the *first* open (entry animation) */
@starting-style {
  .popover:popover-open {
    opacity: 0;
    transform: translateY(8px) scale(.985);
  }
}

/* When closed, the open-state style is still applied unless
   we explicitly reset */
.popover:not(:popover-open) {
  transform: translateY(8px) scale(.985);
}
```

`@starting-style` is the modern way to define "what the element
looks like the moment it appears" — pair it with the closed-state
above for a smooth symmetric animation.

## Positioning

Three positioning primitives:

1. **Default** — `inset: 0; margin: auto;` (centred).
2. **Custom CSS** — explicit `top`, `left`, etc.
3. **CSS Anchor Positioning** — attach to an `anchor-name`.

```html
<button id="trigger" style="anchor-name:--trigger">Open</button>

<div id="p" popover="manual" style="position-anchor:--trigger"
     class="anchored">…</div>

<style>
  .anchored {
    /* Anchor pos — relative to the trigger element */
    inset-area: block-end span-inline-end;
    inset: auto;
    margin: 0;
    /* Optional: rotate per anchor */
    position-try-options: flip-block, flip-inline;
  }
</style>
```

CSS Anchor Positioning (Chrome 125+, Safari TP) lets the popover
position itself relative to a named anchor without JS measurement.

## Light-dismiss, focus, and stacking

| Property | `popover="auto"` | `popover="manual"` |
|---|---|---|
| Top-layer stacking | ✅ | ✅ |
| Top-layer group | one at a time | independent |
| ESC closes | ✅ | ❌ (unless we bind it) |
| Click outside closes | ✅ | ❌ |
| Focus trap | ❌ (use `<dialog>` if needed) | ❌ |
| Inert when hidden | ✅ | ✅ |

Light-dismiss means clicking *anywhere outside* the popover
(including other auto popovers) closes it. ESC also closes.

Stacking means showing a second auto popover implicitly closes
the first one. (For stacked tooltips, use `popover="manual"`.)

## Event lifecycle

| Event | Fires when… |
|---|---|
| `beforetoggle` | About to show / hide; cancellable |
| `toggle` | After state changes |

```javascript
el.addEventListener('beforetoggle', (e) => {
  if (!canShow(e)) e.preventDefault()
})

el.addEventListener('toggle', (e) => {
  console.log(e.newState)
  document.documentElement.classList.toggle('has-open-popover', e.newState === 'open')
})
```

## Inert / Page interaction

When an auto popover is open, the rest of the page is **not** inert
by default — only the previous popover/s are. To make the page
inert while a popover is open:

```css
:has(.popover:popover-open) main { pointer-events: none; }
```

Or use a JS observer.

## Patterns

### Tooltip (non-modal, hover-driven)

```html
<button popovertarget="tip" popovertargetaction="show"
        popovertargetactionhover="show">Hover me</button>
<div id="tip" popover="manual">A small hint.</div>

<style>
  #tip[popover] { width: max-content; max-width: 220px;
                  padding: .5rem .75rem; font: 14px/1.5 system-ui; }
  button:hover ~ #tip { /* for non-Popover-API hover fallbacks */ }
</style>
```

(`popovertargetactionhover` is in flight as a CSS-mode declarative
attribute; check support before relying on it. The current
JS-free fallback is the `:hover` selector.)

### Modal stack

```html
<dialog popover="manual" id="m1">…</dialog>
<dialog popover="manual" id="m2">…</dialog>
```

`<dialog popover>` (Chrome 124+) gets light-dismiss on top of
`<dialog>` modal semantics. Truly "best of both".

### Pair with View Transitions

Set matching `view-transition-name` on the trigger and the popover
to morph between them on open:

```html
<button popovertarget="m1" style="view-transition-name: m1-trigger">Open</button>
<div id="m1" popover="auto" style="view-transition-name: m1-popover">…</div>

<style>
  ::view-transition-old(m1-trigger),
  ::view-transition-new(m1-popover) {
    animation-duration: 240ms;
    animation-timing-function: cubic-bezier(.2,.8,.2,1);
  }
</style>
```

## Browser support

| Feature | Chrome / Edge | Firefox | Safari |
|---|---|---|---|
| Popover API | 114+ | 125+ | 17+ |
| `popovertarget` declarative | 114+ | 125+ | 17+ |
| `transition-behavior: allow-discrete` | 117+ | 129+ | 17.4+ |
| `@starting-style` | 117+ | 129+ | 17.5+ |
| CSS Anchor Positioning (`position-anchor`) | 125+ | TP | 26 TP |
| `<dialog popover>` | 124+ | TP | TP |

## Cross-references

- [MDN — Popover API](https://developer.mozilla.org/en-US/docs/Web/API/Popover_API)
- [Open UI Popover proposal](https://open-ui.org/components/popover.research.html)
- [web.dev — Popover API](https://web.dev/articles/popover)
