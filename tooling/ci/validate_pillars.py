#!/usr/bin/env python3
"""Deterministic structural and routing validator for Pillars 1.2 projects.

The validator is optional repository tooling. It checks local files only and
never fetches the standard catalog or calls an external service.

Usage:
    python3 tooling/ci/validate_pillars.py [PROJECT_ROOT ...]
        [--recursive-scopes] [--standalone PATH ...] [--fixtures FILE ...]

Requires PyYAML.
"""

import argparse
from pathlib import Path
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
IDENTITY_SEGMENT_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
ASCII_UPPER = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
ASCII_LOWER = "abcdefghijklmnopqrstuvwxyz"
ASCII_LOWER_TABLE = str.maketrans(ASCII_UPPER, ASCII_LOWER)
ALWAYS_WORD_BUDGET = 1000
ALWAYS_BYTE_BUDGET = 8 * 1024
ALWAYS_SCOPE_WORD_BUDGET = 2000
ALWAYS_SCOPE_BYTE_BUDGET = 16 * 1024
ROUTED_WORD_BUDGET = 2000
ROUTED_BYTE_BUDGET = 16 * 1024


class Findings:
    """Ordered errors and warnings, each reported once.

    Conformance fixtures re-validate every scope they route through, so the
    same finding can be raised many times in one run.
    """

    def __init__(self):
        self.errors = []
        self.warnings = []

    @staticmethod
    def _add(bucket, where, message):
        entry = (str(where), message)
        if entry not in bucket:
            bucket.append(entry)

    def error(self, where, message):
        self._add(self.errors, where, message)

    def warn(self, where, message):
        self._add(self.warnings, where, message)


def split_frontmatter(text):
    """Return (frontmatter_yaml, body), or (None, text) without a leading block."""
    match = re.match(r"^---[ \t]*\n(.*?)\n---[ \t]*\n?(.*)$", text, re.DOTALL)
    if not match:
        return None, text
    return match.group(1), match.group(2)


def normalize_selector(value):
    """Apply the portable ASCII token normalization from SPEC.md."""
    lowered = value.translate(ASCII_LOWER_TABLE)
    return " ".join(re.sub(r"[^a-z0-9]+", " ", lowered).split())


def selector_matches(task, selector):
    task_tokens = normalize_selector(task).split()
    selector_tokens = normalize_selector(selector).split()
    if not selector_tokens or len(selector_tokens) > len(task_tokens):
        return False
    width = len(selector_tokens)
    return any(task_tokens[index:index + width] == selector_tokens
               for index in range(len(task_tokens) - width + 1))


def valid_identity(identity):
    if not isinstance(identity, str):
        return False
    parts = identity.split("/")
    return 1 <= len(parts) <= 2 and all(IDENTITY_SEGMENT_RE.fullmatch(part) for part in parts)


def derived_identity(path, identity_root):
    rel = Path(path).absolute().relative_to(Path(identity_root).absolute())
    return rel.with_suffix("").as_posix()


def display_path(path, display_root):
    try:
        return Path(path).resolve().relative_to(Path(display_root).resolve()).as_posix()
    except ValueError:
        return str(Path(path).resolve())


def validate_string_list(value, field, where, findings, required=False,
                         normalized_duplicates=True):
    if value is None:
        if required:
            findings.error(where, "field '%s' is required" % field)
        return []
    if not isinstance(value, list):
        findings.error(where, "field '%s' must be a list" % field)
        return []
    if required and not value:
        findings.error(where, "field '%s' must contain at least one item" % field)
        return []

    valid = []
    seen = {}
    for index, item in enumerate(value):
        if not isinstance(item, str) or not item.strip():
            findings.error(where, "field '%s' item %d must be a non-empty string" % (field, index))
            continue
        key = normalize_selector(item)
        if not key:
            findings.error(where, "field '%s' item %d has no portable matcher tokens" % (field, index))
            continue
        if not normalized_duplicates:
            key = item
        if key in seen:
            findings.error(where, "field '%s' has duplicate items '%s' and '%s'" %
                           (field, seen[key], item))
            continue
        seen[key] = item
        valid.append(item)
    return valid


