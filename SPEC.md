# Pillars Specification

Version 1.0.1.

This document defines the Pillars standard. It specifies the pillar file template, the YAML frontmatter schema, the loading mechanism, and the missing-pillar protocol. An implementation that conforms to this spec is *Pillars-compatible*.

## 1. Philosophy

The pillar's job is to surface what the agent **cannot infer from the code**. Coding agents are capable; the standard exists to prevent *drift*, not to put the agent on rails.

Core principle:

> Include prescriptive content only when it would *not* be inferred from the facts.

"Project uses Drizzle" doesn't need a rule "use Drizzle"; the agent infers. But "project uses Drizzle AND never raw SQL outside `db/raw.ts`" does need stating, because Drizzle and raw SQL can coexist; the agent can't infer that constraint from code alone.

Tone: pillars should read like *what an experienced engineer would tell a new contributor on day one*. Conversational, declarative, reasoned. Not like compliance documentation.

## 2. Repository layout

A Pillars-compatible project has:

- `AGENTS.md` at the repository root: the protocol description.
- `agents/` at the repository root: a folder containing pillar files.

Pillar files use the `.md` extension and live at `agents/<name>.md` for top-level pillars or `agents/<parent>/<name>.md` for sub-pillars.

## 3. Pillar file structure

Every pillar file consists of YAML frontmatter followed by an 8-section markdown body.

### 3.1 Frontmatter schema

```yaml
---
pillar: data
status: present
always_load: false
covers: [database schema, migrations, queries, storage]
triggers: [database, schema, migration, query, table, column]
must_read_with: [auth, config]
see_also: [api, observe]
---
```

| Field | Type | Required | Default | Meaning |
|---|---|---|---|---|
| `pillar` | string | yes | — | Canonical name. Must match filename (without `.md`). |
| `status` | enum | no | `present` | `present` or `stub`. See section 5. |
| `always_load` | boolean | no | `false` | If `true`, the pillar is loaded every session regardless of triggers. |
| `covers` | list of strings | yes | — | One-line scope. For skim and discovery. |
| `triggers` | list of strings | yes (unless `always_load: true`) | — | Keywords/phrases the agent matches against the task description. |
| `must_read_with` | list of strings | no | `[]` | Direct hard dependencies. Loaded with this pillar (depth 1; not transitive). |
| `see_also` | list of strings | no | `[]` | Soft dependencies. Loaded only if the task explicitly touches that area. |

Sub-pillars use the same schema. Their parent is derived from the file path, not the frontmatter.

### 3.2 Body template (8 sections)

The body follows this shape exactly. Sections 3-6 are populated only when they add value; if Context already implies the content, skip them.

1. **Scope** — what this pillar covers, what it doesn't.
2. **Context** — declarative facts about this project in this domain. Stack choices, file locations, naming, conventions in use. The default-populated section.
3. **Decisions** — non-obvious choices and why they were made.
4. **Rules** — hard constraints not inferable from Context. The agent must follow these. Used sparingly.
5. **Workflows** — multi-step procedures the agent might not infer from facts alone.
6. **Watchouts** — soft warnings from experience, with reasoning. Not bans; informed warnings.
7. **Touchpoints** — couplings to other pillars (mirrors frontmatter for human readability).
8. **Gaps** — explicit "not decided yet." Tells the agent when to ask the human.

Empty sections are marked `(none)`. Examples appear inline within Context, Rules, or Workflows rather than as their own section.

### 3.3 Graduated firmness (sections 3-6)

| Section | Firmness | Job |
|---|---|---|
| Decisions | Informative | "Here's why we picked this." |
| Rules | Hard | "Follow this constraint." |
| Workflows | Procedural | "Here's the recipe." |
| Watchouts | Soft | "Be aware this has burned us." |

### 3.4 Pillar maturity gradient

A pillar exists once it has frontmatter and a Scope statement. Other sections fill in over the project's lifetime:

```
stub -> partially populated -> fully populated
```

There is no obligation to fill all 8 sections at creation time. Many pillars stay partially populated indefinitely.

## 4. Loading mechanism

`AGENTS.md` describes the protocol the agent follows at the start of every task. The protocol is:

