"""Current Stage 1 animation acceptance, real Chromium and game drawImage.

Exports complete 8-idle/4-fire reference reels without flattening the runtime's
independent turret, launch rack, bank/roll or targetable module ownership.
"""
from pathlib import Path
import sys,json,base64,subprocess
from PIL import Image,ImageDraw
from playwright.sync_api import sync_playwright
import imageio_ffmpeg
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'))
import shoot
OUT=ROOT/'_shots/boss_motion_1009';DEST=ROOT/'_ART_SOURCES/stage1_motion_1009/returned_live'
OUT.mkdir(parents=True,exist_ok=True)
DEST.mkdir(parents=True,exist_ok=True)
units=['s1tankheavy','s1tanklight','s1tankapc','s1truckmissile','s1boatpatrol','s1boatgun','s1corvette','s1landingcraft','s1jetdelta','s1jetbomber']
errors=[];checks=[];reels={};port,stop=shoot.serve(str(ROOT))
def check(name,ok,data=None):checks.append({'name':name,'pass':bool(ok),'data':data});print(('PASS ' if ok else 'FAIL ')+name,flush=True)
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1280,'height':900});p.set_default_timeout(120000)
  p.on('pageerror',lambda e:errors.append(str(e)))
  p.on('console',lambda m:errors.append(m.text[:700]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append(f'HTTP {r.status} {r.url}') if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
  p.wait_for_timeout(50)
  p.evaluate('()=>{beginStage(1);setState(GS.PLAY);BOFCinematicDirector.cancel();story=null;stagePlan=[];enemies=[];boss=null;subBoss=null;player.invuln=1e9;s1mWarm();}')
  for _ in range(2000):
   if p.evaluate('()=>{stageLoadTick();return stageLoadInfo(1).ready&&s1mKeys().every(k=>XART.rdy(k));}'):break
   p.wait_for_timeout(25)
  else:raise RuntimeError('Stage 1 or generated cells failed to load')
  check('All 48 moving-part cells and four-frame muzzle aliases load',p.evaluate('Object.values(S1M_ART).flat().length===48&&s1mKeys().every(k=>XART.rdy(k))'))
  contact=Image.new('RGBA',(8*160,len(units)*160),(14,22,33,255));labels=ImageDraw.Draw(contact)
  def new(unit):
   p.evaluate('(type)=>{enemies=[];eBullets=[];spawnEnemy(type,240,220);window.E=enemies.at(-1);E.x=240;E.y=220;E.spin=0;E._navBob=E._navLean=E._navPulse=0;E._furyMove=null;E.hp=E.maxhp;E.flash=0;E.t=0;E._s1mFired=null;drawEnemy(E);}',unit)
   for _ in range(12):p.wait_for_timeout(25);p.evaluate('()=>drawEnemy(E)')
  def render(t,fire=False,flash=False):
   q=p.evaluate('([t,fire,flash])=>{E.t=t;E._s1mFired=fire?0:null;E.flash=flash?.12:0;const c=document.createElement("canvas");c.width=c.height=512;const g=c.getContext("2d"),draw=ctx.drawImage;ctx.save();ctx.setTransform(3,0,0,3,256-E.x*3,256-E.y*3);ctx.drawImage=function(...args){g.setTransform(ctx.getTransform());g.globalAlpha=ctx.globalAlpha;g.globalCompositeOperation=ctx.globalCompositeOperation;g.imageSmoothingEnabled=ctx.imageSmoothingEnabled;g.drawImage(...args);return draw.apply(ctx,args);};try{drawEnemy(E);}finally{ctx.drawImage=draw;ctx.restore();}return c.toDataURL().split(",")[1];}',[t,fire,flash])
   import io
   return Image.open(io.BytesIO(base64.b64decode(q))).convert('RGBA')
  for row,unit in enumerate(units):
   new(unit);strip=Image.new('RGBA',(8*512,512));cells=[]
   fps=12 if unit=='s1tanklight' else 10
   for i in range(8):
    im=render((i+.01)/fps);cells.append(im);strip.alpha_composite(im,(i*512,0));thumb=im.resize((160,160),Image.Resampling.NEAREST);contact.alpha_composite(thumb,(i*160,row*160));labels.text((i*160+3,row*160+2),unit+' '+str(i+1),fill='#dce4ee')
   strip.save(DEST/(unit+'__idle_intact__01-08.png'))
   unique=len({im.tobytes() for im in cells});check(unit+' has eight distinct idle cells',unique==8,unique)
   if unit!='s1landingcraft':
    strip=Image.new('RGBA',(4*512,512));fire_cells=[]
    for i in range(4):
     # The existing Fury Fleet launch rig remains separately articulated.
     p.evaluate('(i)=>{const M=furyBoatModules(E);if(M)for(const m of M){m.phase="launch";m.t=i*.12;}}',i)
     if not p.evaluate('E._modTank===1||E.type==="s1truckmissile"'):
      p.evaluate('(i)=>{_navalFlashes=[];S1M.actor=E;navalFlash(E,{x:E.x,y:E.y+E.h*.44},.8,E.type.includes("bomber")||E.type==="s1boatgun"?S1_MUZZLE_MILITARY:S1_MUZZLE_ROTARY,{hpx:34,life:.26});S1M.actor=null;_navalFlashes.at(-1).t=(i+.01)*.065;}',i)
     im=render((i+.01)*.065,True)
     # Naval flashes normally render in the world layer, separately from actors.
     if not p.evaluate('E._modTank===1||E.type==="s1truckmissile"'):
      q=p.evaluate('()=>{const c=document.createElement("canvas");c.width=c.height=512;const g=c.getContext("2d"),draw=ctx.drawImage;ctx.save();ctx.setTransform(3,0,0,3,256-E.x*3,256-E.y*3);ctx.drawImage=function(...args){g.setTransform(ctx.getTransform());g.globalAlpha=ctx.globalAlpha;g.globalCompositeOperation=ctx.globalCompositeOperation;g.imageSmoothingEnabled=ctx.imageSmoothingEnabled;g.drawImage(...args);return draw.apply(ctx,args);};try{drawNavalFlashes();}finally{ctx.drawImage=draw;ctx.restore();}return c.toDataURL().split(",")[1];}')
      import io
      im.alpha_composite(Image.open(io.BytesIO(base64.b64decode(q))).convert('RGBA'))
     strip.alpha_composite(im,(i*512,0));fire_cells.append(im)
    strip.save(DEST/(unit+'__fire_intact__01-04.png'));check(unit+' has four distinct fire cells',len({im.tobytes() for im in fire_cells})==4)
   new(unit);normal=render(.3);hit=render(.3,flash=True)
   normal.save(OUT/(unit+'-normal.png'));hit.save(OUT/(unit+'-hit.png'))
   # Compare only the authored opaque body pixels; wakes/exhaust must keep moving.
   import numpy as np
   a=np.array(normal);b=np.array(hit);mask=(a[:,:,3]>220)&(a[:,:,:3].max(axis=2)>24)
   brighter=float((b[:,:,:3].mean(axis=2)[mask]>a[:,:,:3].mean(axis=2)[mask]+24).mean())
   check(unit+' body retains visible white hit flash',brighter>.45,round(brighter,3))
   reels[unit]={'idle':8,'fire':0 if unit=='s1landingcraft' else 4,'design':'current live renderer','runtime':'independent parts, not flattened reel'}
  contact.save(OUT/'stage1-native-reels.png')
  new('s1tankheavy')
  p.evaluate('()=>{E._modAngle=Math.PI/2-.65;E.t=.2;}');left=render(.2)
  p.evaluate('()=>{E._modAngle=Math.PI/2+.65;}');right=render(.2)
  check('Tank turret still aims independently in both directions',left.tobytes()!=right.tobytes())
  left.save(OUT/'stage1-turret-left.png');right.save(OUT/'stage1-turret-right.png')
  new('s1boatgun');p.evaluate('()=>{const M=furyBoatModules(E);M[0].hp=0;M[0].phase="destroyed";}');render(.2).save(OUT/'stage1-broken-boat-module.png')
  check('Boat weapons retain their own destructible HP and ready/launch/reload states',p.evaluate('()=>{const M=furyBoatModules(E);return M[0].hp===0&&M[1].hp>0;}'))
  new('s1truckmissile');p.evaluate('()=>{const count=eBullets.length;S1M.actor=E;eShootT(E.x,E.y+40,Math.PI/2,3,"s1jungleMissile",{});S1M.actor=null;window.lastRocket=eBullets.at(-1);}');check('Buggy launches real rocket from authored roof tube',p.evaluate('()=>lastRocket.x===E.x-11&&lastRocket.y===E.y-20&&S1M.shots.at(-1).type===E.type'))
  # Real full-engine Stage 1 capture: no scripted replacement firing director.
  p.evaluate(shoot.SETUP,{'state':'PLAY','stage':1,'pilot':'yuri','invuln':True})
  p.evaluate('()=>{run.mode="arcade";diffKey="normal";DIFF=difficultyForRun(run.mode,diffKey);run.pilot="yuri";beginStage(1);setState(GS.PLAY);player.reset();player.x=worldWidth()/2;player.y=VH-110;player.dead=false;player.out=false;BOFCinematicDirector.cancel();story=null;fb2Talk=null;special=null;thunderStorm=null;thaw=null;player.invuln=1e9;timeScale=1;window.s1Shots=0;}')
  for _ in range(1800):
   if p.evaluate('()=>{stageLoadTick();return stageLoadInfo(1).ready;}'):break
   p.wait_for_timeout(25)
  # Use the repository's complete frame loop: terrain scroll is draw-owned.
  # updatePlay alone plus drawWorld(0) freezes the wave-gating terrain clock
  # and can enter the dam assault before covering any ordinary naval waves.
  for _ in range(90):
   err=p.evaluate(shoot.STEP,60)
   if err:raise RuntimeError('Stage 1 loop: '+err)
   if p.evaluate('S1M.shots.length>0'):break
   p.wait_for_timeout(10)
  print('LIVE START '+json.dumps(p.evaluate('({stageTimer,waveIdx,waves:stagePlan.length,player:{x:player.x,y:player.y,dead:player.dead},actors:enemies.map(e=>({type:e.type,x:e.x,y:e.y,pattern:e.pattern,atk:e._atk,mod:e._modJet,sp:e._spd,fire:e._shotCd})),shots:S1M.shots.length})')),flush=True)
  folder=OUT/'stage1-gameplay';folder.mkdir(exist_ok=True)
  live_types=set()
  for i in range(40*15):
   err=p.evaluate(shoot.STEP,4)
   if err:raise RuntimeError('Stage 1 capture loop: '+err)
   p.evaluate('s1Shots=Math.max(s1Shots,S1M.shots.length)')
   live_types.update(p.evaluate('S1M.shots.map(q=>q.type)'))
   (folder/f'{i:04d}.png').write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')));p.wait_for_timeout(5)
  subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-v','error','-y','-framerate','15','-i',str(folder/'%04d.png'),'-c:v','libx264','-crf','19','-pix_fmt','yuv420p',str(OUT/'stage1-gameplay.mp4')],check=True)
  data=p.evaluate('({shots:s1Shots,draws:S1M.draws})');data['types']=sorted(live_types)
  check('Stage 1 live controllers fire during full-engine gameplay',p.evaluate('s1Shots>0'),data)
  br.close()
finally:stop()
check('No page, console or asset errors',not errors,errors)
(DEST/'manifest.json').write_text(json.dumps(reels,indent=2)+'\n',encoding='utf-8')
result={'passed':sum(c['pass'] for c in checks),'failed':[c for c in checks if not c['pass']],'errors':errors,'checks':checks}
(OUT/'stage1-verification.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps({'passed':result['passed'],'failed':result['failed'],'errors':errors}),flush=True)
if result['failed'] or errors:sys.exit(1)