def validate_reference_list(value, field, identity, where, findings):
    refs = validate_string_list(value, field, where, findings, required=False,
                                normalized_duplicates=False)
    for ref in refs:
        if not valid_identity(ref):
            findings.error(where, "field '%s' has invalid identity '%s'" % (field, ref))
        if ref == identity:
            findings.error(where, "field '%s' contains a self-reference to '%s'" % (field, ref))
    return refs


def check_headings(body, where, findings):
    all_headings = re.findall(r"^##[ \t]+([^\n#]+?)[ \t]*$", body, re.MULTILINE)
    unexpected = [heading for heading in all_headings if heading not in REQUIRED_SECTIONS]
    if unexpected:
        findings.error(where, "unexpected level-2 sections: " + ", ".join(unexpected))
    found = [heading for heading in all_headings if heading in REQUIRED_SECTIONS]
    if found == REQUIRED_SECTIONS:
        check_empty_sections(body, where, findings)
        return
    missing = [section for section in REQUIRED_SECTIONS if section not in found]
    if missing:
        findings.error(where, "missing or misnamed sections: " + ", ".join(missing))
    else:
        findings.error(where, "section order is %s, expected %s" % (found, REQUIRED_SECTIONS))


def check_empty_sections(body, where, findings):
    """Warn about sections with no text; SPEC.md asks for (none) instead."""
    parts = re.split(r"^##[ \t]+([^\n#]+?)[ \t]*$", body, flags=re.MULTILINE)
    for heading, content in zip(parts[1::2], parts[2::2]):
        if heading in REQUIRED_SECTIONS and not content.strip():
            findings.warn(where, "section '%s' is empty; write (none) when nothing applies" %
                          heading)


def count_words(text):
    return len(re.findall(r"[A-Za-z0-9]+(?:['-][A-Za-z0-9]+)*", text))


def validate_pillar(path, identity_root, findings, display_root):
    where = display_path(path, display_root)
    text = Path(path).read_text(encoding="utf-8")
    fm_raw, body = split_frontmatter(text)
    if fm_raw is None:
        findings.error(where, "no YAML frontmatter block")
        return None
    try:
        frontmatter = yaml.safe_load(fm_raw) or {}
    except yaml.YAMLError as exc:
        findings.error(where, "unparseable frontmatter: %s" % exc)
        return None
    if not isinstance(frontmatter, dict):
        findings.error(where, "frontmatter is not a mapping")
        return None

    identity = derived_identity(path, identity_root)
    if not valid_identity(identity):
        findings.error(where, "path-derived identity '%s' is invalid or nested too deeply" % identity)

    stem = Path(path).stem
    pillar = frontmatter.get("pillar")
    if not isinstance(pillar, str) or not pillar:
        findings.error(where, "frontmatter missing required string field: pillar")
    elif pillar != stem:
        findings.error(where, "pillar '%s' does not match filename '%s'" % (pillar, stem))

    covers = validate_string_list(frontmatter.get("covers"), "covers", where, findings, required=True)

    always_load = frontmatter.get("always_load", False)
    if not isinstance(always_load, bool):
        findings.error(where, "field 'always_load' must be a boolean")
        always_load = False

    triggers = validate_string_list(
        frontmatter.get("triggers"), "triggers", where, findings,
        required=not always_load,
    )
    status = frontmatter.get("status", "present")
    if status not in ("present", "stub"):
        findings.error(where, "status '%s' must be 'present' or 'stub'" % status)

    must_read_with = validate_reference_list(
        frontmatter.get("must_read_with"), "must_read_with", identity, where, findings,
    )
    see_also = validate_reference_list(
        frontmatter.get("see_also"), "see_also", identity, where, findings,
    )
    if len(must_read_with) > 3:
        findings.warn(where, "must_read_with has %d entries; more than 3 is a boundary smell" %
                      len(must_read_with))

    check_headings(body, where, findings)

    words = count_words(text)
    bytes_count = len(text.encode("utf-8"))
    word_budget = ALWAYS_WORD_BUDGET if always_load else ROUTED_WORD_BUDGET
    byte_budget = ALWAYS_BYTE_BUDGET if always_load else ROUTED_BYTE_BUDGET
    if words > word_budget:
        findings.warn(where, "%d words exceeds the recommended %d-word %s budget" %
                      (words, word_budget, "always-loaded" if always_load else "task-routed"))
    if bytes_count > byte_budget:
        findings.warn(where, "%d bytes exceeds the recommended %d-byte %s budget" %
                      (bytes_count, byte_budget, "always-loaded" if always_load else "task-routed"))

    return {
        "identity": identity,
        "pillar": pillar or stem,
        "path": Path(path).resolve(),
        "where": where,
        "status": status,
        "always_load": always_load,
        "covers": covers,
        "triggers": triggers,
        "must_read_with": must_read_with,
        "see_also": see_also,
        "words": words,
        "bytes": bytes_count,
    }


