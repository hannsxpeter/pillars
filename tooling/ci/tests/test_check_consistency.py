import importlib.util
from pathlib import Path
import textwrap
import unittest


MODULE_PATH = Path(__file__).resolve().parents[1] / "check_consistency.py"
SPEC = importlib.util.spec_from_file_location("check_consistency", MODULE_PATH)
consistency = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(consistency)

TAG = "https://github.com/hannsxpeter/pillars/releases/tag/v"


def changelog(*entries):
    """Build changelog text from (version, date) pairs, newest first."""
    blocks = ["# Changelog\n\n## [Unreleased]\n\nNo unreleased changes.\n"]
    for version, date in entries:
        blocks.append(textwrap.dedent("""\
            ## [{version}] - {date}

            Release notes.

            [{version}]: {tag}{version}
            """).format(version=version, date=date, tag=TAG))
    return "\n".join(blocks)


class ChangelogHistoryTests(unittest.TestCase):

    def test_intact_history_passes(self):
        text = changelog(("1.2.2", "2026-08-04"), ("1.2.1", "2026-08-04"),
                         ("1.2.0", "2026-08-03"), ("1.1.0", "2026-07-13"))
        self.assertEqual(consistency.changelog_errors(text, "1.2.2"), [])

    def test_bulk_bump_that_duplicates_a_released_entry_is_an_error(self):
        # A repo-wide 1.2.1 -> 1.2.2 substitution rewrites the released 1.2.1
        # entry in place. Adding the real 1.2.2 entry then leaves two of them.
        text = changelog(("1.2.2", "2026-08-04"), ("1.2.2", "2026-08-04"),
                         ("1.2.0", "2026-08-03"))
        errors = consistency.changelog_errors(text, "1.2.2")
        self.assertTrue(any("more than one entry" in error for error in errors))

    def test_missing_newest_entry_is_an_error(self):
        text = changelog(("1.2.1", "2026-08-04"), ("1.2.0", "2026-08-03"))
        errors = consistency.changelog_errors(text, "1.2.2")
        self.assertTrue(any("expected the release version '1.2.2'" in error
                            for error in errors))

    def test_out_of_order_history_is_an_error(self):
        text = changelog(("1.2.2", "2026-08-04"), ("1.1.0", "2026-07-13"),
                         ("1.2.0", "2026-08-03"))
        errors = consistency.changelog_errors(text, "1.2.2")
        self.assertTrue(any("descending order" in error for error in errors))

    def test_anchor_pointing_at_another_tag_is_an_error(self):
        text = changelog(("1.2.2", "2026-08-04")).replace(
            "[1.2.2]: %s1.2.2" % TAG, "[1.2.2]: %s1.2.1" % TAG)
        errors = consistency.changelog_errors(text, "1.2.2")
        self.assertTrue(any("points at tag 'v1.2.1'" in error for error in errors))

    def test_entry_without_an_anchor_is_an_error(self):
        text = changelog(("1.2.2", "2026-08-04"), ("1.2.0", "2026-08-03")).replace(
            "[1.2.0]: %s1.2.0\n" % TAG, "")
        errors = consistency.changelog_errors(text, "1.2.2")
        self.assertTrue(any("no release-tag anchor" in error for error in errors))

    def test_anchor_without_an_entry_is_an_error(self):
        text = changelog(("1.2.2", "2026-08-04")) + "\n[1.1.0]: %s1.1.0\n" % TAG
        errors = consistency.changelog_errors(text, "1.2.2")
        self.assertTrue(any("no matching entry" in error for error in errors))

    def test_empty_history_is_an_error(self):
        errors = consistency.changelog_errors("# Changelog\n", "1.2.2")
        self.assertEqual(len(errors), 1)
        self.assertIn("no released version entries", errors[0])

    def test_repository_changelog_is_intact(self):
        text = (consistency.ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        self.assertEqual(consistency.changelog_errors(text, consistency.VERSION), [])


if __name__ == "__main__":
    unittest.main()
