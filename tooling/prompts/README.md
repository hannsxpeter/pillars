# Universal Prompts

Tool-agnostic prompts that drive Pillars meta-operations in any AI coding tool. Paste the relevant prompt into your tool's chat to run the procedure.

These work in: Claude Code, Cursor, Codex CLI, Gemini CLI, opencode, Aider, Windsurf, Cline, Continue, Pieces, and anything else that can read a project and write files based on instructions.

If your tool has a native command/skill format, see the `tooling/<tool>/` directory (when available) for tighter integration. For now, the universal prompts are the broadest-compatibility option.

## The prompts

| File | When to use |
|---|---|
| [`pillars-check.md`](pillars-check.md) | Validate identities, frontmatter, sections, floors, references, catalogs, and budgets. Does not audit code drift. |
| [`pillars-find-gaps.md`](pillars-find-gaps.md) | Index body `Gaps`, stubs, and cataloged absences across scopes. |
| [`pillars-init.md`](pillars-init.md) | Bootstrap Pillars. Detects archetype, drops AGENTS.md, scaffolds stubs, and reconciles exclusions with the local catalog. |
| [`pillars-author.md`](pillars-author.md) | Draft or revise a specific pillar from the codebase. Scans relevant code, presents 8-section draft for approval. |
| [`pillars-map-task.md`](pillars-map-task.md) | Map a task to the pillars that should load and explain why. |
| [`pillars-verify.md`](pillars-verify.md) | Audit pillars against current code. Flags drift with evidence, suggests fixes. Manual lightweight check. |
| [`pillars-sync-design.md`](pillars-sync-design.md) | Reconcile root `design.md` with Pillars. Reports proposed updates in both directions without writing files. |
| [`pillars-sync-prd.md`](pillars-sync-prd.md) | Reconcile PRDs or requirements docs with Pillars. |
| [`pillars-sync-readme.md`](pillars-sync-readme.md) | Reconcile README with Pillars. |
| [`pillars-trim.md`](pillars-trim.md) | Review pillars for bloat, duplication, and over-prescription. |

## How to use

### Generic flow (works in any tool)

1. Open the relevant prompt file in this folder.
2. Copy its full content to your clipboard.
3. Paste it as a single message into your AI coding tool's chat.
4. For `pillars-author.md`, add the pillar name at the bottom (the prompt's last line asks you to fill it in).
5. The AI will follow the procedure step by step.

### Per-tool quick install

For tools where the universal prompts are the recommended integration:

| Tool | Install doc |
|---|---|
| Cursor | [install-cursor.md](install-cursor.md) |
| Codex CLI | [install-codex-cli.md](install-codex-cli.md) |
| Gemini CLI | [install-gemini-cli.md](install-gemini-cli.md) |
| opencode | [install-opencode.md](install-opencode.md) |
| Aider | [install-aider.md](install-aider.md) |
| Windsurf | [install-windsurf.md](install-windsurf.md) |
| Cline | [install-cline.md](install-cline.md) |
| Continue | [install-continue.md](install-continue.md) |

For Claude Code, prefer the native skill bundle in [../claude-skill/](../claude-skill/) for init, author, and verify. Use the prompt files directly for the smaller report-only workflows.

## Why these are separate from the Claude Code skill

The Claude Code skill (`tooling/claude-skill/`) packages selected procedures as Claude Code skill files with proper frontmatter, triggers, and slash-command invocation. That packaging is tool-specific.

The universal prompts here are the same procedures formatted as paste-in instructions, with no tool-specific framing. They're slightly more verbose (because they include orientation that a native skill takes for granted) but they work everywhere.

The Claude Code skill bundle packages init, author, and verify as native skills. The smaller report-only workflows are prompt-only for now, because they should stay available without adding a CLI or another native packaging surface.

## Drift between forms

If a procedural update happens, matching prompt and skill forms should be updated together when both exist. For now, treat the procedures as canonically defined here in the prompts; the Claude Code skill mirrors the procedures it packages.

## Reference

- Pillars standard: https://github.com/hannsxpeter/pillars
- SPEC.md: https://github.com/hannsxpeter/pillars/blob/v1.2.0/SPEC.md
- PILLARS.md: https://github.com/hannsxpeter/pillars/blob/v1.2.0/PILLARS.md
