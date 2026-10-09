"""Export current actor plates through Chromium's own game drawImage path."""
from pathlib import Path
import sys,json,base64,io,argparse
from PIL import Image,ImageDraw
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'))
import shoot
OUT=ROOT/'_shots/smooth_motion_1009';SRC=ROOT/'_ART_SOURCES/smooth_motion_1009/reference'
OUT.mkdir(parents=True,exist_ok=True);SRC.mkdir(parents=True,exist_ok=True)
args=argparse.ArgumentParser();args.add_argument('--refresh-reference',action='store_true');opts=args.parse_args()
if (SRC/'roster.json').exists() and not opts.refresh_reference:
 sys.exit('Authored reference baseline already exists. Use --refresh-reference only when intentionally replacing it for a new art pass.')
errors=[];records=[];port,stop=shoot.serve(str(ROOT))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch();p=br.new_page(viewport={'width':1280,'height':900});p.set_default_timeout(120000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.goto(f'http://127.0.0.1:{port}/index.html')
  p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF);p.wait_for_timeout(60)
  p.evaluate('()=>{if(typeof SM10!=="undefined"){drawEnemy=SM10.base.enemy;drawModularTank=SM10.base.tank;XART.get=SM10.base.get;furyShipCanvas=SM10.base.fury;}}')
  for stage in range(2,9):
   p.evaluate('(n)=>{beginStage(n);setState(GS.PLAY);BOFCinematicDirector.cancel();story=null;fb2Talk=null;boss=null;subBoss=null;enemies=[];stagePlan=[];player.invuln=1e9;}',stage)
   for _ in range(1800):
    if p.evaluate('()=>{stageLoadTick();return stageLoadInfo(run.stage).ready;}'):break
    p.wait_for_timeout(20)
   units=p.evaluate('()=>Object.keys(({2:VOLC,3:S3ICE,4:S4CHASE,5:S5SPACE,6:S6STORM,7:S7TOXIC,8:S8MEGA})[run.stage])')
   if stage==2:units=[u for u in units if u!='golem']+['firejet1002']
   sheet=Image.new('RGBA',(6*200,((len(units)+5)//6)*220),(15,22,32,255));g=ImageDraw.Draw(sheet)
   for i,unit in enumerate(units):
    meta=p.evaluate('(type)=>{enemies=[];spawnEnemy(type,240,220);window.E=enemies.at(-1);if(!E)return null;E.x=240;E.y=220;E.spin=0;E.t=0;E.hp=E.maxhp;E.flash=0;E._bank=E._frBank=0;drawEnemy(E);return {stage:run.stage,type:E.type,w:E.w,h:E.h,biome:E._biomePlate,volc:E._volc,ice:E._s3ice,chase:E._s4chase,space:E._s5space,storm:E._s6storm,toxic:E._s7toxic,mega:E._s8mega,mutator:E._mutator1003,alien:E._alien1003,mod:E._modTank||E._modJet||E._toxicJet};}',unit)
    if not meta:continue
    for _ in range(20):p.evaluate('drawEnemy(E)');p.wait_for_timeout(20)
    q=p.evaluate('()=>{const c=document.createElement("canvas");c.width=c.height=512;const g=c.getContext("2d"),draw=ctx.drawImage;ctx.save();ctx.setTransform(3,0,0,3,256-E.x*3,256-E.y*3);ctx.drawImage=function(...args){g.setTransform(ctx.getTransform());g.globalAlpha=ctx.globalAlpha;g.globalCompositeOperation=ctx.globalCompositeOperation;g.drawImage(...args);return draw.apply(ctx,args);};try{drawEnemy(E);}finally{ctx.drawImage=draw;ctx.restore();}return c.toDataURL().split(",")[1];}')
    im=Image.open(io.BytesIO(base64.b64decode(q))).convert('RGBA');im.save(SRC/(f'stage{stage}_{unit}.png'));meta['reference']=f'stage{stage}_{unit}.png';records.append(meta)
    thumb=im.resize((200,200),Image.Resampling.NEAREST);sheet.alpha_composite(thumb,((i%6)*200,(i//6)*220+20));g.text(((i%6)*200+4,(i//6)*220+3),unit,fill='#dde9ff')
   sheet.save(OUT/f'stage{stage}-roster.png');print('STAGE',stage,len(units),flush=True)
  # Export the nine pilot neutral hulls plus current Furyship, no baked plume.
  for pilot in ['axel','cole','decker','falva','freezer','juggernaut','lizzie','maverick','yuri']:
   p.evaluate('(pk)=>{run.pilot=pk;XART.rdy("ship_"+pk);}',pilot)
   for _ in range(50):
    if p.evaluate('(pk)=>XART.rdy("ship_"+pk)',pilot):break
    p.wait_for_timeout(20)
   q=p.evaluate('(pk)=>{const im=XART.get("ship_"+pk),c=document.createElement("canvas");c.width=c.height=512;const g=c.getContext("2d"),k=400/im.height;g.imageSmoothingEnabled=false;g.drawImage(im,256-im.width*k/2,56,im.width*k,400);return c.toDataURL().split(",")[1];}',pilot)
   Image.open(io.BytesIO(base64.b64decode(q))).save(SRC/('pilot_'+pilot+'.png'))
  p.evaluate('furyShipReady()');p.wait_for_timeout(1000)
  q=p.evaluate('()=>{const c=document.createElement("canvas");c.width=c.height=512;const g=c.getContext("2d"),draw=ctx.drawImage;ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.drawImage=function(...args){g.setTransform(ctx.getTransform());g.drawImage(...args);return draw.apply(ctx,args);};try{furyShipBlit("base",256,256,400,400,"axel");}finally{ctx.drawImage=draw;ctx.restore();}return c.toDataURL().split(",")[1];}')
  Image.open(io.BytesIO(base64.b64decode(q))).save(SRC/'furyship.png')
  # Export each directional BLUE cell using the original game crop utility.
  for f in range(3):
   q=p.evaluate('(f)=>{const c=document.createElement("canvas");c.width=c.height=512;const g=c.getContext("2d"),draw=ctx.drawImage;ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.drawImage=function(...args){g.setTransform(ctx.getTransform());g.drawImage(...args);return draw.apply(ctx,args);};try{missionCell("bluejets",f,0,0,512,512);}finally{ctx.drawImage=draw;ctx.restore();}return c.toDataURL().split(",")[1];}',f)
   Image.open(io.BytesIO(base64.b64decode(q))).save(SRC/f'bluejet_{f}.png')
  br.close()
finally:stop()
(SRC/'roster.json').write_text(json.dumps({'actors':records,'errors':errors},indent=2)+'\n',encoding='utf-8')
print('Actors',len(records),'errors',errors,flush=True)
