---
name: htmx
description: Hypermedia-driven interactivity without a JS framework. Use this skill to build interactive sites using HTMX 2.x for navigation, server communication, and partial-page updates, paired with native HTML/CSS for visual richness. Triggers on tasks involving htmx, hx-get, hx-post, hx-swap, server-rendered hypermedia, partial-page updates, and progressive enhancement without a SPA framework. Pairs with native HTML5 elements and the Web Animations API for sites that feel "alive". Alternative to React/Svelte/Vue SPAs, Barba.js, and Turbolinks for users who want fast, server-driven sites with no build step.
---

# HTMX — Beautiful Hypermedia-Driven Sites

> **Current version**: HTMX **2.0.x** (released 2024-06; 2.x is the
> current stable line). Examples assume **htmx.org 2.0** semantics
> (`hx-on:` namespaced event handlers, the `view-transition` extension
> officially supported, `hx-headers`, `hx-swap-v2` defaults).
> **Audit date**: 2026-09-23.

HTMX turns HTML into a complete client-side runtime: the browser
fetches HTML fragments over HTTP and swaps them into the DOM — no
single-page-app framework required. Combined with modern HTML5
elements, CSS scroll-driven animations, and the View Transitions API,
a server-rendered site can feel as smooth as a heavyweight SPA without
shipping 200+ KB of JavaScript.

**When to use this skill:**

- Building interactive sites with a server-side framework or static
  generator (Flask, Express, Go, Rust/Axum, Django, Rails, Eleventy,
  Astro, Cloudflare Workers, etc.) — anything that can return HTML.
- Replacing a chunky SPA with progressive enhancement, especially when
  the team is small or the build pipeline is overhead.
- Sites where the navigation, forms, and partial updates should work
  even without JavaScript (HTMX is the progressive enhancement layer).
- Server-rendered apps that need slick page transitions, instant
  search, live form validation, infinite scroll, or polling — all
  expressed as HTML attributes.

**When NOT to use it:**

- Heavy client-side state graphs, real-time collaborative editors, or
  rich dashboards that need global fine-grained reactivity. Reach for
  React/Solid/Svelte with a real backend instead, or use HTMX for the
  shell and a single Web Component island for the rich surface.
- Apps that genuinely need an offline shell with a Service Worker;
  HTMX assumes connectivity to the server.

**Companion libraries that go well with HTMX:**

- **Alpine.js** — small (15 KB) for tiny stateful widgets a server
  template can't express (toggles, dropdowns, tabs).
- **petite-vue** — Vue-like API in 6 KB; a slightly fuller Alpine.
- **Hyperscript** — jQuery-for-the-soul event handling in HTML for
  things htmx doesn't directly express (`on click put "..." into me`).
- **Idiomorph** — smarter HTML swap strategy that preserves
  focus/scroll/forms (used by `hx-swap="morph:"` via extension).

---

## Core Concepts

### 1. The htmx mental model

In a classic SPA, the client fetches **data** (JSON) and renders it.
In HTMX, the client fetches **HTML** and swaps it in. The server is
in charge of rendering; the client is in charge of *where* and *when*.
This makes the network and the cache your friends, and removes the
build step.

```html
<!-- Click → fetch /contacts → swap returned HTML into #main -->
<button hx-get="/contacts" hx-target="#main">Load contacts</button>
```

That's an entire interactive flow. The browser does no JSON
serialisation, no virtual DOM diffing, no client-side templating.

### 2. The thirteen attributes that cover 90% of use

