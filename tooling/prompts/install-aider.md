# Pillars in Aider

[Aider](https://aider.chat/) does not load project instruction files on its own. You hand them to it as read-only context with `--read` on the command line, `/read-only` in chat, or a `read:` list in `.aider.conf.yml`. Read-only files are cached when prompt caching is enabled.

## Runtime alignment

### Option A: read AGENTS.md and the pillars (recommended)

```bash
aider --read AGENTS.md --read agents
```

Passing the `agents` directory reads every file under it, including sub-pillar folders and `catalog.yaml`. Aider does not expand glob patterns in `--read`, so pass the directory rather than a pattern such as `agents/*.md`.

Aider resolves these paths from the directory it was launched in, so start it from the project root. To make it permanent, add this to `.aider.conf.yml` in the project root:

```yaml
read: [AGENTS.md, agents]
```

This loads every pillar at session start, which differs from the Pillars protocol's task-routed loading: Aider sees all pillars and the model applies the protocol to decide which ones matter. For a small pillar set that is usually fine.

### Option B: task-routed loading by hand

For a large pillar set, read only the protocol:

```bash
aider --read AGENTS.md
```

Then, per task, add the pillars the protocol selects with `/read-only agents/<name>.md`. This keeps context small at the cost of a manual step.

## Running the prompt workflows

Aider has no persistent custom slash commands. Use paste-in:

1. Open the relevant prompt file in this folder.
2. Copy its content.
3. Paste into Aider's chat as a single message.

Or save the prompt file into your project and add it with `/read-only <file>`, then ask Aider to follow it.

## Removing

Remove the `--read` flags or the `read:` entries from `.aider.conf.yml`.

## Reference

- Aider: https://aider.chat/
- Aider conventions docs: https://aider.chat/docs/usage/conventions.html
- Pillars standard: https://github.com/hannsxpeter/pillars
