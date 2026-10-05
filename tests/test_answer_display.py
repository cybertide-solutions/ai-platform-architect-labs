"""Regression cases based on the trainer's actual live report from 2026-10-05."""
import unittest
from engine import read_data
from engine.identity import FINANCE,BUYER
from engine.purchasing import Purchases,format_inr,bounded_agent
from engine.knowledge import Index,evidence_errors,render_policy_evidence
from engine.platform import Platform

class SpendDisplay(unittest.TestCase):
    def test_paise_conversion_and_indian_grouping(self):
        for minor,expected in [(0,'INR 0.00'),(1,'INR 0.01'),(199,'INR 1.99'),
                (6500000,'INR 65,000.00'),(99000000,'INR 9,90,000.00'),
                (12345678901,'INR 12,34,56,789.01')]:
            with self.subTest(minor=minor):self.assertEqual(format_inr(minor),expected)
        for invalid in [True,-1,1.5,'6500000']:
            with self.assertRaises(ValueError):format_inr(invalid)

    def test_live_report_wrong_model_total_cannot_reach_display(self):
        class CapturedFailure:
            def __init__(self):self.count=0
            def message(self,*args,**kwargs):
                self.count+=1
                if self.count==1:return {'role':'assistant','content':None,'tool_calls':[
                    {'id':'t1','type':'function','function':{'name':'spend_summary',
                    'arguments':'{"quarter":"2026-Q1","supplier":"Nova"}'}}]}
                return {'role':'assistant','content':'Total spend: ₹65,00,000 (6,500,000 INR)'}
        db=Purchases()
        try:result=bounded_agent(CapturedFailure(),'Nova Q1',FINANCE,db)
        finally:db.close()
        self.assertEqual(result['answer'],'Nova, 2026-Q1: INR 65,000.00 across 2 orders. Source: orders snapshot 2026-07-01.')
        self.assertEqual(result['answer_mode'],'tool_facts')
        self.assertEqual(result['trace'][0]['result']['total_minor'],6500000)

    def test_tool_free_financial_guess_is_not_complete(self):
        class Guess:
            def message(self,*args,**kwargs):return {'content':'Nova spend is INR 65,00,000.'}
        db=Purchases()
        try:result=bounded_agent(Guess(),'Nova Q1',FINANCE,db)
        finally:db.close()
        self.assertEqual(result['status'],'no_supported_result')
        self.assertNotIn('65,00,000',result['answer'])

class PolicyDisplay(unittest.TestCase):
    def setUp(self):
        self.ix=Index();self.ix.build('v1',read_data('policies.json'));self.db=Purchases()
        self.hits=self.ix.search('When is Nova paid, and what is its late-payment penalty?',BUYER)
        self.source=next(h for h in self.hits if h['id']=='A-TERMS')
    def tearDown(self):self.ix.close();self.db.close()
    def candidate(self):return {'status':'answered','answer':'The contract does not specify a late-payment penalty.',
        'evidence':[{'id':'A-TERMS','quote':'For Nova, the signed contract specifies 30 days.'}]}
    def test_captured_unsupported_contract_claim_not_displayed(self):
        candidate=self.candidate()
        self.assertEqual(evidence_errors(candidate,self.hits),[]) # Syntax alone is insufficient.
        class SelectedSource:
            model='authored-regression-fixture'
            def json(self,*args):return candidate
        result=Platform(self.ix,self.db,SelectedSource()).ask(BUYER,'policy','When is Nova paid, and what is its late-payment penalty?')
        self.assertNotIn('contract does not specify',result['answer'])
        self.assertIn('signed contract specifies 30 days',result['answer'])
        self.assertIn('remains unverified',result['scope_note'])
        self.assertEqual(result['evidence'][0]['quote'],self.source['text'])
    def test_complete_selected_passage_preserves_contract_exception(self):
        result=render_policy_evidence(self.candidate(),self.hits)
        self.assertIn('45 days',result['answer']);self.assertIn('30 days',result['answer'])
        self.assertIn('Do not use the standard term when a contract exception applies.',result['answer'])
    def test_forged_quote_still_rejected(self):
        candidate=self.candidate();candidate['evidence'][0]['quote']='The contract has no penalty whatsoever.'
        self.assertEqual(render_policy_evidence(candidate,self.hits)['status'],'invalid_model_output')
    def test_insufficient_answer_cannot_invent_a_refusal_reason(self):
        candidate={'status':'insufficient','answer':'The law forbids disclosing this information.','evidence':[]}
        result=render_policy_evidence(candidate,self.hits)
        self.assertNotIn('law',result['answer']);self.assertEqual(result['evidence'],[])

if __name__=='__main__':unittest.main()
