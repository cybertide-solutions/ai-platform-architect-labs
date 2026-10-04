"""Two applications share admission, model access, failure policy and telemetry."""
import time,uuid,json
from .knowledge import ANSWER_PROMPT,evidence_errors
from .purchasing import QUERY_PROMPT
APPS={
 'policy':{'roles':{'buyer','finance'},'prompt_version':'policy-v1'},
 'spend':{'roles':{'finance'},'prompt_version':'query-v1'}}
class Platform:
    def __init__(self,index,purchases,model=None,index_version='v1',embedder=None,quota=20,clock=time.monotonic):
        self.index=index;self.purchases=purchases;self.model=model;self.index_version=index_version;self.embedder=embedder
        self.quota=quota;self.used={};self.events=[];self.cache={};self.failures=0;self.open_until=0;self.clock=clock
    def ask(self,who,app,question,planned_query=None):
        start=self.clock();rid=uuid.uuid4().hex[:12]
        event={'request_id':rid,'tenant':who.tenant,'application':app if app in APPS else 'unknown',
               'model':self.model.model if self.model else 'no-model','index':self.index_version}
        result={'status':'error'}
        try:
            if not isinstance(question,str) or not 1<=len(question)<=1500:return self._finish(event,{'status':'invalid_input'},start)
            if app not in APPS or not (set(who.roles)&APPS[app]['roles']):return self._finish(event,{'status':'denied'},start)
            key=(who.tenant,who.subject,app)
            if self.used.get(key,0)>=self.quota:return self._finish(event,{'status':'quota'},start)
            self.used[key]=self.used.get(key,0)+1
            if self.model and self.clock()<self.open_until:return self._finish(event,{'status':'circuit_open'},start)
            ck=(who.subject,who.tenant,who.roles,who.entitlement_version,app,self.index_version,APPS[app]['prompt_version'],event['model'],question)
            if app=='policy':
                if ck in self.cache:return self._finish(event,dict(self.cache[ck],cache=True),start)
                hits=self.index.search(question,who,self.index_version,embedder=self.embedder)
                if not hits:result={'status':'insufficient','answer':'No authorised matching passage.','evidence':[]}
                elif self.model:
                    result=self.model.json(ANSWER_PROMPT,json.dumps({'question':question,'passages':[{'id':r['id'],'text':r['text']} for r in hits]}))
                    errors=evidence_errors(result,hits)
                    if errors:result={'status':'invalid_model_output','errors':errors}
                else:result={'status':'evidence_only','passages':hits,'note':'Search result, not a generated answer.'}
                if result['status'] in ('answered','insufficient','evidence_only'):self.cache[ck]=dict(result)
                result=dict(result,cache=False)
            else:
                if self.model:args=self.model.json(QUERY_PROMPT,question)
                elif planned_query is not None:args=planned_query
                else:return self._finish(event,{'status':'live_or_explicit_query_required'},start)
                result=self.purchases.summary(who,args)
            self.failures=0
        except Exception:
            self.failures+=1
            if self.failures>=2:self.open_until=self.clock()+10
            result={'status':'dependency_error','action':'manual review or retry after service recovery'}
        return self._finish(event,result,start)
    def _finish(self,event,result,start):
        event.update(status=result['status'],elapsed_ms=round((self.clock()-start)*1000,2),cache=result.get('cache',False))
        self.events.append(event);return dict(result,request_id=event['request_id'])
