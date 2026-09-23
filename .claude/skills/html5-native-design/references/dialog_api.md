# `<dialog>` Element Reference

A first-class modal/notification primitive. `<dialog>` opens, manages
focus trapping, supports modal and non-modal modes, and lives in
the top layer.

## Element shape

```html
<dialog id="confirm">
  <article>
    <h2>Confirm order</h2>
    <p>You're about to place a $42 order.</p>
    <form method="dialog" class="actions">
      <button value="cancel">Cancel</button>
      <button value="confirm" autofocus>Confirm</button>
    </form>
  </article>
</dialog>
```

| Attribute | Effect |
|---|---|
| `open` | Open on initial render |
| `closedby="closerequest"` (Chrome 130+) | Browser handles ESC + click-outside |
| `closedby="none"` | Never closed by browser (you handle ESC/click) |
| `closedby="any"` | Browser closes on clickout too |
| `popover` (Chrome 124+) | Combines `<dialog>` modal with Popover light-dismiss |

## Methods

```javascript
const dlg = document.getElementById('confirm')

dlg.showModal()    // top-layer modal: page becomes inert, focus trap, ESC closes
dlg.show()        // non-modal: renders in top layer but no inert, no focus trap
dlg.close('value')
                 // close with optional returnValue; if user clicked a <button value=…>, that's the value

dlg.open          // boolean — current state
dlg.returnValue   // the value from the closing button (or `close()` arg)

dlg.addEventListener('close', () => {
  console.log(dlg.returnValue)  // 'cancel' | 'confirm' | ''
})
```

## Forms and returnValue

```html
<form method="dialog">
  <button value="cancel">Cancel</button>
  <button value="confirm" autofocus>Confirm</button>
</form>
```

- `method="dialog"` is a submit that closes the dialog instead of
  GETing the form.
- The closing `button`'s `value` attribute is what `dlg.returnValue`
  becomes.
- `autofocus` on the default button means Enter calls it
  immediately.

```javascript
dlg.addEventListener('close', () => {
  if (dlg.returnValue === 'confirm') doTheThing()
})
```

## Style and animation

```css
dialog {
  border: 1px solid light-dark(#ddd, #1f2630);
  border-radius: .75rem;
  background: light-dark(#fff, #131a20);
  color: light-dark(#1a1a1a, #f1f1f1);
  padding: 0;
  margin: auto;
  inset: 0;
  max-width: min(90vw, 480px);

  /* Open / close animation */
  opacity: 0;
  transform: translateY(8px) scale(.985);
  transition:
    opacity 220ms ease-out,
    transform 280ms cubic-bezier(.2,.8,.2,1),
    overlay 280ms allow-discrete,
    display 280ms allow-discrete;
}

dialog[open] {
  opacity: 1;
  transform: none;
}

@starting-style {
  dialog[open] {
    opacity: 0;
    transform: translateY(8px) scale(.985);
  }
}

dialog::backdrop {
  background: transparent;
  transition: background 220ms ease-out;
}

dialog[open]::backdrop {
  background: rgba(0, 0, 0, .45);
}

@supports not (transition-behavior: allow-discrete) {
  dialog { transition: none; }
}
```

`::backdrop` (CSS pseudo) targets the page overlay. Use
`background` and `transition` to fade it in/out.

## Focus management

`showModal()` automatically:
1. Stores the active element.
2. Moves focus to the first `tabindex='0'` or focusable element
   inside, falling back to the dialog itself.
3. Traps focus inside the dialog.
4. On `close()`, restores focus to the stored element.

If you have a primary action, give it `autofocus` so Enter
triggers it:

```html
<button autofocus>Submit</button>
```

## `<dialog popover>` — combine with light-dismiss

Chrome 124+ ships `<dialog popover>` which inherits light-dismiss
from Popover + focus trap + top-layer from `<dialog>`:

```html
<dialog id="m1" popover="auto" closedby="any">
  <p>Closes on click outside.</p>
</dialog>
```

In a multi-modal stack, `<dialog popover="auto">` lets you click
outside to close without binding `keydown` + click-outside handlers.

## `closedby` attribute

