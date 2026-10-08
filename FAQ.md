# FAQ

Questions about Pillars, ordered from "I just found this" to "I am implementing the spec."

New here? Start with [the README](README.md).

## Starting out

### What is this, in one sentence?

A way to write down what your AI coding assistant needs to know about your project, in plain markdown files it reads automatically, so it stops guessing and re-deciding things you already settled.

### Do I need to be a programmer to use it?

No. The files are plain markdown, and most of what belongs in them is a decision rather than code. "We use Stripe and never store card numbers ourselves" is a good pillar line. So is "this pricing copy was approved by legal, do not reword it."

You do need a project with code in it, and an AI coding tool. Writing the files themselves is closer to writing an onboarding doc than to programming, and your assistant can draft most of them from your existing code if you ask.

### What does it cost?

Nothing. Pillars is released under [CC0](LICENSE), which is as close to public domain as a license gets. There is no account, no company behind a paywall, no premium tier. Use it in commercial work without attribution if you like.

### How long does setup take?

About five minutes for a new project: copy one file, create one folder, write two short starter pillars. Same for an existing project.

The pillars themselves fill in over the life of the project, as you make decisions. There is no "fill in all 24 topics before you start" requirement, and there never will be.

### Do I have to write all 24 topics?

No. The catalog exists so you consider each topic once, not so you complete each one. Command-line tools commonly exclude 11 of them, and marking a topic as not applicable is a fully supported answer, recorded in one line. See [PILLARS.md](PILLARS.md) for suggested starting points by project type.

### Can I adopt it gradually?

Yes, and that is the intended path. Start with the two always-loaded pillars: what the project is (`context.md`) and how the repository is organized (`repo.md`). Add others as decisions get made. Anything you have not written up yet either gets marked as a known gap or simply produces no claim, rather than a confident wrong guess.

### Do I need to install anything?

No. The daily loop is just markdown files that your AI tool already reads.

There is an optional validator for teams who want automated structure checks in CI ([`tooling/ci/validate_pillars.py`](tooling/ci/validate_pillars.py)). It reads local files, calls no model and no external service, and compatibility never depends on it. If you want a structure check without any setup, paste [`tooling/prompts/pillars-check.md`](tooling/prompts/pillars-check.md) into your assistant instead.

### Which AI tools work with this?

