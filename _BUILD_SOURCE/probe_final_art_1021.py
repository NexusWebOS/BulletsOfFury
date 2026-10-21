from pathlib import Path
from PIL import Image
from io import BytesIO
from playwright.sync_api import sync_playwright
import ast,sys,json,base64,http.server
R=Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury');sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
O=R/'_shots/final_version_1021/native';O.mkdir(parents=True,exist_ok=True);checks=[];errors=[]
def getconst(file,name):return next(ast.literal_eval(n.value) for n in ast.parse((R/'_BUILD_SOURCE'/file).read_text(encoding='utf-8')).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id==name for t in n.targets))
SETUP=getconst('probe_feedback_1002.py','SETUP');BOOT=getconst('probe_boss_redesign_1020.py','BOOT')
def ck(name,ok,data=None):checks.append(dict(name=name,ok=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name,flush=True)
http.server.ThreadingHTTPServer.request_queue_size=128;port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport=dict(width=1440,height=1000));p.set_default_timeout(180000);p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:800]) if m.type=='error' or 'draw error' in m.text else None)
  p.goto(f'http://127.0.0.1:{port}');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF);p.mouse.click(600,400)
  p.evaluate(SETUP,dict(stage=8,kind='vileexistence',pilot='cole'));p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(8)&&v18Warm()}');p.evaluate(BOOT)
  for diff in ['easy','normal','hard','furious']:
   for kind in ['skystrike','side','throw','spin','dance','charge','shield','ball','pickup','gun','break','punch','fists']:
    row=p.evaluate('''([kind,diff])=>{setup20(8,diff);Q=hb20State(B);hb20Start(B,kind);tick20(30);paint20();const q=hb20Pose(B);return{key:q.a.key,k:q.k,finite:Number.isFinite(B.x+B.y),action:Q.action?.type};}''',[kind,diff]);ck(diff+' '+kind+' selects the re-authored bank',row['key'].startswith('fv21_hammer_') and row['finite'],row)
    if diff=='normal':(O/('hammer-'+kind+'.png')).write_bytes(base64.b64decode(p.evaluate('cv.toDataURL().split(",")[1]')))
   row=p.evaluate('''diff=>{setup20(8,diff);Q=hb20State(B);Q.shield=0;Q.action=null;const before=capturePart20('core');B._lastPart=B.parts[0];modularHit(1);const after=capturePart20('core');let pixels=0;for(let i=0;i<after.length;i+=4)if(before[i]!==after[i]||before[i+1]!==after[i+1]||before[i+2]!==after[i+2])pixels++;tick20(18);return{pixels,expired:B.flash<=0,key:hb20Pose(B).a.key};}''',diff);ck(diff+' Hammer visibly flashes and expires',row['pixels']>20 and row['expired'],row)
  p.evaluate(SETUP,dict(stage=6,pilot='cole'));p.evaluate('run._gp4StageX="right";CC21.card=3;CC21.owner="right";CC21.t=0;');p.wait_for_function('stageXArenaReady()')
  for t in [0,12,36,68,93]:
   row=p.evaluate('''t=>{CC21.t=t;ctx.setTransform(SS,0,0,SS,0,0);stageXArenaDraw(0);return{sy:stageXArenaSrcY(),t:CC21.t};}''',t);ck('coastal city '+str(t)+'s scroll stays finite',isinstance(row['sy'],(int,float)),row);(O/f'city-{t}.png').write_bytes(base64.b64decode(p.evaluate('cv.toDataURL().split(",")[1]')))
  for family in ['bubble_hex','bubble_volt','bubble_fire','bubble_toxic','bubble_ice','bubble_void']:
   row=p.evaluate('''family=>{const e={x:VW/2,y:VH/2,w:90,h:90,t:1},s=enemyShieldEquip(e,family,100);s.phase='active';for(const a of Object.values(FV21_ART.sheets))XART.rdy(a.key);return{kind:s.kind};}''',family)
   p.wait_for_function('()=>Object.values(FV21_ART.sheets).filter(a=>a.key.includes("shield")).every(a=>XART.rdy(a.key))')
   row=p.evaluate('''family=>{const e={x:VW/2,y:VH/2,w:90,h:90,t:1},s=enemyShieldEquip(e,family,100);s.phase='active';s.animT=1;ctx.setTransform(SS,0,0,SS,0,0);ctx.fillStyle='#071626';ctx.fillRect(0,0,VW,VH);ctx.fillStyle='#ffa040';ctx.fillRect(e.x-20,e.y-20,40,40);drawEnemyShieldLayer(e,true);return{draws:FV21.draws[FV21_SHIELDS[family]],center:Array.from(ctx.getImageData(Math.floor(e.x*SS),Math.floor(e.y*SS),1,1).data)};}''',family);ck(family+' new animated shell keeps hull visible',row['draws']>0 and row['center'][0]>100,row);(O/(family+'.png')).write_bytes(base64.b64decode(p.evaluate('cv.toDataURL().split(",")[1]')))
  ck('No native renderer errors',not errors,errors);br.close()
finally:stop()
(O/'report.json').write_text(json.dumps(dict(checks=checks,errors=errors),indent=2));print(json.dumps(dict(checks=len(checks),passed=sum(q['ok'] for q in checks),errors=errors)));sys.exit(bool(errors) or not all(q['ok'] for q in checks))
