"""Synthetic transport/control tests only. Test answers never enter live prompts."""
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from deepseek_client import DeepSeek, Journal
from six_step import freeze, load_frozen, literal_errors, local_search, run_framework


def complete_verdict(**fields):
    return dict(fully_supported=True, unsupported_parts=[], checks={
        k: {"status": "supported", "reason": "synthetic complete evidence"}
        for k in ("subject", "value_unit", "time", "scope", "meaning")}, **fields)


class LiveTests(unittest.TestCase):
    def test_freeze_exact_task_excludes_report_and_summary(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "task.md").write_bytes(b"exact task\r\n")
            notes = root / "notes"
            notes.mkdir()
            (notes / "source.md").write_text("---\nid: doc\nsource: https://example.test/\ntype: note\nsummary: DO NOT FEED THIS\n---\nValue: 10.\n")
            (notes / "final.md").write_text("---\nid: final_report_x\ntype: report\n---\nOLD ANSWER")
            freeze(root / "task.md", notes, root / "frozen")
            task, sources, manifest = load_frozen(root / "frozen")
            self.assertEqual(task, "exact task\r\n")
            self.assertEqual(sources[0]["text"], "Value: 10.\n")
            self.assertEqual(manifest["source_count"], 1)
            (root / "frozen/task.md").write_text("changed")
            with self.assertRaisesRegex(ValueError, "hash mismatch"):
                load_frozen(root / "frozen")

    def test_empty_search_is_recordable_and_does_not_drop_corpus(self):
        sources = [{"source_id": "doc", "text": "value ten"}]
        ranked, matches = local_search("zzzz", sources)
        self.assertEqual(matches, [])
        self.assertEqual(ranked, sources)

    def test_citation_exists_but_wrong_quote_is_rejected(self):
        sources = [{"source_id": "doc", "text": "Value: 10."}]
        self.assertEqual(literal_errors({"bindings": [{"source_id": "doc", "quote": "Value: 10."}]}, sources), [])
        self.assertIn("quoted_span_not_found", literal_errors({"bindings": [{"source_id": "doc", "quote": "Value: 20."}]}, sources))

    def test_model_checker_cannot_override_missing_quote(self):
        with tempfile.TemporaryDirectory() as tmp:
            journal = Journal(tmp, "")
            responses = [
                {"questions": [{"claim_key": "Q", "question": "value?", "completion_condition": "bound value", "query": "value", "source_type": "record"}]},
                {"candidates": [{"statement": "10", "kind": "fact", "bindings": [{"source_id": "doc", "quote": "Value: 10."}]},
                                {"statement": "20", "kind": "fact", "bindings": [{"source_id": "doc", "quote": "Value: 20."}]}], "gaps": []},
                {"verdicts": [complete_verdict(claim_key="Q1C1", status="supported", reason="match"), {"claim_key": "Q1C2", "status": "supported", "reason": "bad checker"}]},
                {"report_markdown": "Value: 10. [[Q1C1]]"},
                {"passed": True, "issues": [], "task_coverage": [{"requirement": "value", "status": "covered"}]}]
            class MockModel:
                def ask(self, stage, instruction, data, **kwargs):
                    if stage == "report":
                        assert len(data["checked_claims"]) == 1
                    return responses.pop(0)
            state = run_framework("Find value", [{"source_id": "doc", "url": "https://example.test", "fetched_at": "today", "text": "Value: 10."}], MockModel(), journal)
            self.assertEqual(state["claim_counts"], {"supported": 1, "conflict": 0, "missing": 1})
            self.assertEqual(state["spent"], 2)
            self.assertFalse(state["deliverable"])

    def test_budget_denies_before_network_and_redacts(self):
        with tempfile.TemporaryDirectory() as tmp:
            journal = Journal(tmp, "secret-example")
            client = DeepSeek("secret-example", journal, max_cny=0.00001)
            with patch("deepseek_client.request_json") as request:
                with self.assertRaisesRegex(RuntimeError, "budget"):
                    client.ask("test", "JSON", {})
                request.assert_not_called()
            journal.event("test", {"value": "secret-example"})
            self.assertNotIn("secret-example", (Path(tmp) / "trace.jsonl").read_text())

    def test_truncated_model_output_stops_without_retry(self):
        with tempfile.TemporaryDirectory() as tmp:
            client = DeepSeek("example", Journal(tmp, "example"))
            raw = json.dumps({"model": "deepseek-flash", "usage": {"prompt_tokens": 20, "completion_tokens": 30},
                              "choices": [{"finish_reason": "length", "message": {"content": "{\"x\":"}}]})
            with patch("deepseek_client.request_json", return_value=raw) as request:
                with self.assertRaisesRegex(RuntimeError, "stage failed"):
                    client.ask("test", "JSON", {})
                self.assertEqual(request.call_count, 1)
            self.assertEqual(client.calls, 1)
            self.assertAlmostEqual(client.estimated_cny, (20*2+30*8)/1_000_000)
            self.assertTrue((Path(tmp) / "01-test-error.json").exists())


if __name__ == "__main__":
    unittest.main()
