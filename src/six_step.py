"""Assignment 3. Small offline framework, not a general natural-language verifier.

The policy only sees checker verdicts, never evaluator gold labels. An operation
unit is one proposal or one check; query/read are inside the proposal operation.
"""
import re


CHECKPOINT_SENTENCE = "Resume begins from the latest committed checkpoint."


def verify_candidate(claim, candidate, sources):
    source = sources.get(candidate.get("source_id"))
    if not source:
        return {"status": "missing", "reason": "source_not_found"}
    quote = candidate.get("quote", "")
    if not quote or quote not in source["text"]:
        return {"status": "missing", "reason": "quoted_span_not_found"}
    rule = claim["rule"]
    if rule == "checkpoint":
        observed = "latest committed checkpoint" if quote == CHECKPOINT_SENTENCE else None
    elif rule == "sold_price":
        match = re.search(r"Sold price:\s*\$([\d,]+)", quote)
        observed = int(match.group(1).replace(",", "")) if match else None
    elif rule == "equity":
        match = re.fullmatch(r"purchase=(\d+); debt=(\d+); equity=V-debt", quote)
        observed = None if not match else {"threshold": int(match[2]), "negative_when": "V < debt", "drop_fraction": round(1 - int(match[2]) / int(match[1]), 10)}
    elif rule in {"annual_price_comparison", "inventory_change"}:
        # This adapter does not infer time series from a single snapshot.
        return {"status": "missing", "reason": "two_comparable_periods_not_available"}
    else:
        return {"status": "missing", "reason": "unsupported_rule"}
    if observed is None:
        return {"status": "missing", "reason": "field_not_extractable"}
    same = candidate.get("claim_key") == claim["claim_key"] and candidate.get("value") == observed
    return {"status": "supported" if same else "conflict", "reason": "field_value_match" if same else "field_or_value_mismatch", "observed_value": observed, "pointer": source["pointer"]}


def citation_only(claim, candidate, sources):
    """Deliberately weak A/B baseline: citation existence, NOT factual support."""
    return {"status": "supported" if candidate.get("source_id") in sources else "missing", "reason": "citation_exists_only"}


def choose_candidate(checked):
    return next((row["candidate"] for row in checked if row["verdict"]["status"] == "supported"), None)


def stop_policy(complete, remaining, pending, statuses):
    if complete:
        return "completed"
    if pending and remaining < 2:
        return "budget_exhausted"
    if "conflict" in statuses:
        return "conflict"
    return "missing_evidence"


def run_framework(task, sources, proposals, budget=6, checker=verify_candidate):
    if not isinstance(budget, int) or budget < 0:
        raise ValueError("budget must be a non-negative integer")
    claims = task["claims"]
    if len({c["claim_key"] for c in claims}) != len(claims):
        raise ValueError("claim keys must be unique")
    spent, trace, checked, selected = 0, [], {}, {}
    pending = False
    for claim in claims:
        key = claim["claim_key"]
        checked[key] = []
        trace.append({"step": "decompose", "input": task["question"], "claim_key": key, "completion_condition": claim["completion_condition"]})
        for candidate in proposals.get(key, []):
            if budget - spent < 2:
                pending = True
                break
            trace.append({"step": "plan_query", "claim_key": key, "query": claim["query"], "source_type": claim["source_type"]})
            spent += 1
            source = sources.get(candidate.get("source_id"))
            trace.append({"step": "propose_observe", "claim_key": key, "candidate": candidate, "observation": source["text"] if source else "EMPTY_RESULT", "pointer": source["pointer"] if source else None, "spent": spent, "remaining_budget": budget - spent})
            verdict = checker(claim, candidate, sources)
            spent += 1
            trace.append({"step": "bind_verify", "claim_key": key, "candidate": candidate, "verdict": verdict, "spent": spent, "remaining_budget": budget - spent})
            checked[key].append({"candidate": candidate, "verdict": verdict})
        selected[key] = choose_candidate(checked[key])
    statuses = [row["verdict"]["status"] for rows in checked.values() for row in rows]
    stop = stop_policy(all(selected.values()) and bool(claims), budget - spent, pending, statuses)
    # Review state is deliberately distinct from the process stop state.
    review = "rule_checked" if stop == "completed" and checker is verify_candidate else "not_passed"
    return {"task_id": task["task_id"], "claims": claims, "trace": trace, "selected": selected, "spent": spent, "remaining_budget": budget - spent, "stop_reason": stop, "review_status": review, "review_scope": "same deterministic checker; no independent human/LLM review", "deliverable": stop == "completed" and review == "rule_checked"}
