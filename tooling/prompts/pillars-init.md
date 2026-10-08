# Pillars Init Prompt

Paste this entire file into your AI coding tool's chat to bootstrap the Pillars standard in the current project. Works in any tool: Claude Code, Cursor, Codex CLI, Gemini CLI, opencode, Aider, Windsurf, Cline, Continue, Pieces for Developers, or any other AI assistant that can read a project and write files.

For installation as a native command/skill in specific tools, see the relevant install doc in this folder.

---

## Task: bootstrap Pillars in this project

You are going to set up the [Pillars](https://github.com/hannsxpeter/pillars) standard in the current project. Follow this procedure exactly. Do not skip steps.

### Step 0: Check for existing adoption

Run every step from the scope root: the repository root, or a package directory when the user wants Pillars for one package inside a monorepo. For a package, first confirm it is a genuinely independent scope. Root guidance applies first and nearest-scope guidance wins conflicts. A package `AGENTS.md` may be a thin declaration that inherits the root protocol and records only local exclusions or refinements.

Run:

```
ls AGENTS.md agents/
```

If either `AGENTS.md` or `agents/` exists with content, stop and ask the user:

> Pillars is already partially set up. Do you want to: (a) abort, (b) re-initialize from scratch (overwrite), or (c) augment (fill in missing pillars only)?

Wait for the user's decision before continuing. Otherwise proceed.

Then run:

```
ls -d docs/adr docs/decisions decisions adr 2>/dev/null
```

If a decision-record corpus exists, do NOT migrate it into pillar sections. Flattening those files discards the supersession history that made them worth keeping. Note the path for the Step 6 summary and plan to reference it from `arch.md`. Step 5 covers routing them instead.

### Step 1: Detect the project archetype

Scan the project structure and pick the archetype that best matches. Priority order:

| Archetype | Signals |
|---|---|
| CLI tool | `Cargo.toml` with `[bin]`, `go.mod` with `cmd/`, `package.json` with `bin` field, Python `console_scripts` |
| Internal API service | server framework deps (express/fastapi/gin/axum), no React/Vue/Svelte, no static asset dir |
| SaaS dashboard / web app | React/Next/Remix/Vue/Svelte/Nuxt/Solid in deps, `app/` or `pages/` dir |
| Marketing site | Astro/Hugo/Jekyll/11ty/Gatsby, CMS integration (Sanity/Contentful), heavy `content/` |
| Mobile app | `pubspec.yaml` (Flutter), `Podfile` (iOS), `app/build.gradle` (Android), React Native deps |
| ML pipeline | torch/tensorflow/scikit-learn/transformers, `models/`, `notebooks/`, `pipelines/`, MLflow/Argo configs |
| Open-source library | publish config, documented public API, no application entry point |
| Empty / greenfield | Few/no source files |

If ambiguous (e.g., Next.js could be SaaS or marketing), ask the user to confirm before proceeding.

If empty/greenfield, ask what they're building and map to the closest archetype.

### Step 2: Fetch canonical files

Fetch these from the Pillars repo (use your tool's web-fetch or download capability):

- AGENTS.md: `https://raw.githubusercontent.com/hannsxpeter/pillars/v1.2.2/AGENTS.md`
- SPEC: `https://raw.githubusercontent.com/hannsxpeter/pillars/v1.2.2/SPEC.md` (reference)
- PILLARS: `https://raw.githubusercontent.com/hannsxpeter/pillars/v1.2.2/PILLARS.md` (reference)
- Starter absent catalog: `https://raw.githubusercontent.com/hannsxpeter/pillars/v1.2.2/agents/catalog.yaml`

If you cannot fetch URLs, use the inline AGENTS.md template at the bottom of this prompt. It is the canonical file, word for word. If you cannot fetch the starter catalog, build `agents/catalog.yaml` (`version: 1`, then an `absent:` list) from the Core table in Step 5 for every Core identity you neither stub nor exclude, and tell the user the Common entries were skipped.

### Step 3: Write AGENTS.md at the scope root

Drop the fetched AGENTS.md content (or the inline template below) at `<scope-root>/AGENTS.md`. Replace the `excluded: []` block with archetype-appropriate exclusions:

| Archetype | Typical exclusions |
|---|---|
| CLI tool | ui, api, auth, deploy, observe, i18n, a11y, analytics, async, cache, notifications |
| Internal API service | ui, a11y, seo (if no end-user surface), notifications (if no end users) |
| SaaS dashboard | [] (leave empty initially) |
| Marketing site | data, api, auth (if no users), observe (if platform-provided), async |
| Mobile app | seo, i18n (if single-locale), realtime (if not collaborative) |
| ML pipeline | ui, i18n, a11y, notifications, analytics |
| Open-source library | ui, api (if not a service), auth, observe, deploy (if not hosted), notifications, analytics |
| Empty/greenfield | [] (leave empty) |

Use the structured form with reasons:

```yaml
excluded:
  - name: ui
    reason: CLI tool; no visual UI surface
  - name: observe
    reason: stderr logging only; no metrics or tracing
```

Infer concrete reasons from detected stack when possible (e.g., "Vercel Analytics covers monitoring" for Vercel-hosted projects).

### Step 4: Create `agents/` directory with always-loaded stubs

```
mkdir agents
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

(stub) Fill with the project's identity, domain language, product invariants, glossary.

## Context

(stub) Describe what this project is, who it's for, the domain language.

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

- This pillar is a stub. Ask the user about: what the project is, who uses it, core domain vocabulary, what must be true at all times.
```

Write `agents/repo.md` with the same structure but covering file layout, naming, structural decisions. Use `see_also: [context]` and the appropriate Scope/Context placeholders.

### Step 5: Write Core-pillar stubs that apply

Use this matrix to decide which Core pillars get stubs:

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

For each `yes` (or `maybe` after asking the user), write a stub at `agents/<pillar>.md` with the standard 8-section template and `status: stub`. A `no` gets no stub; that identity stays in `agents/catalog.yaml` unless Step 3 excluded it. Copy `covers` and `triggers` from this table, which matches the starter catalog:

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

All stubs get `must_read_with: []` and `see_also: []` initially; couplings get added when content arrives.

Decision rationale goes in each pillar's own `Decisions` section by default. Do NOT scaffold `agents/arch/decisions.md` at init. Raise the decision-depth sub-pillar only when the project already has a decision-record corpus (Step 0) or the user says rationale churns enough that a flat section will not hold it. When warranted, `agents/arch/decisions.md` takes the identity `arch/decisions`, routes on its own triggers, and may declare `must_read_with: [arch]`. The parent is not auto-loaded. `stack/decisions` works the same way for technology choices.

### Step 6: Summary

Print a concise summary to the user:

```
Pillars adopted (archetype: <archetype-name>).

Files created:
- AGENTS.md
- agents/context.md (stub, always-loaded)
- agents/repo.md (stub, always-loaded)
- agents/catalog.yaml (offline metadata for remaining absent concerns)
- agents/<core-pillars>.md (N stubs)

Excluded pillars: <list with reasons>

Existing decision records: <path, or omit this line entirely if none were found>

Next steps:
1. Fill context.md with what this project is.
2. Fill repo.md with your folder layout.
3. Fill other stubs as decisions get made.

The agent will read AGENTS.md every session and align to your pillars.
```

### Step 7: Offer immediate next action

Ask:

> Want me to populate `context.md` now from your description, or leave it as a stub?

If yes, draft `context.md` from what the user has told you. Use the same procedure as `pillars-author` (see the companion `pillars-author.md` prompt).

---

## Constraints

- Do NOT write files without showing the user what's about to land.
- Do NOT populate stubs with inferred content. Stubs stay stubs until the user fills them.
- Do NOT overwrite existing `AGENTS.md` or pillar files without explicit confirmation.
- Do NOT exceed the 8-section template per pillar.
- Do NOT modify `.cursorrules`, `CLAUDE.md`, `.windsurfrules`, or other tool-specific files. If they exist, note them and recommend the user reduce them to a redirect to AGENTS.md.

## Inline AGENTS.md template (use if URL fetch is unavailable)

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

---

## Reference

- Pillars standard: https://github.com/hannsxpeter/pillars
- SPEC.md: https://github.com/hannsxpeter/pillars/blob/v1.2.2/SPEC.md
- PILLARS.md: https://github.com/hannsxpeter/pillars/blob/v1.2.2/PILLARS.md
- Worked examples: https://github.com/hannsxpeter/pillars/tree/v1.2.2/examples
