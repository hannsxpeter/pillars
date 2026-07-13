# Pillars in Windsurf

Windsurf reads `.windsurfrules` at the project root (and `~/.windsurfrules` globally). Recent versions also support `AGENTS.md` directly.

## Runtime alignment

### Option A: native AGENTS.md (preferred if your version supports it)

If your Windsurf version reads `AGENTS.md`, no extra config needed.

### Option B: .windsurfrules redirect

For Windsurf versions that only read `.windsurfrules`, create a thin redirect:

`.windsurfrules`:

```markdown
This project follows the Pillars standard (https://github.com/hannsxpeter/pillars).

Before doing any code work, read `AGENTS.md` at the project root and follow its protocol to load the relevant pillars from `./agents/*.md`.

Do not infer conventions when a relevant pillar exists. Do not silently ignore a Gaps entry; ask the user.
```

Windsurf will load `.windsurfrules` as system context; the agent then proceeds via AGENTS.md.

## Running the prompt workflows

Windsurf's persistent custom-command support varies by version, so use paste-in:

1. Open the relevant prompt file in this folder.
2. Copy its content.
3. Paste into Windsurf's Cascade chat as a single message.

## Removing

Delete `.windsurfrules` if you added one.

## Reference

- Windsurf: https://codeium.com/windsurf
- Pillars standard: https://github.com/hannsxpeter/pillars
