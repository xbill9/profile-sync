---
name: profile-sync
description: Trigger when checking, updating or rolling out public profiles from bio.md and tracker.md, including "sync my profiles", "update my bio", "check the sites", "add a site", "pull my LinkedIn", a new certification or role to publish, or naming a profile site such as LinkedIn, GitHub, dev.to, Medium, Substack, Credly, AWS Builder Center, g.dev, Advocu or Luma. Covers the per-site routes and limits, exact comparison of each field before saving, live verification and tracker updates.
argument-hint: "[site]"
---

# Syncing public profiles

`bio.md` says what is true. `tracker.md` says where it has landed. Every site gets text from `bio.md`. The job is unattended: finish every site, then report.

Run from the repo root. Scripts are in `.claude/skills/profile-sync/scripts/`.

```bash
python3 .claude/skills/profile-sync/scripts/preflight.py    # bio.md and tracker.md agree; exit 1 if not
python3 .claude/skills/profile-sync/scripts/check-live.py   # live text from every site with a public source
python3 .claude/skills/profile-sync/scripts/payload.py <site> [section]   # the exact text for a site
python3 .claude/skills/profile-sync/scripts/payload.py <site> --js        # JS that compares a field to that text
python3 .claude/skills/profile-sync/scripts/make-avatar.py  # upload sizes of the default picture; needs Pillow
python3 -m unittest discover -s tests                       # the checks themselves
```

Read `references/sites.md` before touching a site. It holds the route, field, limit, save control and verification for each one.

## Three ways a sync goes wrong

**1. A save that looks done and is not.** A click on Done left a Substack bio empty, and a typed URL lost a digit while the page reported a successful save. Verify the field before saving and the live page after. The tool's report of what it typed proves nothing.

**2. Local state mistaken for live state.** A row saying `Current` and a date that matches are claims. `check-live.py` fetches what a visitor gets. Where no public source exists, read the page in Chrome. Two edits on the same day share one `version`, so version equality alone cannot show a site has today's text.

**3. A number copied instead of computed.** The headline said 10x, the About said 9, and each looked fine alone. `preflight.py` counts the `Certifications` list and fails when a claim disagrees. Check the credential at its source, such as Credly, before changing a count.

## Roll out a change

1. Change `bio.md` first and set `version` to today. If a site was edited directly, copy that change back first.
2. Run `preflight.py`. Do not start while it fails.
3. Run `check-live.py` and read `tracker.md` to list what needs work. A site that does not use the changed section takes the new version with no edit, once its row is checked.
4. Do not ask before saving. `bio.md` is the approval. Stop only if live text has something `bio.md` lacks and cannot explain, since an unexplained value is not disposable. A superseded older bio is not that case: replace it.
5. For each approved field:
   - Use the API where it can write. Otherwise use Chrome in a new tab.
   - Scroll to the field with JS, focus it, and confirm `document.activeElement` before any typing.
   - Select the old text and type the payload.
   - Compare the field to `payload.py --js`. Save only on an exact match. If the text does not fit, use the longest existing section that fits. If none fits, add a shorter section to `bio.md` built only from existing sentences.
   - Read the save control's position after scrolling. Positions from an earlier screenshot are stale.
   - Decline any share or announcement prompt the user did not ask for.
6. After each save, reload and compare the live text. Record `Current`, the synced version and the check date only then. If a login, review queue or limit stops the update, mark `Blocked` and explain in Notes.
7. Run `preflight.py` and `check-live.py`, commit straight to `main`, and push. Report which sites are `Current`, `Blocked` or not reached, and anything that went wrong on a public page.

## Add a site

Claim the first free handle from `usernames` in `identity.toml`, trying each in order, and upload `avatar/avatar-800.jpg` where the site still shows a stock picture. Get the public profile URL, since dashboards are private. Read the live text, add a row with `Unverified`, add the site to `identity.toml`, add a section to `references/sites.md`, and add any form limit to `LIMITS` in `biolib.py`. A site with a public read route goes in `live_short()` in `check-live.py`.

## Rules

- This repo is public. Never commit a private email address, phone number, login detail or token. `preflight.py` scans for the first two.
- Renaming a handle on an existing site can break its links, so a site keeps the handle it holds unless the user asks.
- Keep `bio.md` site-neutral. Length variants are sections; per-site copies are not.
- Do not change a site's text when the user asked only for a check.
- Every new failure gets a check in `preflight.py` with a test and a passing control in `tests/`, or a line in `references/sites.md`.
