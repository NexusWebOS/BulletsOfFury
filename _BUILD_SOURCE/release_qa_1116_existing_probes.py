from pathlib import Path
import subprocess,json,hashlib,time,sys
R=Path(__file__).resolve().parents[1];O=R/'_shots/release_qa_1116';O.mkdir(parents=True,exist_ok=True)
(O/'legacy').mkdir(exist_ok=True)
names=sys.argv[1:]or['probe_playthrough_weapons_1011.py','probe_forge_campaign_save_0920.py','probe_hq_forge_1023.py','probe_enemy_patterns_coop_1013.py']
results=json.loads((O/'existing-probes.json').read_text(encoding='utf8'))if(O/'existing-probes.json').exists()else[]
for name in names:
 f=R/'_BUILD_SOURCE'/name;start=time.monotonic();print('RUN '+name,flush=True)
 # Original native test logic, separate evidence destination; no test/source mutation.
 code=f.read_text(encoding='utf8').replace("'_shots/","'_shots/release_qa_1116/legacy/").replace('"_shots/','"_shots/release_qa_1116/legacy/').replace('C:/Users/Mike/Desktop/Github Coding/BulletsOfFury',R.as_posix())
 (O/'legacy/enemy_patterns_1013').mkdir(exist_ok=True)
 bootstrap='import sys;sys.path.insert(0,'+repr(str(R/'_BUILD_SOURCE'))+');__file__='+repr(str(f))+';exec(compile('+repr(code)+',__file__,"exec"))'
 log=O/(f.stem+'.log')
 try:
  with log.open('w',encoding='utf8')as out:q=subprocess.run([sys.executable,'-u','-c',bootstrap],cwd=R,stdout=out,stderr=subprocess.STDOUT,timeout=1200)
  row={'test':name,'exit':q.returncode,'seconds':round(time.monotonic()-start,1),'log':str(log.relative_to(R))}
 except subprocess.TimeoutExpired:row={'test':name,'exit':'timeout','seconds':round(time.monotonic()-start,1),'log':str(log.relative_to(R))}
 results.append(row);(O/'existing-probes.json').write_text(json.dumps(results,indent=2),encoding='utf8');print(json.dumps(row),flush=True)
 print(log.read_text(encoding='utf8')[-1600:],flush=True)
