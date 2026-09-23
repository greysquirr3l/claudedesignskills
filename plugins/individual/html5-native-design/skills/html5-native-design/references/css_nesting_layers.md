# CSS Nesting and Cascade Layers

Two CSS features that turn modern CSS into a *real* authoring
system: **nesting** for composition, **layers** for cascade control.

## Nesting

CSS Nesting (Chrome 112+, Edge 112+, Firefox 117+, Safari 16.5+) is
SCSS-like nesting that compiles to flat selectors automatically.

```css
.card {
  border: 1px solid #eee;
  border-radius: .5rem;

  & h2 {
    margin: 0 0 .5rem 0;
    font-size: 1.25rem;
  }

  & p {
    margin: 0;
    opacity: .8;

    & a {
      color: var(--accent);
    }
  }

  &:hover,
  &:focus-within {
    border-color: var(--accent);
  }

  &::before {
    content: '';
    display: block;
  }
}
```

### Rules

- `&` references the parent selector. Required at the start of nested
  rules.
- **`@media` queries nest naturally** — no need to wrap the whole
  rule.
- **`@container`, `@supports`, `@layer`** all nest too.
- **No `&` required for at-rules** that don't take a selector.
- Specificity is exactly what the flattened output would be.

```css
/* @media nests */
.card {
  display: block;
  @media (min-width: 600px) {
    display: grid;
    grid-template-columns: 240px 1fr;
  }
}

/* @container nests */
.card { container-type: inline-size; }
@container (min-width: 480px) {
  .card {
    display: grid;
    & .meta { display: grid; grid-template-columns: 1fr 1fr; }
  }
}
```

### Why use it

- Cuts lines and indentation cleanly for component-based CSS.
- Lets you co-locate media queries with the rule that triggers them.
- Matches the visual structure of the component.

### Pitfalls

| Pitfall | Fix |
|---|---|
| `&` missing | Add `&` at the start of nested selectors |
| `&` doesn't compose visually with `&` chains like `& + &` | Use `&` to anchor; the second `&` becomes the prev sibling's selector |
| Nested `@layer` creates a new layer, not a sublayer | Always declare layers at the top of the stylesheet |
| Selector list can't start with `&` and a combinator | `& > .x { ... }` — yes; `> .x { ... }` — no |

## Cascade Layers (`@layer`)

`@layer` (Chrome 99+, Edge 99+, Firefox 97+, Safari 15.4+) orders
sections of CSS by importance *deterministically*, regardless of
specificity or source order.

```css
@layer reset, base, components, utilities;

/* Later layers win; layer order is set by the @layer declaration above */
@layer reset { html { margin: 0; padding: 0; } }
@layer base { body { font: 16px/1.5 system-ui; } }
@layer components { .button { padding: .5rem 1rem; } }
@layer utilities { .button { padding: 2rem 1rem; } /* wins — utilities trumps components */ }
```

A component layer that sets `.button { padding: .5rem 1rem }` will
be overridden by a `.button { padding: 2rem }` in `utilities` —
*even if the component has higher specificity*.

### Layer order rules

1. **First declaration wins**: `@layer a, b, c;` puts `a` first (lowest).
2. **Order matters**: later layers win over earlier.
3. **Anonymous layers**: `@layer { ... }` without a name — useful
   for first-touch declarations.
4. **`!important` flips the order**: layers matter for specificity
   among non-`!important` rules; among `!important` rules, later
   layers win first.

### Layer rules for component CSS

```css
@layer reset, base, tokens, components, utility;

@layer reset { /* … */ }
@layer base { /* … */ }

@layer tokens {
  :root {
    --bg: #fafafa;
    --fg: #1a1a1a;
  }
}

@layer components {
  .card {
    background: var(--bg);
    color: var(--fg);
    padding: 1rem;
    border: 1px solid light-dark(#eee, #1f2630);
  }
}

@layer utility {
  .card-large { padding: 2rem; }
}
```

Inside `components`, you can rely on `utility` rules to override
defaults — and the user can write `@layer components, utility;` to
swap their order without rewriting the components themselves.

### Sub-layers

```css
@layer reset, components;

@layer components {
  @layer forms, layouts, buttons;
  /* Now: reset < forms < layouts < buttons */
}
```

`@layer forms { … }` inside `components` defines a sub-layer. The
resulting order is `reset < components.forms < components.layouts <
components.buttons`. Useful when a single file has multiple
component kinds.

### `@import` and layer order

```css
@import url(reset.css) layer(reset);
@import url(theme.css) layer(theme);

@layer components { … }
```

### Pitfalls

| Pitfall | Fix |
|---|---|
| Layers declared late go to the top of the order | Always declare the full layer order at the top of your stylesheet |
| `!important` reverses the order | Reserve `!important` for theme/utility overrides |
| `@layer` blocks don't reset by source order within themselves | Source order within a layer is the same as before — only cross-layer order is overridden |
| Anonymous layers can't be referenced | Name every layer you'd want to import or invert |

## Cross-references

- [CSS Nesting specification](https://drafts.csswg.org/css-nesting-1/)
- [Cascade Layers specification](https://drafts.csswg.org/css-cascade-5/#layering)
- [MDN — @layer](https://developer.mozilla.org/en-US/docs/Web/CSS/@layer)
- [web.dev — Cascade layers](https://web.dev/articles/cascade-layers)
