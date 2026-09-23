# HTMX 2.x API Reference

Quick reference for **HTMX 2.0.x** attributes, events, and config.
Each entry shows the canonical 2.x form plus a note when it differs
from 1.x.

## Attributes

### Request

| Attribute | Effect | Default |
|---|---|---|
| `hx-get="<url>"` | Issue `GET` on natural event | — |
| `hx-post="<url>"` | Issue `POST` | — |
| `hx-put`, `hx-patch`, `hx-delete` | Same shape, different verb | — |
| `hx-trigger="<spec>"` | Trigger condition | element-appropriate natural event |
| `hx-target="<css>"` | Where to swap | the element itself |
| `hx-swap="innerHTML\|outerHTML\|beforebegin\|afterbegin\|beforeend\|afterend\|delete\|none"` | How to swap | `innerHTML` |
| `hx-swap="show:<sel>:<where>"` (2.x) | Scroll-into-view after swap; `:top`/`:bottom`/`:middle`/`:start`/`:end` | none |
| `hx-swap="morph:<style>"` (extension) | Idiomorph-backed merge | `none` |
| `hx-include="<css>"` | Extra fields to include in the request | none |
| `hx-params="<csv>"` | Param whitelist/blacklist (prefix `none,` to whitelist) | all |
| `hx-vals='<json>'` | Extra JSON params | `{}` |
| `hx-headers='<json>'` | Extra HTTP headers | `{}` |
| `hx-attribute="<name>"` (2.x) | Override a request header to mirror a DOM attribute | none |
| `hx-confirm="<msg>"` | `window.confirm()` before request | none |

### Cache / push-state

| Attribute | Effect |
|---|---|
| `hx-push-url="true\|<url>"` | `pushState` on swap |
| `hx-replace-url="true\|<url>"` | `replaceState` on swap |
| `hx-history="false"` | Disable history for this element (2.x) |
| `hx-push-url` / `hx-replace-url` / `hx-history` together | Most-specific wins (2.x) |

### Selectors / scoping

| Attribute | Effect |
|---|---|
| `hx-select="<css>"` | Apply `hx-select` to the response: pick a subtree (server returns a full document; client picks the matched subtree) |
| `hx-select-oob="<css>"` | Same, but as an OOB swap |
| `hx-ext="<ext1>,<ext2>"` | Enable extensions on this element |
| `hx-disinherit="<attr>"` | Stop children from inheriting attribute |
| `hx-disabled` | Disable htmx processing in this subtree |

### Lifecycle

| Attribute | Effect |
|---|---|
| `hx-on::<event>="<js>"` (2.x) | Inline event handler (was `hx-on`) |
| `hx-on::event-without-target` | Fires for htmx events too |
| `hx-on:htmx:configRequest="..."` | Standard event hook |

## Events

| Event | Fires when… |
|---|---|
| `htmx:configRequest` | About to send; mutate `e.detail.parameters`, `e.detail.headers` |
| `htmx:beforeRequest` | Right before `fetch` |
| `htmx:beforeSend` | After headers, before body |
| `htmx:xhr:progress` | Per progress event |
| `htmx:beforeOnLoad` | Response received, before swap; can `e.preventDefault()` |
| `htmx:afterOnLoad` | After successful swap |
| `htmx:beforeSwap` | Just before DOM update; can mutate `e.detail.serverResponse` |
| `htmx:afterSwap` | DOM updated |
| `htmx:beforeHistorySave` | URL change pending |
| `htmx:beforeHistoryUpdate` | History API updated |
| `htmx:load` | New DOM loaded (also OOB) |
| `htmx:responseError` | 4xx/5xx response |
| `htmx:sendError` | Network error |
| `htmx:timeout` | Request exceeded `config.timeout` |
| `htmx:afterRequest` | Always (success or failure) — best for unified error display |

## Triggers

