---
name: sync-profile
description: Roll the current bio.md out to public profile sites listed in tracker.md, editing each in Chrome and updating its tracker row.
disable-model-invocation: true
---

Roll out `bio.md` to the sites in `tracker.md`. `$ARGUMENTS` optionally names one site; otherwise work through every row marked `Behind` or `Unverified`.

1. Read `bio.md` and `tracker.md`. Note the `version` and, with `git diff` or `git log`, which sections changed since each site's synced version.
2. For each site:
   - If it is `Behind` and its "Text used" sections did not change, set its synced version to the current one and mark it `Current`. No edit is needed.
   - Otherwise open the profile in a new Chrome tab and compare the live text to the `bio.md` section it uses.
   - If they differ, show the user the exact old and new text and wait for confirmation before saving. If the live site has something `bio.md` lacks, stop and raise it, because the fix belongs in `bio.md` first.
   - After saving, reload the live profile and confirm the new text appears. Record the synced version, last checked date and `Current`.
   - If a login, review queue or length limit stops the update, mark the row `Blocked` and explain in Notes.
3. Report which sites are `Current`, which are `Blocked`, and any that were not reached.

Never mark a site `Current` from a saved edit alone; the live check is what counts.
