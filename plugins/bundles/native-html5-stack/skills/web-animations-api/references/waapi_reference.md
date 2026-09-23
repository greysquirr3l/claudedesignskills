# Web Animations API Reference

## Element.animate(keyframes, options)

```typescript
const anim = el.animate(
  [
    { opacity: 0, transform: 'translateY(20px)' },
    { opacity: 1, transform: 'none' }
  ],
  {
    duration: 280,                          // ms
    delay: 0,                               // ms
    iterations: 1,                          // 1, N, or Infinity
    iterationStart: 0,                      // ms offset
    direction: 'normal',                    // normal | reverse | alternate | alternate-reverse
    fill: 'auto',                           // auto | none | backwards | forwards | both
    composite: 'replace',                   // replace | add | accumulate
    iterationComposite: 'replace',          // replace | accumulate
    easing: 'cubic-bezier(.2, .8, .2, 1)',  // string OR 4-tuple array
  }
)
```

`keyframes` can be an array of property maps OR a
`KeyframeEffect`-equivalent object. WAAPI supports individual
transform properties (`translateX`, `rotateX`) and the composite
`transform` shorthand; CSS-side, both forms compose.

```javascript
// Multi-keyframe — intermediate stops are linearly interpolated
el.animate(
  [
    { transform: 'translateX(0)' },
    { transform: 'translateX(50%)' },
    { transform: 'translateX(0)' }
  ],
  { duration: 1000, iterations: Infinity }
)
```

## Animation interface

```typescript
interface Animation {
  // Read
  readonly effect: AnimationEffect | null
  readonly timeline: AnimationTimeline | null
  readonly playState: 'idle' | 'pending' | 'running' | 'paused' | 'finished'
  readonly currentTime: number | null           // ms
  readonly startTime: number | null            // ms
  readonly playbackRate: number                // 1.0 = normal, 0.5 = half, -1 = reverse
  readonly pending: boolean

  // Lifecycle
  finish(): void         // jump to end
  cancel(): void         // reset to base, fire 'cancel' event
  persist(): void        // don't auto-remove when finished
  pause(): void
  play(): void

  // Promise
  readonly ready: Promise<this>
  readonly finished: Promise<this>
  readonly updatePromise: Promise<void>

  // Events
  onfinish: ((e: AnimationPlaybackEvent) => void) | null
  oncancel: ((e: AnimationPlaybackEvent) => void) | null
  addEventListener('finish', cb)
  addEventListener('cancel', cb)
  addEventListener('remove', cb)
}
```

## document.getAnimations()

```javascript
document.getAnimations()                        // every animation
document.getAnimations({ subtree: true })       // also those in shadow DOM
el.getAnimations({ subtree: true })             // per-element

// Useful patterns
const all = document.getAnimations()
const mine = all.filter(a => a.effect?.target === el)

// Cancellation
all.forEach(a => a.cancel())
```

## Easing

| String | Notes |
|---|---|
| `'linear'` | Constant |
| `'ease'`, `'ease-in'`, `'ease-out'`, `'ease-in-out'` | Standard |
| `'cubic-bezier(.34, 1.56, .64, 1)'` | W3C "easeOutBack" — spring-like overshoot |
| `'steps(60)'` | Step easing; not useful for scroll-bound |
| `'linear'` array `[0, 0, 1, 1]` | Bezier cubic-bezier |

For a stiffer spring, use the `'cubic-bezier(.34, 1.56, .64, 1)'`
shape with shorter duration. A real spring needs a library like
`motion-spring`; WAAPI has no spring easing primitive in 2026.

## Composite

`composite: 'replace'` (default) — this animation wins over the
underlying value.

`composite: 'add'` — this animation's value is *added* to the
underlying value at runtime. Useful for spring-like overlays.

`composite: 'accumulate'` — accumulated across iterations. Rarely used.

```javascript
// Two animations on the same property — they don't fight:
el.animate([{ transform: 'translateX(0)' }, { transform: 'translateX(50px)' }],
           { duration: 200, composite: 'replace' })
el.animate([{ transform: 'rotate(0)' }, { transform: 'rotate(45deg)' }],
           { duration: 200, composite: 'replace' })  // one replaces transform; the other also replaces
// Both control `transform`; replace resolves by last-wins.
// Add → sums translateX and rotate (browser handles transform-list).
```

## fill modes

| Mode | Behaviour |
|---|---|
| `'auto'` | The element's base state outside the animation's lifetime. |
| `'none'` | Element returns to its base state before / after. |
| `'backwards'` | Element takes its first-keyframe value during `delay`. |
| `'forwards'` | Element keeps its last-keyframe value after the animation ends. |
| `'both'` | Combination of backwards and forwards. |

For most "I want the element to stay where it ends up" cases, use
`fill: 'forwards'`.

## Events

| Event | Fires when… |
|---|---|
| `animationstart` / `animationend` (CSS) | When CSS `@keyframes` animation begins/ends |
| `transitionrun` / `transitionend` | CSS `transition` lifecycle |
| `animationcancel` | CSS animation cancelled by removing target / pausing |
| `finish` | WAAPI animation reached end (or was finished by `finish()`) |
| `cancel` | WAAPI animation cancelled |
| `remove` | Animation removed from `getAnimations()` |

## Animation timeline quirks

1. **Background tabs throttle** — running WAAPI on a hidden tab
   doesn't update; the animation effectively pauses. Use
   `composite: 'add'` to layer over throttled state.
2. **`iterations: Infinity`** — for indefinite loops (e.g. CPU
   spinner), pair with `pause()` in a `document.visibilitychange`
   handler.
3. **Persistent animations** — by default, finished animations are
   removed from `getAnimations()` to save memory. Call `.persist()`
   if you want to inspect `currentTime` later.
4. **`fill: 'forwards'` + `cancel()`** — the next state after cancel
   is the base state, not the last keyframe. Use `pause()` before
   cancel if you want the freeze-frame.

## API cross-references

| Spec | Lives at |
|---|---|
| Web Animations API | <https://www.w3.org/TR/web-animations-1/> |
| Web Animations API Level 2 | <https://www.w3.org/TR/web-animations-2/> |
| `Animation.timeline` extensions | <https://developer.mozilla.org/en-US/docs/Web/API/Animation/timeline> |
| `document.getAnimations` | <https://developer.mozilla.org/en-US/docs/Web/API/Document/getAnimations> |
