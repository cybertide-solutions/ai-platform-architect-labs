"""Durable approval of a purchase draft; transactional, local-only purchase request ledger."""
import sqlite3,json,hashlib,secrets,time
FIELDS={'supplier','amount_minor','purpose'}
def valid(draft):
    return (isinstance(draft,dict) and set(draft)==FIELDS and draft['supplier'] in ('Nova','Delta') and
            type(draft['amount_minor']) is int and 0<draft['amount_minor']<=100000000 and
            isinstance(draft['purpose'],str) and 1<=len(draft['purpose'])<=200)
class ApprovalLedger:
    def __init__(self,path=':memory:'):
        self.db=sqlite3.connect(path,timeout=5,isolation_level=None)
        self.db.execute('CREATE TABLE IF NOT EXISTS reviews(token TEXT PRIMARY KEY, digest TEXT, expires REAL, used INTEGER, reviewer TEXT)')
        self.db.execute('CREATE TABLE IF NOT EXISTS requests(tenant TEXT, subject TEXT, request_key TEXT, digest TEXT, receipt TEXT, PRIMARY KEY(tenant,subject,request_key))')
    def digest(self,who,draft):
        return hashlib.sha256(json.dumps([who.subject,who.tenant,who.roles,who.entitlement_version,draft],sort_keys=True).encode()).hexdigest()
    def approve(self,reviewer,who,draft,now=None):
        if reviewer.tenant!=who.tenant or 'finance' not in reviewer.roles:raise PermissionError('Authorised same-tenant finance review required')
        if not valid(draft):raise ValueError('Invalid purchase draft')
        token=secrets.token_hex(20);self.db.execute('INSERT INTO reviews VALUES(?,?,?,0,?)',(token,self.digest(who,draft),(time.time() if now is None else now)+300,reviewer.subject));return token
    def commit(self,who,draft,token,request_key,now=None):
        if not valid(draft) or not isinstance(request_key,str) or not 1<=len(request_key)<=80:return {'status':'invalid_request'}
        digest=self.digest(who,draft);clock=time.time() if now is None else now
        self.db.execute('BEGIN IMMEDIATE')
        try:
            old=self.db.execute('SELECT digest,receipt FROM requests WHERE tenant=? AND subject=? AND request_key=?',(who.tenant,who.subject,request_key)).fetchone()
            if old:
                result={'status':'replayed','receipt':old[1]} if old[0]==digest else {'status':'conflict'}
            else:
                review=self.db.execute('SELECT digest,expires,used FROM reviews WHERE token=?',(token,)).fetchone()
                if not review or review[0]!=digest or review[1]<=clock or review[2]:result={'status':'review_required'}
                else:
                    receipt='PR-'+secrets.token_hex(5)
                    self.db.execute('INSERT INTO requests VALUES(?,?,?,?,?)',(who.tenant,who.subject,request_key,digest,receipt))
                    self.db.execute('UPDATE reviews SET used=1 WHERE token=?',(token,));result={'status':'created','receipt':receipt}
            self.db.execute('COMMIT');return result
        except Exception:self.db.execute('ROLLBACK');raise
    def close(self):self.db.close()
