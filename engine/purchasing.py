"""SQL is authoritative for totals. The model may request only typed, predefined operations."""
import sqlite3,json
from . import read_data
QUERY_PROMPT='''Extract a spend-summary request as JSON with exactly quarter and supplier.
quarter is 2026-Q1 or 2026-Q2 or null. supplier is Nova, Delta or null (null means all suppliers).
Do not write SQL or calculate money. Missing quarter stays null. Return JSON only.'''
def query_errors(args):
    if not isinstance(args,dict) or set(args)!={'quarter','supplier'}:return ['wrong fields']
    errors=[]
    if args['quarter'] not in ('2026-Q1','2026-Q2'):errors.append('missing/invalid quarter')
    if args['supplier'] not in ('Nova','Delta',None):errors.append('invalid supplier')
    return errors
class Purchases:
    def __init__(self,path=':memory:'):
        self.db=sqlite3.connect(path)
        self.db.execute('CREATE TABLE IF NOT EXISTS orders (id TEXT PRIMARY KEY, tenant TEXT, supplier TEXT, quarter TEXT, amount_minor INTEGER)')
        with self.db:self.db.executemany('INSERT OR IGNORE INTO orders VALUES(?,?,?,?,?)',[(r['id'],r['tenant'],r['supplier'],r['quarter'],r['amount_minor']) for r in read_data('orders.json')])
    def summary(self,who,args):
        errors=query_errors(args)
        if errors:return {'status':'clarify','errors':errors}
        # Never execute model-generated SQL. Tenant is exclusively trusted server context.
        total,count=self.db.execute('SELECT COALESCE(SUM(amount_minor),0),COUNT(*) FROM orders WHERE tenant=? AND quarter=? AND (? IS NULL OR supplier=?)',
            (who.tenant,args['quarter'],args['supplier'],args['supplier'])).fetchone()
        return {'status':'ok','currency':'INR','total_minor':total,'order_count':count,'quarter':args['quarter'],'supplier':args['supplier'],'source':'orders snapshot 2026-07-01'}
    def close(self):self.db.close()
TOOLS=[{'type':'function','function':{'name':'spend_summary','description':'Read an authorised spend summary for a quarter. Identity is supplied by the service.',
 'parameters':{'type':'object','additionalProperties':False,'properties':{'quarter':{'type':'string','enum':['2026-Q1','2026-Q2']},'supplier':{'type':['string','null'],'enum':['Nova','Delta',None]}},'required':['quarter','supplier']}}}]
def dispatch(name,args,who,purchases):
    return purchases.summary(who,args) if name=='spend_summary' else {'status':'tool_denied'}
def bounded_agent(client,question,who,purchases,max_steps=3):
    history=[{'role':'system','content':'Use spend_summary for exact financial facts. Never invent a total, identity or approval.'},{'role':'user','content':question}];trace=[]
    for step in range(max_steps):
        message=client.message(history,tools=TOOLS);calls=message.get('tool_calls') or []
        if not calls:return {'status':'complete','answer':message.get('content',''),'trace':trace}
        if len(calls)>3:return {'status':'limit','trace':trace}
        history.append(message)
        for call in calls:
            f=call.get('function',{})
            try:args=json.loads(f.get('arguments',''))
            except (ValueError,TypeError):args=None
            result=dispatch(f.get('name'),args,who,purchases);trace.append({'tool':f.get('name'),'result':result})
            history.append({'role':'tool','tool_call_id':call['id'],'content':json.dumps(result)})
    return {'status':'limit','trace':trace}
