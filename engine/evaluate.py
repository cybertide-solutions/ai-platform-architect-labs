"""Curated release evidence: report outcome, failure slice and observed provenance."""
from . import read_data
from .identity import BUYER,FINANCE,BEACON
from .knowledge import Index,visible
from .purchasing import Purchases

def retrieval_suite(index,version='v1',embedder=None):
    out=[]
    for t in read_data('retrieval_cases.json'):
        who={'buyer':BUYER,'finance':FINANCE,'beacon':BEACON}[t['principal']]
        hits=index.search(t['question'],who,version,k=2,embedder=embedder)
        ids=[h['id'] for h in hits]
        # Null expected source is a refusal case. Positive cosine alone is not abstention.
        out.append({'case':t['id'],'slice':'retrieval' if t['source'] else 'refusal',
                    'passed':t['source'] in ids if t['source'] else not hits,'observed':ids})
        out.append({'case':t['id']+'-access','slice':'access','passed':all(visible(h,who) for h in hits),'observed':ids})
    return out

def release_gate(rows,required=('retrieval','refusal','access')):
    missing=set(required)-{r['slice'] for r in rows}
    failures=[r['case'] for r in rows if r['passed'] is not True]
    return {'release':not missing and not failures,'missing_slices':sorted(missing),'failures':failures,
            'passed':len(rows)-len(failures),'total':len(rows)}

def semantic_review(platform):
    rows=[]
    for t in read_data('answer_cases.json'):
        who={'buyer':BUYER,'finance':FINANCE,'beacon':BEACON}[t['principal']]
        rows.append({'case':t['id'],'question':t['question'],'expected':t['expected'],
            'actual':platform.ask(who,'policy',t['question']),'human_correct':None,'human_supported':None,'human_complete':None})
    return rows
