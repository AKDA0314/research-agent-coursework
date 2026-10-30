# Assignment 1: explanation (eight sentences)

1. The loop writes an explicit rule-based rationale, action, and observation at each step.
2. A search hit determines the next read action, and the observed passage determines what the verification tool receives.
3. An empty search result is retained and stops with `missing_evidence`, rather than repeating the query without new evidence.
4. A missing tool stops with `illegal_action`, and a tool exception is recorded as `tool_error`.
5. The hard `max_steps` ceiling stops with `budget_exhausted`, including a zero-step input.
6. The quoted checkpoint sentence supports `latest committed checkpoint`, but the inverted value `Forget committed work` must stop with `verification_failed`.
7. Compared with one-shot generation this adds observable feedback and a value-check action, but the rule-based checker is narrow and is not an independent human or LLM reviewer.
8. ReAct's step ceiling is not full cost accounting; assignment 3 separately charges every proposal and every check.

The function-body physical-line limit is enforced by `test_react_body_under_30_physical_lines`, including the docstring conservatively and excluding blank/comment lines.
The phrase “thought” in this exercise is a short authored policy rationale, not an extracted private model reasoning trace.
