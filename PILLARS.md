# Pillars Enumeration

This document lists the pillars Pillars defines, their tiers, their scopes, and the boundary calls that draw lines between them. It also documents sub-pillar patterns.

The standard's *structure* lives in [SPEC.md](SPEC.md). This document is the *catalog*.

## Tier overview

- **Always-loaded (2):** `context`, `repo`. Tiny by spec (~one page each). Loaded every session via `always_load: true` in frontmatter.
- **Tier 1 — Core (9, task-routed):** topics every non-trivial project should *consider*. Not every project populates them all; excluding is first-class. The tier exists so adopters reason about each topic, not so they must implement each.
- **Tier 2 — Common (10):** recommended when relevant. Add as the project grows into them.
- **Tier 3 — Domain (open set):** topics whose presence depends on *what* you're building. Often the primary pillars for the projects that need them: `realtime` for collab apps, `ml` for ML systems, `seo` for marketing sites, `payments` for e-commerce.
- **Sub-pillars:** folder-based deep-dives within a top-level pillar. Same template and frontmatter.

## Always-loaded (2)

| Pillar | Covers |
|---|---|
| `context.md` | Domain language, product invariants, glossary, why the project exists. Tiny by spec. |
| `repo.md` | File layout, naming conventions, where things go. Every file-touching task needs this. |

## Tier 1 — Core (9, task-routed)

| Pillar | Covers |
|---|---|
| `stack.md` | Tech choices, dependencies, version constraints, why each was chosen. |
| `arch.md` | System architecture, services, boundaries, data flow at the system level. |
| `data.md` | Data model, schema, migrations, queries, storage. |
| `api.md` | API contract: HTTP, RPC, internal. Request/response shapes. Versioning. |
| `ui.md` | Web/visual UI conventions. Components. Design tokens. (CLI UX lives in Tier 3 `cli.md`.) |
| `auth.md` | Identity, sessions, access. Authn + authz. (Secrets live in `config.md`.) |
| `quality.md` | Testing, error handling, code style, naming. Sub-pillars when a project wants depth. |
| `deploy.md` | Cutover, environments, promotion, rollback. |
| `observe.md` | Logging, metrics, tracing, alerts, runbooks. |

## Tier 2 — Common (10)

| Pillar | Covers |
|---|---|
| `config.md` | Env vars, feature flags, secrets handling, configuration. |
| `security.md` | Adversarial concerns beyond auth: input validation, OWASP, threat model, dependency CVEs. |
| `compliance.md` | Regulatory mapping: SOC2, HIPAA, GDPR, PCI. Project-specific. |
| `i18n.md` | Translation, locale, RTL, formatting. |
| `a11y.md` | Accessibility standards, WCAG, screen reader patterns. |
| `analytics.md` | Product event tracking, user telemetry, KPIs. |
| `integrations.md` | Third-party services consumed, outbound API calls, contracts. Above ~3-5 significant integrations, promote each to a sub-pillar (`integrations/<service>.md`). |
| `async.md` | Background jobs, queues, schedulers, cron, event-driven work. |
| `cache.md` | Caching strategy, invalidation, layers, TTLs. |
| `notifications.md` | *Transactional* notifications (order confirmations, password resets, system alerts) via email/SMS/push. Marketing or lifecycle email lives in Tier 3 `email.md`. |

## Tier 3 — Domain (open, examples)

The standard provides examples; projects coin new domain pillars freely when justified.

Common examples: `ml.md`, `realtime.md`, `payments.md`, `email.md` (marketing/lifecycle), `search.md`, `mobile.md`, `state.md` (frontend state management; essential when relevant despite Tier 3 placement), `forms.md`, `validation.md`, `seo.md`, `event-bus.md`, `pubsub.md`, `cms.md`, `crm.md`, `cli.md` (CLI UX: color, prompts, output formatting), `inventory.md` (e-commerce stock/SKU rules), `data-pipeline.md`, `etl.md`.

**Tier 3 placement does not imply "rarely needed."** For some project types, a Tier 3 pillar is the *primary* concern. The "Domain" tier captures concerns whose presence depends on *what* you're building, not on how big the project is.

## Boundary calls

The standard defines these tiebreakers for pillar pairs that get confused. When in doubt, refer here.

### Auth vs. security

- **`auth.md`** = "who's allowed to do what." Identity, sessions, permissions.
- **`security.md`** = everything else adversarial. Input validation, OWASP, dependency CVEs, threat model, attacker-already-inside scenarios.

### Auth vs. config

- Secrets live in **`config.md`**, not `auth.md`. Auth handles access; config handles configuration including secret materials.

### Analytics vs. observe

- **`analytics.md`** = understanding *users* (product KPIs, behavioral events).
- **`observe.md`** = understanding *system health* (operational telemetry, error rates, latency).
- The same event might emit to both pipelines; the rules for emitting them differ.

