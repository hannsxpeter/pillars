# Pillars

[![License: CC0-1.0](https://img.shields.io/badge/license-CC0--1.0-blue.svg)](LICENSE)
[![Status: stable 1.2](https://img.shields.io/badge/status-stable%201.2-green.svg)](CHANGELOG.md)
[![Spec: v1.2.1](https://img.shields.io/badge/spec-v1.2.1-green.svg)](SPEC.md)
[![AGENTS.md: compatible](https://img.shields.io/badge/AGENTS.md-compatible-purple.svg)](AGENTS.md)
[![Tooling: optional](https://img.shields.io/badge/tooling-optional-lightgrey.svg)](tooling/)
[![Tool: agnostic](https://img.shields.io/badge/tool-agnostic-blue.svg)](FAQ.md#how-is-this-different-from-cursor-rules-windsurfrules-etc)

**An open standard for project-specific instructions that keep coding agents aligned.**

Pillars is a decomposed, frontmatter-driven convention for documenting what a coding agent (Claude Code, Cursor, Copilot, Codex, Gemini, opencode, Aider, others) needs to know about a project before it writes a single line of code. Inspired by [design.md](https://github.com/google-labs-code/design.md), generalized into a tiered set of pillar files plus a thin `AGENTS.md` loader.

## Quick start

In your project root:

```bash
curl -O https://raw.githubusercontent.com/hannsxpeter/pillars/v1.2.1/AGENTS.md
mkdir agents
curl -o agents/catalog.yaml https://raw.githubusercontent.com/hannsxpeter/pillars/v1.2.1/agents/catalog.yaml
```

Then open your coding agent and say:

> *Adopt Pillars 1.2.1. Read SPEC.md and PILLARS.md from https://github.com/hannsxpeter/pillars/tree/v1.2.1. Scaffold the always-loaded stubs and applicable Core stubs, then remove created or excluded identities from the local catalog.*

The pinned tag makes installation reproducible. `catalog.yaml` is an optional offline index of concerns you have not authored or excluded yet; remove entries as you create pillars. See [Adoption](#adopting-pillars) below for details.

## What Pillars solves

Coding agents drift. Without project-specific context they:

- Reach for the wrong library (Drizzle when you use Prisma).
- Place files where they don't belong (components in `src/lib/` when the convention is `src/components/`).
- Re-invent decisions you already made (auth strategy, error handling, naming).
- "Fix" intentional behavior because they don't know why it exists.

Linters and type systems catch some of this. They don't catch *intent*. Pillars is the layer between "what the code looks like" and "what an experienced engineer would tell a new contributor on day one."

## What Pillars is not

- Not a workflow tool. It produces no work; it surfaces context.
- Not a compliance document. Pillars are briefings, not rulebooks. The agent is trusted by default.
- Not tool-specific. Any agent that reads markdown and parses YAML can implement it.
- Not tooling. This repo defines the standard. Tooling (CLI, skills, IDE wrappers) lives separately, when it exists. See [the tooling philosophy](#standard-vs-tooling).

## How it works (one minute)

1. A project adopts Pillars by adding an `AGENTS.md` at the repo root and a folder of pillar files at `./agents/`.
2. Each pillar covers one domain (`data.md`, `auth.md`, `ui.md`, etc.) and follows an 8-section template with YAML frontmatter.
3. When an agent starts a task, it scans the frontmatter, picks the relevant pillars based on the task description, loads them, and follows their content.
4. Pillars come in tiers: 2 always-loaded, 11 Core, 11 Common, plus open-ended Domain pillars. Most projects use a focused subset. Excluded pillars are first-class.
5. Routing has a portable token-matching baseline. Sub-pillars use path-qualified identities, and nested scopes let monorepo packages refine root guidance.

Full spec: [SPEC.md](SPEC.md). Pillar catalog with tiers, boundaries, and sub-pillar patterns: [PILLARS.md](PILLARS.md). FAQ: [FAQ.md](FAQ.md). This project dogfoods itself; the [AGENTS.md](AGENTS.md) and [agents/](agents/) folder demonstrate the standard in use. For a compact end-to-end adoption example, see [examples/saas-dashboard/](examples/saas-dashboard/).

## Adopting Pillars

### For a new project

1. Copy [AGENTS.md](AGENTS.md) from this repo into your repo root.
2. Create an `agents/` folder and optionally copy [`agents/catalog.yaml`](agents/catalog.yaml) for offline silent-gap discovery.
3. Ask your coding agent to write stubs for the two always-loaded pillars (`context.md`, `repo.md`) and any Core pillars that apply. Reference [examples/](examples/) for shape.
4. Remove catalog entries when their pillar is created or explicitly excluded.
5. Fill sections as you make decisions. A pillar exists once it has frontmatter and a Scope statement; the rest fills in over time.

### For an existing project

1. Copy `AGENTS.md` into your repo root.
2. Add a local `agents/catalog.yaml` for concerns you want the agent to discover while they are absent. Without a catalog entry, an unknown concern produces no Pillars-specific claim.
3. Do not create every pillar upfront. A catalog match degrades gracefully: the agent infers from code, states the assumption, and recommends the relevant pillar.
4. As inferences hit edge cases, ask the agent to author that pillar and remove its catalog entry.

## Standard vs. tooling

The repo defines the **standard** at the root (the spec, template, catalog, protocol). It's portable: any agent in any tool can read it.

**Tooling** lives in [`tooling/`](tooling/). It automates the meta-operations (bootstrap, authoring, drift detection) but isn't required. The standard works in every major AI coding tool with zero tooling installed.

### Multi-tool support

Tooling ships in two forms, with broad coverage:

| Form | Tools | Where |
|---|---|---|
| Native skill bundle | Claude Code | [`tooling/claude-skill/`](tooling/claude-skill/) |
| Universal prompts + per-tool install guides | Cursor, Codex CLI, Gemini CLI, opencode, Aider, Windsurf, Cline, Continue, and any other AI tool | [`tooling/prompts/`](tooling/prompts/) |

The prompt form covers optional report-first workflows for bootstrap, authoring, verification, structural checks, task routing, gap indexing, trimming, and reconciliation with design, product, and README documents.

Pick your tool's install doc in [`tooling/prompts/`](tooling/prompts/) for one-paragraph setup instructions, or paste a prompt file directly into your tool's chat to run the operation.

The repository also ships an optional deterministic validator, unit tests, and task-to-load-set fixtures. They use local files only and are not required for compatibility.

### Versioning note

Pillars-compatible means compatible with the standard in [SPEC.md](SPEC.md): the `AGENTS.md` protocol, `agents/` layout, frontmatter schema, loading behavior, and missing-pillar behavior. Tooling changes do not change project compatibility unless `SPEC.md` changes.

Repository releases may include standard changes, tooling changes, or both. The changelog labels tooling-only releases as "Standard itself unchanged" so adopters know whether they need to update their project files.

### design.md interop

Pillars was inspired by the same pattern that made `design.md` useful: durable, agent-readable project intent in markdown. They fit together cleanly when `design.md` remains the rich design brief and Pillars becomes the task-routed operating memory.

Use root `design.md` for product intent, user journeys, UX rationale, and design narrative. Use `agents/*.md` for the durable facts, decisions, constraints, and gaps agents need while implementing specific tasks. The [`pillars-sync-design.md`](tooling/prompts/pillars-sync-design.md) prompt compares both directions and reports proposed updates without writing files.

## Repository layout

```
pillars/
├── README.md           # this file
├── SPEC.md             # the formal standard
├── PILLARS.md          # the pillar enumeration: tiers, boundaries, sub-pillar patterns
├── AGENTS.md           # this project's own AGENTS.md (dogfooded protocol)
├── FAQ.md              # adoption and usage questions
├── CONTRIBUTING.md     # how to contribute
├── CODE_OF_CONDUCT.md  # community standards
├── SECURITY.md         # security policy
├── CHANGELOG.md        # version history
├── LICENSE             # CC0 1.0 Universal
├── agents/             # this project's own pillar files (dogfooded)
│   ├── context.md
│   ├── repo.md
│   └── catalog.yaml    # optional offline absent-concern metadata
├── examples/           # worked example pillars for adopters
│   ├── data.md
│   ├── auth.md
│   ├── auth/           # sub-pillar worked example (agent-facing registration)
│   │   └── agent-registration.md
│   └── saas-dashboard/ # compact end-to-end adoption example
├── tooling/            # optional tooling and repository QA
│   ├── claude-skill/   # Claude Code native skill bundle
│   │   ├── pillars-init/
│   │   ├── pillars-author/
│   │   └── pillars-verify/
│   ├── ci/             # validator, pinned dependency, and unit tests
│   │   ├── validate_pillars.py
│   │   ├── check_consistency.py
│   │   ├── requirements.txt
│   │   └── tests/
│   ├── conformance/    # routing fixtures and benchmark protocol
│   └── prompts/        # Universal paste-in prompts + per-tool install guides
│       ├── pillars-check.md
│       ├── pillars-find-gaps.md
│       ├── pillars-init.md
│       ├── pillars-author.md
│       ├── pillars-map-task.md
│       ├── pillars-verify.md
│       ├── pillars-sync-prd.md
│       ├── pillars-sync-readme.md
│       ├── pillars-sync-design.md
│       ├── pillars-trim.md
│       └── install-{cursor,codex-cli,gemini-cli,opencode,aider,windsurf,cline,continue}.md
└── DESIGN-NOTES.md     # design conversation log
```

## Status

Stable 1.2.0. This backward-compatible release adds the decision-depth sub-pillar pattern on top of 1.1, which specified deterministic routing, path-qualified sub-pillar identities, offline absent discovery, nested scopes, content budgets, and expanded catalog boundaries. No schema or loading behavior changed. The conformance suite is repeatable and local. Hypothetical pressure tests are not presented as adopter evidence, and the optional live-model benchmark template remains unscored until a real run is published. See [CHANGELOG.md](CHANGELOG.md) for version history.

## Contributing

Pull requests and proposals are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for the contribution model (RFC-style for spec changes, direct PR for typos and examples).

## License

[CC0 1.0 Universal](LICENSE). Use Pillars freely, in any project, public or private, with or without attribution. The standard wins by being adopted.
