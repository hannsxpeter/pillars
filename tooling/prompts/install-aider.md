# Pillars in Aider

[Aider](https://aider.chat/) reads conventions files (`CONVENTIONS.md`, recent versions also support `AGENTS.md`) and includes them in the system context.

## Runtime alignment

### Option A: native AGENTS.md (preferred)

If your Aider version reads `AGENTS.md`, no extra config needed. The runtime loop just works.

Confirm by checking your `aider.conf.yml` for a `read:` entry or by running `aider --help | grep -i agents`.

### Option B: explicit `--read` flag

If your Aider version doesn't auto-read `AGENTS.md`, add it explicitly:

```bash
aider --read AGENTS.md --read 'agents/*.md'
```

Or persistently in `~/.aider.conf.yml`:

```yaml
read:
  - AGENTS.md
  - agents/*.md
```

This loads all pillar files into Aider's context at session start. Note: this differs from the Pillars protocol's task-routed loading. Aider sees all pillars; the agent matches relevance internally.

### Option C: CONVENTIONS.md redirect

For older Aider versions that only read `CONVENTIONS.md`:

`CONVENTIONS.md`:

```markdown
# Project conventions

This project follows the [Pillars](https://github.com/hannsxpeter/pillars) standard.

Read `AGENTS.md` at the repo root and follow its protocol to load the relevant pillars from `./agents/*.md` before doing any work.
```

## Running the prompt workflows

Aider doesn't have persistent slash commands beyond its built-ins. Use paste-in:

1. Open the relevant prompt file in this folder.
2. Copy its content.
3. Paste into Aider's chat as a single message.

Or use the `/load` command (if available in your version) to load the prompt as additional context.

## Removing

Remove `--read AGENTS.md` flags or the `read:` block from your aider config. Delete `CONVENTIONS.md` if you added a redirect.

## Reference

- Aider: https://aider.chat/
- Aider conventions docs: https://aider.chat/docs/usage/conventions.html
- Pillars standard: https://github.com/hannsxpeter/pillars
