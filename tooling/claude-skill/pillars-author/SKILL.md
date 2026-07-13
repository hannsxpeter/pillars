---
name: pillars-author
description: "Draft or revise a specific Pillars pillar file by scanning the relevant code, decisions, and conventions in the current project. Given a pillar name (e.g., data, auth, api, ui, stack, arch), this skill performs targeted archaeology on the codebase, drafts the 8-section pillar body following the Pillars template, includes proper YAML frontmatter, and presents the draft for the user's approval before writing. Use this skill when the user asks to 'author pillar X,' 'draft data.md,' 'create the auth.md pillar,' 'generate pillar from code,' 'fill in pillar X,' 'populate context.md,' or names a specific pillar they want filled in."
version: 0.2.0
updated: 2026-07-13
compatible_with:
  - claude-code
standard_version: ">=1.1.0"
---

# Pillars Author

This skill drafts a specific Pillars pillar by scanning the relevant code and presenting a faithful 8-section body for the user to approve.

## When to use this skill

Trigger when the user wants a *specific* pillar drafted or revised, with the pillar name given. Typical requests:

- "Author the data.md pillar from my codebase."
- "Draft auth.md."
- "Fill in stack.md."
- "Populate context.md from the project description."
- "Create the api.md pillar."

If the user wants to *scaffold the whole standard*, prefer `pillars-init`. If they want to *check pillars for drift*, prefer `pillars-verify`.

## What this skill produces

A complete pillar file at `agents/<pillar>.md` (or sub-pillar at `agents/<parent>/<name>.md`) with:

