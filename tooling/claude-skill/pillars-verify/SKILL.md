---
name: pillars-verify
description: "Audit the current project's Pillars files against the actual codebase. Walks each pillar's Context section, checks whether its declarative claims (stack, file locations, conventions, decisions) still match the code, flags drift, and proposes specific fixes for each finding. Use this skill when the user asks to 'verify pillars,' 'check pillars for drift,' 'audit pillars,' 'are my pillars up to date,' 'check if my pillars match the code,' or after a significant refactor when they want to confirm the pillars still reflect reality."
version: 0.2.0
updated: 2026-07-13
compatible_with:
  - claude-code
standard_version: ">=1.1.0"
---

# Pillars Verify

This skill audits the project's pillar files against the current state of the codebase. It walks each pillar's Context section, checks claims, and flags drift with specific evidence.

## When to use this skill

Trigger when the user wants to check whether their pillars are still accurate. Typical requests:

- "Verify the pillars."
- "Check if my pillars are still accurate."
- "Audit the pillars against the codebase."
- "Are my pillars out of date?"
- "I just did a big refactor; check the pillars."

If the user wants to *bootstrap* Pillars, prefer `pillars-init`. If they want to *author or rewrite a specific pillar*, prefer `pillars-author`.

## What this skill produces

A structured drift report in the chat (no files written by default). For each pillar:

- Claims checked
- Drift findings (if any), with the specific evidence in code
- Proposed fixes for each finding
- Suggested next action

After presenting the report, the user can decide which findings to address and (optionally) invoke `pillars-author` to refresh a specific pillar.

## Procedure

### Step 1. Locate the project's scopes and pillars

Check the standard locations:

```bash
ls AGENTS.md agents/
```

If either is missing, tell the user: "This project doesn't appear to have Pillars set up. Run `/pillars-init` first." End.

Also find nested directories containing both `AGENTS.md` and `agents/`. Verify each scope independently and apply nearest-scope precedence when claims conflict. Read each scope's exclusions and optional `agents/catalog.yaml`. Exclusions are intentional. Catalog entries are known absences, not pillar claims.

### Step 2. Inventory the pillar files

For each file in `agents/` (and `agents/**` for sub-pillars):

