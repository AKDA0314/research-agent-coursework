"""Historical regressions + adversarial offline tests. Never supplied to live generation."""
import copy
import json
import sys
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from deepseek_client import Journal
from six_step import binding_check, effective_verdict, literal_errors, numeric_anchors, run_framework

FIXTURE = json.loads((ROOT / 'tests/fixtures/binding-cases.json').read_text())
SOURCES = FIXTURE['sources']


def original(key):
    return copy.deepcopy(next(r['candidate'] for r in FIXTURE['cases'] if r['candidate']['claim_key'] == key))


def repaired(key):
    cand = original(key)
    binding = cand['bindings'][0]
    body = next(s['text'] for s in SOURCES if s['source_id'] == binding['source_id'])
    if key == 'Q1C4':
        binding['quote'] = body  # heading + period + price, exact frozen span
    else:
        binding['quote'] = body[body.index('Cockburn Central has 2,446 properties.'):body.index('  * Houses have a median rent')].rstrip()
    return cand


def check(cand, sources=SOURCES):
    return binding_check(cand, sources)


def complete_verdict(**fields):
    return dict(fully_supported=True, unsupported_parts=[], checks={
        k: {"status": "supported", "reason": "synthetic complete evidence"}
        for k in ("subject", "value_unit", "time", "scope", "meaning")}, **fields)