| Attribute | Purpose |
|---|---|
| `hx-get` / `hx-post` (and `put/patch/delete`) | Issue a request on a natural event. |
| `hx-target` | CSS selector for the swap destination. Default: the element itself. |
| `hx-swap` | `innerHTML` (default), `outerHTML`, `beforebegin`, `afterend`, `beforeend`, `afterbegin`, `delete`, `none`, or, with the morph extension, `morph:` |
| `hx-trigger` | `click` (default for non-form), `change`, `submit`, `load`, `revealed`, `intersect`, `every 2s`, custom events… |
| `hx-confirm` | Show a JS `confirm()` dialog before issuing the request. |
| `hx-include` | Include additional form fields / element values in the request. |
| `hx-params` | Whitelist/blacklist parameters to send. |
| `hx-vals` / `hx-headers` / `hx-attribute` | Extra JSON params, headers, request-attribute overrides. |
| `hx-swap-v2` *(htmx 2)* | New fine-grained timing controls: `transition`, `swap`, `settle`. |
| `hx-push-url` | Update the URL on swap. Boosts `<a>` and `<form>` into SPA-feeling nav. |
| `hx-boost` | Add to any page to upgrade all `<a>` / `<form>` to AJAX automatically. |
| `hx-indicator` | CSS selector for an element to add `htmx-request` class to during the request. |
| `hx-disabled` | Disable htmx on this subtree (handy inside an existing widget). |

### 3. Natural events: where HTMX "lives"

- **`<button>`** → click triggers the request.
- **`<a>`** → click triggers the request (HTMX prevents the nav).
- **`<form>`** → submit triggers the request (multipart, validation,
  Enter-to-submit all still work).
- **`<input>` / `<textarea>` / `<select>`** → change triggers by default
  in htmx 2.

```html
<form hx-post="/sign-up"
      hx-target="#status"
      hx-swap="innerHTML"
      hx-on::after-request="if(event.detail.successful) this.reset()">
  <input name="email" type="email" required>
  <button>Sign up</button>
</form>
<p id="status" role="status"></p>
```

`hx-on::after-request` is the htmx 2 namespaced event syntax — the
modern replacement for the old `hx-on="htmx:afterRequest: ..."` syntax.

### 4. Targets and swaps

```html
<!-- Append a new row to a list every time the form submits -->
<form hx-post="/messages" hx-target="#messages" hx-swap="beforeend">
  <input name="text" required><button>Send</button>
</form>
<ul id="messages"></ul>
```

Swaps send HTML back from the server. Render **partial templates** —
never send a full document when you can send a fragment. A typical
server function returns:

```python
# Flask example
@app.route("/messages", methods=["POST"])
def post_message():
    msg = Message(body=request.form["text"])
    db.session.add(msg); db.session.commit()
    return render_template("partials/message.html", msg=msg)
```

### 5. Triggers beyond click

htmx 2 recognises the `intersect` trigger (formerly the
IntersectionObserver extension), the `every <duration>` trigger
(polling), and the `from:closest <selector>` modifier:

```html
<!-- Lazy-load on scroll into viewport -->
<section hx-get="/api/section/3" hx-trigger="intersect once">…</section>

<!-- Poll every 5 seconds -->
<div hx-get="/dashboard/live" hx-trigger="every 5s" hx-swap="innerHTML">…</div>

<!-- Click on the closest matching ancestor -->
<table>
  <tr hx-get="/row/1" hx-trigger="click from:closest tr" hx-target="closest td">…</tr>
</table>
```

### 6. Boost: turn the whole site into an SPA

Add `<body hx-boost="true">` (or `hx-boost` on any container) to
upgrade every `<a>` and `<form>` to AJAX automatically. Pair with
`hx-push-url="true"` (the default when boosted) for proper back-button
support and View Transitions below.

```html
<body hx-boost="true" hx-ext="view-transition">
  <nav><a href="/about">About</a></nav>
  <main id="main">…</main>
</body>
```

### 7. Loading & error UI

htmx 2 adds the `htmx-indicator` class to the element matching
`hx-indicator` (or any ancestor with `hx-indicator` set) and removes
it when the request completes. Style it with `opacity` /
`transition`:

```css
.htmx-indicator { opacity: 0; transition: opacity 200ms ease-in; }
.htmx-request .htmx-indicator { opacity: 1; }
.htmx-request.htmx-indicator { opacity: 1; }
```

