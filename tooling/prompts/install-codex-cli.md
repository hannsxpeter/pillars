# Pillars in Codex CLI

OpenAI Codex CLI natively reads `AGENTS.md` at the project root and applies it as system context for the session. Pillars works in Codex with zero installation beyond the standard itself.

## Runtime alignment (no install needed)

Once your project has `AGENTS.md` and `agents/` at the root, Codex CLI will:

1. Read `AGENTS.md` on session start.
2. Follow its protocol to scan `agents/*.md` frontmatter.
3. Load the relevant pillars based on the task.
4. Comply with their content during code work.

No Codex-specific configuration is required.

## Running the prompt workflows

Codex CLI's persistent custom-command support varies by version, so the portable way to invoke meta-operations is to paste the prompt content:

### Option A: paste into chat

1. Open the relevant `pillars-*.md` prompt from this folder.
2. Copy its content.
3. Paste into your Codex CLI chat.
4. The agent follows the procedure.

### Option B: pipe via stdin

If your Codex CLI accepts piped input as the initial message:

```bash
cat tooling/prompts/pillars-init.md | codex
```

(Adapt the binary name to your install; check `codex --help` for input modes.)

### Option C: project-level alias

You can stage the prompts inside your project as a one-time convenience:

```bash
mkdir -p .codex/prompts
cp tooling/prompts/pillars-*.md .codex/prompts/
```

Then ask Codex CLI to read `.codex/prompts/pillars-init.md` and follow it.

## Removing

If you used Option C, delete `.codex/prompts/`. Nothing else to clean up.

## Reference

- OpenAI Codex CLI: https://github.com/openai/codex
- Pillars standard: https://github.com/hannsxpeter/pillars
