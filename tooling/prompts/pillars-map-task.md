# Pillars Map Task Prompt

Paste this file into an AI coding tool to explain the deterministic Pillars load set for a task. This workflow reports only and does not execute the task or modify files.

## Task: map a task to Pillars

### Step 1: Get the task and target

Use the supplied task text. If none is present, ask for it. Use an explicitly named file or directory as the target. Otherwise use the current working directory.

### Step 2: Resolve applicable scopes

Starting at the repository root and ending at the target, identify every directory with both `AGENTS.md` and `agents/`. If none exists, report that Pillars is not set up and stop.

Apply scopes from outermost to innermost. Non-conflicting guidance accumulates. The nearest scope wins conflicts. A child exclusion suppresses an inherited task-routed pillar of the same identity for that child.

### Step 3: Read local metadata

For each scope, read:

- Every pillar's `pillar`, `status`, `always_load`, `covers`, `triggers`, `must_read_with`, and `see_also` fields.
- The local `AGENTS.md` `excluded:` block.
- Optional `agents/catalog.yaml` absent entries.

Use the path-derived identity. `agents/auth.md` is `auth`; `agents/auth/agent-registration.md` is `auth/agent-registration`. Bare references resolve top-level pillars only.

### Step 4: Use the portable matcher

For both task text and selector:

1. Lowercase ASCII letters.
2. Replace each run outside ASCII letters and digits with one space.
3. Trim and split on spaces.
4. Match only when the selector's full token sequence appears contiguously in the task tokens.

For example, `schema-change` matches `Schema change`; `api` does not match `capital`. Report deterministic matches separately from any optional semantic matches.

### Step 5: Compute each local load set

1. Add every `always_load: true` pillar.
2. Add non-always pillars whose `triggers` match the task. These are primaries.
3. Record matching catalog entries as absent concerns.
4. Add each primary's `must_read_with` targets at depth 1 only.
5. For each selected pillar, resolve `see_also`. Add a present target only when the task matches the target identity, `triggers`, or `covers` with the same matcher. Record a matching catalog target as absent.
6. Deduplicate by scope plus identity while preserving all selection reasons.

Do not match primary pillars from `covers`. Do not follow dependency dependencies. Do not follow `see_also` recursively.

### Step 6: Report

```markdown
# Pillars Task Map

Task: <task>
Target: <target>

## Load Set

| Scope | Identity | Why it loads |
|---|---|---|
| `root` | `context` | always-loaded |
| `<scope>` | `<identity>` | trigger, dependency, or see_also reason |

## Absent, Stub, Or Excluded

- `<scope>::<identity>`: <state and required behavior>

## Scope Precedence

- <overrides, inherited guidance, or suppressions>

## Routing Notes

- <optional semantic additions, weak selectors, or unresolved references>
```

If no task-routed pillar matches, say that only always-loaded pillars apply. If a catalog entry matches, state the assumption that the task would require and recommend authoring that identity.

## Constraints

- Do not write files or execute the mapped task.
- Do not invent globally known absent pillars. Use only local catalog entries.
- Do not treat unknown non-floor concerns as errors.
- Do not follow dependencies transitively.

## Now: map this task

**Task:** _<replace with the task>_

**Target:** _<optional path>_
