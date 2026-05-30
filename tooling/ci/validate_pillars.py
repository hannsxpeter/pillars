#!/usr/bin/env python3
"""validate_pillars.py: deterministic structural validator for Pillars projects.

Checks a Pillars-compatible repository for structural conformance with SPEC.md:
frontmatter schema, the eight-section heading order, pillar/filename agreement,
the always-loaded floor pillars, and must_read_with reference resolution.

This is repository-internal QA for the Pillars standard's own CI. It is not a
published CLI product; the standard stays usable with zero tooling. Adopters may
run it if they find it useful.

Usage:
    python3 tooling/ci/validate_pillars.py [PROJECT_ROOT ...] [--standalone PATH ...]

PROJECT_ROOT args are validated as full Pillars projects (AGENTS.md plus
agents/). Paths after --standalone are scanned for loose pillar files (any
*.md with a `pillar:` frontmatter field) and structurally linted on their own;
directories that are themselves projects are skipped so nothing is checked
twice. Use --standalone for worked-example pillars that live outside an
agents/ tree.

Exits non-zero when any ERROR-level finding is present. Warnings never fail the
run. Requires PyYAML (pip install pyyaml).
"""

import os
import re
import sys

try:
    import yaml
except ImportError:
    sys.stderr.write("PyYAML is required: pip install pyyaml\n")
    sys.exit(2)

REQUIRED_SECTIONS = [
    "Scope", "Context", "Decisions", "Rules",
    "Workflows", "Watchouts", "Touchpoints", "Gaps",
]
FLOOR_PILLARS = ("context", "repo")


class Findings:
    def __init__(self):
        self.errors = []
        self.warnings = []

    def error(self, where, msg):
        self.errors.append((where, msg))

    def warn(self, where, msg):
        self.warnings.append((where, msg))


def split_frontmatter(text):
    """Return (frontmatter_yaml, body) or (None, text) when no leading block."""
    match = re.match(r"^---[ \t]*\n(.*?)\n---[ \t]*\n?(.*)$", text, re.DOTALL)
    if not match:
        return None, text
    return match.group(1), match.group(2)


def extract_excluded(agents_md_text):
    """Return excluded pillar names from the first excluded-bearing YAML fence in
    AGENTS.md. Best effort; used only to suppress reference warnings."""
    for fence in re.findall(r"```ya?ml[ \t]*\n(.*?)```", agents_md_text, re.DOTALL):
        if "excluded:" not in fence:
            continue
        try:
            data = yaml.safe_load(fence)
        except yaml.YAMLError:
            continue
        if isinstance(data, dict) and isinstance(data.get("excluded"), list):
            names = set()
            for item in data["excluded"]:
                if isinstance(item, str):
                    names.add(item)
                elif isinstance(item, dict) and isinstance(item.get("name"), str):
                    names.add(item["name"])
            return names
    return set()


def check_headings(body, where, findings):
    found = [h for h in re.findall(r"^##[ \t]+([A-Za-z]+)", body, re.MULTILINE)
             if h in REQUIRED_SECTIONS]
    if found == REQUIRED_SECTIONS:
        return
    missing = [s for s in REQUIRED_SECTIONS if s not in found]
    if missing:
        findings.error(where, "missing or misnamed sections: " + ", ".join(missing))
    else:
        findings.error(where, "section order is %s, expected %s" % (found, REQUIRED_SECTIONS))


def validate_pillar(path, root, findings):
    rel = os.path.relpath(path, root)
    with open(path, encoding="utf-8") as handle:
        text = handle.read()

    fm_raw, body = split_frontmatter(text)
    if fm_raw is None:
        findings.error(rel, "no YAML frontmatter block")
        return None
    try:
        frontmatter = yaml.safe_load(fm_raw) or {}
    except yaml.YAMLError as exc:
        findings.error(rel, "unparseable frontmatter: %s" % exc)
        return None
    if not isinstance(frontmatter, dict):
        findings.error(rel, "frontmatter is not a mapping")
        return None

    stem = os.path.splitext(os.path.basename(path))[0]
    pillar = frontmatter.get("pillar")
    if not pillar:
        findings.error(rel, "frontmatter missing required field: pillar")
    elif pillar != stem:
        findings.error(rel, "pillar '%s' does not match filename '%s'" % (pillar, stem))

    if not isinstance(frontmatter.get("covers"), list):
        findings.error(rel, "field 'covers' missing or not a list")

    always_load = frontmatter.get("always_load", False)
    if not isinstance(always_load, bool):
        findings.error(rel, "field 'always_load' must be a boolean")
        always_load = bool(always_load)
    if not always_load and not isinstance(frontmatter.get("triggers"), list):
        findings.error(rel, "field 'triggers' missing or not a list (required unless always_load: true)")

    status = frontmatter.get("status", "present")
    if status not in ("present", "stub"):
        findings.error(rel, "status '%s' must be 'present' or 'stub'" % status)

    for field in ("triggers", "must_read_with", "see_also"):
        if field in frontmatter and not isinstance(frontmatter[field], list):
            findings.error(rel, "field '%s' must be a list" % field)

    check_headings(body, rel, findings)
    return {"pillar": pillar or stem, "fm": frontmatter, "rel": rel, "always_load": always_load}


