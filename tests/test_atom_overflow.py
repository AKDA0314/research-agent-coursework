"""Replay the saved 25-atom response offline; never call a real model."""
import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from six_step import expand_candidates, select_check_batch, run_framework
from deepseek_client import Journal
FIXTURE = json.loads((ROOT / 'tests/fixtures/atom-overflow-20261104.json').read_text())

class OverflowTests(unittest.TestCase):
    def test_saved_response_partition_is_lossless_stable_and_bounded(self):
        before = copy.deepcopy(FIXTURE)
        atoms = expand_candidates(FIXTURE['proposal'])
        self.assertEqual(len(atoms),25)
        selected, deferred = select_check_batch(atoms)
        self.assertEqual((len(selected),len(deferred)),(16,9))
        self.assertEqual({c['proposal_origin']['group'] for c in selected},set(range(1,9)))
        identity = lambda c: tuple(c['proposal_origin'].values())
        self.assertEqual(set(map(identity,selected)) | set(map(identity,deferred)),set(map(identity,atoms)))
        self.assertFalse(set(map(identity,selected)) & set(map(identity,deferred)))
        self.assertEqual(select_check_batch(atoms),(selected,deferred))
        self.assertEqual(FIXTURE,before)

    def test_boundaries_and_malformed_structure(self):
        for n in (0,1,16,17,32):
            atoms=[{'statement':str(i),'proposal_origin':{'group':i//4+1,'atom':i%4+1}} for i in range(n)]
            selected,deferred=select_check_batch(atoms)
            self.assertEqual(len(selected),min(n,16))
            self.assertEqual(len(deferred),max(0,n-16))
            if n<=16: self.assertEqual(selected,atoms)
        for groups in ([{'atoms':[{}]*5}], [{}]*9, [{'atoms':[{'atoms':[]}]}]):
            with self.assertRaises(ValueError): expand_candidates({'candidates':groups,'gaps':[]})
        for limit in (0,-1,True,1.5):
            with self.assertRaises(ValueError): select_check_batch([],limit)

    def replay(self, bad_citation=False, fail_check=False):
        seen={}
        class Model:
            def ask(self,stage,instruction,data,**kwargs):
                seen[stage]=copy.deepcopy(data)
                if stage=='plan':
                    return {'questions':[dict(claim_key='Q'+str(i),question='Review',completion_condition='Bound',query='Furlong',source_type='frozen') for i in range(1,4)]}
                if stage.startswith('proposal_'): return copy.deepcopy(FIXTURE['proposal'])
                if stage.startswith('check_'):
                    if fail_check: raise RuntimeError('Synthetic check failure')
                    return {'verdicts':[{'claim_key':c['claim_key'],'status':'missing','reason':'Offline replay without source corpus'} for c in data['candidates']]}
                if stage=='report':
                    overflow=next(g for g in data['gaps'] if g.get('gap_kind')=='check_batch_limit')['claim_keys'][0]
                    return {'report_markdown':'缺少核验证据。'+ ('[['+overflow+']]' if bad_citation else '')}
                return {'passed':True,'issues':[],'task_coverage':[{'requirement':'evidence','status':'disclosed_gap','evidence_status':'missing','report_quote':'缺少核验证据。'}]}
        with tempfile.TemporaryDirectory() as tmp:
            if fail_check:
                with self.assertRaises(RuntimeError): run_framework('task',[],Model(),Journal(tmp,''))
                state=None
            else: state=run_framework('task',[],Model(),Journal(tmp,''))
            artifacts={p.name:(json.loads(p.read_text()) if p.suffix=='.json' else p.read_text()) for p in Path(tmp).iterdir()}
        return state,seen,artifacts

    def test_full_run_persists_overflow_separately_with_no_extra_calls(self):
        state,seen,files=self.replay()
        self.assertEqual(len(seen),9)
        self.assertEqual(state['spent'],6)
        self.assertEqual(state['deferred_claim_count'],27)
        self.assertEqual(state['claim_counts'],{'supported':0,'conflict':0,'missing':48})
        deferred=files['deferred-claims.json']
        self.assertEqual(len(deferred),27)
        self.assertTrue(all(r['status']=='not_checked' for r in deferred))
        ids={r['candidate']['claim_key'] for r in deferred}
        checked={r['candidate']['claim_key'] for r in files['claims.json']}
        self.assertFalse(ids & checked)
        self.assertEqual(seen['report']['checked_claims'],[])
        self.assertEqual(seen['report_audit']['claims'],[])
        self.assertIn('27 条候选',files['report.md'])
        events=[json.loads(s) for s in files['trace.jsonl'].splitlines()]
        selection=[e['data'] for e in events if e['event']=='proposal_selection']
        self.assertEqual(len(selection),3)
        self.assertTrue(all(len(e['selected_ids'])==16 and len(e['deferred_ids'])==9 for e in selection))

    def test_deferred_citation_blocks_even_if_model_audit_passes(self):
        state,seen,files=self.replay(bad_citation=True)
        self.assertEqual(state['status'],'blocked_review')
        self.assertTrue(any(x.startswith('unknown_citation:') for x in files['report-audit.json']['mechanical_issues']))

    def test_overflow_survives_checker_failure(self):
        state,seen,files=self.replay(fail_check=True)
        self.assertEqual(len(files['deferred-claims.json']),9)
        self.assertTrue(any(g.get('gap_kind')=='check_batch_limit' for g in files['gaps.json']))
        self.assertNotIn('report-audit.json',files)

if __name__=='__main__': unittest.main()
