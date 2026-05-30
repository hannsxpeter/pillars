# Pillars

## Project
- **Name:** Pillars
- **Target folder:** `pillars/`
- **Status:** designing the standard in plan mode; folder scaffolding deferred until ExitPlanMode.

### Proposed folder structure (executed on ExitPlanMode)
```
pillars/
├── README.md            # what Pillars is, why, how to adopt
├── SPEC.md              # the formal standard: template, frontmatter, loading, missing-pillar protocol
├── PILLARS.md           # the pillar enumeration: tiers, names, scopes, boundary calls
├── AGENTS.md            # the project's own AGENTS.md (dogfooded protocol description)
├── agents/              # the project's own pillar files (dogfooded)
│   ├── context.md
│   └── repo.md
├── examples/            # additional worked example pillars for adopters
│   ├── data.md
│   └── auth.md
└── DESIGN-NOTES.md      # this plan file, preserved as the design conversation log
```

The repo dogfoods itself: Pillars's own AGENTS.md and `agents/` directory demonstrate the standard in use. `examples/` provides reference pillars for adopters.

## Context
The user is designing a standalone product: an open standard for project-specific instructions that keep coding agents (Claude, Cursor, Copilot, Codex, etc.) aligned to a codebase's rules, conventions, and decisions. Inspired by `design.md` from google-labs-code, but decomposed into a tiered set of pillar files with an AGENTS.md-style loader that routes the agent to the right pillar before any work begins.

Targets both new projects (pillars filled in progressively as decisions are made) and existing projects (pillars generated from the code as it stands).

This product is independent of ready-suite. ready-suite was only a reference during ideation and is not a dependency.

## Scope of This Plan
Only **Layer 1: The Standard** is in scope.

In scope:
- The spec: what each pillar file must contain (template).
- The loading mechanism: how a coding agent navigates from AGENTS.md to the relevant pillars.
- The pillar list: which topics get their own file, across three tiers, plus the always-loaded set.
- The missing-pillar protocol: how the standard handles graceful degradation on incomplete adoption.

Out of scope (separate future product):
- The toolkit: commands to bootstrap pillars, generate from code, detect drift, refresh.

## Decisions Locked
- **Project name:** Pillars. Folder: `pillars/`.
- Standalone product, no dependency on ready-suite.
- Layer 1 (the spec) only for now; Layer 2 (toolkit) is a later product.
- Audience: both new and existing projects.
- Every pillar shares the 8-section body template and the YAML frontmatter schema (below).
- Entry point is an `AGENTS.md`-style file; standard composes with the broader AGENTS.md convention by sitting underneath it (AGENTS.md points at the pillar directory and describes the protocol).
- **Loading strategy:** frontmatter-driven discovery. Primaries + direct `must_read_with` (depth 1). No transitive following. Frequently-needed pillars graduate to `always_load: true`.
- Pillar architecture: two always-loaded pillars + three tiers (Core / Common / Specialized) + optional sub-pillars.
- **Sub-pillar discovery:** folder-based. Sub-pillars live in `./agents/<parent>/<name>.md`. No `parent:` field in frontmatter.
- Missing pillars handled via four-state protocol (Present / Stub / Excluded / Absent).
- **License:** CC0 1.0 (Universal Public Domain Dedication). Maximum adoption velocity; attribution to Pillars happens in README and other comms, not via license obligation.
- Worked examples drafted: `context.md` (for the Pillars project itself) and `AGENTS.md` (dogfooded).

## Decisions Open
- AGENTS.md final wording polish (current draft is functional).
- Optional: draft `repo.md` as a second worked example before exiting plan mode.
- Optional: pressure-test the standard against 2-3 hypothetical projects before exiting.

## Philosophy: Briefings, Not Rulebooks

The pillar's job is to surface what the agent **cannot infer from the code** — project-specific facts, decisions, and lessons. Not to dictate what the agent does with that knowledge. Coding agents are capable; over-constraining them removes their value. The standard exists to **prevent drift**, not to put the agent on rails.

Core principle:
> Include prescriptive content only when it would *not* be inferred from the facts.

