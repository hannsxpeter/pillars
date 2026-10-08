# Pillars in opencode

[opencode](https://opencode.ai/) reads `AGENTS.md` at the project root natively. Pillars works in opencode with zero installation beyond the standard itself.

## Runtime alignment (no install needed)

Once your project has `AGENTS.md` and `agents/` at the root, opencode will:

1. Read `AGENTS.md` on session start.
2. Follow its protocol to scan pillar frontmatter under `agents/`, including sub-pillar folders.
3. Load the relevant pillars based on the task.
4. Comply with their content during code work.

No opencode-specific configuration required.

## Running the prompt workflows

opencode supports custom commands and agents via `.opencode/` configuration. To install Pillars meta-operations as opencode commands:

### Option A: opencode custom commands

Check your opencode version's command format (it has evolved). If your version supports `.opencode/commands/` or similar:

```bash
mkdir -p .opencode/commands
for name in init author verify check map-task find-gaps trim sync-design sync-prd sync-readme; do
  curl -fsSL -o ".opencode/commands/pillars-$name.md" \
    "https://raw.githubusercontent.com/hannsxpeter/pillars/v1.2.2/tooling/prompts/pillars-$name.md"
done
```

Then invoke via matching slash commands such as `/pillars-check`, `/pillars-map-task`, and `/pillars-sync-readme`. Adapt the file format (frontmatter, extension) to match your opencode version's expectations.

### Option B: paste into chat (always works)

1. Open the relevant prompt file.
2. Copy its content.
3. Paste into opencode chat.

The agent follows the procedure step by step.

## Removing

Delete `.opencode/commands/pillars-*.md` if you used Option A.

## Reference

- opencode: https://opencode.ai/
- Pillars standard: https://github.com/hannsxpeter/pillars
