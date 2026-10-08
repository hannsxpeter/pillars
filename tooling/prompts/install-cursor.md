# Pillars in Cursor

Cursor has good native support for project-level rules and custom commands. Two ways to integrate Pillars:

## Option A: Project rule + paste-in prompts (recommended)

Add a Cursor rule that ensures the agent reads AGENTS.md on every interaction. Then paste the prompts from this folder when you want to run a Pillars workflow.

1. In your project, create `.cursor/rules/pillars.mdc`:

```markdown
---
description: Follow the Pillars standard in this project
globs:
alwaysApply: true
---

This project follows the [Pillars](https://github.com/hannsxpeter/pillars) standard. Before doing any code work, read `AGENTS.md` at the project root and follow its protocol to load the relevant pillars from `./agents/**/*.md`.

Do not infer conventions when a relevant pillar exists; consult the pillar. Do not silently ignore a `Gaps` entry; ask the user instead.
```

2. To run a workflow, open the relevant `pillars-*.md` prompt in this folder, copy the content, and paste it into Cursor's chat. The agent will follow the procedure.

## Option B: Cursor Commands (optional, cleaner UX)

If you want `/pillars-init` and similar to work natively in Cursor:

1. Download the prompt files as Cursor commands, pinned to the release you adopted:

```bash
mkdir -p .cursor/commands
for name in init author verify check map-task find-gaps trim sync-design sync-prd sync-readme; do
  curl -fsSL -o ".cursor/commands/pillars-$name.md" \
    "https://raw.githubusercontent.com/hannsxpeter/pillars/v1.2.2/tooling/prompts/pillars-$name.md"
done
```

2. Restart Cursor or reload the workspace. The commands will be available via matching slash commands such as `/pillars-check`, `/pillars-map-task`, and `/pillars-sync-readme`.

Note: Cursor's command format is evolving. If your version uses a different file structure (e.g., `.mdc` extension with frontmatter), wrap each prompt's content with the expected frontmatter block. The command body itself is the prompt content unchanged.

## Removing

Delete `.cursor/rules/pillars.mdc` and (if used) `.cursor/commands/pillars-*.md`. Nothing else to clean up.

## Reference

- Cursor docs on Rules: https://docs.cursor.com/context/rules
- Pillars standard: https://github.com/hannsxpeter/pillars