Error responses automatically trigger the `htmx:responseError` and
`htmx:sendError` events; show a toast in `hx-on::response-error`.

---

## Common Patterns — Beautiful, Reusable, Server-Driven

### 1. The "amazing scroll-driven landing" skeleton

Pair HTMX with the **web-animations-api** skill for the visual layer.
This example pulls a new "scene" each time the user reaches a marker
section:

```html
<main hx-boost="true" hx-target="main" hx-swap="innerHTML show:window:top"
      hx-ext="view-transition">
  <section class="hero" data-animate="reveal">…</section>

  <section hx-get="/api/case-study/1"
           hx-trigger="intersect once threshold:0.4"
           hx-target="this"
           hx-swap="outerHTML">
    <!-- Server renders a placeholder until intersected -->
  </section>

  <section hx-get="/api/case-study/2"
           hx-trigger="intersect once threshold:0.4"
           hx-target="this"
           hx-swap="outerHTML"></section>
</main>
```

The `show:window:top` modifier scrolls the window to the top of the
newly-swapped content — common after a click-to-load navigation.

### 2. Inline CRUD — edit-in-place using `outerHTML` swap

```html
<li id="contact-1">
  <span>Ada Lovelace</span>
  <button hx-get="/contacts/1/edit"
          hx-target="#contact-1"
          hx-swap="outerHTML">Edit</button>
  <button hx-delete="/contacts/1"
          hx-confirm="Delete Ada?"
          hx-target="#contact-1"
          hx-swap="outerHTML"
          hx-headers='{"X-CSRF-Token": "{{csrf}}"}'>Delete</button>
</li>
```

The Edit endpoint returns the contact rendered as a tiny `<form>`
with `hx-put` + `hx-target="#contact-1" hx-swap="outerHTML"` so a
successful save swaps back to the read view without a reload.

### 3. Live search with debounce

```html
<input name="q"
       hx-get="/search"
       hx-trigger="input changed delay:250ms, keyup[key=='Enter']"
       hx-target="#results"
       hx-swap="innerHTML">
<ul id="results"></ul>
```

`delay:250ms` is HTMX's built-in debounce. The additional
`keyup[key=='Enter']` triggers immediate search on Enter.

### 4. Infinite scroll

```html
<ul id="feed">
  <li>… item …</li>
  <li>… item …</li>
  <!-- Sentinel row: fires when it scrolls into view -->
  <li hx-get="/feed?page=2"
      hx-trigger="intersect once"
      hx-target="#feed"
      hx-swap="beforeend"
      hx-indicator="#feed-spinner">
    Loading more…
  </li>
</ul>
<span id="feed-spinner" class="htmx-indicator">…</span>
```

### 5. Polling dashboards / live updates

```html
<section hx-get="/api/live"
         hx-trigger="every 10s"
         hx-swap="innerHTML"
         hx-target="this"></section>
```

Combine with `hx-disinherit` to stop nested updates from re-triggering
the poll, and pair with SSE or WebSockets (via the `sse` and `ws`
extensions) for true server-push.

### 6. Server-Sent Events and WebSockets

The `sse` extension connects an element to an EventSource; the
`event-name` attribute picks the event:

```html
<div hx-ext="sse" sse-connect="/stream" sse-swap="message"
     hx-swap="innerHTML"></div>
```

The `ws` extension connects to a WebSocket and renders each message:

```html
<div hx-ext="ws" ws-connect="/ws">
  <div id="messages" hx-swap-oob="beforeend"></div>
</div>
```

```html
<!-- From the server: send <div id="messages" hx-swap-oob="beforeend">…</div> -->
```

`hx-swap-oob` ("out-of-band") means "swap this fragment outside the
normal flow" — perfect for chat-style UIs.

### 7. Forms with optimistic UI and server-side validation

