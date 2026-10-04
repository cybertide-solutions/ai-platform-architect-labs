import unittest,tempfile,copy,json,threading,os,urllib.request
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from unittest.mock import patch
from engine import read_data
from engine.identity import BUYER,FINANCE,BEACON,Identity
from engine.knowledge import Index,evidence_errors
from engine.purchasing import Purchases,dispatch,query_errors
from engine.approvals import ApprovalLedger
from engine.platform import Platform
from engine.evaluate import retrieval_suite,release_gate
from engine.provider import ModelClient,ModelError

class Contracts(unittest.TestCase):
    def setUp(self):
        self.ix=Index();self.ix.build('v1',read_data('policies.json'));self.db=Purchases()
    def tearDown(self):self.ix.close();self.db.close()
    def test_frozen_retrieval_cases(self):
        rows=retrieval_suite(self.ix);self.assertEqual(len(rows),16);self.assertTrue(release_gate(rows)['release'])
    def test_inactive_unapproved_other_tenant_excluded(self):
        hits=self.ix.search('supplier payment terms administrator approval',BUYER,k=10)
        self.assertFalse({'A-TERMS-OLD','UNAPPROVED','B-TERMS'}&{h['id'] for h in hits})
    def test_finance_source_denied_to_buyer(self):
        self.assertEqual(self.ix.search('negotiated discount schedule',BUYER),[])
        self.assertEqual(self.ix.search('negotiated discount schedule',FINANCE)[0]['id'],'A-DISCOUNT')
    def test_index_version_is_immutable(self):
        with self.assertRaises(Exception):self.ix.build('v1',read_data('policies.json'))
        self.assertTrue(release_gate(retrieval_suite(self.ix))['release'])
    def test_missing_source_candidate_fails(self):
        self.ix.build('bad',[d for d in read_data('policies.json') if d['id']!='A-TERMS'])
        self.assertFalse(release_gate(retrieval_suite(self.ix,'bad'))['release'])
    def test_missing_evaluation_slice_blocks(self):
        self.assertFalse(release_gate([{'case':'a','slice':'retrieval','passed':True}])['release'])
    def test_evidence_checks_provenance_not_semantics(self):
        hits=self.ix.search('standard supplier payment terms',BUYER);h=hits[0]
        answer={'status':'answered','answer':'False claim: 90 days','evidence':[{'id':h['id'],'quote':h['text']}]}
        self.assertEqual(evidence_errors(answer,hits),[])
        answer['evidence'][0]['id']='B-TERMS';self.assertIn('unavailable source',evidence_errors(answer,hits))
    def test_forged_quote_rejected(self):
        hits=self.ix.search('standard supplier payment terms',BUYER)
        answer={'status':'answered','answer':'x','evidence':[{'id':hits[0]['id'],'quote':'invented policy sentence'}]}
        self.assertIn('quote mismatch',evidence_errors(answer,hits))
    def test_sql_exact_and_tenant_scoped(self):
        args={'quarter':'2026-Q1','supplier':'Nova'}
        self.assertEqual(self.db.summary(FINANCE,args)['total_minor'],6500000)
        self.assertEqual(self.db.summary(BEACON,args)['total_minor'],99000000)
        self.assertEqual(self.db.summary(FINANCE,dict(args,supplier=None))['total_minor'],8900000)
    def test_sql_injection_and_identity_override_rejected(self):
        self.assertEqual(self.db.summary(FINANCE,{'quarter':'2026-Q1','supplier':"Nova' OR 1=1"})['status'],'clarify')
        self.assertTrue(query_errors({'quarter':'2026-Q1','supplier':'Nova','tenant':'beacon'}))
    def test_unknown_tool_denied(self):self.assertEqual(dispatch('payment',{},FINANCE,self.db)['status'],'tool_denied')
    def test_missing_quarter_clarifies(self):self.assertEqual(self.db.summary(FINANCE,{'quarter':None,'supplier':'Nova'})['status'],'clarify')
    def test_app_role_denied(self):self.assertEqual(Platform(self.ix,self.db).ask(BUYER,'spend','x')['status'],'denied')
    def test_cache_tenant_and_entitlement_boundaries(self):
        p=Platform(self.ix,self.db);q='standard supplier payment terms'
        self.assertFalse(p.ask(BUYER,'policy',q)['cache']);self.assertTrue(p.ask(BUYER,'policy',q)['cache'])
        b=p.ask(BEACON,'policy',q);self.assertFalse(b['cache']);self.assertEqual(b['passages'][0]['id'],'B-TERMS')
        revised=Identity(BUYER.subject,BUYER.tenant,BUYER.roles,2)
        self.assertFalse(p.ask(revised,'policy',q)['cache'])
    def test_quota_consumer_isolation(self):
        p=Platform(self.ix,self.db,quota=1);q='standard payment terms'
        p.ask(BUYER,'policy',q);self.assertEqual(p.ask(BUYER,'policy',q)['status'],'quota')
        self.assertNotEqual(p.ask(BEACON,'policy',q)['status'],'quota')
    def test_circuit_stops_dependency_calls(self):
        class Fault:
            model='test-fault'
            def __init__(self):self.calls=0
            def json(self,*a):self.calls+=1;raise TimeoutError()
        fault=Fault();p=Platform(self.ix,self.db,fault,clock=lambda:0)
        statuses=[p.ask(BUYER,'policy','standard payment terms')['status'] for _ in range(3)]
        self.assertEqual(statuses,['dependency_error','dependency_error','circuit_open']);self.assertEqual(fault.calls,2)

