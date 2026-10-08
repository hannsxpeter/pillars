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

This pillar covers Northstar CRM's product identity, domain terms, and invariants. It does not cover file layout (`repo.md`), data model details (`data.md`), or authentication and authorization rules (`auth.md`).

## Context

Northstar CRM is a multi-tenant B2B dashboard for account teams. Users manage accounts, contacts, notes, tasks, and team membership inside a workspace.

**Glossary:**

- **Workspace:** a tenant. Every customer organization has one workspace.
- **Member:** a user inside a workspace.
- **Owner:** the member role that can manage invites, workspace settings, and destructive actions.
- **Account:** a customer or prospect company tracked by the sales team.
- **Contact:** a person associated with an account.

**Product invariants:**

- A user can belong to multiple workspaces.
- Workspace data must never leak across tenants.
- Account and contact records are workspace-scoped.
- Membership role is scoped to a workspace, not to the global user.

## Decisions

- **Workspace over tenant in UI copy.** Reason: customers understand "workspace"; engineers still use `tenant_id` in the database because it is concise and conventional.
- **One active workspace per session.** Reason: most workflows happen inside a single customer organization; switching workspace is explicit.

## Rules

(none)

## Workflows

(none)

## Watchouts

- **Do not treat a user's email domain as tenant identity.** Some customers use consultants and shared domains. Workspace membership is the source of truth.

## Touchpoints

- `see_also: [repo]`: most implementation tasks also need file layout.

## Gaps

- Enterprise workspace hierarchy is undecided. Do not invent parent-child workspace behavior.
