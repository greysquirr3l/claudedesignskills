# Starter assets

This directory contains ready-to-use assets for the `htmx` skill.

## `starter/index.html`

A zero-build, copy-and-open starter that exercises:

- **Boost** — `hx-boost="true"` upgrades all `<a>` and `<form>`
  automatically.
- **View Transitions** — `hx-ext="view-transition"` makes every
  page change feel native via the View Transitions API.
- **Lazy section** — `hx-trigger="intersect once"` swaps in a new
  card when scrolled into view.
- **Form** — `hx-post` with `hx-target` for a one-line echo
  submission.

Open the file directly in a browser (or with any static HTTP server
like `python3 -m http.server`). Each `hx-get` / `hx-post` will
trigger a 404 unless you put a stub server behind it; for a real
demo, see `express_demo/`.

## `express_demo/`

A minimal Express + EJS + HTMX demo with boost, infinite scroll,
OOB swaps, and a `view-transition` extension hook. Run:

```bash
cd express_demo
npm install
npm start
```

## `view_transition_landing/`

The "amazing scroll-driven landing" skeleton referenced in
`SKILL.md` §1 (Common Patterns). It uses only the HTML/CSS in this
file — pair with `web-animations-api` for visual polish.

## Related skills

These starter assets are most useful when paired with:

- `web-animations-api` — for the motion layer (`::view-transition-*`,
  scroll-driven CSS, WAAPI).
- `html5-native-design` — for the UI primitives (Popover, dialog,
  container queries, `:has()`).
- `modern-web-design` — for cross-cutting design tokens and rules.
