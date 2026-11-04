"""Freeze, inspect models, or execute exactly one bounded DeepSeek run."""
import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from deepseek_client import DeepSeek, Journal, PRICE, request_json
from six_step import digest, freeze, load_frozen, run_framework


def read_key(path=None):
    if path:
        path = Path(path)
        if path.stat().st_mode & 0o077:
            raise ValueError("Key file permissions must be 600; use chmod 600 on that file")
        lines = path.read_text(encoding="utf-8").splitlines()
        values = [line.split("=", 1)[1].strip().strip("\"'") for line in lines if line.startswith("DEEPSEEK_API_KEY=")]
        key = values[0] if len(values) == 1 else ""
    else:
        key = os.environ.get("DEEPSEEK_API_KEY", "").strip()
    if not key or any(c.isspace() for c in key) or not key.isascii():
        raise ValueError("Fill DEEPSEEK_API_KEY in the local key file or environment; never paste it into chat")
    return key


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    prepare = sub.add_parser("freeze", help="No API calls; copy task bytes and saved source bodies")
    prepare.add_argument("--task", type=Path, required=True)
    prepare.add_argument("--notes", type=Path, required=True)
    prepare.add_argument("--out", type=Path, required=True)
    check = sub.add_parser("check", help="Offline validation only; no key read, no API calls")
    check.add_argument("--task", type=Path, required=True)
    check.add_argument("--frozen", type=Path, required=True)
    models = sub.add_parser("models", help="GET /models only; no text generation")
    models.add_argument("--key-file", type=Path)
    run = sub.add_parser("run", help="One run, no automatic retries; maximum CNY 5")
    run.add_argument("--key-file", type=Path)
    run.add_argument("--frozen", type=Path, required=True)
    run.add_argument("--out", type=Path, required=True)
    run.add_argument("--task", type=Path, default=ROOT / "evidence/task.md", help="Expected task bytes; use the new version for a changed scope")
    run.add_argument("--baseline", type=Path, default=ROOT / "evidence/report.md")
    run.add_argument("--max-cny", type=float, default=5.0)
    args = parser.parse_args()
    if args.command == "freeze":
        print(json.dumps(freeze(args.task, args.notes, args.out), ensure_ascii=False, indent=2))
        return 0
    if args.command == "check":
        task, sources, manifest = load_frozen(args.frozen)
        if digest(args.task.read_bytes()) != manifest["task_sha256"]:
            raise ValueError("Frozen task differs from --task file")
        # Raw artifacts are located in the parent of this V2 frozen folder.
        for relative, expected in manifest.get("raw_files", {}).items():
            raw = args.frozen.parent / relative
            if digest(raw.read_bytes()) != expected:
                raise ValueError("Raw evidence hash mismatch: " + relative)
        print(json.dumps({"ok": True, "api_calls": 0, "source_count": len(sources),
                          "task_sha256": manifest["task_sha256"], "corpus_sha256": manifest["corpus_sha256"],
                          "same_task_as_original": manifest["task_sha256"] == digest((ROOT / "evidence/task.md").read_bytes()),
                          "known_gaps": manifest.get("known_gaps", [])}, ensure_ascii=False, indent=2))
        return 0
    key = read_key(args.key_file)
    if args.command == "models":
        try:
            response = json.loads(request_json("/models", key, timeout=30))
            rows = [{"id": r["id"], "name": r.get("name")} for r in response["data"]]
            print(json.dumps({"models": rows, "requested_model": "deepseek-flash",
                              "available": any(r["id"] == "deepseek-flash" for r in rows)}, ensure_ascii=False, indent=2))
            return 0
        except Exception as exc:
            # Do not emit raw request headers or exception bodies during setup.
            print("Model-list check failed: " + type(exc).__name__, file=sys.stderr)
            return 1
    task, sources, manifest = load_frozen(args.frozen)
    if digest(args.task.read_bytes()) != manifest["task_sha256"]:
        raise ValueError("Frozen task differs from --task file")
    baseline = args.baseline.read_bytes()
    args.out.mkdir(parents=True, exist_ok=False)
    args.out.chmod(0o700)
    journal = Journal(args.out, key)
    client = DeepSeek(key, journal, args.max_cny)
    protocol = {"started_utc": datetime.now(timezone.utc).isoformat(), "model": "deepseek-flash",
                "expected_serving_version": "DeepSeek-V4.1-Flash-1017 (official alias mapping; response recorded separately)",
                "thinking": "disabled", "temperature": 0, "max_api_calls": 9, "max_cny": args.max_cny,
                "task_file": str(args.task.resolve()),
                "same_task_as_original": manifest["task_sha256"] == digest((ROOT / "evidence/task.md").read_bytes()),
                "price_snapshot": PRICE, "inputs": manifest, "baseline_report_sha256": digest(baseline),
                "code_sha256": {p: digest((ROOT / p).read_bytes()) for p in ("src/six_step.py", "src/deepseek_client.py", "scripts/run_live.py")},
                "operation_unit": "One proposal batch or one checker batch; planning/report/audit are extra API calls, counted in money.",
                "retrieval": "Local only; all frozen source bodies read each round; no live search/fetch.",
                "comparison": "Historical reference only; inspect same_task_as_original and corpus hashes. A changed task/snapshot is a new study, not a controlled quality comparison or stability test.",
                "budget_limit": "Client-side conservative estimate from peak uncached rates, UTF-8 byte allowance and max output. Not a provider-enforced account spending cap.",
                "retries": 0, "repeat_runs": 1, "human_review": "pending"}
    journal.write("protocol.json", protocol)
    # Snapshot reference is for comparison only. It is never included in prompts.
    (args.out / "baseline-report.md").write_bytes(baseline)
    journal.event("start", protocol)
    try:
        state = run_framework(task, sources, client, journal)
        # Recheck the freeze after generation; fail if files changed mid-run.
        load_frozen(args.frozen)
        code_changed = [p for p, h in protocol["code_sha256"].items() if digest((ROOT / p).read_bytes()) != h]
        if code_changed:
            raise ValueError("Runtime code changed during run")
    except Exception as exc:
        events = [json.loads(line) for line in (args.out / "trace.jsonl").read_text(encoding="utf-8").splitlines()]
        budgets = [e["data"]["spent"] for e in events if e["event"] == "budget"]
        spent = max(budgets, default=0)
        state = {"status": "failed", "stop_reason": "execution_error", "error_type": type(exc).__name__,
                 "error": str(exc), "spent": spent, "remaining_budget": 6-spent, "deliverable": False, "human_review": "pending"}
        journal.event("failure", state)
    state.update(api_calls=client.calls, estimated_cost_cny=round(client.estimated_cny, 6), max_cny=args.max_cny,
                 task_sha256=manifest["task_sha256"], corpus_sha256=manifest["corpus_sha256"],
                 finished_utc=datetime.now(timezone.utc).isoformat(), formal_race_fact="not_run")
    journal.write("run.json", state)
    print(journal.clean(json.dumps(state, ensure_ascii=False, indent=2)))
    return 1 if state["status"] in {"failed", "blocked_review"} else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ValueError, OSError) as exc:
        print("Setup failed (no new generation requested): " + str(exc), file=sys.stderr)
        sys.exit(2)
