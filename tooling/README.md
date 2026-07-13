# Pillars Tooling

Tooling forms that automate Pillars meta-operations across AI coding tools.

The **standard** itself ships separately as portable markdown ([SPEC.md](../SPEC.md), [PILLARS.md](../PILLARS.md), [AGENTS.md](../AGENTS.md)). It works in every major AI coding tool with **zero tooling installed**: the runtime alignment loop is just the tool reading `AGENTS.md` and following its protocol.

Tooling is optional. Use it when meta-operations like creating pillars, drafting from code, checking drift, mapping tasks, finding gaps, trimming bloat, or reconciling external docs get tedious to do by hand.

## What's here

```
tooling/
├── claude-skill/           # Native Claude Code skill bundle
│   ├── pillars-init/
│   ├── pillars-author/
│   └── pillars-verify/
├── ci/                     # Deterministic structural validator (this repo's CI)
│   ├── validate_pillars.py
│   ├── requirements.txt
│   └── tests/
├── conformance/            # Task routing fixtures and benchmark protocol
└── prompts/                # Universal paste-in prompts + per-tool install guides
    ├── pillars-check.md
    ├── pillars-find-gaps.md
    ├── pillars-init.md
    ├── pillars-author.md
    ├── pillars-map-task.md
    ├── pillars-verify.md
    ├── pillars-sync-design.md
    ├── pillars-sync-prd.md
    ├── pillars-sync-readme.md
    ├── pillars-trim.md
    ├── install-cursor.md
    ├── install-codex-cli.md
    ├── install-gemini-cli.md
    ├── install-opencode.md
    ├── install-aider.md
    ├── install-windsurf.md
    ├── install-cline.md
    └── install-continue.md
```

## Which form for which tool

| Tool | Recommended form | Notes |
|---|---|---|
| Claude Code | `claude-skill/` (native skill bundle) | Drop into `~/.claude/skills/`; invoke via `/pillars-init` etc. |
| Cursor | `prompts/install-cursor.md` | Rule file + optional commands; or paste-in |
| Codex CLI | `prompts/install-codex-cli.md` | Native AGENTS.md support; paste-in for meta-ops |
| Gemini CLI | `prompts/install-gemini-cli.md` | Native AGENTS.md or GEMINI.md redirect |
| opencode | `prompts/install-opencode.md` | Native AGENTS.md support; optional commands |
| Aider | `prompts/install-aider.md` | `--read AGENTS.md` flag or conventions file |
| Windsurf | `prompts/install-windsurf.md` | `.windsurfrules` redirect or native AGENTS.md |
| Cline | `prompts/install-cline.md` | `.clinerules` redirect or native AGENTS.md |
| Continue | `prompts/install-continue.md` | `systemMessage` + `slashCommands` config |
| Any other AI coding tool | `prompts/` (paste-in) | The prompts are tool-agnostic; works anywhere |

## Quick start (any tool)

1. Adopt the standard: copy `AGENTS.md` to your project root, create `agents/`, and optionally add `agents/catalog.yaml`.
2. Read the install doc for your tool.
3. Use the meta-operation prompts (or skill, in Claude Code) to bootstrap and maintain pillars.

## Prompt operations

The universal prompts implement these procedures:

| Operation | Job |
|---|---|
| **check** | Validate structure, identities, list fields, section order, floors, references, and budgets |
| **find-gaps** | Index unresolved `Gaps` across pillars and classify their impact |
| **init** | Bootstrap Pillars: detect archetype, drop AGENTS.md, scaffold `agents/`, write stubs, set exclusions |
| **author** | Draft a specific pillar from the codebase via targeted archaeology, present 8-section draft for approval |
| **map-task** | Explain which pillars load for a task and why |
| **verify** | Audit pillars against current code, flag drift with evidence, suggest fixes (no auto-fix) |
| **sync-design** | Reconcile root `design.md` with Pillars and report proposed updates in both directions |
| **sync-prd** | Reconcile PRDs or requirements docs with Pillars |
| **sync-readme** | Reconcile README with Pillars |
| **trim** | Report bloat, duplication, and over-prescription in pillars |

The Claude Code skill bundle currently packages the three higher-touch procedures: init, author, and verify. Smaller report-only workflows remain prompt-only. The deterministic validator covers machine-checkable structure and routing; it does not replace judgment-based drift verification.

## Deterministic validator and conformance suite

The local validator is an executable QA surface without being a required or published package. It checks:

- Frontmatter types, unique list items, identity and filename agreement, section order, floors, exclusions, self-references, fan-out, and content budgets.
- Path-qualified `must_read_with` and `see_also` references.
- Local absent catalogs and present, absent, or excluded conflicts.
- Deterministic trigger and `see_also` matching through task-to-load-set fixtures.
- Nested-scope inheritance, override, and exclusion behavior.

Run the same gates as CI:

```bash
python3 -m pip install -r tooling/ci/requirements.txt
python3 -m unittest discover -s tooling/ci/tests -v
python3 tooling/ci/validate_pillars.py \
  . --recursive-scopes \
  --standalone examples \
  --fixtures tooling/conformance/fixtures.yaml
python3 tooling/ci/check_consistency.py
```

The validator uses local files only. With `--recursive-scopes`, it discovers every nested scope that contains both `AGENTS.md` and `agents/`. The standard still works without Python, PyYAML, CI, or this implementation. For a report-only manual check, use `tooling/prompts/pillars-check.md`.

The conformance directory also includes an optional live-model benchmark protocol and an intentionally blank result template. No score is claimed until real runs and raw artifacts exist.

## Why no full per-tool wrappers

For most tools listed above, the universal prompts plus a thin install doc covers the integration. Building full per-tool wrappers (a Cursor command bundle, a Gemini commands TOML set, etc.) is multiplicative work that drifts as each tool's command format evolves.

Claude Code gets a full skill bundle because it has a stable native skill format and is the most common tooling target. Other tools get install docs that show how to use the universal prompts inside their existing command/rules surfaces.

When a particular tool develops a stable native command format and Pillars adoption signal warrants a tighter integration, a native bundle for that tool can ship as `tooling/<tool>/`. PRs welcome.

## License

[CC0 1.0 Universal](../LICENSE). Same as the standard. Use freely.
