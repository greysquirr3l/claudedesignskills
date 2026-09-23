#!/usr/bin/env python3
"""HTML5 form generator.

Generate accessible input markup that pairs the right HTML element,
the right `autocomplete` token (from the WHATWG autofill spec), and
the right `inputmode` for the field.

Usage:
    ./form_generator.py --email            # email field
    ./form_generator.py --search           # search field
    ./form_generator.py --phone            # phone field
    ./form_generator.py --credit-card      # full credit-card form
    ./form_generator.py --address          # full address form
    ./form_generator.py --list             # list supported field names
    ./form_generator.py --json             # JSON of field definitions

Field definitions come from the WHATWG HTML spec "Autofill" section
and WHATWG "inputmode" section. Mobile keyboards and password
managers depend on correct attribute usage.
"""

from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path


# Authoritative WHATWG / W3C autofill tokens
FIELDS: dict[str, dict] = {
    "name":         {"label": "Full name",       "type": "text",  "autocomplete": "name",         "inputmode": "text"},
    "given-name":   {"label": "First name",      "type": "text",  "autocomplete": "given-name",   "inputmode": "text"},
    "family-name":  {"label": "Last name",       "type": "text",  "autocomplete": "family-name",  "inputmode": "text"},
    "email":        {"label": "Email",           "type": "email", "autocomplete": "email",        "inputmode": "email",  "required": True},
    "phone":        {"label": "Phone",           "type": "tel",   "autocomplete": "tel",          "inputmode": "tel"},
    "organization": {"label": "Organisation",    "type": "text",  "autocomplete": "organization", "inputmode": "text"},
    "street":       {"label": "Street address",  "type": "text",  "autocomplete": "street-address", "inputmode": "text"},
    "city":         {"label": "City",            "type": "text",  "autocomplete": "address-level2", "inputmode": "text"},
    "state":        {"label": "State / Province", "type": "text",  "autocomplete": "address-level1", "inputmode": "text"},
    "postal":       {"label": "Postal code",     "type": "text",  "autocomplete": "postal-code",    "inputmode": "text"},
    "country":      {"label": "Country",         "type": "text",  "autocomplete": "country",       "inputmode": "text"},
    "cc-number":    {"label": "Card number",     "type": "text",  "autocomplete": "cc-number",    "inputmode": "numeric", "pattern": "[0-9 ]{13,19}"},
    "cc-exp":       {"label": "Expiration",      "type": "text",  "autocomplete": "cc-exp",       "inputmode": "numeric", "placeholder": "MM / YY"},
    "cc-csc":       {"label": "CVC",             "type": "text",  "autocomplete": "cc-csc",       "inputmode": "numeric", "maxlength": 4},
    "cc-name":      {"label": "Name on card",    "type": "text",  "autocomplete": "cc-name",      "inputmode": "text"},
    "username":     {"label": "Username",        "type": "text",  "autocomplete": "username",     "inputmode": "text", "required": True},
    "password":     {"label": "Password",        "type": "password", "autocomplete": "current-password", "inputmode": "text"},
    "new-password":{"label": "New password",    "type": "password", "autocomplete": "new-password",    "inputmode": "text"},
    "otp":          {"label": "One-time code",   "type": "text",  "autocomplete": "one-time-code", "inputmode": "numeric", "pattern": "[0-9]{4,8}"},
    "search":       {"label": "Search",          "type": "search", "autocomplete": "off",          "inputmode": "search"},
    "url":          {"label": "URL",             "type": "url",   "autocomplete": "url",          "inputmode": "url"},
    "birthday":     {"label": "Birthday",        "type": "date",  "autocomplete": "bday",         "inputmode": "numeric"},
    "color":        {"label": "Colour",          "type": "color", "autocomplete": "off",          "inputmode": "text"},
}


def render_field(name: str, f: dict, indent: str = "  ") -> str:
    attrs = [
        f'type="{f["type"]}"',
        f'name="{name}"',
        f'autocomplete="{f["autocomplete"]}"',
        f'inputmode="{f["inputmode"]}"',
        f'id="f-{name}"',
    ]
    if f.get("required"):
        attrs.append("required")
    if f.get("pattern"):
        attrs.append(f'pattern="{f["pattern"]}"')
    if f.get("placeholder"):
        attrs.append(f'placeholder="{f["placeholder"]}"')
    if f.get("maxlength"):
        attrs.append(f'maxlength="{f["maxlength"]}"')
    enterkeyhint = f.get("enterkeyhint", "next" if name != "search" else "search")
    attrs.append(f'enterkeyhint="{enterkeyhint}"')

    attrs_str = " ".join(attrs)
    return (
        f'{indent}<label>{f["label"]}\n'
        f'{indent}  <input {attrs_str}>\n'
        f'{indent}</label>'
    )


def render_form(field_names: list[str], action: str = "/api/submit", method: str = "post") -> str:
    body = "\n".join(render_field(n, FIELDS[n], indent="  ") for n in field_names)
    return (
        f'<form action="{action}" method="{method}" novalidate>\n'
        f'{body}\n'
        f'  <button type="submit">Submit</button>\n'
        f'</form>'
    )


def render_credit_card() -> str:
    return render_form(["cc-name", "cc-number", "cc-exp", "cc-csc"])


def render_address() -> str:
    return render_form(["street", "city", "state", "postal", "country"])


def render_signin() -> str:
    return render_form(["username", "password"])


def render_signup() -> str:
    return render_form(["email", "new-password"])


PROFILES: dict[str, callable] = {
    "email":         lambda: render_form(["email"]),
    "search":        lambda: render_form(["search"]),
    "phone":         lambda: render_form(["phone"]),
    "credit-card":   render_credit_card,
    "address":       render_address,
    "signin":        render_signin,
    "signup":        render_signup,
}


def list_fields() -> str:
    return "\n".join(f"- {n}: {FIELDS[n]['autocomplete']}" for n in sorted(FIELDS))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--field", choices=sorted(FIELDS), help="Print one field's markup"
    )
    parser.add_argument(
        "--profile", choices=sorted(PROFILES), help="Print a full form by profile"
    )
    parser.add_argument(
        "--form",
        action="append",
        metavar="FIELD",
        choices=sorted(FIELDS),
        help="Add a field to a custom form",
    )
    parser.add_argument("--list", action="store_true", help="List fields")
    parser.add_argument("--json", action="store_true", help="Dump field JSON")
    parser.add_argument(
        "--action", default="/api/submit", help="Form action attribute"
    )
    args = parser.parse_args()

    if args.list:
        print(list_fields())
        return 0

    if args.json:
        print(json.dumps(FIELDS, indent=2, sort_keys=True))
        return 0

    if args.field:
        print(render_field(args.field, FIELDS[args.field]))
        return 0

    if args.profile:
        print(PROFILES[args.profile]())
        return 0

    if args.form:
        print(render_form(args.form, action=args.action))
        return 0

    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
