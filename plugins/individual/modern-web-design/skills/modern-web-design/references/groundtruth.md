# Ground-Truth Examples (greysquirr3l/pattern_lab)

> Sourced 2026-09-23 from
> <https://github.com/greysquirr3l/pattern_lab> @ commit-era around
> 2026-06. Files are copied as-is from the user's working examples.

This skill ships with two ground-truth files from `pattern_lab`:

- `assets/groundtruth/pattern_lab_2026.html` (~89 KB) — every
  modern design pattern the user has catalogued for 2026:
  typography, colour, depth, bento grids, focus states, glass,
  container queries, `:has()`, and OKLCH.
- `assets/groundtruth/nth_letter_lab.html` (~46 KB) — the
  `nth-letter` typography trick (custom-property-driven letter
  tinting).

## What the 2026 pattern lab demonstrates

The 2026 pattern lab showcases every modern web-design primitive
this skill documents, in their finished state:

| Section | Maps to this skill's section |
|---|---|
| Tracking & Kinetics | Typography Physics |
| Tactile & Contextual buttons | Button Architecture |
| Nested Corner Math | Border radius with `calc()` and `--radius-cell` |
| Depth Without Shadows | Borderless depth via layering |
| Cyber Gradients & Tints | Colour Theory |
| Line Length: The 65ch Rule | Readability |
| Focus States | Accessibility |
| OKLCH: Perceptually Uniform Color | Colour System 2026 |
| Glassmorphism | Visual Depth 2026 |
| Bento Grid | Layout 2026 |
| Container Queries | Responsive Design 2026 |
| `:has()` Parent Selector | CSS Selectors 2026 |
| (and more — tracking, scroll-driven, animation primitives) |  |

## What the nth-letter lab demonstrates

The `::nth-letter` CSS pseudo-element isn't shipped yet (it's a
[CSS Pseudo-Elements Module Level 4 proposal](https://drafts.csswg.org/css-pseudo-4/)
that's been gestating). The pattern_lab fakes it with per-glyph
element wrappers + custom properties. The result: **twelve pure-CSS
typography effects** that would normally need JavaScript libraries.

| # | Section title | Highlight trick |
|---|---|---|
| 1 | Alternating skew | `::nth-letter(odd\|even)` parity |
| 2 | Spectral hue | `oklch()` + index rotation through the colour wheel |
| 3 | Kinetic wave | `animation-delay × index` |
| 4 | Every third glyph | `::nth-letter(3n)` modular count |
| 5 | Reactive bloom | `:hover` + `:has()` |
| 6 | Travelling shimmer | staggered glow / mask |
| 7 | Neon flicker | per-glyph random duration |
| 8 | Solari flip board | `perspective + rotateX` |
| 9 | Chromatic glitch | `text-shadow + jitter` |
| 10 | Typewriter dissolve | `transition-delay` reversal |
| 11 | Bulge sweep | `scaleX` wave + squash |
| 12 | Dust accumulation | `blur + translateY` halos |

Useful for advanced typography work, especially headings and short
text where each character is a typographic unit (logo-style
treatments, hero typography, badges).

> **Note**: every one of these effects ships **zero JS**. Open
> the lab in DevTools and search for `<script` — there's none.
> It's the strongest demonstration of "what's possible without a
> framework" in the entire pattern_lab.

## How to use them

```bash
# Find glassmorphism
grep -n "backdrop-filter\|glassmorphism" assets/groundtruth/pattern_lab_2026.html

# Find OKLCH examples
grep -n "oklch\|oklab" assets/groundtruth/pattern_lab_2026.html

# Find nth-letter
grep -n "nth-letter\|letter-spacing" assets/groundtruth/nth_letter_lab.html
```

Pick the section you like, copy the `<style>` block, then adapt
the colour tokens to your brand.

## Re-pull when the user updates pattern_lab

```bash
gh api 'repos/greysquirr3l/pattern_lab/contents/2026_pattern_lab.html' \
   -q .content | base64 -d > assets/groundtruth/pattern_lab_2026.html
gh api 'repos/greysquirr3l/pattern_lab/contents/2026_nth_letter_lab.html' \
   -q .content | base64 -d > assets/groundtruth/nth_letter_lab.html
```

## Colour tokens you can lift wholesale

```css
:root {
  --bg-base:              #0a0e27;   /* deep navy */
  --bg-surface:           #131836;
  --bg-surface-highlight: #1c2345;

  --text-primary:   #fafbfc;
  --text-secondary: #94a3b8;

  --neon-cyan:       #00f5ff;
  --neon-coral:      #ff006e;
  --electric-purple: #764ba2;

  --space-1: 8px;
  --space-2: 16px;
  --space-3: 24px;
  --space-4: 32px;
  --space-6: 48px;

  --border-light: rgba(255, 255, 255, 0.08);
}
```

These tokens power every example in both files.

## Note on independence

The SKILL.md is descriptive (the design principles); the lab is
exemplary (a finished design system). If a discrepancy appears,
the lab is correct — it's the user's working code.
