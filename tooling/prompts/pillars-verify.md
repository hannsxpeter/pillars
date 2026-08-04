# Pillars Verify Prompt

Paste this entire file into your AI coding tool's chat to audit your project's Pillars files against the current state of the code. Works in any tool: Claude Code, Cursor, Codex CLI, Gemini CLI, opencode, Aider, Windsurf, Cline, Continue, Pieces, etc.

For installation as a native command/skill in specific tools, see the relevant install doc in this folder.

---

## Task: audit Pillars against the current codebase

You are going to verify the project's [Pillars](https://github.com/hannsxpeter/pillars) files against the actual state of the code. Walk each present pillar's Context section, check claims, flag drift with evidence, and propose specific fixes.

**Do not auto-fix.** Present findings; the user decides what to act on.

### Step 1: Locate the scopes and pillars

```
ls AGENTS.md agents/
```

If either is missing:

> This project doesn't appear to have Pillars set up. Use the `pillars-init` prompt first.

End.

Also find nested directories containing both `AGENTS.md` and `agents/`. Verify each scope independently and apply nearest-scope precedence when claims conflict. Read each scope's exclusions and optional `agents/catalog.yaml`. Exclusions are intentional. Catalog entries are known absences, not pillar claims.

### Step 2 — Inventory pillar files

For each file in `agents/` (recursively for sub-pillars):

- Parse the YAML frontmatter.
- Note `pillar`, `status`, `always_load`, `covers`.
- If `status: stub`, skip drift checks (stubs claim nothing).
- If `status: present`, proceed to checks.

### Step 3 — Run drift checks per present pillar

Use evidence-driven verification. For each claim in the Context section, verify against code.

#### 3a. Stack/dependency claims (high priority)

Claims like "We use Drizzle ORM," "Postgres 16," "Better-Auth," "Next.js 15."

Check against:
- `package.json` (deps, devDeps)
- `pyproject.toml` (dependencies)
- `Cargo.toml` (`[dependencies]`)
- `go.mod`
- Other lockfiles

Drift example:
- Claim (in `data.md`): "We use Drizzle ORM."
- Evidence: `package.json` has `prisma`, no `drizzle-orm`.
- Finding: **drift** — declared Drizzle, code uses Prisma.

#### 3b. File-location claims

Claims like "Schema in `src/db/schema.ts`," "Routes under `src/api/v2/`."

Check actual paths:

```
ls src/db/ 2>/dev/null
ls src/api/ 2>/dev/null
find . -name "schema.ts" -not -path "*/node_modules/*"
```

Drift example:
- Claim: "Schema in `src/db/schema.ts`."
- Evidence: file doesn't exist; found `app/lib/db/schema.ts` instead.
- Finding: **drift**.

#### 3c. Convention claims

Claims like "Table names are plural snake_case," "Tests use `*.test.ts`."

Sample-check 3-5 representative files. If the convention holds in the sample, treat as confirmed. If it fails in 2+ of 5, flag drift with examples.

#### 3d. Architecture claims

Claims like "Three services: api, worker, web," "Multi-tenant via `tenant_id`."

Check structural evidence: top-level dirs match declared services; sample-check multi-tenant tables for `tenant_id`.

#### 3e. Decision-section claims (medium priority)

Decisions are historical. Check whether the rationale still holds. If the decision was "We chose Postgres for write throughput" and the project switched to SQLite, that's drift. If the decision was "We picked Drizzle because we need raw SQL escape hatches" and the project still uses Drizzle (even if it rarely uses raw SQL), the decision still holds; not drift.

#### 3f. Rules claims (medium priority)

Rules are constraints. Sample-check whether they're followed.

Drift example:
- Rule (in `data.md`): "Never write raw SQL outside `src/db/raw.ts`."
- Evidence: found `postgres.unsafe(...)` in `src/api/v2/reports.ts`.
- Finding: **rule violation** — code violates the declared rule.

### Step 4 — Compile findings

For each pillar with findings:

```
## <pillar>.md

Claims checked: N
Findings: M

### Finding 1: <short title>
- **Claim:** <quoted from pillar>
- **Evidence:** <what you found in the code, with file paths>
- **Severity:** drift | rule violation | minor
- **Proposed fix:** <specific change to the pillar OR to the code, depending on which is wrong>

### Finding 2: ...
```

If no findings: "No drift detected for `<pillar>.md`."

### Step 5 — Surface global patterns

Look for cross-cutting issues:

- **A pillar claims a tech the project doesn't have.** Likely a stale pillar.
- **The project uses a tech no pillar mentions.** Likely a new pillar needed, or existing pillar's Context needs the addition.
- **Excluded pillars now have code in their area.** Example: `excluded: [ui]` but the project now has `src/components/`. The exclusion may need to be removed and `ui.md` authored.

### Step 6 — Present the report

```
# Pillars Drift Report

Project: <name from context.md>
Pillars scanned: N across S scopes (M present, K stubs, L excluded, A cataloged absent)
Findings: <total>

<per-pillar findings>

## Global observations

<cross-cutting issues>

## Suggested next actions

1. Refresh <pillar>.md to fix <N> drift findings. Use the `pillars-author` prompt for `<pillar>`.
2. Author <new-pillar>.md to capture <evidence>. Use the `pillars-author` prompt.
3. Investigate rule violation in <file>: <rule>.
```

Ask the user which findings to act on. Do not auto-fix.

### Step 7 — (Optional) Hand off

If the user picks a finding to address:
- For Context drift: route them to `pillars-author <pillar>` for revision.
- For a new pillar needed: route to `pillars-author <new-pillar>`.
- For a rule violation in code: tell the user the code change is theirs to make (optionally with agent help in a separate turn).

---

## Constraints

- Do NOT auto-fix anything.
- Do NOT write or modify files.
- Do NOT flag stylistic differences as drift unless the pillar declared a hard rule.
- Do NOT treat stubs as drift; stubs claim nothing.
- Do NOT flag excluded pillars as gaps; exclusions are intentional.
- Do NOT treat catalog entries as present claims. Report only evidence that an absent concern has become load-bearing or should be excluded.

## Common failure modes to avoid

- **False positives from imprecise claims.** Read claims charitably; treat them as the most natural interpretation.
- **Over-confident drift on weak evidence.** Use sample sizes when judging conventions.
- **Treating Watchouts as drift candidates.** Watchouts are historical pain; not drift signals.

## Scope limits

- No CI/CD integration. This is a manual, in-session audit.
- No cross-project drift detection. Current project only.
- No autonomous remediation. Findings only.

---

## Reference

- Pillars standard: https://github.com/hannsxpeter/pillars
- SPEC.md: https://github.com/hannsxpeter/pillars/blob/v1.2.2/SPEC.md
- PILLARS.md: https://github.com/hannsxpeter/pillars/blob/v1.2.2/PILLARS.md

---

Now: scan the project and produce the drift report.
