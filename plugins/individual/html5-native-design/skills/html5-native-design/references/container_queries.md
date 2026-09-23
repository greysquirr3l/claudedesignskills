# Container Queries Reference

Container queries let a component adapt its internal layout based on
its *own* size, not the viewport. Browser support: Chrome 105+,
Edge 105+, Firefox 117+, Safari 16+ — universal in 2026.

## The shape

```css
.card {
  container-type: inline-size;
  container-name: card;             /* optional — useful for disambiguation */
}

@container card (min-width: 480px) {
  .card .meta { display: grid; grid-template-columns: 1fr 1fr; }
}
```

`container-type: inline-size` puts the container in a "size
query"-capable state. `container-type: size` covers both axes (less
common; rare in layouts).

## `container-type` values

| Value | Effect |
|---|---|
| `inline-size` | Inline (default block writing) axis is queryable |
| `size` | Both axes queryable; element becomes size-contained |
| `normal` | Default — element is not a container |
| `scroll-state` | Element's scroll position is queryable (`@container scroll-state(...)`) |

## `container-name`

Disambiguates when multiple containers nest:

```css
.outer { container-type: inline-size; container-name: outer; }
.inner { container-type: inline-size; container-name: inner; }

@container outer (min-width: 600px) { … }
@container inner (min-width: 200px) { … }
```

`@container (min-width: 600px)` (no name) applies to the *nearest*
container ancestor; rarely ambiguous if your container names are
distinct.

## Container condition syntax

```css
@container (min-width: 480px) { … }                 /* inline size */
@container (max-width: 480px) { … }
@container (width: 480px) { … }                    /* exact — useful for breakpoints */
@container (min-width: 320px) and (max-width: 480px) { … }
@container (min-width: 320px) or (max-width: 240px) { … }
@container not (min-width: 600px) { … }
@container style(--variant: dark) { … }             /* container-style queries (next gen) */
@container scroll-state(stuck: inline-end) { … }
```

The full set of media features is supported — `aspect-ratio`,
`orientation`, `prefers-color-scheme` (this last only on the
**root** container if it's the page).

## Style and state queries

CSS Container Style Queries let you switch themes based on a
*custom property* set on the container:

```css
.card { container-type: inline-size; container-name: card; }
.card { --variant: light; }

@container card style(--variant: dark) {
  .card { background: #131a20; color: #f1f1f1; }
}

/* Set the variant from somewhere up the tree */
.theme-dark .card { --variant: dark; }
```

Support: Chrome 111+, Edge 111+, Firefox 128+, Safari 18+.

## Scroll-state queries

`@container scroll-state(...)` lets a component react to its own
scroll position without JS:

```css
.scrollable {
  container-type: scroll-state;
  container-name: scroll;
  overflow: auto;
  max-height: 240px;
}

@container scroll(scroll-top: 0) {
  .scrollable::before { content: 'Top ↑'; }
}

@container scroll(stuck: top) {
  .scrollable header { position: sticky; top: 0; background: white; }
}

@container scroll(scrollable: top) {
  .scrollable .top-marker { opacity: 1; }
}
```

Support: Chrome 133+, Edge 133+, Firefox ⏳.

## Container query units

Inside `@container`, you can use **container query units** that are
relative to the container, not the viewport:

| Unit | Relative to… |
|---|---|
| `cqw` | container inline-size (1cqw = 1% of container width) |
| `cqh` | container block-size |
| `cqi` | container inline-size (alias) |
| `cqb` | container block-size (alias) |
| `cqmin` | min of cqi, cqb |
| `cqmax` | max of cqi, cqb |

```css
.card {
  container-type: inline-size;
  font-size: clamp(1rem, 4cqi, 1.5rem);
  padding: 2cqi;
}
```

## How it interacts with the cascade

- `@container` queries follow normal CSS cascade rules. Order
  matters.
- Specificity of `@container` is the same as media queries.
- Container queries **don't** cascade `:has()`-style state out.

## A reusable pattern: components that adapt to their parent's grid

```css
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(320px, 100%), 1fr));
  gap: clamp(1rem, 2vw, 1.5rem);
}
.card {
  container-type: inline-size;
  container-name: card;
  border: 1px solid light-dark(#eee, #1f2630);
  border-radius: .75rem;
  padding: clamp(1rem, 2cqi, 2rem);
  background: light-dark(#fff, #131a20);
}

@container card (min-width: 480px) {
  .card { display: grid; grid-template-columns: 240px 1fr; gap: 2cqi; }
}
@container card (max-width: 479px) {
  .card { display: block; }
  .card .image { margin-bottom: 1rem; }
}
```

The card itself picks its own internal layout. The grid handles the
"where do these go" question.

## Pitfalls

| Pitfall | Fix |
|---|---|
| `@container` not firing | Did you set `container-type` on the ancestor? |
| Inherited media queries still apply | `@media (min-width: 600px)` and `@container (min-width: 600px)` are independent |
| Container goes from `inline-size` to unstyled elements | `inline-size` is a strong spec — the element *must* be set up; missing `container-type` silently disables queries |
| `cqw` units at 0% | The element has 0 inline size (e.g. a column at hidden mobile breakpoint); use a fallback |
| `style()` queries don't match | The ancestor must have the custom property set; custom-property inheritance is by default |
| Shadow DOM container queries | Containers in shadow DOM work; the same constraints apply |

## Cross-references

- [MDN — CSS container queries](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_container_queries)
- [CSS Containment specification](https://drafts.csswg.org/css-contain-3/)
- [web.dev — Container queries](https://web.dev/articles/cq-container-queries)
