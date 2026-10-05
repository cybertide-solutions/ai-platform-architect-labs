import io,json,tempfile,urllib.error,unittest
from pathlib import Path
from unittest.mock import patch
from engine.provider import ModelClient,ModelError,USER_AGENT
from verification.groq_check import run

class ProviderErrors(unittest.TestCase):
    def test_identified_api_request(self):
        def response(request,**kwargs):
            self.assertEqual(request.get_header('User-agent'),USER_AGENT)
            self.assertEqual(request.get_header('Accept'),'application/json')
            self.assertEqual(request.get_header('Authorization'),'Bearer private-example-key')
            return io.BytesIO(b'{"choices": [], "usage": {}}')
        with patch('urllib.request.urlopen',side_effect=response):
            ModelClient('https://api.groq.com/openai/v1','test','private-example-key').post('chat/completions',{})
    def test_edge_diagnostic_retained(self):
        error=urllib.error.HTTPError('https://example.test',403,'Forbidden',{},io.BytesIO(b'error code: 1010'))
        client=ModelClient('https://example.test','test','private-example-key')
        with patch('urllib.request.urlopen',side_effect=error):
            with self.assertRaises(ModelError) as caught:client.post('chat/completions',{})
        self.assertEqual(caught.exception.http_status,403)
        self.assertEqual(caught.exception.provider_code,'1010')
        self.assertIn('client signature',str(caught.exception))
        self.assertEqual(client.calls[0]['provider_code'],'1010')
    def test_structured_error_redacts_credential(self):
        body=json.dumps({'error':{'code':'model_permission_blocked','message':'Blocked private-example-key'}}).encode()
        error=urllib.error.HTTPError('https://example.test',403,'Forbidden',{},io.BytesIO(body))
        client=ModelClient('https://example.test','test','private-example-key')
        with patch('urllib.request.urlopen',side_effect=error):
            with self.assertRaises(ModelError) as caught:client.post('chat/completions',{})
        self.assertNotIn('private-example-key',str(caught.exception)+json.dumps(client.calls))
        self.assertIn('[REDACTED]',str(caught.exception))
    def test_block_stops_after_one_attempt_and_does_not_score_answers(self):
        error=urllib.error.HTTPError('https://example.test',403,'Forbidden',{},io.BytesIO(b'error code: 1010'))
        with tempfile.TemporaryDirectory() as td:
            with patch('urllib.request.urlopen',side_effect=error) as transport:
                path,summary=run('private-example-key',output=str(Path(td)/'report.json'))
                self.assertEqual(transport.call_count,1)
            report=json.loads(path.read_text())
        self.assertEqual(summary['run_status'],'blocked')
        self.assertEqual(summary['extraction_evaluated'],0)
        self.assertEqual(summary['requests_attempted'],1)
        self.assertTrue(all(r['matches_label'] is None for r in report['extraction']))
        self.assertEqual(report['policy_answers'],[])
        self.assertEqual(report['blocked']['provider_code'],'1010')
