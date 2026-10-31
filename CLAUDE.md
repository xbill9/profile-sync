# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Tracks one person's public profiles across sites. [Design doc](https://claude.ai/artifact/MkBAzwExf6dPvxL13foykC).

- `bio.md` is the source of truth. Change it first, never a site first. If a site was edited directly, copy that change back to `bio.md` before anything else.
- Each change to `bio.md` sets its frontmatter `version` to the current date (`YYYY-MM-DD`).
- `tracker.md` has one row per site. Status is exactly one of `Current`, `Behind`, `Unverified`, `Blocked`.
- A site is `Current` only when its synced version matches `bio.md` and the live profile has been checked. A site that doesn't use the changed section takes the new version with no edit.
- Keep `bio.md` site-neutral: plain Markdown, no site-specific syntax.
- This repo is public. Never commit private email addresses, phone numbers, login details or tokens.
- Profile edits go through Chrome in the user's logged-in session. Confirm before each save, since a save is public immediately.
