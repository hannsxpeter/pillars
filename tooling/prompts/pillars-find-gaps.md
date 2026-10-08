# Pillars Find Gaps Prompt

Paste this entire file into your AI coding tool's chat to produce a project-level index of unresolved `Gaps` across Pillars files. This is a report-only workflow. It does not write files.

Use this when you want to see where agents should ask before inferring.

---

## Task: index Pillars gaps

You are going to scan the project's Pillars files and report every unresolved gap. Do not write, edit, move, or delete files.

### Step 1: Locate Pillars

Check for:

```bash
ls AGENTS.md agents/
find . -name AGENTS.md -not -path "./.git/*" -not -path "*/node_modules/*" | sort
```

A scope is a directory with both `AGENTS.md` and `agents/`. List each scope's pillar files, including sub-pillar folders, with `find <scope>/agents -name "*.md" -type f | sort`.

If `AGENTS.md` or `agents/` is missing, report:

> This project does not appear to have Pillars set up. Use `pillars-init.md` first.

Then stop.

### Step 2: Inventory pillars

For each applicable root or nested scope, read its exclusions and optional `agents/catalog.yaml`. For each pillar file, parse frontmatter and note:

- Path
- `pillar`
- `status`
- `covers`
- `triggers`

Read the body and extract the `## Gaps` section.

Catalog entries are known absent concerns, not body gaps. Report them in a separate `Cataloged Absences` section unless the same identity is excluded or present, which is a structural conflict.

### Step 3: Classify gaps

For each gap, classify:

| Classification | Meaning |
|---|---|
| `decision needed` | Human must decide before implementation |
| `policy missing` | A durable policy is not defined |
| `technical unknown` | Implementation shape is not decided |
| `future capability` | Known future work, not current implementation |
| `stub follow-up` | Pillar is a stub and needs authoring |

Also estimate task impact:

| Impact | Meaning |
|---|---|
| `high` | Likely blocks or risks common implementation tasks |
| `medium` | Matters for a known area but not every task |
| `low` | Useful to track, unlikely to block near-term work |

### Step 4: Produce the report

Use this format:

```markdown
# Pillars Gap Index

Project: <best available project name>
Pillars scanned: <N>
Gaps found: <N>
Cataloged absences: <N>

## High Impact

### `agents/<pillar>.md`: <short title>
- **Gap:** <gap text>
- **Classification:** <classification>
- **Why it matters:** <agent behavior impact>
- **Suggested owner/question:** <who or what to ask>

## Medium Impact

...

## Low Impact

...

## Stub Pillars

- `agents/<pillar>.md`: <summary>

## Cataloged Absences

- `<scope>::<identity>`: <covers and likely task impact>

## Suggested Next Actions

1. <highest-value question to answer>
2. <next question>
```

If no gaps are found, say:

> No unresolved Pillars gaps found.

---

## Constraints

- Do not write files.
- Do not modify files.
- Do not resolve gaps by inference.
- Do not treat `(none)` as a gap.
- Do not treat example text outside `agents/` as project gaps.

---

Now: scan this project and produce the gap index.
