"""Verify every new cell and actual jet/virus cinematics in native Chromium."""
from pathlib import Path
import sys,json,base64,hashlib
import numpy as np
from PIL import Image,ImageDraw
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
OUT=ROOT/'_shots/homecoming_takeover_1010';OUT.mkdir(parents=True,exist_ok=True)
PILOTS=['cole','axel','freezer','yuri','maverick','falva','lizzie','decker','juggernaut']
checks=[];errors=[];states=[]
def check(name,value,data=None):
 checks.append(dict(name=name,passed=bool(value),data=data));print(('PASS ' if value else 'FAIL ')+name,flush=True)
 if not value:print(json.dumps(data),flush=True)
port,stop=shoot.serve(str(ROOT))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport=dict(width=1280,height=900));p.set_default_timeout(120000)
  p.on('pageerror',lambda e:errors.append(str(e)))
  p.on('console',lambda m:errors.append(m.text[:1000]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append('HTTP '+str(r.status)+': '+r.url) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
  p.evaluate("()=>{Object.defineProperty(navigator,'getGamepads',{configurable:true,value:()=>[]});BOFCinematicDirector.cancel();run.mode='campaign';run.pilot='cole';story=null;fb2Talk=null;s6Opening=null;drawVictory._t=0;drawVictory._ready=false;drawVictory._wait=0;drawVictory._waitF=0;drawVictory._sfx={};drawVictory._trueEnding=true;setState(GS.VICTORY);victoryEndingWarm();for(const a of Object.values(HC10_ART).flat())XART.rdy(a.key);}")
  p.wait_for_function('victoryEndingReady()&&sv10Warm()&&hl10Warm()&&Object.values(HC10_ART).flat().every(a=>XART.rdy(a.key))',polling=50)
  p.evaluate(shoot.STEP,2);check('Ending loads all selected-jet and takeover dependencies before its clock advances',p.evaluate('drawVictory._ready&&drawVictory._t<.1&&sv10Warm()'))
  registry=p.evaluate('HC10_ART');check('Archived generated aircraft and active infection/environment art remain preserved',sum(len(v) for v in registry.values())==467)
  captures=p.evaluate('''async()=>{const size={w:cv.width,h:cv.height},out=[];
   try{ctx.setTransform(1,0,0,1,0,0);
    for(const [bank,cells] of Object.entries(HC10_ART))if(cells.length>1)for(let f=0;f<cells.length;f++){
     const a=cells[f];cv.width=a.w;cv.height=a.h;ctx.setTransform(1,0,0,1,0,0);
     ctx.clearRect(0,0,a.w,a.h);hc10Cell(bank,f,a.pivot[0],a.pivot[1],a.w);
     out.push({bank,frame:f,png:cv.toDataURL()});if(f%8===7)await new Promise(r=>setTimeout(r,0));}
    return out;
   }finally{cv.width=size.w;cv.height=size.h;ctx.setTransform(SS,0,0,SS,0,0);}}''')
  native=OUT/'native';native.mkdir(exist_ok=True);mismatches=[];unique={};wingFixtures={}
  for q in captures:
   f=native/(q['bank']+'_'+str(q['frame']).zfill(2)+'.png');f.write_bytes(base64.b64decode(q['png'].split(',')[1]))
   pixels=np.array(Image.open(f).convert('RGBA'));a=registry[q['bank']][q['frame']];source=np.array(Image.open(ROOT/a['path']).convert('RGBA'))
   mask=source[:,:,3]>=160;expected=source[:,:,:3].astype(float)*source[:,:,3:4]/255
   delta=np.abs(pixels[:,:,:3].astype(float)-expected);bad=int((delta[mask]>1.01).any(axis=1).sum());mismatches.append(dict(bank=q['bank'],frame=q['frame'],bad=bad))
   unique.setdefault(q['bank'],set()).add(hashlib.sha256(pixels.tobytes()).hexdigest())
   if q['bank'].endswith('_landing'):
    solid=pixels[:,:,:3].max(axis=2)>48;spans=[]
    for y in range(len(solid)):
     xs=np.flatnonzero(solid[y])
     if len(xs):spans.append((int(xs[-1]-xs[0]),y,int(xs[0]),int(xs[-1])))
    widest=max(v[0] for v in spans);tips=[v for v in spans if v[0]>=widest-3]
    wingFixtures.setdefault(q['bank'],[]).append(dict(frame=q['frame'],x=float(np.median([(v[2]+v[3])/2 for v in tips])),y=float(np.median([v[1] for v in tips]))))
  check('Every visible pixel in all 464 sprite cells matches the native game composite',all(q['bad']==0 for q in mismatches),mismatches if any(q['bad'] for q in mismatches) else None)
  check('All flight, landing and infection reels contain distinct native rendered frames',all(len(v)==len(registry[k]) for k,v in unique.items()),{k:len(v) for k,v in unique.items()})
  check('Every delivered frame is even, fixed-size, fixed-pivot and keeps its complete silhouette',all(a['w']==a['h'] and a['w'] in [384,448] and a['pivot']==[a['w']//2,a['h']//2] and min(a['opaque_bounds'][:2])>0 and max(a['opaque_bounds'][2:])<a['w'] for bank in registry.values() if len(bank)>1 for a in bank))
  check('Native wing fixtures remain anchored while every canopy, gear and boarding step moves',all(abs(f['x']-224)<=2 and abs(f['y']-224)<=2 for frames in wingFixtures.values() for f in frames),wingFixtures)
  # Film contact sheets are made from the real game context, not a replacement renderer.
  for bank in [pk+'_'+side for pk in PILOTS for side in ['front','rear','landing']]+['infection']:
   frames=sorted(native.glob(bank+'_*.png'));sheet=Image.new('RGB',(8*192,((len(frames)+7)//8)*208),(0,0,0));d=ImageDraw.Draw(sheet)
   for i,f in enumerate(frames):
    im=Image.open(f).convert('RGB').resize((192,192),Image.Resampling.NEAREST);sheet.paste(im,((i%8)*192,(i//8)*208));d.text(((i%8)*192+4,(i//8)*208+192),str(i),fill='#fff')
   sheet.save(OUT/(bank+'-native-sheet.png'))
  p.evaluate('()=>{window.__hc10FuryCalls=0;window.__hc10OldFury=furyShipDrawFlight;furyShipDrawFlight=function(){__hc10FuryCalls++;return __hc10OldFury.apply(this,arguments);};HC10.draws={};}')
  def seek(t,name=None):
   p.evaluate("t=>{drawVictory._t=t;ctx.setTransform(SS,0,0,SS,0,0);drawVictory(0);}",t)
   if name:p.screenshot(path=str(OUT/(name+'.png')))
   return p.evaluate('drawVictory._t<VICTORY_DISH_AT?HL10.last:SV10.last')
  pilots=[]
  for pk in PILOTS:
   p.evaluate("pk=>{run.pilot=pk;hl10Warm(pk);}",pk);p.wait_for_function('hl10Warm()',polling=50)
   a=seek(1.2,pk+'-portal');b=seek(4.2,pk+'-earth');c=seek(5.95);d=seek(7.8,pk+'-coast')
   land=seek(11.2,pk+'-landing');exit=seek(14.8,pk+'-exit');walk=seek(18.8,pk+'-walk')
   pilots.append(dict(pilot=pk,portal=a['flight'],earth=b['flight'],descent=c['flight'],coast=d['flight'],landing=land['ship'],exit=exit['actor'],walk=walk['actor']))
  check('All nine selected pilots render the original straight front/rear ship images for every flight shot',all(q['portal']['bank']=='ship_'+q['pilot']+'_so6' and q['earth']['bank']==q['coast']['bank']=='ship_'+q['pilot']+'_so2' for q in pilots),pilots)
  check('Actual Earth shots travel down a constant centreline and shrink to the planet',all(q['earth']['jet']['x']==q['descent']['jet']['x'] and q['earth']['jet']['y']<q['descent']['jet']['y'] and q['earth']['jet']['width']>q['descent']['jet']['width'] and q['earth']['rotation']==q['descent']['rotation']==0 for q in pilots))
  check('Every pilot lands the same original static rear view and disembarks into the existing physical HQ route',all(q['landing']['bank']=='ship_'+q['pilot']+'_so2' and q['exit'] and q['walk'] for q in pilots))
  native_static=p.evaluate('''async()=>{const size={w:cv.width,h:cv.height},out=[];
   try{cv.width=cv.height=384;
    for(const pk of HC10.pilots)for(const view of ['front','rear']){
     const key='ship_'+pk+'_so'+(view==='front'?6:2),a=BOFX.ships[key];
     ctx.setTransform(1,0,0,1,0,0);ctx.imageSmoothingEnabled=false;ctx.clearRect(0,0,384,384);
     ctx.drawImage(XART.get(key),a[4],a[5],a[2],a[3],192-a[2]/2,192-a[3]/2,a[2],a[3]);
     const expected=ctx.getImageData(0,0,384,384).data;
     ctx.clearRect(0,0,384,384);hc10StaticShip(pk,view,192,192,a[2]);
     const actual=ctx.getImageData(0,0,384,384).data;let changed=0;
     for(let i=0;i<actual.length;i++)if(actual[i]!==expected[i])changed++;
     out.push({pilot:pk,view,key,changed,png:cv.toDataURL()});await new Promise(r=>setTimeout(r,0));}
    return out;
   }finally{cv.width=size.w;cv.height=size.h;ctx.setTransform(SS,0,0,SS,0,0);}}''')
  for q in native_static:
   (native/(q['key']+'-static.png')).write_bytes(base64.b64decode(q.pop('png').split(',')[1]))
  check('All eighteen active static views are pixel-identical to the original in-game ship images',all(q['changed']==0 for q in native_static),native_static)
  check('Homecoming dependency lists exclude every rejected generated aircraft reel',p.evaluate("HC10.pilots.every(pk=>!hl10Assets(pk).some(a=>/^hc10_.*_(front|rear|landing)_/.test(a.key)))"))
  seam=[]
  for pk in PILOTS:
   p.evaluate('pk=>{run.pilot=pk;hl10Warm(pk);}',pk);p.wait_for_function('hl10Warm()',polling=50)
   a=seek(9.39999);b=seek(9.4)
   seam.append(dict(pilot=pk,dx=abs(a['flight']['jet']['x']-b['ship']['x']),dy=abs(a['flight']['jet']['y']-b['ship']['y']),widthDelta=abs(a['flight']['jet']['width']-p.evaluate("HL10.last.ship.scale*hc10ShipGeometry(run.pilot,'rear').w"))))
  check('Approach and landing share one continuous static image, position and size',all(q['dx']<.001 and q['dy']<.001 and q['widthDelta']<.001 for q in seam),seam)
  check('Fury spaceship flight renderer is never used in any of the new jet shots',p.evaluate('__hc10FuryCalls===0'))
  seen=set();flight=set();p.evaluate("run.pilot='cole';")
  for i in range(180):
   s=seek(i/60)
   if s['flight']['portal'] and s['flight']['portal']['visible']:seen.add(s['flight']['portal']['frame'])
   flight.add(s['flight']['frame'])
   if i%30==0:p.wait_for_timeout(3)
  check('Real portal exit uses every opening, swirling and closing frame from the gameplay gate',seen==set(range(32)),sorted(seen))
  check('Aircraft stay on their exact original static image while the portal animates',flight=={0})
  seen=set();effects=set();codeCounts=[];p.evaluate('SV10.events=[];drawVictory._sfx={};')
  for i in range(984):
   s=seek(26.4+i/60)
   if s['bank']=='infection':seen.add(s['frame'])
   if 'effectFrame' in s:effects.add(s['effectFrame'])
   if i%30==0:p.wait_for_timeout(3);codeCounts.append(len(s['codeLines']))
  check('Continuous takeover shows all thirty-two growing infection poses and sixteen contact effects',seen==set(range(32)) and effects==set(range(16)),dict(growth=sorted(seen),effects=sorted(effects)))
  cues=p.evaluate("SV10.events.filter(e=>e.cue!=='code')")
  check('Infection, corruption and transmission each sound once, followed by live code beeps',len(cues)==3 and all(q['available'] and q['played'] for q in cues) and p.evaluate("SV10.events.filter(e=>e.cue==='code').length>=20"),cues)
  for q,name in [(1,'wide'),(2.6,'close'),(3.6,'roots'),(5.6,'infection'),(7,'corruption'),(10,'virus'),(13.5,'transmission'),(16.3,'fade')]:
   states.append(seek(26.4+q,name))
  check('Binary and code spread from zero lines to the whole cinematic',codeCounts[0]==0 and max(codeCounts)>100 and states[-3]['corruption']==1,codeCounts)
  check('Requested binary sequence is visibly rendered, not just stored in dialogue',any(L['text']=='10001001000' for L in states[-3]['codeLines']))
  code=p.evaluate('''()=>{const W=cutsceneViewWidth(),H=VH;ctx.setTransform(SS,0,0,SS,0,0);ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
   sv10CodeDraw(10,W,H);const started=performance.now();for(let i=0;i<12;i++)sv10CodeDraw(10+i/60,W,H);
   return {png:cv.toDataURL(),glyphs:Object.keys(SV10.codeGlyphs).length,ms:(performance.now()-started)/12};}''')
  f=OUT/'code-only.png';f.write_bytes(base64.b64decode(code.pop('png').split(',')[1]));ar=np.asarray(Image.open(f).convert('RGB')).astype(float)
  visible=ar.max(axis=2)>80;green=(ar[:,:,1]>ar[:,:,0]*1.35)&(ar[:,:,1]>ar[:,:,2]*1.35)&visible
  check('Live code preserves the authored font shapes with a readable green palette',green.sum()>visible.sum()*.75,dict(green=int(green.sum()),visible=int(visible.sum()),**code))
  check('Cached code glyphs keep the screen-wide takeover within a thirty-fps rendering budget',code['glyphs']>10 and code['ms']<33.3,code)
  seek(43.2,'command');check('Fury Command follows the complete satellite takeover',p.evaluate('drawVictory._t===43.2&&VICTORY_WARNING_AT===42.8'))
  # Landing, physical doorway and regular/Arcade branches are shared with the prior owner.
  a=seek(11.2,'landing');b=seek(23,'doorway');check('Existing gear touchdown, camera push and doorway entry continue correctly',a['grounded'] and b['actor']['inside'] and b['doorFrame']==15 and b['camera']['zoom']>2.7)
  p.set_viewport_size(dict(width=480,height=900));p.wait_for_timeout(100);seek(4.2,'narrow-earth');seek(36.4,'narrow-virus')
  dims=p.evaluate('()=>{const r=cv.getBoundingClientRect();return{x:r.width/cutsceneViewWidth(),y:r.height/VH};}')
  check('Narrow cinematic remains evenly proportioned',abs(dims['x']/dims['y']-1)<.005,dims)
  p.evaluate("()=>{run.mode='campaign';drawVictory._trueEnding=false;drawVictory._t=26.5;drawVictory(0);}");check('Ordinary campaign still skips the sequel stinger',p.evaluate('drawVictory._t===VICTORY_CARD_AT'))
  p.evaluate("()=>{run.mode='arcade';drawVictory._t=.8;drawVictory(0);}");check('Arcade keeps its direct score card',p.evaluate('drawVictory._t===.8'))
  check('No page, console or asset errors',not errors,errors);br.close()
finally:stop()
report=dict(passed=sum(q['passed'] for q in checks),failed=sum(not q['passed'] for q in checks),checks=checks,errors=errors,states=states)
(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(dict(passed=report['passed'],failed=report['failed'],errors=errors)),flush=True)
sys.exit(1 if report['failed'] else 0)
