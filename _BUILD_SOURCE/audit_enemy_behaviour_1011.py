"""Native, no-player-fire roster audit. Not a human clear or a balance score."""
from pathlib import Path
import json,sys
from playwright.sync_api import sync_playwright
import shoot
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'_shots/enemy_behaviour_1011';OUT.mkdir(parents=True,exist_ok=True)
port,stop=shoot.serve(str(ROOT));errors=[];rows=[]
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--autoplay-policy=no-user-gesture-required','--mute-audio'])
  p=br.new_page(viewport={'width':1280,'height':1000});p.set_default_timeout(120000)
  p.on('pageerror',lambda e:errors.append(str(e)))
  p.on('console',lambda m:errors.append(m.text[:600]) if m.type=='error' or 'draw error' in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
  p.add_script_tag(path=str(ROOT/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js'))
  stages=[int(a) for a in sys.argv[1:] if a.isdigit()] or list(range(1,10))
  for stage in stages:
   p.evaluate('(s)=>EA11.setup(s,"normal")',stage)
   p.wait_for_function('()=>{stageLoadTick();return stageLoadInfo(run.stage).ready;}',polling=50)
   specs=p.evaluate('EA11.collect()');print('ROSTER',stage,[(s['type'],s['pattern']) for s in specs],flush=True)
   (OUT/'roster.json').write_text(json.dumps(p.evaluate('EA11.specs'),indent=2))
   for spec in specs:
    if not p.evaluate('(s)=>EA11.case(s)',spec):continue
    q=None
    for _ in range(16):
     q=p.evaluate('EA11.step(60)');p.wait_for_timeout(3)
     if q and q.get('dead'):break
    q={'stage':stage,'diff':'normal','spec':spec,**(q or {})};rows.append(q)
    print('UNIT',stage,spec['type'],{k:q.get(k) for k in ['shots','beams','visible','maxY','blocked','actions','gate']},flush=True)
    (OUT/('after.json' if '--after' in sys.argv else 'baseline.json')).write_text(json.dumps({'rows':rows,'errors':errors},indent=2))
  br.close()
finally:stop()
print('ERRORS',errors,flush=True)