### Repo vs. arch

- **`repo.md`** = file layout (where files go).
- **`arch.md`** = system shape (what services/modules exist, how they communicate).
- If a rule changes where a file goes, it's `repo`. If it changes module/service structure, it's `arch`.

### Quality bundle

- **`quality.md`** keeps testing + errors + style + naming together by default.
- Splittable via sub-pillars (`quality/testing.md`, `quality/style.md`) when a project needs depth.

### Dedicated integration pillar vs. `integrations.md`

- If the integration has its own business logic and lifecycle (Stripe billing, Auth0 user sync), give it a dedicated Tier 3 pillar.
- If it's a thin wrapper around a third-party API, list it under `integrations.md`.
- Rule of thumb: would *removing* the integration change the product, or just a feature?

### UI scope

- **`ui.md`** = web/visual UI conventions only.
- CLI UX (color, prompts, output format) gets a Tier 3 `cli.md`. Not in scope for `ui.md`.

### Compliance scope

- **`compliance.md`** is project-specific. SaaS often needs SOC 2; ML touching biometric/health data needs HIPAA/GDPR; CLI tools may need nothing. Excluding `compliance` entirely is legitimate.

### Notifications vs. email

- **`notifications.md`** (Tier 2) = *transactional* notifications (order confirmations, password resets) via email/SMS/push.
- **`email.md`** (Tier 3) = *marketing/lifecycle* email (campaigns, drip sequences). Different operational and regulatory rules (sending limits, suppression lists, CAN-SPAM).

## Sub-pillar conventions

Sub-pillars live in a folder named for their parent: `./agents/<parent>/<name>.md`. Hierarchy is path-derived; no `parent:` field in frontmatter. Sub-pillars use the same 8-section template and the same frontmatter schema as top-level pillars. They participate in loading the same way.

### Common sub-pillar patterns

| Pattern | Example sub-pillars | When |
|---|---|---|
| **Cross-cutting Tier 3 specialty** | `security/ml.md`, `quality/ml.md`, `observe/ml.md` | When a Domain pillar (`ml`, `realtime`, `mobile`) has implications across Core pillars. The Domain pillar owns its domain; sub-pillars capture cross-cuts. |
| **Multiple API surfaces** | `api/storefront.md`, `api/admin.md`, `api/webhooks.md` | Apps with distinct API consumers and contracts. |
| **Integration saturation** | `integrations/algolia.md`, `integrations/klaviyo.md` | When `integrations.md` has more than ~3-5 significant entries. |
| **UI depth** | `ui/components.md`, `ui/animations.md`, `ui/tokens.md` | UI-heavy projects where one pillar bloats. |
| **Quality depth** | `quality/testing.md`, `quality/style.md` | When testing rules are substantial enough to warrant their own home. |
| **Multi-tenancy** | `data/multi-tenant.md` | SaaS apps where tenant isolation rules deserve focused attention. |
| **Data shape** | `data/migrations.md`, `data/queries.md` | When data conventions split cleanly into schema management vs. query patterns. |

### Loading behavior

A sub-pillar can declare `must_read_with: [parent]` if loading the sub-pillar requires its parent. Conversely, a top-level pillar might list specific sub-pillars in `see_also` to flag where deep-dive material lives. The standard does not auto-load a parent when a sub-pillar matches; coupling is explicit.

## Archetype starter exclusions

Adopters often start from an archetype list to avoid rediscovering common exclusions. These are *suggestions*, not enforced:

| Archetype | Typical exclusions |
|---|---|
| CLI tool | ui, api, auth, observe, i18n, a11y, analytics, async, cache, notifications |
| Internal API service | ui, a11y, seo (if no end-user surface), notifications (if no end users) |
| ML pipeline | ui, i18n, a11y, notifications, analytics |
| Marketing site | data, api, auth (if no users), observe (if platform-provided), async |
| Mobile app | seo, i18n (if single-locale), `realtime` (if not collaborative) |
| Open-source library | ui, api (if not a service), auth, observe, deploy (if not hosted), notifications, analytics |
| SaaS dashboard | (none initially; add as decisions get made) |
| Empty / greenfield | (none initially; add exclusions as the project takes shape) |

Reasons are recommended in `AGENTS.md`'s `excluded:` block so future contributors understand the call.

## Naming conventions

- Pillar file: `<name>.md` where `<name>` is the canonical pillar name in lowercase.
- Sub-pillar file: `<parent>/<name>.md` under `./agents/`.
- Frontmatter `pillar:` matches the filename without `.md`.
- Pillar names are nouns or noun phrases (`auth`, `data`, `multi-tenant`), never verbs.

## Maturity gradient

A pillar exists once it has frontmatter and a Scope statement, even if Sections 3-8 are empty (or `(none)`). Sections fill in over the project's lifetime: stub -> partially populated -> fully populated. There is no obligation to fill all 8 sections at creation time.
