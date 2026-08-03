# Pillars Init Prompt

Paste this entire file into your AI coding tool's chat to bootstrap the Pillars standard in the current project. Works in any tool: Claude Code, Cursor, Codex CLI, Gemini CLI, opencode, Aider, Windsurf, Cline, Continue, Pieces for Developers, or any other AI assistant that can read a project and write files.

For installation as a native command/skill in specific tools, see the relevant install doc in this folder.

---

## Task: bootstrap Pillars in this project

You are going to set up the [Pillars](https://github.com/hannsxpeter/pillars) standard in the current project. Follow this procedure exactly. Do not skip steps.

### Step 0 — Check for existing adoption

Run:

```
ls AGENTS.md agents/
```

If either `AGENTS.md` or `agents/` exists with content, stop and ask the user:

> Pillars is already partially set up. Do you want to: (a) abort, (b) re-initialize from scratch (overwrite), or (c) augment (fill in missing pillars only)?

Wait for the user's decision before continuing. Otherwise proceed.

### Step 1 — Detect the project archetype

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

### Step 2 — Fetch canonical files

Fetch these from the Pillars repo (use your tool's web-fetch or download capability):

- AGENTS.md: `https://raw.githubusercontent.com/hannsxpeter/pillars/v1.2.0/AGENTS.md`
- SPEC: `https://raw.githubusercontent.com/hannsxpeter/pillars/v1.2.0/SPEC.md` (reference)
- PILLARS: `https://raw.githubusercontent.com/hannsxpeter/pillars/v1.2.0/PILLARS.md` (reference)
- Starter absent catalog: `https://raw.githubusercontent.com/hannsxpeter/pillars/v1.2.0/agents/catalog.yaml`

If you cannot fetch URLs, use the inline AGENTS.md template at the bottom of this prompt.

### Step 3 — Write AGENTS.md at the repo root

Drop the fetched AGENTS.md content (or the inline template below) at `<project-root>/AGENTS.md`. Replace the `excluded: []` block with archetype-appropriate exclusions:

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

### Step 4 — Create `agents/` directory with always-loaded stubs

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

### Step 5 — Write Core-pillar stubs that apply

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

For each `yes` (or `maybe` after asking the user), write a stub at `agents/<pillar>.md` with the standard 8-section template. Use these triggers per pillar:

| Pillar | triggers |
|---|---|
| stack | [stack, framework, library, dependency, package, version] |
| arch | [architecture, service, module, boundary, design, system] |
| data | [database, schema, migration, query, table, column, model] |
| api | [api, endpoint, route, request, response, http, rpc] |
| ui | [ui, component, page, layout, design, style, theme] |
| auth | [auth, login, session, role, permission, access, user] |
| quality | [test, testing, error, lint, style, naming] |
| development | [develop, development, local setup, bootstrap, debug] |
| release | [release, version, changelog, publish, semver] |
| deploy | [deploy, cutover, environment, rollback, promotion] |
| observe | [log, logging, metric, tracing, alert, monitoring, runbook] |

All stubs get `must_read_with: []` and `see_also: []` initially; couplings get added when content arrives.

### Step 6 — Summary

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

Next steps:
1. Fill context.md with what this project is.
2. Fill repo.md with your folder layout.
3. Fill other stubs as decisions get made.

The agent will read AGENTS.md every session and align to your pillars.
```

### Step 7 — Offer immediate next action

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

This project follows [Pillars 1.2.0](https://github.com/hannsxpeter/pillars/tree/v1.2.0). Coding agents read project pillar files before acting.

## At the start of any task

1. Resolve applicable scopes from repository root to the task target. Apply outer scopes first; nearest-scope guidance wins conflicts.
2. In each scope, scan pillar frontmatter, local exclusions, and optional `agents/catalog.yaml`.
3. Load always-loaded pillars. Match task tokens against other `triggers`; matches are primaries and catalog matches are absent concerns.
4. Add each primary's `must_read_with` identities at depth 1. Use path-qualified identities for sub-pillars.
5. Add a selected pillar's `see_also` target only when the task matches its identity, `triggers`, or `covers` with the same matcher.
6. Read selected bodies and comply with Rules, Workflows, Watchouts, and Gaps.

## Handling missing pillars

| State | Action |
|---|---|
| `status: present` | Load and comply. |
| `status: stub` | Concern acknowledged but rules undefined. Ask the human. Do not infer silently. |
| Identity in `excluded:` | Treat as not applicable in this scope. |
| Trigger matches local `agents/catalog.yaml` entry | Infer from code, state the assumption, and recommend the pillar. |
| No local file, exclusion, or catalog entry | Make no Pillars-specific claim. |

If `context.md` or `repo.md` is missing and not explicitly excluded, pause and ask for a stub or exclusion.

## Portable matcher

Lowercase ASCII letters, replace non-alphanumeric runs with spaces, and match complete contiguous token sequences. Semantic matching may add results but cannot remove deterministic matches.

## Excluded pillars

```yaml
excluded: []
```

## Reference

- Pillar files: `./agents/*.md`
- Optional absent catalog: `./agents/catalog.yaml`
- Spec: https://github.com/hannsxpeter/pillars/blob/v1.2.0/SPEC.md
- Pillar enumeration: https://github.com/hannsxpeter/pillars/blob/v1.2.0/PILLARS.md
````

---

## Reference

- Pillars standard: https://github.com/hannsxpeter/pillars
- SPEC.md: https://github.com/hannsxpeter/pillars/blob/v1.2.0/SPEC.md
- PILLARS.md: https://github.com/hannsxpeter/pillars/blob/v1.2.0/PILLARS.md
- Worked examples: https://github.com/hannsxpeter/pillars/tree/v1.2.0/examples
