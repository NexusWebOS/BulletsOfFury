from pathlib import Path
import sys,json
from playwright.sync_api import sync_playwright
R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');W=Path(__file__).resolve().parent
sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import serve,TRAP_RAF,STEP
port,stop=serve(str(R));errors=[];out={}
try:
 with sync_playwright()as pw:
  b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)))
  p.goto(f'http://127.0.0.1:{port}/index.html?debug=1',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5');p.mouse.click(3,3);p.evaluate(TRAP_RAF)
  p.evaluate('run.stage=7;stageLoadBegin(7)');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(7)}',timeout=180000)
  p.evaluate('''()=>{diffKey='furious';debugStartFight({stage:7,role:'boss',kind:'sludgeemperor'},{pilot:'cole'});spawnBoss('sludgeemperor');debugFight.spawned=true;warnT=0;BOFCinematicDirector.cancel();setState(GS.PLAY);bossActive=true;DBGT.god=true;const M=s7mInit(boss);M.parts.forEach(p=>{if(p.id.startsWith('front')||p.id.startsWith('gun'))p.hp=0;});boss.y=270;M.drop=M.height=0;M.r25Walk=false;s7mSet(boss,'er28-mortar');run.weapon=3;run.wlevel=5;run.wlevels=WEAPONS.map(()=>5);run.bombs=0;Input.keys.j=false;}''')
  out['fixture']='Native rear-stage fixture. Front/gun HP removed before test; rear HP and later damage are unmodified. Actual player laser input only; no missiles.'
  out['parts']=[]
  for id in ['rearL','rearR']:
   before=p.evaluate('''id=>{const b=boss,M=b._s7mod;s7mSet(b,'er28-mortar');b.y=270;M.drop=M.height=0;const pose=s7mPose(b).find(p=>p.id===id),q=s7mWorld(b,pose.target);player.x=q.x;player.y=VH-65;Input.keys.j=true;return{id,hp:M.parts.find(p=>p.id===id).hp,target:q,center:b.x};}''',id)
   for _ in range(6):
    err=p.evaluate(STEP,30)
    if err:errors.append(err)
   after=p.evaluate('''id=>({hp:boss._s7mod.parts.find(p=>p.id===id).hp,core:boss._s7mod.core,cans:boss._s7mod.er28Canisters.map(c=>c.hp),weapon:run.weapon})''',id);out['parts'].append({'before':before,'after':after,'ordinaryLaserDamagedLeg':after['hp']<before['hp']})
   p.screenshot(path=str(W/(id+'-laser-native.png')))
  out['canisterShots']=[]
  for id in ['canL','canR']:
   before=p.evaluate('''id=>{const b=boss,M=b._s7mod;s7mSet(b,'er28-mortar');const pose=s7mPose(b).find(p=>p.id===id),q=s7mWorld(b,pose);player.x=q.x;player.y=VH-65;Input.keys.j=true;return{id,hp:M.er28Canisters.find(p=>p.id===id).hp};}''',id)
   p.evaluate(STEP,120);after=p.evaluate('id=>boss._s7mod.er28Canisters.find(p=>p.id===id).hp',id);out['canisterShots'].append({'id':id,'before':before['hp'],'after':after,'damaged':after<before['hp']})
  p.evaluate('Input.keys.j=false');out['coreStillProtected']=p.evaluate('boss._s7mod.er28Canisters.some(c=>c.hp>0)&&boss._s7mod.core===boss._s7mod.coreMax')
  out['jumpMarker']=p.evaluate('''()=>{const b=boss,M=b._s7mod;M.mode='recover';player.x=camLeftX()+45;M.r25Jump=2;s7mSet(b,'jump');return{mode:M.mode,middle:worldWidth()/2,x:M.target.x,markerX:M.landing?.x,y:M.target.y,markerY:M.landing?.y}}''');out['jumpMarkerMatchesLane']=out['jumpMarker']['mode']=='jump'and out['jumpMarker']['x']==out['jumpMarker']['middle']==out['jumpMarker']['markerX']and abs(out['jumpMarker']['markerY']-out['jumpMarker']['y']-55)<.01
  b.close()
finally:stop()
out['errors']=errors;out['passed']=all(q['ordinaryLaserDamagedLeg']for q in out['parts'])and all(q['damaged']for q in out['canisterShots'])and out['coreStillProtected']and out['jumpMarkerMatchesLane']and not errors;(W/'rear-weapon-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out),flush=True)
