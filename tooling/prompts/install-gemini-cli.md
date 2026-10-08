# Pillars in Gemini CLI

Gemini CLI reads `GEMINI.md` (its native project-instructions file) and, in recent versions, `AGENTS.md`. Pillars works in Gemini CLI by either approach.

## Runtime alignment

### Option A: native AGENTS.md (preferred)

If your Gemini CLI version reads `AGENTS.md`, no additional config is needed. The standard's runtime loop just works.

### Option B: GEMINI.md redirect

If your version only reads `GEMINI.md`, create a thin redirect:

`GEMINI.md`:

```markdown
# Project agent instructions

This project follows the [Pillars](https://github.com/hannsxpeter/pillars) standard.

Read `AGENTS.md` at the repo root and follow its protocol to load the relevant pillars from `./agents/**/*.md` before doing any work.
```

The agent reads `GEMINI.md`, sees the redirect, and proceeds via `AGENTS.md`.

## Running the prompt workflows

### Option A: Gemini CLI commands (if supported in your version)

Gemini CLI supports custom commands in some versions via files in `~/.gemini/commands/` (global) or `.gemini/commands/` (per-project). Format varies by version.

If your version supports them, download the prompt files, pinned to the release you adopted:

```bash
mkdir -p "$HOME/.gemini/commands"
for name in init author verify check map-task find-gaps trim sync-design sync-prd sync-readme; do
  curl -fsSL -o "$HOME/.gemini/commands/pillars-$name.md" \
    "https://raw.githubusercontent.com/hannsxpeter/pillars/v1.2.2/tooling/prompts/pillars-$name.md"
done
```

Then invoke via matching slash commands such as `/pillars-check`, `/pillars-map-task`, and `/pillars-sync-readme` in Gemini chat.

If your version uses a different command format (e.g., TOML with frontmatter), adapt the prompt content into that shape; the body stays the same.

### Option B: paste into chat (always works)

1. Open the relevant prompt file.
2. Copy its content.
3. Paste into Gemini CLI chat.

## Removing

Delete `GEMINI.md` (if you added a redirect) and any files under `~/.gemini/commands/` or `.gemini/commands/`.

## Reference

- Gemini CLI: https://github.com/google-gemini/gemini-cli
- Pillars standard: https://github.com/hannsxpeter/pillars
