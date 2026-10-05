"""Live donor disarm/low-health checks and readable gas pixels."""
from pathlib import Path
import json,base64,traceback
from playwright.sync_api import sync_playwright
import shoot as sh
R=Path(__file__).resolve().parents[1];O=R/'_shots/gameplay_audit_1004/modules';O.mkdir(parents=True,exist_ok=True)
SETUP=(R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text(encoding='utf-8').split('SETUP="""')[1].split('"""')[0]
report={};errors=[]
def frames(p,n,code):
 for i in range(0,n,30):
  p.evaluate('(n)=>{for(let i=0;i<n;i++){'+code+'}}',min(30,n-i));p.wait_for_timeout(10)
def shot(p,name):
 p.evaluate('()=>{shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}')
 (O/(name+'.png')).write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')))
port,stop=sh.serve(str(R))
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch(args=['--no-sandbox']);p=browser.new_page(viewport={'width':1100,'height':950})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' or 'draw error' in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);p.wait_for_function('()=>window.__bofFrames>4',timeout=120000);p.evaluate(sh.TRAP_RAF)
  p.evaluate('()=>r30Warm()');p.wait_for_function('()=>Object.values(FMC_ART).every(a=>XART.rdy(a.key))',timeout=120000)
  report['forms']=[]
  for form in range(1,8):
   p.evaluate(SETUP,{'stage':8,'kind':'vileexistence','diff':'furious'})
   p.evaluate('(i)=>{j3Encounter(B,2);j3Mimic(B,i);B._r30.mode="fight";B.enter=false;B.hp=B.maxhp*.24;player.invuln=1e9;window.seenShots=new Set();}',form)
   frames(p,1200,'player.invuln=1e9;updatePlay(1/60);for(const q of eBullets)seenShots.add(q);if(i%10===0){ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}')
   shot(p,'lowhp-'+str(form))
   report['forms'].append(p.evaluate('()=>({form:j3State(B).mimic,history:j3State(B).gp4Donors[j3State(B).mimic].history,shots:seenShots.size,finite:Number.isFinite(B.x+B.y)&&eBullets.every(q=>Number.isFinite(q.x+q.y+q.vx+q.vy)),hp:B.hp/B.maxhp})'))
  p.evaluate(SETUP,{'stage':8,'kind':'vileexistence','diff':'furious'})
  report['disarm']=p.evaluate('''()=>{j3Encounter(B,2);j3Mimic(B,1);B._r30.mode='fight';const P=gd4Create(B,1).p;
   B.parts.find(q=>q.id==='left').destroyed=true;B.parts.find(q=>q.id==='rackL').destroyed=true;eBullets=[];
   ovTwinMG(P);ovRocketSide(P,-1);ovRocketSide(P,1);const m=gd4Port(P,1,'right');
   return{shots:eBullets.length,onlyLiveMuzzle:Math.abs(eBullets[0].x-m.x)<.001,types:eBullets.map(q=>q.kind)};}''')
  shot(p,'helicopter-disarmed')
  p.evaluate(SETUP,{'stage':7,'kind':'sludgeemperor','diff':'furious'})
  p.evaluate('()=>{for(let i=0;i<6;i++)XART.rdy("nl6c_low_rolling_bank_"+i);s67Clouds=[];s67CloudSpawn(player.x,player.y-40);s67CloudSpawn(player.x+30,player.y-60);for(const c of s67Clouds)c.t=1;}')
  p.wait_for_function('()=>Array.from({length:6},(_,i)=>XART.rdy("nl6c_low_rolling_bank_"+i)).every(Boolean)',timeout=120000)
  shot(p,'readable-gas');report['gas']=p.evaluate('()=>({clouds:s67Clouds.length,player:{x:player.x,y:player.y}})')
  browser.close()
except Exception as e:report['fatal']=str(e);traceback.print_exc()
finally:stop()
report['errors']=errors;(O/'report.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report,indent=2))
