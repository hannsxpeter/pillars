# Pillars Conformance Assets

These assets test the portable routing behavior in `SPEC.md` without an external service or model call.

Run the deterministic suite:

```bash
python3 tooling/ci/validate_pillars.py \
  . --recursive-scopes \
  --standalone examples \
  --fixtures tooling/conformance/fixtures.yaml
```

Each fixture maps a task and target path to three ordered sets:

- `load`: selected pillars labeled `<scope>::<identity>`.
- `primaries`: direct trigger matches.
- `absent`: matching entries from the local offline catalog.

`root` labels the fixture project root. Nested labels are paths relative to that root. Fixture selectors use only the portable minimum matcher. Semantic retrieval can add matches in product use, but it must preserve this deterministic result.

The [benchmark protocol](BENCHMARK-PROTOCOL.md) describes a separate, optional live-model evaluation. [RESULTS-TEMPLATE.md](RESULTS-TEMPLATE.md) is intentionally blank. The repository does not claim scores that were not measured.