def parse_exclusions(agents_md, findings, display_root):
    where = display_path(agents_md, display_root)
    text = Path(agents_md).read_text(encoding="utf-8")
    matching_fence = None
    for fence in re.findall(r"```ya?ml[ \t]*\n(.*?)```", text, re.DOTALL):
        if "excluded:" in fence:
            matching_fence = fence
            break
    if matching_fence is None:
        findings.error(where, "no YAML excluded block found")
        return {}, set()
    try:
        data = yaml.safe_load(matching_fence)
    except yaml.YAMLError as exc:
        findings.error(where, "excluded block is not valid YAML: %s" % exc)
        return {}, set()
    if not isinstance(data, dict) or not isinstance(data.get("excluded"), list):
        findings.error(where, "excluded must be a YAML list")
        return {}, set()

    entries = {}
    for index, item in enumerate(data["excluded"]):
        reason = None
        if isinstance(item, str):
            identity = item
        elif isinstance(item, dict) and isinstance(item.get("name"), str):
            identity = item["name"]
            reason = item.get("reason")
            if reason is not None and (not isinstance(reason, str) or not reason.strip()):
                findings.error(where, "excluded item %d reason must be a non-empty string" % index)
        else:
            findings.error(where, "excluded item %d must be a string or name/reason mapping" % index)
            continue
        if not valid_identity(identity):
            findings.error(where, "excluded identity '%s' is invalid" % identity)
        if identity in entries:
            findings.error(where, "excluded identity '%s' is duplicated" % identity)
            continue
        if reason is None:
            findings.warn(where, "excluded identity '%s' has no reason" % identity)
        entries[identity] = reason
    return entries, set(entries)