def validate_project(root, findings):
    agents_md = os.path.join(root, "AGENTS.md")
    agents_dir = os.path.join(root, "agents")
    label = os.path.basename(root.rstrip("/")) or root

    if not os.path.isfile(agents_md):
        findings.error(label, "AGENTS.md not found at project root")
    if not os.path.isdir(agents_dir):
        findings.error(label, "agents/ directory not found")
        return 0

    excluded = set()
    if os.path.isfile(agents_md):
        with open(agents_md, encoding="utf-8") as handle:
            excluded = extract_excluded(handle.read())

    results = []
    for dirpath, _dirs, names in os.walk(agents_dir):
        for name in sorted(names):
            if name.endswith(".md"):
                result = validate_pillar(os.path.join(dirpath, name), root, findings)
                if result:
                    results.append(result)

    by_name = {r["pillar"]: r for r in results}

    for floor in FLOOR_PILLARS:
        floor_path = os.path.join(agents_dir, floor + ".md")
        if not os.path.isfile(floor_path):
            findings.error("agents/", "required floor pillar '%s.md' is missing" % floor)
        elif floor in by_name and by_name[floor]["always_load"] is not True:
            findings.error("agents/%s.md" % floor, "floor pillar must declare always_load: true")

    known = set(by_name)
    for result in results:
        for ref in (result["fm"].get("must_read_with") or []):
            if isinstance(ref, str) and ref not in known and ref not in excluded:
                findings.warn(result["rel"],
                              "must_read_with -> '%s' is neither a present pillar nor excluded" % ref)

    return len(results)


def find_project_dirs(root_abs):
    projects = set()
    for dirpath, _dirs, names in os.walk(root_abs):
        if "AGENTS.md" in names:
            projects.add(os.path.abspath(dirpath))
    return projects


def validate_standalone(path, base, findings):
    """Structurally lint loose pillar files (any *.md with a `pillar:` field) under
    `path`, skipping subtrees that are themselves projects (they own an AGENTS.md and
    are validated separately). `base` is the directory relpaths display against."""
    target = os.path.abspath(path)
    if os.path.isfile(target):
        candidates = [target]
    else:
        skip_dirs = find_project_dirs(target)
        candidates = []
        for dirpath, _dirs, names in os.walk(target):
            dir_abs = os.path.abspath(dirpath)
            if any(dir_abs == p or dir_abs.startswith(p + os.sep) for p in skip_dirs):
                continue
            for name in sorted(names):
                if name.endswith(".md"):
                    candidates.append(os.path.join(dirpath, name))

    count = 0
    for candidate in candidates:
        with open(candidate, encoding="utf-8") as handle:
            fm_raw, _body = split_frontmatter(handle.read())
        if fm_raw is None:
            continue
        try:
            frontmatter = yaml.safe_load(fm_raw)
        except yaml.YAMLError:
            continue
        if not isinstance(frontmatter, dict) or "pillar" not in frontmatter:
            continue
        validate_pillar(candidate, base, findings)
        count += 1
    return count


def main(argv):
    roots = []
    standalone = []
    bucket = roots
    for arg in argv[1:]:
        if arg == "--standalone":
            bucket = standalone
            continue
        bucket.append(arg)
    if not roots and not standalone:
        roots = ["."]

    findings = Findings()
    base = os.path.abspath(".")
    total = 0
    for root in roots:
        total += validate_project(os.path.abspath(root), findings)
    for path in standalone:
        total += validate_standalone(path, base, findings)

    for where, msg in findings.errors:
        print("ERROR  %s: %s" % (where, msg))
    for where, msg in findings.warnings:
        print("WARN   %s: %s" % (where, msg))

    scope = "%d project(s)" % len(roots)
    if standalone:
        scope += " plus standalone paths"
    print("\nChecked %d pillar file(s) across %s: %d error(s), %d warning(s)."
          % (total, scope, len(findings.errors), len(findings.warnings)))
    return 1 if findings.errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
