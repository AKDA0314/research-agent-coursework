"""Offline safeguards for one audit retry; no real provider calls."""
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))
from deepseek_client import DeepSeek, Journal, SYSTEM
from six_step import digest
from retry_audit import prepare, validate_audit


class AuditRetryTests(unittest.TestCase):
    def test_saved_data_preserved_and_only_requested_factors_change(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            data = {"task": "Original task", "report": "Report", "claims": []}
            request = {"model": "deepseek-flash", "temperature": 0, "thinking": {"type": "disabled"},
                       "response_format": {"type": "json_object"}, "stream": False, "max_tokens": 5000,
                       "messages": [{"role": "system", "content": SYSTEM}, {"role": "user", "content": "Audit\n\nJSON input:\n" + json.dumps(data, ensure_ascii=False)}]}
            (root / "09-report_audit-request.json").write_text(json.dumps(request))
            (root / "report.md").write_text(data["report"])
            (root / "run.json").write_text(json.dumps({"task_sha256": digest(data["task"].encode()), "corpus_sha256": "test", "estimated_cost_cny": 0.1}))
            _, loaded, compact, change = prepare(root, "compact", 5000)
            self.assertEqual(loaded, data)
            self.assertTrue(change["instruction_changed"])
            self.assertEqual(compact["max_tokens"], 5000)
            _, _, increased, change = prepare(root, "original", 8000)
            self.assertEqual(increased["messages"], request["messages"])
            self.assertFalse(change["instruction_changed"])
            self.assertEqual(increased["max_tokens"], 8000)
            (root / "report.md").write_text("changed report")
            with self.assertRaisesRegex(ValueError, "Report differs"):
                prepare(root, "compact", 5000)

    def test_incomplete_or_issue_bearing_audit_cannot_pass(self):
        data = {"report": "No findings", "claims": []}
        base = {"passed": True, "issues": [], "task_coverage": [{"requirement": "Scope", "status": "covered", "reason": "Disclosed"}],
                "review_complete": True, "issues_truncated": False, "coverage_truncated": False}
        self.assertTrue(validate_audit(base, data, "compact")["effective_passed"])
        for changes in ({"issues": ["Unresolved"]}, {"review_complete": False}, {"issues_truncated": True}, {"coverage_truncated": True}):
            self.assertFalse(validate_audit(dict(base, **changes), data, "compact")["effective_passed"])
        bad = dict(base, issues=["x" * 101])
        with self.assertRaisesRegex(ValueError, "bounds"):
            validate_audit(bad, data, "compact")
        del base["review_complete"]
        with self.assertRaisesRegex(ValueError, "flags"):
            validate_audit(base, data, "compact")

    def test_one_call_cap_even_if_called_again(self):
        with tempfile.TemporaryDirectory() as tmp:
            model = DeepSeek("test-secret", Journal(tmp, "test-secret"), max_calls=1)
            response = json.dumps({"choices": [{"finish_reason": "stop", "message": {"content": "{}"}}],
                                   "usage": {"prompt_tokens": 10, "completion_tokens": 2}})
            with patch("deepseek_client.request_json", return_value=response) as transport:
                model.ask("report_audit", "JSON", {})
                with self.assertRaisesRegex(RuntimeError, "budget"):
                    model.ask("report_audit", "JSON", {})
                self.assertEqual(transport.call_count, 1)

    def test_unknown_report_citation_blocks_even_when_model_approves(self):
        audit = {"passed": True, "issues": [], "task_coverage": [{"requirement": "Citations", "status": "covered", "reason": "OK"}]}
        result = validate_audit(audit, {"report": "Claim [[bogus]]", "claims": []}, "original")
        self.assertFalse(result["effective_passed"])
        self.assertEqual(result["mechanical_issues"], ["unknown_citation:bogus"])


if __name__ == "__main__":
    unittest.main()