"Project uses Drizzle" doesn't need a separate rule "use Drizzle" — the agent infers. But "project uses Drizzle AND never raw SQL outside `db/raw.ts`" *does* need stating, because Drizzle and raw SQL can coexist; the agent can't infer that constraint from code alone.

Watchouts work the same way: they exist because the failure mode isn't visible in the code. The reasoning is the load-bearing content, not the prohibition.

Tone consequence: pillars should read like *what an experienced engineer would tell a new contributor on day one*. Conversational, declarative, reasoned. Not like compliance documentation.

## Pillar Template (8 sections, middle-ground)
Every pillar's body follows this shape so agents can parse predictably. The template combines a briefing foundation (Context + Decisions) with a prescriptive layer (Rules + Watchouts). Sections 3-6 are populated only when they earn their keep; if Context already implies the content, don't restate it.

1. **Scope** — what this pillar covers, what it doesn't.
2. **Context** — declarative facts about this project in this domain. Stack choices, file locations, naming, conventions in use, where things live. The default-populated section. The bulk of the pillar.
3. **Decisions** — non-obvious choices and why they were made. Captures reasoning the code can't show. Example: "We picked Drizzle over Prisma because we need raw SQL escape hatches and migration introspection." Optional; skip when there's nothing non-obvious to explain.
4. **Rules** — hard constraints not inferable from Context. The agent must follow these. Used sparingly. Example: "Never raw SQL outside `db/raw.ts` — the audit logger only intercepts queries that go through the ORM." Optional; skip when Context covers the constraint.
5. **Workflows** — multi-step procedures the agent might not infer from facts alone. Example: "Adding a column: schema edit, drizzle-kit generate, drizzle-kit push, update seeds." Optional; skip when the procedure is obvious from Context.
6. **Watchouts** — soft warnings from experience, with reasoning. Not bans; informed warnings. The agent decides. Example: "Adding columns in dev without a migration causes drift across machines because the prod pipeline only runs declared migrations." Optional; skip when there's no historical pain worth surfacing.
7. **Touchpoints** — couplings to other pillars (mirrors frontmatter for human readability).
8. **Gaps** — explicit "not decided yet." Tells the agent when to ask the human instead of inferring.

### Graduated firmness ladder (sections 3-6)
| Section | Firmness | Job |
|---|---|---|
| Decisions | Informative | "Here's why we picked this." |
| Rules | Hard | "Follow this constraint." |
| Workflows | Procedural | "Here's the recipe." |
| Watchouts | Soft | "Be aware this has burned us." |

Examples appear inline within Context, Rules, or Workflows rather than as their own section.

### Core authoring principle
> Include prescriptive content only when it would *not* be inferred from the facts.

The agent is trusted by default. Rules and Watchouts exist for the residual: things the agent genuinely can't derive from Context. Most pillars will use 5-6 of the 8 sections meaningfully; empty sections explicitly marked "(none)".

## Frontmatter Schema
Every pillar opens with YAML frontmatter. Machine-readable header, human-readable body.

```yaml
---
pillar: data                       # the canonical name
status: present | stub             # default present; stub means "concern acknowledged, rules undefined"
always_load: false                 # default false; true means loaded every session regardless of triggers
covers: [...]                      # one-line scope, for skim and discovery
triggers: [keyword, phrase, ...]   # the agent uses these to decide relevance
must_read_with: [auth, config]     # direct hard dependencies; loaded with this pillar (depth 1, no transitive)
see_also: [api, observe]           # soft, loaded only if task explicitly touches that area
---
```

### Field semantics
- `pillar`: canonical name. Filename and pillar name should match.
- `status`: `present` (real content) or `stub` (file exists but rules not yet authored). Drives behavior: stub means "ask, don't infer."
- `always_load`: pillars with `true` are loaded every session. Used sparingly. Currently applies to `context` and `repo` only.
- `covers`: one-line scope.
- `triggers`: keywords/phrases the agent uses to match tasks to pillars. Should be specific enough not to over-match.
- `must_read_with`: **direct** hard edges. The agent loads these alongside the primary; it does NOT transitively follow their `must_read_with`. If a pillar genuinely needs transitive deps, list them directly. Frequently-needed pillars graduate to `always_load: true`.
- `see_also`: soft edges. Agent loads only if the task explicitly touches that area.

