# Pillars Check Prompt

Paste this file into an AI coding tool to perform a report-only Pillars 1.2 structure check. For factual drift between pillar claims and code, use `pillars-verify.md`.

## Task: check Pillars structure

### Step 1: Find scopes

Locate directories containing both `AGENTS.md` and `agents/`, starting with the repository root. A missing root `AGENTS.md` or `agents/` is a blocking issue for a repository that claims root adoption. Validate nested scopes independently.

### Step 2: Inventory local metadata

For every scope, inventory pillar markdown files recursively, the local `excluded:` block, and optional `agents/catalog.yaml`. Derive each identity from its path:

- `agents/auth.md` has identity `auth` and `pillar: auth`.
- `agents/auth/agent-registration.md` has identity `auth/agent-registration` and `pillar: agent-registration`.

One sub-pillar level is portable. Identity segments use lowercase ASCII letters, digits, and internal hyphens.

### Step 3: Validate pillar frontmatter

Check that:

- `pillar` is a string matching the leaf filename.
- `status` is `present` or `stub`.
- `always_load` is a boolean when present.
- `covers` is a list of non-empty strings.
- `triggers` is a list of non-empty strings unless always-loaded.
- `must_read_with` and `see_also` are lists of valid identities.
- List items are the correct type and unique after portable matcher normalization.
- Identities are unique and do not collide on case-insensitive filesystems.
- Neither reference field contains a self-reference.
- More than three hard dependencies produces a boundary-smell warning.

Top-level references remain bare names. Sub-pillar references must be path-qualified. A bare name never searches sub-pillars by leaf.

### Step 4: Validate the body and budgets

Require these headings in order: Scope, Context, Decisions, Rules, Workflows, Watchouts, Touchpoints, Gaps. Empty sections use `(none)`.

Report budget warnings at:

- Always-loaded file: over 1,000 words or 8 KiB.
- All always-loaded files in one scope: over 2,000 words or 16 KiB.
- Task-routed file: over 2,000 words or 16 KiB.

Budgets are warnings, not compatibility errors.

### Step 5: Validate floors, exclusions, and catalog

- `context` and `repo` must exist with `always_load: true`, or be explicitly excluded.
- A floor exclusion is valid but produces a warning.
- An identity cannot be both present and excluded.
- `agents/catalog.yaml`, when present, has `version: 1` and an `absent:` list.
- Each catalog entry has a valid unique `identity` and string-list `triggers`; `covers` is optional.
- An identity cannot be present, cataloged absent, and excluded in more than one state.
- `context` and `repo` cannot be cataloged absent.

### Step 6: Validate references

Resolve every reference within its declaring scope.

- A missing, non-excluded `must_read_with` target is blocking.
- A present or excluded `see_also` target is valid.
- A `see_also` target may also resolve to the local catalog as an absent soft concern.
- Do not follow references transitively during structural validation.

### Step 7: Report

```markdown
# Pillars Structure Check

Scopes: <N>
Pillar files: <N>
Blocking issues: <N>
Warnings: <N>

## Blocking Issues

- `<path>`: <reason>

## Warnings

- `<path>`: <reason>

## Confirmed

- <identities, floors, references, catalog, budgets, or scope checks that passed>

## Suggested Next Actions

1. <highest-value repair>
2. <next repair>
```

If no blocking issues exist, say: `No blocking Pillars structure issues found.`

## Constraints

- Do not write or modify files.
- Do not audit factual drift against code.
- Do not require a package, CLI, model call, or external network access.
- Do not invent absent concerns that are not in the local catalog.
