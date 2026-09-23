#!/usr/bin/env python3
"""htmx example generator.

Generates stand-alone HTML + minimal CSS + minimal JS snippets for
the most-used HTMX patterns. Useful for quickly scaffolding a new
HTMX-driven site or for pasting into a documentation page.

Usage:
    ./htmx_examples.py                  # interactive pattern picker
    ./htmx_examples.py --pattern boost  # print one pattern to stdout
    ./htmx_examples.py --all           # dump every pattern to ./out/
    ./htmx_examples.py --list           # list available pattern names
    ./htmx_examples.py --version        # print HTMX version pinned by the skill

Patterns included: boost, live-search, infinite-scroll, polling,
modal-popover, tabs, accordion, click-to-load, oob-swap, sse, ws,
file-upload, drag-swap, multi-step-form, table-filter, optimistic-ui,
view-transition-landing.

Each generated snippet uses HTMX 2.0.x from the official CDN and is
self-contained (open the file in a browser to see it work).
"""

from __future__ import annotations
import argparse
import sys
from pathlib import Path

HTMX_VERSION = "2.0.4"
HTMX_CDN = f"https://cdn.jsdelivr.net/npm/htmx.org@{HTMX_VERSION}/dist/htmx.min.js"
HTMX_EXT_HEAD_SUPPORT = (
    f"https://cdn.jsdelivr.net/npm/htmx-ext-head-support@{HTMX_VERSION}/head-support.js"
)
HTMX_EXT_VIEW_TRANSITION = (
    f"https://cdn.jsdelivr.net/npm/htmx-ext-view-transition@{HTMX_VERSION}/view-transition.js"
)
HTMX_EXT_IDIOMORPH = (
    f"https://cdn.jsdelivr.net/npm/htmx-ext-morph@{HTMX_VERSION}/morph.js"
)
HTMX_EXT_SSE = f"https://cdn.jsdelivr.net/npm/htmx-ext-sse@{HTMX_VERSION}/sse.js"
HTMX_EXT_WS = f"https://cdn.jsdelivr.net/npm/htmx-ext-ws@{HTMX_VERSION}/ws.js"
HTMX_EXT_RESPONSE_TARGETS = (
    f"https://cdn.jsdelivr.net/npm/htmx-ext-response-targets@{HTMX_VERSION}/response-targets.js"
)

DOCTYPES = (
    "<!doctype html>\n"
    '<html lang="en">\n'
    '<head>\n'
    '  <meta charset="utf-8">\n'
    '  <meta name="viewport" content="width=device-width,initial-scale=1">\n'
    "  <title>{title}</title>\n"
    '  <script src="{cdn}" defer></script>{extra_scripts}'
    "  <style>{style}</style>\n"
    "</head>\n"
    '<body>\n'
    "{body}\n"
    "</body>\n"
    "</html>\n"
)


def _wrap(title: str, body_html: str, css: str, extra_scripts: str = "") -> str:
    return DOCTYPES.format(
        title=title,
        cdn=HTMX_CDN,
        extra_scripts=f"\n  {extra_scripts}" if extra_scripts else "",
        style=css,
        body=body_html,
    )


# ----------------- patterns -------------------------------------------------


def pattern_boost() -> str:
    body = """
<nav hx-boost="true">
  <a href="/">Home</a>
  <a href="/about">About</a>
  <a href="/contact">Contact</a>
</nav>
<main id="main" hx-target="main" hx-swap="innerHTML show:window:top">
  <h1>Home</h1>
  <p>Click any nav link — the page swap feels native.</p>
</main>
"""
    css = """
body { font: 16px/1.55 system-ui; padding: 2rem; max-width: 720px; margin: 0 auto; }
nav { display: flex; gap: 1rem; padding-bottom: 1rem; border-bottom: 1px solid #eee; }
a { color: #06b6d4; text-decoration: none; }
main.htmx-swapping { opacity: 0; transition: opacity 180ms ease-out; }
.htmx-added { animation: pop 240ms cubic-bezier(.2,.8,.2,1); }
@keyframes pop {
  from { transform: translateY(8px) scale(.985); opacity: 0; }
  to   { transform: none; opacity: 1; }
}
"""
    return _wrap("boost", body, css)


