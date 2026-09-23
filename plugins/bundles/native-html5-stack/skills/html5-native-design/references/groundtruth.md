# Ground-Truth Examples (greysquirr3l/pattern_lab)

> Sourced 2026-09-23 from
> <https://github.com/greysquirr3l/pattern_lab> @ commit-era around
> 2026-06. Files are copied as-is from the user's working examples.

This skill ships with two ground-truth files from `pattern_lab`:

- `assets/groundtruth/html5_apis_lab.html` (~92 KB) — every modern
  Web platform API implemented with the dark navy / neon design
  tokens.
- `assets/groundtruth/periodic_table.html` (~57 KB) — a finished
  interactive periodic table built with native HTML (popovers,
  dialogs, container queries, custom data).

## What the HTML5 APIs lab demonstrates

13 finished Web platform API examples:

| # | Section title | API | Maps to SKILL.md § |
|---|---|---|---|
| 1 | Local Storage | `localStorage` + `storage` event | (advanced; covered by html5-native-design but not as a primary pattern) |
| 2 | Geolocation | `navigator.geolocation.getCurrentPosition` | Web platform APIs |
| 3 | Drag and Drop | native DnD + `draggable` + visual feedback | Web platform APIs |
| 4 | Web Workers | `new Worker(...)` + `postMessage` | Web platform APIs |
| 5 | Intersection Observer | `IntersectionObserver` + CSS classes | (related to `view()` timeline) |
| 6 | Clipboard API | `navigator.clipboard.readText / writeText` | Web platform APIs |
| 7 | Fullscreen API | `element.requestFullscreen` | Web platform APIs |
| 8 | History API | `history.pushState`, `popstate` | (related to HTMX boost) |
| 9 | Web Speech API | `SpeechSynthesis` / `SpeechRecognition` | Web platform APIs |
| 10 | Notification API | `Notification.requestPermission` | Web platform APIs |
| 11 | Page Visibility API | `document.visibilityState` | Web platform APIs |
| 12 | BroadcastChannel API | same-origin pub/sub across tabs | (advanced; reference-only) |
| 13 | Popover API | declarative `popovertarget` + manual pattern | Common Patterns §2 |

> The lab covers twelve APIs this skill doesn't go deep on.
> They're useful references for when a user needs full coverage of
> any of those primitives — point at the lab.

## What the periodic table demonstrates

A complete, finished web page that:

- Uses native `<details>`, container queries, and `:has()` to lay
  out 118 element cards.
- Applies the lab's colour system (oklch-derived tints) per
  chemical-family.
- Adds an animated filter overlay via `popover=manual`.
- Uses native `<dialog>` for the inspector panel.

Read it as a reference for "what can be done without a UI
framework". Each section in the SKILL.md has a peer section in
the lab showing the production design.

## How to use them in a project

```bash
# Find the Popover section in the HTML5 APIs lab
grep -n "popover\|<dialog" assets/groundtruth/html5_apis_lab.html | head
```

```bash
# Find where container queries are used
grep -n "container-type\|@container" assets/groundtruth/periodic_table.html
```

Pick the pattern you like, copy the relevant `<section>` and
`<style>` block, then adapt the colour tokens to your brand.

## Re-pull when the user updates pattern_lab

```bash
gh api 'repos/greysquirr3l/pattern_lab/contents/2026_html5_apis.html' \
   -q .content | base64 -d > assets/groundtruth/html5_apis_lab.html
gh api 'repos/greysquirr3l/pattern_lab/contents/periodic_table.html' \
   -q .content | base64 -d > assets/groundtruth/periodic_table.html
```

## The colour tokens you can lift wholesale

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

These tokens power every example in both files. Adopt them
whole-sale or remix the palette while keeping the spacing scale.

## Note on independence

The SKILL.md is descriptive (the API surface); the lab is
exemplary (a finished page that uses the API). If a discrepancy
appears, the lab is correct.