### Sub-pillar discovery: folder-based
Sub-pillars live in a nested folder named for their parent: `./agents/data/migrations.md` is a sub-pillar of `data`. The hierarchy is derived from the path; no `parent:` field in frontmatter. Sub-pillars use the same template and frontmatter schema as top-level pillars.

## Loading Strategy

**AGENTS.md is a protocol, not a registry.** Approximate body:

> Pillar files live in `./agents/*.md`. At the start of any task:
> 1. Always load: every pillar whose frontmatter has `always_load: true`.
> 2. Scan all other pillars' frontmatter. Identify the primary pillar(s) whose `triggers` match the task.
> 3. Load the primaries and every pillar listed in their `must_read_with` (depth 1 only; do not follow transitively).
> 4. Consult `see_also` only if the task explicitly touches that area.
> 5. Follow `Rules`. Apply `Workflows`. Heed `Watchouts`. Defer to `Gaps`.

AGENTS.md is ~40 lines, including the missing-pillar protocol (below). Does not grow when pillars are added.

**Loading is a single pass, depth-1.** Read all frontmatter cheaply (~20 small headers at most), pick primaries, load primaries plus their direct `must_read_with` entries. No transitive following. Authors get a predictable, declared load set per pillar.

**Why depth 1, not transitive closure.** Predictability for authors: reading one pillar's frontmatter tells you exactly what loads alongside it. Forces honest declaration: if `data` needs `auth` and `config`, both are listed directly; coupling is visible at the source. Frequently-needed pillars graduate to `always_load: true` instead of becoming hidden transitive deps.

**Self-diagnosing decomposition.** Standard flags it as a smell if any pillar's `must_read_with` has more than ~3 entries, or if a coupling pattern looks like "every pillar lists the same N pillars." The fix is to promote the common dependency to `always_load: true` or to revisit pillar boundaries. Bad decomposition is visible in the frontmatter.

### Why this over a central router or chain walk
- **Decentralized:** adding a pillar requires zero AGENTS.md changes.
- **Portable:** any agent in any tool implements it with a YAML parser plus a graph walk. No tool-specific extensions.
- **Layered:** frontmatter for the agent, body for the human, same file.
- **Composable with the broader AGENTS.md convention:** a project's AGENTS.md can point at `./agents/` and inherit cleanly without conflicting.
- **Minimal spec:** the standard fits in ~200 lines of prose. Someone could implement against it in a day.

## Missing-Pillar Protocol

A pillar can be in four states relative to a project. The standard specifies what the agent does in each:

| State | Indicator | Agent behavior |
|---|---|---|
| **Present** | File exists, `status: present` | Load and comply normally |
| **Stub** | File exists, `status: stub`, minimal body | Acknowledge the concern; ask the human before making decisions; do not silently infer |
| **Excluded** | Name appears in AGENTS.md's `excluded:` list (e.g., a CLI tool with `excluded: [ui, i18n, a11y]`) | Concern not applicable; proceed without |
| **Absent (silent gap)** | Trigger matches a known pillar name, but no file exists and not excluded | Graceful degradation: infer conventions from existing code, *state the assumption in the response*, recommend creating the pillar |

### Why four states (not fewer)
- **Stub vs. Absent** differ in agent action: stub means "ask," absent means "infer and disclose." Collapsing them loses important behavior.
- **Excluded** prevents the agent from flagging legitimate non-concerns as gaps. Without it, absent pillars generate noise.
- **Absent is not a hard error** because real codebases adopt incrementally. If absence blocked work, nobody would adopt.

### Special case: always-loaded pillars
`context` and `repo` (the only `always_load: true` pillars) do not degrade silently. If either is missing on a project claiming compliance, the agent pauses and asks the human to either create stubs or declare them excluded.

