# Profile Sprawl: Solving a Problem You Didn't Know You Had

*Subtitle: Every public profile you own says something slightly different about you. A step by step guide to treating your bio as source code, with one file, one tracker and an agent skill that checks the live sites.*

This article provides a step by step guide to keeping a public web presence consistent across many sites. An agent skill for Claude Code is built that treats a bio as source code: one file holds the facts, one table records where it has landed, and scripts read the live sites to confirm it.

https://github.com/xbill9/profile-sync

**Every profile you own is a copy of your bio, and copies drift. The fix is the one software already uses: a single source, a status table and a check that reads production.**

---

#### What Is Profile Sprawl?

A working developer collects profiles. LinkedIn, GitHub, Medium, dev.to, Substack, a certification wallet, a community portal, a program dashboard. Each one was accurate on the day you filled it in.

Profile sprawl is what happens next. A new role or credential goes on the site you happened to have open, and the rest keep the old text. No site reports an error, because each one is internally fine. The inconsistency exists only across sites, and nobody reads them side by side except a recruiter, a conference organizer or a reviewer.

---

#### How Bad Could It Be?

One audit of ten profiles belonging to one person, read on 2026-10-31, the day after a new certification was issued:

| Site | Certifications | Years of experience |
| --- | --- | --- |
| LinkedIn headline | 10 | |
| LinkedIn About | 9 | over 30+ |
| Medium | 9 | 20+ |
| Google Developers profile | 9 | 20+ |
| Credly | 9 | 20+ |
| Advocu | 9 | |

The same LinkedIn profile disagreed with itself. The headline said 10 and the About said 9, and each line looked fine alone.

The other four sites had a different problem. AWS Builder Center listed 0 credentials, dev.to held a tagline, GitHub held an unexplained string, and Substack was empty apart from the platform's default text.

---

#### At This Point You Should Have

