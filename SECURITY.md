# Security Policy

Pillars is a documentation standard, not executable software, so its security surface is narrow. This document covers the few real concerns.

## Reporting a vulnerability

If you find a security-relevant issue in this repository or in the standard itself, please **do not open a public issue**. Instead:

1. Use GitHub's [private vulnerability reporting](https://github.com/hannsxpeter/pillars/security/advisories/new) for this repository, or
2. Contact the maintainers directly through GitHub.

You'll get an acknowledgment within a week. Coordinated disclosure timelines are negotiated case by case based on severity and impact.

## What counts as a security issue here

Pillars defines a markdown convention. The realistic concerns are:

1. **The standard recommends practices that systematically leak data.** Example: if `SPEC.md` or `PILLARS.md` advised adopters to put secrets in pillar files, that would be a serious issue. (Current standard advises the opposite; secrets live in `config.md` *with the secret materials referenced, not embedded*.)
2. **Worked examples in `examples/` contain real credentials or sensitive data.** Examples should be illustrative and entirely synthetic. If a real credential leaked into an example, please report.
3. **An adopter is misled by the standard into a vulnerable pattern.** Example: if the `auth.md` example recommends an insecure auth approach, please report so we can correct it.

## What does NOT count

- Bugs in code or services that *use* Pillars (those go to the relevant project, not here).
- Security concerns about specific AI tools that consume `AGENTS.md` (those go to the tool maker).
- Pillars in *adopting* projects that contain secrets. (Adopters' problem; the standard tells them not to.)
- Speculative attacks ("an attacker could write a malicious AGENTS.md and trick an agent"). The agent's threat model is the agent's responsibility.

## Adopter guidance

When adopting Pillars in your own project:

- **Treat pillar files like documentation.** They can be public. They should not contain secrets, API keys, tokens, passwords, private hostnames, or PII.
- **Secret *references* are fine; secret *values* are not.** A pillar can say "the database URL is in `DATABASE_URL` env var." It should not say "the database URL is `postgres://user:pass@host:5432/db`."
- **Threat modeling lives in `security.md`, not `auth.md`.** Keeping these separate clarifies who owns adversarial concerns.
- **Personal-data handling lives in `privacy.md`.** Use it for classification, purpose, consent, retention, deletion, and subject rights. Keep secret values out of every pillar.

## Disclosure history

No vulnerabilities reported to date.