1. **Load always-pillars.** Read every file in `agents/` (recursively) whose frontmatter has `always_load: true`.
2. **Identify primary pillars.** Scan the frontmatter of all other pillar files. For each, check whether any of its `triggers` match the current task description (substring, keyword, or semantic match — implementation-defined). The matches are this task's primaries.
3. **Compute the load set.** Start with the primaries. Add every pillar listed in their `must_read_with`. **Depth 1 only.** Do not transitively follow `must_read_with` of those pillars.
4. **Load bodies.** Read the bodies of every pillar in the load set.
5. **Consult `see_also` selectively.** If the task explicitly touches an area named in a loaded pillar's `see_also`, load that pillar too.
6. **Comply.** Follow `Rules`. Apply `Workflows`. Heed `Watchouts` (with judgment). Defer to `Gaps` (ask the human; don't infer silently).

### 4.1 Why depth 1, not transitive closure

Predictability for authors. Reading a pillar's frontmatter tells you *exactly* what loads alongside it. Forces honest declaration: if `data` needs `auth` and `config`, both are listed directly; coupling is visible at the source. Frequently-needed pillars graduate to `always_load: true` instead of becoming hidden transitive dependencies.

### 4.2 Self-diagnosing decomposition

The standard treats these patterns as boundary smells:

- A pillar's `must_read_with` has more than 3 entries.
- A coupling pattern where many pillars list the same set of dependencies. Promote the shared dependency to `always_load: true` instead.

Bad decomposition is visible in the frontmatter; the standard surfaces it without external tooling.

### 4.3 Trigger matching is implementation-defined

Step 2 deliberately leaves the matching technique open: a conforming tool may match `triggers` by substring, keyword, or semantic similarity. Pillar *content* is fully portable across tools; relevance *matching* is intentionally not pinned, because tools differ in retrieval capability and fixing one algorithm would freeze the standard to today's techniques. The practical consequence is that two conforming tools may select slightly different primaries for the same task. Three things bound that variance: the always-loaded floor (`context`, `repo`) loads regardless of matching, the depth-1 rule (section 4.1) caps how far a primary pulls in others, and any pillar that must load for a class of task can be promoted to `always_load: true`. Author `triggers` for recall: include the obvious synonyms a task might use, rather than assuming a particular matching algorithm.

## 5. Missing-pillar protocol

A pillar can be in one of four states relative to a project:

| State | Indicator | Agent behavior |
|---|---|---|
| **Present** | File exists; `status: present` (or omitted) | Load and comply normally. |
| **Stub** | File exists; `status: stub`; minimal body | Acknowledge the concern. Ask the human before making decisions in this area. Do not silently infer. |
| **Excluded** | Name appears in `AGENTS.md`'s `excluded:` list | Concern is not applicable to this project. Proceed without. |
| **Absent (silent gap)** | A trigger matches a known pillar name, but no file exists and not excluded | Graceful degradation. Infer conventions from existing code. State the assumption in the response. Recommend creating the pillar. |

### 5.1 Special case: always-loaded pillars

`context` and `repo` (the only `always_load: true` pillars in the standard) do not degrade silently. If either is missing on a project claiming Pillars compliance, the agent pauses and asks the human to either create stubs or declare them excluded.

### 5.2 Exclusion form

`AGENTS.md` declares exclusions in a structured form:

```yaml
excluded:
  - name: observe
    reason: Vercel Analytics + built-in alerting cover our needs
  - name: i18n
    reason: English-only product
```

A bare list form (`excluded: [observe, i18n]`) is also valid; reasons are recommended but not required.

## 6. AGENTS.md requirements

A Pillars-compatible `AGENTS.md` contains:

- A reference to the Pillars standard.
- The 6-step loading protocol from section 4.
- The 4-state missing-pillar table from section 5.
- An `excluded:` block (may be empty).

`AGENTS.md` does *not* enumerate pillar names; it describes the protocol only. The pillar set lives in `agents/`. This means `AGENTS.md` does not grow as pillars are added.

A reference implementation is in this repository's [AGENTS.md](AGENTS.md).

## 7. Versioning

This spec uses semantic versioning. The current version is 1.0.1.

- Major: changes to frontmatter schema or loading mechanics that break existing pillars.
- Minor: additions to the schema or protocol that are backward-compatible.
- Patch: clarifications and corrections without behavior changes.

## 8. License

This specification is dedicated to the public domain under [CC0 1.0 Universal](LICENSE). No attribution is required to adopt or implement Pillars. Attribution is welcomed but never enforced.