class DurableActions(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.path=Path(self.tmp.name)/'actions.db';self.ledger=ApprovalLedger(self.path)
        self.draft={'supplier':'Nova','amount_minor':1200000,'purpose':'Workstation'}
    def tearDown(self):self.ledger.close();self.tmp.cleanup()
    def test_wrong_reviewer_denied(self):
        with self.assertRaises(PermissionError):self.ledger.approve(BEACON,BUYER,self.draft)
        with self.assertRaises(PermissionError):self.ledger.approve(BUYER,BUYER,self.draft)
    def test_tamper_expiry_and_entitlement(self):
        token=self.ledger.approve(FINANCE,BUYER,self.draft,now=1000)
        self.assertEqual(self.ledger.commit(BUYER,dict(self.draft,amount_minor=1),token,'1',now=1001)['status'],'review_required')
        who=Identity(BUYER.subject,BUYER.tenant,BUYER.roles,2)
        self.assertEqual(self.ledger.commit(who,self.draft,token,'2',now=1001)['status'],'review_required')
        self.assertEqual(self.ledger.commit(BUYER,self.draft,token,'3',now=1300)['status'],'review_required')
    def test_restart_replay_and_conflict(self):
        token=self.ledger.approve(FINANCE,BUYER,self.draft)
        first=self.ledger.commit(BUYER,self.draft,token,'key');self.ledger.close();self.ledger=ApprovalLedger(self.path)
        replay=self.ledger.commit(BUYER,self.draft,token,'key')
        self.assertEqual(first['receipt'],replay['receipt']);self.assertEqual(replay['status'],'replayed')
        self.assertEqual(self.ledger.commit(BUYER,dict(self.draft,amount_minor=1),token,'key')['status'],'conflict')
    def test_concurrent_retry_creates_one(self):
        token=self.ledger.approve(FINANCE,BUYER,self.draft);barrier=threading.Barrier(2)
        def commit():
            ledger=ApprovalLedger(self.path);barrier.wait()
            try:return ledger.commit(BUYER,self.draft,token,'same-key')
            finally:ledger.close()
        with ThreadPoolExecutor(max_workers=2) as pool:
            a=pool.submit(commit);b=pool.submit(commit);rows=[a.result(),b.result()]
        self.assertEqual(sorted(r['status'] for r in rows),['created','replayed'])
        self.assertEqual(rows[0]['receipt'],rows[1]['receipt'])
        self.assertEqual(self.ledger.db.execute('SELECT COUNT(*) FROM requests').fetchone()[0],1)

class ProviderProtocol(unittest.TestCase):
    # Authored HTTP payload fixtures validate adapter mechanics, not live model quality.
    def test_requires_https(self):
        with self.assertRaises(ModelError):ModelClient('http://example.test','test','not-a-secret').post('x',{})
    def test_secret_not_in_repr(self):self.assertNotIn('private-value',repr(ModelClient('https://example.test','test','private-value')))
    def test_json_parsing_and_malformed_reply(self):
        client=ModelClient('https://example.test','test','x')
        with patch.object(client,'message',return_value={'content':'{"quarter":"2026-Q1","supplier":"Nova"}'}):
            self.assertEqual(client.json('s','u')['supplier'],'Nova')
        with patch.object(client,'message',return_value={'content':'not-json'}):
            with self.assertRaises(ModelError):client.json('s','u')
    def test_vector_order_dimensions_and_persistence(self):
        client=ModelClient('https://example.test','fixture-vector','x')
        with patch.object(client,'post',return_value={'data':[{'index':1,'embedding':[0.,1.]},{'index':0,'embedding':[1.,0.]}]}):
            self.assertEqual(client.vectors(['a','b']),[[1.,0.],[0.,1.]])
        class FixtureEmbedding:
            model='fixture-vector'
            def vectors(self,texts):return [[1.,0.] for _ in texts]
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/'v.db';ix=Index(path);ix.build('v',read_data('policies.json'),FixtureEmbedding());ix.close()
            ix=Index(path);hits=ix.search('x',BUYER,'v',embedder=FixtureEmbedding())
            self.assertTrue(hits);self.assertTrue(all(h['tenant']=='aster' for h in hits));ix.close()
        with patch.object(client,'post',return_value={'data':[{'index':0,'embedding':[1.]},{'index':1,'embedding':[1.,2.]}]}):
            with self.assertRaises(ModelError):client.vectors(['a','b'])

if __name__=='__main__':unittest.main()
