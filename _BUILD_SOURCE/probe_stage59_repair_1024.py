from pathlib import Path
import json,base64
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/stage59_1024';O.mkdir(exist_ok=True);checks=[];errors=[]
def ck(name,ok,data=None):checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name,flush=True)
port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--mute-audio','--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1280,'height':900});p.set_default_timeout(180000);p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:300]) if m.type=='error' else None);p.goto(f'http://127.0.0.1:{port}');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
  if not p.evaluate('!!window.BOF_STAGE59_REPAIR'):p.add_script_tag(url=f'http://127.0.0.1:{port}/assets/stage59_repair_1024.js')
  for diff in ['normal','hard','furious']:
   p.evaluate('''d=>{diffKey=d;debugStartFight({stage:5,role:'mini',kind:'spacebomber',name:'Space Bomber'},{pilot:'maverick'});spawnSubBoss__inner('spacebomber');window.B=subBoss;debugFight.spawned=true;B.enter=B._noHit=false;B.y=B.ty;B._drawY=B.y;B._bomber.mode='hc-recover';BOFCinematicDirector.cancel();fb2Intro=null;story=null;player.dead=false;player.y=VH-55;player.invuln=1e9;enemies=[];l5Rocks=[];eBullets=[];pBullets=[];}''',diff)
   row=p.evaluate('''()=>{const P=B._bomber.parts.find(p=>p.id==='laserR');B._bomber.core=0;for(const p of B._bomber.parts)if(p!==P)p.hp=0;B.hp=P.hp;const q=siegeBomberParts(B).find(p=>p.id==='laserR'),before=P.hp;const shot={kind:'spaceLaser',x:q.x,y:q.y+q.h*.45,vx:0,vy:0,w:8,h:24,dmg:10,lv:1,t:0,seat:1};spaceBulletTick(shot,1/60);retinaScanClear();const targets=retinaBossTargets(B);for(const t of targets)retinaScanAdd(t);return{damage:before-P.hp,targets:targets.map(t=>({id:t._retinaId,valid:retinaTargetValid(t)})),marks:retinaScanState().marks.length,kind:shot.kind}}''')
   ck(diff+' native space laser damages last right turret',row['damage']==10,row);ck(diff+' Retina exposes only surviving right turret',len(row['targets'])==1 and row['targets'][0]['valid'] and row['marks']==1,row)
   # Trace real full-column beam into the surviving module, then exhaust the
   # final displayed pool through native travelling laser hits, not a forced win.
   row=p.evaluate('''()=>{const P=B._bomber.parts.find(p=>p.id==='laserR'),q=siegeBomberParts(B).find(p=>p.id==='laserR'),beam={x:q.x,w:10,top:-20,bot:VH-50},hit=siegeBomberBeam(B,beam),before=P.hp;if(hit)siegeBomberHit(B,4,hit.x,hit.y,hit.id);const damage=before-P.hp;for(let i=0;i<500&&!B.dead;i++){const q=siegeBomberParts(B).find(p=>p.id==='laserR');spaceBulletTick({kind:'spaceLaser',x:q.x,y:q.y,vx:0,vy:0,w:8,h:24,dmg:10,lv:1,t:0,seat:1},1/60);}return{damage,dead:B.dead,hp:B.hp,pool:P.hp,live:retinaBossTargets(B).length}}''')
   ck(diff+' held beam reaches right turret and native final exhaustion wins',row['damage']==4 and row['dead'] and row['hp']==0 and row['pool']==0 and row['live']==0,row)
  p.evaluate("()=>{debugStartFight({stage:9,role:'mini',kind:'voidhorizon',name:'Black Event Horizon'},{pilot:'maverick'});spawnSubBoss__inner('voidhorizon');window.B=subBoss;debugFight.spawned=true;player.invuln=1e9;BOFCinematicDirector.cancel();fb2Intro=null;story=null;}")
  p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(9)&&["ns9x_horizonblk_0","bf22_water_orb"].every(k=>XART.rdy(k))}',timeout=180000)
  for diff in ['normal','hard','furious']:
   row=p.evaluate('''d=>{diffKey=d;const F=B._s9rift;F.t=0;F.s5924={mode:'entry',t:0,age:0,cycle:0};B.dead=false;F.core.disabled=false;F.core.hp=F.core.maxhp;const modes=new Set(),positions=[];eBullets=[];S5924.shots=[];let warnings=0;const warn=combatWarningDraw;combatWarningDraw=function(owner,q){if(owner===B&&q.fieldOnly)warnings++;return warn.apply(this,arguments)};try{for(let i=0;i<1440;i++){s9VoidHorizonTick(B,1/60);modes.add(F.s5924.mode);if(i%60===0){positions.push([B.x,B.y]);s9VoidHorizonDraw(B);}for(const q of eBullets){q.x+=q.vx;q.y+=q.vy;}eBullets=eBullets.filter(q=>q.y>-80&&q.y<VH+80&&q.x>camLeftX()-80&&q.x<camRightX()+80);}}finally{combatWarningDraw=warn}return{modes:[...modes],movement:Math.max(...positions.map(q=>q[0]))-Math.min(...positions.map(q=>q[0])),warnings,shots:S5924.shots.length,allFromEye:S5924.shots.every(q=>Math.hypot(q.x-q.eye.x,q.y-q.eye.y)<.01),finite:Number.isFinite(B.x+B.y),width:B.w,height:B.h}}''',diff)
   ck(diff+' black horizon moves and uses all four warned eye attacks',row['finite'] and row['movement']>100 and all(x in row['modes'] for x in ['aimed','orbit','sweep','spin']) and row['warnings']>0 and row['shots']>0 and row['allFromEye'],row)
  ck('No page/console errors',not errors,errors)
  br.close()
finally:stop()
result=dict(passed=sum(c['passed'] for c in checks),failed=sum(not c['passed'] for c in checks),checks=checks,errors=errors);(O/'repair-report.json').write_text(json.dumps(result,indent=2)+'\n');print('SUMMARY',result['passed'],result['failed']);raise SystemExit(bool(result['failed']))
