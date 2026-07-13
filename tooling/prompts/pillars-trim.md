# Pillars Trim Prompt

Paste this entire file into your AI coding tool's chat to review Pillars files for bloat, duplication, and over-prescription. This is a report-only workflow. It does not write files.

Use this to protect the "briefings, not rulebooks" philosophy.

---

## Task: review Pillars for trim opportunities

You are going to scan the project's Pillars files and report where they could be shorter, clearer, or less duplicative. Do not write, edit, move, or delete files.

### Step 1: Locate Pillars

Check for:

```bash
ls AGENTS.md agents/
find agents -name "*.md" -type f | sort
```

If `AGENTS.md` or `agents/` is missing, report:

> This project does not appear to have Pillars set up. Use `pillars-init.md` first.

Then stop.

### Step 2: Scan structure and size

For each root or nested scope and each pillar file:

- Count approximate lines and words.
- Parse frontmatter.
- Note `must_read_with` count.
- Read all 8 sections.

### Step 3: Look for trim signals

Flag:

- Rules that simply restate Context.
- Rules without a reason.
- Watchouts without a reason.
- Very long Context sections that could be split or summarized.
- Duplicate claims repeated across pillars.
- More than 3 `must_read_with` entries.
- Compliance-style or command-heavy prose.
- Large examples that could move to `examples/`.
- Pillars covering multiple domains that should be split.
- Always-loaded files over 1,000 words or 8 KiB, or over 2,000 words and 16 KiB in aggregate per scope.
- Task-routed files over 2,000 words or 16 KiB without a documented reason.

Do not flag concise, useful specificity as bloat.

### Step 4: Produce the report

Use this format:

```markdown
# Pillars Trim Report

Project: <best available project name>
Pillars scanned: <N>
Findings: <N>

## High Value Trims

### Finding 1: <short title>
- **File:** `agents/<pillar>.md`
- **Section:** <section>
- **Issue:** <what is bloated or duplicated>
- **Why it matters:** <agent context impact>
- **Suggested trim:** <short recommendation>

## Minor Trims

...

## Healthy Patterns

- <things worth preserving>

## Suggested Next Actions

1. <highest-value trim>
2. <next trim>
```

If no trim findings are found, say:

> No Pillars trim issues found.

---

## Constraints

- Do not write files.
- Do not modify files.
- Do not remove context just because it is detailed.
- Do not penalize examples when they are short and clarify a non-obvious rule.
- Do not suggest new abstractions unless they reduce real duplication or confusion.

---

Now: review this project's Pillars for trim opportunities.
