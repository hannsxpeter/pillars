# Pillars in Cline

Cline reads `.clinerules` at the project root. Recent versions also support `AGENTS.md`.

## Runtime alignment

### Option A: native AGENTS.md (preferred if supported)

If your Cline version reads `AGENTS.md` directly, no extra config needed.

### Option B: .clinerules redirect

For versions that only read `.clinerules`:

`.clinerules`:

```markdown
This project follows the Pillars standard (https://github.com/hannsxpeter/pillars).

Before doing any code work, read `AGENTS.md` at the project root and follow its protocol to load the relevant pillars from `./agents/*.md`.

Do not infer conventions when a relevant pillar exists. Do not silently ignore a Gaps entry; ask the user.
```

## Running the prompt workflows

Cline supports custom workflows in some versions. For broad compatibility, use paste-in:

1. Open the relevant prompt file in this folder.
2. Copy its content.
3. Paste into Cline's chat.

If your Cline version supports custom commands in a specific format, adapt the prompt content into that format; the body stays the same.

## Removing

Delete `.clinerules` if you added one.

## Reference

- Cline: https://github.com/cline/cline
- Pillars standard: https://github.com/hannsxpeter/pillars
