# The Pillar Catalog

**This is the menu of topics you can write up, not a list of homework.**

Every project has a handful of things an AI assistant cannot work out on its own: what the product actually is, where files belong, how login works, how you ship. This document names those topics so you can decide, once, which ones matter for your project. Most projects use a focused subset and deliberately skip the rest.

New to Pillars? Read [the README](README.md) first. The exact file format and loading behavior live in [SPEC.md](SPEC.md).

## How to use this page

1. Skim the tables below and pick the topics that apply to your project.
2. Write those pillars, starting with the two always-loaded ones.
3. Mark topics that clearly do not apply as excluded, in one line, in your `AGENTS.md`. A command-line tool has no login screen, and recording that is genuinely useful.
4. For topics you know matter but have not documented yet, add an entry to `agents/catalog.yaml` so the assistant knows what it does not know.

You are never required to fill in everything, and a partially written pillar beats no pillar. Suggested starting points by project type are at the [bottom of this page](#archetype-starter-exclusions).

## The tiers, in plain terms

- **Always-loaded (2):** `context` and `repo`. Read on every single task, so they stay short.
- **Tier 1, Core (11):** the topics almost every real project has an opinion about. Loaded only when the task is relevant, and can be excluded.
- **Tier 2, Common (11):** cross-cutting topics that show up often but not always. Add them when they apply.
- **Tier 3, Domain (open set):** whatever is specific to your product, such as payments, search, or inventory. You invent these.
- **Sub-pillars:** a deeper dive inside one topic, kept in a folder, for when a single pillar starts getting crowded.

## Always-loaded (2)

| Pillar | Covers |
|---|---|
| `context.md` | Project identity, domain language, invariants, glossary, and why the project exists. |
| `repo.md` | File layout, naming conventions, ownership, and where things go. |

## Tier 1, Core (11)

| Pillar | Covers |
|---|---|
| `stack.md` | Technology choices, dependencies, version constraints, and why each was chosen. |
| `arch.md` | System architecture, services, boundaries, and system-level data flow. |
| `data.md` | Data model, schema, migrations, queries, and storage. |
| `api.md` | HTTP, RPC, and internal API contracts, shapes, and versioning. |
| `ui.md` | Web and visual UI conventions, components, and design tokens. CLI UX belongs in Domain `cli.md`. |
| `auth.md` | Identity, sessions, authentication, authorization, and access. Secrets belong in `config.md`. |
| `quality.md` | Testing, error handling, code style, and naming. |
| `development.md` | Local setup, inner-loop commands, debugging, generated artifacts, and contributor workflow. |
| `release.md` | Versioning, release criteria, changelog policy, artifact publication, and release ownership. |
| `deploy.md` | Environments, promotion, cutover, rollback, and runtime delivery. |
| `observe.md` | Logs, metrics, traces, alerts, and operational runbooks. |

`development` and `release` are Core in 1.1 because nearly every maintained project has local workflow and version-publication decisions that are neither repository layout nor deployment behavior. They remain task-routed, so their addition does not increase the always-loaded floor.

## Tier 2, Common (11)

| Pillar | Covers |
|---|---|
| `config.md` | Environment variables, feature flags, secrets handling, and configuration. |
| `security.md` | Adversarial concerns beyond auth: input validation, threat models, dependency vulnerabilities. |
| `privacy.md` | Personal-data classification, collection, consent, retention, deletion, and subject rights. |
| `compliance.md` | Project-specific regulatory and control mappings such as SOC 2, HIPAA, GDPR, and PCI. |
| `i18n.md` | Translation, locale, right-to-left layout, and formatting. |
| `a11y.md` | Accessibility standards, assistive technology, and WCAG patterns. |
| `analytics.md` | Product event tracking, user telemetry, and KPIs. |
| `integrations.md` | Third-party services and outbound contracts. Promote substantial integrations to sub-pillars or Domain pillars. |
| `async.md` | Background jobs, queues, schedules, and event-driven work. |
| `cache.md` | Cache layers, invalidation, and time-to-live policy. |
| `notifications.md` | Transactional email, SMS, and push notifications. Marketing email belongs in Domain `email.md`. |

`privacy` is distinct from compliance. Projects handle personal data even when no formal compliance mapping is maintained, so the concern deserves direct routing rather than being buried in legal controls.

## Tier 3, Domain (open set)

Projects may coin domain pillars when a concern is load-bearing and does not fit the cross-project catalog. Tier 3 placement means product-dependent, not unimportant.

Common examples include:

- Product capabilities: `ml`, `realtime`, `payments`, `search`, `mobile`, `forms`, `seo`, `cms`, `crm`, `cli`, `inventory`, `email`.
- Business model: `domain` or a specific noun such as `orders`, `subscriptions`, `entitlements`, or `pricing`.
- Operating model: `tenancy`, `billing`, `reliability`, `performance`, `infrastructure`, `documentation`.
- Data movement: `event-bus`, `pubsub`, `data-pipeline`, `etl`.
- Frontend depth: `state`, `validation`, `animations`.

Use a precise domain noun when possible. `orders.md` is more useful than a catch-all `business-rules.md` when orders are the actual bounded concern.

## Boundary calls

Two topics often feel like they overlap, and you end up unsure where a fact belongs. These are the calls the standard has already made, with the reasoning. Skip this section until you actually hit one of these questions.

### Auth vs. security

- `auth.md` answers who may do what: identities, sessions, roles, and permissions.
- `security.md` covers other adversarial concerns: untrusted input, abuse, vulnerabilities, and threat models.

### Auth vs. config

Secret material and configuration live in `config.md`. Auth owns how identity and access use that material.

### Data vs. privacy vs. compliance

- `data.md` describes representation, storage, queries, and lifecycle mechanics.
- `privacy.md` describes which data is personal, why it is collected, how long it is kept, and how people exercise rights.
- `compliance.md` maps project behavior to external regulations and control frameworks.

A deletion implementation may touch all three, but each pillar answers a different question.

### Analytics vs. observe

- `analytics.md` explains user and product behavior.
- `observe.md` explains system health and operational behavior.

One event may feed both systems, but collection rules and audiences differ.

### Repo vs. development vs. stack

- `repo.md` says where files belong and how the repository is organized.
- `development.md` says how contributors set up, run, generate, and debug the project.
- `stack.md` says which technologies and dependency versions the project chose.

### Arch vs. infrastructure

- `arch.md` describes logical services, module boundaries, and data flow.
- Domain `infrastructure.md` describes provisioned resources, topology, infrastructure-as-code, capacity, and provider constraints.

Use a dedicated infrastructure pillar only when those operational details are substantial. Small projects can keep infrastructure facts in `deploy.md` or `stack.md`.

### Release vs. deploy

- `release.md` covers version decisions, readiness, changelogs, artifacts, and publication.
- `deploy.md` covers placing a release into an environment, promotion, cutover, and rollback.

A library can release without deploying. A continuously delivered service may deploy many revisions under one product release.

### Quality vs. reliability vs. performance

- `quality.md` covers how changes are verified and code quality is maintained.
- Domain `reliability.md` covers service objectives, failure budgets, resilience, and recovery expectations.
- Domain `performance.md` covers latency, throughput, resource budgets, benchmarks, and optimization constraints.
- `observe.md` owns the telemetry used to measure reliability and performance.

Keep reliability and performance in existing pillars when the guidance is small. Promote them when they have independent budgets, owners, or workflows.

### Domain rules vs. data or API

- A business-domain pillar owns invariants, vocabulary, lifecycle, and decisions such as entitlement or order state rules.
- `data.md` owns how those concepts are stored.
- `api.md` owns how those concepts cross an interface.

Do not make schema shape or endpoint shape the only record of a business invariant.

### Tenancy vs. auth or data

- Domain `tenancy.md` owns tenant boundaries, membership lifecycle, cross-tenant policy, and isolation invariants.
- `auth.md` owns identities and permission checks.
- `data.md` owns storage enforcement and query patterns.

For a narrow data-only concern, `data/multi-tenant.md` remains a good sub-pillar. Use top-level `tenancy.md` when tenancy changes product behavior across auth, data, billing, and operations.

### Billing vs. payments

- Domain `billing.md` owns plans, metering, invoices, credits, tax inputs, and entitlement consequences.
- Domain `payments.md` owns payment collection, payment methods, processor states, refunds, and disputes.

Simple products can combine them. Split when invoicing or entitlements have a lifecycle independent of processor transactions.

### Documentation vs. repo or development

- Domain `documentation.md` owns audience, information architecture, source-of-truth policy, examples, and publication workflow.
- `repo.md` owns where documentation files live.
- `development.md` owns local commands that build or preview documentation.

Create `documentation.md` only when docs are a product surface or have a substantial maintenance model.

### Dedicated integration vs. integrations

- Keep thin outbound clients in `integrations.md`.
- Give an integration a sub-pillar or Domain pillar when it has product behavior, lifecycle, or substantial operational policy.

Rule of thumb: would removing it change the product or merely one implementation detail?

### UI vs. CLI

`ui.md` covers visual UI. Domain `cli.md` covers terminal prompts, color, output formatting, exit codes, and scripting behavior.

### Notifications vs. email

`notifications.md` covers transactional delivery across email, SMS, and push. Domain `email.md` covers marketing and lifecycle campaigns, consent, suppression, and sending policy.

## Sub-pillar conventions

Sub-pillars live at `agents/<parent>/<name>.md`. Their path-derived identity is `<parent>/<name>`, while the frontmatter `pillar` value remains the leaf `<name>`. References to sub-pillars must use the path-qualified identity.

Sub-pillars use the same 8 sections and routing fields as top-level pillars. A sub-pillar may declare `must_read_with: [parent]` when it needs its parent. The parent is not auto-loaded.

### Common sub-pillar patterns

| Pattern | Examples | Use when |
|---|---|---|
| Cross-cutting specialty | `security/ml`, `quality/ml`, `observe/ml` | A Domain concern changes several Core areas. |
| Multiple API surfaces | `api/storefront`, `api/admin`, `api/webhooks` | Consumers have distinct contracts. |
| Integration saturation | `integrations/algolia`, `integrations/klaviyo` | The shared integration pillar is losing focus. |
| UI depth | `ui/components`, `ui/animations`, `ui/tokens` | UI guidance has stable sub-domains. |
| Quality depth | `quality/testing`, `quality/style` | Testing or style needs focused procedures. |
| Data depth | `data/migrations`, `data/queries`, `data/multi-tenant` | Schema, query, or isolation guidance stands alone. |
| Decision depth | `arch/decisions`, `stack/decisions` | Rationale has enough volume or churn that a flat `Decisions` section stops being readable, or superseded choices need to stay on the record. |

## Archetype starter exclusions

Find your project type and use the right column as a starting point for what to mark as not applicable. These are suggestions, not requirements, and you can change your mind later.

| Archetype | Typical exclusions |
|---|---|
| CLI tool | ui, api, auth, deploy, observe, i18n, a11y, analytics, async, cache, notifications |
| Internal API service | ui, a11y, seo if no user surface, notifications if no end users |
| ML pipeline | ui, i18n, a11y, notifications, analytics |
| Marketing site | data, api, auth if no users, observe if platform-provided, async |
| Mobile app | seo, i18n if single-locale, realtime if not collaborative |
| Open-source library | ui, api if not a service, auth, observe, deploy if not hosted, notifications, analytics |
| SaaS dashboard | none initially |
| Empty or greenfield | none initially |

Record reasons in `AGENTS.md` so future contributors can distinguish deliberate exclusions from forgotten work.

## Naming and maturity

- Top-level identity: `<name>` at `agents/<name>.md`.
- Sub-pillar identity: `<parent>/<name>` at `agents/<parent>/<name>.md`.
- Identity segments are lowercase nouns or noun phrases with optional internal hyphens.
- Frontmatter `pillar` matches the file's leaf name.
- A pillar can remain partially populated indefinitely. Empty sections use `(none)`.
