# Pillars Author Prompt

Paste this entire file into your AI coding tool's chat to draft or revise a specific Pillars pillar from your codebase. Works in any tool: Claude Code, Cursor, Codex CLI, Gemini CLI, opencode, Aider, Windsurf, Cline, Continue, Pieces, etc.

Tell the AI which pillar to author at the end of this prompt (e.g., "Author the `data` pillar").

For installation as a native command/skill in specific tools, see the relevant install doc in this folder.

---

## Task: author a specific Pillars pillar from this codebase

You are going to draft (or revise) a specific [Pillars](https://github.com/hannsxpeter/pillars) pillar by scanning the relevant code in this project and presenting a faithful 8-section pillar body for the user's approval before writing.

### Step 1 — Determine which pillar

The user named a pillar. Confirm it's a valid one from the [Pillars catalog](https://github.com/hannsxpeter/pillars/blob/v1.2.0/PILLARS.md):

- Always-loaded: `context`, `repo`
- Core: `stack`, `arch`, `data`, `api`, `ui`, `auth`, `quality`, `development`, `release`, `deploy`, `observe`
- Common: `config`, `security`, `privacy`, `compliance`, `i18n`, `a11y`, `analytics`, `integrations`, `async`, `cache`, `notifications`
- Domain (examples): `ml`, `realtime`, `payments`, `billing`, `tenancy`, `reliability`, `performance`, `infrastructure`, `documentation`, `email`, `search`, `mobile`, `state`, `forms`, `validation`, `seo`, `cli`
- Sub-pillar form: `<parent>/<name>` (e.g., `data/multi-tenant`)

If the user's pillar isn't on this list and isn't an obvious domain pillar, ask them to confirm before proceeding.

### Step 2 — Check if the pillar already exists

```
ls agents/<pillar>.md
```

- If absent: this is a *create* operation.
- If present and `status: stub`: this is a *populate* operation. Preserve frontmatter; fill sections.
- If present and `status: present`: this is a *revise* operation. Tell the user. Ask whether they want to (a) merge (preserve existing Decisions/Watchouts), (b) overwrite, or (c) abort. Default to merge.

### Step 3 — Scan the relevant code

Each pillar has typical scan areas. Use this table:

| Pillar | Scan paths (typical) | Config files | What to look for |
|---|---|---|---|
| context | `README.md`, `package.json` description, recent commits | `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod` | Project name, purpose, target users, domain vocabulary |
| repo | Top-level directory tree, `.editorconfig`, build config paths | tsconfig, vite, build configs | Folder layout, file naming, where things go |
| stack | `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, lockfiles | All dep manifests | Languages, frameworks, ORMs, build tools |
| arch | `src/`, `apps/`, `services/`, `packages/` tops, `docker-compose`, infra | docker-compose.yml, terraform/, k8s | Services, modules, boundaries, data flow |
| data | `src/db/`, `prisma/`, `drizzle/`, `migrations/`, `schema/`, `models/` | ORM config | Schema, migrations, query patterns |
| api | `src/api/`, `routes/`, `pages/api/`, `app/api/`, OpenAPI specs | API framework config | Endpoint shapes, versioning, request/response |
| ui | `src/components/`, `src/ui/`, `app/`, `pages/`, design tokens | Tailwind/CSS config | Component conventions, design system |
| auth | `src/auth/`, `middleware/auth*`, identity provider config | next-auth, better-auth, OAuth env vars | Identity flow, sessions, roles |
| quality | `tests/`, `__tests__/`, `*.test.*`, `*.spec.*`, lint/format config | eslint, prettier, biome, vitest, jest | Testing, style, error patterns |
| development | setup docs, scripts, dev containers, generators | task runners, editor config | Local setup, inner loop, debugging |
| release | changelog, tags, publishing workflows | package metadata, release automation | Versioning, release gates, publication |
| deploy | `Dockerfile`, `Procfile`, `.github/workflows/`, `vercel.json`, `netlify.toml` | CI configs, IaC | Cutover, environments, rollback |
| observe | logging setup, metrics setup, error tracking init | OpenTelemetry, Sentry, Datadog | Logging, metrics, alerts |
| config | `.env*`, `config/`, feature flag init, `app.config*` | env example, config schema | Env vars, feature flags, secrets handling |
| security | `middleware/`, validation libs, audit configs | dependabot.yml, security policies | Input validation, CSRF/CORS, dep scanning |
| privacy | data inventory, retention jobs, consent and deletion flows | privacy policy, data maps | Personal data, purpose, retention, rights |
| integrations | SDK imports, webhook handlers | API key env vars | Third-party services, contracts |
| async | `jobs/`, `workers/`, `queue/`, cron | BullMQ, Sidekiq, Celery configs | Background work, retries |
| cache | Redis init, in-memory cache, CDN config | TTL constants | Strategy, invalidation |
| notifications | email templates, SMS service, push setup | Resend, SendGrid, Twilio config | Transactional patterns |

For Domain pillars, use judgment to identify relevant code. For sub-pillars, scan within the parent's territory. Use path-derived identities in references: `agents/auth/agent-registration.md` has `pillar: agent-registration` but is referenced as `auth/agent-registration`.

### Step 4 — Draft the 8 sections

Apply the "earn your keep" principle: populate a section only when it adds value the others don't.

**Scope** (always): one paragraph. What this pillar covers, what it does NOT. Reference boundary calls from [PILLARS.md](https://github.com/hannsxpeter/pillars/blob/v1.2.0/PILLARS.md).

**Context** (always): declarative facts. The bulk of the pillar.
- Stack/library choices visible in code.
- File locations.
- Naming conventions.
- Top-level invariants.
- Minimal directory tree if helpful.
- Tiny inline code shapes when they ground the convention.

**Decisions** (optional): non-obvious choices and *why*. Skip if reasoning isn't visible in code/comments/user input. Do NOT fabricate.

**Rules** (optional, sparing): hard constraints not inferable from Context. Examples: "Never raw SQL outside `src/db/raw.ts`." If you don't see a clear non-inferable constraint, leave as `(none)`.

**Workflows** (optional): multi-step procedures not obvious from Context. Skip if the procedure is obvious.

**Watchouts** (optional): soft warnings *with reasoning*. Only include with evidence of historical pain (TODO comments, defensive code, bug-related patterns). If none, leave as `(none)`.

**Touchpoints** (always): mirror frontmatter `must_read_with` and `see_also` in plain English with reasons.

**Gaps** (always for fresh pillars): explicit "not decided yet" entries. Surface unknowns rather than inferring them.

### Step 5 — Draft the frontmatter

```yaml
---
pillar: <name>
status: present  # or "stub" if explicitly requested
always_load: false  # true only for context and repo
covers: [...]
triggers: [keyword1, keyword2, ...]
must_read_with: []  # max 3 entries; more is a boundary smell
see_also: []
---
```

Keep always-loaded pillars at or below 1,000 words and 8 KiB. Keep task-routed pillars at or below 2,000 words and 16 KiB unless the project documents a justified exception.

### Step 6 — Present the draft

**Never write the file without user approval.** Show the draft in chat:

```
Draft for agents/<pillar>.md:

---
<frontmatter>
---

<body>
```

Ask:

> Approve to write? Or want me to revise specific sections first?

If revisions requested, iterate.

### Step 7 — Write on approval

Write to `agents/<pillar>.md` (or `agents/<parent>/<name>.md` for sub-pillars). If revising an existing pillar, preserve existing Decisions and Watchouts content when merging. Remove the same identity from `agents/catalog.yaml` when the new pillar replaces a locally cataloged absence.

After writing:

```
Wrote agents/<pillar>.md.

Sections populated: <list>
Sections marked (none): <list>
Gaps to revisit: <list>

The agent will load this pillar when triggered by: <list triggers>.
```

### Step 8 — Suggest related pillars

If authoring this pillar surfaced concepts belonging in another pillar (e.g., authoring `data.md` revealed multi-tenancy concerns), suggest:

> While authoring this, I noticed <concept>. That likely belongs in `<other-pillar>.md`. Want me to author that next?

---

## Constraints

- Do NOT write files without user approval.
- Do NOT fabricate Decisions or Watchouts. Surface gaps instead.
- Do NOT exceed the 8-section template.
- Do NOT modify other pillar bodies in this invocation. Removing the authored identity from `agents/catalog.yaml` is required metadata cleanup.
- Do NOT modify AGENTS.md (use `pillars-init` for that).
- Do NOT populate Rules with content inferable from Context.

## Common failure modes to avoid

- **Over-populating Rules.** When in doubt, leave Rules empty.
- **Inventing Decisions.** If the why isn't visible, note in Gaps.
- **Pillar boundary creep.** If you find yourself writing auth content in `data.md`, stop. Cross-reference in Touchpoints; don't duplicate.

---

## Reference

- Pillars standard: https://github.com/hannsxpeter/pillars
- SPEC.md: https://github.com/hannsxpeter/pillars/blob/v1.2.0/SPEC.md
- PILLARS.md: https://github.com/hannsxpeter/pillars/blob/v1.2.0/PILLARS.md
- Worked examples: https://github.com/hannsxpeter/pillars/tree/v1.2.0/examples

---

## Now: author the following pillar

**Pillar to author:** _<replace this line with the pillar name, e.g., `data` or `auth` or `data/multi-tenant`>_