def pattern_live_search() -> str:
    body = """
<input name="q" placeholder="Search…"
       hx-get="/api/search"
       hx-trigger="input changed delay:250ms, keyup[key=='Enter']"
       hx-target="#results"
       hx-swap="innerHTML"
       hx-indicator="#spinner"
       style="width:100%;padding:.5rem .75rem;font-size:1rem;border:1px solid #ddd;border-radius:.5rem">
<span id="spinner" class="htmx-indicator" style="opacity:0;margin-left:.5rem">⏳</span>
<ul id="results" style="list-style:none;padding:1rem 0"></ul>
"""
    css = """
body { font: 16px/1.55 system-ui; padding: 2rem; max-width: 540px; margin: 0 auto; }
.htmx-request.htmx-indicator, .htmx-request .htmx-indicator { opacity: 1; }
.htmx-indicator { transition: opacity 200ms; }
"""
    return _wrap("live-search", body, css)


def pattern_infinite_scroll() -> str:
    body = """
<h1>Feed</h1>
<ul id="feed" style="list-style:none;padding:0">
  <li>Item 1</li><li>Item 2</li><li>Item 3</li><li>Item 4</li>
</ul>
<li hx-get="/api/feed?page=2"
    hx-trigger="intersect once"
    hx-target="#feed"
    hx-swap="beforeend"
    hx-indicator="#bottom-spinner"
    style="padding:1rem;text-align:center;color:#888">Loading more…</li>
<div id="bottom-spinner" class="htmx-indicator" style="text-align:center">⏳</div>
"""
    css = "body { font:16px/1.55 system-ui;padding:2rem;max-width:540px;margin:0 auto; }"
    return _wrap("infinite-scroll", body, css)


def pattern_polling() -> str:
    body = """
<section hx-get="/api/live"
         hx-trigger="every 5s"
         hx-target="this"
         hx-swap="innerHTML"
         hx-indicator="#pulse">
  Loading live data…
</section>
<span id="pulse" class="htmx-indicator"
      style="display:inline-block;width:.5rem;height:.5rem;border-radius:50%;background:#22c55e;opacity:0;margin-left:.5rem"></span>
"""
    css = "body { font:16px/1.55 system-ui;padding:2rem;max-width:540px;margin:0 auto; }"
    return _wrap("polling", body, css)


def pattern_modal_popover() -> str:
    body = """
<button popovertarget="confirm" popovertargetaction="show"
        hx-delete="/api/posts/1"
        hx-target="#status"
        hx-swap="innerHTML"
        hx-confirm="Delete this post?"
        style="padding:.5rem 1rem;border:1px solid #ddd;border-radius:.375rem;background:#fff;cursor:pointer">
  Delete post
</button>
<div id="status" style="margin-top:1rem"></div>

<div id="confirm" popover="auto"
     style="padding:1.5rem;border:1px solid #ddd;border-radius:.5rem;max-width:320px;
            box-shadow:0 8px 24px rgba(0,0,0,.1)">
  <p>Delete this post?</p>
  <button popovertarget="confirm" popovertargetaction="hide">Cancel</button>
  <button onclick="this.dispatchEvent(new CustomEvent('confirm'))"
          style="background:#dc2626;color:#fff">Confirm</button>
</div>
"""
    css = "body { font:16px/1.55 system-ui;padding:2rem;max-width:540px;margin:0 auto; }"
    return _wrap("modal-popover", body, css)


def pattern_tabs() -> str:
    body = """
<div role="tablist">
  <button hx-get="/api/tab/1" hx-target="#tab-panel" hx-swap="innerHTML">Tab 1</button>
  <button hx-get="/api/tab/2" hx-target="#tab-panel" hx-swap="innerHTML">Tab 2</button>
  <button hx-get="/api/tab/3" hx-target="#tab-panel" hx-swap="innerHTML">Tab 3</button>
</div>
<div id="tab-panel" role="tabpanel" style="padding:1rem 0"></div>
"""
    css = """
body { font:16px/1.55 system-ui;padding:2rem;max-width:540px;margin:0 auto; }
[role="tablist"] button { padding:.5rem 1rem;border:1px solid #ddd;background:#fff;cursor:pointer; }
[role="tablist"] button + button { border-left:none; }
[role="tablist"] button:first-child { border-radius:.375rem 0 0 .375rem; }
[role="tablist"] button:last-child  { border-radius:0 .375rem .375rem 0; }
"""
    return _wrap("tabs", body, css)


