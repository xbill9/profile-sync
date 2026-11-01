#!/usr/bin/env python3
"""Fail the run if bio.md or tracker.md is wrong. Exit 1 on any failure.

    preflight.py [--bio PATH] [--tracker PATH]

Counts are computed here, never by the model: the certification count in the
headline and Long is compared with the list it claims to summarise.
"""

import argparse
import datetime
import re
import sys

from biolib import (
    COLUMNS,
    LIMITS,
    REQUIRED,
    STATUSES,
    plain,
    read_bio,
    read_tracker,
    sections_used,
    url_of,
)

EMAIL = re.compile(r"(?<![/\w.-])[\w.+-]+@[\w-]+\.[\w.-]+")
PHONE = re.compile(r"\+\d[\d ().-]{7,}\d|\(\d{3}\) ?\d{3}[ .-]\d{4}|(?<![\w/-])\d{3}[ .-]\d{3}[ .-]\d{4}(?![\w/-])")
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def check(version, sections, header, rows, today=None):
    """Return a list of failure strings. Empty means the files are consistent."""
    fails = []
    today = today or datetime.datetime.now().astimezone().date().isoformat()

    if not version or not DATE.match(version):
        fails.append(f"bio.md: version {version!r} is not YYYY-MM-DD")
    elif version > today:
        fails.append(f"bio.md: version {version} is after today {today}")

    for name in REQUIRED:
        if not sections.get(name):
            fails.append(f"bio.md: section {name} is missing or empty")
    for name, body in sections.items():
        if re.search(r"\b(TODO|TBD)\b", body):
            fails.append(f"bio.md: section {name} has a placeholder")

    listed = sum(ln.rstrip().endswith("(Google Cloud)") for ln in sections.get("Certifications", "").splitlines())
    claims = [
        ("Headline", r"(\d+)x Google Cloud Certified"),
        ("Long", r"hold (\d+) (?:official )?Google Cloud certifications"),
        ("Summary", r"hold (\d+) (?:official )?Google Cloud certifications"),
    ]
    for name, pattern in claims:
        m = re.search(pattern, sections.get(name, ""))
        if m and int(m.group(1)) != listed:
            fails.append(f"bio.md: {name} claims {m.group(1)} Google Cloud certifications, the list has {listed}")

    for name, body in sections.items():
        for rx, label in ((EMAIL, "email address"), (PHONE, "phone number")):
            if rx.search(body):
                fails.append(f"bio.md: section {name} contains a possible {label}")

    if header != COLUMNS:
        fails.append(f"tracker.md: columns are {header}, expected {COLUMNS}")
    seen = set()
    for row in rows:
        site = row.get("Site", "?")
        status = row.get("Status", "")
        if site in seen:
            fails.append(f"tracker.md: {site} appears twice")
        seen.add(site)
        if status not in STATUSES:
            fails.append(f"tracker.md: {site} has status {status!r}")
        for cell in row.values():
            for rx, label in ((EMAIL, "email address"), (PHONE, "phone number")):
                if rx.search(cell):
                    fails.append(f"tracker.md: {site} contains a possible {label}")
        for name in sections_used(row):
            if name == "none":
                continue
            if name not in sections:
                fails.append(f"tracker.md: {site} uses section {name}, which bio.md lacks")
            limit = LIMITS.get((site, name))
            if limit and len(plain(sections.get(name, ""))) > limit:
                fails.append(f"tracker.md: {site} allows {limit} characters in {name}, the text has {len(plain(sections[name]))}")
        if status == "Current":
            if row.get("Synced version") != version:
                fails.append(f"tracker.md: {site} is Current at {row.get('Synced version')}, bio.md is {version}")
            if not DATE.match(row.get("Last checked", "")):
                fails.append(f"tracker.md: {site} is Current with no live check date")
            if not url_of(row).startswith("http"):
                fails.append(f"tracker.md: {site} is Current with no profile URL")
        if status == "Blocked" and not row.get("Notes"):
            fails.append(f"tracker.md: {site} is Blocked with no explanation in Notes")
    return fails


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bio")
    ap.add_argument("--tracker")
    args = ap.parse_args()
    version, sections = read_bio(args.bio)
    header, rows = read_tracker(args.tracker)
    fails = check(version, sections, header, rows)
    for f in fails:
        print(f"  FAIL  {f}")
    counts = {s: sum(r.get("Status") == s for r in rows) for s in sorted(STATUSES)}
    print(f"bio.md {version}, {len(rows)} sites: {counts}")
    print("preflight FAILED" if fails else "preflight OK")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
