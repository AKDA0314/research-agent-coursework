# Furlong V2 failed-run regression repair — 2026-11-04

Failure used: `.local-runs/furlong-2km-run-20261104-184811` (9 completed calls, CNY 0.503846 estimated, `blocked_review`). This repair does not change that result.

## Changes and evidence

- The actual Q3C6 stored a JSON derivation inside `calculation`. The old binder read only `derivations`. The binder now safely parses that legacy field, records its origin, and applies the same bound-input, Decimal arithmetic and unit checks. Malformed JSON, conflicting fields, wrong results and unsafe expressions still fail. New prompts specify one `derivations` array.
- A proposal may contain explicitly authored `atoms`, each with its own statement and bindings. The program flattens these, assigns independent IDs, preserves group/atom lineage, and checks every atom separately. It never invents a narrower claim or inherits a parent's evidence. Q1C1's quoted price/date can therefore be submitted independently from an unbound configuration; the original compound is still rejected.
- Numeric bedroom/bathroom/car counts must have corresponding labelled evidence. The actual Q2C3 false-positive now receives a deterministic veto even if the model says `supported`. Explicit square-metre notation must be bound; plain `172m` does not prove `172m²`. JSON distance/circle flags must include record identity in the same quote. These are conservative guards, not a universal semantic verifier.
- Bare historical price fields do not silently acquire AUD. Proposal instructions request existing normalized currency records, year/subject context and transformation notes. The actual Q1C8 remains rejected with its old bindings; an explicitly bound existing normalized record passes the mechanical checks.
- Verified spans now carry frozen `source_kind` and `transformation` metadata. Writer instructions require sample distance, circle membership, source type, period and access date columns, with unresolved fields clearly marked. Planning area overlap must not be invented.
- Audit coverage separates `covered`, `disclosed_gap`, and `missing`. A disclosed gap must point to an exact report quotation expressing the gap, with `evidence_status=missing`. This acknowledges disclosure, not fulfillment of the underlying data requirement. Real issues and a raw model rejection still block. The writer/auditor must distinguish an unverified candidate from proof that a source contains no data.

Historical repair setting: eight groups, with up to four atoms per group and sixteen total atoms per round. That total-output guard subsequently caused the 19:02 run to fail; the [overflow follow-up](atom-overflow-fix.md) now accepts up to 32 structurally valid atoms, checks at most 16, and persists the rest as unverified. Output allowances are now 7,000 tokens per proposal and 8,000 per checker; report/audit allowances remain 7,000/5,000. The six classroom units, maximum nine API calls, no automatic retries and client-side CNY 5 ceiling remain unchanged. More output headroom can increase cost; each request is checked against the remaining estimated monetary allowance.

## Validation and limits

58 offline tests passed, including 12 new tests using [the actual failed-run fixture](../tests/fixtures/furlong-v2-failures.json) and [regression tests](../tests/test_furlong_failure.py). An end-to-end mocked three-pair run checks the ledger, trace, calculation normalization, partial-atom selection and final gate. Mock verdicts are test inputs, not research evidence; fixtures are never supplied to the live generator.

No paid model request was made for this repair. Offline tests do not establish live model stability, research completeness or a future audit pass. Semantic subject matching, scope and dates still need model and human review. The fixed corpus still lacks exhaustive two-timepoint inventory, a complete comparable sales population, complete current development pipeline data and survey-grade parcel locations.

Before/after hashes cover 231 original files (including the task, snapshot preparation, latest report/logs and earlier failed runs). Preservation evidence is saved locally under `.local-runs/review-fix-20261104/`; the portable result is [review-fix-regression.json](../results/review-fix-regression.json).

Task SHA-256: `5559615bee7d0d2c8d8ccb6c4c4ebe1a5678af873ae4fa7cc76f9eba2d6e7f4a`

Corpus SHA-256: `0babe546e045e7c192cf7e63b1a1a15bd1106b869805ffbe7cc870d398641d3f`

This is the same V2 task/snapshot as the latest failed run, not the earlier 1 km task. Because candidate decomposition and checking rules changed, raw supported-claim counts should not be used as a quality score across versions. Compare actual supported statements, omissions, audit issues and costs instead.

## Run again

From the repository root:

```sh
new_run=".local-runs/furlong-2km-fixed-$(date +%Y%m%d-%H%M%S)"
python3 scripts/run_live.py run \
  --key-file .local-runs/deepseek.env \
  --task tasks/furlong-2km-v2/task.md \
  --frozen .local-runs/furlong-2km-20261104/frozen \
  --out "$new_run" \
  --max-cny 5
```

Every run uses a new directory. Inspect `report.md`, `report-audit.json`, `claims.json`, `trace.jsonl` and `run.json` there. A successful same-model audit yields `report_generated`; human review stays pending and `deliverable` stays false. This repair does not force `done` or overwrite any failed run. CNY 5 is the client's conservative estimated budget, not a provider-enforced account spending cap.
