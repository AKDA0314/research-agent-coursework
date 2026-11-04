"""Reproduce deterministic classroom traces and the single-factor experiment."""
import copy
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from react_loop import react_loop
from offline_rules import run_framework, verify_candidate, citation_only


def save(name, value):
    target = ROOT / "results" / name
    target.parent.mkdir(exist_ok=True)
    target.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def react_tools(fixture, candidate):
    return {
        "search": lambda query: {"kind": "search", "query": query, "hits": ["classroom-quote"]},
        "read": lambda sid: {"kind": "source", "source_id": sid, **fixture["sources"][sid]},
        "verify": lambda observation: {"supported": verify_candidate(fixture["task"]["claims"][0], candidate, {observation["source_id"]: observation})["status"] == "supported", "candidate": candidate, "observed_pointer": observation["pointer"]},
    }


def main():
    raw = (ROOT / "fixtures/checkpoint.json").read_bytes()
    fixture = json.loads(raw)
    task, sources, proposals = (fixture[k] for k in ("task", "sources", "proposals"))
    candidates = proposals["resume_origin"]
    for name, candidate in [("success", candidates[-1]), ("conflict", candidates[0])]:
        save("react-" + name + ".json", react_loop(task["question"], react_tools(fixture, candidate)))
    save("react-empty.json", react_loop(task["question"], {"search": lambda q: {"kind": "search", "hits": []}}))
    save("six-success.json", run_framework(task, sources, proposals))
    save("six-conflict.json", run_framework(task, sources, {"resume_origin": [candidates[0]]}))
    before = run_framework(task, sources, proposals, checker=citation_only)
    after = run_framework(task, sources, proposals)
    save("checker-ablation.json", {"design_factor": "checker only: citation existence vs field/value binding", "fixture_sha256": hashlib.sha256(raw).hexdigest(), "held_fixed": ["task", "source text", "candidate list and order", "selector: first supported", "budget: six units", "stop policy"], "before": before, "after": after, "interpretation": "The correct candidate was present in both runs. The weak checker passed the inverted candidate; the unchanged selector chose it. This is an offline deterministic checker demonstration, not a model capability improvement or a second HyperResearch run."})
    binding = json.loads((ROOT / "fixtures/reiwa-binding.json").read_text())
    save("six-reiwa-success.json", run_framework(binding["task"], binding["sources"], binding["proposals"]))
    save("six-reiwa-conflict.json", run_framework(binding["task"], binding["sources"], binding["conflict_proposals"]))
    property_file = ROOT / "fixtures/property.json"
    if property_file.exists():
        prop = json.loads(property_file.read_text(encoding="utf-8"))
        save("six-property.json", run_framework(prop["task"], prop["sources"], prop["proposals"]))
        ab_proposals = copy.deepcopy(prop["proposals"])
        ab_proposals["negative_equity"][0]["value"]["threshold"] = 768000
        save("property-ablation.json", {"design_factor": "checker only", "fixture_sha256": hashlib.sha256(property_file.read_bytes()).hexdigest(), "held_fixed": ["full original task text", "frozen source inputs", "same candidates including deliberately wrong threshold", "candidate order", "first-supported selector", "six operation units"], "before": run_framework(prop["task"], prop["sources"], ab_proposals, checker=citation_only), "after": run_framework(prop["task"], prop["sources"], ab_proposals), "scope": "Deterministic local replay, not a second HyperResearch host run; original price/inventory gaps persist in both runs."})
    print("Offline traces generated; no network, LLM calls, or billing changes.")


if __name__ == "__main__":
    main()