### Bootstrapping flows that fall out of this
- **New project:** create stubs for every Tier 1 pillar that applies; explicitly exclude (with reasons) those that don't. A pillar "exists" once it has frontmatter and a Scope statement, even if other sections are empty. Sections within each pillar fill in over the project's lifetime as decisions get made. Stub -> partially populated -> fully populated is the maturity gradient. There is no obligation to fill all eight sections at creation time.
- **Existing project:** pillars mostly absent. Agent degrades to inference with explicit assumption-stating. Pillars get authored from inferred patterns over time (manually or via the future toolkit).

## Pillar Architecture

- **Always-loaded (2):** `context`, `repo`. Tiny by spec (~one page each). Loaded every session via `always_load: true`.
- **Tier 1 — Core (9 task-routed):** topics every non-trivial project should *consider*. Not every project populates them all; excluding is first-class. The tier exists so adopters reason about each topic, not so they must implement each.
- **Tier 2 — Common (10):** recommended when relevant. Add as the project grows into them.
- **Tier 3 — Domain (open set):** topics that depend on what you're building. Often the *primary* pillars for the projects that need them: `realtime` for collab apps, `ml` for ML systems, `seo` for marketing sites, `payments` for e-commerce. The standard provides examples; projects coin new domain pillars freely (e.g., `inventory.md` for e-commerce).
- **Sub-pillars:** folder-based; `./agents/<parent>/<name>.md`. Same template and frontmatter as top-level pillars.

### Always-Loaded (2)

| Pillar | Covers |
|---|---|
| `context.md` | Domain language, product invariants, glossary, why the project exists. Tiny by spec. |
| `repo.md` | File layout, naming conventions, where things go. Every file-touching task needs this. |

### Tier 1 — Core (9, task-routed)

| Pillar | Covers |
|---|---|
| `stack.md` | Tech choices, dependencies, version constraints, why each was chosen. |
| `arch.md` | System architecture, services, boundaries, data flow at the system level. |
| `data.md` | Data model, schema, migrations, queries, storage. |
| `api.md` | API contract: HTTP, RPC, internal. Request/response shapes. Versioning. |
| `ui.md` | Visual + interaction conventions. Components. Design tokens. (Excluded if no UI.) |
| `auth.md` | Identity, sessions, access. Authn + authz. (Secrets live in `config.md`.) |
| `quality.md` | Testing, error handling, code style, naming. Sub-pillars allowed if a project wants depth. |
| `deploy.md` | Cutover, environments, promotion, rollback. |
| `observe.md` | Logging, metrics, tracing, alerts, runbooks. |

### Tier 2 — Common (10)

| Pillar | Covers |
|---|---|
| `config.md` | Env vars, feature flags, secrets handling, configuration. |
| `security.md` | Adversarial concerns beyond auth: input validation, OWASP, threat model, dependency CVEs. |
| `compliance.md` | Regulatory mapping: SOC2, HIPAA, GDPR, PCI. |
| `i18n.md` | Translation, locale, RTL, formatting. |
| `a11y.md` | Accessibility standards, WCAG, screen reader patterns. |
| `analytics.md` | Product event tracking, user telemetry, KPIs. (Distinct from `observe`.) |
| `integrations.md` | Third-party services consumed, outbound API calls, contracts. Above ~3-5 significant integrations, promote each to a sub-pillar (`integrations/<service>.md`). |
| `async.md` | Background jobs, queues, schedulers, cron, event-driven work. |
| `cache.md` | Caching strategy, invalidation, layers, TTLs. |
| `notifications.md` | *Transactional* notifications: order confirmations, password resets, system alerts via email/SMS/push. Marketing or lifecycle email lives in `email.md` (Tier 3). |

### Tier 3 — Domain (open, examples)

`ml.md`, `realtime.md`, `payments.md`, `email.md` (marketing/lifecycle; transactional lives in `notifications.md`), `search.md`, `mobile.md`, `state.md` (frontend state management; essential when relevant despite Tier 3 placement), `forms.md`, `validation.md`, `seo.md`, `event-bus.md`, `pubsub.md`, `cms.md`, `crm.md`, `cli.md` (CLI UX: color, prompts, output formatting), `inventory.md` (e-commerce stock/SKU rules), `data-pipeline.md`, `etl.md`, plus any domain pillar the project needs. The list is illustrative, not exhaustive — projects coin new domain pillars when justified.

