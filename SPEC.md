# Pillars Specification

Version 1.2.2.

> **Who this document is for.** This is the precise, formal definition of the standard, written for people implementing Pillars in a tool or writing pillars by hand and wanting the exact rules. It is deliberately technical.
>
> If you just want to use Pillars in your project, you do not need to read this. Start with [the README](README.md), then [PILLARS.md](PILLARS.md) for the catalog of topics, then [FAQ.md](FAQ.md) for practical questions. Your AI assistant can read this document on your behalf.

This document defines the Pillars standard. It specifies pillar structure, routing, local discovery, nested scopes, and missing-pillar behavior. An implementation that conforms to this spec is *Pillars-compatible*.

## 1. Philosophy

A pillar surfaces what an agent cannot reliably infer from code. Coding agents are capable; the standard exists to prevent drift, not to put the agent on rails.

Core principle:

> Include prescriptive content only when it would not be inferred from the facts.

"Project uses Drizzle" does not need a rule that says "use Drizzle." The agent can infer that. "Never use raw SQL outside `db/raw.ts`" does need stating because code alone may not reveal that constraint.

Pillars should read like an experienced engineer briefing a new contributor on day one. They are conversational, declarative, and reasoned, not compliance documents.

## 2. Repository layout and scopes

A Pillars scope contains:

- `AGENTS.md` at the scope root: the protocol description.
- `agents/` at the scope root: pillar files and, optionally, `catalog.yaml`.

The repository root is the default scope. A monorepo or nested project may define another scope by placing its own `AGENTS.md` and `agents/` directory in a descendant directory.

The root `AGENTS.md` carries the full loading protocol. A descendant `AGENTS.md` may be a thin scope declaration when it explicitly inherits that root protocol and records only local exclusions or refinements. This avoids copying the protocol into every package while keeping the scope boundary visible to agents and tools.

Pillar files use the `.md` extension and live at `agents/<name>.md` or `agents/<parent>/<name>.md`. One level of sub-pillar nesting is portable. Deeper pillar nesting is outside this version of the standard.

### 2.1 Applicable scopes

For a task that names or modifies a path, applicable scopes are every scope root that contains that path, ordered from the repository root to the nearest containing scope. For a task without a target path, use the current working directory as the target. If multiple unrelated targets are in different scopes, compute a load set for each scope chain and keep the results labeled by scope.

Each applicable scope computes its local load set independently. Load ancestor guidance before descendant guidance.

### 2.2 Inheritance and precedence

- Non-conflicting guidance from every applicable scope applies.
- When two applicable pillars with the same identity conflict, the pillar in the nearest scope wins.
- A descendant exclusion suppresses an inherited task-routed pillar with the same identity for that descendant scope.
- A descendant pillar and descendant exclusion with the same identity are invalid.
- An ancestor always-loaded pillar remains applicable unless a descendant provides the same identity, in which case both may be read but the descendant wins on conflicts.
- Dependencies and `see_also` references resolve within their declaring scope. They do not reach into ancestor or descendant scopes.

A project with only the repository-root scope behaves exactly like a Pillars 1.0 project.

## 3. Pillar file structure

Every pillar file consists of YAML frontmatter followed by an 8-section markdown body.

### 3.1 Frontmatter schema

```yaml
---
pillar: data
status: present
always_load: false
covers: [database schema, migrations, queries, storage]
triggers: [database, schema, migration, query, table, column]
must_read_with: [auth, config]
see_also: [api, observe]
---
```

| Field | Type | Required | Default | Meaning |
|---|---|---|---|---|
| `pillar` | string | yes | none | Leaf name. Must match the filename without `.md`. |
| `status` | enum | no | `present` | `present` or `stub`. See section 6. |
| `always_load` | boolean | no | `false` | If `true`, load the pillar for every task in its scope. |
| `covers` | list of strings | yes | none | Short scope selectors for readers and conditional `see_also` matching. |
| `triggers` | list of strings | yes unless always-loaded | none | Keywords or phrases used to select primary pillars. |
| `must_read_with` | list of identities | no | `[]` | Direct hard dependencies. Loaded depth 1 only. |
| `see_also` | list of identities | no | `[]` | Soft dependencies loaded only when the task matches the referenced area. |

List items are non-empty strings. Selector lists (`covers`, `triggers`) are unique after section 5.1 normalization. Reference lists are unique by exact canonical identity.

