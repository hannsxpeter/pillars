# SaaS Dashboard Adoption Example

This folder is a compact end-to-end example of Pillars in a fictional SaaS dashboard project called Northstar CRM. It is not a template to copy byte-for-byte. It shows how a real adoption feels once `AGENTS.md` and several pillars work together.

## Project Snapshot

Northstar CRM is a multi-tenant B2B dashboard for account teams. It uses Next.js, Postgres, Drizzle, Better-Auth, and Vercel. The example includes the minimum set of files needed to demonstrate the runtime loop:

```text
saas-dashboard/
├── AGENTS.md
└── agents/
    ├── context.md
    ├── repo.md
    ├── catalog.yaml
    ├── auth.md
    └── data.md
```

## What This Demonstrates

- Always-loaded pillars: `context.md` and `repo.md`.
- Task-routed pillars: `auth.md` and `data.md`.
- Depth-1 `must_read_with`: auth and data load together because tenant isolation spans both.
- `see_also` as a soft hint, not an automatic chain walk.
- Local `catalog.yaml` discovery for relevant concerns that have no pillar yet.
- Gaps that tell the agent when to ask instead of inventing a policy.

## Before And After

Before Pillars, an agent asked to add "team invite links" might:

- Put invite state in a generic `users` table because it saw user records first.
- Skip tenant scoping on the invite lookup.
- Add permission checks inside a database helper because it seemed locally convenient.

After Pillars, the same task loads:

- `context.md` for product language: tenant, workspace, account team.
- `repo.md` for where route handlers and database helpers live.
- `auth.md` because the task mentions invites, users, roles, and permissions.
- `data.md` through `auth.md`'s `must_read_with`, because invite state is tenant-scoped data.

The agent now sees that permissions belong at the route boundary, tenant-scoped tables carry `tenant_id`, and unresolved SSO policy is a gap to ask about.

## Where design.md Fits

If Northstar CRM had a root `design.md`, it would hold the richer product story: target users, account-team journeys, navigation rationale, and UX tradeoffs. The pillars would not duplicate that whole narrative. They would summarize only the durable implementation guidance agents need during tasks.

For example:

| `design.md` content | Pillars destination |
|---|---|
| Account-team workflow narrative | `context.md` summary of product language and invariants |
| Workspace switcher UX rationale | `ui.md` if present, or a gap until UI rules are authored |
| Owner-only invite journey | `auth.md` rules and workflow |
| Tenant isolation experience | `data.md` and `auth.md` constraints |

Use `pillars-sync-design.md` to compare both directions. It reports proposed updates from `design.md` into pillars and from pillars back into `design.md`, but it does not write files.

## Useful Maintenance Prompts

This example is small, but the report-only prompts show how an adopter would maintain it:

| Prompt | Example use |
|---|---|
| `pillars-map-task.md` | Map "Add an owner-only team invite link" to `context`, `repo`, `auth`, and `data` |
| `pillars-find-gaps.md` | Surface SSO, background job layout, and soft-delete policy as open questions |
| `pillars-trim.md` | Check whether `auth.md` and `data.md` duplicate tenant-scoping guidance |
| `pillars-sync-readme.md` | Compare the public README for Northstar CRM with `context.md` and `repo.md` |
| `pillars-sync-prd.md` | Compare a product requirements doc for team invites with `auth.md` and `data.md` |

## Example Task Routing

These rows are checked in CI against the portable minimum matcher (see `tooling/conformance/fixtures.yaml`). The matcher does not stem words, which is why the catalog lists both `page` and `pages`.

| Task | Primary pillars | Additional load |
|---|---|---|
| "Add an owner-only team invite link" | `auth` | `data` via `must_read_with`; `repo` and `context` always load |
| "Add a `last_contacted_at` column to accounts" | `data` | `auth` via `must_read_with`; `repo` and `context` always load |
| "Move account pages into a new route group" | none present | `repo` and `context` always load; the local catalog reports absent `ui` |

## Why It Is Small

This example intentionally stops before a full production pillar set. A real SaaS dashboard would likely add `stack.md`, `api.md`, `ui.md`, `quality.md`, `development.md`, `release.md`, `deploy.md`, `observe.md`, `config.md`, `security.md`, and `privacy.md`. The goal here is to show the end-to-end loading behavior without drowning the reader in a fake application.
