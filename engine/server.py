"""Local HTTP deployment with server-bound application identities; no public publishing."""
import os,json
from http.server import HTTPServer,BaseHTTPRequestHandler
from .identity import BUYER,FINANCE,BEACON
from .knowledge import Index
from .purchasing import Purchases
from .platform import Platform
from .provider import ModelClient
from . import read_data

def create_server(port=0,live=False):
    tokens=[os.environ.get(n,'') for n in ['POLICY_TOKEN','SPEND_TOKEN','BEACON_TOKEN']]
    if not all(tokens) or len(set(tokens))!=3:raise ValueError('Provide three distinct demo credentials.')
    bindings=dict(zip(tokens,[(BUYER,'policy'),(FINANCE,'spend'),(BEACON,'policy')]))
    ix=Index();ix.build('v1',read_data('policies.json'));db=Purchases()
    platform=Platform(ix,db,ModelClient.environment() if live else None)
    class Handler(BaseHTTPRequestHandler):
        def log_message(self,*args):pass
        def send(self,code,body):
            data=json.dumps(body).encode();self.send_response(code)
            self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(data)))
            self.send_header('Cache-Control','no-store');self.end_headers();self.wfile.write(data)
        def do_GET(self):
            self.send(200,{'status':'ready','mode':'live' if live else 'search-and-sql'}) if self.path=='/health' else self.send(404,{'status':'not_found'})
        def do_POST(self):
            if self.path!='/v1/ask':return self.send(404,{'status':'not_found'})
            header=self.headers.get('Authorization','');binding=bindings.get(header[7:]) if header.startswith('Bearer ') else None
            if not binding:return self.send(401,{'status':'unauthorised'})
            try:
                n=int(self.headers.get('Content-Length','0'))
                if not 0<n<=4096:return self.send(413,{'status':'too_large'})
                body=json.loads(self.rfile.read(n))
                if not isinstance(body,dict) or set(body) not in ({'question'},{'question','query'}):return self.send(400,{'status':'invalid_fields'})
                if live and 'query' in body:return self.send(400,{'status':'query_override_disabled_in_live_mode'})
            except (ValueError,TypeError):return self.send(400,{'status':'invalid_json'})
            who,app=binding
            result=platform.ask(who,app,body['question'],planned_query=body.get('query'))
            status={'quota':429,'denied':403,'invalid_input':400,'dependency_error':503,'circuit_open':503}.get(result['status'],200)
            self.send(status,result)
    class Server(HTTPServer):
        def get_request(self):
            sock,addr=super().get_request();sock.settimeout(5);return sock,addr
    return Server((os.environ.get('LAB_BIND','127.0.0.1'),port),Handler),platform
if __name__=='__main__':
    srv,platform=create_server(int(os.environ.get('LAB_PORT','8765')),os.environ.get('LIVE_MODE')=='1')
    print('Listening on local lab port',srv.server_port)
    try:srv.serve_forever()
    finally:srv.server_close();platform.index.close();platform.purchases.close()
