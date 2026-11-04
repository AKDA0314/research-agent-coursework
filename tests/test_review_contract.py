"""V2 regressions: partial approval, unit-aware arithmetic, explicit rounding."""
import copy
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from six_step import binding_check, effective_verdict


def verdict():
    return {'status':'supported','reason':'Supported', 'fully_supported':True, 'unsupported_parts':[],
            'checks':{k:{'status':'supported','reason':'Bound'} for k in
                      ('subject','value_unit','time','scope','meaning')}}


def calc(expression='(purchase - loan) / purchase', result='20%', **extra):
    text='教学假设：购价 AUD 1,000,000；贷款余额 AUD 800,000。'
    candidate={'kind':'calculation','statement':'条件计算 '+result,
        'bindings':[{'source_id':'TASK','quote':text}],
        'derivations':[dict(expression=expression,result=result,
                           inputs={'purchase':'AUD 1,000,000','loan':'AUD 800,000'},**extra)]}
    return candidate, [{'source_id':'TASK','text':text}]


class ReviewContractTests(unittest.TestCase):
    def test_partial_supported_never_reaches_report(self):
        candidate={'binding_check':{'errors':[]}}
        for aspect in ['time','scope','meaning']:
            raw=verdict();raw['checks'][aspect]={'status':'missing','reason':'Only core figure supported'}
            self.assertEqual(effective_verdict(candidate,raw)['status'],'missing')
            self.assertEqual(raw['status'],'supported')
        raw=verdict();raw['unsupported_parts']=['house type not in span']
        self.assertEqual(effective_verdict(candidate,raw)['status'],'missing')
        raw=verdict();raw['fully_supported']=False
        self.assertEqual(effective_verdict(candidate,raw)['status'],'missing')

    def test_missing_or_malformed_semantic_contract_is_not_approval(self):
        for raw in [{'status':'supported','reason':'trust me'},dict(verdict(),checks={}),
                    dict(verdict(),fully_supported='true'),dict(verdict(),unsupported_parts=None)]:
            self.assertEqual(effective_verdict({'binding_check':{'errors':[]}},raw)['status'],'missing')
        self.assertEqual(effective_verdict({'binding_check':{'errors':[]}},verdict())['status'],'supported')

    def test_ratio_and_currency_calculations(self):
        for expr,result in [('(purchase - loan) / purchase','20%'),('loan','AUD 800,000'),
                            ('1 - loan / purchase','20%'),('purchase - loan','AUD 200,000')]:
            c,s=calc(expr,result);self.assertEqual(binding_check(c,s)['errors'],[],(expr,result))

    def test_wrong_scaling_currency_dimensions_and_unbound_inputs_rejected(self):
        for expr,result in [('(purchase - loan) / purchase','0.2%'),('purchase - loan','USD 200,000'),
                            ('purchase * loan','AUD 800,000'),('purchase + 1','AUD 1,000,001'),
                            ('(purchase - loan) / purchase * 100','20%')]:
            c,s=calc(expr,result);self.assertTrue(binding_check(c,s)['errors'],(expr,result))
        c,s=calc();c['derivations'][0]['inputs']['loan']='$800,000'
        self.assertTrue(binding_check(c,s)['calculation_errors'])
        c,s=calc();c['derivations'][0]['inputs']={'purchase':'1000000','loan':'800000'}
        self.assertTrue(binding_check(c,s)['errors'])  # cannot erase currencies

    def test_explicit_percentage_rounding(self):
        c,s=calc('loan / (purchase - loan + loan)','80.00%',decimal_places=2)
        self.assertEqual(binding_check(c,s)['errors'],[])
        text='Values AUD 750,000 and AUD 845,000'
        c={'kind':'calculation','statement':'增长约12.67%', 'bindings':[{'source_id':'d','quote':text}],
           'derivations':[{'expression':'(new - old) / old','inputs':{'old':'AUD 750,000','new':'AUD 845,000'},
                           'result':'12.67%','decimal_places':2}]}
        self.assertEqual(binding_check(c,[{'source_id':'d','text':text}])['errors'],[])
        c['derivations'][0]['result']='12.66%'
        self.assertTrue(binding_check(c,[{'source_id':'d','text':text}])['errors'])

    def test_fetch_date_is_preserved_separately_from_content(self):
        c={'kind':'fact','statement':'record','bindings':[{'source_id':'d','quote':'record'}]}
        got=binding_check(c,[{'source_id':'d','text':'record','url':'https://example.test','fetched_at':'2026-11-04'}])
        self.assertEqual(got['verified_spans'][0]['fetched_at'],'2026-11-04')
        self.assertEqual(got['verified_spans'][0]['quote'],'record')

if __name__=='__main__': unittest.main()
