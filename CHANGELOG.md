# Changelog

All notable changes to the Pillars standard are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versions follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html):

- **Major** — frontmatter schema or loading-mechanism changes that break existing pillars.
- **Minor** — backward-compatible additions to schema, protocol, or pillar catalog.
- **Patch** — clarifications and corrections without behavior changes.

## [Unreleased]

No unreleased changes.

## [1.0.1] - 2026-05-30

Documentation and tooling consistency pass. Standard behavior is unchanged; the SPEC.md change is a clarification only.

### Added

- **`tooling/ci/validate_pillars.py`** and **`.github/workflows/validate.yml`**: a deterministic, dependency-light structural validator for Pillars projects, wired into this repository's CI. It checks frontmatter schema, the eight-section heading order, `pillar`/filename agreement, the always-loaded floor pillars, and `must_read_with` reference resolution, and it structurally lints the standalone worked examples under `examples/`. This is repository-internal QA, not a published CLI; the standard stays usable with zero tooling.
- **`examples/auth/agent-registration.md`**: a worked sub-pillar example showing how a project documents agent-facing self-registration (for example, the WorkOS `auth.md` agent-registration protocol) for its coding agent. Demonstrates the sub-pillar folder convention.
- **`FAQ.md`**: a new entry disambiguating Pillars' `auth.md` context pillar from WorkOS's runtime `auth.md` agent-registration protocol (same filename, different layer).

### Changed

- **`SPEC.md`**: added section 4.3 clarifying that trigger matching is implementation-defined, and what that means for cross-tool portability. Clarification only; no schema or loading-behavior change.
- **`FAQ.md`**: corrected the CLI exclusion count to 10 (matching the catalog and the init skill); it previously read 13.
- **`CONTRIBUTING.md`**: refreshed the semantic-versioning examples to post-1.0 values and removed a stale pre-1.0 conditional from the Discussions note.
- **`tooling/prompts/install-cursor.md`, `install-codex-cli.md`, `install-windsurf.md`**: removed stale `v0.1` version qualifiers.
- **`examples/saas-dashboard/README.md`**: removed `design.md` from the file tree (it is illustrative and not shipped in the example); the relationship is still covered under "Where design.md Fits."
- **`AGENTS.md`**: reworded the excluded-pillars note so the empty default reads cleanly in its dual role as the adopter template.
- **`agents/repo.md`** and **`tooling/README.md`**: documented the new `tooling/ci/` directory.
- **`DESIGN-NOTES.md`**: genericized a committed local filesystem path.
- **`PILLARS.md`**: completed the archetype starter exclusion table with SaaS dashboard and greenfield rows (both default to no exclusions).
- **`tooling/claude-skill/pillars-init/SKILL.md`** and **`tooling/prompts/pillars-init.md`**: aligned the archetype exclusion tables and matrix header to `PILLARS.md`.
- **`agents/repo.md`**: noted CI workflows in the `.github/` description.
- **`README.md`** and **`FAQ.md`**: updated CLI/CI roadmap language to reflect the shipped internal validator.
- **`.github/ISSUE_TEMPLATE/bug.yml`**: fixed a stale `SPEC.md` section reference (4.0 to 4).

[1.0.1]: https://github.com/aihxp/pillars/releases/tag/v1.0.1

## [1.0.0] - 2026-05-14

Stable standard release. No breaking schema or loading-protocol changes from 0.1.x.

### Added

- **`tooling/prompts/pillars-sync-design.md`**: paste-in reconciliation report for projects that use both root `design.md` and Pillars. It reports `design.md -> pillars`, `pillars -> design.md`, and conflict findings without writing files.
- **`tooling/prompts/pillars-sync-prd.md`**: paste-in reconciliation report for product requirements documents and Pillars.
- **`tooling/prompts/pillars-map-task.md`**: paste-in report that maps a task to its Pillars load set and explains why each pillar loads.
- **`tooling/prompts/pillars-find-gaps.md`**: paste-in project-level index of unresolved `Gaps` across pillars.
- **`tooling/prompts/pillars-trim.md`**: paste-in report for bloat, duplication, and over-prescription in pillars.
- **`tooling/prompts/pillars-sync-readme.md`**: paste-in reconciliation report for README and Pillars.

### Changed

- Promoted the Pillars specification to 1.0.0 to mark the AGENTS.md protocol, `agents/` layout, frontmatter schema, depth-1 loading behavior, and missing-pillar protocol as stable.
- README and FAQ now describe Pillars as stable 1.0.0 instead of pre-1.0.
- README, FAQ, tooling docs, install guides, and the SaaS example now document the expanded report-only prompt set.

[1.0.0]: https://github.com/aihxp/pillars/releases/tag/v1.0.0

## [0.1.3] - 2026-05-14

Standard itself unchanged.

### Added

- **`tooling/prompts/pillars-check.md`**: paste-in structural conformance check for frontmatter, required sections, floor pillars, references, and exclusions. This gives adopters a no-CLI validation path.
- **`examples/saas-dashboard/`**: compact end-to-end adoption example with `AGENTS.md`, always-loaded pillars, task-routed pillars, and example task loading behavior.

### Changed

- Dogfooded `agents/context.md` and `agents/repo.md` now reflect the current repository shape, including optional tooling.
- README, FAQ, and contributing docs now clarify that standard compatibility is defined by `SPEC.md`; tooling-only releases do not change compatibility.

