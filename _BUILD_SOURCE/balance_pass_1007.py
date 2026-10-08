"""Native balance measurements; limited controller results are not human clear rates."""
from pathlib import Path
import argparse,sys,json,time,hashlib,base64
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1] if Path(__file__).parent.name=='_BUILD_SOURCE' else Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury')
sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
P=argparse.ArgumentParser();P.add_argument('--cases',required=True);P.add_argument('--out',default='balance_1007');P.add_argument('--resume',action='store_true');P.add_argument('--fresh-case',action='store_true');args=P.parse_args()
O=R/'_shots'/args.out;O.mkdir(parents=True,exist_ok=True)
cases=json.loads(Path(args.cases).read_text());report={'method':'Native Chromium, fixed simulation step, 10Hz rendering; input controller reacts to delayed visible geometry; no forced damage or invulnerability. Entry cinematics skipped in isolated encounter fixtures.','runs':[],'errors':[],'sourceHashes':{p:hashlib.sha256((R/p).read_bytes()).hexdigest() for p in ['assets/game.js','_BUILD_SOURCE/balance_lab_1007.js']}}
if args.resume and (O/'report.json').exists():report=json.loads((O/'report.json').read_text())
done={r['c']['id'] for r in report['runs']};port,stop=shoot.serve(str(R));start=time.monotonic()
def save(): (O/'report.json').write_text(json.dumps(report,indent=2)+'\n')
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--mute-audio','--autoplay-policy=no-user-gesture-required'])
  def boot():
   context=br.new_context(viewport={'width':1100,'height':950})
   # Prevent test scores/analytics leaving the local browser context.
   context.route('**/*',lambda route:route.continue_() if route.request.url.startswith(('http://127.0.0.1:','data:','blob:')) else route.abort())
   p=context.new_page();p.on('pageerror',lambda e:report['errors'].append(str(e)))
   p.on('console',lambda m:report['errors'].append(m.text[:500]) if m.type=='error' and ('127.0.0.1' in m.text or 'ERR_' not in m.text) else None)
   p.on('response',lambda r:report['errors'].append(f'{r.status} {r.url}') if r.status>=400 else None)
   p.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load',timeout=120000);p.wait_for_function('()=>window.__bofFrames>4',timeout=120000);p.evaluate(shoot.TRAP_RAF);p.wait_for_timeout(50)
   p.add_script_tag(path=str(R/'_BUILD_SOURCE/balance_lab_1007.js'));report['meta']=p.evaluate('()=>BAL7.meta()');save()
   if cases and cases[0].get('attack'):p.add_script_tag(path=str(R/'_BUILD_SOURCE/balance_attacks_1007.js'))
   if cases and cases[0].get('naturalEntry'):p.add_script_tag(path=str(R/'_BUILD_SOURCE/balance_natural_entry_1007.js'))
   if cases and cases[0].get('explicitLoadout'):p.add_script_tag(path=str(R/'_BUILD_SOURCE/balance_explicit_loadout_1007.js'))
   return context,p
  context,p=boot()
  report['freshBrowserContextPerCase']=args.fresh_case
  case_index=0
  for c in cases:
   if c['id'] in done:continue
   if args.fresh_case and case_index:
    context.close();context,p=boot()
   case_index+=1
   begun=time.monotonic();print('RUN '+c['id'],flush=True)
   try:
    setup=p.evaluate('c=>BAL7.setup(c)',c)
    # Yield while the real lazy loader decodes the encounter art; no fake Image objects.
    for _ in range(12):p.evaluate('()=>{stageLoadTick();drawWorld(0);}');p.wait_for_timeout(50)
    if c.get('attack'):p.evaluate('c=>BAL7.attackStart(c)',c)
    status={}
    while not status.get('done'):
     status=p.evaluate('n=>BAL7.step(n)',120);p.wait_for_timeout(1)
    result=p.evaluate('()=>BAL7.result()');result.pop('attackOwner',None);result['setup']=setup;result['wallSeconds']=round(time.monotonic()-begun,2)
    if c.get('capture'):
     p.evaluate('()=>{shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}')
     (O/(c['id']+'.png')).write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')));result['screenshot']=c['id']+'.png'
    report['runs'].append(result);save();print(json.dumps({k:result[k] for k in ['outcome','t','hpRatio','finalLives','shots','wallSeconds']}),flush=True)
   except Exception as e:report['errors'].append(c['id']+': '+str(e));save();raise
  report['wallSeconds']=round(time.monotonic()-start,2);save();br.close()
finally:stop()
print(json.dumps({'runs':len(report['runs']),'errors':report['errors'],'out':str(O)}),flush=True)
