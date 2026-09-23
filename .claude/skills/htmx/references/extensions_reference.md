# HTMX Extensions Reference

HTMX 2 ships with built-in support for View Transitions and Morph,
and the community maintains several extensions for SSE, WebSockets,
multi-swap, preload, and more.

## Built-in extensions (htmx 2.x)

These are part of `htmx.org` — no separate install, just enable via
`hx-ext`:

### `view-transition`

Bridges every swap to the View Transitions API when supported. Pair
with `view-transition-name` on matched swapped nodes for per-section
choreography.

```html
<body hx-boost="true" hx-ext="view-transition">
  <main id="main">…</main>
</body>
<style>
  ::view-transition-old(root), ::view-transition-new(root) {
    animation-duration: 280ms;
    animation-timing-function: cubic-bezier(.2,.8,.2,1);
  }
</style>
```

Fallback for browsers without support: htmx falls back to a normal
swap; the CSS `::view-transition-*` pseudo-elements are ignored.

### `morph`

Uses [Idiomorph](https://github.com/bigskysoftware/idiomorph) to
merge HTML without losing focus, scroll position, or pending form
input.

```html
<li hx-get="/api/tasks/1" hx-swap="morph:outerHTML" hx-ext="morph">…</li>
<!-- Idiomorph is loaded with this extension -->
<script src="https://cdn.jsdelivr.net/npm/htmx-ext-morph@2.0.4/morph.js" defer></script>
```

Morph modes:

- `morph:innerHTML` — replace children while keeping the element.
- `morph:outerHTML` — replace element; structures must match well.
- `morph:content` — Idiomorph's lightest mode; useful for `<table
  tbody>` row replacements.

## Community extensions (CDN-loadable)

| Extension | Purpose | URL pattern |
|---|---|---|
| `sse` | Subscribe to Server-Sent Events | `/dist/sse.js` |
| `ws` | WebSocket subscriptions | `/dist/ws.js` |
| `head-support` | Merge `<title>` and other head tags | `/dist/head-support.js` |
| `multi-swap` | Swap multiple named regions in one response | `/dist/multi-swap.js` |
| `response-targets` | Trigger swaps from response headers (`HX-Trigger-After-Swap`) | `/dist/response-targets.js` |
| `preload` | Prefetch `/api/...` URLs on hover | `/dist/preload.js` |
| `path-deps` | Refresh elements when the URL path matches a pattern | `/dist/path-deps.js` |
| `restored` | Trigger a request when the user navigates back | `/dist/restored.js` |
| `ajax-header` | Set a custom request header for htmx traffic | (inline, no script) |
| `form-json` | Serialize forms as JSON instead of form-data | `/dist/form-json.js` |
| `loading-states` | Adds extra CSS hooks during request | `/dist/loading-states.js` |

All extensions live at
`https://cdn.jsdelivr.net/npm/htmx-ext-<name>@<version>/dist/<name>.js`.
Pin versions for reproducibility.

## Loading extension scripts

```html
<script src="https://cdn.jsdelivr.net/npm/htmx.org@2.0.4/dist/htmx.min.js" defer></script>
<script src="https://cdn.jsdelivr.net/npm/htmx-ext-sse@2.0.4/sse.js" defer></script>
<script src="https://cdn.jsdelivr.net/npm/htmx-ext-ws@2.0.4/ws.js" defer></script>
<script src="https://cdn.jsdelivr.net/npm/htmx-ext-morph@2.0.4/morph.js" defer></script>
<script src="https://cdn.jsdelivr.net/npm/htmx-ext-view-transition@2.0.4/view-transition.js" defer></script>
<script src="https://cdn.jsdelivr.net/npm/htmx-ext-response-targets@2.0.4/response-targets.js" defer></script>
```

## `sse` — Server-Sent Events

```html
<div hx-ext="sse" sse-connect="/stream"
     sse-swap="tick"
     hx-swap="innerHTML"></div>
```

Attributes:

| Attribute | Purpose |
|---|---|
| `sse-connect="<url>"` | Open the EventSource |
| `sse-swap="<event-name>"` | Element receives `<event-name>` messages |
| `sse-close="<event-name>"` | Element receives `<event-name>` and closes |

Server contract (text/event-stream):

```
event: tick
data: <li>Item 1</li>

event: tick
data: <li>Item 2</li>
```

## `ws` — WebSocket

```html
<div hx-ext="ws" ws-connect="/ws">…</div>
<form ws-send><input name="msg"><button>Send</button></form>
```

For per-element routing, use `ws-connect#container-id`:

```html
<div hx-ext="ws" ws-connect="/chat"
     hx-trigger="refresh from:body"
     ws-message--refresh="if(event.detail.message === 'refresh') location.reload()">
  …
</div>
```

## `response-targets`

Map an `HX-Trigger` (response header) to a CSS selector.

```javascript
// server.js — send a header that triggers a swap
response.setHeader('HX-Trigger', 'tabChanged')
response.setHeader('HX-Trigger-After-Swap', 'analyticsEvent')
```

```html
<div id="content" hx-ext="response-targets"
     hx-on::tab-changed="document.querySelector('#tabs').dispatchEvent(new Event('refresh'))">
</div>
```

## `multi-swap`

Swap multiple named regions in a single response (server returns a
document with `id="region-name"` fragments).

```html
<main hx-ext="multi-swap" hx-get="/api/dashboard">
  <div id="metrics"></div>
  <div id="charts"></div>
  <div id="alerts"></div>
</main>
```

Server response:

```html
<div id="metrics">…updated…</div>
<div id="charts">…updated…</div>
<div id="alerts">…updated…</div>
```

## `preload`

Prefetch resources on hover/touch to make navigations instant:

```html
<a href="/about" preload="Mouseover" preload-images="true">About</a>
```

Or globally:

```javascript
htmx.config.preloadImages = true
```

`preload` is part of `htmx-preload` package; pin to a version.

## `path-deps`

Refresh elements when the URL path matches a pattern:

```html
<section hx-get="/api/case-studies" hx-trigger="path-deps"
         path-deps="/case-studies">
  Loading…
</section>
```

Useful for "active" nav highlighting, breadcrumbs, or sidebar
fragments that depend on which route is loaded.

## Combining extensions

```html
<body hx-boost="true"
      hx-ext="view-transition,response-targets,path-deps">
  …
</body>
```

Each extension adds its own attributes (`sse-connect`, `ws-connect`,
`path-deps`, …). No conflicts unless two extensions try to claim the
same event or attribute.
