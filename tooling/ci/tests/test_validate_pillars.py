import importlib.util
from pathlib import Path
import tempfile
import textwrap
import unittest


MODULE_PATH = Path(__file__).resolve().parents[1] / "validate_pillars.py"
SPEC = importlib.util.spec_from_file_location("validate_pillars", MODULE_PATH)
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


def pillar_text(name, *, always=False, covers=None, triggers=None,
                must=None, see=None, body_extra=""):
    covers = covers or [name]
    triggers = [] if triggers is None and always else (triggers or [name])
    must = must or []
    see = see or []
    return textwrap.dedent("""\
        ---
        pillar: {name}
        status: present
        always_load: {always}
        covers: {covers}
        triggers: {triggers}
        must_read_with: {must}
        see_also: {see}
        ---

        ## Scope

        Scope text.

        ## Context

        Context text. {body_extra}

        ## Decisions

        (none)

        ## Rules

        (none)

        ## Workflows

        (none)

        ## Watchouts

        (none)

        ## Touchpoints

        (none)

        ## Gaps

        (none)
        """).format(
            name=name,
            always=str(always).lower(),
            covers="[" + ", ".join(covers) + "]",
            triggers="[" + ", ".join(triggers) + "]",
            must="[" + ", ".join(must) + "]",
            see="[" + ", ".join(see) + "]",
            body_extra=body_extra,
        )


def write_agents(root, excluded="[]"):
    root.mkdir(parents=True, exist_ok=True)
    (root / "AGENTS.md").write_text(textwrap.dedent("""\
        # Test Protocol

        ```yaml
        excluded: {excluded}
        ```
        """).format(excluded=excluded), encoding="utf-8")
    (root / "agents").mkdir(parents=True, exist_ok=True)


def write_floor(root):
    (root / "agents" / "context.md").write_text(
        pillar_text("context", always=True), encoding="utf-8")
    (root / "agents" / "repo.md").write_text(
        pillar_text("repo", always=True), encoding="utf-8")


class MatcherTests(unittest.TestCase):
    def test_portable_matcher_normalizes_punctuation_and_case(self):
        self.assertTrue(validator.selector_matches("Apply a Schema-Change now", "schema change"))

    def test_portable_matcher_uses_token_boundaries(self):
        self.assertFalse(validator.selector_matches("Fix capitalization", "api"))

    def test_non_ascii_selector_has_no_portable_tokens(self):
        self.assertEqual(validator.normalize_selector("数据"), "")


class StructuralTests(unittest.TestCase):
    def test_recursive_scope_discovery_is_parent_first(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            child = root / "packages" / "web"
            write_agents(root)
            write_agents(child)
            self.assertEqual(validator.discover_scope_roots(root),
                             [root.resolve(), child.resolve()])

    def test_subpillar_identity_is_path_qualified(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "auth" / "agent-registration.md"
            path.parent.mkdir()
            path.write_text(pillar_text("agent-registration", must=["auth"]), encoding="utf-8")
            findings = validator.Findings()
            record = validator.validate_pillar(path, root, findings, root)
            self.assertEqual(record["identity"], "auth/agent-registration")
            self.assertFalse(findings.errors)

    def test_list_types_and_normalized_duplicates_are_errors(self):
        findings = validator.Findings()
        validator.validate_string_list(["schema-change", "Schema change", 7],
                                       "triggers", "test", findings)
        self.assertEqual(len(findings.errors), 2)

    def test_self_reference_and_deep_reference_are_errors(self):
        findings = validator.Findings()
        validator.validate_reference_list(["auth", "a/b/c"], "see_also", "auth", "test", findings)
        self.assertEqual(len(findings.errors), 2)

    def test_dependency_fanout_is_warning(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "data.md"
            path.write_text(pillar_text("data", must=["auth", "api", "config", "observe"]),
                            encoding="utf-8")
            findings = validator.Findings()
            validator.validate_pillar(path, root, findings, root)
            self.assertTrue(any("boundary smell" in message for _, message in findings.warnings))

    def test_bare_subpillar_reference_is_ambiguous(self):
        records = [
            {"identity": "auth/token", "where": "a", "must_read_with": [], "see_also": []},
            {"identity": "api/token", "where": "b", "must_read_with": [], "see_also": []},
            {"identity": "consumer", "where": "c", "must_read_with": ["token"], "see_also": []},
        ]
        findings = validator.Findings()
        validator.check_references(records, {item["identity"]: item for item in records},
                                   set(), findings)
        self.assertTrue(any("ambiguous" in message for _, message in findings.errors))

    def test_portable_identity_collision_is_error(self):
        records = [
            {"identity": "Auth", "where": "Auth.md"},
            {"identity": "auth", "where": "auth.md"},
        ]
        findings = validator.Findings()
        validator.check_identity_uniqueness(records, findings)
        self.assertTrue(any("ambiguous" in message for _, message in findings.errors))

    def test_floor_exclusions_are_warnings_not_errors(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_agents(root, "[context, repo]")
            findings = validator.Findings()
            validator.validate_project(root, findings, root)
            self.assertFalse(findings.errors)
            self.assertEqual(len([message for _, message in findings.warnings
                                  if "floor pillar" in message]), 2)

    def test_present_and_excluded_conflict_is_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_agents(root, "[auth]")
            write_floor(root)
            (root / "agents" / "auth.md").write_text(pillar_text("auth"), encoding="utf-8")
            findings = validator.Findings()
            validator.validate_project(root, findings, root)
            self.assertTrue(any("both present and excluded" in message
                                for _, message in findings.errors))

    def test_content_budget_is_warning(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "context.md"
            path.write_text(pillar_text("context", always=True,
                                        body_extra="word " * 1100), encoding="utf-8")
            findings = validator.Findings()
            validator.validate_pillar(path, root, findings, root)
            self.assertTrue(any("word" in message and "budget" in message
                                for _, message in findings.warnings))


class RoutingTests(unittest.TestCase):
    def test_see_also_uses_target_covers_with_same_matcher(self):
        model = {
            "pillars": {
                "context": {"always_load": True, "triggers": [], "covers": [],
                            "must_read_with": [], "see_also": []},
                "data": {"always_load": False, "triggers": ["query"], "covers": [],
                         "must_read_with": [], "see_also": ["api"]},
                "api": {"always_load": False, "triggers": ["endpoint"],
                        "covers": ["request contract"], "must_read_with": [], "see_also": []},
            },
            "catalog": {},
        }
        result = validator.compute_scope_load(model, "Change request contract in this query")
        self.assertEqual(result["primaries"], ["data"])
        self.assertEqual(result["load"], ["api", "context", "data"])

    def test_local_catalog_reports_absent_match(self):
        model = {
            "pillars": {},
            "catalog": {"release": {"triggers": ["release"], "covers": []}},
        }
        result = validator.compute_scope_load(model, "Prepare release notes")
        self.assertEqual(result["absent"], ["release"])

    def test_repository_conformance_fixtures_pass(self):
        fixture = Path(__file__).resolve().parents[2] / "conformance" / "fixtures.yaml"
        findings = validator.Findings()
        count = validator.run_conformance_file(fixture, findings, fixture.parents[2])
        self.assertEqual(count, 6)
        self.assertFalse(findings.errors, findings.errors)


if __name__ == "__main__":
    unittest.main()
