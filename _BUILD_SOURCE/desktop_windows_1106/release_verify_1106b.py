from pathlib import Path
import subprocess,time,json,hashlib
W=Path(__file__).resolve().parent;S=W.parent/'Releases/BulletsOfFury-Setup-2026-11-06.exe';Q=W/('qa/setup-v2-'+str(int(time.time())));Q.mkdir();T=Q/'Installed BOF';checks=[]
def ck(n,v,d=None):checks.append(dict(name=n,passed=bool(v),data=d));print('PASS'if v else'FAIL',n,str(d)[:140]if d else'',flush=True)
def rows(folder):
 p=folder/'desktop.jsonl';return [json.loads(x)for x in p.read_text().splitlines()]if p.exists()else[]
try:
 p=subprocess.run([str(S),'--self-test','--payload',str(S),'--qa-dir',str(Q/'self')],timeout=90);ck('Native host and bounded payload self-tests',p.returncode==0)
 p=subprocess.Popen([str(S),'--qa-dir',str(Q/'install'),'--profile',str(Q/'profile'),'--qa-tour','--qa-install','--target',str(T),'--no-register','--no-shortcuts'])
 p.wait(timeout=240);log=rows(Q/'install');ck('Complete installer extracts and verifies every game file',p.returncode==0 and any(r['name']=='install-complete'for r in log),[r for r in log if r['name']=='install-complete'])
 if not T.exists():raise RuntimeError('Installation did not complete')
 marker=json.loads((T/'BOF-INSTALL.json').read_text());ck('Test install leaves desktop shortcuts and system registration untouched',not marker['registered']and not marker['shortcuts'])
 for n in ['Bullets of Fury.exe','BOF Launcher.exe','game/assets/game.js','game/index.html','game/assets/projectile_contract_1106.js']:
  source=W/'host'/n if not n.startswith('game/')else Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury')/n[5:]
  ck('Installed '+n+' matches the tested revision',hashlib.sha256((T/n).read_bytes()).digest()==hashlib.sha256(source.read_bytes()).digest())
 # Uninstall only the test-owned installation, through its normal ownership ledger.
 p=subprocess.Popen([str(T/'BOF Launcher.exe'),'--uninstall','--qa-uninstall','--qa-dir',str(Q/'uninstall'),'--profile',str(Q/'profile')]);p.wait(timeout=60)
 end=time.monotonic()+60
 while T.exists()and time.monotonic()<end:time.sleep(.25)
 ck('Uninstaller removes the complete test-owned install',not T.exists())
finally:
 (Q/'checks.json').write_text(json.dumps(checks,indent=2));(W/'qa/setup-v2-latest.json').write_text(json.dumps(dict(directory=str(Q),checks=checks),indent=2));print('EVIDENCE',Q)
 if any(not c['passed']for c in checks):raise SystemExit(1)