def pattern_accordion() -> str:
    body = """
<details>
  <summary>Section A</summary>
  <div hx-get="/api/accordion/a"
       hx-trigger="intersect once"
       hx-swap="innerHTML"
       style="padding:1rem 0">
    Loading…
  </div>
</details>
<details>
  <summary>Section B</summary>
  <div hx-get="/api/accordion/b"
       hx-trigger="intersect once"
       hx-swap="innerHTML"
       style="padding:1rem 0">
    Loading…
  </div>
</details>
"""
    css = "body { font:16px/1.55 system-ui;padding:2rem;max-width:540px;margin:0 auto; }"
    return _wrap("accordion", body, css)


def pattern_click_to_load() -> str:
    body = """
<ul id="replies" style="list-style:none;padding:0">
  <li>First reply</li>
  <li>Second reply</li>
</ul>
<button hx-get="/api/replies?after=2"
        hx-target="#replies"
        hx-swap="beforeend">Load more</button>
"""
    css = "body { font:16px/1.55 system-ui;padding:2rem;max-width:540px;margin:0 auto; }"
    return _wrap("click-to-load", body, css)


def pattern_oob_swap() -> str:
    body = """
<form hx-post="/api/messages" hx-target="#log" hx-swap="beforeend" hx-ext="head-support">
  <input name="text" required>
  <button>Send</button>
</form>
<!-- /api/messages returns:
     <div id="log" hx-swap-oob="beforeend">…</div>
     plus an out-of-band <span id="count" hx-swap-oob="true">42</span>
     to update a counter outside this form -->
<ul id="log"></ul>
Counter: <span id="count">0</span>
"""
    css = "body { font:16px/1.55 system-ui;padding:2rem;max-width:540px;margin:0 auto; }"
    return _wrap(
        "oob-swap",
        body,
        css,
        extra_scripts=f'<script src="{HTMX_EXT_HEAD_SUPPORT}" defer></script>',
    )


def pattern_sse() -> str:
    body = """
<h1>Live ticker</h1>
<ul id="ticker" hx-ext="sse" sse-connect="/stream" sse-swap="tick"
    style="list-style:none;padding:0;font:14px ui-monospace,monospace;color:#0891b2">
</ul>
"""
    css = "body { font:16px/1.55 system-ui;padding:2rem;max-width:540px;margin:0 auto; }"
    return _wrap(
        "sse", body, css, extra_scripts=f'<script src="{HTMX_EXT_SSE}" defer></script>'
    )


def pattern_ws() -> str:
    body = """
<h1>Chat (WebSocket)</h1>
<div hx-ext="ws" ws-connect="/ws" style="border:1px solid #eee;border-radius:.5rem;padding:1rem;height:20rem;overflow:auto">
  <div id="chat"></div>
</div>
<form ws-send>
  <input name="text" required>
  <button>Send</button>
</form>
"""
    css = "body { font:16px/1.55 system-ui;padding:2rem;max-width:540px;margin:0 auto; }"
    return _wrap(
        "ws", body, css, extra_scripts=f'<script src="{HTMX_EXT_WS}" defer></script>'
    )


def pattern_file_upload() -> str:
    body = """
<form hx-post="/api/upload"
      hx-target="#upload-status"
      hx-swap="innerHTML"
      enctype="multipart/form-data">
  <input type="file" name="file" required>
  <button>Upload</button>
</form>
<div id="upload-status" style="margin-top:1rem"></div>
"""
    css = "body { font:16px/1.55 system-ui;padding:2rem;max-width:540px;margin:0 auto; }"
    return _wrap("file-upload", body, css)


def pattern_drag_swap() -> str:
    body = """
<ul id="list"
    hx-get="/api/list"
    hx-trigger="load"
    hx-swap="innerHTML"
    style="list-style:none;padding:0">
</ul>
<!-- Server-rendered list items gain draggable=true and
     draggable-target sibling swap markup. See references/server_patterns.md -->
"""
    css = "body { font:16px/1.55 system-ui;padding:2rem;max-width:540px;margin:0 auto; }"
    return _wrap("drag-swap", body, css)


def pattern_multi_step_form() -> str:
    body = """
<form hx-post="/api/checkout"
      hx-target="#checkout"
      hx-swap="outerHTML"
      hx-ext="morph">
  <!-- Step 1 -->
  <fieldset hx-get="/api/checkout/step/2"
            hx-target="this"
            hx-swap="outerHTML"
            hx-trigger="change from:closest fieldset"
            hx-include="this">
    <legend>Shipping</legend>
    <label>Country <input name="country" required></label>
  </fieldset>
</form>
<div id="checkout"></div>
"""
    css = "body { font:16px/1.55 system-ui;padding:2rem;max-width:540px;margin:0 auto; }"
    return _wrap(
        "multi-step-form",
        body,
        css,
        extra_scripts=f'<script src="{HTMX_EXT_IDIOMORPH}" defer></script>',
    )


