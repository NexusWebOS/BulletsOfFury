"""Reproduce reported failures using the real loaded browser runtime."""
from pathlib import Path
import sys,json,base64
from playwright.sync_api import sync_playwright
import shoot as sh
sys.stdout.reconfigure(encoding='utf-8')
R=Path(__file__).resolve().parents[1];O=R/'_shots/gameplay_audit_1004/blockers';O.mkdir(parents=True,exist_ok=True)
SETUP=(R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text(encoding='utf-8').split('SETUP="""')[1].split('"""')[0]
port,stop=sh.serve(str(R));errors=[];report={}
def frames(p,n,expr='updatePlay(1/60);drawWorld(1/60);'):
 for i in range(0,n,20):
  p.evaluate('(n)=>{for(let i=0;i<n;i++){'+expr+'}}',min(20,n-i));p.wait_for_timeout(8)
def shot(p,name):
 (O/(name+'.png')).write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')))
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=browser.new_page(viewport={'width':1100,'height':950})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:1000]) if m.type=='error' or 'draw error' in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);p.wait_for_function('()=>window.__bofFrames>4',timeout=120000);p.evaluate(sh.TRAP_RAF)
  p.evaluate(SETUP,{'stage':4,'kind':'stormsovereign','diff':'furious'})
  frames(p,120);shot(p,'storm-arrival')
  report['stormBefore']=p.evaluate('()=>({hp:B.hp,noHit:B._noHit,x:B.x,y:B.y,w:B.w,cam:camX,world:worldWidth(),shield:B._s4war.shield,mode:B._er26.mode,parts:B._mr27.parts})')
  report['nodes']=p.evaluate('()=>B._s4war.shield.nodes.map(n=>{const hp=n.hp;_lastHitX=n.x;_lastHitY=n.y;_dmgBullet={kind:"mg",x:n.x,y:n.y,dmg:50};const hit=bossHitTest(n.x,n.y),selected=B._s4ShieldHit===n;hitBoss(50);return {hit,selected,before:hp,after:n.hp,body:B.hp};})')
  p.evaluate('()=>{run.weapon=0;run.wlevel=5;run.wlevels[0]=5;run.infusion=null;run.forge={};window.auditSamples=[];}')
  for k in range(24):
   frames(p,120,'const node=B._s4war.shield.nodes.find(n=>!n.dead);player.x=node?node.x:B.x;player.y=VH-45;player.invuln=1e9;pShoot();updatePlay(1/60);drawWorld(1/60);')
   p.evaluate('()=>auditSamples.push({hp:B.hp,shield:B._s4war.shield.active,nodes:B._s4war.shield.nodes.map(n=>({hp:n.hp,x:n.x,y:n.y})),mode:B._er26.mode,noHit:B._noHit})')
  report['stormSamples']=p.evaluate('()=>auditSamples');shot(p,'storm-after-fire')
  p.evaluate('()=>{run.mode="campaign";run.forgeElems={kinetic:1,fire:1,ice:1,lightning:1,chrome:1,water:1,toxic:1,dark:1};run.loadout=[0,1,2,3,4,5];run.wlevels=WEAPONS.map(()=>3);forgeStart(()=>{});forge.t=2;forge.row=1;forge.esel=4;Input.mouse.down=false;}')
  frames(p,2,'drawForge(1/60);');shot(p,'forge-before')
  for k in range(7):
   p.keyboard.press('ArrowUp');frames(p,2,'drawForge(1/60);')
  shot(p,'forge-after');report['forge']=p.evaluate('()=>({row:forge.row,esel:forge.esel,scroll:forge.scroll,previewError:forge.preview?.err,disc:forgeDiscovered()})')
  report['errors']=errors;browser.close()
finally:stop()
(O/'report.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report,indent=2))
