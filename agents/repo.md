---
pillar: repo
status: present
always_load: true
covers: [file layout, naming conventions, where things go, repository structure]
triggers: []
must_read_with: []
see_also: [context]
---

## Scope

This pillar covers the file and folder layout of the Pillars repository: where each document lives, what naming convention each file follows, and how the directory structure reflects the standard's own conventions. It does not cover the structure of pillar *content* (that's `SPEC.md`) or the catalog of pillars themselves (that's `PILLARS.md`).

## Context

Pillars is a documentation repository, not an application codebase. Its layout is intentionally flat at the root with three visible structural directories:

```
pillars/
├── README.md           # human-first intro and adoption guide
├── SPEC.md             # the formal standard
├── PILLARS.md          # the pillar enumeration with tiers and boundaries
├── AGENTS.md           # this project's own AGENTS.md, dogfooded protocol
├── FAQ.md              # adoption and usage questions
├── CONTRIBUTING.md     # contribution process
├── CODE_OF_CONDUCT.md  # community standards
├── SECURITY.md         # security policy
├── CHANGELOG.md        # standard and tooling release notes
├── LICENSE             # CC0 1.0 dedication
├── DESIGN-NOTES.md     # design conversation log
├── agents/             # this project's pillars, dogfooded
│   ├── context.md      # always-loaded
│   ├── repo.md         # always-loaded
│   └── catalog.yaml    # offline metadata for locally absent concerns
├── examples/           # adopter-facing examples
│   ├── data.md
│   ├── auth.md
│   ├── auth/           # sub-pillar worked example (agent-facing registration)
│   │   └── agent-registration.md
│   └── saas-dashboard/ # compact end-to-end adoption example
└── tooling/            # optional prompts, skills, validator, tests, and conformance assets
    ├── prompts/        # paste-in prompts and per-tool install guides
    ├── claude-skill/   # Claude Code skill bundle
    ├── ci/             # offline validator, consistency checker, unit tests
    └── conformance/    # routing fixtures, fixture project, benchmark protocol
```

**Naming:**

- Top-level docs use SCREAMING-CASE (`README.md`, `SPEC.md`, `PILLARS.md`, `AGENTS.md`, `LICENSE`, `DESIGN-NOTES.md`). Convention for repo-level documents.
- Pillar files use lowercase single-word names (`context.md`, `data.md`, `auth.md`). Matches the `pillar:` field in frontmatter.
- Sub-pillars live in a folder named for the parent (`agents/<parent>/<name>.md`).
- Sub-pillar references use their path-derived identity (`<parent>/<name>`). The frontmatter `pillar` value remains the leaf filename.

**Anchor files:**

- `README.md` is for humans landing on the repo.
- `SPEC.md` is the canonical standard.
- `PILLARS.md` is the catalog.
- `AGENTS.md` is the loader, dogfooded.
- `agents/` holds the project's own pillars (dogfooded).
- `examples/` holds worked example pillars and compact adoption examples for adopters to reference.
- `tooling/` holds optional helper forms and repository QA. It packages prompts, skills, the deterministic validator, unit tests, conformance fixtures, and benchmark protocol assets.
- `.github/` holds repository hosting metadata such as issue templates, PR templates, and CI workflows (for example, `workflows/validate.yml`, which runs the structural validator). It is not part of the Pillars standard.

## Decisions

- **Flat root layout with three visible structural directories.** Reason: keeps top-level scannable. Anyone landing on the repo sees the documents that define the standard (README, SPEC, PILLARS, AGENTS) immediately, while examples and optional tooling stay grouped.
- **`agents/` for dogfooded pillars; `examples/` for adopter references.** Reason: separates "this project's own pillars" from "pillars an adopter might want to copy." Keeps dogfooding honest while still providing reference material.
- **`tooling/` for optional helper forms.** Reason: prompts and skills make meta-operations easier, but the standard must remain usable without installing anything.
- **SCREAMING-CASE at root, lowercase under `agents/` and `examples/`.** Reason: matches conventional repo expectations (README, LICENSE in caps) while keeping pillar filenames machine-friendly (lowercase matches `pillar:` field).
- **Executable QA stays under `tooling/`.** Reason: validator tests and conformance assets support the standard but do not turn optional tooling into a runtime requirement.

## Rules

- **Pillar filename must match the `pillar:` frontmatter field.** Loading is path-based; mismatch breaks discovery.
- **Sub-pillars must live in `agents/<parent>/<name>.md`.** No `parent:` field in frontmatter; the path is the source of truth.
- **`agents/catalog.yaml` records only absent concerns.** Present pillar metadata stays in frontmatter; exclusions stay in `AGENTS.md`.
- **`agents/`, `examples/`, and `tooling/` are the only visible structural directories.** Don't introduce new top-level folders without updating this pillar. Hidden repository metadata such as `.github/` is allowed when it supports project hosting.

## Workflows

- **Adding a new top-level document:** decide if it belongs at root (canonical reference) or under `agents/` (dogfooded pillar) or `examples/` (adopter reference). Use SCREAMING-CASE at root; lowercase elsewhere. Link from `README.md` if it's a canonical reference.
- **Adding a new dogfooded pillar:** create `agents/<name>.md` with frontmatter and 8-section body. Update `PILLARS.md` if it's a new pillar in the standard's catalog. Cross-link from `README.md` if it changes the high-level shape.
- **Adding a new sub-pillar:** create `agents/<parent>/<name>.md`. The parent pillar may already exist or be created at the same time.
- **Adding a new tooling form:** place it under `tooling/<form>/` or `tooling/prompts/`, document it in `tooling/README.md`, and keep the standard documents clear that tooling is optional.

## Watchouts

- **Don't put adopter-facing pillars in `agents/`.** That directory is for this project's *own* pillars, dogfooded. Adopter references live in `examples/`. Mixing them confuses readers.
- **Don't rename SCREAMING-CASE docs casually.** Tools, search results, and external links assume conventional names (`README.md`, `LICENSE`).
- **Don't fragment with deep nesting.** Sub-pillars use one level of nesting (`agents/<parent>/<name>.md`). Deeper nesting was considered and rejected; if a domain needs more depth, it's a sign the parent boundary is wrong.

## Touchpoints

- `see_also: [context]`: repo layout and project identity are tightly related; readers often need both.

## Gaps

(none)
