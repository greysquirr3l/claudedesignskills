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
finished, designerly form. Twelve demos live at
<https://greysquirr3l.github.io/pattern_lab/2026_scroll_timeline_lab.html>
under the heading "CSS `scroll-timeline` Lab". The lab opens with a
useful framing: "Before `animation-timeline`, every scroll-linked
effect required JavaScript — a scroll event listener, throttling with
`requestAnimationFrame`, manual progress calculation, and DOM
updates on every tick."

| # | Section title (verbatim from lab) | Highlight technique |
|---|---|---|
| 1 | Reading progress bar | `scroll-timeline-name` on `html` |
| 2 | Scroll-reveal entrance | `animation-timeline: view()` |
| 3 | CSS parallax | named timeline + layer depth |
| 4 | Horizontal scroll drives a gauge | `scroll-timeline-axis: inline` |
| 5 | Vertical event timeline | `view()` + alternating reveal |
| 6 | Conversation timeline | per-bubble `view()` entrance |
| 7 | Step progress | per-node `view()` activation |
| 8 | Palette rotation | `@property --hue + scroll()` |
| 9 | Scroll-peel stickers | `animation-range: contain → exit` |
| 10 | Warp-speed starfield | scroll-driven streak length |
| 11 | Scroll typewriter | `max-width: 0ch → 100%` |
| 12 | Card deck deal | `rotateY + translateX + view()` |

The lab also includes a Core Insight callout: "Scroll-driven
animations don't replace `@keyframes` — they replace the **clock**
that drives them. Swap elapsed time for scroll position, and the
same keyframe that fades in a modal now fades in a card as it
enters the viewport. That single conceptual swap — combined with
`@property` for animatable custom properties and `timeline-scope`
for cross-DOM reach — unlocks palette rotation, warp-speed
starfields, typewriters, 3D card decks, and peel effects. All pure
CSS. All on the compositor thread."

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
