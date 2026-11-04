"""Offline A/B using actual HyperResearch citecheck functions on a tiny fixture DB.

Usage: python3 scripts/run_source_experiment.py HYPERRESEARCH_SOURCE
No model, HTTP requests, original vault writes, or source modifications.
"""
import copy
import hashlib
import json
import sqlite3
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from offline_rules import run_framework, verify_candidate


def save(path, data):
    (ROOT / path).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    source = Path(sys.argv[1]).resolve()
    commit = subprocess.check_output(["git", "-C", str(source), "rev-parse", "HEAD"], text=True).strip()
    assert commit == "75b1ecfb2891184fad2cc1a2ddf9abe476f5b54c"
    sys.path.insert(0, str(source / "src"))
    from hyperresearch.core.citecheck import extract_pairs, triage_pairs, sample_needs_llm
    fixture = json.loads((ROOT / "fixtures/reiwa-binding.json").read_text())
    excerpt = json.loads((ROOT / "evidence/source-excerpt.json").read_text())
    assert fixture["sources"]["reiwa-record"]["text"] == excerpt["excerpt"]
    db = sqlite3.connect(":memory:")
    db.row_factory = sqlite3.Row
    db.executescript("CREATE TABLE notes(id TEXT, title TEXT); CREATE TABLE sources(url TEXT, note_id TEXT); CREATE TABLE claims(note_id TEXT, claim TEXT, quoted_support TEXT, numbers TEXT);")
    db.execute("INSERT INTO notes VALUES(?,?)", ("reiwa-record", "Frozen REIWA sold-price excerpt"))
    db.execute("INSERT INTO sources VALUES(?,?)", (excerpt["url"], "reiwa-record"))
    db.execute("INSERT INTO claims VALUES(?,?,?,?)", ("reiwa-record", "", excerpt["excerpt"], ""))
    task, sources, proposals = (fixture[k] for k in ("task", "sources", "proposals"))

    def mechanical(claim, candidate, source_map):
        pairs = extract_pairs(candidate["sentence"], db)
        triaged = triage_pairs(pairs, db)
        if len(pairs) != 1:
            return {"status": "missing", "reason": "not_exactly_one_binding", "hyperresearch_output": triaged}
        pair = pairs[0]
        verdict = pair["verdict"]
        return {"status": "supported" if verdict == "supported-mechanical" else "missing", "reason": verdict, "hyperresearch_output": triaged, "sampled_for_llm": sample_needs_llm(pairs)}

    def bound(claim, candidate, source_map):
        upstream = mechanical(claim, candidate, source_map)
        local = verify_candidate(claim, candidate, source_map)
        return {**local, "hyperresearch_output": upstream["hyperresearch_output"], "sampled_for_llm": upstream.get("sampled_for_llm", [])}

    before = run_framework(task, sources, proposals, checker=mechanical)
    after = run_framework(task, sources, proposals, checker=bound)
    assert before["selected"]["recorded_price"]["field"] == "current_market_value"
    assert after["selected"]["recorded_price"]["field"] == "sold_price"
    assert before["spent"] == after["spent"] == 6
    result = {
        "commit": commit,
        "module_sha256": hashlib.sha256((source / "src/hyperresearch/core/citecheck.py").read_bytes()).hexdigest(),
        "fixture_sha256": hashlib.sha256((ROOT / "fixtures/reiwa-binding.json").read_bytes()).hexdigest(),
        "input_provenance": "Real saved short quotation; temporary SQLite claims row seeded from that quotation. Not the original vault DB or a full host run. Candidate sentences are deliberate test mutations, not original report statements.",
        "changed_factor": "add field/value binding to the mechanical-check decision",
        "fixed": ["task", "quote", "temporary DB", "candidate sentences/order", "selector", "six operation units"],
        "before": before, "after": after,
        "boundary": "Both runs have no independent review and deliverable=false. The adapter preserves raw needs-llm as pending evidence, without running an LLM. Added rules only cover this declared field. Light originally skipped step 14.5; this is a separate module experiment, not retroactive verification of the report."
    }
    save("results/hyperresearch-binding-ablation.json", result)
    db.close()
    print("Actual citecheck A/B: wrong-field candidate selected before; sold-price candidate selected after; 6 units each.")


if __name__ == "__main__":
    main()
