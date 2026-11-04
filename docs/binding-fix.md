# Evidence binding repair — 2026-11-04

The saved Q1C4 and Q1C6 quotes were genuine, but incomplete. Q1C4 omitted the
$975,000 amount; Q1C6 omitted the 90.60% change (and its period). Those numbers
exist elsewhere in the frozen sources. This establishes a binding defect, not
that the numbers were invented or that every part of either claim is correct.

## What changed

- `binding_check` in [six_step.py](../src/six_step.py) verifies each quote against
  its identified source and records the source-body hash, character offsets and
  line numbers. Multiple valid spans may jointly support one claim.
- Monetary and percentage anchors are normalized with Decimal, including comma,
  full-width and common scale formatting. An absent anchor forces `missing`, even
  when the model returns `supported`. Different currencies/units are not silently
  exchanged. An ambiguous `$` is not assumed to mean USD or AUD.
- The semantic checker receives a whitelist of candidate fields and verified
  bound spans, not the full corpus. Its instructions forbid borrowing evidence
  from the task, other claims or memory. Proposals still read the frozen corpus.
- Missing/conflicting claims enter `gaps.json`, subsequent proposal context and
  the report/audit inputs. `claims.json` and `bind_verify` trace events retain the
  model verdict, program validation and effective verdict separately.
- Derived values require explicit named, bound inputs and a limited arithmetic
  expression. Decimal arithmetic is recomputed without `eval`. A free-text
  formula or a `calculation` label alone cannot bypass the numeric guard.
  Correct arithmetic still needs semantic checking of units and assumptions.
- Raw API response artifacts remain intact. The final human-review gate and
  existing status vocabulary are unchanged; this repair does not create `done`.

## Evidence and commands

From the repository root:

```sh
python3 -m unittest discover -s tests -p 'test_binding.py' -v
python3 scripts/validate_submission.py
```

[Regression tests](../tests/test_binding.py) use a
[fixture extracted from the real failed run](../tests/fixtures/binding-cases.json),
plus synthetic counterexamples. Fixture labels never enter live generation.
[Offline before/after results](../results/binding-regression.json) show the two
old bindings rejected and proposed replacement spans accepted by the mechanical
binding gate. These are proposed repairs, not edits to the original report and
not new model-reviewed research conclusions.

37 tests pass in the complete suite, including 11 new binding tests. Tests cover
both real failures, complete replacement spans, wrong sources, fabricated quotes,
multiple spans, numeric formatting, currency/unit differences, safe calculations,
a checker that wrongly approves everything, downstream gaps and trace retention.
The semantic counterexample deliberately shows that “the number appears” alone
cannot distinguish houses from units or increase from decrease.

## Harness use and preservation

Official `@deepseek-ai/dsh@0.2.1-rc.5` was run with DeepSeek Flash in an isolated
code copy. It produced code and tests, but its session ended with a Messages
stream idle timeout. Review found invalid exceptions that could waive missing
money evidence, incomplete context isolation, and incorrect test expectations.
Those draft rules were not adopted. Codex reimplemented and tested the guard,
retaining the useful separation of span validation, model judgment and effective
verdict. This is AI-assisted work, not a student handwritten implementation.

Local Harness events, rejected draft, starting code copies and hash manifests
remain under `.local-runs/binding-fix-20261104/` (gitignored). A portable summary is
in [binding-regression.json](../results/binding-regression.json). Reported token
usage gives a conservative estimate of CNY 2.406366 at the project's existing
price snapshot; the timed-out final request has unknown usage, so this is not a
complete bill or a provider-enforced spending cap. No automatic Harness retry or
new research run was performed.

All 70 hashed historical run/frozen-input files remain byte-for-byte unchanged.
The original reports, `failed`/`blocked_review` records and original HyperResearch
`blocked` state are preserved.

## What this can and cannot improve

This fixes a reproducible false acceptance path and makes omissions visible
before writing a report. Bound evidence also gives the checker a smaller,
consistent context. Explicit derivations distinguish observed numbers from
computed results. These are reliability improvements demonstrated by regression
and integration tests, not a measured improvement in real report quality.

Numeric syntax coverage is intentionally limited. Dates, subject, region,
negation, sample size, statistical definition and relevance still need semantic
review. The generator/checker use the same model; a dishonest semantic verdict
can still pass a structurally valid but misleading quote. Missing data cannot be
repaired by this code. There is no adaptive retrieval or automatic rebind loop
added here, no new live quality/stability comparison, and no formal RACE/FACT run.
A next quality evaluation should freeze task/corpus/model/budget, retain every
attempt, compare pre/post defect rates and have a human inspect accepted claims.

## Live follow-up — 2026-11-04

The user-run repaired pipeline completed nine calls but remained blocked_review.
Inspection exposed a new false rejection: `per cent` was not recognized by the
numeric parser. This spelling is now supported with two regression tests (39
total passing); the historical run was not modified or rerun. See the
[comparison record](../results/repaired-run-comparison-20261104.json).
Partial semantic support is still incorrectly approved in some model verdicts,
and generated calculations do not consistently follow the structured contract.
More rejections and lower token cost do not establish better research quality.
