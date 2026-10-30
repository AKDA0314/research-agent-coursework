import ast
import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "scripts")]
from react_loop import react_loop
from six_step import verify_candidate, run_framework, citation_only
from run_offline import react_tools


class FrameworkTests(unittest.TestCase):
    def setUp(self):
        self.f = json.loads((ROOT / "fixtures/checkpoint.json").read_text())
        self.task, self.sources, self.proposals = (self.f[k] for k in ("task", "sources", "proposals"))
        self.claim = self.task["claims"][0]
        self.candidates = self.proposals["resume_origin"]

    def test_react_body_under_30_physical_lines(self):
        source = (ROOT / "src/react_loop.py").read_text()
        node = next(n for n in ast.parse(source).body if isinstance(n, ast.FunctionDef))
        lines = source.splitlines()[node.body[0].lineno - 1:node.end_lineno]
        count = len([s for s in lines if s.strip() and not s.lstrip().startswith("#")])
        self.assertLessEqual(count, 30, count)

    def test_react_success(self):
        trace = react_loop(self.task["question"], react_tools(self.f, self.candidates[-1]))
        self.assertEqual(trace[-1]["stop_reason"], "answered")
        self.assertEqual([r["action"]["name"] for r in trace], ["search", "read", "verify"])

    def test_react_inverted_value(self):
        trace = react_loop(self.task["question"], react_tools(self.f, self.candidates[0]))
        self.assertEqual(trace[-1]["stop_reason"], "verification_failed")

    def test_react_empty_and_illegal(self):
        self.assertEqual(react_loop("q", {})[-1]["stop_reason"], "illegal_action")
        rows = react_loop("q", {"search": lambda q: {"kind": "search", "hits": []}})
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[-1]["stop_reason"], "missing_evidence")

    def test_react_limits(self):
        for limit in (0, 1, 2):
            rows = react_loop("q", react_tools(self.f, self.candidates[-1]), max_steps=limit)
            self.assertEqual(rows[-1]["stop_reason"], "budget_exhausted")

    def test_react_error_is_recorded(self):
        def broken(q):
            raise ValueError("fixture failure")
        self.assertEqual(react_loop("q", {"search": broken})[-1]["stop_reason"], "tool_error")

    def test_six_success_full_six_units(self):
        run = run_framework(self.task, self.sources, self.proposals)
        self.assertEqual(run["stop_reason"], "completed")
        self.assertEqual(run["spent"], 6)
        self.assertTrue(run["deliverable"])
        self.assertEqual([r["verdict"]["status"] for r in run["trace"] if r["step"] == "bind_verify"], ["conflict", "missing", "supported"])

    def test_six_conflict(self):
        run = run_framework(self.task, self.sources, {"resume_origin": self.candidates[:1]})
        self.assertEqual(run["stop_reason"], "conflict")
        self.assertFalse(run["deliverable"])

    def test_budget_never_negative_or_half_pair(self):
        for budget in range(6):
            run = run_framework(self.task, self.sources, self.proposals, budget)
            self.assertEqual(run["stop_reason"], "budget_exhausted")
            self.assertGreaterEqual(run["remaining_budget"], 0)
            self.assertEqual(run["spent"] % 2, 0)

    def test_binding_not_only_citation(self):
        good = copy.deepcopy(self.candidates[-1])
        for key, value, status in [("claim_key", "unrelated", "conflict"), ("quote", "invented quote", "missing"), ("source_id", "absent", "missing")]:
            bad = {**good, key: value}
            self.assertEqual(verify_candidate(self.claim, bad, self.sources)["status"], status)

    def test_ablation_same_budget_and_different_selection(self):
        before = run_framework(self.task, self.sources, self.proposals, checker=citation_only)
        after = run_framework(self.task, self.sources, self.proposals)
        self.assertEqual(before["spent"], after["spent"])
        self.assertEqual(before["selected"]["resume_origin"]["value"], "Forget committed work")
        self.assertEqual(after["selected"]["resume_origin"]["value"], "latest committed checkpoint")
        self.assertFalse(before["deliverable"])

    def test_no_mutation_or_scoring_labels(self):
        snapshot = copy.deepcopy(self.f)
        a = run_framework(self.task, self.sources, self.proposals)
        self.assertEqual(a, run_framework(self.task, self.sources, self.proposals))
        self.assertEqual(snapshot, self.f)
        for candidate in self.candidates:
            self.assertEqual(set(candidate), {"claim_key", "source_id", "quote", "value"})

    def test_property_gaps_preserved(self):
        prop = json.loads((ROOT / "fixtures/property.json").read_text())
        run = run_framework(prop["task"], prop["sources"], prop["proposals"])
        self.assertEqual(run["spent"], 6)
        self.assertEqual(run["stop_reason"], "missing_evidence")
        self.assertIsNone(run["selected"]["price_change"])
        self.assertIsNone(run["selected"]["inventory_change"])
        self.assertEqual(run["selected"]["negative_equity"]["value"]["threshold"], 800000)
        self.assertFalse(run["deliverable"])

    def test_wrong_numeric_threshold_rejected(self):
        prop = json.loads((ROOT / "fixtures/property.json").read_text())
        prop["proposals"]["negative_equity"][0]["value"]["threshold"] = 768000
        before = run_framework(prop["task"], prop["sources"], prop["proposals"], checker=citation_only)
        after = run_framework(prop["task"], prop["sources"], prop["proposals"])
        self.assertEqual(before["spent"], after["spent"])
        self.assertIsNotNone(before["selected"]["negative_equity"])
        self.assertIsNone(after["selected"]["negative_equity"])
        self.assertEqual(after["stop_reason"], "conflict")

    def test_same_frozen_reiwa_task_two_outcomes(self):
        fixture = json.loads((ROOT / "fixtures/reiwa-binding.json").read_text())
        excerpt = json.loads((ROOT / "evidence/source-excerpt.json").read_text())
        self.assertEqual(fixture["sources"]["reiwa-record"]["text"], excerpt["excerpt"])
        success = run_framework(fixture["task"], fixture["sources"], fixture["proposals"])
        failure = run_framework(fixture["task"], fixture["sources"], fixture["conflict_proposals"])
        self.assertEqual(success["task_id"], failure["task_id"])
        self.assertEqual(success["claims"], failure["claims"])
        self.assertEqual(success["spent"], failure["spent"])
        self.assertEqual(success["spent"], 6)
        self.assertEqual(success["stop_reason"], "completed")
        self.assertEqual(failure["stop_reason"], "conflict")
        self.assertFalse(failure["deliverable"])
        self.assertEqual([r["verdict"]["status"] for r in success["trace"] if r["step"] == "bind_verify"], ["conflict", "conflict", "supported"])

    def test_wrong_field_even_with_same_number(self):
        fixture = json.loads((ROOT / "fixtures/reiwa-binding.json").read_text())
        claim = fixture["task"]["claims"][0]
        wrong = fixture["proposals"]["recorded_price"][0]
        self.assertEqual(verify_candidate(claim, wrong, fixture["sources"])["status"], "conflict")


if __name__ == "__main__":
    unittest.main(verbosity=2)
