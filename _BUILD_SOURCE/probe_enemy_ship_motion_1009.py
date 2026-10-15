"""Actual Chromium renderer: reels, flashes, independent guns and ship rigs."""
from pathlib import Path
import sys,json,base64,io,subprocess
from PIL import Image,ImageDraw
import numpy as np
from playwright.sync_api import sync_playwright
import imageio_ffmpeg
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
OUT=ROOT/'_shots/smooth_motion_1009';OUT.mkdir(exist_ok=True);checks=[];errors=[];port,stop=shoot.serve(str(ROOT))
def check(name,ok,data=None):checks.append({'name':name,'pass':bool(ok),'data':data});print(('PASS ' if ok else 'FAIL ')+name,flush=True)
def image_of(p):return Image.open(io.BytesIO(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')))).convert('RGBA')
def inkbox(im):
 y,x=np.where(np.max(np.array(im)[:,:,:3],axis=2)>12);return (int(x.min()),int(y.min()),int(x.max())+1,int(y.max())+1)
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1280,'height':900});p.set_default_timeout(120000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:700]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append(f'HTTP {r.status} {r.url}') if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF);p.wait_for_timeout(60)
  p.evaluate('()=>sm10Warm(Object.keys(SM10_ART))');p.wait_for_function('()=>Object.values(SM10_ART).flat().every(a=>XART.rdy(a.key))',polling=50)
  check('Stage queues include new enemy and all pilot cells',p.evaluate('()=>[1,2,3,4,5,6,7,8,9].every(n=>{stageLoadBegin(n,[]);return sm10StageBanks(n).flatMap(k=>SM10_ART[k].map(a=>a.key)).every(k=>_stageLoads[n].keys.includes(k));})'))
  all_units=p.evaluate('()=>Object.entries(SM10_ENEMIES).flatMap(([n,units])=>Object.keys(units).map(type=>({stage:+n,type}))).concat([{stage:4,type:"s4airfield"},{stage:4,type:"s4minitank"}])')
  contact=Image.new('RGBA',(6*220,((len(all_units)+5)//6)*220),(15,22,32,255));g=ImageDraw.Draw(contact)
  for j,unit in enumerate(all_units):
   p.evaluate('(n)=>{H3.ending=null;beginStage(n);setState(GS.PLAY);story=null;BOFCinematicDirector.cancel();enemies=[];}',unit['stage'])
   for _ in range(1800):
    if p.evaluate('()=>{stageLoadTick();return stageLoadInfo(run.stage).ready;}'):break
    p.wait_for_timeout(20)
   p.evaluate('(type)=>{spawnEnemy(type,240,220);window.E=enemies.at(-1);E.x=240;E.y=220;E.spin=0;E.flash=0;E._bank=0;E.t=0;window.HP=[E.hp,E.maxhp,E.w,E.h];}',unit['type'])
   signatures=[];im=None
   for f in range(8):
    p.evaluate('(f)=>{E.t=(f+.01)/12;ctx.setTransform(SS,0,0,SS,0,0);ctx.clearRect(0,0,cv.width,cv.height);drawEnemy(E);}',f)
    q=p.evaluate('()=>cv.toDataURL()');signatures.append(q)
    if f==3:im=image_of(p)
   check(unit['type']+' eight rendered frames and unchanged hitbox/HP',len(set(signatures))==8 and p.evaluate('JSON.stringify(HP)===JSON.stringify([E.hp,E.maxhp,E.w,E.h])'))
   box=inkbox(im);thumb=im.crop(box);thumb.thumbnail((190,180),Image.Resampling.NEAREST);contact.alpha_composite(thumb,((j%6)*220+(220-thumb.width)//2,(j//6)*220+30));g.text(((j%6)*220+5,(j//6)*220+8),f"S{unit['stage']} {unit['type']}",fill='#dde9ff')
   p.evaluate('()=>{E.flash=.12;ctx.clearRect(0,0,cv.width,cv.height);drawEnemy(E);}')
   # The actual game context is alpha:false: cleared background also has A=255.
   # Measure the occupied RGB silhouette, not the whole opaque backing canvas.
   white=image_of(p);a=np.array(white);rgb=a[:,:,:3].astype(int);mask=np.max(rgb,axis=2)>80
   neutral=float(np.mean(np.ptp(rgb[mask],axis=1)<3)) if mask.any() else 0
   bright=float(np.mean(np.min(rgb[mask],axis=1)>220)) if mask.any() else 0
   check(unit['type']+' visible white hit frame',neutral>.99 and bright>.70,{'neutral':neutral,'bright':bright})
  contact.save(OUT/'enemy-native-contact.png')
  p.evaluate('()=>{beginStage(4);setState(GS.PLAY);enemies=[];spawnEnemy("s4airfield",240,220);window.E=enemies.at(-1);E.x=240;E.y=220;E.t=.1;E.flash=0;}')
  def tank_shot(angle):
   p.evaluate('(a)=>{E._modAngle=a;ctx.clearRect(0,0,cv.width,cv.height);drawEnemy(E);}',angle);return p.evaluate('()=>cv.toDataURL()')
  down=tank_shot(1.57079632679);left=tank_shot(3.14159265359);check('Desert turret still aims independently of the moving hull',down!=left and p.evaluate('E._modTank===4'))
  native=json.loads((ROOT/'_ART_SOURCES/smooth_motion_1009/reference/ship-rigs.json').read_text());pilots=[k for k in native if k!='furyship'];sheet=Image.new('RGBA',(3*300,3*300),(15,22,32,255));g=ImageDraw.Draw(sheet)
  for j,pk in enumerate(pilots):
   samples=[]
   for f in range(8):
    meta=p.evaluate('({pk,f})=>{run.pilot=pk;state=GS.PLAY;player._bank=0;SM10.clock=(f+.01)/12;const im=XART.get("ship_"+pk);ctx.setTransform(SS,0,0,SS,0,0);ctx.clearRect(0,0,cv.width,cv.height);drawShipSprite(240,220,160,"");return {w:im.width,h:im.height,key:_shipFrameKey(pk),thr:SHIP_THR[pk].nf};}',{'pk':pk,'f':f});samples.append(p.evaluate('()=>cv.toDataURL()'))
    if f==3:im=image_of(p)
   check(pk+' eight native ship frames retain original canvas/nozzle rig',len(set(samples))==8 and meta['w']==native[pk]['w'] and meta['h']==native[pk]['h'] and meta['thr']==native[pk]['thr'] and meta['key']=='ship_'+pk,meta)
   thumb=im.crop(inkbox(im));thumb.thumbnail((260,250),Image.Resampling.NEAREST);sheet.alpha_composite(thumb,((j%3)*300+(300-thumb.width)//2,(j//3)*300+25));g.text(((j%3)*300+9,(j//3)*300+7),pk,fill='#dde9ff')
  sheet.save(OUT/'pilot-native-contact.png')
  fury=Image.new('RGBA',(3*300,3*300),(15,22,32,255));g=ImageDraw.Draw(fury);colors=[]
  for j,pk in enumerate(pilots):
   samples=[]
   for f in range(8):
    size=p.evaluate('({pk,f})=>{SM10.clock=(f+.01)/12;ctx.clearRect(0,0,cv.width,cv.height);furyShipBlit("base",240,220,180,180,pk);const im=furyShipCanvas("base",pk);return [im.width,im.height];}',{'pk':pk,'f':f});samples.append(p.evaluate('()=>cv.toDataURL()'))
    if f==3:im=image_of(p);colors.append(samples[-1])
   check(pk+' Furyship eight frames retain current 128px hull',len(set(samples))==8 and size==[128,128])
   thumb=im.crop(inkbox(im));thumb.thumbnail((260,250),Image.Resampling.NEAREST);fury.alpha_composite(thumb,((j%3)*300+(300-thumb.width)//2,(j//3)*300+25));g.text(((j%3)*300+9,(j//3)*300+7),pk,fill='#dde9ff')
  check('Furyship pilot hull palettes stay distinct',len(set(colors))==9);fury.save(OUT/'fury-native-contact.png')
  p.evaluate('()=>{beginStage(6);setState(GS.PLAY);story=null;fb2Talk=null;BOFCinematicDirector.cancel();enemies=[];boss=null;subBoss=null;stagePlan=[];player.invuln=1e9;window.STORM=[];for(const type of ["s6lancer","s6cyclone","s6skimmer","s6dart","s6thunder"]){spawnEnemy(type,100+STORM.length*60,110);const e=enemies.at(-1);e.spin=Math.PI;STORM.push(e);}}')
  p.evaluate(shoot.STEP,60);p.wait_for_timeout(20)
  check('Southbound Stage 6 hulls animate with stale north spin',p.evaluate('()=>STORM.every(e=>Number.isFinite(e._sm10Frame))'))
  (OUT/'stage6-motion-native.png').write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')))
  # Record real update/draw loops, not a slideshow of generated source sheets.
  width,height=p.evaluate('[cv.width,cv.height]');writer=imageio_ffmpeg.write_frames(str(OUT/'stage6-flight.mp4'),(width,height),fps=15,codec='libx264',quality=7,macro_block_size=1);writer.send(None)
  for _ in range(90):
   p.evaluate(shoot.STEP,4);p.wait_for_timeout(5);writer.send(np.array(image_of(p).convert('RGB')))
  writer.close()
  br.close()
finally:stop()
check('No page, console or asset errors',not errors,errors)
result={'passed':sum(q['pass'] for q in checks),'failed':[q for q in checks if not q['pass']],'errors':errors,'checks':checks}
(OUT/'enemy-ship-verification.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps({'passed':result['passed'],'failed':result['failed'],'errors':errors}),flush=True)
if result['failed'] or errors:sys.exit(1)
