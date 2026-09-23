# HTML5 Native Design — Asset Library

## `starter/index.html`

A single-file demo exercising every primitive in the skill:

- `<dialog>` modal (animated open/close)
- Popover (light-dismiss + animated)
- `<details>` (smooth `grid-template-rows` animation)
- Container-queried card (auto-adaptive layout)
- Native form fields with proper `autocomplete` tokens
- Exclusive accordion (`details[name=…]`)

Open the file in a browser; every primitive works without a build
step. Pair with the `web-animations-api` skill's CSS scroll-driven
animations to add `animation-timeline: view()` reveals.

## `components/image-figure.html`

A Web Component using Declarative Shadow DOM — the shadow tree
arrives via `<template>` and renders without waiting for the JS to
run. The component exposes a `caption` slot, an `src` attribute,
and uses container queries for layout.

## `components/tabs.html`

A `<theme-tabs>` Web Component backed by radio buttons for state. The
state is fully native (works without JS); the custom element only
handles state propagation between the inputs and the panels.

## `components/count-up.html`

A `<count-up>` Web Component that animates a numeric display on
first paint, using the Web Animations API (`Element.animate`). CSS
custom-property interpolation for browsers that support it.

## Related skills

- `htmx` — for the server-rendered half; pair every form with
  `hx-post` and every modal with a `hx-get` to render its body.
- `web-animations-api` — for the motion layer; pair `<dialog>`
  open/close and Popover transitions with WAAPI for non-CSS-driven
  choreography.
- `gsap-scrolltrigger` — when scroll orchestration grows too
  complex for CSS scroll-driven animations.
- `motion-framer` — when you're in React and want the
  declarative `motion.div` API.
- `modern-web-design` — accessibility rules above this skill.
