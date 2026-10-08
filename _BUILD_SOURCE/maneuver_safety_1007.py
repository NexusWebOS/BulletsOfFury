"""Real-browser survival screen. Fresh context per case; no protected player."""
from pathlib import Path
import argparse,json,sys,time,http.server,base64,hashlib
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
p=argparse.ArgumentParser();p.add_argument('--cases',required=True);p.add_argument('--out',required=True);p.add_argument('--resume',action='store_true');a=p.parse_args()
O=R/'_shots/maneuver_safety_1007'/a.out;O.mkdir(parents=True,exist_ok=True);cases=json.loads(Path(a.cases).read_text());report={'runs':[],'errors':[],'method':'Fresh Chromium context; real images/collisions; 60 Hz simulation, 10 Hz rendering; delayed geometry and bounded eight-way inputs. No forced damage, invulnerability or bonus resources.'}
if a.resume and (O/'report.json').exists():report=json.loads((O/'report.json').read_text())
done={q['c']['id'] for q in report['runs']};http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None;port,stop=shoot.serve(str(R))
def save():(O/'report.json').write_text(json.dumps(report,indent=2)+'\n')
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--mute-audio']);report['browser']=br.version
  for c in cases:
   if c['id'] in done:continue
   began=time.monotonic();context=br.new_context(viewport={'width':1050,'height':940});context.route('**/*',lambda x:x.continue_() if x.request.url.startswith(('http://127.0.0.1:','data:','blob:')) else x.abort());page=context.new_page();page.set_default_timeout(120000)
   page.on('pageerror',lambda e:report['errors'].append(str(e)));page.on('response',lambda r:report['errors'].append(str(r.status)+' '+r.url) if r.status>=400 else None)
   page.goto(f'http://127.0.0.1:{port}/index.html?quality=performance');page.wait_for_function('()=>window.__bofFrames>4');page.evaluate(shoot.TRAP_RAF)
   for script in ['balance_lab_1007.js','maneuver_lab_1007.js']:page.add_script_tag(path=str(R/'_BUILD_SOURCE'/script))
   if c.get('learned'):page.add_script_tag(path=str(R/'_BUILD_SOURCE/maneuver_learned_1007.js'))
   page.evaluate('c=>MV7.setup(c)',c)
   deadline=time.monotonic()+90
   while time.monotonic()<deadline:
    page.evaluate('()=>{stageLoadTick();drawWorld(0);}');page.wait_for_timeout(35)
    if page.evaluate('()=>stageLoadInfo(run.stage).ready'):break
   status={};lastcap=0
   while not status.get('done'):
    status=page.evaluate('()=>MV7.step(180)');page.wait_for_timeout(4)
    if c.get('capture') and status['t']-lastcap>=15:
     lastcap=status['t'];page.evaluate('()=>{ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}')
     (O/(c['id']+'-'+str(round(lastcap))+'.png')).write_bytes(base64.b64decode(page.evaluate('()=>cv.toDataURL().split(",")[1]')))
   q=page.evaluate('()=>MV7.result()');q['alive']=page.evaluate('()=>!player.dead&&!player.out');q['wallSeconds']=round(time.monotonic()-began,2);report['runs'].append(q);save();print(json.dumps({k:q[k] for k in ['outcome','t','deaths','lives','remainingHP','wallSeconds']}|{'id':c['id']}),flush=True);context.close()
  br.close()
finally:stop()
report['runtimeSHA256']={str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (R/'assets').glob('*.js')};save();print('COMPLETE',len(report['runs']),'errors',len(report['errors']));assert not report['errors']
