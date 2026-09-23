# /web-animations-api-waapi_examples

Generate stand-alone HTML examples for WAAPI, CSS scroll-driven animations, and the View Transitions API.

## Usage

```
/web-animations-api-waapi_examples                       # interactive
/web-animations-api-waapi_examples --pattern basic-reveal
/web-animations-api-waapi_examples --pattern scroll-driven-reveal
/web-animations-api-waapi_examples --pattern vt-same-doc
/web-animations-api-waapi_examples --pattern raf-leaderboard
/web-animations-api-waapi_examples --all --out ./out
/web-animations-api-waapi_examples --list
```

Patterns: `basic-reveal`, `stagger`, `spring-ish`, `scrubable`, `dialog-open`, `hover-lift`, `accordion`, `swipe-dismiss`, `morph-vt`, `scroll-driven-reveal`, `reading-progress`, `headline-shrink`, `parallax-bg`, `vt-same-doc`, `vt-cross-doc`, `vt-image-grid`, `reduced-motion`, `raf-leaderboard`.

## Implementation

Runs `.claude/skills/web-animations-api/scripts/waapi_examples.py` directly. Every pattern is a single-file HTML demo.

## Example

```bash
/web-animations-api-waapi_examples --pattern scroll-driven-reveal > scroll.html
open scroll.html
```

