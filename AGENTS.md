# Pillars: Agent Protocol

This project follows the [Pillars](https://github.com/aihxp/pillars) standard. Coding agents working in this repository read the pillar files in `./agents/*.md` to stay aligned with the project's facts, decisions, and conventions.

## At the start of any task

1. **Load always-pillars.** Read every file in `./agents/` (recursively) whose frontmatter has `always_load: true`. These load every session regardless of task.

2. **Identify primary pillars.** Scan the frontmatter of all other files in `./agents/`. For each, check whether any of its `triggers` match the current task. The matching pillars are this task's primaries.

3. **Compute the load set.** Start with the primaries. Add every pillar listed in their `must_read_with` (depth 1; do not follow transitively). The result is the full load set.

4. **Load bodies.** Read the bodies of every pillar in the load set.

5. **Consult `see_also` selectively.** If the task explicitly touches an area named in a loaded pillar's `see_also`, read that pillar too. Otherwise skip.

6. **Comply.** Follow `Rules`. Apply `Workflows`. Heed `Watchouts` (with judgment). Defer to `Gaps` (ask the human; don't infer silently).

## Handling missing pillars

| State | Action |
|---|---|
| `status: present` | Load and comply. |
| `status: stub` | Concern acknowledged but rules undefined. Ask the human before making decisions in this area. Do not infer silently. |
| Name in `excluded:` (below) | Not applicable to this project. Proceed without. |
| Trigger matches a known name, file absent, not excluded | Graceful degradation. Infer conventions from code. State the assumption in your response. Recommend creating the pillar. |

If `context.md` or `repo.md` is missing entirely, pause and ask the human to either create stubs or declare them excluded. These are the floor.

## Excluded pillars

List the pillars this project intentionally excludes here, each with a reason so future contributors understand the call. The list is empty by default; populate it as you decide which concerns don't apply to your project.

```yaml
excluded: []
```

When non-empty, the form is:

```yaml
excluded:
  - name: observe
    reason: Vercel Analytics + built-in alerting cover our needs
  - name: i18n
    reason: English-only product
```

## Reference

- Pillar files in this repo: `./agents/*.md`
- Pillars standard: https://github.com/aihxp/pillars
- Spec: https://github.com/aihxp/pillars/blob/main/SPEC.md
- Pillar enumeration with tiers and boundaries: https://github.com/aihxp/pillars/blob/main/PILLARS.md
- Worked examples: https://github.com/aihxp/pillars/tree/main/examples
