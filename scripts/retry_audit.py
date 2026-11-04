"""One explicit audit-only retry. Preserve original report, inputs and failure."""
import argparse
import json
import math
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from deepseek_client import DeepSeek, Journal, SYSTEM, PRICE
from six_step import digest, coverage_errors
from run_live import read_key

COMPACT = '''
输出长度约束（不改变审查依据）：只返回完整 JSON，不写前言或重复意见。
issues 最多 12 条不同问题，每条最多 100 个字符，定位报告章节或 claim_key；合并重复、同义问题。
task_coverage 最多 20 项，将相近要求分组，requirement 最多 60 字符，reason 最多 80 字符。
保留 passed、issues、task_coverage，并新增三个布尔字段：
review_complete（是否完成本次输入范围内全部审查）、issues_truncated（是否仍有无法列完的问题）、coverage_truncated（是否仍有未列完的覆盖项）。
不能为缩短输出遗漏未解决问题：超过上述容量则标相应 truncated=true、review_complete=false、passed=false。
有任何 issues、missing 覆盖、未完成审查或截断，passed 必须 false。优先在长度内闭合完整 JSON。
'''


def prepare(source_run, style, max_tokens):
    source_run = Path(source_run)
    raw = (source_run / "09-report_audit-request.json").read_bytes()
    request = json.loads(raw)
    expected = {"model": "deepseek-flash", "temperature": 0, "thinking": {"type": "disabled"},
                "response_format": {"type": "json_object"}, "stream": False}
    if set(request) != set(expected) | {"messages", "max_tokens"} or any(request.get(k) != v for k, v in expected.items()):
        raise ValueError("Unsupported saved request configuration; refusing silent changes")
    messages = request["messages"]
    if len(messages) != 2 or messages[0] != {"role": "system", "content": SYSTEM} or messages[1].get("role") != "user":
        raise ValueError("Saved system prompt/roles differ from this client")
    instruction, separator, data_text = messages[1]["content"].partition("\n\nJSON input:\n")
    if not separator:
        raise ValueError("Cannot identify saved audit input")
    data = json.loads(data_text)
    if data.get("report") != (source_run / "report.md").read_text(encoding="utf-8"):
        raise ValueError("Report differs from the saved audit request")
    previous = json.loads((source_run / "run.json").read_text(encoding="utf-8"))
    if digest(data["task"].encode("utf-8")) != previous["task_sha256"]:
        raise ValueError("Task hash mismatch")
    if data_text != json.dumps(data, ensure_ascii=False):
        raise ValueError("Input serialization differs; refusing silent changes")
    if style == "compact":
        instruction += COMPACT
    new_request = dict(request)
    new_request["max_tokens"] = max_tokens
    new_request["messages"] = [dict(messages[0]), {"role": "user", "content": instruction + separator + data_text}]
    change = {"source_request_sha256": digest(raw), "report_sha256": digest(data["report"].encode()),
              "audit_data_sha256": digest(data_text.encode()), "task_sha256": previous["task_sha256"],
              "corpus_sha256": previous["corpus_sha256"], "style": style,
              "old_max_tokens": request["max_tokens"], "new_max_tokens": max_tokens,
              "instruction_changed": instruction != messages[1]["content"].partition(separator)[0],
              "audit_data_unchanged": True, "model_parameters_unchanged": True,
              "prior_estimated_cost_cny": previous["estimated_cost_cny"]}
    return instruction, data, new_request, change


