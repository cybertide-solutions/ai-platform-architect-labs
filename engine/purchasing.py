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
        return {'status':'ok','currency':'INR','minor_unit':'paise','total_minor':total,
            'total_display':format_inr(total),'order_count':count,'quarter':args['quarter'],
            'supplier':args['supplier'],'source':'orders snapshot 2026-07-01',
            'measure':'recorded purchase-order amounts; not proof of payments'}
    def close(self):self.db.close()
TOOLS=[{'type':'function','function':{'name':'spend_summary','description':'Read an authorised spend summary for a quarter. Identity is supplied by the service.',
 'parameters':{'type':'object','additionalProperties':False,'properties':{'quarter':{'type':'string','enum':['2026-Q1','2026-Q2']},'supplier':{'type':['string','null'],'enum':['Nova','Delta',None]}},'required':['quarter','supplier']}}}]
def dispatch(name,args,who,purchases):
    return purchases.summary(who,args) if name=='spend_summary' else {'status':'tool_denied'}

def format_inr(total_minor):
    """The database stores integer paise. Format rupees without floating point or a model."""
    if type(total_minor) is not int or total_minor < 0:
        raise ValueError('Spend must be nonnegative integer paise.')
    rupees,paise=divmod(total_minor,100)
    digits=str(rupees)
    if len(digits)>3:
        groups=[];head=digits[:-3]
        while head:
            groups.insert(0,head[-2:]);head=head[:-2]
        digits=','.join(groups+[digits[-3:]])
    return f'INR {digits}.{paise:02d}'

def render_spend_summary(result):
    if result.get('status')!='ok' or result.get('currency')!='INR':
        raise ValueError('An authorised successful INR summary is required.')
    amount=format_inr(result['total_minor'])
    supplier=result['supplier'] or 'All suppliers'
    return (f"{supplier}, {result['quarter']}: {amount} across {result['order_count']} orders. "
            f"Source: {result['source']}.")

def bounded_agent(client,question,who,purchases,max_steps=3):
    history=[{'role':'system','content':'Use spend_summary for financial facts. total_minor is integer paise (100 paise = 1 INR). Never invent a total, identity or approval. The service renders financial answers from tool results.'},{'role':'user','content':question}];trace=[]
    for step in range(max_steps):
        message=client.message(history,tools=TOOLS);calls=message.get('tool_calls') or []
        if not calls:
            # Model prose is not a financial authority. Only executed, validated tools
            # supply the displayed answer; a tool-free guess is never marked complete.
            facts=[t['result'] for t in trace if t['tool']=='spend_summary' and t['result'].get('status')=='ok']
            if not facts:return {'status':'no_supported_result','answer':'No successful authorised spend query. Clarify the request.','trace':trace}
            if any(t['result'].get('status')!='ok' for t in trace):
                return {'status':'clarify','answer':'At least one requested tool operation was not successful. Review the trace and clarify the request.','trace':trace}
            answers=list(dict.fromkeys(render_spend_summary(f) for f in facts))
            return {'status':'complete','answer':'\n'.join(answers),'answer_mode':'tool_facts','trace':trace}
        if len(calls)>3:return {'status':'limit','trace':trace}
        history.append(message)
        for call in calls:
            f=call.get('function',{})
            try:args=json.loads(f.get('arguments',''))
            except (ValueError,TypeError):args=None
            result=dispatch(f.get('name'),args,who,purchases);trace.append({'tool':f.get('name'),'result':result})
            history.append({'role':'tool','tool_call_id':call['id'],'content':json.dumps(result)})
    return {'status':'limit','trace':trace}
