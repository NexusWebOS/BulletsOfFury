"""Export the live Stage 1 renderers, not the historical NEF plate aliases."""
from pathlib import Path
import sys,json,base64
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'))
import shoot
OUT=ROOT/'_shots/boss_motion_1009';SEED=ROOT/'_ART_SOURCES/stage1_motion_1009/live_reference'
OUT.mkdir(parents=True,exist_ok=True)
SEED.mkdir(parents=True,exist_ok=True)
units=['s1tankheavy','s1tanklight','s1tankapc','s1truckmissile','s1boatpatrol','s1boatgun','s1corvette','s1landingcraft','s1jetdelta','s1jetbomber']
errors=[];port,stop=shoot.serve(str(ROOT))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch();p=br.new_page(viewport={'width':1280,'height':900})
  p.on('pageerror',lambda e:errors.append(str(e)))
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
  p.evaluate('()=>{beginStage(1);setState(GS.PLAY);BOFCinematicDirector.cancel();story=null;stagePlan=[];enemies=[];boss=null;subBoss=null;run.shield=0;window.refs=[];}')
  for _ in range(1800):
   if p.evaluate('()=>{stageLoadTick();return stageLoadInfo(1).ready;}'):break
   p.wait_for_timeout(25)
  for unit in units:
   p.evaluate('(type)=>{spawnEnemy(type,240,220);const e=enemies.at(-1);e.x=240;e.y=220;e.spin=0;e._navBob=0;e._navLean=0;e._navPulse=0;e.flash=0;e.hp=e.maxhp;e._furyMove=null;window.E=e;drawEnemy(e);}',unit)
   for _ in range(24):
    p.wait_for_timeout(60);p.evaluate('()=>{ctx.setTransform(SS,0,0,SS,0,0);drawEnemy(E);}')
   data=p.evaluate('()=>{const canvas=document.createElement("canvas");canvas.width=640;canvas.height=640;const g=canvas.getContext("2d"),draw=ctx.drawImage;ctx.save();ctx.setTransform(4,0,0,4,320-E.x*4,320-E.y*4);ctx.drawImage=function(...args){g.setTransform(ctx.getTransform());g.globalAlpha=ctx.globalAlpha;g.globalCompositeOperation=ctx.globalCompositeOperation;g.imageSmoothingEnabled=ctx.imageSmoothingEnabled;g.drawImage(...args);return draw.apply(ctx,args);};try{drawEnemy(E);}finally{ctx.drawImage=draw;ctx.restore();}return{png:canvas.toDataURL().split(",")[1],type:E.type,art:E.art,nef:E._nef,modTank:E._modTank,fury:furyJetVariant(E),w:E.w,h:E.h,drawW:E._drawW,drawH:E._drawH};}')
   (SEED/(unit+'.png')).write_bytes(base64.b64decode(data.pop('png')))
   p.evaluate('(d)=>refs.push(d)',data)
  (SEED/'manifest.json').write_text(json.dumps(p.evaluate('refs'),indent=2),encoding='utf-8')
  for key in ['overhaul_tank_1_hull','overhaul_tank_1_turret','furyboat_0_0','furyboat_1_0','furyjet_0_bank_0','furyjet_1_bank_0','furyjet_2_bank_0','furyjet_3_bank_0']:
   for _ in range(180):
    if p.evaluate('(k)=>XART.rdy(k)',key):break
    p.wait_for_timeout(30)
   q=p.evaluate('(k)=>{const im=k.startsWith("furyjet")?furyJetGreenFrame(k,+k.split("_")[1],XART.get(k)):XART.get(k),c=document.createElement("canvas");c.width=im.width||im.naturalWidth;c.height=im.height||im.naturalHeight;c.getContext("2d").drawImage(im,0,0);return c.toDataURL().split(",")[1];}',key)
   (SEED/(key+'.png')).write_bytes(base64.b64decode(q))
  print(json.dumps({'units':len(units),'errors':errors,'directory':str(SEED)}));br.close()
finally:stop()
if errors:sys.exit(1)
