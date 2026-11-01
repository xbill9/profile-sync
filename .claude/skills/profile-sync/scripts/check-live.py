#!/usr/bin/env python3
"""Fetch the sites that expose a profile without a browser and compare with bio.md.

    check-live.py [site ...]

A saved form and a tracker row are local claims; this reads what a visitor gets.
Exit 1 if a site marked Current differs. A site not marked Current that differs is
reported only. Sites with no fetchable source print SKIP and need the browser
check in references/sites.md.
"""

import json
import re
import sys
import urllib.parse
import urllib.request

from biolib import plain, read_bio, read_tracker, url_of


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "profile-sync", "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)


def live_short(site, url):
    """Return the site's live one-line bio, or None if it has no fetchable source."""
    if site == "GitHub":
        return fetch("https://api.github.com/users/" + url.rstrip("/").rsplit("/", 1)[1]).get("bio")
    if site == "dev.to":
        return fetch("https://dev.to/api/users/by_username?url=" + url.rstrip("/").rsplit("/", 1)[1]).get("summary")
    if site == "Substack":
        handle = re.search(r"/@([^/]+)", url).group(1)
        return fetch(f"https://substack.com/api/v1/user/{urllib.parse.quote(handle)}/public_profile").get("bio")
    return None


def main():
    only = {a.lower() for a in sys.argv[1:]}
    _, sections = read_bio()
    want = plain(sections["Short"])
    _, rows = read_tracker()
    bad = 0
    for row in rows:
        site = row["Site"]
        if only and site.lower() not in only:
            continue
        try:
            got = live_short(site, url_of(row))
        except (OSError, ValueError) as e:  # a network failure is a failed check, never a pass
            print(f"  FAIL  {site}: could not read the live profile: {e}")
            bad += row["Status"] == "Current"
            continue
        if got is None:
            print(f"  SKIP  {site}: browser check")
        elif got == want:
            print(f"  OK    {site}: live text matches Short")
        elif row["Status"] == "Current":
            print(f"  FAIL  {site}: marked Current, live text is {got!r}")
            bad += 1
        else:
            print(f"  DIFF  {site} ({row['Status']}): live text is {got!r}")
    print("check-live FAILED" if bad else "check-live OK")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
