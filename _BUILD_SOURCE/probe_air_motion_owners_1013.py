from pathlib import Path
import sys,json
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];P=R/'_shots/air_motion_1013';P.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
port,stop=shoot.serve(str(R));results=[];errors=[]
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=b.new_page();p.on('pageerror',lambda e:errors.append(str(e)));p.goto(f'http://localhost:{port}/index.html',timeout=120000);p.wait_for_function('window.__bofFrames>4',timeout=120000);p.evaluate(shoot.TRAP_RAF)
  for stage in [1,6]:
   r=p.evaluate(shoot.SETUP,{'state':'PLAY','stage':stage,'pilot':'cole','invuln':True});assert r['ok'],r
   p.wait_for_function('(s)=>{stageLoadTick();return stageLoadReady(s)}',arg=stage,timeout=120000)
   if stage==1:
    p.wait_for_function('()=>["s1jetdelta","s1jetbomber","s1jetdelta_b","s1jetbomber_b"].every(k=>XART.rdy(AM13_ART[k].roll.key))',timeout=60000)
    results+=p.evaluate('''()=>{const out=[];for(const type of ['s1jetdelta','s1jetbomber','s1jetdelta_b','s1jetbomber_b'])for(const frame of [0,4,8,12,15]){const e=spawnEnemy(type,240,240);e._furyMove={kind:'roll',t:(frame+.1)/16*.58,dur:.58};e.flash=.12;ctx.setTransform(1,0,0,1,0,0);if(!furyFleetDraw(e)||e._air13Frame!==frame)throw new Error('Fury '+type+' '+frame);out.push({owner:type,frame,key:e._air13RenderedKey})}return out}''')
   else:
    p.wait_for_function('()=>["blue","red","green","orange"].every(r=>XART.rdy((r==="blue"?AM13_ART.s6dart:AM13_ART["stealth_"+r]).heading.key))',timeout=60000)
    results+=p.evaluate('''()=>{const out=[];for(const role of ['blue','red','green','orange'])for(const direction of ['south','west','north','east']){const e=spawnEnemy('s6dart',240,240);e.hp=e.maxhp=500;e._fb2Stealth={role,direction};e.flash=.12;ctx.setTransform(1,0,0,1,0,0);if(!ap10StealthDraw(e)||!e._air13RenderedKey?.endsWith('_heading'))throw new Error('stealth '+role+' '+direction);out.push({owner:role,direction,frame:e._air13Frame,key:e._air13RenderedKey})}return out}''')
  assert not errors,errors;b.close()
finally:stop()
(P/'owner_qa.json').write_text(json.dumps({'checks':results,'errors':errors},indent=2));print('PASS',len(results),'Fury/stealth body-owner fixtures')
