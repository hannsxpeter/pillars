# Pillars

[![License: CC0-1.0](https://img.shields.io/badge/license-CC0--1.0-blue.svg)](LICENSE)
[![Status: stable 1.2](https://img.shields.io/badge/status-stable%201.2-green.svg)](CHANGELOG.md)
[![Spec: v1.2.2](https://img.shields.io/badge/spec-v1.2.2-green.svg)](SPEC.md)
[![AGENTS.md: compatible](https://img.shields.io/badge/AGENTS.md-compatible-purple.svg)](AGENTS.md)
[![Tooling: optional](https://img.shields.io/badge/tooling-optional-lightgrey.svg)](tooling/)
[![Tool: agnostic](https://img.shields.io/badge/tool-agnostic-blue.svg)](FAQ.md#how-is-this-different-from-cursor-rules-or-windsurfrules)

### Your AI coding assistant starts every session knowing nothing about your project. Pillars fixes that.

Pillars is a free, open standard for writing down what an AI assistant needs to know about your project before it touches your code. You write a handful of short files in plain language. Your assistant reads the ones that matter for the task at hand, and stops guessing.

It works with Claude Code, Cursor, Copilot, Codex, Gemini, opencode, Aider, and anything else that reads instructions from your repository. No account, no install, no vendor, no lock-in.

**[Start in five minutes](#start-in-five-minutes)** | **[See what a pillar looks like](#what-a-pillar-actually-looks-like)** | **[Read the spec](SPEC.md)**

---

## The problem, in plain terms

An AI coding assistant can read your code. It cannot read your reasons.

It never saw the meeting where your team picked one database over another. It does not know that the odd-looking workaround in the checkout flow is deliberate. It does not know which folder a new file is supposed to go in, or that you moved off a library six months ago and never want to see it again.

So it guesses. And the guesses look like this:

- It reaches for the wrong library, the one you deliberately abandoned.
- It puts files in the wrong place, and now your project has two conventions.
- It re-decides things you already decided, differently each time.
- It "fixes" behavior that was intentional, and quietly breaks something.

Linters and type checkers catch typos and type errors. They cannot catch intent. So the job falls to you: re-explaining the same context in every new chat, forever.

## The idea

Think about onboarding a new team member.

You do not hand them the codebase and wish them luck. You give them a short briefing. Here is what we are building. Here is how we work. Here is the thing that will surprise you in week one.

**Pillars is that briefing, written once, and read automatically by your AI assistant every time it works on your project.**

Each file covers one topic, and is called a pillar: what the product is, how the repository is organized, how data is stored, how login works, how you ship. A small file at your repository root tells the assistant how to find them.

The assistant only reads what is relevant. Ask it to change a database table and it reads your data pillar. Ask it to restyle a button and it does not.

## Before and after

| You ask | Without Pillars | With Pillars |
|---|---|---|
| "Add a customer table" | Picks a database library at random, invents a naming style, forgets your tenant column | Uses your library, your naming style, and flags the tenant rule before writing anything |
| "Where should this new component go?" | Guesses. Half your components end up somewhere new | Puts it where your other components live, because that is written down |
| "Speed up this query" | Rewrites it in raw SQL, bypassing the audit logging you rely on | Knows raw SQL is allowed in exactly one file, and why |
| "Why is this code like this?" | Assumes it is a bug and offers to remove it | Reads the recorded decision and leaves it alone |

## Who this is for

You do not need to be an engineer to get value from this, or to write one of these files.

| If you are | Pillars gives you |
|---|---|
| A solo builder or someone building with AI, without a deep coding background | A way to make the assistant stop contradicting itself between sessions |
| An engineering team | One source of truth that works across every teammate's tool of choice |
| A founder, product manager, or designer | A place to record product decisions in plain words that the AI will actually follow |
| An open-source maintainer | Context that travels with the repository, so contributors and their assistants start aligned |
| A consultant or agency | A repeatable way to hand a project over without a week of meetings |

Most of what belongs in a pillar is a decision, not code. "We use Stripe for payments and we never store card numbers ourselves" is a genuinely useful pillar line. So is "the pricing page copy is approved by legal, do not reword it." If you can explain it to a new hire, you can write it into a pillar.

## Start in five minutes

### Option A: just ask your assistant (no terminal required)

Open your AI coding tool in your project and paste this:

> *Adopt Pillars 1.2.2. Read SPEC.md and PILLARS.md from https://github.com/hannsxpeter/pillars/tree/v1.2.2. Scaffold the always-loaded stubs and applicable Core stubs, then remove created or excluded identities from the local catalog.*

It will set up the files and ask you a few questions about your project. Answer them in plain language.

### Option B: copy two files first

From your project folder:

```bash
curl -O https://raw.githubusercontent.com/hannsxpeter/pillars/v1.2.2/AGENTS.md
mkdir agents
curl -o agents/catalog.yaml https://raw.githubusercontent.com/hannsxpeter/pillars/v1.2.2/agents/catalog.yaml
```

Then paste the prompt from Option A. Pinning the version tag keeps the setup reproducible.

`catalog.yaml` is optional. It is a checklist of topics you have not written up yet, so the assistant knows what it does not know instead of quietly inventing an answer. Delete entries as you write the real thing.

**You are not expected to fill everything in on day one.** Two files, `context.md` and `repo.md`, are worth writing early. The rest accumulates as you make decisions. A half-written pillar is more useful than no pillar.

## What a pillar actually looks like

It is a normal markdown file. The block at the top tells the assistant when to read it. Everything below is written for a human.

```markdown
---
pillar: data
status: present
covers: [database schema, migrations, queries, storage]
triggers: [database, schema, migration, query, table, postgres]
must_read_with: [auth, config]
---

## Scope
The data layer: schema, migrations, query patterns, storage.
Request and response shapes live in `api.md`.

## Context
We use Drizzle ORM against Postgres 16. All table definitions live in
one file, `src/db/schema.ts`. Migrations are generated, never hand-written.
Every table has `id`, `created_at`, and `updated_at`.

## Decisions
- **Drizzle over Prisma.** We need raw SQL escape hatches for analytics.
- **One schema file.** It forces us to notice cross-table relations.

## Rules
- Never write raw SQL outside `src/db/raw.ts`. The audit logger only
  sees queries that pass through there.

## Watchouts
- A bug that allows cross-tenant joins is a security incident, not a
  feature bug. Pair with `auth.md` before touching anything tenant-scoped.

## Gaps
- Soft delete versus hard delete is still undecided. Ask before choosing.
```

Two things worth noticing. **Decisions** records the reasoning, not just the choice, so nobody relitigates it at midnight. **Gaps** is where you admit what is not settled yet, which tells the assistant to ask you instead of inventing an answer.

The full template has eight sections. You fill in the ones that earn their place and leave the rest empty. Details in [SPEC.md](SPEC.md).

## How it works

1. You add one file at your repository root, `AGENTS.md`, and a folder called `agents/` holding your pillars.
2. Each pillar declares, in a few lines at the top, what it covers and which words in a task should summon it.
3. When you give the assistant a task, it scans those declarations, loads the two always-on pillars plus whichever others match, and follows them.
4. Anything you have not written up yet degrades gracefully. The assistant states its assumption out loud and suggests writing that pillar, rather than silently guessing.

There are 24 topics in the standard catalog: 2 always loaded, 11 Core, 11 Common, plus as many project-specific ones as you need. Most projects use a focused subset, and deliberately marking a topic as "not applicable here" is a first-class answer. A command-line tool has no login screen, and saying so is useful information.

Full catalog with what each topic covers: [PILLARS.md](PILLARS.md).

## Why this does not rot like normal documentation

Most internal documentation dies quietly. Someone writes it, nobody reads it, it drifts out of date, and eventually everyone learns to ignore it.

Pillars is read on every session, by the assistant, out loud, in its output. When a pillar goes stale the assistant starts confidently doing the wrong thing, in front of you, today. That is annoying, and annoying gets fixed.

Regular documentation rots silently. Pillars rots loudly.

## What Pillars is not

- **Not a workflow tool.** It produces no work. It supplies context.
- **Not a rulebook.** These are briefings. The assistant is trusted to use judgment, not marched through a compliance checklist.
- **Not tied to one vendor.** Any assistant that reads markdown can use it.
- **Not software you install.** This repository defines the standard. Helper tools exist, and they are optional.

## Works with the tools you already use

| Form | Tools | Where |
|---|---|---|
| Native skill bundle | Claude Code | [`tooling/claude-skill/`](tooling/claude-skill/) |
| Paste-in prompts and per-tool setup guides | Cursor, Codex CLI, Gemini CLI, opencode, Aider, Windsurf, Cline, Continue, and anything else | [`tooling/prompts/`](tooling/prompts/) |

The standard itself works in every major AI coding tool with nothing installed. The helpers just automate the housekeeping: setting Pillars up, drafting a pillar from existing code, checking whether your pillars still match reality, showing which pillars a given task would load, and reconciling your pillars with a design doc, a product requirements doc, or your README.

Pick your tool's setup guide in [`tooling/prompts/`](tooling/prompts/), or paste a prompt file straight into your assistant's chat.

For teams who want automated checks, the repository also ships a small offline validator and test suite. It reads local files only, calls no model and no service, and is never required for compatibility.

## Learn more

| Document | Read it when |
|---|---|
| [SPEC.md](SPEC.md) | You want the precise, formal rules. Short enough to read in one sitting |
| [PILLARS.md](PILLARS.md) | You want the catalog of topics and guidance on which to use |
| [FAQ.md](FAQ.md) | You have a practical question about adopting it |
| [examples/saas-dashboard/](examples/saas-dashboard/) | You want to see a complete small project set up end to end |
| [examples/](examples/) | You want realistic sample pillars to copy from |
| [DESIGN-NOTES.md](DESIGN-NOTES.md) | You want to know why the standard is shaped this way |

This project uses its own standard. The [AGENTS.md](AGENTS.md) and [agents/](agents/) folder here are the real thing, not a demo.

## Plain-language glossary

- **Pillar.** One markdown file covering one topic, such as data or login.
- **AGENTS.md.** The small file at your repository root that tells the assistant how to find and load pillars.
- **Always-loaded pillar.** The two pillars read on every task: what the project is, and how the repository is organized.
- **Trigger.** A word or phrase that makes a pillar relevant to a task.
- **Stub.** A pillar you have started but not filled in. It tells the assistant to ask you rather than assume.
- **Excluded.** A topic you have marked as not applicable to this project, on purpose.
- **Gap.** Something you know is unresolved, written down so the assistant surfaces it instead of deciding for you.

## Repository layout

```
pillars/
├── README.md           # this file
├── SPEC.md             # the formal standard
├── PILLARS.md          # the catalog: topics, tiers, and boundaries
├── AGENTS.md           # this project's own loader, using the standard
├── FAQ.md              # adoption and usage questions
├── CONTRIBUTING.md     # how to contribute
├── CODE_OF_CONDUCT.md  # community standards
├── SECURITY.md         # security policy
├── CHANGELOG.md        # version history
├── LICENSE             # CC0 1.0 Universal
├── agents/             # this project's own pillars
│   ├── context.md
│   ├── repo.md
│   └── catalog.yaml    # optional index of topics not yet written up
├── examples/           # sample pillars and a full worked project
│   ├── data.md
│   ├── auth.md
│   ├── auth/
│   │   └── agent-registration.md
│   └── saas-dashboard/
├── tooling/            # optional helpers and repository QA
│   ├── claude-skill/   # Claude Code skill bundle
│   ├── ci/             # offline validator and tests
│   ├── conformance/    # routing fixtures and benchmark protocol
│   └── prompts/        # paste-in prompts and per-tool setup guides
└── DESIGN-NOTES.md     # design conversation log
```

## Status

Stable 1.2. This release is backward compatible with 1.1 and 1.0. Nothing about the file format or loading behavior changed, so existing adopters need no migration.

Version history: [CHANGELOG.md](CHANGELOG.md).

Honest note on evidence: the conformance suite here is repeatable and runs locally, and the standard has been pressure-tested against constructed scenarios. Published before-and-after adoption studies from real projects are still accumulating, and this repository does not present hypothetical tests as adopter evidence.

## Contributing

Proposals and pull requests are welcome, including from people who are not engineers. Wording, examples, and "this was confusing" reports are genuinely useful. See [CONTRIBUTING.md](CONTRIBUTING.md) for how changes to the standard are proposed.

## License

[CC0 1.0 Universal](LICENSE). Use Pillars freely, in any project, public or private, commercial or not, with or without credit. There is no catch. The standard wins by being adopted.
