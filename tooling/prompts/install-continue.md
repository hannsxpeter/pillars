# Pillars in Continue

[Continue](https://continue.dev/) is configured via `.continue/config.json` (or `.continue/config.yaml`). It supports custom system messages, context providers, and slash commands.

## Runtime alignment

Continue can read `AGENTS.md` either by pointing its `systemMessage` at it or by adding it as a context provider.

### Option A: systemMessage reference

In `.continue/config.json`, add a `systemMessage` that points the agent at AGENTS.md:

```json
{
  "models": [...],
  "systemMessage": "This project follows the Pillars standard. Read AGENTS.md at the project root and follow its protocol to load the relevant pillars from ./agents/**/*.md before any code work. Comply with their Rules, apply Workflows, heed Watchouts, defer to Gaps."
}
```

Continue prepends this to every chat. The agent then reads AGENTS.md as part of its setup.

### Option B: file context

In Continue's chat, manually include AGENTS.md and the relevant pillars via `@<file>` references.

## Running the prompt workflows

Continue supports custom slash commands via `.continue/config.json`'s `slashCommands` array. To register the Pillars meta-operations:

```json
{
  "slashCommands": [
    {
      "name": "pillars-check",
      "description": "Check Pillars file structure",
      "prompt": "<paste the entire content of pillars-check.md here>"
    },
    {
      "name": "pillars-sync-design",
      "description": "Reconcile design.md and Pillars",
      "prompt": "<paste the entire content of pillars-sync-design.md here>"
    },
    {
      "name": "pillars-sync-prd",
      "description": "Reconcile requirements docs and Pillars",
      "prompt": "<paste the entire content of pillars-sync-prd.md here>"
    },
    {
      "name": "pillars-sync-readme",
      "description": "Reconcile README and Pillars",
      "prompt": "<paste the entire content of pillars-sync-readme.md here>"
    },
    {
      "name": "pillars-map-task",
      "description": "Map a task to Pillars",
      "prompt": "<paste the entire content of pillars-map-task.md here>"
    },
    {
      "name": "pillars-find-gaps",
      "description": "Index unresolved Pillars gaps",
      "prompt": "<paste the entire content of pillars-find-gaps.md here>"
    },
    {
      "name": "pillars-trim",
      "description": "Review Pillars for bloat",
      "prompt": "<paste the entire content of pillars-trim.md here>"
    },
    {
      "name": "pillars-init",
      "description": "Bootstrap Pillars in this project",
      "prompt": "<paste the entire content of pillars-init.md here>"
    },
    {
      "name": "pillars-author",
      "description": "Draft a Pillars pillar from the codebase",
      "prompt": "<paste the entire content of pillars-author.md here>"
    },
    {
      "name": "pillars-verify",
      "description": "Audit Pillars against the current codebase",
      "prompt": "<paste the entire content of pillars-verify.md here>"
    }
  ]
}
```

Then invoke via matching slash commands such as `/pillars-check`, `/pillars-map-task`, and `/pillars-sync-readme` in Continue's chat.

Alternative: paste the prompts into chat directly without registering commands. The paste-in path always works.

## Removing

Remove the `systemMessage` and `slashCommands` entries from `.continue/config.json`.

## Reference

- Continue: https://continue.dev/
- Continue config docs: https://docs.continue.dev/customization/overview
- Pillars standard: https://github.com/hannsxpeter/pillars