def validate_audit(audit, data, style):
    issues, coverage = audit.get("issues"), audit.get("task_coverage")
    if type(audit.get("passed")) is not bool or not isinstance(issues, list) or not all(isinstance(x, str) for x in issues):
        raise ValueError("Invalid audit passed/issues fields")
    if not isinstance(coverage, list) or not coverage or any(not isinstance(r, dict) or r.get("status") not in {"covered", "disclosed_gap", "missing"}
            or not isinstance(r.get("requirement"), str) or not isinstance(r.get("reason"), str) for r in coverage):
        raise ValueError("Invalid audit coverage")
    complete = True
    if style == "compact":
        flags = ("review_complete", "issues_truncated", "coverage_truncated")
        if any(type(audit.get(k)) is not bool for k in flags):
            raise ValueError("Missing compact completeness flags")
        if len(issues) > 12 or any(len(x) > 100 for x in issues) or len(coverage) > 20 or any(len(r["requirement"]) > 60 or len(r["reason"]) > 80 for r in coverage):
            raise ValueError("Compact output bounds violated; raw output retained")
        complete = audit["review_complete"] and not audit["issues_truncated"] and not audit["coverage_truncated"]
    allowed = {r["candidate"]["claim_key"] for r in data["claims"] if r["verdict"]["status"] == "supported"}
    refs = re.findall(r"\[\[([^\]]+)\]\]", data["report"])
    mechanical = ["unknown_citation:" + r for r in refs if r not in allowed]
    if allowed and not refs:
        mechanical.append("report_has_no_claim_citations")
    mechanical.extend(coverage_errors(coverage, data["report"]))
    passed = audit["passed"] and complete and not issues and not mechanical
    result = dict(audit)
    result.update(mechanical_issues=mechanical, effective_passed=bool(passed), human_review="pending", same_model_checker=True)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-run", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--key-file", type=Path)
    parser.add_argument("--style", choices=("compact", "original"), default="compact")
    parser.add_argument("--max-tokens", type=int, default=5000)
    parser.add_argument("--max-cny", type=float, default=0.5)
    parser.add_argument("--dry-run", action="store_true", help="Validate saved input and print proposed changes; no key read or network")
    args = parser.parse_args()
    if not 1000 <= args.max_tokens <= 16000:
        raise ValueError("max-tokens must be between 1000 and 16000")
    if not math.isfinite(args.max_cny) or not 0 < args.max_cny <= 5:
        raise ValueError("Invalid CNY budget")
    instruction, data, request, change = prepare(args.source_run, args.style, args.max_tokens)
    previous_cost = change["prior_estimated_cost_cny"]
    if not isinstance(previous_cost, (int, float)) or not math.isfinite(previous_cost) or not 0 <= previous_cost < 5:
        raise ValueError("Invalid or exhausted original-run cost")
    budget = min(args.max_cny, 5 - previous_cost)
    allowance = ((len(json.dumps(request, ensure_ascii=False).encode())+4096)*2 + args.max_tokens*8)/1_000_000
    if allowance > budget:
        raise ValueError("Request allowance exceeds remaining monetary budget")
    if args.out.exists() or args.source_run.resolve() in args.out.resolve().parents:
        raise ValueError("Choose a new sibling output directory; preserve original artifacts")
    protocol = {**change, "started_utc": datetime.now(timezone.utc).isoformat(), "source_run_name": args.source_run.name,
                "kind": "explicit_single_audit_retry", "max_api_calls": 1, "retry_budget_cny": budget, "request_allowance_cny": allowance,
                "price_snapshot": PRICE, "automatic_retries": 0, "preserve_source_run": True,
                "scope": "Replay exactly the saved report-audit input; no new research or report generation. Known missing audit context remains unchanged.",
                "comparison_limit": "One retry, not proof of causality or stability. Changing style and max_tokens together changes two factors.",
                "code_sha256": {p: digest((ROOT / p).read_bytes()) for p in ("scripts/retry_audit.py", "src/deepseek_client.py")}}
    if args.dry_run:
        print(json.dumps(protocol, ensure_ascii=False, indent=2))
        return 0
    key = read_key(args.key_file)
    args.out.mkdir(parents=True, mode=0o700, exist_ok=False)
    journal = Journal(args.out, key)
    client = DeepSeek(key, journal, budget, max_calls=1)
    journal.write("protocol.json", protocol)
    journal.event("start", protocol)
    try:
        response = client.ask("report_audit", instruction, data, max_tokens=args.max_tokens)
        audit = validate_audit(response, data, args.style)
        journal.write("report-audit.json", audit)
        state = {"status": "audit_completed" if audit["effective_passed"] else "blocked_review", "stop_reason": "audit_retry_completed",
                 "review_status": "same_model_checked" if audit["effective_passed"] else "not_passed"}
    except Exception as exc:
        state = {"status": "failed", "stop_reason": "audit_retry_error", "error_type": type(exc).__name__, "error": str(exc)}
        journal.event("failure", state)
    state.update(deliverable=False, human_review="pending", api_calls=client.calls,
                 estimated_cost_cny=round(client.estimated_cny, 6), original_plus_this_retry_estimated_cny=round(previous_cost+client.estimated_cny, 6),
                 source_run_name=args.source_run.name, report_sha256=change["report_sha256"], formal_race_fact="not_run",
                 finished_utc=datetime.now(timezone.utc).isoformat())
    journal.write("run.json", state)
    journal.event("stop", state)
    print(journal.clean(json.dumps(state, ensure_ascii=False, indent=2)))
    return 0 if state["status"] == "audit_completed" else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ValueError, OSError, KeyError) as exc:
        print("Setup failed; no generation started: " + str(exc), file=sys.stderr)
        sys.exit(2)
