"""Run explicit live Groq checks; access failures block evaluation rather than score it."""
import json,os,datetime
from pathlib import Path
from engine import read_data
from engine.provider import ModelClient,ModelError
from engine.purchasing import QUERY_PROMPT,Purchases,bounded_agent
from engine.knowledge import Index
from engine.platform import Platform
from engine.identity import FINANCE
from engine.evaluate import semantic_review

class StopVerification(Exception):pass

def run(key,model='openai/gpt-oss-20b',output='outputs/groq-live-report.json'):
    client=ModelClient('https://api.groq.com/openai/v1',model,key,max_calls=30,timeout=45)
    report={'date_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'provider':'Groq','model':model,
        'provenance':'actual live calls by the person running this script','extraction':[],
        'embeddings':'not tested: configure a separate embedding model',
        'semantic_acceptance':'pending independent review of actual answers'}
    def blocked(exc):
        if isinstance(exc,ModelError) and exc.http_status in (401,403,429):
            report['blocked']={'http_status':exc.http_status,'provider_code':exc.provider_code,'diagnostic':str(exc)}
            raise StopVerification()
    old=os.environ.get('CHAT_OPTIONS');os.environ['CHAT_OPTIONS']=json.dumps({'max_completion_tokens':4096})
    ix=Index();ix.build('v1',read_data('policies.json'));db=Purchases()
    cases=read_data('query_cases.json')
    try:
        for case in cases:
            try:
                actual=client.json(QUERY_PROMPT,case['question'])
                row={'id':case['id'],'split':case['split'],'question':case['question'],'expected':case['expected'],
                     'actual':actual,'matches_label':actual==case['expected'],'status':'evaluated'}
            except Exception as exc:
                row={'id':case['id'],'matches_label':None,'status':'not_evaluated','error_type':type(exc).__name__}
                if isinstance(exc,RuntimeError):row['diagnostic']=str(exc)
                report['extraction'].append(row)
                blocked(exc)
                continue
            report['extraction'].append(row)
        try:
            result=bounded_agent(client,'Use spend_summary to find Nova spend in 2026-Q1.',FINANCE,db)
            observed=any(t['tool']=='spend_summary' and t['result'].get('total_minor')==6500000 for t in result['trace'])
            report['native_tools']={'actual':result,'expected_tool_total_observed':observed,
                                    'final_prose_accuracy':'requires human comparison with tool facts'}
        except Exception as exc:
            report['native_tools']={'status':'not_evaluated','error_type':type(exc).__name__}
            if isinstance(exc,RuntimeError):report['native_tools']['diagnostic']=str(exc)
            blocked(exc)
        # Platform catches exceptions to expose controlled service responses. Inspect telemetry
        # after each case to stop promptly if provider access becomes blocked during this stage.
        from engine.identity import BUYER,BEACON
        platform=Platform(ix,db,client,quota=20);report['policy_answers']=[]
        for case in read_data('answer_cases.json'):
            who={'buyer':BUYER,'finance':FINANCE,'beacon':BEACON}[case['principal']]
            before=len(client.calls)
            result=platform.ask(who,'policy',case['question'])
            report['policy_answers'].append({'case':case['id'],'question':case['question'],'expected':case['expected'],
                'actual':result,'human_correct':None,'human_supported':None,'human_complete':None})
            if len(client.calls)>before and client.calls[-1].get('http_status') in (401,403,429):
                event=client.calls[-1]
                blocked(ModelError(event.get('diagnostic','Provider access blocked'),event['http_status'],event.get('provider_code')))
    except StopVerification:
        completed={row['id'] for row in report['extraction']}
        for case in cases:
            if case['id'] not in completed:report['extraction'].append({'id':case['id'],'status':'not_evaluated','matches_label':None,'reason':'run blocked'})
        report.setdefault('native_tools',{'status':'not_evaluated','reason':'run blocked'})
        report.setdefault('policy_answers',[])
        report['semantic_acceptance']='not evaluated: provider access blocked'
    finally:
        ix.close();db.close()
        if old is None:os.environ.pop('CHAT_OPTIONS',None)
        else:os.environ['CHAT_OPTIONS']=old
    report['request_telemetry']=client.calls
    report['summary']={'run_status':'blocked' if 'blocked' in report else 'completed',
        'extraction_passes':sum(r.get('matches_label') is True for r in report['extraction']),
        'extraction_evaluated':sum(r.get('status')=='evaluated' for r in report['extraction']),
        'extraction_cases':len(cases),'requests_attempted':len(client.calls)}
    path=Path(output);path.parent.mkdir(exist_ok=True,parents=True)
    serialized=json.dumps(report,indent=2)
    if key:serialized=serialized.replace(key,'[REDACTED]')
    path.write_text(serialized)
    return path,report['summary']
