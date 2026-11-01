"""Parse bio.md and tracker.md. Stdlib only; every other script imports this."""

import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[4]
STATUSES = {"Current", "Behind", "Unverified", "Blocked"}
REQUIRED = ["Headline", "Short", "Summary", "Long", "Roles", "Community", "Certifications"]
COLUMNS = ["Site", "Profile URL", "Text used", "Synced version", "Last checked", "Status", "Notes"]

# (site, section) -> characters allowed, each read off the site's own form.
LIMITS = {
    ("Credly", "Summary"): 600,
    ("dev.to", "Short"): 200,
    ("LinkedIn", "Long"): 2600,
    ("Medium", "Short"): 160,
    ("Google Developers profile", "Long"): 750,
    ("AWS Builder Center", "Short"): 255,
}


def read_bio(path=None):
    """Return (version, {section: raw text}) from bio.md."""
    text = pathlib.Path(path or ROOT / "bio.md").read_text(encoding="utf-8")
    m = re.match(r"---\n(.*?)\n---\n", text, re.DOTALL)
    version = None
    if m:
        v = re.search(r"^version:\s*(\S+)", m.group(1), re.MULTILINE)
        version = v.group(1) if v else None
    sections = {}
    for chunk in re.split(r"^## ", text, flags=re.MULTILINE)[1:]:
        title, _, body = chunk.partition("\n")
        sections[title.strip()] = body.strip()
    return version, sections


def plain(raw):
    """Section text as a site receives it: Markdown autolink brackets removed."""
    return re.sub(r"<(https?://[^>]+)>", r"\1", raw).strip()


def _cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def read_tracker(path=None):
    """Return tracker rows as dicts, in file order, with the header row's columns."""
    text = pathlib.Path(path or ROOT / "tracker.md").read_text(encoding="utf-8")
    lines = [ln for ln in text.splitlines() if ln.startswith("|")]
    if len(lines) < 2:
        return [], []
    header = _cells(lines[0])
    return header, [dict(zip(header, _cells(ln))) for ln in lines[2:]]


def sections_used(row):
    return [s.strip() for s in row.get("Text used", "").split(",") if s.strip()]


def url_of(row):
    return row.get("Profile URL", "").strip("<>")
