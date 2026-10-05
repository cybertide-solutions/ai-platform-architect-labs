"""Check launch links and bootstrap behavior without requiring a Google account."""
from pathlib import Path
import json,os,sys,tempfile,types,unittest,subprocess
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
NOTEBOOKS=sorted((ROOT/'notebooks').glob('*.ipynb'))+sorted((ROOT/'verification').glob('*.ipynb'))
def bootstrap_source(path):
    book=json.loads(path.read_text())
    src=''.join(next(c for c in book['cells'] if c['cell_type']=='code')['source'])
    return src.split('ROOT = prepare_lab_files()')[0]
def ready_folder(path):
    for name in ['engine/__init__.py','engine/knowledge.py','data/policies.json','data/orders.json']:
        f=path/name;f.parent.mkdir(parents=True,exist_ok=True);f.write_text('{}')
class ColabSetup(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.home=Path(self.tmp.name);self.previous=Path.cwd();self.old_path=sys.path[:]
        (self.home/'working').mkdir();os.chdir(self.home/'working')
        google=types.ModuleType('google');google.__path__=[];colab=types.ModuleType('google.colab');google.colab=colab
        self.modules=patch.dict(sys.modules,{'google':google,'google.colab':colab});self.modules.start()
        ns={};exec(bootstrap_source(NOTEBOOKS[0]),ns);self.prepare=ns['prepare_lab_files']
    def tearDown(self):
        os.chdir(self.previous);sys.path[:]=self.old_path;self.modules.stop();self.tmp.cleanup()
    def test_all_links_and_bootstraps_match(self):
        readme=(ROOT/'README.md').read_text();baseline=bootstrap_source(NOTEBOOKS[0]);self.assertEqual(len(NOTEBOOKS),11)
        for path in NOTEBOOKS:
            self.assertIn('https://colab.research.google.com/github/cybertide-solutions/ai-platform-architect-labs/blob/main/'+path.relative_to(ROOT).as_posix(),readme)
            self.assertEqual(bootstrap_source(path),baseline)
    def test_fresh_download_and_rerun_preserves_work(self):
        def clone(args,**kwargs):ready_folder(Path(args[-1]));return subprocess.CompletedProcess(args,0,'','')
        with patch('subprocess.run',side_effect=clone) as run:
            root=self.prepare(self.home/'content');self.assertEqual(run.call_count,1);(root/'my-work.txt').write_text('keep')
            self.assertEqual(self.prepare(self.home/'content'),root);self.assertEqual(run.call_count,1)
            self.assertEqual((root/'my-work.txt').read_text(),'keep')
    def test_incomplete_folder_is_not_overwritten(self):
        target=self.home/'content/ai-platform-architect-labs';target.mkdir(parents=True);(target/'my-work.txt').write_text('keep')
        with patch('subprocess.run') as run:
            with self.assertRaisesRegex(RuntimeError,'incomplete course folder'):self.prepare(self.home/'content')
            run.assert_not_called()
        self.assertEqual((target/'my-work.txt').read_text(),'keep')
    def test_failed_clone_cleans_partial_download(self):
        with patch('subprocess.run',return_value=subprocess.CompletedProcess([],1,'','failure')):
            with self.assertRaisesRegex(RuntimeError,'download failed'):self.prepare(self.home/'content')
        self.assertEqual(list((self.home/'content').iterdir()),[])
    def test_timeout_cleans_staging(self):
        with patch('subprocess.run',side_effect=subprocess.TimeoutExpired('git',120)):
            with self.assertRaisesRegex(RuntimeError,'timed out'):self.prepare(self.home/'content')
        self.assertEqual(list((self.home/'content').iterdir()),[])
    def test_local_package_needs_no_clone(self):
        ready_folder(self.home/'working')
        with patch('subprocess.run') as run:
            self.assertEqual(self.prepare(self.home/'content'),self.home/'working');run.assert_not_called()