- Parse the YAML frontmatter.
- Note `pillar`, `status`, `always_load`, and `covers`.
- If `status: stub`, skip drift checks (stubs don't claim anything to drift from).
- If `status: present`, proceed to checks.

### Step 3. For each present pillar, run the drift checks

The check strategy is *evidence-driven*. For each declarative claim in the Context section, verify against code. Use this priority:

#### 3a. Stack/dependency claims (highest priority)

Claims like "We use Drizzle ORM," "Postgres 16," "Better-Auth," "Next.js 15."

Check against:
- `package.json` `dependencies` and `devDependencies`
- `pyproject.toml` `dependencies`
- `Cargo.toml` `[dependencies]`
- `go.mod`
- Other lockfiles

Drift example:
- Claim (in `data.md` Context): "We use Drizzle ORM."
- Evidence: `package.json` has `prisma` but no `drizzle-orm`.
- Finding: **drift** — declared Drizzle, code uses Prisma.

#### 3b. File-location claims

Claims like "Schema lives in `src/db/schema.ts`," "Routes under `src/api/v2/`."

Check by listing the actual paths:

```bash
ls src/db/ 2>/dev/null
ls src/api/ 2>/dev/null
find . -name "schema.ts" -not -path "*/node_modules/*"
```

Drift example:
- Claim (in `data.md`): "Schema in `src/db/schema.ts`."
- Evidence: file doesn't exist; found `app/lib/db/schema.ts` instead.
- Finding: **drift** — declared `src/db/schema.ts`, actual `app/lib/db/schema.ts`.

#### 3c. Convention claims

Claims like "Table names are plural snake_case," "Test files use `*.test.ts`."

Sample-check 3-5 representative files. If the convention holds in the sample, treat as confirmed. If it fails in 2+ of 5, flag drift with examples.

#### 3d. Architecture claims

Claims like "Three services: api, worker, web," "Multi-tenant via `tenant_id` column."

Check structural evidence:
- Top-level directories matching declared services.
- For multi-tenancy, sample-check tenant-scoped tables for `tenant_id` columns.

#### 3e. Decision-section claims (medium priority)

Decisions are often historical. Check whether the rationale still holds. Example: a Decision says "We picked Drizzle because we need raw SQL escape hatches." If the code now never uses raw SQL, the decision still holds (the option was retained); not drift.

But if the Decision says "We chose Postgres over SQLite for write throughput" and the code shows the project switched to SQLite, *that's drift*.

#### 3f. Rules claims (medium priority)

Rules are constraints. Sample-check whether they're being followed in code.

Drift example:
- Rule (in `data.md`): "Never write raw SQL outside `src/db/raw.ts`."
- Evidence: found `postgres.unsafe(...)` calls in `src/api/v2/reports.ts`.
- Finding: **rule violation** — code violates the declared rule. Worth flagging even though it's not strictly pillar drift; the agent should know.

### Step 4. Compile findings

Structure findings per pillar. Use this format:

```
## <pillar>.md

Claims checked: N
Findings: M

### Finding 1: <short title>
- **Claim:** <quoted from pillar>
- **Evidence:** <what you found in the code>
- **Severity:** drift | rule violation | minor
- **Proposed fix:** <specific change to make to the pillar, OR to the code if the pillar is correct>

### Finding 2: ...
```

If no findings, say so explicitly: "No drift detected for `<pillar>.md`."

### Step 5. Surface global patterns

Beyond per-pillar findings, look for cross-cutting issues:

- **A pillar claims a tech the project doesn't have.** Likely the pillar is stale (project migrated away).
- **The project uses a tech no pillar mentions.** Likely a new pillar is needed, or an existing pillar's Context needs the addition.
- **Excluded pillars now have code in their area.** Example: `excluded: [ui]` but the project now has a `src/components/` directory. The exclusion may need to be removed and `ui.md` authored.

### Step 6. Present the report

Format:

```
# Pillars Drift Report

Project: <name from context.md>
Pillars scanned: N across S scopes (M present, K stubs, L excluded, A cataloged absent)
Findings: <total drift count>

<per-pillar findings>

## Global observations

<cross-cutting issues>

## Suggested next actions

1. Refresh <pillar>.md to fix <N> drift findings. Run `/pillars-author <pillar>`.
2. Author <new-pillar>.md to capture <evidence>. Run `/pillars-author <pillar>`.
3. Investigate rule violation in <file>: <rule>.
4. ...
```

Ask the user which findings they want to act on. Do not auto-fix.

### Step 7. (Optional) Hand off to other skills

If the user picks a specific finding to address:

- For drift in a Context section: route to `pillars-author <pillar>` for revision.
- For a new pillar needed: route to `pillars-author <new-pillar>`.
- For a rule violation in code: this isn't a Pillars action; tell the user the code change is theirs to make, optionally with agent help in a separate turn.

## What this skill does NOT do

- **Does not auto-fix anything.** Findings are presented; fixes are user-approved actions through `pillars-author` or direct code edits.
- **Does not write files.** No filesystem modifications.
- **Does not call external APIs.** All checks use local file reads and grep-style scans.
- **Does not flag stylistic differences as drift.** "We use camelCase" vs. "we mostly use camelCase but have some snake_case in legacy code" is not a finding unless the pillar declared a hard rule.
- **Does not check Watchouts.** Watchouts are historical pain points; they aren't drift candidates. The pain may have been mitigated, but the warning still has value as context.

## Common failure modes

- **False positives from imprecise claims.** If a pillar's Context says "We use Postgres" and the code has both Postgres and Redis, that's not drift (Redis is a cache layer). Read claims carefully; treat them as the most natural interpretation.
- **Stubs treated as drift.** Stubs claim nothing. Skip them. The stub itself is a pending action, surfaced separately if the user wants.
- **Excluded pillars as gaps.** Exclusions are intentional. Don't flag absence of `ui.md` as drift when `ui` is in the exclusion list. Do flag if the code shows UI surface despite the exclusion (covered in Step 5).
- **Over-confident drift on weakly-evidenced claims.** If a pillar says "Components live in `src/ui/`" and the project has 2 files in `src/ui/` plus 30 in `src/components/`, that's drift. If it's 30 vs. 2 the other way, the pillar is still right. Use sample sizes when judging.

## Scope limits

- **No CI/CD integration.** This is a manual, in-session audit. A CLI form of this check would belong in CI; see the Pillars roadmap for that future direction.
- **No autonomous remediation.** Findings are presented; user decides what to act on.
- **No cross-project drift detection.** Operates on the current project only.

## Reference

- Pillars standard: https://github.com/hannsxpeter/pillars
- SPEC.md: https://github.com/hannsxpeter/pillars/blob/v1.2.0/SPEC.md
- PILLARS.md: https://github.com/hannsxpeter/pillars/blob/v1.2.0/PILLARS.md
