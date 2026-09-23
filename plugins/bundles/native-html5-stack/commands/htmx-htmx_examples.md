# /htmx-htmx_examples

Generate stand-alone HTML snippets for the most-used HTMX patterns.

## Usage

```
/htmx-htmx_examples                              # interactive picker
/htmx-htmx_examples --pattern boost            # one pattern to stdout
/htmx-htmx_examples --pattern live-search
/htmx-htmx_examples --pattern infinite-scroll
/htmx-htmx_examples --pattern view-transition-landing
/htmx-htmx_examples --all --out ./out          # dump all 17 to dir
/htmx-htmx_examples --list                     # list pattern names
/htmx-htmx_examples --version                  # pinned HTMX version
```

Patterns: `boost`, `live-search`, `infinite-scroll`, `polling`, `modal-popover`, `tabs`, `accordion`, `click-to-load`, `oob-swap`, `sse`, `ws`, `file-upload`, `drag-swap`, `multi-step-form`, `table-filter`, `optimistic-ui`, `view-transition-landing`.

## Implementation

Runs `.claude/skills/htmx/scripts/htmx_examples.py` directly. Each snippet uses HTMX **2.0.x** from the official CDN and is self-contained — open the file in a browser to see it work.

## Example

```bash
/htmx-htmx_examples --pattern view-transition-landing > landing.html
open landing.html
```

