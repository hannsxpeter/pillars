#!/usr/bin/env python3
"""Check release links, versions, catalog counts, URLs, and stale terminology."""

from pathlib import Path
import re
import sys
from urllib.parse import unquote

import yaml


ROOT = Path(__file__).resolve().parents[2]
VERSION = "1.2.0"
CORE = [
    "stack", "arch", "data", "api", "ui", "auth", "quality",
    "development", "release", "deploy", "observe",
]
COMMON = [
    "config", "security", "privacy", "compliance", "i18n", "a11y",
    "analytics", "integrations", "async", "cache", "notifications",
]
IGNORED_PARTS = {".git", ".godpowers", "__pycache__"}


def maintained_files():
    for path in ROOT.rglob("*"):
        if not path.is_file() or any(part in IGNORED_PARTS for part in path.parts):
            continue
        if path.suffix in {".md", ".py", ".yml", ".yaml"}:
            yield path


def check_local_links(errors):
    pattern = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
    for path in maintained_files():
        if path.suffix != ".md":
            continue
        text = path.read_text(encoding="utf-8")
        for raw_target in pattern.findall(text):
            target = raw_target.strip().strip("<>").split()[0]
            if not target or target.startswith("#") or re.match(r"^[a-z]+://", target):
                continue
            file_part = unquote(target.split("#", 1)[0])
            if not file_part:
                continue
            resolved = (path.parent / file_part).resolve()
            if not resolved.exists():
                errors.append("%s: broken local link '%s'" %
                              (path.relative_to(ROOT), raw_target))


def check_urls_and_terms(errors):
    stale_phrases = [
        "The 1.0.0 standard is " + "single-repo",
        "Do I have to use all " + "21 pillars?",
        "https://github.com/" + "aihxp/pillars",
        "https://raw.githubusercontent.com/" + "aihxp/pillars",
    ]
    for path in maintained_files():
        text = path.read_text(encoding="utf-8")
        for phrase in stale_phrases:
            if phrase in text:
                errors.append("%s: stale phrase or URL '%s'" %
                              (path.relative_to(ROOT), phrase))
        unpinned_raw = "raw.githubusercontent.com/hannsxpeter/pillars/" + "main/"
        if unpinned_raw in text:
            errors.append("%s: raw install URL is not pinned to a release tag" %
                          path.relative_to(ROOT))


def check_versions(errors):
    expected = {
        "SPEC.md": "Version %s." % VERSION,
        "README.md": "Spec: v%s" % VERSION,
        "AGENTS.md": "Pillars %s" % VERSION,
        "CHANGELOG.md": "## [%s] - 2026-08-03" % VERSION,
    }
    for rel, marker in expected.items():
        if marker not in (ROOT / rel).read_text(encoding="utf-8"):
            errors.append("%s: missing release marker '%s'" % (rel, marker))
    for path in [
        ROOT / "tooling/claude-skill/pillars-init/SKILL.md",
        ROOT / "tooling/claude-skill/pillars-author/SKILL.md",
        ROOT / "tooling/claude-skill/pillars-verify/SKILL.md",
    ]:
        text = path.read_text(encoding="utf-8")
        if 'standard_version: ">=1.1.0"' not in text:
            errors.append("%s: stale standard compatibility" % path.relative_to(ROOT))
    requirements = (ROOT / "tooling/ci/requirements.txt").read_text(encoding="utf-8").strip()
    if requirements != "PyYAML==6.0.3":
        errors.append("tooling/ci/requirements.txt: dependency pin is not the verified release")
    workflow = (ROOT / ".github/workflows/validate.yml").read_text(encoding="utf-8")
    if "--recursive-scopes" not in workflow:
        errors.append(".github/workflows/validate.yml: nested scope discovery is not enabled")
    for action in ("actions/checkout@v7", "actions/setup-python@v6"):
        if action not in workflow:
            errors.append(".github/workflows/validate.yml: expected current action pin '%s'" % action)


def check_catalog(errors):
    catalog = yaml.safe_load((ROOT / "agents/catalog.yaml").read_text(encoding="utf-8"))
    actual = [entry["identity"] for entry in catalog.get("absent", [])]
    expected = CORE + COMMON
    if actual != expected:
        errors.append("agents/catalog.yaml: expected ordered identities %s, got %s" %
                      (expected, actual))

    pillars_text = (ROOT / "PILLARS.md").read_text(encoding="utf-8")
    for identity in expected:
        if "`%s.md`" % identity not in pillars_text:
            errors.append("PILLARS.md: catalog identity '%s' is not enumerated" % identity)
    if "Tier 1, Core (11)" not in pillars_text or "Tier 2, Common (11)" not in pillars_text:
        errors.append("PILLARS.md: tier counts do not match the 1.1 catalog")

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    if "11 Core, 11 Common" not in readme:
        errors.append("README.md: catalog counts are stale")
    faq = (ROOT / "FAQ.md").read_text(encoding="utf-8")
    if "CLI tools commonly exclude 11 of them" not in faq:
        errors.append("FAQ.md: CLI exclusion count is stale")

    expected_core_line = "- Core: " + ", ".join("`%s`" % item for item in CORE)
    expected_common_line = "- Common: " + ", ".join("`%s`" % item for item in COMMON)
    for rel in [
        "tooling/prompts/pillars-author.md",
        "tooling/claude-skill/pillars-author/SKILL.md",
    ]:
        text = (ROOT / rel).read_text(encoding="utf-8")
        if expected_core_line not in text or expected_common_line not in text:
            errors.append("%s: authoring catalog list is stale" % rel)


def main():
    errors = []
    check_local_links(errors)
    check_urls_and_terms(errors)
    check_versions(errors)
    check_catalog(errors)
    if errors:
        for error in errors:
            print("ERROR  " + error)
        print("\nConsistency check failed with %d error(s)." % len(errors))
        return 1
    print("Consistency check passed: links, versions, owner URLs, catalog, CI, and terminology align.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
