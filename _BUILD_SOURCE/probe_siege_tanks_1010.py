"""Verify the isolated art-review page with the game's actual Chromium ctx."""
from pathlib import Path
import sys,json,base64,io,hashlib
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
OUT=ROOT/'_shots/siege_tanks_1010';OUT.mkdir(exist_ok=True)
checks=[];errors=[]
def check(name,ok,data=None):
 checks.append({'name':name,'pass':bool(ok),'data':data});print(('PASS ' if ok else 'FAIL ')+name,flush=True)
def capture(f,name):
 data=base64.b64decode(f.evaluate('()=>cv.toDataURL().split(",")[1]'));(OUT/(name+'.png')).write_bytes(data)
 return np.array(Image.open(io.BytesIO(data)).convert('RGB'))
def step(f,seconds):
 for _ in range(int(seconds*10)):
  f.evaluate('()=>{for(let i=0;i<6;i++)PT10.tick(1/60);ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}')
  f.wait_for_timeout(5)

# Validate delivered files as well as the runtime's metadata. Padding must
# preserve one common canvas/pivot/scale throughout every animation bank.
manifest=json.loads((ROOT/'_ART_SOURCES/siege_tanks_1010/manifest.json').read_text())['banks']
cells=[q for bank in manifest.values() for q in bank]
check('Every delivered frame has even integer dimensions',all(isinstance(q['w'],int) and isinstance(q['h'],int) and q['w']>0 and q['h']>0 and q['w']%2==0 and q['h']%2==0 for q in cells))
check('Actual PNG dimensions match the registered even canvases',all(Image.open(ROOT/q['path']).size==(q['w'],q['h']) for q in cells))
check('Each bank retains a uniform canvas, pivot and proportional scale',all(len({(q['w'],q['h'],*q['pivot'],q['scale']) for q in bank})==1 for bank in manifest.values()))
port,stop=shoot.serve(str(ROOT))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1320,'height':1100});p.set_default_timeout(120000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:600]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append(f'HTTP {r.status} {r.url}') if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/docs/previews/siege_tanks_1010/index.html');f=p.frames[1]
  f.wait_for_function('window.PT10&&PT10.ready()',polling=50);f.evaluate(shoot.TRAP_RAF);f.wait_for_timeout(60)
  check('Preview owns 58 banks / 553 authored cells',f.evaluate('Object.keys(ST10_ART).length===58&&Object.values(ST10_ART).flat().length===553'))
  for unit in (sys.argv[1:] or ['sonic','devastator','deviator']):
   p.locator('[data-unit="'+unit+'"]').click();f.wait_for_function('PT10.ready()',polling=50)
   f.evaluate('()=>{PT10.mode="combat";PT10.auto=false;PT10.t=0;PT10.restore();ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}')
   capture(f,unit+'-idle');check(unit+' eight independent mounted modules',f.evaluate('PT10.rig().length===8&&Object.values(PT10.parts).every(p=>!p.gone)'))
   q=f.evaluate('()=>{ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);PT10.drawTank(VW/2,VH/2);return {width:PT10.specs[PT10.unit].width,k:PT10.scale()};}')
   a=capture(f,unit+'-assembly-pixels');yy,xx=np.where(np.max(a,axis=2)>5);actual=int(xx.max()-xx.min()+1)
   check(unit+' assembled width matches requested scale',abs(actual-q['width'])<=3,{'target':q['width'],'actual':actual,'k':q['k']})
   for suffix,frames in [('hull',16),('track_left',16),('track_right',16),('weapon',16),('charge',16),('projectile',16),('explosion',32),('impact',16)]:
    bank=f.evaluate('(name)=>ST10_ART[name]',unit+'_'+suffix)
    check(unit+' '+suffix+' correct unique frame count',len(bank)==frames and len(set(a['sha256'] for a in bank))==frames)
    hashes=[];pixels=[]
    for i in range(frames):
     hashes.append(f.evaluate('(q)=>{ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);PT10.cell(q.bank,q.f,240,200,.65);return cv.toDataURL();}',{'bank':unit+'_'+suffix,'f':i}))
     if suffix in ['hull','track_left','track_right','weapon']:
      pixels.append(np.array(Image.open(io.BytesIO(base64.b64decode(hashes[-1].split(',')[1]))).convert('RGB')).astype(float))
     if i%8==7:f.wait_for_timeout(5)
    check(unit+' '+suffix+' all native frames visible and distinct',len(set(hashes))==frames)
    if pixels:
     ref=pixels[0];mask=(np.max(ref,axis=2)>50)&(np.ptp(ref,axis=2)<15)
     if unit=='deviator' and suffix!='hull':
      # Bronze guards/gimbals are stationary. Gray links are the deliberately
      # scrolling tread belt and must never be used as registration fixtures.
      mask=(ref[:,:,0]>60)&(ref[:,:,0]>ref[:,:,1]*1.12)&(ref[:,:,1]>ref[:,:,2]*1.20)
     ys,xs=np.indices(mask.shape)
     if suffix.startswith('track'):mask&=(abs(xs-240)>13)&(abs(xs-240)<30)&(abs(ys-200)<38)
     elif suffix=='weapon':mask&=(abs(xs-240)<24)&(abs(ys-200)<22)
     else:mask&=(abs(xs-240)<50)&(abs(ys-200)<50)
     yy,xx=np.where(mask);shifts=[]
     for im in pixels:
      _,dx,dy=min((float(np.mean((ref[yy,xx]-im[yy+dy,xx+dx])**2))+.15*(abs(dx)+abs(dy)),dx,dy) for dy in range(-5,6) for dx in range(-5,6));shifts.append([dx,dy])
     check(unit+' '+suffix+' fixed metal fixture stays registered',len(xx)>30 and max(abs(v) for s in shifts for v in s)<=2,shifts)
   f.evaluate('()=>{PT10.restore();PT10.flash();ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}')
   capture(f,unit+'-white-hit')
   f.evaluate('()=>{ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);PT10.drawTank(240,256);}')
   a=capture(f,unit+'-white-pixels');mask=np.max(a,axis=2)>100
   check(unit+' white hits preserve the complete current silhouette',np.mean(np.ptp(a[mask].astype(int),axis=1)<3)>.98)
   f.evaluate('()=>{PT10.restore();for(const id of Object.keys(PT10.parts)){PT10.hit(id);PT10.hit(id);}PT10.tick(.2);ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}')
   capture(f,unit+'-critical');check(unit+' all critical modules retain separate anchors',f.evaluate('Object.values(PT10.parts).every(p=>p.damage===1&&!p.gone)'))
   f.evaluate('()=>{PT10.restore();PT10.break("weapon");}');step(f,.4);capture(f,unit+'-break')
   check(unit+' main weapon breaks independently without fading',f.evaluate('PT10.parts.weapon.gone&&!PT10.parts.hull.gone&&PT10.debris.length===1&&PT10.debris[0].spin!==0&&!PT10.debris[0].alpha'))
   step(f,.5);check(unit+' detached weapon enters explosion and leaves decal',f.evaluate('PT10.debris.length===0&&PT10.bursts.some(q=>q.bank==="explosion")&&PT10.decals.length>0'))
   f.evaluate('()=>{PT10.restore();PT10.fire(PT10.unit==="sonic");}');step(f,.5);capture(f,unit+'-charge')
   # Observe actual moving shots, then the full native detonation.
   observed=[];charged=None
   for _ in range(26):
    step(f,.1);q=f.evaluate('()=>({shots:PT10.shots.map(s=>({dy:s.y-s.startY,dir:s.dir})),burst:PT10.bursts.some(q=>q.charged)})');observed+=q['shots']
    if q['burst'] and charged is None:
     charged=f.evaluate('()=>({...PT10.bursts.find(q=>q.charged)})');capture(f,unit+'-charged-blast')
   check(unit+' projectiles travel south from anchored muzzle',len(observed)>0 and all(s['dy']>=0 and 0<s['dir']<np.pi for s in observed),observed[:5])
   check(unit+' attack leaves persistent impact decals',f.evaluate('PT10.decals.length>0'))
   if unit=='sonic' and charged:
    peak=f.evaluate('ST10_METRICS.sonic_explosion.peakInk');field=f.evaluate('viewW()*PLAY.h')
    check('Charged sonic authored footprint requests 33% of playfield',abs(peak*charged['k']**2/field-.33)<.001,charged)
    frames=f.evaluate('ST10_ART.sonic_explosion');peakf=f.evaluate('ST10_METRICS.sonic_explosion.peakInkFrame')
    f.evaluate('(q)=>{ctx.setTransform(SS,0,0,SS,0,0);ctx.clearRect(0,0,cv.width,cv.height);ctx.save();ctx.translate(-camX,0);PT10.cell("sonic_explosion",q.i,q.b.x,q.b.y,q.b.k);ctx.restore();}',{'i':peakf,'b':charged})
    a=capture(f,'sonic-blast-footprint');ss=f.evaluate('SS');bounds=f.evaluate('({y:PLAY.y,h:PLAY.h,w:viewW()})');crop=a[round(bounds['y']*ss):round((bounds['y']+bounds['h'])*ss)]
    visible=float(np.sum(np.max(crop,axis=2)>4)/(field*ss*ss))
    check('Charged sonic footprint is fully visible at approximately 33%',abs(visible-.33)<.015,visible)
    f.evaluate('(q)=>{ctx.setTransform(SS,0,0,SS,0,0);PT10.originalDraw(0);ctx.save();ctx.translate(-camX,0);PT10.cell("sonic_explosion",q.i,q.b.x,q.b.y,q.b.k);ctx.restore();}',{'i':peakf,'b':charged});capture(f,'sonic-blast-peak')
   f.evaluate('()=>{PT10.restore();PT10.destroy();}');step(f,.6);capture(f,unit+'-destroy')
   step(f,1.6);check(unit+' entire tank breaks into eight physical pieces then explosions',f.evaluate('Object.values(PT10.parts).every(p=>p.gone)&&PT10.debris.length===0&&PT10.decals.length>=8'))
   f.evaluate('()=>{PT10.restore();PT10.mode="scale";drawWorld(0);}')
   f.wait_for_timeout(200);capture(f,unit+'-size-comparison')
   f.evaluate('()=>{PT10.mode="effects";PT10.t=.4;drawWorld(0);}')
   capture(f,unit+'-effect-reels')
   f.evaluate('()=>{PT10.mode="damage";drawWorld(0);}')
   capture(f,unit+'-damage-plates')
  p.locator('[data-unit="sonic"]').click();f.wait_for_function('PT10.ready()',polling=50);f.evaluate('()=>{PT10.mode="combat";PT10.auto=false;PT10.restore();drawWorld(0);}')
  p.screenshot(path=str(OUT/'preview-desktop.png'));p.set_viewport_size({'width':600,'height':1000});p.screenshot(path=str(OUT/'preview-narrow.png'))
  check('Preview has no horizontal overflow at 600 px',p.evaluate('document.documentElement.scrollWidth<=innerWidth'))
  production='\n'.join((ROOT/q).read_text(encoding='utf-8') for q in ['index.html','assets/siege_tanks_art_1010.js','assets/siege_tanks_1010.js'])
  check('Production imports shipping art without preview code or source paths',all(q not in production for q in ['_ART_SOURCES/','preview_runtime.js','ST10_ART','PT10.']))
  br.close()
finally:stop()
check('No page, console or asset errors',not errors,errors)
result={'passed':sum(q['pass'] for q in checks),'failed':[q for q in checks if not q['pass']],'checks':checks,'errors':errors}
(OUT/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'passed':result['passed'],'failed':result['failed'],'errors':errors}),flush=True)
if result['failed'] or errors:sys.exit(1)
