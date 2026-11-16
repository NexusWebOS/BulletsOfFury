from pathlib import Path
from playwright.sync_api import sync_playwright
import sys,json
R=Path(__file__).resolve().parents[1];O=R/'_shots/release_qa_1116/fatal';O.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
rows=[];errors=[]
with sync_playwright()as w:
 b=w.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required'])
 for name,sequence in [('fresh5',[5]),('fresh8',[8]),('after5',[5,8])]:
  p=b.new_page(viewport={'width':1440,'height':1000});p.set_default_timeout(150000);p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None)
  p.goto('http://127.0.0.1:8765/index.html?release-fatal=1116');p.wait_for_function('window.__bofFrames>6');p.evaluate(shoot.TRAP_RAF)
  p.evaluate("()=>{BOFOnline.submitScore=()=>{};window.QFatal=[];const original=playerHit;playerHit=function(source){const before=player.dead,context={source,stage:run.stage,weapon:run.weapon,space:run.spaceMode,active:spaceWeaponsActive(),spaceWeapon:run.spaceWeapon,charge:run._spaceShadowCharge,held:run._spaceShadowHeld,invuln:player.invuln,x:player.x,y:player.y,time:stateT,stack:new Error().stack};const r=original.apply(this,arguments);if(!before&&player.dead)QFatal.push(context);return r;};}")
  for stage in sequence:
   p.evaluate("n=>{BOSSMODE.start(n,'boss','cole',false,'furious');player.invuln=1e8;player._spawnClearT=1e8;Input.keys.j=true;}",stage);p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(run.stage)}',polling=50)
   for i in range(70):
    p.evaluate(shoot.STEP,30);p.wait_for_timeout(1)
    if p.evaluate('player.dead'):break
   q=p.evaluate("()=>({state,stage:run.stage,dead:player.dead,life:run.lives,weapon:run.weapon,space:run.spaceMode,active:spaceWeaponsActive(),fatal:QFatal.slice(),erased:player._eradicated,evap:player._hammerEvap,void:!!player._voidDeath})");q.update(case=name);rows.append(q);print(json.dumps(q),flush=True);p.evaluate('()=>{Input.keys.j=false;SC12.refresh();}');p.screenshot(path=str(O/(name+'-'+str(stage)+'.png')))
  p.close()
 b.close()
(O/'report.json').write_text(json.dumps({'rows':rows,'errors':errors,'scope':'Protected stationary native reproduction: only fatal-source diagnosis, no balance/win claim.'},indent=2),encoding='utf8')