def pattern_table_filter() -> str:
    body = """
<table id="data"
       hx-get="/api/table"
       hx-trigger="load, keyup delay:200ms changed from:filter-input"
       hx-target="#data"
       hx-swap="outerHTML"
       hx-include="#filter-form">
  <thead><tr><th>Name</th><th>Email</th></tr></thead>
  <tbody><tr><td>Loading…</td><td>…</td></tr></tbody>
</table>
<form id="filter-form">
  <input id="filter-input" name="q" placeholder="Filter…">
</form>
"""
    css = "body { font:16px/1.55 system-ui;padding:2rem;max-width:540px;margin:0 auto; }"
    return _wrap("table-filter", body, css)


def pattern_optimistic_ui() -> str:
    body = """
<form hx-post="/api/likes"
      hx-target="none"
      hx-on::after-request="if(event.detail.successful) this.querySelector('button').textContent='♥ liked'">
  <button>♡ like</button>
</form>
"""
    css = "body { font:16px/1.55 system-ui;padding:2rem;max-width:540px;margin:0 auto; }"
    return _wrap("optimistic-ui", body, css)


def pattern_view_transition_landing() -> str:
    body = """
<body hx-boost="true" hx-ext="view-transition" hx-target="#main" hx-swap="innerHTML">
  <nav style="display:flex;gap:1rem;padding:1rem 2rem;border-bottom:1px solid #eee">
    <a href="/">Home</a>
    <a href="/about">About</a>
    <a href="/contact">Contact</a>
  </nav>
  <main id="main" style="padding:2rem;max-width:720px;margin:0 auto">
    <h1 style="view-transition-name: page-title">Home</h1>
    <p>Click any link — the page swaps with a View Transition.</p>
  </main>
</body>

<style>
  ::view-transition-old(root), ::view-transition-new(root) {
    animation-duration: 280ms;
    animation-timing-function: cubic-bezier(.2,.8,.2,1);
  }
  ::view-transition-group(page-title) {
    animation-duration: 320ms;
  }
</style>
"""
    css = ""
    extra = f'<script src="{HTMX_EXT_VIEW_TRANSITION}" defer></script>'
    return _wrap(
        "view-transition-landing",
        body,
        css,
        extra_scripts=extra,
    )


PATTERNS: dict[str, callable] = {
    "boost": pattern_boost,
    "live-search": pattern_live_search,
    "infinite-scroll": pattern_infinite_scroll,
    "polling": pattern_polling,
    "modal-popover": pattern_modal_popover,
    "tabs": pattern_tabs,
    "accordion": pattern_accordion,
    "click-to-load": pattern_click_to_load,
    "oob-swap": pattern_oob_swap,
    "sse": pattern_sse,
    "ws": pattern_ws,
    "file-upload": pattern_file_upload,
    "drag-swap": pattern_drag_swap,
    "multi-step-form": pattern_multi_step_form,
    "table-filter": pattern_table_filter,
    "optimistic-ui": pattern_optimistic_ui,
    "view-transition-landing": pattern_view_transition_landing,
}


def list_patterns() -> str:
    return "\n".join(f"- {name}" for name in sorted(PATTERNS))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--pattern", choices=sorted(PATTERNS), help="Print one pattern to stdout"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Dump every pattern to ./out/<name>.html",
    )
    parser.add_argument(
        "--list", action="store_true", help="List available pattern names"
    )
    parser.add_argument(
        "--version",
        action="store_true",
        help=f"Print the HTMX version this skill pins ({HTMX_VERSION})",
    )
    parser.add_argument(
        "--out",
        default="./out",
        help="Output directory for --all (default: ./out)",
    )
    args = parser.parse_args()

    if args.list:
        print(list_patterns())
        return 0

    if args.version:
        print(f"HTMX {HTMX_VERSION} (htmx.org 2.x)")
        return 0

    if args.pattern:
        print(PATTERNS[args.pattern]())
        return 0

    if args.all:
        out_dir = Path(args.out)
        out_dir.mkdir(parents=True, exist_ok=True)
        for name, fn in PATTERNS.items():
            (out_dir / f"{name}.html").write_text(fn(), encoding="utf-8")
        print(f"Wrote {len(PATTERNS)} patterns to {out_dir.resolve()}")
        return 0

    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