**Note:** Tier 3 placement does not imply "rarely needed." For some project types, a Tier 3 pillar is the *primary* concern: `realtime` for collaborative apps, `ml` for ML systems, `seo` for marketing sites, `payments` for e-commerce. The "Domain" tier captures concerns whose presence depends on *what* you're building, not on *how big* your project is.

### Boundary calls (settled in this iteration)
- **`auth.md` vs. `security.md`:** auth is "who's allowed to do what" (identity + permissions); security is "everything else adversarial" (input validation, OWASP, dependency CVEs, threat model).
- **`auth.md` vs. `config.md`:** secrets live in `config.md`, not `auth.md`. Auth handles access; config handles configuration including secret materials.
- **`analytics.md` vs. `observe.md`:** analytics = understanding users (product KPIs); observe = understanding system health (operational telemetry). Same event might emit to both; rules for emitting them differ.
- **`repo.md` vs. `arch.md`:** repo covers file layout (where files go); arch covers system shape (what services/modules exist). If a rule changes where a file goes, it's repo; if it changes module/service structure, it's arch.
- **`quality.md` as a bundle:** keeps testing + errors + style together. Splittable via sub-pillars (`quality/testing.md`) when a project needs depth.
- **Dedicated integration pillar vs. `integrations.md`:** if the integration has its own business logic and lifecycle (Stripe billing, Auth0 user sync), give it a dedicated Tier 3 pillar. If it's a thin wrapper around a third-party API, list it under `integrations.md`. Rule of thumb: would removing the integration change the product, or just a feature?
- **`ui.md` scope:** web/visual UI conventions. CLI UX (color, prompts, output format) gets a Tier 3 `cli.md` pillar; not in scope for `ui.md`.
- **`compliance.md`:** project-specific. SaaS often needs SOC 2; ML touching biometric/health data needs HIPAA/GDPR; CLI tools may need nothing. Excluding compliance entirely is legitimate.

## Sub-Pillar Conventions

Sub-pillars live in a folder named for their parent: `./agents/<parent>/<name>.md`. Hierarchy is path-derived; no `parent:` field in frontmatter. Sub-pillars use the same 8-section template and the same frontmatter schema as top-level pillars. They participate in loading the same way (matched by `triggers`, loaded with their direct `must_read_with`).

### Common sub-pillar patterns

| Pattern | Example sub-pillars | When |
|---|---|---|
| **Cross-cutting Tier 3 specialty** | `security/ml.md`, `quality/ml.md`, `observe/ml.md` | When a Tier 3 domain pillar (`ml`, `realtime`, `mobile`) has implications across Core pillars. The Tier 3 pillar owns its domain; sub-pillars capture cross-cuts. |
| **Multiple API surfaces** | `api/storefront.md`, `api/admin.md`, `api/webhooks.md` | Apps with distinct API consumers and contracts. |
| **Integration saturation** | `integrations/algolia.md`, `integrations/klaviyo.md` | When `integrations.md` has more than ~3-5 significant entries. |
| **UI depth** | `ui/components.md`, `ui/animations.md`, `ui/tokens.md` | UI-heavy projects where one pillar bloats. |
| **Quality depth** | `quality/testing.md`, `quality/style.md` | When testing rules are substantial enough to warrant their own home. |
| **Multi-tenancy** | `data/multi-tenant.md` | SaaS apps where tenant isolation rules deserve focused attention. |
| **Data shape** | `data/migrations.md`, `data/queries.md` | When data conventions split cleanly into schema management vs. query patterns. |

### Loading behavior

A sub-pillar can declare `must_read_with: [parent]` if loading the sub-pillar requires its parent. Conversely, a top-level pillar might list specific sub-pillars in `see_also` to flag where deep-dive material lives. The standard does not auto-load a parent when a sub-pillar matches — coupling is explicit.

## Pressure-Test Findings (from walking 3 hypothetical projects)

