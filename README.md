# Lesson 03 — Research, feedback, and verification

This is an AI-assisted coursework submission draft, not a benchmark claim.
The actual HyperResearch run remains **blocked on verification**.
Formal **RACE and FACT were not run or submitted**.

Authorized public submission repository: [AKDA0314/research-agent-coursework](https://github.com/AKDA0314/research-agent-coursework).

## Latest update — 2026-11-04

- **Current state:** the latest paid run failed at proposal 1 (25 atoms exceeded the 16-atom limit). The overflow repair is tested offline, **not yet rerun against the live model**. No claim of `done`, stability, or instructor acceptance.
- **63 offline tests pass.** New regressions use saved failed responses, including evidence binding, calculation formats and overflow handling.
- **Six real run records are now published as review copies:** [run-by-run history](docs/practice-history.md), [reports and traces](evidence/live-runs/README.md), [export manifest](evidence/live-runs/export-manifest.json). Full API payloads and full frozen corpora remain local; public traces retain all events but replace source bodies with hashes.
- **The 2 km task is a new version:** [task](tasks/furlong-2km-v2/task.md), [scope and snapshot guide](docs/furlong-2km-v2.md). It is not the original HyperResearch task and does not establish a controlled same-task comparison.
- Latest implementation notes: [binding repair](docs/binding-fix.md), [V2 regression repair](docs/furlong-review-fix.md), [overflow repair](docs/atom-overflow-fix.md).

## Reproduce the offline work

The historical rule-based runner is now isolated in `src/offline_rules.py`.
The new [live runner guide](docs/live-run.md) explains the DeepSeek entry point in
`src/six_step.py`: actual model planning, proposals, checks and report generation
from the exact task and saved source bodies. It does not import the handcrafted
classroom candidates. Original local run artifacts are excluded from Git; selected public review copies are exported separately.

The [first real DeepSeek run and comparison](docs/live-comparison-01.md) used
9 generation calls on 2026-11-01, with an estimated CNY 0.733804 at conservative
peak rates. A report was generated but remains `blocked_review`. The comparison
documents report errors, checker misses and audit false alarms; it is not a
stability or framework-superiority claim.

Python 3.9+ and the standard library are sufficient for the new coursework code:

```sh
python3 scripts/run_offline.py
python3 -m unittest discover -s tests -v
python3 scripts/validate_submission.py
```

These commands make no network requests, invoke no language model, and do not change the original research run. Generated JSON goes to `results/`.

## Submission map

| Requirement | Artifact | Status and scope |
|---|---|---|
| 1: ≤30-line ReAct loop | [Code](src/react_loop.py), [explanation](docs/react.md) | Executable rule-based loop; AI-authored scaffold for learner review |
| 1: success and inverted-value failure | [Success](results/react-success.json), [failure](results/react-conflict.json) | Frozen classroom example, not a live model run |
| 2: actual reproduction and gate | [Report](docs/reproduction-report.md), [manifest](evidence/run.json), [gate JSON](evidence/run-verify-full.json) | Actual light run; blocked, 8/9 checks pass |
| 2: data flow and actual returns | [Data flow](docs/dataflow.md), [search](evidence/evidence-search-return.txt), [fetch](evidence/evidence-fetch-return.txt) | Historical returned text; fetch JSON was truncated by the original command |
| 2: isolation and one-factor experiment | [Isolation](results/isolation.json), [property replay A/B](results/property-ablation.json) | Source-module isolation + deterministic offline checker ablation; not a second HyperResearch agent run |
| 2: product comparison and evaluation protocol | [Comparison](docs/product-comparison.md), [RACE/FACT](docs/evaluation.md) | Public/source evidence; no commercial same-task experiment or official benchmark score |
| 3: six-step framework | [Live code](src/six_step.py), [live guide](docs/live-run.md), [historical replay](src/offline_rules.py) | Live model path separated from the deterministic classroom demonstration |
| 3: same original property task | [Frozen task](evidence/task.md), [trace](results/six-property.json), [seven-row comparison](docs/six-step.md#same-task-comparison) | Same task text replayed against frozen gaps/assumptions; incomplete evidence remains incomplete |
| 3: success/conflict demonstrations | [Success](results/six-success.json), [conflict](results/six-conflict.json) | Same checkpoint teaching task, six-unit ceiling; not full-property success |
| 3: same-source property-subtask pair | [REIWA success](results/six-reiwa-success.json), [REIWA conflict](results/six-reiwa-conflict.json) | Same explicitly narrowed historical-price task and quotation; six units each |
| 2/3: actual HyperResearch checker A/B | [Raw results](results/hyperresearch-binding-ablation.json), [experiment guide](docs/verification-update.md) | Actual pinned citecheck functions + one binding-rule change; temporary fixture DB, no LLM or host rerun |
| All: English README and AI disclosure | This file, [disclosure](docs/AI_USE.md), [submission status](docs/submission-status.md) | Learner explanation and instructor acceptance remain pending |

## Evidence boundaries

The preserved HyperResearch snapshot is version 0.11.1, commit `75b1ecfb2891184fad2cc1a2ddf9abe476f5b54c`.
Its real run used the property task; the six-step replay uses the same task text, but no fresh retrieval.
The price/inventory evidence gaps were manually curated from the preserved run, so the replay is not an independent rediscovery of those gaps.
The checkpoint fixture contains the sentence supplied by the course and handcrafted candidates; it is not an official downloaded dataset.
The added REIWA pair uses a real saved quotation and an explicitly narrowed subtask, not a completed full property investigation. Candidate mutations are authored tests, not original report errors.
Success here means the narrow rule-based check passed, not that an LLM became better or a human independently reviewed the result.
The six operation units in the classroom are not USD and are not directly comparable to HyperResearch's `budget_usd`.

## Privacy, provenance, and rights

Only whitelisted evidence is exported. Local usernames and absolute home paths are replaced; the export manifest records before/after SHA-256 digests.
Virtual environments, credentials, OAuth URLs, full chat sessions, and browser profiles are excluded.
The submission still contains the public property address used in the assignment; prefer a private repository if that research interest is sensitive.
Historical reports and regression fixtures include selected source material needed to inspect failures. Full raw fetch archives and complete frozen corpus files are not part of this export.
Upstream HyperResearch source is linked at its commit, not vendored; it is MIT-licensed upstream. Third-party materials retain their original rights.

## AI assistance and learner responsibility

AI inspected existing files, drafted the new Python scaffold/tests/docs, and assembled the sanitized evidence package.
Claude's earlier research and closeout are preserved as historical evidence; new offline results are separately labeled.
The learner has not yet personally explained all six decisions or rewritten the AI-authored ReAct loop.
If “handwritten” requires unaided authorship, this scaffold must be revised by the learner before final submission; this README does not claim otherwise.
See the [remaining checklist](docs/submission-status.md) before presenting the work as fully accepted coursework.

Evidence-binding repair and regression evidence: [binding-fix](docs/binding-fix.md).
