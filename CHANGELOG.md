# Changelog

All notable changes to the Pillars standard are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versions follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html):

- **Major** — frontmatter schema or loading-mechanism changes that break existing pillars.
- **Minor** — backward-compatible additions to schema, protocol, or pillar catalog.
- **Patch** — clarifications and corrections without behavior changes.

## [Unreleased]

Repository QA only. No standard or tooling behavior changed, so nothing here affects Pillars compatibility.

### Added

- **Changelog history guard in `tooling/ci/check_consistency.py`:** released entries are append-only, but the repo-wide version substitution that repins install URLs each release will happily rewrite an already-published entry in place. The damage survives review because the result still looks like a well-formed changelog. The check now verifies that the newest entry matches the release version, that no version has two entries, that entries descend, and that every entry has a release-tag anchor pointing at its own tag. Caught during the 1.2.2 release, where a bulk `1.2.1 -> 1.2.2` substitution rewrote the published 1.2.1 entry.
- **`tooling/ci/tests/test_check_consistency.py`:** first unit coverage for the consistency checker, including a regression case that replays the bulk-substitution failure and a case asserting the repository's own changelog is intact.

## [1.2.2] - 2026-08-04

Documentation only. The standard itself is unchanged, and Pillars compatibility is unaffected. Projects on 1.2.1 need no edits.

### Changed

- **`README.md`:** rewritten for a general audience. The old opening described the mechanism ("a decomposed, frontmatter-driven convention") to readers who did not yet know what problem it solved. It now leads with the problem in plain language, frames pillars as the briefing you would give a new team member, and adds a before-and-after table, an audience table that names non-engineers explicitly, an annotated sample pillar, and a plain-language glossary. Installation now offers a paste-a-prompt path before the terminal path, since a reader who does not use `curl` was previously stopped at the first instruction.
- **`FAQ.md`:** reordered from newcomer questions to implementer questions. Adds the entries a first-time reader actually asks: what this is in one sentence, whether you need to be a programmer, what it costs, which tools work. Spec rationale moved into a "Design decisions, for the curious" section so it no longer sits between a reader and their adoption question. Every prior answer is preserved.
- **`PILLARS.md`:** retitled "The Pillar Catalog" and reframed as a menu rather than a checklist, since the tier tables read as 24 required files to a newcomer. Adds a four-step "how to use this page" and plain-language tier descriptions. Tables, boundary calls, and archetype exclusions are unchanged.
- **`SPEC.md`:** adds a "who this document is for" note pointing non-implementers at README, PILLARS, and FAQ. The normative text is deliberately untouched; softening the spec would cost implementers the precision they depend on.
- **`CONTRIBUTING.md`:** opens by stating that non-engineers can contribute and names three low-friction entry points. A standard fails by being confusing more often than by being wrong, so "this section confused me" reports are worth soliciting directly.
- **`tooling/ci/check_consistency.py`:** the FAQ staleness guard pinned the exact sentence `CLI tools commonly exclude 11 of them`, coupling a count check to one phrasing. It now matches `commonly exclude 11 of them`, keeping the guard on the number while leaving the wording free.
- **Adoption guidance:** install and reference URLs are repinned from `v1.2.1` to `v1.2.2`.

[1.2.2]: https://github.com/hannsxpeter/pillars/releases/tag/v1.2.2

## [1.2.1] - 2026-08-04

Tooling and documentation only. The standard itself is unchanged, and Pillars compatibility is unaffected. Projects on 1.2.0 need no edits.

### Changed

- **`pillars-init` skill (0.2.0 -> 0.3.0) and the matching `pillars-init.md` prompt:** Step 0 now detects an existing decision-record corpus (`docs/adr/`, `docs/decisions/`, `decisions/`, `adr/`) and instructs against migrating it, since flattening those files into a `Decisions` section discards the supersession history that made them worth keeping. Step 5 teaches the decision-depth sub-pillar as an escalation the user opts into, not something init scaffolds. Step 6 reports the corpus location when one is found. The skill keeps its `>=1.1.0` compatibility floor: sub-pillar identities have existed since 1.1, so 1.2 names the pattern without being required to use it.
- **`README.md`:** the status badge read "stable 1.1" through the whole 1.2.0 release. It now tracks the current minor.
- **Adoption guidance:** install and reference URLs are repinned from `v1.2.0` to `v1.2.1`.

[1.2.1]: https://github.com/hannsxpeter/pillars/releases/tag/v1.2.1

