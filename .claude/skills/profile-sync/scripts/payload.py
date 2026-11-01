#!/usr/bin/env python3
"""Print the exact text a site receives, and JavaScript that proves a field holds it.

    payload.py <site> [section]      text, with its character count on stderr
    payload.py <site> --js           one JS function, verify(value), per section

Typing into a form drops characters, so a field is compared with this text before
every save. The JS carries the text base64-encoded, which survives quotes, emoji
and newlines.
"""

import base64
import sys

from biolib import plain, read_bio, read_tracker, sections_used


def text_for(site, section=None):
    _, sections = read_bio()
    _, rows = read_tracker()
    row = next((r for r in rows if r["Site"].lower() == site.lower()), None)
    if row is None:
        sys.exit(f"no tracker row for {site}")
    used = [section] if section else sections_used(row)
    return {name: plain(sections[name]) for name in used}


def main():
    args = [a for a in sys.argv[1:] if a != "--js"]
    if not args:
        sys.exit(__doc__)
    texts = text_for(args[0], args[1] if len(args) > 1 else None)
    for name, text in texts.items():
        print(f"{name}: {len(text)} characters", file=sys.stderr)
        if "--js" in sys.argv:
            b64 = base64.b64encode(text.encode()).decode()
            print(
                f"// {name}\nconst want=new TextDecoder().decode(Uint8Array.from(atob('{b64}'),c=>c.charCodeAt(0)));\n"
                "const norm=s=>s.replace(/\\s+/g,' ').trim();\n"
                "const verify=v=>({exact:norm(v)===norm(want),len:v.length,want:want.length});"
            )
        else:
            print(text)


if __name__ == "__main__":
    main()
