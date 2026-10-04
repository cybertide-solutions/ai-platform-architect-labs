"""Execute notebook code cells in fresh Python processes, explicitly without live APIs."""
from pathlib import Path
import json,subprocess,sys,os,tempfile,time
root=Path(__file__).resolve().parents[1]
results=[]
for path in sorted((root/'notebooks').glob('*.ipynb')):
    book=json.loads(path.read_text());cells=[(''.join(c['source']),i) for i,c in enumerate(book['cells']) if c['cell_type']=='code']
    script='\n'.join(f"exec(compile({src!r}, {str(path.name+':cell'+str(i))!r}, 'exec'))" for src,i in cells)
    env=dict(os.environ,LIVE_MODE='0')
    start=time.perf_counter()
    result=subprocess.run([sys.executable,'-c',script],cwd=root,env=env,capture_output=True,text=True,timeout=90)
    row={'notebook':path.name,'code_cells':len(cells),'passed':result.returncode==0,'elapsed_seconds':round(time.perf_counter()-start,2)}
    results.append(row);print(('PASS ' if row['passed'] else 'FAIL ')+path.name)
    if result.returncode:print(result.stderr[-6000:])
(root/'outputs').mkdir(exist_ok=True)
(root/'outputs/notebook-rehearsal.json').write_text(json.dumps(results,indent=2))
print('Live model, native model tools, actual embeddings, Colab and Docker are not validated by this check.')
sys.exit(0 if all(r['passed'] for r in results) else 1)
