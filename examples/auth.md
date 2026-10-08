---
pillar: auth
status: present
always_load: false
covers: [identity, sessions, authentication, authorization, role-based access]
triggers: [auth, login, logout, session, signin, signup, role, permission, access, jwt, oauth, user, tenant]
must_read_with: [data, config]
see_also: [security, api]
---

> This is a **worked example** of an `auth.md` pillar for an adopter to reference. It illustrates a typical Better-Auth + role-based setup with multi-tenant scoping. Replace this content with your project's actual conventions when adopting.

## Scope

This pillar covers identity, sessions, and access decisions: how users authenticate, how sessions are represented, how roles and permissions are checked. It does not cover secrets storage (that's `config.md`) or adversarial threats beyond auth (that's `security.md`).

## Context

The project uses **Better-Auth** for authentication, backed by the same Postgres instance used for application data (see `data.md`). Sessions are stored server-side; the client holds an opaque session cookie.

**File layout:**

```
src/auth/
├── config.ts          # Better-Auth configuration
├── middleware.ts      # session validation, request enrichment
├── permissions.ts     # role definitions and permission checks
└── providers.ts       # OAuth provider setup (Google, GitHub)
```

**Identity model:**

- A `users` table holds account-level identity (email, password hash, OAuth identity).
- A `memberships` table joins users to tenants with a role (`owner`, `admin`, `member`, `viewer`).
- A user can belong to multiple tenants; the current tenant is part of the session.

**Session shape (server-side):**

- `userId`: the authenticated user.
- `tenantId`: the active tenant for this session.
- `role`: the user's role in the active tenant.
- `expiresAt`: 30-day sliding window, rotated on every request.

**Permission model:**

- Permissions are checked at the controller/handler boundary, never inside the data layer.
- Permission check signature: `can(session, action, resource)` returning a boolean.
- Action names follow `<verb>:<resource>` (e.g., `read:document`, `delete:user`).

## Decisions

- **Better-Auth over Auth.js / Clerk / Auth0.** Reason: self-hosted (no external dependency), Postgres-native (no extra service), supports both email/password and OAuth in one library.
- **Server-side sessions, not JWT.** Reason: revocation is a primary requirement (admin-triggered logout, tenant deactivation). JWTs make revocation hard.
- **Role on the membership, not on the user.** Reason: same person can be `admin` in one tenant and `viewer` in another. Roles are scoped to the tenant.
- **Permission checks at the handler boundary.** Reason: keeps the data layer ignorant of auth; testable in isolation; enforces a single place where access decisions happen.

## Rules

- **Never make a data query that bypasses `tenantId` scoping for tenant-scoped resources.** The session's `tenantId` must filter every query that touches a `tenant_id` column. See `data.md` for the multi-tenant schema rules.
- **Never check permissions inside data-layer functions.** Permission checks live at the handler. Data-layer functions assume the caller has authorized; they don't re-check.
- **Never store the password hash anywhere outside the `users` table.** No logging, no analytics, no error reports.
- **Always rotate the session on permission elevation** (e.g., user accepts an admin invite). Old session is invalidated; client receives a new cookie.

## Workflows

- **Adding a new permission:**
  1. Define the action name in `src/auth/permissions.ts` (`<verb>:<resource>`).
  2. Add it to the relevant role(s) in the role-permission map.
  3. Call `can(session, action, resource)` at the handler boundary.
  4. Add a test for both the allowed and denied paths.

- **Adding an OAuth provider:**
  1. Register the app with the provider; store credentials in environment via `config.md`'s conventions.
  2. Add the provider config to `src/auth/providers.ts`.
  3. Update the sign-in UI to include the provider button.
  4. Test the full round-trip in a staging environment before merging.

## Watchouts

- **Cross-tenant data leaks are the #1 risk.** Any query that returns tenant-scoped rows must include `tenant_id` filtering. A bug here is a security incident. Pair this pillar with `data/multi-tenant.md` whenever touching tenant-scoped code.
- **Don't lengthen session expiry to "fix" logout complaints.** The 30-day sliding window is intentional. Real fix: investigate why sessions are dropping prematurely (usually a cookie domain/path issue).
- **Better-Auth's email verification flow has a known UX gap on slow inboxes.** Users get the verification email but click before the row hits the DB. The retry path is handled but worth flagging when debugging "I clicked the link and it said expired."

## Touchpoints

- `must_read_with: [data, config]`: auth queries the `users` and `memberships` tables (data); session secrets and provider credentials live in config.
- `see_also: [security, api]`: security covers non-auth adversarial concerns (rate limiting, brute force); api covers how handlers consume session state.

## Gaps

- **SSO/SAML support** is not implemented. Will be required by some enterprise customers; design is undecided.
- **Audit log retention** for auth events (logins, role changes) is not policy-defined. Currently retained indefinitely; needs a retention rule that satisfies compliance (see `compliance.md` if present).
