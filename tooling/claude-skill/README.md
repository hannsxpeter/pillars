# Pillars Skills for Claude Code

Skill-form tooling for the [Pillars](https://github.com/hannsxpeter/pillars) standard. These skills run inside Claude Code and automate the meta-operations around adopting and maintaining Pillars: bootstrapping a new project, authoring pillars from code, and verifying pillars against the current codebase.

The standard itself ships separately as portable markdown. These skills are *one* form of tooling; a CLI, a Cursor wrapper, or other forms could exist alongside. None of them are required to use the standard; they make adoption easier.

## What's in this bundle

| Skill | Job |
|---|---|
| `pillars-init` | Bootstrap Pillars in a project. Detects archetype, drops AGENTS.md, scaffolds `./agents/`, writes stubs, and reconciles exclusions with the local catalog. |
| `pillars-author` | Author a specific pillar from the codebase. Scans relevant code, drafts the 8-section pillar following the template, asks before writing. |
| `pillars-verify` | Walk pillar Context claims against the current codebase. Flag drift, suggest fixes. Manual lightweight check; no CI integration. |

## Install

These skills follow Claude Code's standard skill directory layout. To install:

1. Locate your Claude Code skills directory. On macOS/Linux this is typically `~/.claude/skills/`. If you're using a custom location, substitute it below.
2. Copy each skill's directory into that location:

```bash
cp -r tooling/claude-skill/pillars-init ~/.claude/skills/
cp -r tooling/claude-skill/pillars-author ~/.claude/skills/
cp -r tooling/claude-skill/pillars-verify ~/.claude/skills/
```

3. Restart Claude Code (or open a new session) for the skills to register.

If your Claude Code installation uses a plugin marketplace or a project-scoped skill folder, copy the directories there instead. The skills are self-contained.

## Use

In a Claude Code session, invoke skills explicitly with a slash command or by natural-language request that matches the skill description.

**Bootstrapping:**

```
/pillars-init
```

or

> Set up Pillars on this project.

The skill detects the project archetype, scaffolds `AGENTS.md` and `./agents/`, writes stubs, and sets archetype exclusions.

**Authoring a pillar:**

```
/pillars-author data
```

or

> Author the data.md pillar by scanning my codebase.

The skill scans the relevant code (using the pillar's typical trigger areas), drafts the 8 sections, and presents the draft for your approval before writing.

**Verifying pillars:**

```
/pillars-verify
```

or

> Check whether my pillars still match the codebase.

The skill walks each pillar's Context section and checks claims against current code. Flags drift, suggests fixes.

## What these skills don't do

- **No CI execution inside the skills.** The repository's optional deterministic validator and conformance suite are the CI surface; the skills remain interactive.
- **No drift remediation.** The verify skill flags drift; it doesn't auto-fix. Fixing is a human + agent collaboration on what the current truth is.
- **No cross-repository orchestration.** Each skill operates on the current repository, including its applicable nested scopes.

## Versioning

Skill versions are tracked in each skill's frontmatter. Skills are versioned independently from the Pillars standard but should always be compatible with the latest minor version of the standard.

| Skill | Version | Standard compatibility |
|---|---|---|
| `pillars-init` | 0.4.0 | Pillars v1.1.0+ |
| `pillars-author` | 0.3.0 | Pillars v1.1.0+ |
| `pillars-verify` | 0.2.1 | Pillars v1.1.0+ |

## License

[CC0 1.0 Universal](../../LICENSE). Same as the standard. Use freely.