class BindingTests(unittest.TestCase):
    def test_two_real_bad_bindings_are_rejected_despite_original_approval(self):
        for key, unit, value in [('Q1C4', '$', '975000'), ('Q1C6', 'percent', '90.60')]:
            with self.subTest(key=key):
                cand = original(key)
                before = copy.deepcopy(cand)
                self.assertEqual(literal_errors(cand, SOURCES), [])
                validation = check(cand)
                self.assertEqual(cand, before)  # no historical record mutation
                self.assertEqual(validation['missing_anchors'], [{'unit': unit, 'value': value}])
                cand['binding_check'] = validation
                raw = {'status': 'supported', 'reason': 'full page contains the number'}
                self.assertEqual(effective_verdict(cand, raw)['status'], 'missing')
                self.assertEqual(raw['status'], 'supported')

    def test_complete_real_spans_pass_binding_gate_and_have_valid_pointers(self):
        for key in ['Q1C4', 'Q1C6']:
            cand = repaired(key)
            cand['binding_check'] = check(cand)
            self.assertEqual(cand['binding_check']['errors'], [])
            for span in cand['binding_check']['verified_spans']:
                body = next(s['text'] for s in SOURCES if s['source_id'] == span['source_id'])
                self.assertEqual(body[span['start_char']:span['end_char']], span['quote'])
            self.assertEqual(effective_verdict(cand, {'status': 'conflict', 'reason': 'context wrong'})['status'], 'conflict')

    def test_forged_wrong_source_and_unknown_source_quotes(self):
        for mode in ['fabricated', 'wrong_source', 'unknown']:
            cand = repaired('Q1C4')
            if mode == 'fabricated': cand['bindings'][0]['quote'] += ' Guaranteed.'
            elif mode == 'wrong_source': cand['bindings'][0]['source_id'] = SOURCES[0]['source_id']
            else: cand['bindings'][0]['source_id'] = 'unknown'
            self.assertTrue(check(cand)['errors'])
            self.assertEqual(check(cand)['verified_spans'], [])

    def test_normalization_preserves_units_scale_and_currency(self):
        self.assertEqual(numeric_anchors('$975,000 and 90.60%'), numeric_anchors('＄９７５０００ and 90.6 percent'))
        self.assertEqual(numeric_anchors('$975k'), numeric_anchors('$0.975 million'))
        self.assertEqual(numeric_anchors('CNY 150万'), {('CNY', Decimal('1500000'))})
        self.assertNotEqual(numeric_anchors('USD 100'), numeric_anchors('AUD 100'))
        self.assertNotEqual(numeric_anchors('$90.6'), numeric_anchors('90.6%'))
        self.assertEqual(numeric_anchors('2026-09-30'), set())
        self.assertNotEqual(numeric_anchors('$9007199254740993'), numeric_anchors('$9007199254740992'))

    def test_per_cent_variants_are_equivalent_but_not_percentile(self):
        expected = {('percent', Decimal('16.0'))}
        for text in ['16.0%', '16.0 percent', '16.0 per cent', '16.0 PER CENT', '16.0 per\u00a0cent']:
            self.assertEqual(numeric_anchors(text), expected, text)
        self.assertEqual(numeric_anchors('16.0 percentile'), set())

    def test_real_per_cent_quote_does_not_trigger_false_missing(self):
        quote = 'This was 16.0 per cent higher than April 2026 and 20.7 per cent higher than a year ago.'
        cand = {'statement': '16.0% higher than April 2026 and 20.7% higher than a year ago.',
                'kind': 'fact', 'bindings': [{'source_id': 'doc', 'quote': quote}]}
        sources = [{'source_id': 'doc', 'text': quote}]
        self.assertEqual(check(cand, sources)['errors'], [])
        cand['statement'] = '16.1% higher than April 2026'
        self.assertEqual(check(cand, sources)['missing_anchors'], [{'unit': 'percent', 'value': '16.1'}])

    def test_multiple_bound_spans_can_jointly_cover_a_claim(self):
        cand = repaired('Q1C4')
        body = cand['bindings'][0]['quote']
        sid = cand['bindings'][0]['source_id']
        cand['bindings'] = [{'source_id': sid, 'quote': body[:body.index('####')]},
                            {'source_id': sid, 'quote': '#### $975,000'}]
        self.assertEqual(check(cand)['errors'], [])

    def test_unrelated_full_source_or_other_claim_cannot_fill_binding(self):
        cand = original('Q1C4')
        sources = copy.deepcopy(SOURCES) + [{'source_id': 'another', 'text': '$975,000'}]
        self.assertTrue(check(cand, sources)['errors'])
        # Disjoint spans '$' and '975000' cannot be assembled as a price.
        cand = {'statement': '$975000', 'kind': 'fact', 'bindings': [
            {'source_id': 'd', 'quote': '$'}, {'source_id': 'd', 'quote': '975000'}]}
        self.assertTrue(check(cand, [{'source_id': 'd', 'text': '$ and 975000'}])['errors'])

    def test_calculations_need_bound_inputs_and_recomputed_result(self):
        source = [{'source_id': 'd', 'text': 'Rent is $100 per month. Duration 2 months.'}]
        cand = {'statement': 'Total $200', 'kind': 'calculation', 'calculation': 'rent * months',
                'bindings': [{'source_id': 'd', 'quote': source[0]['text']}],
                'derivations': [{'result': '$200', 'expression': 'rent * months',
                                 'inputs': {'rent': '$100', 'months': '2'}}]}
        self.assertEqual(check(cand, source)['errors'], [])
        for mode in ['wrong_result', 'unbound_input', 'unsafe_expression', 'no_derivation', 'fact_kind']:
            bad = copy.deepcopy(cand)
            if mode == 'wrong_result': bad['derivations'][0]['expression'] = 'rent + months'
            elif mode == 'unbound_input': bad['derivations'][0]['inputs']['rent'] = '$150'
            elif mode == 'unsafe_expression': bad['derivations'][0]['expression'] = '__import__("os")'
            elif mode == 'no_derivation': bad['derivations'] = []
            else: bad['kind'] = 'fact'
            self.assertTrue(check(bad, source)['errors'], mode)

    def test_number_presence_is_not_semantic_proof(self):
        cand = {'statement': 'Houses rose 90.60%', 'kind': 'fact',
                'bindings': [{'source_id': 'd', 'quote': 'Units fell 90.60%'}]}
        cand['binding_check'] = check(cand, [{'source_id': 'd', 'text': 'Units fell 90.60%'}])
        self.assertEqual(cand['binding_check']['errors'], [])  # documented mechanical limit
        self.assertEqual(effective_verdict(cand, {'status': 'conflict', 'reason': 'wrong subject/direction'})['status'], 'conflict')

    def test_no_or_invalid_binding_cannot_pass(self):
        for bindings in [None, [], ['bad'], [{'source_id': 'd', 'quote': ''}]]:
            cand = {'statement': '$100', 'kind': 'fact', 'bindings': bindings}
            self.assertTrue(check(cand, [{'source_id': 'd', 'text': '$100'}])['errors'])