[0.1.3]: https://github.com/aihxp/pillars/releases/tag/v0.1.3

## [0.1.2] - 2026-05-13

Multi-tool tooling support. Standard itself unchanged.

### Added

- **`tooling/prompts/`** — universal paste-in prompts that drive the same three operations as the Claude Code skill, but work in any AI coding tool:
  - `pillars-init.md` — tool-agnostic version of the init procedure.
  - `pillars-author.md` — tool-agnostic version of the author procedure. Pillar name supplied at the bottom of the prompt.
  - `pillars-verify.md` — tool-agnostic version of the verify procedure.
- **Per-tool install guides** under `tooling/prompts/install-*.md` for: Cursor, Codex CLI, Gemini CLI, opencode, Aider, Windsurf, Cline, Continue. Each covers runtime alignment (how the tool reads AGENTS.md) and meta-operation invocation (native commands where supported, paste-in where not).
- **`tooling/README.md`** — umbrella intro to all tooling forms with a tool-to-form matrix.
- **`tooling/prompts/README.md`** — how to use the universal prompts.
- README updated to highlight multi-tool support.

### Notes

- Universal prompts and the Claude Code skill drive the same three procedures. Both forms should be updated together when procedures change.
- For tools beyond the eight with install docs (e.g., Pieces, Pi Coder, future tools), the universal prompts work via paste-in. No per-tool wrapper is required for the operations to function.
- CLI still deliberately not included. Roadmap item for v0.2+ when CI demand surfaces.

[0.1.2]: https://github.com/aihxp/pillars/releases/tag/v0.1.2

## [0.1.1] - 2026-05-13

First tooling form ships. Standard itself unchanged.

### Added

- **`tooling/claude-skill/`** — Claude Code skill bundle with three skills:
  - `pillars-init` — bootstrap Pillars in a project. Detects archetype (CLI / SaaS / ML / marketing / mobile / OSS lib / greenfield), drops AGENTS.md, scaffolds `./agents/`, writes stubs, sets archetype-appropriate exclusions with reasons.
  - `pillars-author` — draft a specific pillar from the codebase. Scans relevant code, presents 8-section draft for user approval before writing.
  - `pillars-verify` — audit existing pillars against the current codebase. Walks Context-section claims, flags drift with evidence, suggests fixes. Does not auto-fix.
- **`tooling/claude-skill/README.md`** — install and usage instructions for the skill bundle.
- README updated to reference the tooling directory and explain the standard-vs-tooling split.

### Notes

- Tooling is optional; the standard works unmodified in every major AI coding tool without it.
- CLI form is deliberately not included; deferred until clear demand for CI/scripted use.
- Other tooling forms (Cursor commands, Codex prompts, neutral CLI) may follow when adoption signal warrants.

[0.1.1]: https://github.com/aihxp/pillars/releases/tag/v0.1.1

## [0.1.0] - 2026-05-13

Initial release. Foundations of the Pillars standard.

### Added

- **Specification** (`SPEC.md`): formal definition of the standard, including:
  - Repository layout (`AGENTS.md` at root, `./agents/` directory).
  - 8-section pillar body template (Scope, Context, Decisions, Rules, Workflows, Watchouts, Touchpoints, Gaps).
  - YAML frontmatter schema (`pillar`, `status`, `always_load`, `covers`, `triggers`, `must_read_with`, `see_also`).
  - 6-step loading protocol (depth-1, no transitive closure).
  - Four-state missing-pillar protocol (Present / Stub / Excluded / Absent).
  - Maturity gradient (stub -> partially populated -> fully populated).
- **Pillar enumeration** (`PILLARS.md`): tiered catalog including:
  - 2 always-loaded pillars (`context`, `repo`).
  - 9 Core pillars (`stack`, `arch`, `data`, `api`, `ui`, `auth`, `quality`, `deploy`, `observe`).
  - 10 Common pillars (`config`, `security`, `compliance`, `i18n`, `a11y`, `analytics`, `integrations`, `async`, `cache`, `notifications`).
  - Open-ended Domain tier with worked examples.
  - Boundary call tiebreakers between commonly-confused pillars.
  - Sub-pillar conventions and patterns.
  - Archetype starter exclusion lists (CLI, internal API, ML pipeline, marketing site, mobile app, open-source library).
- **Reference AGENTS.md**: ~50-line protocol description, dogfooded.
- **Dogfooded pillars** (`agents/`):
  - `agents/context.md` — Pillars project identity, domain language, glossary.
  - `agents/repo.md` — Pillars repository layout and naming conventions.
- **Worked examples for adopters** (`examples/`):
  - `examples/data.md` — typical Drizzle + Postgres data pillar.
  - `examples/auth.md` — typical Better-Auth + multi-tenant auth pillar.
- **Design notes** (`DESIGN-NOTES.md`): the full design conversation that produced v0.1, preserved for context.
- **Project documents**: `README.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `FAQ.md`, `LICENSE`.

### Validated

- Standard structure pressure-tested against six hypothetical project archetypes (SaaS dashboard, CLI tool, ML pipeline, marketing site, real-time collaborative app, e-commerce platform). All friction surfaced was guidance-level, not structural.

[0.1.0]: https://github.com/aihxp/pillars/releases/tag/v0.1.0
