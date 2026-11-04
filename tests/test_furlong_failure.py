"""Offline replay of the 2026-11-04 18:48 V2 failure, not live-model evaluation."""
import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from six_step import (binding_check, effective_verdict, expand_candidates,
                      coverage_errors, run_framework, normalized_derivations)
from deepseek_client import Journal

FIXTURE = json.loads((ROOT / 'tests/fixtures/furlong-v2-failures.json').read_text())
SOURCES = FIXTURE['sources']


def original(key):
    return copy.deepcopy(next(r for r in FIXTURE['rows'] if r['candidate']['claim_key'] == key))


def approval(key='test'):
    return {'claim_key': key, 'status': 'supported', 'reason': 'Synthetic all-yes checker',
            'fully_supported': True, 'unsupported_parts': [],
            'checks': {k: {'status': 'supported', 'reason': 'Synthetic'} for k in
                       ('subject', 'value_unit', 'time', 'scope', 'meaning')}}


def narrow_price():
    c = original('Q1C1')['candidate']
    return {'kind': 'fact', 'statement': '11 Furlong Street 成交价 $768,000，成交日 13 May 2025。',
            'bindings': c['bindings'][:3], 'derivations': []}


class FurlongFailureTests(unittest.TestCase):
    def test_exact_saved_calculation_json_recomputed_without_mutation(self):
        c = original('Q3C6')['candidate']; before = copy.deepcopy(c)
        got = binding_check(c, SOURCES)
        self.assertEqual(got['errors'], [])
        self.assertEqual(got['derived_results'], [{'unit': 'percent', 'value': '20'}])
        self.assertEqual(got['derivation_origin'], 'calculation_json')
        self.assertEqual(c, before)
        self.assertIn('unbound_numeric_anchor:percent:20', c['binding_check']['errors'])

    def test_legacy_json_does_not_bypass_math_units_or_bound_inputs(self):
        base = original('Q3C6')['candidate']
        for change in [{'result': '30%'}, {'expression': '__import__("os")'},
                       {'result': 'USD 200,000'}, {'inputs': {'purchase': 'AUD 2,000,000', 'loan': 'AUD 800,000'}}]:
            c = copy.deepcopy(base); d = json.loads(c['calculation']); d.update(change)
            c['calculation'] = json.dumps(d)
            self.assertTrue(binding_check(c, SOURCES)['errors'], change)

    def test_conflicting_malformed_and_text_only_calculations_fail_closed(self):
        base = original('Q3C6')['candidate']
        for value in ['{broken', '[]', '["not an object"]', 'purchase minus loan']:
            c = copy.deepcopy(base); c['calculation'] = value
            self.assertTrue(binding_check(c, SOURCES)['errors'])
        c = copy.deepcopy(base); c['derivations'] = []
        self.assertIn('conflicting_calculation_fields', binding_check(c, SOURCES)['errors'])
        c['derivations'] = [json.loads(c['calculation'])]
        self.assertEqual(binding_check(c, SOURCES)['errors'], [])

    def test_actual_false_supported_bedrooms_now_vetoed(self):
        row = original('Q2C3'); c = row['candidate']
        self.assertEqual(row['model_verdict']['status'], 'supported')
        c['binding_check'] = binding_check(c, SOURCES)
        for field, n in [('beds',5), ('baths',2), ('cars',6)]:
            self.assertIn('unbound_property_count:%s:%d' % (field,n), c['binding_check']['errors'])
        self.assertEqual(effective_verdict(c, row['model_verdict'])['status'], 'missing')

    def test_bound_real_configuration_passes_counts_but_wrong_count_does_not(self):
        source = next(s for s in SOURCES if s['source_id'] == 'lodge12')
        quote = '"Beds": 5,\n  "Baths": 2,\n  "Cars": 6'
        self.assertIn(quote, source['text'])
        c = {'kind': 'fact', 'statement': '12 Lodge Court 为5卧2卫6车位。',
             'bindings': [{'source_id': 'lodge12', 'quote': '"HeadlineAddress": "12 Lodge Court, Cockburn Central WA 6164"'},
                          {'source_id': 'lodge12', 'quote': quote}]}
        self.assertEqual(binding_check(c, SOURCES)['errors'], [])
        c['statement'] = '12 Lodge Court 为6卧2卫5车位。'
        self.assertIn('unbound_property_count:beds:6', binding_check(c, SOURCES)['errors'])
        self.assertIn('unbound_property_count:cars:5', binding_check(c, SOURCES)['errors'])
        # Other numeric values in the price/date cannot stand in for a bed count.
        c['bindings'] = original('Q2C3')['candidate']['bindings']
        self.assertTrue(binding_check(c, SOURCES)['errors'])

    def test_area_cannot_be_inferred_from_m_without_superscript(self):
        c = {'kind':'fact','statement':'土地172m²','bindings':[{'source_id':'d','quote':'Landsize 172m'}]}
        self.assertIn('unbound_area_m2:172', binding_check(c,[{'source_id':'d','text':'Landsize 172m'}])['errors'])
        c['bindings'][0]['quote'] = '172m<sup><small>2</small></sup>'
        self.assertEqual(binding_check(c,[{'source_id':'d','text':c['bindings'][0]['quote']}])['errors'], [])

    def test_generic_distance_boolean_needs_record_identity(self):
        c = original('Q1C1')['candidate']
        self.assertIn('spatial_record_identity_not_bound', binding_check(c, SOURCES)['errors'])
        c = {'kind':'fact','statement':'地图标点距中心29.3米，在圈内。',
             'bindings':[{'source_id':'distance-calculations','quote':'"distance_m": 29.3'}]}
        self.assertTrue(binding_check(c,SOURCES)['errors'])
        text=next(s['text'] for s in SOURCES if s['source_id']=='distance-calculations')
        start=text.index('"source_id": "reiwa-11"')
        end=text.index('"within_2000m": true',start)+len('"within_2000m": true')
        c['bindings'][0]['quote']=text[start:end]
        self.assertEqual(binding_check(c,SOURCES)['errors'], [])

    def test_real_compound_is_rejected_but_explicit_narrow_atom_retained(self):
        whole = original('Q1C1')['candidate']
        self.assertTrue(binding_check(whole, SOURCES)['errors'])
        proposal = {'candidates':[{'atoms':[narrow_price(), {'kind':'fact','statement':'11 Furlong 为4卧3卫2车位。',
                                                   'bindings':whole['bindings'][:1]}]}], 'gaps':[]}
        before = copy.deepcopy(proposal)
        atoms=expand_candidates(proposal)
        self.assertEqual(proposal,before)
        self.assertEqual(atoms[0]['proposal_origin'], {'group':1,'atom':1})
        statuses=[]
        for c in atoms:
            c['binding_check']=binding_check(c,SOURCES)
            statuses.append(effective_verdict(c,approval())['status'])
        self.assertEqual(statuses,['supported','missing'])

    def test_atoms_never_inherit_parent_evidence_or_expand_without_limit(self):
        p={'candidates':[{'bindings':narrow_price()['bindings'],'atoms':[{'kind':'fact','statement':'$768,000'}]}], 'gaps':[]}
        self.assertIn('no_evidence_binding',binding_check(expand_candidates(p)[0],SOURCES)['errors'])
        p={'candidates':[{'atoms':[narrow_price()]*4}]*5,'gaps':[]}
        self.assertEqual(len(expand_candidates(p)),20)
        p['candidates'] *= 2
        with self.assertRaises(ValueError): expand_candidates(p)

    def test_bare_structured_price_stays_rejected_explicit_normalized_record_works(self):
        c=original('Q1C8')['candidate']
        self.assertIn('unbound_numeric_anchor:AUD:750000',binding_check(c,SOURCES)['errors'])
        text=next(s['text'] for s in SOURCES if s['source_id']=='profile')
        start=text.rindex('"CalendarYear": 2024')
        end=text.index('"normalized_price": "AUD 750,000"',start)+len('"normalized_price": "AUD 750,000"')
        c={'kind':'fact','statement':'标准化记录的CalendarYear 2024，MedianHousePrice AUD 750,000，HouseCount 20。',
           'bindings':[{'source_id':'profile','quote':text[start:end]}]}
        self.assertEqual(binding_check(c,SOURCES)['errors'],[])
        self.assertEqual(binding_check(c,SOURCES)['verified_spans'][0]['source_kind'],
                         next(s['source_kind'] for s in SOURCES if s['source_id']=='profile'))

    def test_actual_gap_disclosure_separate_from_evidence_and_original_failure_preserved(self):
        report=FIXTURE['report']
        quote=next(line for line in report.splitlines() if '库存' in line and ('缺' in line or '未' in line))
        row={'requirement':'两时点库存','status':'disclosed_gap','evidence_status':'missing','report_quote':quote}
        self.assertEqual(coverage_errors([row],report),[])
        for change in [{'report_quote':'虚构缺口原句'}, {'evidence_status':'available'}, {'status':'missing'},
                       {'report_quote':' '}, {'report_quote':'库存已完整核实'}]:
            self.assertTrue(coverage_errors([dict(row,**change)],report))
        self.assertTrue(coverage_errors(FIXTURE['audit']['task_coverage'],report))
        self.assertFalse(FIXTURE['audit']['passed'])
        self.assertEqual(len(FIXTURE['audit']['issues']),10)

    def test_end_to_end_three_pairs_trace_partial_atoms_calc_and_gap_policy(self):
        seen={}
        class Model:
            def ask(self,stage,instruction,data,**kwargs):
                seen[stage]=copy.deepcopy(data)
                if stage=='plan':
                    return {'questions':[dict(claim_key='Q'+str(i),question='Review',completion_condition='Bound',query='Furlong',source_type='frozen') for i in range(1,4)]}
                if stage.startswith('proposal_'):
                    bad=original('Q2C3')['candidate']
                    return {'candidates':[{'atoms':[narrow_price(),bad]},original('Q3C6')['candidate']], 'gaps':['库存缺两个完整快照']}
                if stage.startswith('check_'):
                    return {'verdicts':[approval(c['claim_key']) for c in data['candidates']]}
                if stage=='report':
                    return {'report_markdown':'条件算术及窄事实 '+ ' '.join('[['+r['candidate']['claim_key']+']]' for r in data['checked_claims'])+'。库存缺两个完整快照。'}
                return {'passed':True,'issues':[],'task_coverage':[{'requirement':'库存','status':'disclosed_gap','evidence_status':'missing','report_quote':'库存缺两个完整快照。'}]}
        with tempfile.TemporaryDirectory() as tmp:
            task=next(s['text'] for s in SOURCES if s['source_id']=='TASK')
            state=run_framework(task,[s for s in SOURCES if s['source_id']!='TASK'],Model(),Journal(tmp,''))
            trace=[json.loads(x) for x in (Path(tmp)/'trace.jsonl').read_text().splitlines()]
            ledger=json.loads((Path(tmp)/'claims.json').read_text())
        self.assertEqual(len(seen),9)
        self.assertEqual(state['spent'],6)
        self.assertEqual(state['claim_counts'],{'supported':6,'conflict':0,'missing':3})
        self.assertEqual(state['status'],'report_generated')
        self.assertFalse(state['deliverable']);self.assertEqual(state['human_review'],'pending')
        self.assertEqual(len([e for e in trace if e['event']=='proposal_normalized']),3)
        self.assertEqual(ledger[2]['candidate']['binding_check']['derivation_origin'],'calculation_json')
        self.assertEqual(ledger[1]['model_verdict']['status'],'supported')
        self.assertEqual(ledger[1]['verdict']['status'],'missing')
        self.assertEqual(seen['report']['gaps'][-1]['source_absence_proven'],False)
        self.assertNotIn('sources',seen['check_1'])
        self.assertEqual(len(seen['report']['checked_claims']),6)

if __name__ == '__main__': unittest.main()