class BindingIntegrationTests(unittest.TestCase):
    def exercise(self, repair=False):
        candidates = [(repaired if repair else original)(key) for key in ['Q1C4', 'Q1C6']]
        candidates[0]['unbound_source_text'] = 'DO_NOT_BORROW_FULL_SOURCE'
        raw = copy.deepcopy(candidates)
        seen = {}
        class MockModel:
            def ask(self, stage, instruction, data, **kwargs):
                seen[stage] = copy.deepcopy(data)
                if stage == 'plan': return {'questions': [{'claim_key': 'Q1', 'question': 'market?', 'completion_condition': 'bound', 'query': 'Cockburn', 'source_type': 'profile'}]}
                if stage == 'proposal_1': return {'candidates': candidates, 'gaps': []}
                if stage == 'check_1': return {'verdicts': [complete_verdict(claim_key='Q1C'+str(i), status='supported', reason='synthetic verdict') for i in [1, 2]]}
                if stage == 'report': return {'report_markdown': 'Evidence [[Q1C1]] [[Q1C2]]' if repair else '缺证，无法判断。'}
                return {'passed': True, 'issues': [], 'task_coverage': [{'requirement': 'market', 'status': 'covered'}]}
        with tempfile.TemporaryDirectory() as tmp:
            state = run_framework('Market task', SOURCES, MockModel(), Journal(tmp, ''))
            ledger = json.loads((Path(tmp)/'claims.json').read_text())
            events = [json.loads(l) for l in (Path(tmp)/'trace.jsonl').read_text().splitlines()]
            gaps = json.loads((Path(tmp)/'gaps.json').read_text())
        self.assertEqual(candidates, raw)
        return state, seen, ledger, events, gaps

    def test_lying_checker_cannot_approve_bad_bindings_or_hide_gaps(self):
        state, seen, ledger, events, gaps = self.exercise()
        self.assertNotIn('sources', seen['check_1'])
        self.assertNotIn('DO_NOT_BORROW_FULL_SOURCE', json.dumps(seen['check_1']))
        self.assertNotIn('#### $975,000', json.dumps(seen['check_1'], ensure_ascii=False))
        self.assertEqual(seen['report']['checked_claims'], [])
        self.assertEqual(len(seen['report']['rejected_claims']), 2)
        self.assertEqual(len(seen['report_audit']['rejected_claims']), 2)
        self.assertEqual(state['claim_counts']['missing'], 2)
        self.assertEqual(len([g for g in gaps if 'binding_errors' in g]), 2)
        logged = next(e['data']['checked'] for e in events if e['event'] == 'bind_verify')
        self.assertEqual(logged, ledger)
        for row in ledger:
            self.assertEqual(row['model_verdict']['status'], 'supported')
            self.assertEqual(row['verdict']['status'], 'missing')
        self.assertFalse(state['deliverable'])

    def test_repaired_binding_reaches_report_subject_to_semantic_review(self):
        state, seen, _, _, _ = self.exercise(repair=True)
        self.assertEqual(len(seen['report']['checked_claims']), 2)
        self.assertEqual(state['claim_counts']['supported'], 2)
        self.assertFalse(state['deliverable'])  # no change to human-review gate


if __name__ == '__main__':
    unittest.main()
