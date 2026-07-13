# Pillars Sync Design Prompt

Paste this entire file into your AI coding tool's chat to reconcile a root `design.md` with a project's Pillars files. This is a report-only workflow. It does not write files.

Use this when a project already has `design.md`, when a new `design.md` has been written, or when pillars have evolved and you want to know whether `design.md` is stale.

---

## Task: reconcile design.md and Pillars

You are going to compare root `design.md` (if present) with the project's [Pillars](https://github.com/hannsxpeter/pillars) files and produce a sync report. Do not write, edit, move, or delete files.

### Step 1: Locate the artifacts

Check for:

```bash
ls AGENTS.md agents/ design.md
```

If `AGENTS.md` or `agents/` is missing, report:

> This project does not appear to have Pillars set up. Use `pillars-init.md` first.

If `design.md` is missing, report:

> No root `design.md` found. This workflow can still suggest where a future `design.md` would fit, but there is nothing to reconcile yet.

When `design.md` is absent, continue only if the user explicitly asked for guidance on creating one. Otherwise stop after the missing-artifact report.

### Step 2: Load Pillars context

Follow the project's `AGENTS.md` protocol:

1. Load always-loaded pillars.
2. Inventory other pillar files in every applicable root or nested scope. Treat local catalog entries as known absences, not pillar claims.
3. For this reconciliation task, inspect these pillars if present:
   - `context`
   - `arch`
   - `ui`
   - `repo`
   - `data`
   - `auth`
   - any domain pillar whose `covers` or `triggers` mention product, design, UX, brand, flow, journey, customer, tenant, workspace, or core domain objects.

Do not require all of these pillars to exist. Missing non-floor pillars are not errors.

### Step 3: Classify authority

Use this authority model unless the project says otherwise:

| Artifact | Authority |
|---|---|
| Root `design.md` | Product intent, user journeys, UX rationale, product narrative, major experience tradeoffs |
| `agents/context.md` | Durable vocabulary, product invariants, project identity |
| `agents/arch.md` | System shape, boundaries, data flow, technical design |
| `agents/ui.md` | UI implementation conventions, component patterns, design tokens |
| Other `agents/*.md` | Domain-specific operating constraints |

Do not duplicate every claim across files. The goal is reconciliation, not mirroring.

### Step 4: Extract design.md claims

From `design.md`, identify:

- Product purpose and target users.
- Core user journeys.
- UX principles and interaction model.
- Brand, tone, or visual constraints.
- System or architecture assumptions.
- Data model or domain-object assumptions.
- Explicit decisions and rationale.
- Open questions or unresolved design gaps.

For each claim, decide whether it should:

- Stay only in `design.md` as narrative or rationale.
- Be summarized into a pillar because agents need it during implementation.
- Conflict with an existing pillar.
- Be marked as an open `Gaps` item in a pillar.

### Step 5: Extract pillar claims that may affect design.md

From loaded pillars, identify claims that might make `design.md` stale:

- Product vocabulary changed.
- Core domain objects changed.
- Navigation, UI, or interaction conventions changed.
- Architecture changed in a way that affects product behavior.
- Data or auth constraints changed user-facing flows.
- Pillar `Gaps` contradict design.md's apparent certainty.

Do not treat every implementation detail as design-impacting. Only surface claims that affect product intent, user experience, or durable design rationale.

### Step 6: Classify sync direction

For each finding, classify it as:

| Direction | Meaning |
|---|---|
| `design.md -> pillars` | A durable design claim should be summarized into one or more pillars |
| `pillars -> design.md` | A pillar claim makes the root design brief stale or incomplete |
| `conflict` | Both artifacts make incompatible claims and the human must decide authority |
| `no action` | Related content exists, but each artifact is already carrying the right level of detail |

### Step 7: Propose edits, but do not write

For each actionable finding, provide:

- Source artifact and short quote or paraphrase.
- Target artifact.
- Direction.
- Why it matters to agent behavior.
- Proposed edit in concise prose or a small markdown snippet.

Keep proposed snippets short. Do not rewrite whole files.

### Step 8: Produce the report

Use this format:

```markdown
# design.md / Pillars Sync Report

Project: <best available project name>
design.md: present | absent
Pillars inspected: <list>
Findings: <N>

## Summary

<2-4 sentences>

## design.md -> Pillars

### Finding 1: <short title>
- **Source:** `design.md`
- **Target:** `agents/<pillar>.md`
- **Why it matters:** <agent behavior impact>
- **Proposed edit:** <concise snippet or prose>

## Pillars -> design.md

### Finding 1: <short title>
- **Source:** `agents/<pillar>.md`
- **Target:** `design.md`
- **Why it matters:** <product/design impact>
- **Proposed edit:** <concise snippet or prose>

## Conflicts

### Finding 1: <short title>
- **design.md says:** <claim>
- **Pillar says:** <claim>
- **Decision needed:** <question for human>

## No Action

- <important area that is already properly divided>

## Suggested Next Actions

1. <highest-value update>
2. <next update>
```

If there are no findings, say:

> No design.md / Pillars sync issues found.

---

## Constraints

- Do not write files.
- Do not modify files.
- Do not create a new `design.md` unless the user separately asks for that in a new task.
- Do not auto-sync bidirectionally.
- Do not duplicate narrative design rationale into pillars unless agents need it during implementation.
- Do not duplicate implementation conventions into `design.md` unless they affect product intent or user experience.
- Do not treat absent `arch.md`, `ui.md`, or domain pillars as errors.

---

Now: reconcile `design.md` and Pillars for this project.
