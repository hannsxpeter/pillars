---
pillar: agent-registration
status: present
always_load: false
covers: [agent self-registration, agent-facing auth.md protocol, scoped agent credentials, credential revocation]
triggers: [agent registration, agentic signup, agent onboarding, agent credential, agent api key, workos auth.md, id-jag, autonomous agent access]
must_read_with: [auth]
see_also: [api, security]
---

> This is a **worked example** of an `auth` sub-pillar, living at `agents/auth/agent-registration.md`. It shows how a project documents agent-facing self-registration (here, the WorkOS `auth.md` protocol) for its *coding* agent. Replace this content with your project's actual conventions when adopting. Note: the WorkOS `auth.md` described here is a runtime protocol file served at your public domain; it is unrelated to this Pillars pillar despite the shared name.

## Scope

This sub-pillar covers how autonomous agents register with this service and obtain scoped credentials: the `auth.md` protocol file we serve, the discovery and registration endpoints, the credential model, and revocation. It does not cover human authentication (that is the parent `auth.md`), secret storage (`config.md`), or the general HTTP contract (`api.md`).

## Context

The service supports **agentic registration** via the WorkOS [`auth.md`](https://github.com/workos/auth.md) protocol, so AI agents acting for a user can self-onboard without a human completing the signup UI.

- The protocol file is served at `https://api.northstar.example/auth.md` (public web root, not in this repo's source tree). It is generated from `src/agent-auth/manifest.ts`, never hand-edited.
- Discovery is two-hop: Protected Resource Metadata at `/.well-known/oauth-protected-resource` points to authorization-server metadata at `/.well-known/oauth-authorization-server`, which carries the `agent_auth` block (register, claim, and revocation URIs, plus supported identity and credential types).
- Registration, claim, and revocation handlers live in `src/agent-auth/`, mounted separately from the human auth routes in `src/auth/`.
- Agents receive a **scoped API key** (anonymous tier) or a short-lived **access token** (when identity is asserted). Credentials are stored and audited the same way human API keys are (see parent `auth.md`).

**Identity methods, in priority order:**

- `identity_assertion` with an ID-JAG token from a trusted agent provider, mapped to an existing user.
- `identity_assertion` with a verified email.
- `anonymous`, which yields a rate-limited, least-privilege API key only.

## Decisions

- **WorkOS `auth.md` over a bespoke agent-signup endpoint.** Reason: it composes existing IETF pieces (RFC 9728 Protected Resource Metadata, ID-JAG identity assertions) and gives agents a discoverable, documented flow rather than a private contract we would have to publish and support ourselves.
- **Scoped credentials per registration, never a shared key.** Reason: each registration is independently revocable and rate-limitable; a leaked credential is contained.
- **Anonymous tier is least-privilege and quota-capped.** Reason: registration with no asserted identity is the abuse surface, so it gets read-mostly scopes and a low ceiling until an identity is claimed.

## Rules

- **Agent credentials must carry an explicit, least-privilege scope set.** Never issue an agent a credential with a human session's full permissions.
- **Honor revocation on the next call.** A revoked agent credential must fail closed at the handler boundary; do not rely on token expiry alone.
- **Every registration and claim writes an audit event.** Same audit pipeline as human auth; agent actions must be attributable.
- **Do not serve the protocol file from a hand-edited markdown file.** It is generated from `manifest.ts` so the advertised endpoints and the live routes cannot drift.

## Workflows

- **Exposing a new capability to agents:**
  1. Define the scope in `src/agent-auth/scopes.ts`.
  2. Add it to the appropriate identity tier (anonymous vs. asserted) in `manifest.ts`.
  3. Regenerate and redeploy the served `auth.md` and the `agent_auth` metadata.
  4. Test the full `discover -> register -> claim -> call -> revoke` loop in staging before merging.

## Watchouts

- **ID-JAG attestation is still emerging.** Few agent providers issue trusted identity assertions today, so most real traffic lands on the email-claim or anonymous path. Design for that, not for the asserted-identity happy path.
- **The anonymous tier is the abuse vector.** Watch registration rate, per-credential quota, and claim-completion rate; a spike in unclaimed anonymous registrations usually means automated abuse.
- **Filename collision with this pillar.** The runtime `auth.md` served at the domain root and this `agents/auth/agent-registration.md` pillar are different artifacts. Keep the distinction clear in review so nobody tries to "reconcile" them.

## Touchpoints

- `must_read_with: [auth]`: agent registration issues credentials against the same user and tenant model the parent `auth.md` defines.
- `see_also: [api, security]`: api covers how handlers consume agent credentials; security covers rate limiting and the abuse model for the anonymous tier.

## Gaps

- **Which agent providers' ID-JAG assertions we trust** is undecided. Until set, asserted-identity registration is disabled and all agents use the email-claim or anonymous path.
- **Quota policy for the anonymous tier** is a placeholder. It needs a real ceiling and a claim-conversion target before agent registration leaves beta.
