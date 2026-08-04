# Contributing to Pillars

Thank you for considering a contribution.

**You do not have to be an engineer to contribute here.** Pillars is a standard written in prose, and the most common failure mode for a standard is being confusing rather than being wrong. Clearer wording, a better example, or an honest "I read this three times and still did not get it" report is a real contribution, and often a more valuable one than a spec change.

The easiest ways in:

- Found a typo or an unclear sentence? Open a pull request directly, or an issue if you are not comfortable with pull requests.
- Something confused you during adoption? Open an issue with the question template and say what you expected. That is data we cannot get any other way.
- Wrote pillars for a project type not covered here? Share the exclusion list you ended up with.

Beyond that, Pillars is a standard rather than a code project, so its contribution model is closer to RFC-style than to typical open-source software. The rest of this document explains how to propose changes, what is welcome, and what to expect.

## What Pillars accepts

| Kind | Where | Process |
|---|---|---|
| Specification clarifications | `SPEC.md` | Open an issue first if the change is non-trivial; PR for typos and direct fixes |
| New pillars in the catalog | `PILLARS.md` | RFC-style issue first; PR after discussion |
| New worked examples | `examples/` | PR directly; reviewed for quality and accuracy |
| End-to-end adoption examples | `examples/<archetype>/` | PR directly; keep them compact and realistic |
| Tooling prompts | `tooling/prompts/` | PR directly for prompt-only workflows; keep them report-first unless writes are explicitly user-approved |
| Validator and conformance cases | `tooling/ci/`, `tooling/conformance/` | PR directly with unit tests and expected load sets |
| Boundary call refinements | `PILLARS.md` | Issue first to discuss the boundary; PR after agreement |
| Archetype exclusion lists | `PILLARS.md` | PR directly; new archetypes welcome |
| Sub-pillar patterns | `PILLARS.md` | Issue first to discuss; PR after |
| FAQ entries | `FAQ.md` | PR directly |
| Documentation improvements | Any `.md` | PR directly |

For changes to the standard's structure (the 8-section template, the frontmatter schema, the loading mechanism, the missing-pillar protocol), open an RFC issue and expect a longer discussion. Structural changes have ripple effects across every adopter.

## How to propose a change

### Small changes (typos, clarifications, examples)

1. Fork the repo.
2. Make your change on a branch.
3. Open a PR with a clear title and a short description of what changed and why.

### Larger changes (new pillars, boundary calls, structural)

1. Open an issue describing what you want to change and why. Use the `feature` template.
2. Wait for discussion. Maintainers (and other contributors) may push back, ask for examples, or propose alternatives.
3. Once there's rough consensus, send a PR that implements the discussed change.

### Spec-level changes (template, schema, protocol)

Pillars treats these as RFCs. You'll be asked to:

1. Describe the change.
2. Explain the problem it solves (a concrete failure mode in the current standard).
3. Pressure-test it against the existing project archetypes documented in `DESIGN-NOTES.md`.
4. Propose how existing adopters migrate.

Expect a multi-week conversation. The standard is intentionally small and slow-moving.

## Versioning

Pillars uses [Semantic Versioning](https://semver.org/):

- **Major** (`1.x.x` -> `2.x.x`): frontmatter schema or loading-mechanism changes that break existing pillars. Requires migration notes.
- **Minor** (`1.2.x` -> `1.3.x`): backward-compatible additions to schema, protocol, pillar catalog, or sub-pillar patterns.
- **Patch** (`1.2.2` -> `1.2.3`): clarifications, typo fixes, new examples, documentation.

The current version is in `CHANGELOG.md`.

Tooling-only releases may update prompts, skills, install guides, or examples without changing Pillars compatibility. When the standard itself is unchanged, say so clearly in `CHANGELOG.md`.

## Validation before a pull request

Install the pinned validator dependency and run the same checks as CI:

```bash
python3 -m pip install -r tooling/ci/requirements.txt
python3 -m unittest discover -s tooling/ci/tests -v
python3 tooling/ci/validate_pillars.py \
  . --recursive-scopes \
  --standalone examples \
  --fixtures tooling/conformance/fixtures.yaml
python3 tooling/ci/check_consistency.py
git diff --check
```

Spec changes that affect routing must add or update deterministic conformance cases. Validator behavior changes must include focused unit tests. Live-model benchmark results are optional, but claimed results must follow `tooling/conformance/BENCHMARK-PROTOCOL.md` and include raw artifacts.

## Style and tone

Pillars values *briefing tone*: conversational, declarative, reasoned, what an experienced engineer would tell a new contributor on day one. Spec and pillar text should not read like compliance documentation.

Concrete guidance:

- **Declarative over prescriptive.** Say what *is*; let the reader infer constraints.
- **Reason given.** When stating a rule or watchout, include the *why*. The reason is the load-bearing content.
- **Tight examples.** Inline, minimal, just enough to ground the rule.
- **No bullet-list theater.** If a list is fewer than three items, prose is usually better.

## Example quality bar

Worked example pillars must:

- Use the canonical 8-section template.
- Include a representative frontmatter block.
- Be a realistic, *not* a sanitized, set of facts. Show the messy real-world choices, not generic textbook conventions.
- Carry a header note: `> This is a worked example for adopters to reference. Replace this content with your project's actual conventions when adopting.`

End-to-end adoption examples must:

- Include an `AGENTS.md` and a small `agents/` folder.
- Show at least one always-loaded pillar and one task-routed pillar.
- Explain how a realistic task maps to a load set.
- Stay compact enough to read in one sitting.

## What we won't accept

- **Tool-specific extensions to the standard.** Pillars stays portable; if it only works in Claude Code or only in Cursor, it doesn't belong in the spec. Such features go in `tooling/<flavor>/` if it ever lands.
- **Verbose pillars.** A pillar that looks like a compliance audit report defeats the briefing philosophy. Trim.
- **Pillars without reasoning.** Rules and Watchouts without "why" are rejected.
- **New tiers.** The Always-loaded / Core / Common / Domain shape is fixed. Re-tiering individual pillars is open for discussion; adding a tier is not.

## Communication

- **Issues:** for bug reports (ambiguities in the spec, contradictions, broken examples), feature proposals (new pillars, new patterns), and questions.
- **Discussions:** for open-ended conversations that aren't actionable issues (planning the next minor version, exploring patterns).
- **PRs:** for proposed changes. Link to the issue if the change was discussed.

## License of contributions

By contributing to Pillars, you agree your contribution is released under [CC0 1.0 Universal](LICENSE) (public domain). No CLA is required; the dedication is in the license itself.

## Recognition

Contributors are credited in `CHANGELOG.md` for each release. No additional contributor file is maintained.

## Maintainer expectations

This is a small standard maintained by a small team. Expect:

- Issue responses within a week.
- PR reviews within two weeks for non-trivial changes; faster for typos.
- The maintainers reserve the right to close proposals that violate the standard's philosophy (briefings, not rulebooks; portable, not tool-specific). When that happens, you'll get a written explanation, not a silent close.

Thank you again. Standards live or die by the rigor of the people who shape them.
