"""Run explicit live Groq checks and save a shareable report containing no credential."""
import json,os,datetime
from pathlib import Path
from engine import read_data
from engine.provider import ModelClient
from engine.purchasing import QUERY_PROMPT,Purchases,bounded_agent
from engine.knowledge import Index
from engine.platform import Platform
from engine.identity import FINANCE
from engine.evaluate import semantic_review

def run(key,model='openai/gpt-oss-20b',output='outputs/groq-live-report.json'):
    # Endpoint is fixed to the requested provider; supplied data is fictional.
    client=ModelClient('https://api.groq.com/openai/v1',model,key,max_calls=30,timeout=45)
    report={'date_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'provider':'Groq','model':model,
        'provenance':'actual live calls by the person running this script','extraction':[],
        'embeddings':'not tested: configure a separate embedding model',
        'semantic_acceptance':'pending independent review of actual answers'}
    old=os.environ.get('CHAT_OPTIONS');os.environ['CHAT_OPTIONS']=json.dumps({'max_completion_tokens':4096})
    ix=Index();ix.build('v1',read_data('policies.json'));db=Purchases()
    try:
        for case in read_data('query_cases.json'):
            try:
                actual=client.json(QUERY_PROMPT,case['question'])
                row={'id':case['id'],'split':case['split'],'question':case['question'],'expected':case['expected'],
                     'actual':actual,'matches_label':actual==case['expected']}
            except Exception as exc:
                row={'id':case['id'],'matches_label':False,'error_type':type(exc).__name__}
                if isinstance(exc,RuntimeError):row['diagnostic']=str(exc)
            report['extraction'].append(row)
        try:
            result=bounded_agent(client,'Use spend_summary to find Nova spend in 2026-Q1.',FINANCE,db)
            observed=any(t['tool']=='spend_summary' and t['result'].get('total_minor')==6500000 for t in result['trace'])
            report['native_tools']={'actual':result,'expected_tool_total_observed':observed,
                                    'final_prose_accuracy':'requires human comparison with tool facts'}
        except Exception as exc:report['native_tools']={'error_type':type(exc).__name__}
        report['policy_answers']=semantic_review(Platform(ix,db,client,quota=20))
        report['request_telemetry']=client.calls
        report['summary']={'extraction_passes':sum(r['matches_label'] for r in report['extraction']),
                           'extraction_cases':len(report['extraction']),'requests_attempted':len(client.calls)}
    finally:
        ix.close();db.close()
        if old is None:os.environ.pop('CHAT_OPTIONS',None)
        else:os.environ['CHAT_OPTIONS']=old
    path=Path(output);path.parent.mkdir(exist_ok=True,parents=True)
    serialized=json.dumps(report,indent=2)
    # Defence in depth: the key is never placed in the report, but redact any exact accidental occurrence.
    if key:serialized=serialized.replace(key,'[REDACTED]')
    path.write_text(serialized)
    return path,report['summary']