## [1.2.0] - 2026-08-03

Backward-compatible catalog release. No frontmatter schema, identity, or loading behavior changed; a 1.1 project conforms to 1.2 with no edits.

### Added

- **Decision-depth sub-pillar pattern:** `PILLARS.md` documents `arch/decisions` and `stack/decisions` as a recognized sub-pillar shape. Use it when rationale has enough volume or churn that a flat `Decisions` section stops being readable, or when superseded choices need to stay on the record with their original reasoning. The flat `Decisions` section remains the default; this is an escalation path, not a replacement.

### Changed

- **`FAQ.md`:** the per-pillar versioning answer now points at the decision-depth pattern for the case a flat `Decisions` section handles badly, namely reversed choices whose natural edit is deletion.
- **Adoption guidance:** install and reference URLs are repinned from `v1.1.0` to `v1.2.0` so adopters fetch the catalog that documents the new pattern.

[1.2.0]: https://github.com/hannsxpeter/pillars/releases/tag/v1.2.0

## [1.1.0] - 2026-07-13

Backward-compatible standard release focused on portable routing, incremental discovery, monorepos, and measurable conformance.

### Added

- **Path-derived identities:** top-level references remain unchanged, while sub-pillars use unambiguous references such as `auth/agent-registration`.
- **Portable minimum matcher:** primary triggers, absent discovery, and conditional `see_also` loading share deterministic ASCII token matching. Semantic matching remains an optional superset.
- **Offline absent discovery:** optional local `agents/catalog.yaml` files identify silent gaps without network access, global state, or model memory.
- **Nested scopes:** monorepos can combine root and package scopes with outer-to-inner inheritance, nearest-scope conflict precedence, and child exclusions.
- **Catalog guidance:** `development.md` and `release.md` join Core; `privacy.md` joins Common. Domain guidance now covers business rules, tenancy, billing, reliability, performance, infrastructure, and documentation with explicit boundary calls.
- **Context budgets:** recommended word and byte budgets for always-loaded and task-routed pillars, reported as warnings rather than compatibility errors.
- **Conformance assets:** six task-to-load-set fixtures, a local runner, 16 validator unit tests, recursive scope discovery, and CI coverage on current GitHub Actions majors.
- **Evaluation protocol:** a repeatable optional three-condition live-model procedure and an intentionally unpopulated result template. No benchmark score is claimed.

### Changed

- **Validator:** now checks identities, portable collisions, list item types and duplicates, hard and soft references, self-references, dependency fan-out, floors and exclusions, catalogs, budgets, nested scopes, and routing fixtures.
- **Adoption guidance:** install URLs are pinned to `v1.1.0` where practical, and prompts and skills teach catalog maintenance, deterministic matching, identities, and nested scopes.
- **Repository ownership:** release, issue, security, prompt, skill, and documentation URLs now use `hannsxpeter/pillars`.
- **Documentation:** README, SPEC, PILLARS, FAQ, AGENTS, examples, tooling docs, contribution guidance, and release surfaces now describe the same 1.1 behavior and catalog counts.

[1.1.0]: https://github.com/hannsxpeter/pillars/releases/tag/v1.1.0

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

[1.0.1]: https://github.com/hannsxpeter/pillars/releases/tag/v1.0.1

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

[1.0.0]: https://github.com/hannsxpeter/pillars/releases/tag/v1.0.0

## [0.1.3] - 2026-05-14

Standard itself unchanged.

### Added

- **`tooling/prompts/pillars-check.md`**: paste-in structural conformance check for frontmatter, required sections, floor pillars, references, and exclusions. This gives adopters a no-CLI validation path.
- **`examples/saas-dashboard/`**: compact end-to-end adoption example with `AGENTS.md`, always-loaded pillars, task-routed pillars, and example task loading behavior.

### Changed

- Dogfooded `agents/context.md` and `agents/repo.md` now reflect the current repository shape, including optional tooling.
- README, FAQ, and contributing docs now clarify that standard compatibility is defined by `SPEC.md`; tooling-only releases do not change compatibility.

[0.1.3]: https://github.com/hannsxpeter/pillars/releases/tag/v0.1.3

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

[0.1.2]: https://github.com/hannsxpeter/pillars/releases/tag/v0.1.2

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

[0.1.1]: https://github.com/hannsxpeter/pillars/releases/tag/v0.1.1

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

[0.1.0]: https://github.com/hannsxpeter/pillars/releases/tag/v0.1.0
