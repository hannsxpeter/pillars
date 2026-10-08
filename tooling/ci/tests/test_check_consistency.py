import importlib.util
from pathlib import Path
import tempfile
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


def run_with_root(files, check):
    """Run a ROOT-reading check against a temporary repository of files."""
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "repo"
        for rel, text in files.items():
            path = root / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
        original = consistency.ROOT
        consistency.ROOT = root
        try:
            return check()
        finally:
            consistency.ROOT = original


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


class ToolingIndexTests(unittest.TestCase):

    def run_against(self, files):
        errors = []
        run_with_root(files, lambda: consistency.check_tooling_indexes(errors))
        return errors

    def test_indexed_prompts_and_scripts_pass(self):
        errors = self.run_against({
            "tooling/README.md": "pillars-trim.md validate.py",
            "tooling/prompts/README.md": "pillars-trim.md",
            "tooling/prompts/pillars-trim.md": "prompt",
            "tooling/ci/validate.py": "",
        })
        self.assertEqual(errors, [])

    def test_unlisted_prompt_and_script_are_errors(self):
        errors = self.run_against({
            "tooling/README.md": "",
            "tooling/prompts/README.md": "",
            "tooling/prompts/pillars-trim.md": "prompt",
            "tooling/ci/validate.py": "",
        })
        self.assertEqual(errors, [
            "tooling/README.md: does not list tooling/prompts/pillars-trim.md",
            "tooling/prompts/README.md: does not list tooling/prompts/pillars-trim.md",
            "tooling/README.md: does not list tooling/ci/validate.py",
        ])

    def test_repository_tooling_indexes_are_complete(self):
        errors = []
        consistency.check_tooling_indexes(errors)
        self.assertEqual(errors, [])


class InitTemplateTests(unittest.TestCase):

    def test_repository_init_templates_match_canonical_files(self):
        errors = []
        consistency.check_init_templates(errors)
        self.assertEqual(errors, [])

    def test_drifted_embedded_agents_md_is_an_error(self):
        canonical = "# Protocol\n\n```yaml\nexcluded: []\n```\n"
        good_row = "| arch | [system architecture] | [architecture, system design] |\n"
        drifted_row = "| arch | [system architecture] | [architecture, design, system] |\n"
        files = {
            "AGENTS.md": canonical,
            "agents/catalog.yaml": ("version: 1\nabsent:\n"
                                    "  - identity: arch\n"
                                    "    covers: [system architecture]\n"
                                    "    triggers: [architecture, system design]\n"),
            consistency.INIT_FORMS[0]: "````markdown\n" + canonical + "````\n" + good_row,
            consistency.INIT_FORMS[1]: ("````markdown\n" + canonical.replace("[]", "[ui]") +
                                        "````\n" + drifted_row),
        }
        errors = []
        run_with_root(files, lambda: consistency.check_init_templates(errors))
        self.assertEqual(errors, [
            "%s: embedded AGENTS.md does not match the root AGENTS.md" % consistency.INIT_FORMS[1],
            "%s: Core stub row for 'arch' does not match agents/catalog.yaml" %
            consistency.INIT_FORMS[1],
        ])


class SkillVersionTests(unittest.TestCase):

    def test_skill_readme_version_drift_is_an_error(self):
        files = {
            "tooling/claude-skill/README.md": (
                "| `pillars-init` | 0.3.0 | Pillars v1.1.0+ |\n"
                "| `pillars-author` | 0.1.0 | Pillars v1.1.0+ |\n"
                "| `pillars-verify` | 0.1.0 | Pillars v1.1.0+ |\n"),
        }
        for name, version in (("pillars-init", "0.4.0"), ("pillars-author", "0.1.0"),
                              ("pillars-verify", "0.1.0")):
            files["tooling/claude-skill/%s/SKILL.md" % name] = (
                '---\nname: %s\nversion: %s\nstandard_version: ">=1.1.0"\n---\n' %
                (name, version))
        for rel in ("SPEC.md", "README.md", "AGENTS.md", "tooling/ci/requirements.txt",
                    ".github/workflows/validate.yml"):
            files[rel] = ""
        errors = []
        run_with_root(files, lambda: consistency.check_versions(errors))
        self.assertIn("tooling/claude-skill/README.md: version for pillars-init does not match "
                      "its SKILL.md", errors)
        self.assertFalse(any("pillars-author" in error or "pillars-verify" in error
                             for error in errors))


class MaintainedFileTests(unittest.TestCase):

    def test_checkout_under_an_ignored_folder_name_is_still_scanned(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "venv" / "pillars"
            (root / "docs").mkdir(parents=True)
            (root / "docs" / "kept.md").write_text("kept", encoding="utf-8")
            (root / ".venv").mkdir()
            (root / ".venv" / "skipped.md").write_text("skipped", encoding="utf-8")
            original = consistency.ROOT
            consistency.ROOT = root
            try:
                found = sorted(path.name for path in consistency.maintained_files())
            finally:
                consistency.ROOT = original
        self.assertEqual(found, ["kept.md"])


if __name__ == "__main__":
    unittest.main()
