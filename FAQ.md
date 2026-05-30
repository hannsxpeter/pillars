# FAQ

Common questions about Pillars. Organized roughly by audience and frequency.

## What Pillars is

### Why does this exist when `AGENTS.md` already does?

`AGENTS.md` is one file. It works fine for small projects. As a project grows, that one file either bloats (and the agent loads everything every session) or stays thin (and most project knowledge lives in someone's head). Pillars decomposes that one file into a structured set of pillars, each covering one domain, with a loading mechanism so the agent reads only what's relevant to the current task.

`AGENTS.md` is the entry point in Pillars. The standard sits *under* the AGENTS.md convention rather than replacing it.

### How is this different from Cursor rules, `.windsurfrules`, etc.?

Those are tool-specific. They work in one tool and one tool only. Pillars is portable: any agent that reads markdown and parses YAML can implement it. Adopters get one canonical source of truth that survives across Cursor, Claude Code, Codex, Gemini, Aider, and whatever ships next.

### Does this require my AI tool to support it?

The runtime loop requires the tool to read `AGENTS.md` at the project root. Every major AI coding tool (Claude Code, Codex CLI, Cursor, Gemini CLI, opencode, Aider) already does this, either natively or via a one-line shim file pointing at AGENTS.md.

If your tool doesn't read project-level instructions at all, no, Pillars doesn't help you. That's increasingly rare.

### Is this Anthropic-specific?

No. The standard mentions Claude and Claude Code as examples because that's a common adoption path, but Pillars is tool-agnostic by design and accepts no tool-specific extensions.

### Is Pillars' `auth.md` the same as WorkOS's `auth.md`?

No. They share a filename and nothing else. Pillars' `auth.md` is a dev-time **context pillar** at `agents/auth.md` that briefs a *coding* agent on your project's identity and access design. WorkOS's [`auth.md`](https://github.com/workos/auth.md) is a runtime **agent-registration protocol**: a file a live service hosts at `https://yourservice.com/auth.md` so an *autonomous action agent* can sign up for that service on a user's behalf. Different layer, different audience, different lifecycle, and they coexist fine in one project because they live at different paths. If your project adopts agent-facing registration, document it for your coding agent like any other integration: in your `auth.md` pillar, or a focused sub-pillar such as `agents/auth/agent-registration.md`. See [examples/auth/agent-registration.md](examples/auth/agent-registration.md) for a worked example.

## How it works

### Do I have to use all 21 pillars?

No. The standard defines a tiered set so you reason about each topic, but you populate only what applies. CLI tools commonly exclude 10 of them; that's first-class supported via `excluded:` in `AGENTS.md`. See [PILLARS.md](PILLARS.md) for archetype-specific starter exclusion lists.

### Can I use only some pillars and not others?

Yes. The 4-state missing-pillar protocol handles incomplete adoption gracefully: present pillars are loaded, stubs prompt the agent to ask, excluded pillars are treated as not applicable, absent pillars degrade to inference with explicit assumption-stating.

### How does this work for a monorepo?

The 1.0.0 standard is single-repo. For monorepos, the simplest pattern is one set of pillars at the monorepo root, with sub-pillars or domain pillars distinguishing per-app concerns (e.g., `agents/data.md` covers shared schema; `agents/data/orders.md` covers an orders-app-specific table). A more elaborate per-app `AGENTS.md` is possible but not part of the standard yet. Cross-package conventions are a future minor-version topic.

### Can pillars cover non-code concerns (legal, compliance, business rules)?

Yes, when relevant. `compliance.md` (Tier 2) is exactly this. `inventory.md` (Domain) often crosses into business rules. The rule of thumb: if a coding agent needs the information to do its job correctly, it belongs in a pillar.

### What happens if two pillars contradict?

That's a sign of a real contradiction in the project, not a Pillars problem. Resolve by deciding which pillar is authoritative, updating the other to defer, or reconsidering the boundary between them.

## Adoption

### How long does adoption take for a new project?

Five minutes for the install (copy `AGENTS.md`, create `agents/`, write two stubs). The pillars themselves accumulate over the project's lifetime as decisions get made. There's no upfront "fill in every pillar" requirement.

### How long for an existing project?

Five minutes for the install. The agent degrades gracefully on absent pillars (it infers from code and states the assumption), so you can adopt without authoring any pillars upfront. Pillars get authored from the agent's inferences over time.

### Do I need a CLI?

No, not for the runtime alignment loop (the daily use). The standard ships as markdown; every supporting AI tool reads it natively.

A published CLI would help with one-command bootstrap from a clean terminal and as the engine for per-tool skills. For deterministic structure checks, the repo ships a small internal validator ([`tooling/ci/validate_pillars.py`](tooling/ci/validate_pillars.py)) used in its own CI, which adopters can run too. None of this is required to adopt the standard. See [README.md](README.md) for the phased rollout philosophy.

### How do I check structure without a CLI?

Use [`tooling/prompts/pillars-check.md`](tooling/prompts/pillars-check.md). Paste it into your AI coding tool and it will check frontmatter, required headings, floor pillars, references, and exclusions. It does not install anything and it does not audit whether pillar claims match code; use `pillars-verify.md` for drift.

### What report-only maintenance prompts exist?

The prompt set includes small workflows that inspect and report without writing files:

| Prompt | Job |
|---|---|
| `pillars-map-task.md` | Show which pillars should load for a task and why |
| `pillars-find-gaps.md` | Index unresolved `Gaps` across pillars |
| `pillars-trim.md` | Flag bloat, duplication, and over-prescription |
| `pillars-sync-design.md` | Reconcile root `design.md` with Pillars |
| `pillars-sync-prd.md` | Reconcile PRDs or requirements docs with Pillars |
| `pillars-sync-readme.md` | Reconcile README with Pillars |

### How does Pillars work with design.md?

Use `design.md` as the rich design brief and Pillars as task-routed operating memory. Root `design.md` is best for product intent, user journeys, UX rationale, and design narrative. Pillars are best for durable facts, constraints, decisions, workflows, watchouts, and gaps that agents need during implementation.

Do not auto-sync them silently. Use [`tooling/prompts/pillars-sync-design.md`](tooling/prompts/pillars-sync-design.md) to produce a reconciliation report. It identifies `design.md -> pillars` updates, `pillars -> design.md` updates, and conflicts that need a human decision.

### Do tooling updates change compatibility?

Only changes to [SPEC.md](SPEC.md) change what it means to be Pillars-compatible. Prompt, skill, install-guide, and example updates can improve adoption without changing the standard. `CHANGELOG.md` labels tooling-only releases as "Standard itself unchanged."

### Can I adopt incrementally?

Yes. Start with the two always-loaded pillars (`context.md`, `repo.md`). Add Tier 1 pillars as the corresponding decisions get made. Add Tier 2 and Domain pillars when they're load-bearing for your project. Stubs and exclusions are first-class.

## Spec details

### Why depth-1 loading, not transitive closure?

Predictability. Reading a pillar's frontmatter tells you exactly what loads alongside it. Transitive closure hides coupling depth from authors and creates "this loads everything" surprises. Frequently-needed pillars graduate to `always_load: true` instead of being hidden transitive dependencies.

### Why 8 sections in the template?

It's the smallest set that covers both *briefing* (Scope, Context, Decisions) and *prescription* (Rules, Workflows, Watchouts) without forcing one shape onto everything. Sections 3-6 are optional per the "earn your keep" principle: include them only when they aren't inferable from Context.

### Why folder-based sub-pillars instead of a `parent:` frontmatter field?

Visual hierarchy is self-documenting. `./agents/data/migrations.md` is obviously a sub-pillar of `data`. Frontmatter would require opening the file to learn the same fact. Hugo, Jekyll, Astro, MkDocs, and every static site generator use folders for hierarchy; the pattern is conventional.

### Why is tooling optional?

Standards succeed by being portable and small. Tooling is a force multiplier, not a substitute. Pillars 1.0.0 defines compatibility through markdown files and loading behavior, so adoption is not gated on which tooling form you use. Optional tooling lives under `tooling/` when the friction it relieves is well-understood.

### Can I version pillars within a project?

The standard doesn't define per-pillar versioning. The project's git history is the version log. If a pillar undergoes a major rewrite, note it in the `Decisions` section of the pillar itself.

## Philosophy

### Why "briefings, not rulebooks"?

Coding agents are capable. Over-constraining them (long rules lists, banned patterns, compliance-style prose) removes their judgment and produces brittle outputs. Pillars surfaces what the agent *can't infer from code* (project identity, decisions, lessons learned) and trusts the agent to apply that knowledge well. Rules and Watchouts exist for the residual: things the agent can't derive from Context alone.

### What's the "earn your keep" principle?

Each section in a pillar is populated only when it adds value the others don't. If Context already implies a Rule, don't restate the Rule. If a Workflow is obvious from Context, skip it. Empty sections are marked `(none)`. Pillars stay tight; the agent gets clean signal.

### Won't this rot like every documentation system?

Possibly, if no one ever updates pillars. The structural difference: pillars are read by the agent on every session, so they have built-in usage pressure. Stale pillars produce visibly wrong agent behavior (the agent suggests Drizzle when the project uses Prisma), which prompts a fix. Tooling (drift detection in CI) reduces rot further. Pure documentation rots silently; pillars rot loudly.

## Process

### How do I propose a new pillar?

Open an issue using the `feature` template. Describe the project type that needs it, the gap the new pillar fills, and how it relates to existing pillars (boundaries, touchpoints). Discussion happens in the issue. See [CONTRIBUTING.md](CONTRIBUTING.md).

### How often is the spec updated?

Slowly. Major versions are years apart by design. Minor versions are quarterly or as needed for additive changes. Patch versions are continuous.

### Is this stable enough to adopt?

Yes. Pillars 1.0.0 marks the AGENTS.md protocol, `agents/` layout, frontmatter schema, loading behavior, and missing-pillar behavior as stable. The catalog and guidance can still refine through backward-compatible minor releases as real adoption surfaces edge cases.

### How do I report a problem?

Open an issue. Bug template for spec ambiguities or contradictions. Question template for clarification requests. Feature template for proposals.