| Value | Behaviour |
|---|---|
| (unset) | Browser default — ESC closes; click outside does not |
| `none` | Nothing closes it (you bind ESC/click-outside) |
| `closerequest` | ESC closes; click outside does not |
| `any` | ESC closes; click outside also closes |

This is the recommended way to handle dismissal in modern code —
not custom `keydown` listeners.

```html
<dialog closedby="any" id="m1">…</dialog>
```

```javascript
// To programmatically close
dlg.close()

// "Cancel" event fires for any closure (ESC, click, JS)
dlg.addEventListener('cancel', (e) => {
  // You can preventDefault here for "really sure?" prompts
  if (!confirm('Discard changes?')) e.preventDefault()
})
```

## Accessibility

- `<dialog>` has `role="dialog"` automatically.
- The dialog's heading (`<h2>`) should be referenced via `aria-labelledby`.
- Body content should be referenced via `aria-describedby`.

```html
<dialog aria-labelledby="d-title" aria-describedby="d-body">
  <h2 id="d-title">Confirm order</h2>
  <p id="d-body">You're about to place a $42 order.</p>
  …
</dialog>
```

Screen readers treat modal dialogs as a "modal dialog" landmark and
announce them on open.

## Patterns

### "Confirm dialog"

```html
<dialog id="confirm">
  <form method="dialog">
    <h2>Confirm</h2>
    <p>Are you sure?</p>
    <button value="cancel">No</button>
    <button value="ok" autofocus>Yes</button>
  </form>
</dialog>
<button onclick="confirm.showModal()">Open</button>

<script>
  document.getElementById('confirm').addEventListener('close', (e) => {
    if (e.target.returnValue === 'ok') {
      console.log('User said yes.')
    }
  })
</script>
```

### "Modal with previous-page preservation"

```javascript
// Capture the focused element before showModal
let lastFocus = null
function open(dlg) {
  lastFocus = document.activeElement
  dlg.showModal()
}
function close(dlg) {
  dlg.close()
  lastFocus?.focus()  // restore focus to the trigger
}
```

### "Side drawer (non-modal)"

```html
<dialog id="drawer" class="drawer">
  <header><h2>Details</h2></header>
  <div>…</div>
</dialog>
<button onclick="drawer.show()">Open</button>

<style>
  .drawer {
    margin: 0;
    inset: 0 0 0 auto;     /* right edge */
    height: 100vh;
    width: min(90vw, 400px);
    border-radius: 0;
  }
</style>
```

`show()` (not `showModal()`) keeps the page interactive — useful
for navigation drawers.

### "Toast with `closedby='none'` + auto-close"

```html
<dialog closedby="none" id="toast" class="toast">Saved!</dialog>

<script>
  const t = document.getElementById('toast')
  function show(msg) {
    t.textContent = msg
    t.show()
    setTimeout(() => t.close(), 3000)
  }
</script>
```

## Common pitfalls

| Pitfall | Fix |
|---|---|
| `<dialog>` opens but page is still interactive | You called `show()`, not `showModal()`. Or your CSS targets the wrong elements. |
| Backdrop click doesn't close | Add `closedby="any"` (Chrome 130+) or bind click on backdrop. |
| Animation gets stuck | Use `transition-behavior: allow-discrete` together with `@starting-style`. |
| Form submit doesn't close the dialog | `<form>` must have `method="dialog"` (not `method="post"`). |
| `autofocus` doesn't move focus when dialog reopens | `<button autofocus>` only focuses the *first* time the element gains it; pair with `dlg.querySelector('button').focus()` in your show code. |
| Multiple dialogs stack but `inert` only applies to one | Render one dialog at a time, or layer with `<dialog popover="auto">` (Chrome 124+). |
| `returnValue` is empty after Escape | ESC clears returnValue; check `dlg.open` for the state if you care about the dismissal reason. |

## Cross-references

- [MDN — <dialog>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/dialog)
- [Open UI `<dialog>` proposal](https://open-ui.org/components/dialog.research.html)
- [web.dev — Building a dialog component](https://web.dev/articles/building/a-dialog-component)
