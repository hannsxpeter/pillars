---
name: pillars-init
description: "Bootstrap the Pillars standard in a project. Detects the project archetype, writes AGENTS.md, creates `./agents/`, writes always-loaded and applicable Core stubs, reconciles a local absent catalog, and records archetype exclusions. Use this skill when the user asks to set up, adopt, initialize, scaffold, or install Pillars."
version: 0.4.0
updated: 2026-10-08
compatible_with:
  - claude-code
standard_version: ">=1.1.0"
---

# Pillars Init

This skill bootstraps the [Pillars](https://github.com/hannsxpeter/pillars) standard in a project. It is the recommended entry point: it handles archetype detection, AGENTS.md placement, pillar stub creation, and exclusion list setup in one pass.

## When to use this skill

Trigger when the user wants Pillars set up in their current project. Typical requests:

- "Set up Pillars on this project."
- "Adopt the Pillars standard."
- "Initialize Pillars."
- "Scaffold AGENTS.md and pillars."
- "Install Pillars."

If the user wants to *author a specific pillar* from existing code rather than scaffold the whole standard, prefer `pillars-author`. If they want to *check existing pillars* for drift, prefer `pillars-verify`.

## What this skill produces

After running, the user's project will contain:

```
<project>/
├── AGENTS.md             # the protocol description, copied from the Pillars repo
└── agents/
    ├── context.md        # stub, status: stub
    ├── repo.md           # stub, status: stub
    ├── catalog.yaml      # offline metadata for absent concerns
    └── <core-pillars>.md # stubs for Tier 1 pillars that apply to this archetype
```

With archetype-appropriate `excluded:` entries in AGENTS.md.

## Procedure

Follow these steps in order. Each step has a specific output the next step depends on.

### Step 0. Confirm intent and check for existing adoption

Before scaffolding anything, check whether the project already has Pillars in place.

```bash
ls AGENTS.md agents/ 2>/dev/null
```

If `AGENTS.md` already exists, or the `agents/` directory has content:

- Tell the user what you found.
- Ask whether they want to: (a) abort, (b) re-initialize from scratch (will overwrite), or (c) augment by filling in missing pillars only.
- Wait for their decision before proceeding.

If neither exists, proceed.

Then check for an existing decision-record corpus:

```bash
ls -d docs/adr docs/decisions decisions adr 2>/dev/null
```

If one exists, do not migrate it and do not rewrite those files into pillar sections. They are already the project's record, and flattening them into a `Decisions` section discards the supersession history that made them worth keeping. Note the location so Step 6 can report it, and plan to reference it from `arch.md`. If the user wants those records task-routed rather than only referenced, Step 5 covers the decision-depth sub-pillar.

### Step 1. Detect the project archetype

The archetype determines which pillars apply and which are typically excluded. Detect by scanning the project structure and config files. Use this priority order:

| Archetype | Signals |
|---|---|
| **CLI tool** | `Cargo.toml` with `[bin]`, `go.mod` with `cmd/` directory, `package.json` with `bin` field, Python project with `console_scripts` entry point, single-binary build target |
| **Internal API service** | `package.json` with no `react`/`vue`/`svelte`, server framework deps (express, fastapi, gin, axum), no static asset directory |
| **SaaS dashboard / web app** | `package.json` with `react`/`next`/`remix`/`vue`/`svelte`/`nuxt`/`solid`, `app/` or `pages/` directory, `public/` or static asset dir |
| **Marketing site** | Static site generator (Astro, Hugo, Jekyll, 11ty, Gatsby), CMS integration (Sanity, Contentful, Strapi), heavy `content/` directory, public-facing rather than user-account-driven |
| **Mobile app** | `pubspec.yaml` (Flutter), `Podfile`/`*.xcodeproj` (iOS), `app/build.gradle` (Android), React Native (`react-native` in deps) |
| **ML pipeline / service** | `requirements.txt` or `pyproject.toml` with `torch`/`tensorflow`/`scikit-learn`/`transformers`, `models/`, `notebooks/`, `pipelines/`, MLflow/Argo/Kubeflow configs |
| **Open-source library** | `package.json`/`pyproject.toml`/`Cargo.toml`/`go.mod` with publish config but no application entry point; documented public API; no `app/` or service code |
| **Empty / greenfield** | Few files, no source code, possibly just a `package.json` skeleton or nothing |

If detection is ambiguous (e.g., a Next.js project that could be a SaaS dashboard or a marketing site), ask the user to confirm before proceeding.

If the project is **empty/greenfield**, ask the user what they're building. Map their answer to the closest archetype above. If their answer doesn't fit, treat as a custom archetype and skip the exclusion defaults.

### Step 2. Fetch the canonical AGENTS.md and template references

The skill needs the current canonical text of AGENTS.md and the pillar template. Fetch from the Pillars repo:

- AGENTS.md: `https://raw.githubusercontent.com/hannsxpeter/pillars/v1.2.2/AGENTS.md`
- Spec for template reference: `https://raw.githubusercontent.com/hannsxpeter/pillars/v1.2.2/SPEC.md`
- Catalog for archetype exclusions: `https://raw.githubusercontent.com/hannsxpeter/pillars/v1.2.2/PILLARS.md`
- Starter absent catalog: `https://raw.githubusercontent.com/hannsxpeter/pillars/v1.2.2/agents/catalog.yaml`

Use the `WebFetch` tool. Cache locally for the rest of the session.

If fetching fails, use the canonical AGENTS.md text in the "Fallback AGENTS.md" section below; it matches the published file word for word. If you cannot fetch the starter catalog, build `agents/catalog.yaml` (`version: 1`, then an `absent:` list) from the Core table in Step 5 for every Core identity you neither stub nor exclude, and tell the user the Common entries were skipped.

### Step 3. Write AGENTS.md

Drop the fetched AGENTS.md text at the scope root: the repository root, or the package directory when adopting for one monorepo package. Replace the `excluded: []` block with archetype-appropriate exclusions from this table (drawn from PILLARS.md's archetype starter lists):

| Archetype | Typical exclusions |
|---|---|
| CLI tool | ui, api, auth, deploy, observe, i18n, a11y, analytics, async, cache, notifications |
| Internal API service | ui, a11y, seo (if no end-user surface), notifications (if no end users) |
| SaaS dashboard | (none initially; add as decisions get made) |
| Marketing site | data, api, auth (if no users), observe (if platform-provided), async |
| Mobile app | seo, i18n (if single-locale), realtime (if not collaborative) |
| ML pipeline | ui, i18n, a11y, notifications, analytics |
| Open-source library | ui, api (if not a service), auth, observe, deploy (if not hosted), notifications, analytics |
| Empty/greenfield/custom | [] (leave empty; user can add later) |

Use the structured form with reason fields:

```yaml
excluded:
  - name: ui
    reason: CLI tool; no visual UI surface
  - name: observe
    reason: stderr logging is the only observability; no metrics or tracing
```

If the archetype's reason is generic, infer something concrete from the detected stack (e.g., "Vercel Analytics covers monitoring" for a Vercel-deployed marketing site if you can confirm Vercel from the config).

### Step 4. Create the `./agents/` directory and write always-loaded stubs

```bash
mkdir -p agents
```

Write the fetched starter catalog to `agents/catalog.yaml`. Remove entries for every pillar stub created below and every identity recorded in `excluded:`. The catalog must contain only locally absent concerns.

Write `agents/context.md`:

```yaml
---
pillar: context
status: stub
always_load: true
covers: [project identity, domain language, product invariants, glossary]
triggers: []
must_read_with: []
see_also: [repo]
---

## Scope

(stub) Fill in with the project's identity, domain language, product invariants, and a glossary of canonical terms.

## Context

(stub) Describe what this project is, who it's for, the domain language. The agent will ask before inferring while this remains a stub.

## Decisions

(none)

## Rules

(none)

## Workflows

(none)

## Watchouts

(none)

## Touchpoints

- `see_also: [repo]`

## Gaps

- This pillar is a stub. Ask the user about: what the project is, who uses it, the core domain vocabulary, what *must* be true at all times.
```

Write `agents/repo.md`:

```yaml
---
pillar: repo
status: stub
always_load: true
covers: [file layout, naming conventions, where things go, repository structure]
triggers: []
must_read_with: []
see_also: [context]
---

## Scope

(stub) Fill in with the project's file layout, naming conventions, and structural decisions.

## Context

(stub) Describe the folder structure, file naming patterns, where different kinds of code/docs go. The agent will ask before inferring while this remains a stub.

## Decisions

(none)

## Rules

(none)

## Workflows

(none)

## Watchouts

(none)

## Touchpoints

- `see_also: [context]`

## Gaps

- This pillar is a stub. Ask the user about: top-level folder layout, source code organization, naming patterns, where tests/configs/docs live.
```

### Step 5. Write Core-pillar stubs that apply to the archetype

Not every Tier 1 pillar applies to every archetype. Use this matrix to decide which Core pillars to stub:

| Pillar | CLI | Internal API | SaaS | Marketing | Mobile | ML | OSS lib | Greenfield |
|---|---|---|---|---|---|---|---|---|
| stack | yes | yes | yes | yes | yes | yes | yes | yes |
| arch | yes | yes | yes | maybe | yes | yes | maybe | yes |
| data | maybe | yes | yes | no | yes | yes | no | maybe |
| api | no | yes | yes | no | maybe | yes | maybe | yes |
| ui | no | no | yes | yes | yes | no | no | maybe |
| auth | no | maybe | yes | no | yes | yes | no | maybe |
| quality | yes | yes | yes | yes | yes | yes | yes | yes |
| development | yes | yes | yes | yes | yes | yes | yes | yes |
| release | yes | yes | yes | yes | yes | yes | yes | yes |
| deploy | no | yes | yes | yes | yes | yes | no | yes |
| observe | no | yes | yes | maybe | yes | yes | no | maybe |

`maybe` means "ask the user before stubbing." `no` means no stub: the identity stays in `agents/catalog.yaml` as a known absence unless Step 3 excluded it.

For each pillar marked `yes` (or `maybe` after confirmation), write a stub at `agents/<pillar>.md` following the same shape as the always-loaded stubs above, with `always_load: false`. Copy `covers` and `triggers` from this table, which matches the starter catalog:

| Pillar | covers | triggers |
|---|---|---|
| stack | [technology choices, dependencies, version constraints] | [stack, framework, library, dependency, package, version] |
| arch | [system architecture, services, boundaries, data flow] | [architecture, service, module, boundary, system design] |
| data | [data model, schema, migrations, queries, storage] | [database, schema, migration, query, table, column, model] |
| api | [api contracts, requests, responses, versioning] | [api, endpoint, route, request, response, http, rpc] |
| ui | [visual interface, components, design tokens] | [ui, component, page, layout, style, theme] |
| auth | [identity, sessions, permissions, access] | [auth, login, session, role, permission, access, user] |
| quality | [testing, errors, code style, naming] | [test, testing, error, lint, style, naming] |
| development | [local setup, developer workflow, debugging] | [develop, development, local setup, bootstrap, debug] |
| release | [versioning, release preparation, publication] | [release, version, changelog, publish, semver] |
| deploy | [environments, promotion, rollback, cutover] | [deploy, environment, rollback, promotion, cutover] |
| observe | [logging, metrics, tracing, alerts, runbooks] | [log, logging, metric, tracing, alert, monitoring, runbook] |

Use `must_read_with: []` for stubs; the user can add couplings once content exists. Use `see_also: []` for stubs.

Decision rationale belongs in each pillar's own `Decisions` section by default, so do not scaffold `agents/arch/decisions.md` at init. Raise the decision-depth sub-pillar only when the project already has a decision-record corpus (Step 0) or the user says rationale churns enough that a flat section will not hold it. When it is warranted, `agents/arch/decisions.md` takes the identity `arch/decisions`, routes on its own triggers like any other pillar, and may declare `must_read_with: [arch]`. The parent is not auto-loaded. `stack/decisions` works the same way for technology choices. See "Common sub-pillar patterns" in PILLARS.md.

### Step 6. Summarize what landed

Print a concise summary to the user:

```
Pillars adopted.

Files created:
- AGENTS.md (protocol, archetype: <archetype-name>)
- agents/context.md (stub, always-loaded)
- agents/repo.md (stub, always-loaded)
- agents/catalog.yaml (offline metadata for remaining absent concerns)
- agents/stack.md (stub)
- agents/quality.md (stub)
- ... etc ...

Excluded pillars: <list>

Existing decision records: <path, or omit this line entirely if none were found>

Next steps:
1. Fill context.md with what this project is. Run `/pillars-author context` or just edit the file.
2. Fill repo.md with your folder layout.
3. Fill other stubs as decisions get made.

The agent will read AGENTS.md every session and align to your pillars. Stubs prompt the agent to ask; populated pillars let it act.
```

### Step 7. Offer immediate next action

Ask the user:

> Want me to populate `context.md` now from your description, or leave it as a stub for you to fill in?

If yes, transition to `pillars-author` for `context`. If no, end.

## What this skill does NOT do

- **Does not call any external API or LLM directly.** All authoring is the agent's work using its native intelligence; the skill provides procedure, not an autonomous binary.
- **Does not overwrite existing files without explicit confirmation.** Step 0 always checks for prior adoption.
- **Does not populate stubs with inferred content.** Stubs stay stubs until the user (or `pillars-author`) fills them. The standard's protocol says stubs should prompt the agent to ask, not infer.
- **Does not install anything in `~/.claude/`** or modify Claude Code config. This is a project-level scaffold.

## Common failure modes

- **Wrong archetype guess.** If detection is ambiguous, *ask* before writing. Better to clarify than to write the wrong exclusion set.
- **Project has a hand-built `CLAUDE.md` or `.cursorrules`.** Do not delete these. Instead, note them in the summary and recommend the user reduce them to a redirect: `"See AGENTS.md and the pillars in ./agents/."`
- **User wants to adopt for a sub-package in a monorepo.** Pillars supports nested scopes. Confirm the package is a genuinely independent scope, then place its `AGENTS.md` and `agents/` there. Root guidance applies first and nearest-scope guidance wins conflicts. A package `AGENTS.md` may be a thin declaration that inherits the root protocol and records only local exclusions or refinements.

## Fallback AGENTS.md

Use this only when Step 2 cannot fetch the published file.

````markdown
# Pillars: Agent Protocol

This project follows [Pillars 1.2.2](https://github.com/hannsxpeter/pillars/tree/v1.2.2). Coding agents read project pillar files before acting.

## At the start of any task

1. **Resolve scopes.** Starting at the repository root and ending at the task's target path or current directory, find every directory containing both `AGENTS.md` and `agents/`. Apply scopes from outermost to innermost. The nearest scope wins when guidance conflicts.

2. **Inventory local metadata.** In each scope, scan pillar frontmatter recursively. Read exclusions from the local `AGENTS.md` and absent concerns from optional `agents/catalog.yaml`.

3. **Select always and primary pillars.** Load every pillar with `always_load: true`. Match the task against every other pillar's `triggers` using the portable matcher in `SPEC.md`. Matching pillars are primaries. Matching catalog entries are absent concerns.

4. **Add direct dependencies.** Add every identity in each primary's `must_read_with`. Resolve top-level identities such as `auth` at `agents/auth.md` and sub-pillar identities such as `auth/agent-registration` at that exact relative path. Stop at depth 1.

5. **Consult soft references.** Add a selected pillar's `see_also` target only when the task matches that target's identity, `triggers`, or `covers` with the same matcher. Do not follow `see_also` recursively.

6. **Load and comply.** Read selected bodies. Follow `Rules`, apply `Workflows`, heed `Watchouts` with judgment, and defer to `Gaps`. Preserve non-conflicting ancestor guidance; nearest-scope guidance wins conflicts.

## Handling missing pillars

| State | Action |
|---|---|
| `status: present` | Load and comply. |
| `status: stub` | Ask before making decisions in this area. Do not infer silently. |
| Identity in local `excluded:` | Treat as intentionally not applicable in that scope. |
| Trigger matches local `agents/catalog.yaml` entry | Infer from code, state the assumption, and recommend creating the pillar. |
| No local file, exclusion, or catalog entry | Make no Pillars-specific claim about that concern. |

If `context.md` or `repo.md` is missing and not explicitly excluded, pause and ask the human to create a stub or record an exclusion.

## Portable matcher

Lowercase ASCII letters, replace each run of non-alphanumeric characters with one space, trim, and split into tokens. A selector matches when its complete token sequence appears contiguously in the task tokens. Semantic matching may add matches but cannot remove deterministic matches.

## Excluded pillars

```yaml
excluded: []
```

## Reference

- Pillar files in this repo: `./agents/**/*.md`
- Optional absent catalog: `./agents/catalog.yaml`
- Spec: https://github.com/hannsxpeter/pillars/blob/v1.2.2/SPEC.md
- Pillar enumeration: https://github.com/hannsxpeter/pillars/blob/v1.2.2/PILLARS.md
- Worked examples: https://github.com/hannsxpeter/pillars/tree/v1.2.2/examples
````

## Reference

- Pillars standard: https://github.com/hannsxpeter/pillars
- SPEC.md: https://github.com/hannsxpeter/pillars/blob/v1.2.2/SPEC.md
- PILLARS.md: https://github.com/hannsxpeter/pillars/blob/v1.2.2/PILLARS.md
