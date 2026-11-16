from pathlib import Path
from playwright.sync_api import sync_playwright
import sys,json
R=Path(__file__).resolve().parents[1];O=R/'_shots/release_qa_1116/weapons';O.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
rows=[];errors=[]
with sync_playwright()as w:
 b=w.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1440,'height':1000});p.set_default_timeout(180000)
 p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None);p.on('response',lambda r:errors.append(str(r.status)+' '+r.url)if r.status>=400 else None)
 p.goto('http://127.0.0.1:8765/index.html?release-weapons=1116');p.wait_for_function('window.__bofFrames>6');p.evaluate(shoot.TRAP_RAF);p.evaluate(shoot.SETUP,{'state':'PLAY','stage':1,'pilot':'cole','invuln':False});p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(1)}',polling=50)
 p.evaluate("()=>{BOFOnline.submitScore=()=>{};enemies=[];boss=subBoss=null;bossActive=subBossActive=false;special=thunderStorm=null;run._primary1003b='mg';run.ngplus=true;run._earnedUnlocks={mist:true,chaingun:true,lightningOrb:true};laserMistUnlocked=chaingunUnlocked=yuriLightningOrbUnlocked=true;}")
 pilots=p.evaluate('PILOTS.map(p=>p.key)')
 for pilot in pilots:
  for weapon in range(9):
   if weapon==8 and pilot!='yuri':continue
   for elem in [None]+p.evaluate('Object.keys(INFUSIONS)'):
    q={'pilot':pilot,'weapon':weapon,'element':elem}
    result=p.evaluate("""q=>{window.PREV16=forgePreviewNew(q.weapon,q.element,3);PREV16.pilot=q.pilot;const before={stage:run.stage,pilot:run.pilot,weapon:run.weapon,hp:run.lives,infusion:JSON.stringify(run.infusion)};let peak=0;const kinds=new Set(),infusions=new Set();for(let i=0;i<150;i++){forgePreviewTick(PREV16,400,440,1/60);peak=Math.max(peak,PREV16.bullets.length+PREV16.bursts.length+PREV16.parts.length+PREV16.zaps.length);for(const b of PREV16.bullets){kinds.add(b.kind||'standard');if(b._inf)infusions.add(b._inf);}}forgePreviewDraw(PREV16,40,20,VW-80,VH-40);const after={stage:run.stage,pilot:run.pilot,weapon:run.weapon,hp:run.lives,infusion:JSON.stringify(run.infusion)};return{error:PREV16.err,fired:PREV16.fired,peak,kinds:[...kinds],infusions:[...infusions],isolated:JSON.stringify(before)===JSON.stringify(after)};}""",q)
    row={**q,**result};rows.append(row);p.wait_for_timeout(1)
    if elem in [None,'fire','dark'] and weapon in [0,3,5]:
     p.evaluate('()=>forgePreviewDraw(PREV16,40,20,VW-80,VH-40)');p.locator('#screen').screenshot(path=str(O/f'{pilot}-w{weapon}-{elem or "base"}.jpg'),type='jpeg',quality=85)
   print(json.dumps({'pilot':pilot,'weapon':weapon,'cases':len(rows),'bad':sum(bool(r['error'])or not r['isolated']or not r['peak']for r in rows)}),flush=True)
   (O/'report.json').write_text(json.dumps({'scope':'All nine pilots, eligible base weapon slots and nine elements: native Forge preview emission/render and state-isolation smoke at weapon level3. Excludes Yuri-exclusive slot8 for other pilots. Not damage/balance or every live-stage loadout certification.','rows':rows,'errors':errors},indent=2),encoding='utf8')
 b.close()
print(json.dumps({'cases':len(rows),'errors':len(errors),'empty':[r for r in rows if not r['peak']],'exceptions':[r for r in rows if r['error']],'stateLeaks':[r for r in rows if not r['isolated']]}),flush=True)