Walked the standard through:
- **Tenantly** (SaaS multi-tenant dashboard) — 17 pillars active.
- **Skein** (Go CLI tool) — 8 pillars active, 13 excluded.
- **Lensflare** (Python ML embedding service) — 17 pillars active including Tier 3 specialties.

**Structural verdict:** the standard is sound. All three projects mapped cleanly. Tiers, frontmatter, template, loading mechanism all held up. The friction is in *guidance* (boundary tiebreakers, exclusion templates, sub-pillar recommendations), not structure.

**Six concrete updates fall out (most live in PILLARS.md or SPEC.md, none change the structure):**

1. **Reframe "Required Core" -> "Core."** Tier 1 = topics every non-trivial project should *consider*, not *populate*. Skein excludes 5 of 9; that's legitimate. Excluding is first-class.
2. **Make `excluded:` first-class in AGENTS.md.** Provide common-exclusion templates for archetypes: CLI tool, internal API service, ML pipeline, mobile app, marketing site.
3. **Add tiebreaker guidance** to PILLARS.md for the common boundary calls (now logged above).
4. **Document the sub-pillar pattern for cross-cutting Tier 3 specialties.** Adopting `ml.md` often requires `security/ml.md`, `quality/ml.md`, `observe/ml.md` shadow pillars. Standard recommends this explicitly.
5. **Soften "populated" language.** A pillar exists when it has frontmatter + Scope. Sections evolve over project lifetime. Stub status is intentional for new projects.
6. **Add multi-tenancy as a documented sub-pillar example.** `data/multi-tenant.md` is a common need for SaaS projects.

### Friction surfaced but not blocking
- **ML specialties cut across pillars.** Model eval = `ml.md` or `quality.md`? Model drift = `ml.md` or `observe.md`? Adversarial inputs = `ml.md` or `security.md`? Standard's answer: high-Tier-3 specialties OWN their cross-cutting concerns; other pillars cross-reference via `must_read_with`. Accept high `must_read_with` count for specialty pillars.
- **CLI tool excludes 13 pillars.** That's fine but reveals: archetype-based AGENTS.md scaffolds (one for CLI, one for SaaS, one for ML) would dramatically lower adoption friction.

## Second Pressure-Test Pass (3 more projects)

Walked three additional projects to stress areas the first round didn't cover:
- **Brushlight** (marketing site, Next.js static + Sanity CMS): ~12 pillars active. UI-heavy, SEO-critical, content-modeling-heavy.
- **Liveboard** (real-time collaborative whiteboard, SvelteKit + Yjs + Liveblocks): ~17 pillars active. CRDT logic spans multiple pillars.
- **Storefront** (e-commerce, Remix + Shopify Hydrogen + Stripe + Algolia + Klaviyo): ~22 pillars active. Largest project tested. Many Tier 3 specialties.

**New findings (7-14, continuing from round 1):**

7. **Tier 3 name "Specialized" undersells the role.** `realtime`, `ml`, `seo`, `payments` are *primary concerns* for their projects, not rare. Rename Tier 3 -> **"Domain"**.
8. **Domain pillars are first-class even outside the example list.** Storefront needs `inventory.md`; Liveboard might need `crdt.md`. Standard encourages domain pillars without exhaustive enumeration.
9. **Platform-provided exclusions are legitimate.** Extend `excluded:` to support reasons:
   ```yaml
   excluded:
     - name: observe
       reason: Vercel Analytics + built-in alerting cover our needs
   ```
10. **API sub-pillars are common.** Multiple API surfaces (storefront / admin / webhooks) -> `api/<surface>.md` sub-pillars. Normalize in PILLARS.md.
11. **`integrations.md` saturation point ~3-5 entries.** Above that, mid-significance integrations should become sub-pillars: `integrations/algolia.md`.
12. **`notifications.md` vs. `email.md` refined.** notifications = transactional (order confirmation, password reset); `email.md` (Tier 3) = marketing/lifecycle (campaigns, drip sequences). Different regulatory and operational rules.
13. **`state.md` is essential for frontend-heavy apps but not backend services.** Keep Tier 3, note "essential when relevant despite Tier 3 placement."
14. **`ui.md` gets sub-pillars for UI-heavy projects.** `ui/components.md`, `ui/animations.md`, `ui/tokens.md`. Normalize.

