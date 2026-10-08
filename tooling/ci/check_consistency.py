#!/usr/bin/env python3
"""Check release links, versions, catalog counts, URLs, tooling indexes, and stale terminology."""

from pathlib import Path
import re
import sys
from urllib.parse import unquote

import yaml


ROOT = Path(__file__).resolve().parents[2]
VERSION = "1.2.2"
CORE = [
    "stack", "arch", "data", "api", "ui", "auth", "quality",
    "development", "release", "deploy", "observe",
]
COMMON = [
    "config", "security", "privacy", "compliance", "i18n", "a11y",
    "analytics", "integrations", "async", "cache", "notifications",
]
IGNORED_PARTS = {
    ".git", ".godpowers", "__pycache__", ".pytest_cache",
    ".venv", "venv", "node_modules",
}
RELEASE_HEADING = re.compile(r"^## \[(\d+\.\d+\.\d+)\][^\n]*$", re.MULTILINE)
RELEASE_ANCHOR = re.compile(
    r"^\[(\d+\.\d+\.\d+)\]: \S+/releases/tag/v(\d+\.\d+\.\d+)\s*$", re.MULTILINE)
EMBEDDED_AGENTS_MD = re.compile(r"^````markdown\n(.*?)^````$", re.MULTILINE | re.DOTALL)
INIT_FORMS = [
    "tooling/prompts/pillars-init.md",
    "tooling/claude-skill/pillars-init/SKILL.md",
]


def maintained_files():
    for path in ROOT.rglob("*"):
        # Only folders inside the repository count; the checkout itself may
        # live under a folder that happens to share an ignored name.
        if not path.is_file() or IGNORED_PARTS.intersection(path.relative_to(ROOT).parts):
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
    }
    for rel, marker in expected.items():
        if marker not in (ROOT / rel).read_text(encoding="utf-8"):
            errors.append("%s: missing release marker '%s'" % (rel, marker))
    skill_readme = (ROOT / "tooling/claude-skill/README.md").read_text(encoding="utf-8")
    for name in ("pillars-init", "pillars-author", "pillars-verify"):
        path = ROOT / "tooling/claude-skill" / name / "SKILL.md"
        text = path.read_text(encoding="utf-8")
        if 'standard_version: ">=1.1.0"' not in text:
            errors.append("%s: stale standard compatibility" % path.relative_to(ROOT))
        version = re.search(r"^version: (\S+)$", text, re.MULTILINE)
        if not version or "| `%s` | %s |" % (name, version.group(1)) not in skill_readme:
            errors.append("tooling/claude-skill/README.md: version for %s does not match "
                          "its SKILL.md" % name)
    requirements = (ROOT / "tooling/ci/requirements.txt").read_text(encoding="utf-8").strip()
    if requirements != "PyYAML==6.0.3":
        errors.append("tooling/ci/requirements.txt: dependency pin is not the verified release")
    workflow = (ROOT / ".github/workflows/validate.yml").read_text(encoding="utf-8")
    if "--recursive-scopes" not in workflow:
        errors.append(".github/workflows/validate.yml: nested scope discovery is not enabled")
    for action in ("actions/checkout@v7", "actions/setup-python@v6"):
        if action not in workflow:
            errors.append(".github/workflows/validate.yml: expected current action pin '%s'" % action)


def changelog_errors(text, version):
    """Report release-history damage in CHANGELOG text.

    Released entries are append-only. A bulk version bump across the repo is
    the usual way they get rewritten in place, which is invisible in review
    because the result still looks like a well-formed changelog.
    """
    errors = []
    headings = RELEASE_HEADING.findall(text)
    if not headings:
        return ["CHANGELOG.md: no released version entries found"]

    if headings[0] != version:
        errors.append("CHANGELOG.md: newest entry is '%s', expected the release version '%s'"
                      % (headings[0], version))

    seen = set()
    for entry in headings:
        if entry in seen:
            errors.append("CHANGELOG.md: version '%s' has more than one entry" % entry)
        seen.add(entry)

    def parts(entry):
        return tuple(int(piece) for piece in entry.split("."))

    for older, newer in zip(headings[1:], headings):
        if parts(older) >= parts(newer):
            errors.append("CHANGELOG.md: entry '%s' does not precede '%s' in descending order"
                          % (newer, older))

    anchors = {}
    for label, tag in RELEASE_ANCHOR.findall(text):
        if label != tag:
            errors.append("CHANGELOG.md: anchor '[%s]' points at tag 'v%s'" % (label, tag))
        anchors[label] = tag
    for entry in headings:
        if entry not in anchors:
            errors.append("CHANGELOG.md: entry '%s' has no release-tag anchor" % entry)
    for label in anchors:
        if label not in seen:
            errors.append("CHANGELOG.md: anchor '[%s]' has no matching entry" % label)

    return errors


def check_changelog(errors):
    text = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    errors.extend(changelog_errors(text, VERSION))


def check_tooling_indexes(errors):
    """Every shipped prompt and CI script must be listed where readers look."""
    tooling_readme = (ROOT / "tooling/README.md").read_text(encoding="utf-8")
    prompts_readme = (ROOT / "tooling/prompts/README.md").read_text(encoding="utf-8")
    for path in sorted((ROOT / "tooling/prompts").glob("*.md")):
        if path.name == "README.md":
            continue
        for rel, text in (("tooling/README.md", tooling_readme),
                          ("tooling/prompts/README.md", prompts_readme)):
            if path.name not in text:
                errors.append("%s: does not list tooling/prompts/%s" % (rel, path.name))
    for path in sorted((ROOT / "tooling/ci").glob("*.py")):
        if path.name not in tooling_readme:
            errors.append("tooling/README.md: does not list tooling/ci/%s" % path.name)


def core_stub_row(entry):
    return "| %s | [%s] | [%s] |" % (
        entry["identity"], ", ".join(entry.get("covers", [])), ", ".join(entry["triggers"]))


def check_init_templates(errors):
    """Init writes AGENTS.md and Core stubs from text it carries for offline use."""
    canonical = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    catalog = yaml.safe_load((ROOT / "agents/catalog.yaml").read_text(encoding="utf-8"))
    entries = {entry["identity"]: entry for entry in catalog.get("absent", [])}
    for rel in INIT_FORMS:
        text = (ROOT / rel).read_text(encoding="utf-8")
        embedded = EMBEDDED_AGENTS_MD.findall(text)
        if embedded != [canonical]:
            errors.append("%s: embedded AGENTS.md does not match the root AGENTS.md" % rel)
        for identity in CORE:
            if identity in entries and core_stub_row(entries[identity]) not in text:
                errors.append("%s: Core stub row for '%s' does not match agents/catalog.yaml" %
                              (rel, identity))


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
    if "commonly exclude 11 of them" not in faq:
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
    check_changelog(errors)
    check_tooling_indexes(errors)
    check_init_templates(errors)
    check_catalog(errors)
    if errors:
        for error in errors:
            print("ERROR  " + error)
        print("\nConsistency check failed with %d error(s)." % len(errors))
        return 1
    print("Consistency check passed: links, versions, owner URLs, catalog, CI, tooling indexes, "
          "init templates, and terminology align.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
