# Pillars: Agent Protocol

This project follows [Pillars 1.2.2](https://github.com/hannsxpeter/pillars/tree/v1.2.2). Coding agents read project pillar files before acting.

## At the start of any task

1. **Resolve scopes.** Starting at the repository root and ending at the task's target path or current directory, find every directory containing both `AGENTS.md` and `agents/`. Apply scopes from outermost to innermost. The nearest scope wins when guidance conflicts.

2. **Inventory local metadata.** In each scope, scan pillar frontmatter recursively. Read exclusions from the local `AGENTS.md` and absent concerns from optional `agents/catalog.yaml`.

3. **Select always and primary pillars.** Load every pillar with `always_load: true`. Match the task against every other pillar's `triggers` using the portable matcher in `SPEC.md`. Matching pillars are primaries. Matching catalog entries are absent concerns.

4. **Add direct dependencies.** Add every identity in each primary's `must_read_with`. Resolve top-level identities such as `auth` at `agents/auth.md` and sub-pillar identities such as `auth/agent-registration` at that exact relative path. Stop at depth 1.

5. **Consult soft references.** Add a selected pillar's `see_also` target only when the task matches that target's identity, `triggers`, or `covers` with the same matcher. Do not follow `see_also` recursively.

6. **Load and comply.** Read selected bodies. Follow `Rules`, apply `Workflows`, heed `Watchouts` with judgment, and defer to `Gaps`. Preserve non-conflicting ancestor guidance; nearest-scope guidance wins conflicts.

## Handling missing pillars

| State | Action |
|---|---|
| `status: present` | Load and comply. |
| `status: stub` | Ask before making decisions in this area. Do not infer silently. |
| Identity in local `excluded:` | Treat as intentionally not applicable in that scope. |
| Trigger matches local `agents/catalog.yaml` entry | Infer from code, state the assumption, and recommend creating the pillar. |
| No local file, exclusion, or catalog entry | Make no Pillars-specific claim about that concern. |

If `context.md` or `repo.md` is missing and not explicitly excluded, pause and ask the human to create a stub or record an exclusion.

## Portable matcher

Lowercase ASCII letters, replace each run of non-alphanumeric characters with one space, trim, and split into tokens. A selector matches when its complete token sequence appears contiguously in the task tokens. Semantic matching may add matches but cannot remove deterministic matches.

## Excluded pillars

```yaml
excluded: []
```

## Reference

- Pillar files in this repo: `./agents/**/*.md`
- Optional absent catalog: `./agents/catalog.yaml`
- Spec: https://github.com/hannsxpeter/pillars/blob/v1.2.2/SPEC.md
- Pillar enumeration: https://github.com/hannsxpeter/pillars/blob/v1.2.2/PILLARS.md
- Worked examples: https://github.com/hannsxpeter/pillars/tree/v1.2.2/examples