```html
<form hx-post="/orders"
      hx-target="#order-status"
      hx-swap="innerHTML"
      hx-on::after-request="if(event.detail.failed) this.classList.add('error')">
  <label>Quantity <input name="qty" type="number" min="1"></label>
  <button>Place order</button>
</form>
<div id="order-status" role="status"></div>
```

A 200 response replaces `#order-status` with a success block; a 422
replaces it with the form re-rendered including server-side errors —
htmx doesn't care which, since both target the same element.

### 8. Animating the swap

htmx 2 has built-in CSS-class hooks for the swap lifecycle:

- `htmx-swapping` — applied to the target during request setup.
- `htmx-settling` — applied after the swap, until any view-transition finishes.
- `htmx-added` — applied to newly inserted nodes after settling.

```css
.htmx-swapping { opacity: 0; transition: opacity 200ms ease-out; }
.htmx-added   { animation: htmx-pop 240ms cubic-bezier(.2, .8, .2, 1); }
@keyframes htmx-pop {
  from { transform: translateY(8px) scale(.985); opacity: 0; }
  to   { transform: none; opacity: 1; }
}
```

For full page-transition choreography use the `view-transition`
extension (see [Integration Patterns](#integration-patterns) below).

### 9. The morph extension (idiomorph-backed)

For list/detail swaps where you'd normally lose focus, scroll
position, and form-field state, install `idiomorph` and use:

```html
<li hx-get="/contacts/1/refresh"
    hx-trigger="every 30s"
    hx-target="this"
    hx-swap="morph:outerHTML"
    hx-ext="morph">…</li>
```

`morph:outerHTML` keeps the existing element and patches only what
changed — focus, scroll, and pending input survive the refresh.

### 10. Progressive enhancement that degrades gracefully

Every HTMX attribute is a *progressive enhancement*. Without JS:

- `<form action="/sign-up" method="post">` still works (full reload).
- `<a href="/about">` still navigates.
- `hx-get="/search"` becomes inert (the attribute is unknown).

Test by turning off JavaScript — your site should still be usable,
just less smooth.

---

## Integration Patterns

### 1. HTMX + View Transitions API (page-changes feel native)

Enable the built-in `view-transition` extension. Every swap and
boost becomes a View Transition:

```html
<head>
  <style>::view-transition-old(root), ::view-transition-new(root) {
    animation-duration: 240ms;
    animation-timing-function: cubic-bezier(.2, .8, .2, 1);
  }</style>
</head>
<body hx-boost="true" hx-ext="view-transition">
  <main id="main">…</main>
</body>
```

For per-section choreography, give the swapped content a unique
`view-transition-name`:

```html
<article id="post-42" style="view-transition-name: post-42">…</article>
```

Server returned HTML:

```html
<article id="post-42" style="view-transition-name: post-42">
  <!-- updated body -->
</article>
```

> The same `view-transition-name` on the old and new DOM nodes
> triggers a morph between the two snapshots — combined with the
> web-animations-api skill, this is the single biggest "wow" feature
> available without a JS framework.

### 2. HTMX + Alpine.js for tiny stateful widgets

Alpine handles a small piece of state (a tab index, an open/closed
drawer) that doesn't justify a round trip; HTMX handles round trips
for everything else.

```html
<div x-data="{ open: false }">
  <button @click="open = !open">Filter</button>
  <form x-show="open"
        hx-get="/api/results"
        hx-target="#results"
        hx-swap="innerHTML">
    …inputs…
  </form>
</div>
<div id="results"></div>
```

### 3. HTMX + Web Components (encapsulated islands)

A Web Component can own its own internal state while listening for
htmx events. The component renders once; htmx swaps its content as
needed.

```javascript
class CommentThread extends HTMLElement {
  connectedCallback() {
    this.addEventListener('htmx:afterRequest', (e) => {
      if (e.target === this) this.render()
    })
  }
}
customElements.define('comment-thread', CommentThread)
```

```html
<comment-thread hx-get="/posts/42/comments" hx-trigger="revealed">…</comment-thread>
```

### 4. Server framework quick-picks

Pick what fits the team's deploy story:

| Stack | Library | Notes |
|---|---|---|
| Node + Express | `express` + template engine (`eta`, `nunjucks`, `handlebars`) | Use partial templates. Send `Cache-Control: no-store` for dynamic fragments. |
| Python + Flask | `flask` + `jinja2` | `render_template("partials/foo.html")` returns a fragment. |
| Python + Django | `django` | Use `TemplateResponse` with a custom JSON-or-HTML middleware. |
| Go + net/http | `html/template` | Render partials via named sub-templates. |
| Go + chi/echo | `chi` + templ | `templ` generates strongly-typed Go components that compile to HTML. |
| Rust + Axum | `axum` + `maud` / `askama` | MAUD is HTML-in-Rust; Askama is Jinja-style. |
| PHP + Laravel | `blade` | Use `@include('partials.x')`. |
| Edge / Workers | `hono` + JSX | Lightweight; works on Cloudflare, Deno, Bun. |
| Static + Eleventy | `eleventy` | Pre-render; htmx swaps in dev/preview. |
| Astro | `astro` | HTMX-friendly SSR with islands; pair with Alpine. |

The skill stays framework-agnostic by design — every example can be
ported by swapping the template call.

### 5. CSS pairing for "not-bland" sites

Most "boring" HTMX sites forget to style the htmx classes. Add at
minimum:

```css
.htmx-swapping { opacity: 0; transition: opacity 180ms ease-out; }
.htmx-added    { animation: pop 240ms cubic-bezier(.2, .8, .2, 1); }
.htmx-request  .spinner { opacity: 1; }
```

Pair with the `web-animations-api` and `html5-native-design` skills
for the full visual layer (CSS scroll-driven animations, container
queries, View Transitions, etc.).

---

## Configuration Knobs Worth Knowing

### 1. `htmx.config`

Override defaults globally:

```javascript
htmx.config.historyEnabled = true     // enabled by default in 2.x
htmx.config.scrollIntoViewOnBoost = true
htmx.config.defaultSwapStyle = "outerHTML"
htmx.config.timeout = 8000             // ms before triggering htmx:timeout
htmx.config.allowEval = false          // disable `hx-on::eval` (security)
htmx.config.selfRequestsOnly = true    // refuse cross-origin requests
```

### 2. CSRF

Send the CSRF token on every HTMX request via a global header so
forms don't need to remember it:

```javascript
document.body.addEventListener('htmx:configRequest', (e) => {
  e.detail.headers['X-CSRF-Token'] = document.querySelector('meta[name=csrf]').content
})
```

### 3. Security defaults to set

```javascript
htmx.config.selfRequestsOnly = true      // refuse cross-origin swaps
htmx.config.allowScriptTags = false       // strip <script> from swapped HTML
htmx.config.allowEval = false             // no `hx-on::eval`
htmx.config.historyCacheSize = 20         // bounded history cache
htmx.config.refreshOnHistoryMiss = true   // force a reload if cached swap missing
```

When swapping in user-rendered HTML (markdown → HTML, WYSIWYG),
sanitise server-side and consider `allowScriptTags = false` plus a
CSP `script-src` allow-list.

### 4. `htmx:responseError` and friends

Events you almost always want to listen for:

| Event | Fires when… |
|---|---|
| `htmx:configRequest` | A request is being built (mutate headers/params). |
| `htmx:beforeRequest` | Immediately before fetch. |
| `htmx:afterRequest` | After fetch (success or failure). |
| `htmx:responseError` | 4xx/5xx response. |
| `htmx:sendError` | Network error. |
| `htmx:timeout` | Request exceeded `htmx.config.timeout`. |
| `htmx:load` | New DOM content loaded (in OOBS too). |
| `htmx:beforeSwap` | Last chance to abort or swap silently. |
| `htmx:afterSwap` | DOM updated. |
| `htmx:beforeHistorySave` | URL change pending. |

```javascript
document.body.addEventListener('htmx:responseError', (e) => {
  document.querySelector('#toast')?.replaceChildren(
    Object.assign(document.createElement('p'), { textContent: `Error ${e.detail.xhr.status}` })
  )
})
```

---

## Performance & UX

1. **Always return partial templates** — never a full HTML document
   when a fragment will do. Cache-Control `private, max-age=0` is
   usually correct.
2. **Lazy-load below-the-fold sections** with
   `hx-trigger="intersect once threshold:0.2"`.
3. **Debounce inputs** with `delay:200ms` (search, filter).
4. **Compress transfer** — enable Brotli/gzip on the server; HTMX's
   bytes-on-the-wire is the main "cost" relative to a JSON SPA.
5. **Prefetch on hover** with `hx-get` + `hx-trigger="mouseenter once"`,
   or the prefetch extension. Costs one request per link; saves one
   round-trip per navigation.
6. **Connection-pool websockets** — one WebSocket multiplexes many
   panels by routing server events to specific element IDs.
7. **Inline critical CSS** in the document `<head>` so the first paint
   is instant. htmx.org is ~14 KB minified+gzipped — bundle the JS
   in the same HTML to avoid extra round trips on first load.
8. **Pair with the `view-transition` extension** to make navigations
   feel like a SPA without any SPA framework.

---

## Common Pitfalls

1. **`hx-target` resolving to a deleted ancestor** — common when the
   target is `#main` and you swap the *contents* of `#main`
   (`innerHTML`). After the swap, `#main` is gone; subsequent clicks
   fail. Use `hx-target="#main"` with `hx-swap="innerHTML"`, never
   swap the `#main` element itself.
2. **Forgetting CSRF** — POST/PUT/DELETE without `X-CSRF-Token` will
   be rejected. Add a global `htmx:configRequest` listener.
3. **Returning a full HTML document on an AJAX swap** — the browser
   ignores `<html>` wrappers, but extra `<script>` tags can break
   htmx's parser. Set `allowScriptTags = false` defensively.
4. **Animating the swap with `transition` instead of CSS** — htmx
   removes the old content as soon as the response arrives, so a CSS
   `opacity` transition needs to be on the *old* element via the
   `htmx-swapping` class on the *target*. Use `.htmx-swapping { opacity: 0 }`
   for a graceful fade, or use View Transitions for serious
   choreography.
5. **Polling every Ns causes a thundering herd** — use `every 30s`
   not `every 1s`, jitter with `hx-on::configRequest`, or replace
   with SSE.
6. **History cache filling memory** — set
   `htmx.config.historyCacheSize = 20` and serve
   `Cache-Control: no-store` for sensitive routes.
7. **Forms with file uploads** — htmx 2 sends multipart on POSTs
   containing `<input type=file>` automatically, but you must
   `enctype="multipart/form-data"` *and* your server must accept
   it. JSON endpoints won't work.
8. **`<form>` inside a `<form>`** — invalid HTML; moves the inner
   field out of the outer scope. Use `hx-include` instead.
9. **Carrying `hx-*` through `outerHTML` swaps** — when you swap a
   form, the new form's `hx-*` attributes will trigger too, but
   stale event listeners on the *removed* nodes can still fire
   before GC. Always use `outerHTML` for atomic form replacement.
10. **Search bots and no-JS users** — HTMX degrades, but you must
    still return regular `<a href>` and `<form action>` so crawlers
    and the disabled-JS case work.

---

## Quick Recipes

### "Beautiful toast on every action"

```javascript
document.body.addEventListener('htmx:afterRequest', (e) => {
  const toast = document.querySelector('#toast')
  const ok = e.detail.successful
  toast.textContent = ok ? 'Saved' : `Failed (${e.detail.xhr.status})`
  toast.classList.toggle('toast--ok', ok)
  toast.classList.toggle('toast--err', !ok)
  toast.popover = 'manual'
  toast.showPopover()
  setTimeout(() => toast.hidePopover(), 3000)
})
```

### "Inline search results with keyboard nav"

```html
<input hx-get="/search" hx-trigger="input delay:200ms" hx-target="#results"
       hx-on::after-request="document.querySelector('#results').focus()">
<ul id="results" tabindex="-1">
  <!-- Each result is an <a hx-get=... hx-target=#detail hx-swap=outerHTML> -->
</ul>
```

### "Confirm-after-submit refresh"

```html
<form hx-post="/tasks" hx-swap="none"
      hx-on::after-request="
        if (event.detail.successful) {
          document.getElementById('task-list').dispatchEvent(new CustomEvent('refresh'))
          this.reset()
        }">
  <button>Add task</button>
</form>
<ul id="task-list" hx-get="/tasks" hx-trigger="refresh from:body" hx-swap="innerHTML">
  <!-- initial render -->
</ul>
```

### "Confirmation dialog without `hx-confirm`"

`hx-confirm` is a synchronous `window.confirm()`. For something nicer,
use the Popover API (see `html5-native-design`):

```html
<button hx-delete="/posts/1"
        hx-on::click="document.getElementById('confirm-delete').showPopover()"
        popovertarget="confirm-delete" popovertargetaction="show">Delete</button>
<div id="confirm-delete" popover="manual">
  <p>Delete this post?</p>
  <button onclick="this.getRootNode().host.dispatchEvent(new Event('confirm-yes'))">
    Yes
  </button>
</div>
```

(The actual `hx-delete` only fires once the popover triggers
`htmx:confirm` — use `hx-on::htmx:confirm` or wire it from the
popover's button with a custom event.)

---

## Resources

### Scripts (in this skill)
- `htmx_examples.py` — generate stand-alone htmx snippets for the
  most-used patterns (boost, live search, infinite scroll, modal,
  tabs, accordion, polling, click-to-load, OOB swaps, SSE, WS,
  file upload, drag-and-drop swap, multi-step form, table filtering,
  optimistic UI, view transitions).

### References (in this skill)
- `api_reference.md` — complete attribute/event/config reference with
  htmx 2 defaults and 1.x → 2.x deltas.
- `extensions_reference.md` — built-in and community extensions
  (`view-transition`, `morph`, `head-support`, `preload`,
  `response-targets`, `multi-swap`, `path-deps`, `sse`, `ws`,
  `restored`, `hx-on::`).
- `server_patterns.md` — sample server code for Flask, Express,
  Axum, Hono, and Eleventy: returning fragments, CSRF, content
  negotiation.
- `security_checklist.md` — CSRF / XSS / DOM clobbering /
  history-cache pitfalls with safe defaults.

### Assets (in this skill)
- `assets/starter/` — single-file `index.html` you can open with no
  build step (HTMX from the official CDN).
- `assets/express_demo/` — Express + EJS + HTMX demo with boost,
  infinite scroll, OOB swaps, and a `view-transition` extension
  hook.
- `assets/view_transition_landing/` — the "amazing scroll-driven
  landing" skeleton as a working page.

---

## Related Skills

- `web-animations-api` — WAAPI, CSS scroll-driven animations, and the
  View Transitions API. Pair with HTMX for the visual layer.
- `html5-native-design` — Popover, `<dialog>`, container queries,
  `:has()`, subgrid. Pair with HTMX for the UI primitives.
- `gsap-scrolltrigger` — Use alongside HTMX when you want timeline
  orchestration of swap lifecycles.
- `motion-framer` — Not a natural pair; pick HTMX + WAAPI instead if
  you don't already have a React stack.
- `modern-web-design` — for the visual-design callouts above and
  below the htmx surface.
