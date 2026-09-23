# /html5-native-design-form_generator

Generate accessible input markup that pairs the right HTML element, the right `autocomplete` token (from the WHATWG autofill spec), and the right `inputmode` for the field.

## Usage

```
/html5-native-design-form_generator --field email
/html5-native-design-form_generator --profile credit-card
/html5-native-design-form_generator --profile address
/html5-native-design-form_generator --form email password \
    --action /api/signin
/html5-native-design-form_generator --list
/html5-native-design-form_generator --json
```

## Profiles

- `email`, `phone`, `url`, `search`, `otp` — single-field
- `credit-card` — `cc-name`, `cc-number`, `cc-exp`, `cc-csc`
- `address` — `street`, `city`, `state`, `postal`, `country`
- `signin` — `username`, `password`
- `signup` — `email`, `new-password`

## Implementation

Runs `.claude/skills/html5-native-design/scripts/form_generator.py`.

