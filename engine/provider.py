"""A small real Chat Completions/embeddings REST adapter with explicit configuration."""
import json, os, time, urllib.request, urllib.error
from dataclasses import dataclass, field
class ModelError(RuntimeError): pass
@dataclass
class ModelClient:
    base_url: str
    model: str
    api_key: str = field(repr=False)
    calls: list = field(default_factory=list)
    timeout: float = 25
    max_calls: int = 60
    @classmethod
    def environment(cls, prefix='CHAT', model=None):
        values=[os.environ.get(prefix+'_'+x,'') for x in ('URL','MODEL','KEY')]
        if not all(values): raise ModelError(f'Configure {prefix}_URL, {prefix}_MODEL and {prefix}_KEY privately.')
        return cls(values[0],model or values[1],values[2])
    def post(self, endpoint, payload):
        if not self.base_url.startswith('https://'): raise ModelError('The live model endpoint must use HTTPS.')
        if len(self.calls)>=self.max_calls: raise ModelError('Session request allowance reached.')
        row={'model':self.model,'endpoint':endpoint,'status':'error'};start=time.perf_counter()
        try:
            req=urllib.request.Request(self.base_url.rstrip('/')+'/'+endpoint,
                data=json.dumps(payload).encode(),headers={'Content-Type':'application/json','Authorization':'Bearer '+self.api_key})
            with urllib.request.urlopen(req,timeout=self.timeout) as response: data=json.load(response)
            row.update(status='ok',usage=data.get('usage',{}))
            return data
        except urllib.error.HTTPError as exc:
            row['http_status']=exc.code
            raise ModelError(f'Provider HTTP {exc.code}. Review account, quota and capabilities; no automatic retry.') from None
        except (urllib.error.URLError,TimeoutError):
            raise ModelError('Provider unavailable or request timed out.') from None
        finally:
            row['elapsed_ms']=round((time.perf_counter()-start)*1000,2);self.calls.append(row)
    def message(self, messages, tools=None, as_json=False):
        options=json.loads(os.environ.get('CHAT_OPTIONS','{}'))
        if not isinstance(options,dict) or set(options)&{'messages','model','tools','response_format'}: raise ModelError('Invalid CHAT_OPTIONS.')
        payload={'model':self.model,'messages':messages,**options}
        if as_json:payload['response_format']={'type':'json_object'}
        if tools:payload['tools']=tools
        raw=self.post('chat/completions',payload);choices=raw.get('choices',[])
        if not choices or choices[0].get('finish_reason') in ('length','content_filter'):raise ModelError('Missing, truncated or filtered completion.')
        return choices[0]['message']
    def json(self, system, request):
        message=self.message([{'role':'system','content':system},{'role':'user','content':request}],as_json=True)
        try:return json.loads(message.get('content') or '')
        except (ValueError,TypeError):raise ModelError('Invalid JSON/refusal: inspect outcome; do not silently repair.') from None
    def vectors(self, texts):
        raw=self.post('embeddings',{'model':self.model,'input':texts})
        rows=sorted(raw.get('data',[]),key=lambda r:r['index'])
        if [r['index'] for r in rows]!=list(range(len(texts))):raise ModelError('Embedding count/index mismatch.')
        vectors=[r['embedding'] for r in rows]
        if not vectors or not vectors[0] or any(len(v)!=len(vectors[0]) for v in vectors):raise ModelError('Embedding dimension mismatch.')
        return vectors