### Meta-observation: friction is converging
Across six projects, no *structural* problem has surfaced. All findings are *guidance* (boundary calls, tier naming, sub-pillar patterns). The standard's bones are right. Marginal value per additional pressure-test is decreasing; further projects would surface ~3-5 more guidance refinements but nothing structural. Sufficient to author SPEC.md and PILLARS.md confidently. Adopters will find new edges; iterate in v0.2.

## Cuts from earlier drafts
- `ops.md` (replaced by `deploy.md` + `observe.md`).
- `product.md` (renamed to `context.md` to clarify intent).
- `jobs.md` (renamed to `async.md` for broader coverage).
- `governance.md` (too vague; dropped from Tier 3 examples).
- `legal.md` (subsumed by `compliance.md`).

## Worked Example: `agents/context.md` (dogfooded for the Pillars project itself)

```yaml
---
pillar: context
status: present
always_load: true
covers: [project identity, domain language, product invariants, glossary]
triggers: []
must_read_with: []
see_also: [repo]
---
```

### Scope
This pillar describes what Pillars is, the domain language used throughout the standard, the product invariants that hold across all decisions, and a glossary of canonical terms. It does not cover technical conventions (those live in `repo.md`), the standard's authoring template (lives in `SPEC.md`), or the pillar enumeration (lives in `PILLARS.md`).

### Context
Pillars is an open standard for project-specific instructions that keep coding agents (Claude, Cursor, Copilot, Codex, Aider, others) aligned to a codebase's facts, decisions, and conventions. A project adopting Pillars publishes markdown files at `./agents/*.md`, each conforming to the 8-section pillar template and opening with YAML frontmatter the agent uses to decide what to load. An `AGENTS.md` at the repo root describes the loading protocol; it is ~40 lines and does not grow when pillars are added.

The standard is tool-agnostic: any agent that can read markdown and parse YAML can implement Pillars in a day. Pillars sits underneath the broader AGENTS.md convention rather than replacing it; tool-specific files (`CLAUDE.md`, `.cursorrules`, `copilot-instructions.md`) become thin shims pointing at AGENTS.md.

Glossary:
- **Pillar** — a single domain's briefing file (e.g., `data.md`, `auth.md`). Sits in `./agents/`.
- **Always-loaded pillar** — frontmatter has `always_load: true`. Read every session regardless of task. Currently `context` and `repo`.
- **Trigger** — keyword or phrase in frontmatter; the agent matches against the task description to decide relevance.
- **Touchpoint** — declared coupling between pillars. Hard (`must_read_with`) or soft (`see_also`).
- **Closure** — the full set of pillars loaded for a task: primaries plus the transitive closure of `must_read_with`.
- **Stub** — pillar with `status: stub` and minimal body. Signals "concern acknowledged, rules undefined; ask, don't infer."
- **Excluded** — pillar name declared in AGENTS.md's `excluded:` list as not applicable to this project.

Product invariants:
- The standard is portable; no tool-specific extensions allowed.
- Pillars are briefings, not rulebooks; they surface what the agent can't infer from code.
- Loading is single-pass; no chain walks during task execution.
- Missing pillars degrade gracefully via inference + assumption-stating; adoption is incremental.
- The standard is small: the full spec is intended to fit in ~200 lines of prose.

### Decisions
- **Three tiers + always-loaded set, not a flat list.** Reason: handles the long tail of project types without bloating the required core.
- **Frontmatter-driven discovery, not a central router.** Reason: keeps the standard decentralized and portable; adding a pillar requires zero AGENTS.md changes.
- **8-section template combining briefing + prescriptive layers.** Reason: trust the agent by default (Context + Decisions) but allow hard constraints (Rules + Watchouts) when not inferable from facts.
- **Layer 1 (spec) only for v1; Layer 2 (toolkit) separate product.** Reason: a standard should stand alone; tooling versions independently.