def parse_catalog(catalog_path, findings, display_root):
    if not Path(catalog_path).is_file():
        return {}
    where = display_path(catalog_path, display_root)
    try:
        data = yaml.safe_load(Path(catalog_path).read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        findings.error(where, "catalog is not valid YAML: %s" % exc)
        return {}
    if not isinstance(data, dict):
        findings.error(where, "catalog must be a mapping")
        return {}
    if data.get("version") != 1:
        findings.error(where, "catalog version must be 1")
    absent = data.get("absent")
    if not isinstance(absent, list):
        findings.error(where, "catalog absent must be a list")
        return {}

    entries = {}
    for index, item in enumerate(absent):
        item_where = "%s absent item %d" % (where, index)
        if not isinstance(item, dict):
            findings.error(item_where, "entry must be a mapping")
            continue
        identity = item.get("identity")
        if not valid_identity(identity):
            findings.error(item_where, "identity '%s' is invalid" % identity)
            continue
        if identity in entries:
            findings.error(item_where, "identity '%s' is duplicated" % identity)
            continue
        covers = validate_string_list(item.get("covers"), "covers", item_where, findings)
        triggers = validate_string_list(item.get("triggers"), "triggers", item_where, findings, required=True)
        entries[identity] = {"identity": identity, "covers": covers, "triggers": triggers}
    return entries


def check_identity_uniqueness(records, findings):
    exact = {}
    portable = {}
    for record in records:
        identity = record["identity"]
        if identity in exact:
            findings.error(record["where"], "duplicate path-derived identity '%s' also used by %s" %
                           (identity, exact[identity]["where"]))
        else:
            exact[identity] = record
        portable_key = identity.translate(ASCII_LOWER_TABLE)
        if portable_key in portable and portable[portable_key]["identity"] != identity:
            findings.error(record["where"], "identity '%s' is ambiguous with '%s' on portable filesystems" %
                           (identity, portable[portable_key]["identity"]))
        else:
            portable[portable_key] = record
    return exact


def check_references(records, by_identity, excluded, findings, unresolved_are_errors=True,
                     catalog=None):
    catalog = catalog or {}
    leaf_to_subpillars = {}
    for identity in by_identity:
        if "/" in identity:
            leaf_to_subpillars.setdefault(identity.rsplit("/", 1)[1], []).append(identity)

    for record in records:
        for field in ("must_read_with", "see_also"):
            for ref in record[field]:
                if ref in by_identity or ref in excluded or (field == "see_also" and ref in catalog):
                    continue
                if "/" not in ref and ref in leaf_to_subpillars:
                    matches = sorted(leaf_to_subpillars[ref])
                    if len(matches) > 1:
                        message = (
                            "bare reference '%s' is ambiguous; use one of: %s" %
                            (ref, ", ".join(matches))
                        )
                    else:
                        message = (
                            "bare reference '%s' does not resolve sub-pillars; use '%s'" %
                            (ref, matches[0])
                        )
                else:
                    message = "%s reference '%s' is neither present nor excluded" % (field, ref)
                if unresolved_are_errors:
                    findings.error(record["where"], message)
                else:
                    findings.warn(record["where"], message)


def validate_project(root, findings, display_root=None):
    root = Path(root).resolve()
    display_root = Path(display_root or Path.cwd()).resolve()
    agents_md = root / "AGENTS.md"
    agents_dir = root / "agents"
    label = display_path(root, display_root) or "."

    if not agents_md.is_file():
        findings.error(label, "AGENTS.md not found at scope root")
    if not agents_dir.is_dir():
        findings.error(label, "agents/ directory not found at scope root")
        return {"root": root, "pillars": {}, "excluded": set(), "catalog": {}}

    if agents_md.is_file():
        _excluded_entries, excluded = parse_exclusions(agents_md, findings, display_root)
    else:
        excluded = set()

    records = []
    for path in sorted(agents_dir.rglob("*.md")):
        record = validate_pillar(path, agents_dir, findings, display_root)
        if record:
            records.append(record)
    by_identity = check_identity_uniqueness(records, findings)
    catalog = parse_catalog(agents_dir / "catalog.yaml", findings, display_root)

    for identity in sorted(set(by_identity) & excluded):
        findings.error(display_path(agents_md, display_root),
                       "identity '%s' is both present and excluded" % identity)
    for identity in sorted(set(by_identity) & set(catalog)):
        findings.error(display_path(agents_dir / "catalog.yaml", display_root),
                       "identity '%s' is both present and cataloged as absent" % identity)
    for identity in sorted(excluded & set(catalog)):
        findings.error(display_path(agents_dir / "catalog.yaml", display_root),
                       "identity '%s' is both excluded and cataloged as absent" % identity)
    for floor in FLOOR_PILLARS:
        if floor in catalog:
            findings.error(display_path(agents_dir / "catalog.yaml", display_root),
                           "floor identity '%s' cannot be cataloged as absent" % floor)
        if floor not in by_identity:
            if floor in excluded:
                findings.warn(display_path(agents_md, display_root),
                              "floor pillar '%s' is explicitly excluded" % floor)
            else:
                findings.error(display_path(agents_dir, display_root),
                               "floor pillar '%s.md' is missing and not excluded" % floor)
        elif not by_identity[floor]["always_load"]:
            findings.error(by_identity[floor]["where"],
                           "floor pillar must declare always_load: true")

    check_references(records, by_identity, excluded, findings, unresolved_are_errors=True,
                     catalog=catalog)

    always_records = [record for record in records if record["always_load"]]
    total_words = sum(record["words"] for record in always_records)
    total_bytes = sum(record["bytes"] for record in always_records)
    if total_words > ALWAYS_SCOPE_WORD_BUDGET:
        findings.warn(label, "%d always-loaded words exceeds the recommended %d-word scope budget" %
                      (total_words, ALWAYS_SCOPE_WORD_BUDGET))
    if total_bytes > ALWAYS_SCOPE_BYTE_BUDGET:
        findings.warn(label, "%d always-loaded bytes exceeds the recommended %d-byte scope budget" %
                      (total_bytes, ALWAYS_SCOPE_BYTE_BUDGET))

    return {
        "root": root,
        "pillars": by_identity,
        "excluded": excluded,
        "catalog": catalog,
    }


def validate_standalone(path, findings, display_root=None):
    display_root = Path(display_root or Path.cwd()).resolve()
    target = Path(path).resolve()
    if target.is_file():
        candidates = [target]
        identity_root = target.parent
    else:
        identity_root = target
        project_dirs = {item.parent.resolve() for item in target.rglob("AGENTS.md")}
        candidates = []
        for candidate in sorted(target.rglob("*.md")):
            if any(scope in candidate.parents for scope in project_dirs):
                continue
            candidates.append(candidate)

    records = []
    for candidate in candidates:
        text = candidate.read_text(encoding="utf-8")
        fm_raw, _body = split_frontmatter(text)
        if fm_raw is None:
            continue
        try:
            frontmatter = yaml.safe_load(fm_raw)
        except yaml.YAMLError:
            frontmatter = None
        if not isinstance(frontmatter, dict) or "pillar" not in frontmatter:
            continue
        record = validate_pillar(candidate, identity_root, findings, display_root)
        if record:
            records.append(record)
    check_identity_uniqueness(records, findings)
    # Loose examples do not define a complete scope, exclusion set, or absent
    # catalog. Their reference syntax is checked per file, but target existence
    # is validated only for full projects and conformance fixtures.
    return len(records)


def compute_scope_load(model, task):
    pillars = model["pillars"]
    selected = set()
    primaries = set()
    absent = set()
    reasons = {}

    for identity, record in sorted(pillars.items()):
        if record["always_load"]:
            selected.add(identity)
            reasons.setdefault(identity, []).append("always-loaded")
        elif any(selector_matches(task, trigger) for trigger in record["triggers"]):
            selected.add(identity)
            primaries.add(identity)
            matched = [trigger for trigger in record["triggers"] if selector_matches(task, trigger)]
            reasons.setdefault(identity, []).append("trigger: " + matched[0])

    for identity, entry in sorted(model["catalog"].items()):
        if any(selector_matches(task, trigger) for trigger in entry["triggers"]):
            absent.add(identity)

    for identity in sorted(primaries):
        for ref in pillars[identity]["must_read_with"]:
            if ref in pillars:
                selected.add(ref)
                reasons.setdefault(ref, []).append("must_read_with from %s" % identity)

    for identity in sorted(list(selected)):
        for ref in pillars[identity]["see_also"]:
            target = pillars.get(ref) or model["catalog"].get(ref)
            if not target:
                continue
            selectors = [ref] + target["triggers"] + target["covers"]
            if any(selector_matches(task, selector) for selector in selectors):
                if ref in pillars:
                    selected.add(ref)
                    reasons.setdefault(ref, []).append("see_also from %s" % identity)
                else:
                    absent.add(ref)

    return {
        "load": sorted(selected),
        "primaries": sorted(primaries),
        "absent": sorted(absent),
        "reasons": reasons,
    }


def find_applicable_scopes(project_root, target):
    project_root = Path(project_root).resolve()
    target_path = Path(target)
    if not target_path.is_absolute():
        target_path = project_root / target_path
    target_path = target_path.resolve()
    if target_path != project_root and project_root not in target_path.parents:
        raise ValueError("target is outside fixture project")

    directory = target_path if target_path.is_dir() else target_path.parent
    scopes = []
    current = project_root
    if (current / "AGENTS.md").is_file() and (current / "agents").is_dir():
        scopes.append(current)
    relative_parts = directory.relative_to(project_root).parts
    for part in relative_parts:
        current = current / part
        if (current / "AGENTS.md").is_file() and (current / "agents").is_dir():
            scopes.append(current)
    return scopes


def discover_scope_roots(root):
    """Return every complete Pillars scope below root in stable parent-first order."""
    root = Path(root).resolve()
    scopes = set()
    for agents_md in root.rglob("AGENTS.md"):
        scope = agents_md.parent.resolve()
        try:
            scope.relative_to(root)
        except ValueError:
            continue
        if (scope / "agents").is_dir():
            scopes.add(scope)
    return sorted(
        scopes,
        key=lambda scope: (len(scope.relative_to(root).parts), scope.as_posix()),
    )


def scope_label(project_root, scope_root):
    rel = Path(scope_root).resolve().relative_to(Path(project_root).resolve()).as_posix()
    return "root" if rel == "." else rel


def compute_nested_load(project_root, task, target, findings, display_root):
    scopes = find_applicable_scopes(project_root, target)
    models = [validate_project(scope, findings, display_root) for scope in scopes]
    outputs = [compute_scope_load(model, task) for model in models]

    load = []
    primaries = []
    absent = []
    for index, (scope, model, output) in enumerate(zip(scopes, models, outputs)):
        descendant_exclusions = set()
        for descendant in models[index + 1:]:
            descendant_exclusions.update(descendant["excluded"])
        label = scope_label(project_root, scope)
        for identity in output["load"]:
            record = model["pillars"][identity]
            if identity in descendant_exclusions and not record["always_load"]:
                continue
            load.append("%s::%s" % (label, identity))
        primaries.extend("%s::%s" % (label, identity) for identity in output["primaries"])
        absent.extend("%s::%s" % (label, identity) for identity in output["absent"])
    return {"load": load, "primaries": primaries, "absent": absent}


def run_conformance_file(path, findings, display_root=None):
    display_root = Path(display_root or Path.cwd()).resolve()
    fixture_path = Path(path).resolve()
    where = display_path(fixture_path, display_root)
    try:
        data = yaml.safe_load(fixture_path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        findings.error(where, "conformance file is not valid YAML: %s" % exc)
        return 0
    if not isinstance(data, dict) or data.get("version") != 1:
        findings.error(where, "conformance file version must be 1")
        return 0
    cases = data.get("cases")
    if not isinstance(cases, list):
        findings.error(where, "conformance cases must be a list")
        return 0

    count = 0
    for index, case in enumerate(cases):
        case_where = "%s case %d" % (where, index)
        if not isinstance(case, dict):
            findings.error(case_where, "case must be a mapping")
            continue
        name = case.get("name")
        project = case.get("project")
        task = case.get("task")
        target = case.get("target", ".")
        expected = case.get("expected")
        if not all(isinstance(value, str) and value for value in (name, project, task, target)):
            findings.error(case_where, "name, project, task, and target must be non-empty strings")
            continue
        if not isinstance(expected, dict):
            findings.error(case_where, "expected must be a mapping")
            continue
        project_root = fixture_path.parent / project
        try:
            actual = compute_nested_load(project_root, task, target, findings, display_root)
        except (OSError, ValueError) as exc:
            findings.error(case_where, "could not compute load set: %s" % exc)
            continue
        for field in ("load", "primaries", "absent"):
            expected_values = expected.get(field, [])
            if not isinstance(expected_values, list) or not all(isinstance(item, str) for item in expected_values):
                findings.error(case_where, "expected %s must be a string list" % field)
                continue
            if actual[field] != expected_values:
                findings.error(case_where, "%s '%s' expected %s but got %s" %
                               (name, field, expected_values, actual[field]))
        count += 1
    return count


def parse_args(argv):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("roots", nargs="*", help="Pillars project roots")
    parser.add_argument("--recursive-scopes", action="store_true",
                        help="Discover and validate nested Pillars scopes below each root")
    parser.add_argument("--standalone", nargs="*", default=[],
                        help="Loose pillar files or directories")
    parser.add_argument("--fixtures", nargs="*", default=[],
                        help="Conformance fixture YAML files")
    return parser.parse_args(argv[1:])


def main(argv):
    args = parse_args(argv)
    roots = args.roots or (["."] if not args.standalone and not args.fixtures else [])
    findings = Findings()
    display_root = Path.cwd()
    pillar_total = 0
    validated_roots = set()
    for root in roots:
        scope_roots = discover_scope_roots(root) if args.recursive_scopes else [Path(root).resolve()]
        if args.recursive_scopes and not scope_roots:
            findings.error(display_path(root, display_root),
                           "no complete Pillars scopes found recursively")
        for scope_root in scope_roots:
            resolved = Path(scope_root).resolve()
            if resolved in validated_roots:
                continue
            validated_roots.add(resolved)
            model = validate_project(resolved, findings, display_root)
            pillar_total += len(model["pillars"])
    for path in args.standalone:
        pillar_total += validate_standalone(path, findings, display_root)
    fixture_total = 0
    for path in args.fixtures:
        fixture_total += run_conformance_file(path, findings, display_root)

    for where, message in findings.errors:
        print("ERROR  %s: %s" % (where, message))
    for where, message in findings.warnings:
        print("WARN   %s: %s" % (where, message))

    print("\nChecked %d pillar file(s), %d conformance case(s): %d error(s), %d warning(s)." %
          (pillar_total, fixture_total, len(findings.errors), len(findings.warnings)))
    return 1 if findings.errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
