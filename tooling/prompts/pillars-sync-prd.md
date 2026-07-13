# Pillars Sync PRD Prompt

Paste this entire file into your AI coding tool's chat to reconcile product requirements with a project's Pillars files. This is a report-only workflow. It does not write files.

Use this when a project has `PRD.md`, `requirements.md`, `product.md`, `spec.md`, or another product requirements document and you want to know whether the requirements and pillars agree.

---

## Task: reconcile product requirements and Pillars

You are going to compare product requirement documents with the project's [Pillars](https://github.com/hannsxpeter/pillars) files and produce a sync report. Do not write, edit, move, or delete files.

### Step 1: Locate the artifacts

Check for:

```bash
ls AGENTS.md agents/
find . -maxdepth 2 -iname "*prd*.md" -o -iname "requirements*.md" -o -iname "product*.md" -o -iname "spec*.md"
```

If `AGENTS.md` or `agents/` is missing, report:

> This project does not appear to have Pillars set up. Use `pillars-init.md` first.

If no product requirements document is found, report:

> No PRD or requirements document found. There is nothing to reconcile yet.

Then stop.

### Step 2: Load Pillars context

Follow the project's `AGENTS.md` protocol:

1. Load always-loaded pillars.
2. Inventory other pillar files in every applicable root or nested scope. Treat local catalog entries as known absences, not pillar claims.
3. For this reconciliation task, inspect relevant pillars when present:
   - `context`
   - `arch`
   - `api`
   - `ui`
   - `data`
   - `auth`
   - `quality`
   - `deploy`
   - domain pillars whose `covers` or `triggers` match the requirements.

Do not require all of these pillars to exist. Missing non-floor pillars are not errors.

### Step 3: Extract requirement claims

From the PRD or requirements document, identify:

- User stories or required workflows.
- Explicit acceptance criteria.
- Data, auth, API, UI, deployment, or observability implications.
- Nonfunctional requirements such as performance, security, availability, privacy, or accessibility.
- Open questions, assumptions, or out-of-scope items.

### Step 4: Compare against pillars

For each requirement, classify it as:

| Classification | Meaning |
|---|---|
| `covered` | Existing pillars contain enough guidance for agents to implement safely |
| `missing pillar guidance` | A requirement needs durable context that no pillar currently provides |
| `pillar conflict` | A pillar says something incompatible with the requirement |
| `prd stale` | Pillars show the product or implementation reality has moved beyond the PRD |
| `open question` | The PRD or pillars leave a decision unresolved |

### Step 5: Produce the report

Use this format:

```markdown
# PRD / Pillars Sync Report

Project: <best available project name>
Requirement docs inspected: <list>
Pillars inspected: <list>
Findings: <N>

## Summary

<2-4 sentences>

## Missing Pillar Guidance

### Finding 1: <short title>
- **Requirement:** <claim>
- **Suggested pillar:** `agents/<pillar>.md`
- **Why it matters:** <agent behavior impact>
- **Proposed edit:** <short snippet or prose>

## PRD Stale Or Incomplete

### Finding 1: <short title>
- **Pillar source:** `agents/<pillar>.md`
- **Requirement doc:** <file>
- **Why it matters:** <product impact>
- **Proposed PRD update:** <short snippet or prose>

## Conflicts

### Finding 1: <short title>
- **Requirement says:** <claim>
- **Pillar says:** <claim>
- **Decision needed:** <question for human>

## Covered

- <important requirement area already covered by pillars>

## Suggested Next Actions

1. <highest-value update>
2. <next update>
```

If there are no findings, say:

> No PRD / Pillars sync issues found.

---

## Constraints

- Do not write files.
- Do not modify files.
- Do not treat missing non-floor pillars as errors.
- Do not duplicate the full PRD into pillars.
- Do not duplicate implementation details into the PRD unless they affect product requirements.
- Do not resolve product conflicts silently. Ask for a human decision.

---

Now: reconcile product requirements and Pillars for this project.
