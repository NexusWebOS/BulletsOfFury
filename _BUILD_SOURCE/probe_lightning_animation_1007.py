"""Replay the Stage 4 flight reel after removing its transparent terminal cell."""
from pathlib import Path
import sys,json,http.server
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
O=R/'_shots/projectiles_1007/final';report=json.loads((O/'audit.json').read_text(encoding='utf-8'))
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
port,stop=shoot.serve(str(R));errors=[]
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);p=br.new_page();p.set_default_timeout(120000)
  p.route('**/*',lambda r:r.continue_() if r.request.url.startswith(('http://127.0.0.1:','data:','blob:')) else r.abort());p.on('pageerror',lambda e:errors.append(str(e)))
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('()=>window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
  for f in ['balance_lab_1007.js','projectile_lab_1007.js']:p.add_script_tag(path=str(R/'_BUILD_SOURCE'/f))
  p.evaluate("()=>{AP7.begin({stage:4,kind:'stormsovereign',diff:'normal',id:'lightning'});boss=null;bossActive=false;subBoss=null;subBossActive=false;for(let i=0;i<8;i++)XART.rdy('s4w_lightning_mg_round_'+i);}")
  p.wait_for_function("()=>Array.from({length:8},(_,i)=>XART.rdy('s4w_lightning_mg_round_'+i)).every(Boolean)")
  for c in report['specialized']:
   r=next(r for r in c['rows'] if r['variant'].get('_s4wKind')=='lightningmg')
   r['initialFrames']=r.get('initialFrames',r['frames'])
   r['frames']=p.evaluate("""d=>{diffKey=d;DIFF=difficultyForRun('arcade',d);AP7.geometry=[];const out=[];
    for(let f=0;f<32;f++)out.push(AP7.frame({kind:'eshot',_s4wKind:'lightningmg',x:240,y:256,vx:3,vy:0,w:12,h:24,t:f/34,_noArsenal:true}));return out;}""",c['diff'])
   c['geometry']+=p.evaluate('()=>AP7.geometry')
   print(c['diff'],'visible',sum(f['n']>0 for f in r['frames']),'/32',flush=True)
  br.close()
finally:stop()
report['errors']+=errors
(O/'audit.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print('errors',errors,flush=True)