### Rules
(none) — context.md surfaces facts; constraint pillars sit elsewhere.

### Workflows
- **Adding a new top-level pillar to the standard:** decide tier, write frontmatter, write the 8 sections per "earn your keep" principle, update `PILLARS.md` enumeration, declare touchpoints from neighboring pillars where coupling is real.

### Watchouts
- **Don't write Rules content that would be inferred from Context.** Bloats pillars without value. Re-read the principle: prescriptive content only when not inferable.
- **Don't make pillars compliance documents.** Tone is "experienced engineer briefing a new contributor on day one," not "auditor's checklist."
- **Don't over-couple via `must_read_with`.** More than ~3 entries signals a boundary smell; the pillar may be doing too much.

### Touchpoints
- `see_also: [repo]` — tasks that touch file layout in addition to project identity load `repo.md`.

### Gaps
(none open at the standard level; project-specific gaps would be listed here as the standard evolves)

## Worked Example: `AGENTS.md` (dogfooded for the Pillars project itself)

```markdown
# Pillars: Agent Protocol

This project follows the [Pillars](https://pillars.example) standard. Coding
agents working in this repository read the pillar files in `./agents/*.md` to
stay aligned with the project's facts, decisions, and conventions.

## At the start of any task

1. **Load always-pillars.** Read every file in `./agents/` whose frontmatter
   has `always_load: true`. These load every session regardless of task.

2. **Identify primary pillars.** Scan the frontmatter of all other files in
   `./agents/`. For each, check whether its `triggers` match the current task.
   The matching pillars are this task's primaries.

3. **Compute the load set.** Start with the primaries. Add every pillar
   listed in their `must_read_with` (depth 1; do not follow transitively).
   The result is the full load set.

4. **Load bodies.** Read the bodies of every pillar in the load set.

5. **Consult `see_also` selectively.** If the task explicitly touches an area
   named in a loaded pillar's `see_also`, read that pillar too. Otherwise skip.

6. **Comply.** Follow `Rules`. Apply `Workflows`. Heed `Watchouts` (using
   judgment). Defer to `Gaps` (ask the human; don't infer silently).

## Handling missing pillars

| State | Action |
|---|---|
| `status: present` | Load and comply. |
| `status: stub` | Concern acknowledged but rules undefined. Ask the human before making decisions in this area. Do not infer silently. |
| Name in `excluded:` (below) | Not applicable to this project. Proceed without. |
| Trigger matches a known name, file absent, not excluded | Graceful degradation. Infer conventions from code. State the assumption. Recommend creating the pillar. |

If `context.md` or `repo.md` is missing entirely, pause and ask the human to
either create stubs or declare them excluded. These are the floor.

## Excluded pillars

The following pillars are intentionally not used in this project. Reasons are
recommended (not required) so future contributors understand the call.

```yaml
excluded: []
```

When non-empty, the form is:

```yaml
excluded:
  - name: observe
    reason: Vercel Analytics + built-in alerting cover our needs
  - name: i18n
    reason: English-only product
```

## Archetype starter exclusions (suggestions, not enforced)

New adopters can start from an archetype list rather than rediscovering common
exclusions:

- **CLI tool:** ui, api, auth, observe, i18n, a11y, analytics, async, cache, notifications
- **Internal API service:** ui, a11y, seo, notifications (if no end-user surface)
- **ML pipeline:** ui, i18n, a11y, notifications, analytics
- **Marketing site:** data, api, auth (if no users), observe (if platform-provided), async

## Reference

- Pillar files: `./agents/*.md`
- Spec: `./SPEC.md`
- Pillar enumeration: `./PILLARS.md`
```

## Next Steps in This Conversation
1. Review the worked `context.md` and `AGENTS.md` drafts above; iterate if needed.
2. Optionally draft `repo.md` as a second worked example to stress-test the template.
3. Decide remaining open decisions (sub-pillar discovery rule, stopping condition default, license).
4. ExitPlanMode and execute: create `pillars/`, scaffold the folder structure, move DESIGN-NOTES.md, write SPEC.md / PILLARS.md / README.md, copy worked examples into `agents/` and `examples/`.
