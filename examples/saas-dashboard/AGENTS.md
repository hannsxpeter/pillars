# Pillars: Agent Protocol

This fictional project follows Pillars 1.1.0. Coding agents read local pillar metadata before acting.

## At the start of any task

1. Resolve applicable scopes from repository root to the task target. Nearest-scope guidance wins conflicts.
2. Scan pillar frontmatter, this file's exclusions, and optional `agents/catalog.yaml`.
3. Load always-loaded pillars. Match the task against other pillar and catalog `triggers` with the portable matcher.
4. Add each primary's `must_read_with` targets at depth 1. Sub-pillars use path-qualified identities.
5. Add a `see_also` target only when the task matches that target's identity, `triggers`, or `covers` with the same matcher.
6. Read selected bodies. Follow Rules and Workflows, heed Watchouts, and ask about Gaps.

## Portable matcher

Lowercase ASCII letters, replace non-alphanumeric runs with spaces, and match complete contiguous token sequences.

## Handling missing pillars

| State | Action |
|---|---|
| `status: present` | Load and comply. |
| `status: stub` | Ask before making decisions in this area. |
| Identity in `excluded:` | Treat as intentionally not applicable. |
| Trigger matches `agents/catalog.yaml` | Infer from code, state the assumption, and recommend creating the pillar. |
| No local metadata | Make no Pillars-specific claim. |

If `context.md` or `repo.md` is missing and not excluded, ask for a stub or exclusion.

## Excluded pillars

```yaml
excluded:
  - name: mobile
    reason: Web-only product
  - name: ml
    reason: No model training or inference surface
  - name: payments
    reason: Billing is handled by the parent company platform
```
