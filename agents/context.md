---
pillar: context
status: present
always_load: true
covers: [project identity, domain language, product invariants, glossary]
triggers: []
must_read_with: []
see_also: [repo]
---

## Scope

This pillar describes what Pillars is, the domain language used throughout the standard, the product invariants that hold across all decisions, and a glossary of canonical terms. It does not cover technical conventions (those live in `repo.md`), the standard's authoring template (lives in `SPEC.md`), or the pillar enumeration (lives in `PILLARS.md`).

## Context

Pillars is an open standard for project-specific instructions that keep coding agents (Claude, Cursor, Copilot, Codex, Aider, others) aligned to a codebase's facts, decisions, and conventions. A project adopting Pillars publishes markdown files under `./agents/`, each conforming to the 8-section pillar template and opening with YAML frontmatter the agent uses to decide what to load. An `AGENTS.md` describes the loading protocol. An optional local `agents/catalog.yaml` makes absent concerns discoverable offline without becoming a router for present pillars.

The standard is tool-agnostic: any agent that can read markdown and parse YAML can implement Pillars. Pillars sits underneath the broader AGENTS.md convention rather than replacing it; tool-specific files (`CLAUDE.md`, `.cursorrules`, `copilot-instructions.md`) become thin shims pointing at AGENTS.md.

The repo also ships optional tooling forms for meta-operations around the standard: initializing Pillars in a project, authoring a pillar from code, verifying drift, and checking structural conformance. These live under `tooling/` and are not part of the runtime standard. They are distribution aids for humans and agents, not requirements for Pillars compatibility.

**Glossary:**

- **Pillar** — a single domain's briefing file (e.g., `data.md`, `auth.md`). Sits in `./agents/`.
- **Always-loaded pillar** — frontmatter has `always_load: true`. Read every session regardless of task. Currently `context` and `repo`.
- **Trigger** — keyword or phrase in frontmatter; the agent matches against the task description to decide relevance.
- **Identity:** path-derived reference for a pillar: `auth` for a top-level pillar or `auth/agent-registration` for a sub-pillar.
- **Local catalog:** optional `agents/catalog.yaml` metadata for concerns known to be absent in this project.
- **Scope:** a directory with both `AGENTS.md` and `agents/`; nested scopes inherit ancestor guidance and use nearest-scope precedence.
- **Touchpoint** — declared coupling between pillars. Hard (`must_read_with`) or soft (`see_also`).
- **Load set** — the full set of pillars loaded for a task: primaries plus their direct `must_read_with` (depth 1, no transitive following).
- **Stub** — pillar with `status: stub` and minimal body. Signals "concern acknowledged, rules undefined; ask, don't infer."
- **Excluded** — pillar name declared in AGENTS.md's `excluded:` list as not applicable to this project.

**Product invariants:**

- The standard is portable; no tool-specific extensions allowed.
- Pillars are briefings, not rulebooks. They surface what the agent can't infer from code.
- Loading is single-pass, depth 1. No chain walks during task execution.
- Missing pillars degrade gracefully via inference + assumption-stating. Adoption is incremental.
- The standard is small. The full SPEC.md is intended to be readable in a sitting.
- Tooling is optional. A project is Pillars-compatible when it follows the AGENTS.md plus `agents/` protocol, regardless of whether it uses helper prompts or skills.

## Decisions

- **Three tiers plus an always-loaded set, not a flat list.** Reason: handles the long tail of project types without bloating the required core. A flat list of 25+ mandatory pillars would prevent incremental adoption.
- **Frontmatter-driven present discovery, with a narrow local absent catalog.** Reason: present pillars stay decentralized, while silent gaps can be detected deterministically without network access or model memory.
- **8-section template combining briefing + prescriptive layers.** Reason: trust the agent by default (Context + Decisions) but allow hard constraints (Rules + Watchouts) when not inferable from facts.
- **Depth-1 loading, not transitive closure.** Reason: predictability for authors. Each pillar's frontmatter declares the exact load set.
- **Sub-pillars identified by path, not a parent frontmatter field.** Reason: visual hierarchy is self-documenting and path-qualified references remain unambiguous.
- **A portable token matcher is the minimum routing baseline.** Reason: implementations may add semantic recall, but representative tasks must still have a deterministic common result.
- **Nested scopes apply outer to inner with nearest-scope precedence.** Reason: monorepos need shared guidance and package-specific overrides without rewriting the root protocol.
- **Standard and tooling version independently.** Reason: the standard should stand alone, while prompts, skills, and other helper forms can evolve as adoption friction becomes clearer.

## Rules

(none) — context.md surfaces facts; constraint pillars sit elsewhere.

## Workflows

- **Adding a new top-level pillar to the standard:** decide tier, write frontmatter, write the 8 sections per "earn your keep" principle, update `PILLARS.md` enumeration, declare touchpoints from neighboring pillars where coupling is real.
- **Adding a sub-pillar to the standard:** create `./agents/<parent>/<name>.md`; use `<parent>/<name>` in references; document the pattern in `PILLARS.md` if it is new.
- **Recording an absent concern:** add it to the local `agents/catalog.yaml` with deterministic triggers. Remove the entry when the pillar is created or excluded.
- **Adding or changing tooling:** keep the standard untouched unless the spec itself changes. Update the relevant prompt or skill, document the form under `tooling/`, and explain whether the change affects standard conformance or only helper behavior.

## Watchouts

- **Don't write Rules content that would be inferred from Context.** Bloats pillars without value. Re-read the principle: prescriptive content only when not inferable.
- **Don't make pillars compliance documents.** Tone is "experienced engineer briefing a new contributor on day one," not "auditor's checklist."
- **Don't over-couple via `must_read_with`.** More than 3 entries signals a boundary smell; the pillar may be doing too much, or a shared dependency should graduate to `always_load: true`.

## Touchpoints

- `see_also: [repo]` — tasks that touch file layout in addition to project identity load `repo.md`.

## Gaps

- **Real adopter evidence** is still accumulating. The standard has hypothetical pressure tests and worked examples; public before/after adoption stories should be added as real projects use Pillars.
