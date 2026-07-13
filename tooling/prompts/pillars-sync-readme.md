# Pillars Sync README Prompt

Paste this entire file into your AI coding tool's chat to reconcile `README.md` with a project's Pillars files. This is a report-only workflow. It does not write files.

Use this when README is the public project truth and Pillars are the agent-facing project truth.

---

## Task: reconcile README and Pillars

You are going to compare root `README.md` with the project's [Pillars](https://github.com/hannsxpeter/pillars) files and produce a sync report. Do not write, edit, move, or delete files.

### Step 1: Locate the artifacts

Check for:

```bash
ls README.md AGENTS.md agents/
```

If `README.md` is missing, report:

> No root `README.md` found. There is nothing to reconcile.

If `AGENTS.md` or `agents/` is missing, report:

> This project does not appear to have Pillars set up. Use `pillars-init.md` first.

Then stop if either side is missing.

### Step 2: Load relevant pillars

Follow the project's `AGENTS.md` protocol:

1. Load always-loaded pillars.
2. Inspect relevant pillars in every applicable root or nested scope. Treat local catalog entries as known absences, not pillar claims:
   - `context`
   - `repo`
   - `stack`
   - `arch`
   - `data`
   - `api`
   - `deploy`
   - `quality`
   - domain pillars mentioned by README.

Do not require all of these pillars to exist.

### Step 3: Compare claims

Compare README and pillars for:

- Project purpose and audience.
- Setup or quick-start instructions.
- Repository layout.
- Stack, dependency, or architecture claims.
- Public API or command examples.
- Deployment or release claims.
- Contribution or quality expectations.
- Feature status or roadmap statements.

### Step 4: Classify findings

| Classification | Meaning |
|---|---|
| `README stale` | Pillars show current truth that README does not reflect |
| `pillar stale` | README appears newer than the relevant pillar |
| `conflict` | Both make incompatible claims and human decision is needed |
| `missing public docs` | A pillar contains user-facing information that README should mention |
| `agent-only` | A pillar contains implementation guidance that should stay out of README |

### Step 5: Produce the report

Use this format:

```markdown
# README / Pillars Sync Report

Project: <best available project name>
Pillars inspected: <list>
Findings: <N>

## Summary

<2-4 sentences>

## README Stale Or Incomplete

### Finding 1: <short title>
- **Pillar source:** `agents/<pillar>.md`
- **README area:** <section or topic>
- **Why it matters:** <reader impact>
- **Proposed README update:** <short snippet or prose>

## Pillars Stale Or Incomplete

### Finding 1: <short title>
- **README source:** <section or quote>
- **Target pillar:** `agents/<pillar>.md`
- **Why it matters:** <agent behavior impact>
- **Proposed pillar update:** <short snippet or prose>

## Conflicts

### Finding 1: <short title>
- **README says:** <claim>
- **Pillar says:** <claim>
- **Decision needed:** <question for human>

## No Action

- <important area that is already properly divided>

## Suggested Next Actions

1. <highest-value update>
2. <next update>
```

If there are no findings, say:

> No README / Pillars sync issues found.

---

## Constraints

- Do not write files.
- Do not modify files.
- Do not duplicate agent-only implementation rules into README.
- Do not duplicate public marketing or usage copy into pillars unless agents need it.
- Do not treat absent non-floor pillars as errors.

---

Now: reconcile README and Pillars for this project.
