# /html5-native-design-popover_pairs

Generate `popovertarget`+`popover=…` pairs for dropdowns, tooltips, and contextual menus.

## Usage

```
/html5-native-design-popover_pairs --pair 'Edit,/api/edit'
/html5-native-design-popover_pairs --multiple Edit Delete Share
/html5-native-design-popover_pairs --dialog 'Confirm delete'
/html5-native-design-popover_pairs --pair Edit --with-css
/html5-native-design-popover_pairs --list
/html5-native-design-popover_pairs --json
```

## Implementation

Runs `.claude/skills/html5-native-design/scripts/popover_pairs.py`.

## Tips

- `popover=auto` closes on click outside / ESC;   `popover=manual` only closes via a button.
- Stack multiple auto popovers by closing the previous   one automatically.
- Pair with `web-animations-api` View Transitions for   trigger → popover morph: assign matching   `view-transition-name` to both.