### 3.2 Path-derived identity

The canonical identity is derived from the path relative to `agents/`:

| Path | Identity | `pillar` value |
|---|---|---|
| `agents/auth.md` | `auth` | `auth` |
| `agents/auth/agent-registration.md` | `auth/agent-registration` | `agent-registration` |

Reference fields use canonical identities. Existing top-level references such as `auth` and `config` remain valid. A sub-pillar reference must be path-qualified, such as `auth/agent-registration`. A bare name resolves only to a top-level pillar. It never searches sub-pillars by leaf name.

Identity segments use lowercase ASCII letters, digits, and internal hyphens. A segment starts and ends with a letter or digit. This makes identity comparison portable across case-sensitive and case-insensitive filesystems.

### 3.3 Body template

The body contains these headings in order:

1. **Scope**: what the pillar covers and excludes.
2. **Context**: declarative project facts, locations, terms, and conventions.
3. **Decisions**: non-obvious choices and their reasons.
4. **Rules**: hard constraints not inferable from Context.
5. **Workflows**: multi-step procedures that are not obvious from Context.
6. **Watchouts**: experience-based warnings with reasoning.
7. **Touchpoints**: human-readable couplings that mirror frontmatter.
8. **Gaps**: explicit undecided areas where the agent should ask.

Empty sections contain `(none)`. Sections 3 through 6 are populated only when they add distinct value.

### 3.4 Maturity gradient

A pillar exists once it has frontmatter and a Scope statement. Other sections fill in over the project's lifetime:

```text
stub -> partially populated -> fully populated
```

There is no obligation to fill every section with substantive content.

### 3.5 Context budgets

Budgets protect routing value without turning prose length into a conformance contest.

| Category | Recommended per file | Recommended scope total |
|---|---|---|
| Always-loaded | at most 1,000 words and 8 KiB | at most 2,000 words and 16 KiB |
| Task-routed | at most 2,000 words and 16 KiB | no fixed total because only a load set is read |

Exceeding a budget is a warning, not a compatibility error. A project may document a justified exception. Authors should split a routed pillar when a stable sub-domain can stand alone. Always-loaded pillars should be trimmed rather than split because every task pays their cost.

## 4. Local absent-pillar catalog

Absent-pillar discovery must not depend on a website, a model's memory, or a global catalog. A scope may carry an offline discovery supplement at `agents/catalog.yaml`:

```yaml
version: 1
absent:
  - identity: observe
    covers: [system health, telemetry]
    triggers: [log, logging, metric, tracing, alert, monitoring]
  - identity: data/migrations
    covers: [schema change process]
    triggers: [migration, schema change]
```

The catalog lists concerns that are known in this project but do not yet have pillar files. Present pillars remain frontmatter-driven and must not be duplicated in `absent`. Exclusions remain in `AGENTS.md` and must not be duplicated in the catalog.

`catalog.yaml` is optional for compatibility with 1.0 projects. If it is absent, the scope has no locally declared silent gaps. Tools must not fetch the standard catalog or invent absent pillars during routing. Initializers should create a local catalog when the adopter wants executable gap discovery.

Catalog identities and selectors follow the same rules as pillar frontmatter. `covers` is optional; `triggers` is required. The always-loaded floor identities `context` and `repo` cannot be catalog entries because their absence requires an immediate decision.

## 5. Loading mechanism

At the start of every task, for each applicable scope:

1. **Inventory local metadata.** Scan pillar frontmatter, `AGENTS.md` exclusions, and the optional local catalog.
2. **Load always-pillars.** Select every local pillar with `always_load: true`.
3. **Identify primaries and silent gaps.** Match the task against each non-always pillar's `triggers` and each catalog entry's `triggers` using section 5.1. Matching present pillars are primaries. Matching catalog entries follow the absent protocol.
4. **Add hard dependencies.** Add every identity in each primary's `must_read_with`, depth 1 only. Do not follow dependencies of dependency-only pillars.
5. **Consult soft references.** For each selected pillar, resolve each `see_also` target. Add it only when the task matches the target identity, `triggers`, or `covers` using section 5.1. Do not follow `see_also` recursively.
6. **Load and comply.** Read selected bodies. Follow `Rules`, apply `Workflows`, heed `Watchouts` with judgment, and defer to `Gaps`.