- A list of your public profiles and a browser where you are logged in to them
- Python 3, with no extra packages
- [Claude Code](https://claude.ai/code) with the Chrome extension, or the patience to run the same steps by hand
- A git repository, which can be public as long as it holds public text only

---

#### Step 1 — Write One Source File

`bio.md` holds everything a site could need, in plain Markdown with no site-specific syntax. Facts are lists. Text comes in lengths, written from those facts.

```markdown
---
version: 2026-10-31
---

# Bio

## Headline
## Tagline
## Short
## Summary
## Long
## Roles
## Community
## Certifications
## Education
## Links
```

Three lengths cover every form measured here: Short at 133 characters, Summary at 561 and Long at 735. A site gets its own text only when a limit forces it, and even then the shorter text becomes a section of the file. Per-site copies are how sprawl starts.

The rule that keeps this working: a change starts in `bio.md`, never on a site. If a site was edited directly, that change is copied back first.

---

#### Step 2 — Track Where It Has Landed

`tracker.md` is one table with one row per site. Status takes one of four values.

| Status | Meaning |
| --- | --- |
| Current | Synced version matches `bio.md` and the live profile was checked |
| Behind | The site has an older version |
| Unverified | Nobody has compared this site to `bio.md` yet |
| Blocked | Something outside your control stops the update, explained in Notes |

The **Text used** column records which sections a site takes. A change to Long reaches only the sites that use Long, and every other row moves to the new version with no edit.

---

#### Step 3 — Make the Computer Do the Counting

`preflight.py` compares the two files and exits 1 on any disagreement. It counts the `Certifications` list and compares that count with every claim in the text, so a number in a headline can never drift from the list it summarizes.

```text
$ python3 .claude/skills/profile-sync/scripts/preflight.py
bio.md 2026-10-31, 10 sites: {'Behind': 0, 'Blocked': 1, 'Current': 9, 'Unverified': 0}
preflight OK
```

It also fails on a text longer than a site's form allows, a `Current` row with no check date, and a status outside the four values. The repository is public, so it scans both files for email addresses and phone numbers too.

Arithmetic belongs in code. A model or a person can miscount a list. A script compares 10 with 10.

---

#### Step 4 — Read the Live Sites

A tracker row is a claim. `check-live.py` fetches what a visitor gets from each site with a public source and compares it with `bio.md`.

```text
$ python3 .claude/skills/profile-sync/scripts/check-live.py
  SKIP  LinkedIn: browser check
  OK    GitHub: live text matches Short
  SKIP  Medium: browser check
  OK    dev.to: live text matches Short
  OK    Substack: live text matches Short
  SKIP  AWS Builder Center: browser check
  SKIP  Google Developers profile: browser check
  SKIP  Google Cloud Skills Boost: browser check
  SKIP  Credly: browser check
  SKIP  Advocu: browser check
check-live OK
```

A site marked `Current` that differs fails the run. A check that can only pass proves nothing, so the same script was run against a stale value to confirm it exits 1.

---

#### Step 5 — Measure Every Form

Each site has its own field, limit and save button. These are read from the forms themselves, and they live in one reference file so the next run starts with them.

| Site | Field | Limit |
| --- | --- | --- |
| Medium | Short bio | 160 |
| dev.to | Bio | 200 |
| AWS Builder Center | About | 255 |
| Credly | Personal Summary | 600 |
| Google Developers profile | Bio | 750 |
| LinkedIn | About | 2,600 |

A property of one site is evidence about that site only. The Long text at 735 characters fits 2 of these fields and fails the other 4, so the limits go in `biolib.py` and `preflight.py` enforces them before any browser opens.

---

####  Tip: Reading and Writing Are Different Routes

dev.to has a good API, and a key reads the profile with no trouble. Profile fields are read-only there: `PUT` and `PATCH` on `/api/users/me` return 404, so the bio is saved through the settings page. Test both directions before planning a rollout around an API.

---

#### Step 6 — Compare Before Saving

Browser automation can drop a character while reporting success, and a page can show a success message for the wrong text. So each save follows the same order:

1. Scroll to the field and confirm it has focus.
2. Select the old text and type the new text.
3. Compare the field with the exact payload from `bio.md`.
4. Read the position of the save button after scrolling.
5. Save, reload and compare the live text.

`payload.py` supplies step 3. It prints the text for a site, or a small JavaScript function that compares a field with it. The text travels base64-encoded, which survives quotes, emoji and line breaks.

```text
$ python3 .claude/skills/profile-sync/scripts/payload.py Credly > /dev/null
Summary: 561 characters
```

---

####  Tip: Decline the Announcement

Adding a certification on LinkedIn opens a prompt to post about it to your network. Updating a profile and announcing to it are separate decisions. The skill clicks Skip unless an announcement was requested.

---

#### Step 7 — Package It as a Skill

The steps above become an agent skill, in the shape of [publishing-kit](https://github.com/xbill9/publishing-kit):

```text
.claude/skills/profile-sync/
  SKILL.md               the workflow
  references/sites.md    route, field, limit and save button per site
  scripts/biolib.py      reads bio.md and tracker.md
  scripts/preflight.py   the two files agree
  scripts/check-live.py  the live sites agree
  scripts/payload.py     the exact text for a field
tests/test_preflight.py  one case per failure, with a passing case beside it
```

The tests are the guard on the guards. Each failure gets a case that must fail and a case that must pass.

```text
$ python3 -m unittest discover -s tests
Ran 18 tests in 0.004s

OK
```

The passing cases carry weight too. One holds a date, so a phone number pattern that matches `2026-10-31` fails the suite before it can fail every row in the tracker.

---

#### Step 8 — Roll Out One Change

The certification that started this run shows the whole loop.

```bash
# 1. Edit bio.md, set version to today
# 2. Confirm the files agree
python3 .claude/skills/profile-sync/scripts/preflight.py
# 3. In Claude Code, run /profile-sync to roll it out
# 4. Confirm the live sites agree
python3 .claude/skills/profile-sync/scripts/check-live.py
```

The skill works down the tracker, saves each field in Chrome in the logged-in session, reloads each page, records the check date, then commits and pushes. Credentials stay in the browser, so the repository holds public text only.

Before starting, confirm the fact at its source. Here that source was the Credly badge, issued 2026-10-30, which settled whether 10 or 9 was correct.

---

#### Compare and Contrast

| | By hand | A notes file | profile-sync |
| --- | --- | --- | --- |
| Source of truth | Whichever site is newest | A notes file | `bio.md` in git |
| Knows which sites are behind | No | If you update it |  Yes |
| Catches a wrong count | No | No |  Yes |
| Reads the live site | When you look | When you look |  3 sites by script, the rest by browser |

---

#### So, Which One?

Start with Step 1 and Step 2, even with no automation. The first side-by-side read will show you what your profiles have been saying.

Add the skill once you hold more profiles than you can check in one sitting. That number is small, and a new credential is a good day to start.

---

#### Summary

The goal of this article was to keep one person's public profiles consistent across many sites. The key to the solution was treating a bio as source code, with one source file, a status table and a check that reads the live sites. The profile-sync results were:

- 9 of the 10 sites are `Current`, each confirmed on its live page
- The certification count is computed from a list, so the headline and the About can no longer disagree
- 18 tests keep each failure beside a passing case
- 5 sites said 9 certifications the day after a tenth was issued, and 3 said 20+ years
- Google Skills stays `Blocked`: it has no bio field and its public profile page returns an error
- `check-live.py` reads 3 sites and only the Short text, so the other sites still need a browser check

Scope: one person's ten profiles on 2026-10-31, in one Chrome session. Form limits were read from each site's own form on that date and can change. Two edits on the same day share one `version`, so version equality alone does not show that a site has the latest text, and the live comparison covers that gap.

The strategy for keeping a public profile consistent was validated with an incremental step by step approach.

#### References

- [profile-sync](https://github.com/xbill9/profile-sync)
- [The skill's own instructions](https://github.com/xbill9/profile-sync/blob/main/.claude/skills/profile-sync/SKILL.md)
- [Evidence for this article](https://github.com/xbill9/profile-sync/tree/main/articles/profile-sprawl)
- [publishing-kit](https://github.com/xbill9/publishing-kit)
