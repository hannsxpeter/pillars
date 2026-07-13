# Optional Live-Model Benchmark Protocol

This protocol evaluates whether Pillars improves project-aligned task planning. It is not part of standard conformance, and the repository publishes no live-model result until the procedure has actually been run.

## Question

Given the same repository snapshot, task, and project facts, does a model with the computed Pillars load set produce a plan that better respects those facts than the same model using a flat instruction file or no project instructions?

## Controls

1. Pin the repository commit, model identifier, model settings, system prompt, and task set.
2. Start each run in a fresh context.
3. Condition A receives repository files through the normal tool plus the Pillars protocol and computed load set.
4. Condition B receives one flat `AGENTS.md` containing the same project facts as Condition A's available pillars, with no task routing.
5. Condition C receives the same repository files and task but no project instruction files.
6. Keep project facts equivalent between Conditions A and B. The comparison should isolate routing and organization rather than missing information.
7. Randomize condition order and blind graders to condition labels.
8. Run at least three repetitions per task and report every attempted run, including failures.

## Task set

Use at least twelve tasks spanning:

- Repository placement and naming.
- Data, API, auth, and UI changes.
- A task requiring a direct dependency.
- A task requiring conditional `see_also` loading.
- A locally absent concern.
- A nested-scope conflict.
- A task unrelated to any routed pillar.

Store task text and the expected deterministic load set with the results.

## Scoring

Two independent graders score each plan from 0 to 2 on:

- Correct project facts.
- Compliance with explicit Rules.
- Correct file placement.
- Respect for Decisions and Watchouts.
- Appropriate handling of Gaps.
- Avoidance of irrelevant constraints.

Also record instruction-context words or tokens supplied to each condition and time to first complete plan when the host exposes those measurements. Treat efficiency as a separate outcome rather than folding it into the quality score.

Resolve grader disagreements by reporting both raw scores and an adjudicated score. Report per-task results, means, confidence intervals when justified, and the full rubric. Do not collapse all outcomes into one score without the underlying table.

## Publication requirements

- Record date, commit, model identifier, settings, grader identities or model identifiers, and raw outputs.
- Disclose tasks excluded after collection and why.
- Separate deterministic conformance failures from model-quality failures.
- Do not call hypothetical pressure tests adopter evidence.
- Use [RESULTS-TEMPLATE.md](RESULTS-TEMPLATE.md) and link raw artifacts.