Deduplicate by scope plus identity. Preserve every reason a pillar was selected.

### 5.1 Portable minimum matcher

All conforming implementations support this deterministic baseline:

1. Convert ASCII `A` through `Z` to lowercase.
2. Replace every run of characters outside ASCII `a` through `z` and `0` through `9` with one space.
3. Trim leading and trailing spaces.
4. Split on spaces.
5. A selector matches when its complete token sequence appears contiguously in the normalized task tokens.

For example, `schema-change` and `Schema change` both normalize to `schema change`. `api` does not match `capital`. A selector that normalizes to no tokens is invalid.

The minimum matcher applies to primary triggers, absent catalog triggers, and conditional `see_also` area selectors. Implementations may add semantic or non-ASCII matching as an optional superset, but they must expose or retain the deterministic baseline result. Conformance fixtures use only the minimum matcher.

### 5.2 Why depth 1

Depth 1 makes coupling predictable. Reading a primary's frontmatter shows exactly what it brings into the load set. Frequently needed pillars should graduate to `always_load: true` instead of becoming hidden transitive dependencies.

These patterns are boundary smells and should produce warnings:

- More than three identities in `must_read_with`.
- Many pillars repeating the same dependency group.
- A pillar approaching its routed content budget without a clean sub-domain boundary.

## 6. Missing-pillar protocol

| State | Local indicator | Agent behavior |
|---|---|---|
| **Present** | File exists; `status: present` or omitted | Load and comply normally. |
| **Stub** | File exists; `status: stub` | Ask before making decisions in this area. Do not silently infer. |
| **Excluded** | Identity appears in local `AGENTS.md` exclusions | Treat the concern as not applicable in this scope. |
| **Absent** | Matching identity appears in local `agents/catalog.yaml` and no file or exclusion exists | Infer from code, state the assumption, and recommend creating the pillar. |
| **Unknown** | No local file, exclusion, or catalog entry | Make no Pillars-specific claim about that concern. |

A `must_read_with` reference to a missing, non-excluded identity is a structural error because the author declared a hard dependency. A `see_also` reference may resolve to a local catalog entry; when the task matches that soft area, handle it as an absent concern.

### 6.1 Always-loaded floor

`context` and `repo` are the standard floor. If either is missing and not excluded, pause and ask the human to create a stub or explicitly exclude it. Explicit floor exclusions are valid for incremental compatibility but should produce a warning because they remove baseline project context. A floor identity cannot be both present and excluded.

### 6.2 Exclusion form

```yaml
excluded:
  - name: observe
    reason: Platform telemetry and built-in alerting cover this project
  - name: i18n
    reason: English-only product
```

A bare list such as `excluded: [observe, i18n]` is valid. Reasons are recommended.

## 7. AGENTS.md requirements

A Pillars-compatible `AGENTS.md` contains:

- A reference to the Pillars standard.
- The loading protocol in section 5.
- The local missing-pillar behavior in section 6.
- An `excluded:` block, which may be empty.
- Nested-scope precedence when the repository uses nested scopes.

`AGENTS.md` does not enumerate present pillar names. Present routing metadata lives in pillar frontmatter. Optional absent routing metadata lives in `agents/catalog.yaml`.

A reference implementation is in this repository's [AGENTS.md](AGENTS.md).

## 8. Conformance and versioning

Pillars compatibility does not require the repository's validator or any external service. Implementations can validate the standard with their own tooling. Deterministic routing implementations should be checked against representative task-to-load-set fixtures.

This spec uses semantic versioning. The current version is 1.2.2.

- Major: incompatible changes to existing pillar files or loading behavior.
- Minor: backward-compatible additions or newly specified behavior.
- Patch: corrections that do not change behavior.

Pillars 1.1 keeps existing top-level identities and single-scope behavior intact. Local catalogs, path-qualified sub-pillar references, deterministic matching, and nested scopes add portable behavior without requiring adopters to rewrite 1.0 top-level pillars.

Pillars 1.2 changes no schema, identity, or loading rule. It adds the decision-depth sub-pillar pattern to the catalog guidance in `PILLARS.md`. A 1.1 project is a conforming 1.2 project with no edits.

## 9. License

This specification is dedicated to the public domain under [CC0 1.0 Universal](LICENSE). No attribution is required. Attribution is welcomed but never enforced.
