# Web Animations API — Asset Library

## Ground-truth examples

`groundtruth/scroll_timeline_lab.html` — a copy of the user's
`2026_scroll_timeline_lab.html` from
[greysquirr3l/pattern_lab](https://github.com/greysquirr3l/pattern_lab).
Twelve finished, no-framework scroll-driven CSS animation examples
(reading progress bar, parallax, conversation timeline, palette
rotation, scroll-peel stickers, warp starfield, scroll typewriter,
card deck deal, etc.). Use as a polished reference and re-pull from
the user's repo when they update pattern_lab.

## `scroll_showcase/index.html`

A pure-CSS scroll-driven landing with:
- Reading-progress bar (`animation-timeline: scroll(root)`)
- Hero shrink (also `scroll(root)`)
- Reveal-on-scroll sections (`animation-timeline: view()`)
- A CSS-only parallax block

Open directly in a Chrome 115+/Edge 115+/Firefox 136+/Safari 26+
browser. Falling back gracefully on older engines — verify with
DevTools "Emulate prefers-reduced-motion" and a 2024-stable browser
to see the no-feature fallback.

## `view_transition_landing/index.html`

Same-document View Transitions demo with a "click-button swap main
content" pattern. Pairs with the htmx skill's
`view-transition` extension — replace the local `swap()` function
with `hx-get` + `hx-swap` for actual route loading.

## `reduced_motion_demo/index.html`

A minimal `prefers-reduced-motion: reduce` toggle demo — opens in
two side-by-side panels that show the difference between motion
and reduced-motion states.

## Related skills

- `htmx` — pair with the `view-transition` extension to make every
  server response a morph.
- `html5-native-design` — `<dialog>`, Popover, and `<details>`
  open/close animations fit right in.
- `gsap-scrolltrigger` — when you need multi-property scrub
  timelines, GSAP is the right tool.
- `motion-framer` — when you're in React and want the
  declarative `<motion.div>` API.
- `modern-web-design` — accessibility rules above this one.
