# Changelog

All notable changes to the Pillars standard are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versions follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html):

- **Major** — frontmatter schema or loading-mechanism changes that break existing pillars.
- **Minor** — backward-compatible additions to schema, protocol, or pillar catalog.
- **Patch** — clarifications and corrections without behavior changes.

## [Unreleased]

Tooling, examples, documentation, and repository QA. The standard itself is unchanged, so Pillars compatibility is unaffected and projects on 1.2.2 need no edits.

### Added

- **Changelog history guard in `tooling/ci/check_consistency.py`:** released entries are append-only, but the repo-wide version substitution that repins install URLs each release will happily rewrite an already-published entry in place. The damage survives review because the result still looks like a well-formed changelog. The check now verifies that the newest entry matches the release version, that no version has two entries, that entries descend, and that every entry has a release-tag anchor pointing at its own tag. Caught during the 1.2.2 release, where a bulk `1.2.1 -> 1.2.2` substitution rewrote the published 1.2.1 entry.
- **`tooling/ci/tests/test_check_consistency.py`:** first unit coverage for the consistency checker, including a regression case that replays the bulk-substitution failure and a case asserting the repository's own changelog is intact.
- **Example routing fixtures:** three conformance cases pin the "Example Task Routing" table in `examples/saas-dashboard/README.md`. Two of its three rows did not hold under the portable matcher (see Fixed), and nothing caught it because the example was only structurally linted.
- **More consistency guards:** the AGENTS.md embedded in both `pillars-init` forms must equal the root `AGENTS.md` byte for byte; their Core stub `covers` and `triggers` must equal `agents/catalog.yaml`; every prompt and CI script must be listed in the tooling indexes; and the skill version table must match each `SKILL.md`. Each guard was written against drift this pass found.
- **Validator warning for empty sections:** `SPEC.md` asks for `(none)` in an empty section, and a heading with no text now produces a warning. It is a warning rather than an error so adopter CI does not break on upgrade.

### Changed

- **`pillars-init` skill (0.3.0 -> 0.4.0) and prompt:** both now carry the canonical `AGENTS.md` verbatim for offline use. The prompt's fallback had drifted (a non-recursive `./agents/*.md` glob that hid sub-pillars, no scope definition, and flattened compliance wording), and the skill had no fallback at all. Core stubs take `covers` and `triggers` from the starter catalog; the old trigger table added `design` to both `arch` and `ui`, so any task mentioning design routed to both, and stubs had no required `covers`. The prompt gains the skill's monorepo guidance, placed before its first command and with AGENTS.md written at the scope root, and a `no` in the stub matrix now correctly means "stays cataloged absent" rather than "already excluded".
- **`pillars-author` skill (0.2.0 -> 0.3.0) and prompt:** authoring now checks the scope's `excluded:` list first, and offers to remove a matching exclusion with approval, because a pillar and an exclusion with the same identity are invalid. Previously `pillars-verify` sent users to author an excluded pillar, and author forbade the one edit that would make the result valid. Also drops the skill's "more than 50% of sections populated" rule for `status: present`, which contradicted SPEC 3.4; the advice to expect more than three `must_read_with` entries on Domain pillars; and the claim that only `context` and `repo` may be always-loaded. The prompt's scan table gains the `analytics`, `i18n`, `a11y`, and `compliance` rows the skill already had.
- **`pillars-verify` skill (0.2.0 -> 0.2.1) and prompt:** points to the offline validator instead of a roadmap document that does not exist, and notes that `pillars-author` handles exclusion removal.
- **Install guides:** `install-aider.md` is rewritten around how Aider actually loads context. Aider does not read `AGENTS.md` or `CONVENTIONS.md` on its own, and it does not expand globs in `--read`, so the old `--read 'agents/*.md'` and `read: [agents/*.md]` forms named a file that does not exist; `--read agents` reads the directory recursively. Redirect files in the other guides use the recursive `./agents/**/*.md`, and command installs download prompts from tag-pinned URLs instead of copying from a `tooling/prompts/` checkout that adopters do not have.
- **`pillars-check`, `pillars-trim`, `pillars-find-gaps` prompts:** check separates selector uniqueness (normalized) from reference uniqueness (exact) and flags selectors with no portable tokens; trim warns when either aggregate budget is exceeded, not only both; trim and find-gaps discover nested scopes instead of listing only the root `agents/`.
- **`tooling/ci/validate_pillars.py`:** each finding is reported once. Conformance fixtures re-validate every scope they route through, so a single warning used to print once per fixture case that touched it.
- **`tooling/ci/check_consistency.py`:** the changelog date is no longer pinned separately from `VERSION`, since the history guard already checks the newest entry; local virtualenv and `node_modules` folders are skipped, matched only inside the repository so a checkout under a folder named `venv` is still scanned.
- **`LICENSE`:** now carries the full CC0 1.0 legal code. GitHub reported the short dedication as "Other"; the plain-language summary stays in the README.
- **`.github/workflows/validate.yml`:** checkout no longer persists credentials, and the job has a timeout.
- **Housekeeping:** `.gitignore` drops placeholder Node and reserved-tooling entries now that the only tooling language is Python; `DESIGN-NOTES.md` is titled as the historical log it is.

### Fixed

- **`examples/saas-dashboard/`:** the README said "Add `last_contacted_at` to accounts" routes to `data`, but no `data` trigger appears in that sentence; the row now says "column". It also said "Move account pages into a new route group" reports absent `ui`, but the matcher does not stem, so `pages` never matched `page`; the local catalog's `ui` entry now lists both forms, and `components` beside `component`. The owner role no longer claims billing, which the example excludes.
- **`examples/data.md`:** the column workflow generated a migration and then ran `db:push`, which bypasses it; it now runs `db:migrate`, matching the pillar's own watchout.
- **`agents/context.md` and `agents/repo.md`:** the load-set definition now includes always-loaded and `see_also` pillars, and the layout tree lists `tooling/conformance/`.
- **`tooling/README.md`:** the tree lists `check_consistency.py` and the conformance assets; the Aider row matches the corrected guide.
- **`tooling/conformance/RESULTS-TEMPLATE.md`:** adds the system prompt and task set the protocol says to pin, and per-grader plus adjudicated score rows the protocol requires.
- **Community files:** `CODE_OF_CONDUCT.md` no longer suggests a "private GitHub issue", which GitHub does not offer; `CONTRIBUTING.md` no longer points to Discussions, which are disabled; issue templates apply labels that exist (`bug`, `enhancement`, `question`); `FAQ.md` lists GitHub Copilot, which the README already named.

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