- Correct YAML frontmatter (pillar, status, always_load, covers, triggers, must_read_with, see_also).
- 8 body sections (Scope, Context, Decisions, Rules, Workflows, Watchouts, Touchpoints, Gaps).
- `status: present` once content is meaningful; `status: stub` only if the user explicitly wants a stub.
- Sections populated only where they earn their keep (per Pillars' "earn your keep" principle).

## Procedure

### Step 1. Determine which pillar to author

Get the pillar name from the user's request. If ambiguous, ask. Acceptable names are any from the [Pillars catalog](https://github.com/hannsxpeter/pillars/blob/v1.1.0/PILLARS.md):

- Always-loaded: `context`, `repo`
- Core: `stack`, `arch`, `data`, `api`, `ui`, `auth`, `quality`, `development`, `release`, `deploy`, `observe`
- Common: `config`, `security`, `privacy`, `compliance`, `i18n`, `a11y`, `analytics`, `integrations`, `async`, `cache`, `notifications`
- Domain (open): `ml`, `realtime`, `payments`, `billing`, `tenancy`, `reliability`, `performance`, `infrastructure`, `documentation`, `email`, `search`, `mobile`, `state`, `forms`, `validation`, `seo`, `cli`, or project-specific.
- Sub-pillars: same names with a parent path (e.g., `data/multi-tenant`).

If the name isn't in the catalog and isn't an obvious domain pillar, ask the user to confirm before proceeding.

### Step 2. Confirm whether to update or create

Check if the pillar already exists at `agents/<pillar>.md`.

- If absent: this is a *create* operation.
- If present and `status: stub`: this is a *populate* operation. Preserve frontmatter; fill in sections.
- If present and `status: present`: this is a *revise* operation. Tell the user; ask whether they want to (a) merge new content with existing (preserving Decisions/Watchouts history), (b) overwrite, or (c) abort. Default to merge.

### Step 3. Scan the relevant code

Each pillar has a typical scan area. Use this table to focus archaeology:

| Pillar | Scan paths (typical) | Config files | What to look for |
|---|---|---|---|
| context | `README.md`, `package.json` description, recent commits | `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod` | Project name, purpose, target users, domain vocabulary |
| repo | Top-level directory tree, `.editorconfig`, `tsconfig.json`/`vite.config`/`vite.config.ts` paths | Build configs that imply structure | Folder layout, file naming patterns, where things go |
| stack | `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, lockfiles | All dependency manifests | Languages, frameworks, ORMs, build tools, deploy targets |
| arch | `src/`, `apps/`, `services/`, `packages/` top levels, `docker-compose`, infra configs | `docker-compose.yml`, `terraform/`, k8s manifests | Services, modules, boundaries, data flow |
| data | `src/db/`, `prisma/`, `drizzle/`, `migrations/`, `schema/`, `models/` | ORM config | Schema, migrations, query patterns |
| api | `src/api/`, `routes/`, `pages/api/`, `app/api/`, OpenAPI specs | API framework config | Endpoint shapes, versioning, request/response patterns |
| ui | `src/components/`, `src/ui/`, `app/`, `pages/`, design tokens | Tailwind/CSS config, component library | Component conventions, design system, theming |
| auth | `src/auth/`, `middleware/auth*`, identity provider config | `next-auth.config`, `better-auth.config`, OAuth env vars | Identity flow, sessions, roles, permissions |
| quality | `tests/`, `__tests__/`, `*.test.*`, `*.spec.*`, lint config, format config | `eslint`, `prettier`, `biome`, `vitest`, `jest` configs | Testing strategy, style rules, error patterns |
| development | setup docs, scripts, dev containers, generators | task runners, editor config | Local setup, inner loop, debugging |
| release | changelog, tags, publishing workflows | package metadata, release automation | Versioning, release gates, publication |
| deploy | `Dockerfile`, `Procfile`, `.github/workflows/`, `vercel.json`, `netlify.toml` | CI configs, IaC | Cutover strategy, environments, rollback approach |
| observe | logging setup, metrics setup, error tracking init, runbook docs | OpenTelemetry, Sentry, Datadog, Prometheus configs | Logging conventions, metrics emitted, alerts, runbook locations |
| config | `.env*`, `config/`, feature flag service init, `app.config*` | env example files, config schema | Env vars, feature flags, secrets handling |
| security | `middleware/`, validation libs, dependency audit configs | `npm audit`, `dependabot.yml`, security policy | Input validation, CSRF/CORS, dep scanning |
| privacy | data inventory, retention jobs, consent and deletion flows | privacy policy, data maps | Personal data, purpose, retention, rights |
| integrations | SDK imports throughout `src/`, webhook handlers | API key env vars | Third-party services consumed, contract patterns |
| async | `jobs/`, `workers/`, `queue/`, cron config | BullMQ/Sidekiq/Celery configs | Background work patterns, retries, scheduling |
| cache | Redis init, in-memory cache code, CDN config | Cache TTL constants | Caching strategy, invalidation patterns |
| notifications | email templates, SMS service init, push setup | Resend/SendGrid/Twilio config | Transactional patterns, templates, channels |
| analytics | event tracker init, KPI dashboards | PostHog/Mixpanel/Amplitude config | Event taxonomy, dashboards |
| i18n | `locales/`, `i18n/`, translation files | i18next/`next-intl`/Lingui config | Locales supported, RTL, formatters |
| a11y | aria attributes throughout components, a11y testing setup | axe-core or Pa11y configs | WCAG patterns, screen reader conventions |
| compliance | data retention configs, audit log setup, GDPR/HIPAA-relevant comments | privacy policy in repo | Regulatory mapping if any |

For Domain pillars (Tier 3), use your judgment to identify the relevant code. For sub-pillars, scan within the parent's territory. Use path-derived identities in references: `agents/auth/agent-registration.md` has `pillar: agent-registration` but is referenced as `auth/agent-registration`.

### Step 4. Draft the 8 sections

Follow the [Pillars template](https://github.com/hannsxpeter/pillars/blob/v1.1.0/SPEC.md). Earn-your-keep principle: only populate a section when it adds value the others don't.

**Section drafting guidance:**

- **Scope:** one paragraph. What this pillar covers and what it explicitly does *not*. Reference the boundary calls from PILLARS.md where relevant (e.g., for `data.md`, note "queries to the DB live here; API contracts live in `api.md`").

- **Context:** declarative facts. The bulk of the pillar. Include:
  - The stack choices visible in code (frameworks, ORMs, libraries).
  - File locations (where things go).
  - Naming conventions.
  - Top-level invariants.
  - A minimal directory tree if helpful.
  - Inline tiny code shapes where they ground the convention.

- **Decisions:** non-obvious choices and *why*. Only include when the why isn't obvious from Context. Examples: "We picked Drizzle over Prisma because <reason>." If the reasoning isn't visible in code or comments, *ask the user* rather than fabricating.

- **Rules:** hard constraints not inferable from Context. Used *sparingly*. If you don't see a clear non-inferable constraint, leave this as `(none)`. Examples: "Never write raw SQL outside `src/db/raw.ts`."

- **Workflows:** multi-step procedures the agent might not infer. Only include when the workflow isn't obvious from Context. Example: "Adding a column: schema edit, drizzle-kit generate, drizzle-kit push, update seeds." If you don't have evidence of a real workflow, leave as `(none)`.

- **Watchouts:** soft warnings *with reasoning*. Only include when there's evidence of historical pain (TODO comments, bug-related code, defensive patterns). If none visible, leave as `(none)` and note in Gaps: "Watchouts will accumulate after first incidents."

- **Touchpoints:** mirror the frontmatter `must_read_with` and `see_also`. Plain English with reasons.

- **Gaps:** explicit "not decided yet" entries. Things the agent should ask about rather than infer. Always include at least one entry when authoring a fresh pillar from limited information.

### Step 5. Draft the frontmatter

- `pillar`: the canonical name (must match the filename).
- `status`: `present` if the body has meaningful content (>50% of sections populated); `stub` only if the user explicitly wants a stub.
- `always_load`: `true` only for `context` and `repo`. `false` for everything else.
- `covers`: array of one-line scope descriptors.
- `triggers`: keywords the agent will match against task descriptions. Be specific to avoid over-matching.
- `must_read_with`: hard dependencies on other pillars. Keep to 3 or fewer. If you list more, the boundary is wrong.
- `see_also`: soft coupling to other pillars.

Keep always-loaded pillars at or below 1,000 words and 8 KiB. Keep task-routed pillars at or below 2,000 words and 16 KiB unless the project documents a justified exception.

### Step 6. Present the draft for approval

**Never write the file without user approval.** Show the draft in chat with a clear marker:

```
Draft for agents/<pillar>.md:

---
<frontmatter>
---

<body>
```

Then explicitly ask:

> Approve to write? Or want me to revise specific sections first?

If the user asks for revisions, iterate before writing.

### Step 7. Write the file

On approval, write to the target path. Use the `Write` tool. If the file already exists (per Step 2's merge path), use `Edit` to preserve original Decisions/Watchouts content where appropriate. Remove the same identity from `agents/catalog.yaml` when the pillar replaces a locally cataloged absence.

After writing, confirm:

```
Wrote agents/<pillar>.md.

Sections populated: Scope, Context, Decisions, Touchpoints, Gaps.
Sections marked (none): Rules, Workflows, Watchouts.
Gaps to revisit: <list>

The agent will load this pillar when triggered by: <list triggers>.
```

### Step 8. Suggest related pillars

If the authored pillar mentions concepts that belong in other pillars (e.g., authoring `data.md` reveals tenant isolation concerns), suggest:

> While authoring this, I noticed <concept>. That likely belongs in `<other-pillar>.md`. Want me to author that next?

## What this skill does NOT do

- **Does not write without user approval.** Every draft is presented first.
- **Does not fabricate Decisions or Watchouts.** Reasoning that isn't visible in code or stated by the user is left out; surface as Gaps instead.
- **Does not exceed the 8-section template.** No custom sections.
- **Does not update other pillar bodies.** One pillar per invocation. Removing the authored identity from `agents/catalog.yaml` is required metadata cleanup.
- **Does not modify AGENTS.md.** Use `pillars-init` for that.

## Common failure modes

- **Over-populating Rules.** When in doubt, leave Rules empty. The principle is "include prescriptive content only when it would not be inferred from the facts." Most rules are inferable from Context.
- **Inventing Decisions.** If the codebase shows Drizzle but doesn't say why, don't invent reasoning. Note in Gaps: "Decision rationale for Drizzle choice not documented; ask the user."
- **Pillar boundary creep.** If you find yourself writing about auth in `data.md`, stop. Cross-reference auth in Touchpoints; don't duplicate content. The boundary calls in PILLARS.md are the source of truth.
- **Wrong tier.** If the requested pillar name is Tier 3 / Domain (e.g., `payments`, `ml`), follow the same procedure but expect higher `must_read_with` counts since Domain pillars often cross-cut Core pillars.

## Reference

- Pillars standard: https://github.com/hannsxpeter/pillars
- SPEC.md (template, frontmatter): https://github.com/hannsxpeter/pillars/blob/v1.1.0/SPEC.md
- PILLARS.md (catalog, boundary calls, sub-pillar patterns): https://github.com/hannsxpeter/pillars/blob/v1.1.0/PILLARS.md
- Worked examples: https://github.com/hannsxpeter/pillars/tree/v1.1.0/examples
