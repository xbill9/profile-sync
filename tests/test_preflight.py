"""One case per input that went wrong, each with a passing control beside it."""

import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / ".claude/skills/profile-sync/scripts"))

from biolib import COLUMNS, plain
from preflight import check

TODAY = "2026-10-31"


def sections(**over):
    base = {
        "Headline": "CTO | 2x Google Cloud Certified",
        "Short": "CTO.",
        "Summary": "I hold 2 Google Cloud certifications.",
        "Long": "I hold 2 Google Cloud certifications.\n\n<https://medium.com/@xbill999>",
        "Roles": "- CTO",
        "Community": "- GDE",
        "Certifications": "- One (Google Cloud)\n- Two (Google Cloud)\n- Other (AMD)",
    }
    return {**base, **over}


def row(**over):
    base = {
        "Site": "GitHub", "Profile URL": "<https://github.com/xbill9>", "Text used": "Short",
        "Synced version": TODAY, "Last checked": TODAY, "Status": "Current", "Notes": "",
    }
    return {**base, **over}


def run(s=None, rows=None, version=TODAY, header=None):
    return check(version, s or sections(), header or COLUMNS, [row()] if rows is None else rows, today=TODAY)


class Control(unittest.TestCase):
    def test_consistent_files_pass(self):
        self.assertEqual(run(), [])

    def test_public_profile_urls_are_not_emails(self):
        rows = [row(**{"Profile URL": "<https://medium.com/@xbill999>"})]
        self.assertEqual(run(rows=rows), [])

    def test_issue_dates_are_not_phone_numbers(self):
        self.assertEqual(run(sections(Roles="- CTO, May 2002 to present, 2026-10-31")), [])


class Counts(unittest.TestCase):
    def test_headline_count_disagrees_with_list(self):
        fails = run(sections(Headline="CTO | 10x Google Cloud Certified"))
        self.assertTrue(any("Headline claims 10" in f for f in fails), fails)

    def test_long_count_disagrees_with_list(self):
        fails = run(sections(Long="I currently hold 9 official Google Cloud certifications."))
        self.assertTrue(any("Long claims 9" in f for f in fails), fails)


class Tracker(unittest.TestCase):
    def test_current_at_old_version_fails(self):
        fails = run(rows=[row(**{"Synced version": "2026-10-01"})])
        self.assertTrue(any("is Current at" in f for f in fails), fails)

    def test_current_without_live_check_fails(self):
        fails = run(rows=[row(**{"Last checked": "none"})])
        self.assertTrue(any("no live check" in f for f in fails), fails)

    def test_unverified_without_check_passes(self):
        rows = [row(Status="Unverified", **{"Synced version": "none", "Last checked": "none"})]
        self.assertEqual(run(rows=rows), [])

    def test_unknown_status_fails(self):
        self.assertTrue(run(rows=[row(Status="Done")]))

    def test_blocked_needs_notes(self):
        self.assertTrue(run(rows=[row(Status="Blocked")]))
        self.assertEqual(run(rows=[row(Status="Blocked", Notes="Review queue")]), [])

    def test_long_text_over_credly_limit_fails(self):
        s = sections(Summary="x" * 601)
        fails = run(s, rows=[row(Site="Credly", **{"Text used": "Summary"})])
        self.assertTrue(any("allows 600" in f for f in fails), fails)
        self.assertEqual(run(sections(Summary="x" * 600), rows=[row(Site="Credly", **{"Text used": "Summary"})]), [])

    def test_unknown_section_fails(self):
        self.assertTrue(run(rows=[row(**{"Text used": "Tagline"})]))


class Private(unittest.TestCase):
    def test_email_in_bio_fails(self):
        self.assertTrue(run(sections(Roles="- CTO, name@example.com")))

    def test_email_in_tracker_fails(self):
        self.assertTrue(run(rows=[row(Notes="login name@example.com")]))

    def test_phone_in_bio_fails(self):
        self.assertTrue(run(sections(Roles="- CTO, +1 212 555 0100")))


class Bio(unittest.TestCase):
    def test_placeholder_fails(self):
        self.assertTrue(run(sections(Short="TODO: write this")))

    def test_future_version_fails(self):
        self.assertTrue(run(version="2026-11-01", rows=[]))

    def test_autolink_brackets_removed(self):
        self.assertEqual(plain("at <https://medium.com/@xbill999>"), "at https://medium.com/@xbill999")


if __name__ == "__main__":
    unittest.main()
