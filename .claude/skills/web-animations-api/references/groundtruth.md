# Ground-Truth Examples (greysquirr3l/pattern_lab)

> Sourced 2026-09-23 from
> <https://github.com/greysquirr3l/pattern_lab> @ commit-era around
> 2026-06. Files are copied as-is from the user's working examples;
> treat them as a known-good reference of "what great looks like".

This skill ships with a copy of the
**`2026_scroll_timeline_lab.html`** file from `pattern_lab` so you
can see twelve ground-truth, no-framework scroll-driven animation
examples in their finished state.

**Location in this skill:**
`assets/groundtruth/scroll_timeline_lab.html` (~87 KB).

## What the lab demonstrates

The lab covers exactly the ground covered by this skill — but in a
finished, designerly form:

| # | Section title | Pattern | Maps to SKILL.md § |
|---|---|---|---|
| 1 | Reading progress bar | `scroll-timeline-name` on `html` | Common Patterns §3 |
| 2 | Scroll-reveal entrance | `animation-timeline: view()` | Common Patterns §1 |
| 3 | CSS parallax | named timeline + layer depth | Common Patterns §11 |
| 4 | Horizontal scroll drives a gauge | `scroll-timeline-axis: inline` | (rare; reference-only) |
| 5 | Vertical event timeline | `view() + alternating reveal` | Common Patterns §11 |
| 6 | Conversation timeline | per-bubble `view()` entrance | (advanced; reference-only) |
| 7 | Step progress | per-node `view()` activation | (advanced; reference-only) |
| 8 | Palette rotation | `@property --hue + scroll()` | (advanced; reference-only) |
| 9 | Scroll-peel stickers | `animation-range: contain → exit` | Common Patterns §1 |
| 10 | Warp-speed starfield | scroll-driven streak length | (advanced; reference-only) |
| 11 | Scroll typewriter | `max-width: 0ch → 100%` | (advanced; reference-only) |
| 12 | Card deck deal | `rotateY + translateX + view()` | (advanced; reference-only) |

## Why these examples matter

1. **They complete the picture** — the SKILL.md covers the API;
   these files show finished compositions that use the API.
2. **They bundle the design language** — the pattern_lab uses a
   specific dark-mode palette (`--bg-base: #0a0e27`, neon
   `--neon-cyan`, `--neon-coral`, `--electric-purple`) and
   `--space-{1,2,3,4,6}` tokens. Adopt wholesale or remix.
3. **They show the "wow" without the framework** — every example
   in the lab is native CSS + minimal HTML. No GSAP, no Framer,
   no Motion, no library.

## How to use them in a project

```bash
# Find specific patterns
grep -n "view()" assets/groundtruth/scroll_timeline_lab.html
```

Pick the pattern you like, copy the relevant `<section>` and
`<style>` block into your project, and adapt the colour tokens
to match your theme.

## Re-pull when the user updates pattern_lab

```bash
gh api 'repos/greysquirr3l/pattern_lab/contents/2026_scroll_timeline_lab.html' \
   -q .content | base64 -d > assets/groundtruth/scroll_timeline_lab.html
```

## Note on independence

The SKILL.md is descriptive (the API surface); the lab is
exemplary (what a finished site can look like). The
`assets/scroll_showcase/index.html` and `assets/view_transition_landing/`
demos in this skill are simpler — they're starting points. The
lab is the polished reference.

If a discrepancy ever appears between the lab and the SKILL.md,
the lab is correct (it's the user's working code). Open an issue
or update the SKILL.md to match.
