# Lesson 03 — Research, feedback, and verification

This is an AI-assisted coursework submission draft, not a benchmark claim.
The actual HyperResearch run remains **blocked on verification**.
Formal **RACE and FACT were not run or submitted**.

## Reproduce the offline work

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
| 3: six-step framework | [Code](src/six_step.py), [six-step guide](docs/six-step.md) | Six duties, proposal/check budget, separate stop and review state |
| 3: same original property task | [Frozen task](evidence/task.md), [trace](results/six-property.json), [seven-row comparison](docs/six-step.md#same-task-comparison) | Same task text replayed against frozen gaps/assumptions; incomplete evidence remains incomplete |
| 3: success/conflict demonstrations | [Success](results/six-success.json), [conflict](results/six-conflict.json) | Same checkpoint teaching task, six-unit ceiling; not full-property success |
| All: English README and AI disclosure | This file, [disclosure](docs/AI_USE.md), [submission status](docs/submission-status.md) | Learner explanation and repository upload require human confirmation |

## Evidence boundaries

The preserved HyperResearch snapshot is version 0.11.1, commit `75b1ecfb2891184fad2cc1a2ddf9abe476f5b54c`.
Its real run used the property task; the six-step replay uses the same task text, but no fresh retrieval.
The price/inventory evidence gaps were manually curated from the preserved run, so the replay is not an independent rediscovery of those gaps.
The checkpoint fixture contains the sentence supplied by the course and handcrafted candidates; it is not an official downloaded dataset.
Success here means the narrow rule-based check passed, not that an LLM became better or a human independently reviewed the result.
The six operation units in the classroom are not USD and are not directly comparable to HyperResearch's `budget_usd`.

## Privacy, provenance, and rights

Only whitelisted evidence is exported. Local usernames and absolute home paths are replaced; the export manifest records before/after SHA-256 digests.
Virtual environments, credentials, OAuth URLs, full chat sessions, and browser profiles are excluded.
The submission still contains the public property address used in the assignment; prefer a private repository if that research interest is sensitive.
The external source page is represented by a short quotation and URL, not a full redistributed webpage.
Upstream HyperResearch source is linked at its commit, not vendored; it is MIT-licensed upstream. Third-party materials retain their original rights.

## AI assistance and learner responsibility

AI inspected existing files, drafted the new Python scaffold/tests/docs, and assembled the sanitized evidence package.
Claude's earlier research and closeout are preserved as historical evidence; new offline results are separately labeled.
The learner has not yet personally explained all six decisions or rewritten the AI-authored ReAct loop.
If “handwritten” requires unaided authorship, this scaffold must be revised by the learner before final submission; this README does not claim otherwise.
See the [remaining checklist](docs/submission-status.md) before presenting the work as fully accepted coursework.