Any tool that reads project instructions from your repository root. That includes Claude Code, Codex CLI, GitHub Copilot, Cursor, Gemini CLI, opencode, Aider, Windsurf, Cline, and Continue, either natively, via a one-line shim file pointing at `AGENTS.md`, or via a config entry that loads it (Aider's `read:` list, for example). Each tool's setup is in [`tooling/prompts/`](tooling/prompts/).

If your tool ignores project-level instructions entirely, Pillars cannot help you. That is increasingly rare.

### Is this an Anthropic thing? A Claude thing?

No. Claude and Claude Code come up as examples because they are a common way people arrive here. The standard is tool-agnostic by design and deliberately accepts no tool-specific extensions.

## How it compares

### Why not just use one `AGENTS.md` file?

For a small project, one file is fine, and Pillars still uses `AGENTS.md` as the entry point. Pillars sits underneath that convention rather than replacing it.

The problem shows up as a project grows. That single file either bloats, in which case the assistant reads everything every session and the important parts get buried, or it stays thin, in which case most of what matters lives in someone's head. Pillars splits it into focused files and adds a way for the assistant to load only what the current task needs.

### How is this different from Cursor rules or `.windsurfrules`?

Those work in exactly one tool. Pillars is portable: any assistant that reads markdown can use it. You get one source of truth that survives your team using different tools, and survives whatever ships next year.

### How does it relate to `design.md`?

They complement each other. Keep `design.md` as the rich design brief: product intent, user journeys, the reasoning behind the experience. Use pillars as task-routed working memory: the durable facts, constraints, and decisions an assistant needs while implementing something specific.

Do not sync them silently. [`tooling/prompts/pillars-sync-design.md`](tooling/prompts/pillars-sync-design.md) produces a report of what each document should learn from the other, plus conflicts that need a human decision.

### Is your `auth.md` the same as WorkOS's `auth.md`?

No. Same filename, nothing else in common.

The Pillars `auth.md` lives at `agents/auth.md` and briefs a *coding* assistant on how your project handles identity and access. WorkOS's [`auth.md`](https://github.com/workos/auth.md) is a runtime protocol: a file your live service publishes at `https://yourservice.com/auth.md` so an *autonomous agent* can sign itself up on a user's behalf.

Different layer, different audience, different lifecycle. They coexist fine because they live at different paths. If your project does support agent-facing registration, document it for your coding assistant like any other integration, either in your `auth.md` pillar or a focused sub-pillar such as `agents/auth/agent-registration.md`. Worked example: [examples/auth/agent-registration.md](examples/auth/agent-registration.md).

## Living with it

### Will this rot like every other documentation system?

It can, if nobody ever updates it. But there is a structural difference worth understanding.

Normal documentation rots silently. Nobody reads it, so nobody notices it is wrong.

Pillars are read on every session, and stale ones produce visibly wrong behavior in front of you today: the assistant confidently suggests the library you abandoned. That is annoying, and annoying gets fixed. Drift-detection helpers reduce it further. Pillars rots loudly.

### What if two pillars contradict each other?

That usually means your project contains a real contradiction, and the pillars just made it visible. Resolve it by deciding which pillar is authoritative, updating the other to defer to it, or reconsidering where the boundary between them sits.

### Can pillars cover non-code topics like legal, compliance, or business rules?

Yes, when a coding assistant needs them to do its job correctly. `compliance.md` is exactly this. Business-rule pillars such as `orders.md` or `inventory.md` are common. The test is simple: would getting this wrong produce bad code or a bad product decision? If so, write it down.

### How does this work in a monorepo?

Put shared guidance in the root `AGENTS.md` and `agents/`. A package that needs its own routing or overrides can add its own pair. For a task inside that package, the assistant applies scopes from the root inward. Non-conflicting guidance accumulates, and the nearest scope wins any conflict.

Keep a single root scope when packages are similar. Nested scopes earn their place when packages have genuinely independent stacks, layouts, or product boundaries, not as an excuse to duplicate every pillar.

### What maintenance helpers exist?

All of these report and recommend. None of them write files behind your back.

| Prompt | What it does |
|---|---|
| `pillars-map-task.md` | Shows which pillars would load for a given task, and why |
| `pillars-find-gaps.md` | Collects every unresolved gap across your pillars into one list |
| `pillars-trim.md` | Flags bloat, duplication, and over-prescription |
| `pillars-sync-design.md` | Reconciles a root `design.md` with your pillars |
| `pillars-sync-prd.md` | Reconciles product requirements docs with your pillars |
| `pillars-sync-readme.md` | Reconciles your README with your pillars |

### Can I version individual pillars?

The standard does not define per-pillar versioning. Your git history is the version log.

If a pillar gets a major rewrite, note it in that pillar's own Decisions section. When reversed or superseded choices need to stay visible along with their original reasoning, which a flat Decisions list fights because the natural edit is to delete the stale entry, promote the reasoning into a decision sub-pillar such as `arch/decisions`. See [Common sub-pillar patterns](PILLARS.md#common-sub-pillar-patterns).

### Is it stable enough to adopt?

Yes. Version 1.2.2 preserves the stable 1.0 schema and single-scope behavior, plus every 1.1 routing rule. It adds catalog guidance only. Any future incompatible change requires a new major version.

### Do tooling updates break my project?

No. Only changes to [SPEC.md](SPEC.md) change what it means to be Pillars-compatible. Prompts, skills, install guides, and examples can all improve without touching your files. [CHANGELOG.md](CHANGELOG.md) labels tooling-only releases as "Standard itself unchanged" so you can tell at a glance whether a release affects you.

### How often does the standard change?

Slowly, on purpose. Major versions are years apart. Minor versions land quarterly or when an additive change is needed. Patch versions are continuous.

## Design decisions, for the curious

These answer "why is it built this way," and assume more familiarity with the spec.

### Why "briefings, not rulebooks"?

Coding assistants are capable. Over-constraining them with long rule lists, banned-pattern catalogs, and compliance-style prose removes their judgment and produces brittle output. Pillars surfaces what the assistant genuinely cannot infer from code, such as project identity, past decisions, and hard-won lessons, then trusts it to apply that well. The Rules and Watchouts sections exist for the residual: things that cannot be derived from context alone.

### What is the "earn your keep" principle?

Each section in a pillar gets populated only when it adds something the others do not. If Context already implies a Rule, do not restate the Rule. If a Workflow is obvious from Context, skip it. Empty sections are marked `(none)`. Pillars stay tight and the assistant gets clean signal.

### Why eight sections in the template?

It is the smallest set that covers both briefing (Scope, Context, Decisions) and prescription (Rules, Workflows, Watchouts) without forcing one shape onto every topic. Sections 3 through 6 are optional under the earn-your-keep principle.

### Why load only direct dependencies, not the whole chain?

Predictability. Reading a pillar's frontmatter tells you exactly what loads alongside it. Following the chain transitively hides coupling depth from authors and creates "why did this load everything" surprises. Pillars that turn out to be needed constantly graduate to `always_load: true` instead of hiding as transitive dependencies.

### Why folder-based sub-pillars instead of a `parent:` field?

Visual hierarchy documents itself. `agents/data/migrations.md` is obviously a sub-pillar of `data`. A frontmatter field would require opening the file to learn the same fact. Hugo, Jekyll, Astro, MkDocs, and essentially every static site generator use folders for hierarchy, so the pattern is already familiar.

### How do I reference a sub-pillar?

By its path-derived identity. `agents/auth.md` is `auth`; `agents/auth/agent-registration.md` is `auth/agent-registration`. The frontmatter `pillar` value stays the leaf filename, `agent-registration`. Bare references resolve top-level pillars only, so two parents can safely have sub-pillars with the same leaf name.

### Is trigger matching implementation-defined?

Implementations may add semantic matching on top, but 1.1 defines a portable minimum so results stay comparable. ASCII letters are lowercased, punctuation becomes spaces, and a selector matches a contiguous token sequence. That means `schema-change` matches `Schema change`, while `api` does not match `capital`. Primary triggers, catalog triggers, and conditional `see_also` checks all use the same baseline.

### What exactly is `agents/catalog.yaml`?

An optional local index of topics this project knows are absent. It carries identities and triggers so a gap can be found without network access or model memory. Present pillars never need catalog entries, since their own frontmatter routes them, and exclusions stay in `AGENTS.md`. A project with no catalog behaves exactly like 1.0 for present pillars, and simply makes no claim about topics it has not recorded.

### Can I use only some pillars and not others?

Yes. Five states cover incomplete adoption: present pillars load, stubs prompt the assistant to ask, exclusions are treated as not applicable, locally cataloged absences degrade to explicit stated inference, and genuinely unknown topics produce no Pillars-specific claim at all.

### Why is tooling optional?

Standards succeed by being portable and small. Tooling is a multiplier, not a substitute. Pillars 1.2.2 defines compatibility purely through local text files and loading behavior, so adoption never depends on which helper form you use. Optional tooling lives under `tooling/` where the friction it relieves is well understood.

## Getting involved

### How do I propose a new pillar for the standard?

Open an issue with the `feature` template. Describe the kind of project that needs it, the gap it fills, and how it relates to existing pillars. Discussion happens in the issue. See [CONTRIBUTING.md](CONTRIBUTING.md).

### How do I report a problem?

Open an issue. Use the bug template for spec ambiguities or contradictions, the question template for clarifications, and the feature template for proposals.

### Can I contribute if I am not an engineer?

Yes, and it is genuinely useful. Clearer wording, better examples, and honest "this section confused me" reports improve adoption more than most spec changes do.