| Trigger | Effect |
|---|---|
| `click` (button default) | Click on element |
| `change` | Input/select change (input default in 2.x) |
| `submit` (form default) | Form submit |
| `load` | Element enters the DOM |
| `revealed` | Scrolled into viewport |
| `intersect` | IntersectionObserver (2.x; was extension `on-intersect`) |
| `intersect once threshold:0.3` | Once, when at least 30% visible |
| `every 5s` | Polling every 5 seconds |
| `mouseenter`, `mouseleave` | Pointer events |
| `keyup[key=='Enter']` | Filter modifier |
| `from:closest <selector>` | Listen on a different element |
| `from:body` | Listen on `<body>` |
| `throttle:200ms`, `delay:250ms` | Timing modifiers |

## Config (htmx.config)

```javascript
htmx.config = {
  // History / cache
  historyEnabled:       true,    // default in 2.x
  historyCacheSize:     20,      // soft bound; old entries cleared per spec
  refreshOnHistoryMiss: true,    // if cached swap missing, full reload
  restoreHistory:       false,
  // Scroll behaviour
  scrollIntoViewOnBoost: true,
  defaultSettleDelay:    100,
  // Network
  timeout:               0,      // ms
  withCredentials:       false,
  selfRequestsOnly:      true,   // same-origin only (2.x: defaults to true)
  // Parsing
  allowEval:             false,  // disable `hx-on::eval`
  allowScriptTags:       false,  // strip <script> from swapped HTML
  inlineScriptNonce:     '',
  // Behaviour
  defaultSwapStyle:      'innerHTML',
  ignoreTitle:           false,
  disableInheritance:    null,   // default = inherit hx-* from parents
  scrollBehavior:        'smooth',
}
```

## 1.x → 2.x deltas

| 1.x | 2.x |
|---|---|
| `hx-on="htmx:afterRequest: ..."` | `hx-on::after-request="..."` |
| `hx-on-intersect` extension | `hx-trigger="intersect"` (built-in) |
| `hx-swap="show:..."` extension | `hx-swap="show:..."` (built-in) |
| `hx-vals='{js:expression()}'` (1.x) | `hx-on::configRequest` mutate `e.detail.parameters` |
| `hx-trigger="intersect root:..."` | `hx-trigger="intersect root:..."` (unchanged) |
| `htmx:configRequest` headers set | Same; now also `htmx:beforeSend` |
| `htmx:load` only after `hx-trigger="load"` | `htmx:load` also fires for OOB swaps (use `htmx:oob-afterSwap` for OOB specifically) |
| `morph` extension 0.x | `hx-ext="morph"` ships with HTMX 2 |
| `view-transition` extension | Ships with HTMX 2 (no install step) |
| `htmx:replaced` not fired | `htmx:afterSettle` (deprecation-resistant) |

## `hx-on::` namespace cheat-sheet

In HTMX 2, every event is namespaced under `hx-on::`:

```html
<!-- any DOM event -->
<button hx-on::click="alert('hi')">Hi</button>

<!-- htmx events -->
<form hx-on::after-request="if(!event.detail.successful) this.classList.add('error')">
  …
</form>

<!-- filter by event detail fields -->
<input hx-on::keyup="if(event.key === 'Enter') this.form.requestSubmit()">
```

For handler strings with double quotes, use `hx-on:htmx:after-request='single-quoted-string'` or escape.

## `hx-swap` modes (with View Transitions)

```html
<!-- crossfade -->
<div hx-get="/api/x" hx-swap="innerHTML"></div>

<!-- crossfade + view transition -->
<div hx-get="/api/x" hx-swap="innerHTML" hx-ext="view-transition"></div>

<!-- snapshot pair named transition -->
<article style="view-transition-name: card-1">…</article>
<article style="view-transition-name: card-1">…</article>  <!-- after the swap -->
```

## SSR response shape (server contract)

A bare fragment, with optional out-of-band swaps:

```html
<!-- returned by /api/search (200 OK) -->
<li>Result 1</li>
<li>Result 2</li>

<!-- optional OOB -->
<span id="result-count" hx-swap-oob="true">42</span>
<title hx-swap-oob="true" hx-head="merge">Search results</title>  <!-- head-support -->
```

Errors should return the appropriate HTTP status (422 for form
validation, 401 for auth, 503 for transient) **with HTML** so htmx
can swap a friendly error fragment in.
