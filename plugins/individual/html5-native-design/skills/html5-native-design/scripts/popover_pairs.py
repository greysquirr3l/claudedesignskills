#!/usr/bin/env python3
"""Generate Popover pairs (button + popover) markup.

Each pair is a button with `popovertarget="<id>"` and a div with
`id="<id>" popover="…"`. Use this as scaffolding for dropdowns,
tooltips, and contextual menus.

Usage:
    ./popover_pairs.py                                # interactive picker
    ./popover_pairs.py --pair 'Edit|/api/edit'
    ./popover_pairs.py --pair 'Edit|/api/edit' --auto  # popover=auto
    ./popover_pairs.py --multiple Alice Bob Carla
    ./popover_pairs.py --list
    ./popover_pairs.py --json
"""

from __future__ import annotations
import argparse
import json
import re
import sys
from pathlib import Path


def slugify(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def render_pair(label: str, target_url: str = "", popover: str = "auto") -> str:
    pid = slugify(label)
    url_attr = f' hx-get="{target_url}" hx-target="#{pid}-body"' if target_url else ""
    return (
        f'<!-- popover pair: {pid} -->\n'
        f'<button popovertarget="{pid}" popovertargetaction="toggle"\n'
        f'        class="popover-trigger"'
        f'{url_attr}>{label}</button>\n'
        f'\n'
        f'<div id="{pid}" popover="{popover}" class="popover">\n'
        f'  <header>\n'
        f'    <h3>{label}</h3>\n'
        f'    <button popovertarget="{pid}" popovertargetaction="hide" aria-label="Close">×</button>\n'
        f'  </header>\n'
        f'  <div id="{pid}-body">\n'
        f'    <p>Popover body for {label}. Replace with your content.</p>\n'
        f'  </div>\n'
        f'</div>'
    )


def render_multiple(labels: list[str], popover: str = "auto") -> str:
    return "\n\n".join(render_pair(label, popover=popover) for label in labels)


def render_dialog(label: str, body: str = "") -> str:
    pid = slugify(label)
    return (
        f'<!-- dialog: {pid} -->\n'
        f'<dialog id="{pid}" class="dialog">\n'
        f'  <header>\n'
        f'    <h2>{label}</h2>\n'
        f'  </header>\n'
        f'  <article>{body or "Replace with your content."}</article>\n'
        f'  <form method="dialog" class="actions">\n'
        f'    <button value="cancel">Cancel</button>\n'
        f'    <button value="confirm" autofocus>Confirm</button>\n'
        f'  </form>\n'
        f'</dialog>\n'
        f'\n'
        f'<button onclick="{pid}.showModal()">Open {label}</button>'
    )


CSS_POPOVER = """
/* Default styles for all popovers; override per element as needed. */
.popover {
  border: 1px solid light-dark(#ddd, #1f2630);
  border-radius: .5rem;
  padding: 0;
  margin: 0;
  background: light-dark(#fff, #131a20);
  color: light-dark(#1a1a1a, #f1f1f1);
  box-shadow: 0 8px 24px rgba(0,0,0,.1);

  /* Open/close animation */
  opacity: 0;
  transform: translateY(8px) scale(.985);
  transition: opacity 220ms ease-out,
              transform 280ms cubic-bezier(.2,.8,.2,1),
              overlay 280ms allow-discrete,
              display 280ms allow-discrete;
}

.popover:popover-open {
  opacity: 1;
  transform: none;
}

@starting-style {
  .popover:popover-open {
    opacity: 0;
    transform: translateY(8px) scale(.985);
  }
}

.popover header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.25rem;
  border-bottom: 1px solid light-dark(#eee, #1f2630);
}
.popover header h3 { margin: 0; font-size: 1.125rem; }
.popover > div { padding: 1.25rem; }
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--pair", metavar="LABEL[,URL]",
        help="One popover pair: label 'Edit' or 'Edit|/api/edit'"
    )
    parser.add_argument(
        "--auto", action="store_true",
        help="Use popover='auto' (default; light-dismiss). 'manual' otherwise."
    )
    parser.add_argument(
        "--multiple", nargs="+", metavar="LABEL",
        help="Multiple popovers from labels"
    )
    parser.add_argument(
        "--dialog", metavar="LABEL",
        help="Generate a <dialog> instead of a popover"
    )
    parser.add_argument(
        "--list", action="store_true", help="List example pairs"
    )
    parser.add_argument(
        "--json", action="store_true",
        help="Dump example pairs as JSON"
    )
    parser.add_argument(
        "--with-css", action="store_true",
        help="Also print the recommended CSS"
    )
    args = parser.parse_args()

    if args.list:
        print("\n".join(
            ["- Edit|/api/edit",
             "- Delete|/api/delete",
             "- Share|/api/share",
             "- Settings|/api/settings"]
        ))
        return 0

    if args.json:
        pairs = [
            {"label": "Edit", "url": "/api/edit", "popover": "auto"},
            {"label": "Delete", "url": "/api/delete", "popover": "auto"},
            {"label": "Share", "url": "/api/share", "popover": "auto"},
            {"label": "Settings", "url": "/api/settings", "popover": "manual"},
        ]
        print(json.dumps(pairs, indent=2))
        return 0

    if args.pair:
        if "," in args.pair:
            label, url = args.pair.split(",", 1)
        else:
            label, url = args.pair, ""
        popover = "auto" if args.auto else "auto"
        print(render_pair(label, url, popover=popover))
        if args.with_css:
            print("\n" + CSS_POPOVER)
        return 0

    if args.multiple:
        popover = "auto"
        print(render_multiple(args.multiple, popover=popover))
        if args.with_css:
            print("\n" + CSS_POPOVER)
        return 0

    if args.dialog:
        print(render_dialog(args.dialog))
        if args.with_css:
            print("\n" + CSS_POPOVER)
        return 0

    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
