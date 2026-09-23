---
name: animejs
description: Versatile JavaScript animation engine for DOM, CSS, SVG, and JavaScript objects. Use when creating timeline-based animations, stagger effects, SVG morphing, keyframe sequences, or complex choreographed animations. Triggers on tasks involving Anime.js, timeline animations, staggered sequences, SVG path animations, morphing, or multi-step animation choreography. Alternative to GSAP for SVG-heavy animations and React-independent projects.
---

# Anime.js
> **Current version**: Anime.js **v4.5.0** (ESM-first, named exports).
> Examples in this file use the **v4** API: `animate(targets, params)`,
> `createTimeline(opts)`, `stagger()`, `svg.createMotionPath()`,
> `utils.getDash`, and `createSpring()`. Legacy v3 patterns
> (`animate({...})`, `createTimeline()`, `stagger()`,
> `svg.createMotionPath()`, `utils.getDash`, v3 spring easing) are
> documented in [Migration from v3](#migration-from-v3) at the bottom
> of this skill. **Audit date**: 2026-09-23.


Lightweight JavaScript animation library with powerful timeline and stagger capabilities for web animations.

## Overview

Anime.js (pronounced "Anime JS") is a versatile animation engine that works with DOM elements, CSS properties, SVG attributes, and JavaScript objects. Unlike React-specific libraries, Anime.js works with vanilla JavaScript and any framework.

**When to use this skill:**
- Timeline-based animation sequences with precise choreography
- Staggered animations across multiple elements
- SVG path morphing and drawing animations
- Keyframe animations with percentage-based timing
- Framework-agnostic animation (works with React, Vue, vanilla JS)
- Complex easing functions (spring, steps, cubic-bezier)

**Core features:**
- Timeline sequencing with relative positioning
- Powerful stagger utilities (grid, from center, easing)
- SVG morphing and path animations
- Built-in spring physics easing
- Keyframe support with flexible timing
- Small bundle size (~9KB gzipped)

## Core Concepts

### Basic Animation

The `animate()` function creates animations:

```javascript
import { animate } from 'animejs'

animate({
  targets: '.element',
  x: 250,
  rotate: '1turn',
  duration: 800,
  ease: 'inOutQuad'
})
```

### Targets

Multiple ways to specify animation targets:

```javascript
// CSS selector
animate({ targets: '.box' })

// DOM elements
animate({ targets: document.querySelectorAll('.box') })

// Array of elements
animate({ targets: [el1, el2, el3] })

// JavaScript object
const obj = { x: 0 }
animate({ targets: obj, x: 100 })
```

### Animatable Properties

**CSS Properties:**
```javascript
animate({
  targets: '.element',
  x: 250,
  scale: 2,
  opacity: 0.5,
  backgroundColor: '#FFF'
})
```

**CSS Transforms (Individual):**
```javascript
animate({
  targets: '.element',
  x: 250,   // Individual transform
  rotate: '1turn',   // Not 'transform: rotate()'
  scale: 2
})
```

**SVG Attributes:**
```javascript
animate({
  targets: 'path',
  d: 'M10 80 Q 77.5 10, 145 80', // Path morphing
  fill: '#FF0000',
  strokeDashoffset: [utils.getDash, 0] // Line drawing
})
```

**JavaScript Objects:**
```javascript
const obj = { value: 0 }
animate({
  targets: obj,
  value: 100,
  round: 1,
  onUpdate: () => console.log(obj.value)
})
```

### Timeline

Create complex sequences with precise control:

```javascript
const timeline = createTimeline({
  duration: 750,
  ease: 'outExpo'
})

timeline
  .add({
    targets: '.box1',
    x: 250
  })
  .add({
    targets: '.box2',
    x: 250
  }, '-=500') // Start 500ms before previous animation ends
  .add({
    targets: '.box3',
    x: 250
  }, '+=200') // Start 200ms after previous animation ends
```

## Common Patterns

### 1. Stagger Animation (Sequential Reveal)

```javascript
animate({
  targets: '.stagger-element',
  y: [100, 0],
  opacity: [0, 1],
  delay: stagger(100), // Increase delay by 100ms
  ease: 'outQuad',
  duration: 600
})
```

### 2. Stagger from Center

```javascript
animate({
  targets: '.grid-item',
  scale: [0, 1],
  delay: stagger(50, {
    grid: [14, 5],
    from: 'center', // Also: 'first', 'last', index, [x, y]
    axis: 'x'       // Also: 'y', null
  }),
  ease: 'outQuad'
})
```

### 3. SVG Line Drawing

```javascript
animate({
  targets: 'path',
  strokeDashoffset: [utils.getDash, 0],
  ease: 'inOutQuad',
  duration: 2000,
  delay: (el, i) => i * 250
})
```

### 4. SVG Morphing

```javascript
animate({
  targets: '#morphing-path',
  d: [
    { value: 'M10 80 Q 77.5 10, 145 80' }, // Start shape
    { value: 'M10 80 Q 77.5 150, 145 80' }  // End shape
  ],
  duration: 2000,
  ease: 'inOutQuad',
  loop: true,
  direction: 'alternate'
})
```

### 5. Timeline Sequence

```javascript
const tl = createTimeline({
  ease: 'outExpo',
  duration: 750
})

tl.add({
  targets: '.title',
  y: [-50, 0],
  opacity: [0, 1]
})
.add({
  targets: '.subtitle',
  y: [-30, 0],
  opacity: [0, 1]
}, '-=500')
.add({
  targets: '.button',
  scale: [0, 1],
  opacity: [0, 1]
}, '-=300')
```

### 6. Keyframe Animation

```javascript
animate({
  targets: '.element',
  keyframes: [
    { x: 100 },
    { y: 100 },
    { x: 0 },
    { y: 0 }
  ],
  duration: 4000,
  ease: 'inOutQuad',
  loop: true
})
```

### 7. Scroll-Triggered Animation

```javascript
const animation = animate({
  targets: '.scroll-element',
  y: [100, 0],
  opacity: [0, 1],
  ease: 'outQuad',
  autoplay: false
})

window.addEventListener('scroll', () => {
  const scrollPercent = window.scrollY / (document.body.scrollHeight - window.innerHeight)
  animation.seek(animation.duration * scrollPercent)
})
```

## Integration Patterns

### With React

```javascript
import { useEffect, useRef } from 'react'
import { animate } from 'animejs'

function AnimatedComponent() {
  const ref = useRef(null)

  useEffect(() => {
    const animation = animate({
      targets: ref.current,
      x: 250,
      duration: 800,
      ease: 'inOutQuad'
    })

    return () => animation.pause()
  }, [])

  return <div ref={ref}>Animated</div>
}
```

### With Vue

```javascript
export default {
  mounted() {
    animate({
      targets: this.$el,
      x: 250,
      duration: 800
    })
  }
}
```

### Path Following Animation

```javascript
const path = svg.createMotionPath('#motion-path')

animate({
  targets: '.element',
  x: path('x'),
  y: path('y'),
  rotate: path('angle'),
  ease: 'linear',
  duration: 2000,
  loop: true
})
```

## Advanced Techniques

### Spring Easing

```javascript
animate({
  targets: '.element',
  x: 250,
  ease: createSpring({ mass: 1, stiffness: 80, damping: 10, velocity: 0 }), // mass, stiffness, damping, velocity
  duration: 2000
})
```

### Steps Easing

```javascript
animate({
  targets: '.element',
  x: 250,
  easing: 'steps(5)',
  duration: 1000
})
```

### Custom Bezier

```javascript
animate({
  targets: '.element',
  x: 250,
  easing: 'cubicBezier(.5, .05, .1, .3)',
  duration: 1000
})
```

### Direction and Loop

```javascript
animate({
  targets: '.element',
  x: 250,
  direction: 'alternate', // 'normal', 'reverse', 'alternate'
  loop: true,             // or number of iterations
  ease: 'inOutQuad'
})
```

### Playback Control

```javascript
const animation = animate({
  targets: '.element',
  x: 250,
  autoplay: false
})

animation.play()
animation.pause()
animation.restart()
animation.reverse()
animation.seek(500) // Seek to 500ms
```

## Performance Optimization

### Use Transform and Opacity

```javascript
// ✅ Good: GPU-accelerated
animate({
  targets: '.element',
  x: 250,
  opacity: 0.5
})

// ❌ Avoid: Triggers layout
animate({
  targets: '.element',
  left: '250px',
  width: '500px'
})
```

### Batch Similar Animations

```javascript
// ✅ Single animation for multiple targets
animate({
  targets: '.multiple-elements',
  x: 250
})

// ❌ Avoid: Multiple separate animations
elements.forEach(el => {
  animate({ targets: el, x: 250 })
})
```

### Use `will-change` for Complex Animations

```css
.animated-element {
  will-change: transform, opacity;
}
```

### Disable autoplay for Scroll Animations

```javascript
const animation = animate({
  targets: '.element',
  x: 250,
  autoplay: false // Control manually
})
```

## Common Pitfalls

### 1. Forgetting Unit Types

```javascript
// ❌ Wrong: No unit
animate({ targets: '.element', width: 200 })

// ✅ Correct: Include unit
animate({ targets: '.element', width: '200px' })
```

### 2. Using CSS transform Property Directly

```javascript
// ❌ Wrong: Can't animate transform string
animate({ targets: '.element', transform: 'translateX(250px)' })

// ✅ Correct: Individual transform properties
animate({ targets: '.element', x: 250 })
```

### 3. Not Handling Animation Cleanup

```javascript
// ❌ Wrong: Animation continues after unmount
useEffect(() => {
  animate({ targets: ref.current, x: 250 })
}, [])

// ✅ Correct: Pause on cleanup
useEffect(() => {
  const anim = animate({ targets: ref.current, x: 250 })
  return () => anim.pause()
}, [])
```

### 4. Animating Too Many Elements

```javascript
// ❌ Avoid: Animating 1000+ elements
animate({ targets: '.many-items', x: 250 }) // 1000+ elements

// ✅ Better: Use CSS animations for large sets
// Or reduce element count with virtualization
```

### 5. Incorrect Timeline Timing

```javascript
// ❌ Wrong: Missing offset operator
.add({ targets: '.el2' }, '500') // Treated as absolute time

// ✅ Correct: Use relative operators
.add({ targets: '.el2' }, '-=500') // Relative to previous
.add({ targets: '.el3' }, '+=200') // Relative to previous
```

### 6. Overusing Loop

```javascript
// ❌ Avoid: Infinite loops drain battery
animate({
  targets: '.element',
  rotate: '1turn',
  loop: true,
  duration: 1000
})

// ✅ Better: Use CSS animations for infinite loops
@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
```

## Migration from v3

Patterns below are kept verbatim for users upgrading existing codebases.
**Prefer the v4 APIs** demonstrated in the main examples above.

### v3 → v4 API mapping

| v3 (legacy) | v4 (current) |
|---|---|
| `import anime from 'animejs'` | `import { animate, createTimeline, stagger, utils, svg } from 'animejs'` |
| `anime({ targets, ... })` | `animate(targets, { ... })` |
| `anime.timeline(opts)` | `createTimeline(opts)` |
| `anime.stagger(100, opts)` | `stagger(100, opts)` (named export) |
| `anime.setDashoffset` | `utils.getDash` helper |
| `anime.path('#m')` | `svg.createMotionPath('#m')` |
| `easing: 'spring(1, 80, 10, 0)'` | `ease: createSpring({ mass: 1, stiffness: 80, damping: 10, velocity: 0 })` |
| `complete: fn` callback | `onComplete: fn` (all callbacks use `on*` prefix) |
| `begin: fn` callback | `onBegin: fn` |
| `update: fn` callback | `onUpdate: fn` |
| `direction: 'reverse'` | `reversed: true` |
| `direction: 'alternate'` | `alternate: true` (use with `loop`) |
| `loop: true` | `loop: true` (still supported; use `Infinity` for infinite) |
| `translateX: n` | `x: n` |
| `translateY: n` | `y: n` |

### v3 default import (legacy)

```javascript
import anime from 'animejs'

anime({
  targets: '.element',
  translateX: 250,
  duration: 800,
  easing: 'easeInOutQuad',
  complete: () => console.log('done')
})
```

### v4 equivalent (current)

```javascript
import { animate } from 'animejs'

animate('.element', {
  x: 250,
  duration: 800,
  ease: 'inOutQuad',
  onComplete: () => console.log('done')
})
```

### v3 timeline (legacy)

```javascript
const timeline = anime.timeline({ easing: 'easeOutExpo', duration: 750 })
timeline.add({ targets: '.a', translateX: 250 })
            .add({ targets: '.b', translateX: 250 }, '-=500')
```

### v4 equivalent (current)

```javascript
import { createTimeline } from 'animejs'

const tl = createTimeline({ defaults: { ease: 'outExpo', duration: 750 } })
tl.add('.a', { x: 250 })
  .add('.b', { x: 250 }, '-=500')
```

### v3 stagger (legacy)

```javascript
anime({
  targets: '.grid-item',
  scale: [0, 1],
  delay: anime.stagger(50, { grid: [14, 5], from: 'center', axis: 'x' })
})
```

### v4 equivalent (current)

```javascript
import { animate, stagger } from 'animejs'

animate('.grid-item', {
  scale: [0, 1],
  delay: stagger(50, { grid: [14, 5], from: 'center', axis: 'x' })
})
```

### v3 motion path (legacy)

```javascript
const path = anime.path('#motion-path')
anime({ targets: '.el', translateX: path('x'), translateY: path('y'), rotate: path('angle') })
```

### v4 equivalent (current)

```javascript
import { animate, svg } from 'animejs'

const motionPath = svg.createMotionPath('#motion-path')
animate('.el', {
  x: motionPath('x'),
  y: motionPath('y'),
  rotate: motionPath('angle')
})
```

### v3 line drawing helper (legacy)

```javascript
anime({
  targets: 'path',
  strokeDashoffset: [anime.setDashoffset, 0]
})
```

### v4 equivalent (current)

```javascript
import { animate, utils } from 'animejs'

animate('path', {
  strokeDashoffset: [utils.getDash, 0]
})
```

### v3 spring easing (legacy)

```javascript
anime({
  targets: '.element',
  translateX: 250,
  easing: 'spring(1, 80, 10, 0)' // mass, stiffness, damping, velocity
})
```

### v4 equivalent (current)

```javascript
import { animate, createSpring } from 'animejs'

animate('.element', {
  x: 250,
  ease: createSpring({ mass: 1, stiffness: 80, damping: 10, velocity: 0 })
})
```

### Bundle size note

Anime.js v4 ships as ESM with tree-shakable named exports. Importing only
the helpers used (`animate`, `stagger`, `createTimeline`) yields a smaller
bundle than the legacy default-import v3 build. The earlier "~9 KB
gzipped" figure targeted v3; v4 with a single `animate` import is
generally smaller, while the full v4 build (including SVG/timer
utilities) is larger. Measure with your bundler.

## Resources

### Scripts
- `animation_generator.py` - Generate Anime.js animation boilerplate (8 types)
- `timeline_builder.py` - Build complex timeline sequences

### References
- `api_reference.md` - Complete Anime.js API documentation
- `stagger_guide.md` - Stagger utilities and patterns
- `timeline_guide.md` - Timeline sequencing deep dive

### Assets
- `starter_animejs/` - Vanilla JS + Vite template with examples
- `examples/` - Real-world patterns (SVG morphing, stagger grids, timelines)

## Related Skills

- **gsap-scrolltrigger** - More powerful timeline features and scroll integration
- **motion-framer** - React-specific declarative animations
- **react-spring-physics** - Physics-based spring animations
- **lightweight-3d-effects** - Simple 3D effects (Zdog, Vanta.js)

**Anime.js vs GSAP**: Use Anime.js for SVG-heavy animations, simpler projects, or when bundle size matters. Use GSAP for complex scroll-driven experiences, advanced timelines, and professional-grade control.

**Anime.js vs Framer Motion**: Use Anime.js for framework-agnostic projects or when working outside React. Use Framer Motion for React-specific declarative animations with gesture integration.
