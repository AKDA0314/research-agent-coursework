"""Assignment 1: rule-based ReAct, no network or model calls."""


def react_loop(question: str, tools: dict, *, max_steps: int = 6) -> list[dict]:
    """Return explicit, replayable thought/action/observation records."""
    trace, previous = [], None
    for step in range(max(0, max_steps)):
        if previous is None:
            thought, action = "Find evidence for the question", {"name": "search", "input": question}
        elif previous.get("kind") == "search" and previous.get("hits"):
            thought, action = "Read the returned source", {"name": "read", "input": previous["hits"][0]}
        elif previous.get("kind") == "source":
            thought, action = "Check the candidate against the observed passage", {"name": "verify", "input": previous}
        else:
            trace[-1]["stop_reason"] = "missing_evidence"
            return trace
        if action["name"] not in tools:
            trace.append({"thought": thought, "action": action, "observation": {"error": "tool unavailable"}, "stop_reason": "illegal_action"})
            return trace
        try:
            observation = tools[action["name"]](action["input"])
        except Exception as error:
            observation = {"error": type(error).__name__, "detail": str(error)}
        trace.append({"step": step + 1, "thought": thought, "action": action, "observation": observation})
        if action["name"] == "verify" or "error" in observation:
            trace[-1]["stop_reason"] = ("answered" if observation.get("supported") is True else "verification_failed") if "error" not in observation else "tool_error"
            return trace
        previous = observation
    if trace:
        trace[-1]["stop_reason"] = "budget_exhausted"
    else:
        trace.append({"thought": "No steps available", "action": None, "observation": {}, "stop_reason": "budget_exhausted"})
    return trace
