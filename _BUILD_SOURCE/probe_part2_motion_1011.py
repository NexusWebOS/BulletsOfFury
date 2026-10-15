"""Native pixels and existing live controllers for the October11 motion pass."""
from pathlib import Path
from PIL import Image,ImageDraw
import base64,io,json,sys
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
OUT=ROOT/'_shots/part2_motion_1011';OUT.mkdir(parents=True,exist_ok=True)
checks=[];errors=[];port,stop=shoot.serve(str(ROOT))
def check(name,value,data=None):
 checks.append(dict(name=name,passed=bool(value),data=data));print(('PASS ' if value else 'FAIL ')+name,flush=True)
def image_from_canvas(p):
 data=p.evaluate('ctx.canvas.toDataURL("image/png")').split(',',1)[1]
 return Image.open(io.BytesIO(base64.b64decode(data))).convert('RGB')
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport=dict(width=1600,height=900));p.set_default_timeout(120000)
  p.on('pageerror',lambda e:errors.append(str(e)))
  p.on('console',lambda m:errors.append(m.text) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append('HTTP '+str(r.status)+': '+r.url) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>3');p.evaluate(shoot.TRAP_RAF)
  def frames(n):
   for i in range(0,n,12):
    err=p.evaluate(shoot.STEP,min(12,n-i))
    if err:errors.append(err)
    p.wait_for_timeout(4)
  def scene(n,pk='maverick'):
   p.evaluate('()=>{P2M.active=P2M.pending=P2M.choice=null;run.mode="arcade";coopOn=false;GP4.route=null;delete run._gp4StageX;}')
   p.evaluate(shoot.SETUP,dict(state='PLAY',stage=n,pilot=pk,invuln=True))
   p.wait_for_function('n=>{stageLoadTick();return stageLoadInfo(n).ready}',arg=n,polling=50)
   p.evaluate('()=>{BOFCinematicDirector.cancel();story=null;fb2Talk=null;s6Opening=null;H3.ending=null;H3.release=false;stagePlan=[];enemies=[];powerups=[];pBullets=[];eBullets=[];boss=subBoss=null;bossActive=subBossActive=false;subBossDone=true;player.invuln=1e9;player._spawnClearT=1e9;special=null;atomBooms=[];s67Nukes=[];atomFlash=0;run.forge={};run.forgeForms={};run.infusion=null;run._spaceShadowHeld=false;}')
  scene(6)
  p.wait_for_function('()=>Object.values(P2_ART).flat().map(a=>XART.rdy(a.key)).every(Boolean)',polling=50)
  for motion in ['roll','somer']:
   for role in ['blue','red','green','orange']:
    pictures=[];stats=[]
    for i in range(16):
     q=p.evaluate('''q=>{const a=P2MC.views.get(q.role+'|'+q.motion+'|'+q.i);ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,256,256);ctx.drawImage(XART.get(a.key),0,0);const d=ctx.getImageData(0,0,256,256).data;let pixels=0,edge=0,l=256,t=256,r=0,b=0;for(let y=0;y<256;y++)for(let x=0;x<256;x++){const off=(y*256+x)*4;if(d[off]+d[off+1]+d[off+2]>24){pixels++;l=Math.min(l,x);t=Math.min(t,y);r=Math.max(r,x);b=Math.max(b,y);if(x<2||y<2||x>=254||y>=254)edge++;}}ctx.restore();return {key:a.key,pixels,edge,bounds:[l,t,r,b],pivot:a.pivot};}''',dict(role=role,motion=motion,i=i))
     stats.append(q);pictures.append(image_from_canvas(p).crop((0,0,256,256)))
     if i%4==3:p.wait_for_timeout(4)
    contact=Image.new('RGB',(1024,1120),(9,15,23));labels=ImageDraw.Draw(contact)
    for i,im in enumerate(pictures):contact.paste(im,((i%4)*256,(i//4)*280));labels.text(((i%4)*256+8,(i//4)*280+260),stats[i]['key'],fill='white')
    contact.save(OUT/(role+'-'+motion+'-native.png'))
    pictures[0].save(OUT/(role+'-'+motion+'-native.gif'),save_all=True,append_images=pictures[1:],duration=80,loop=0)
    check(role+' '+motion+': all16 actual plates render through the game context, unclipped at a fixed physical pivot',len({q['key'] for q in stats})==16 and all(q['pixels']>500 and q['edge']==0 and q['pivot']==[128,128] for q in stats),stats)
  q=p.evaluate('''()=>{const out=[];for(const role of ['blue','red','green','orange'])for(const motion of ['roll','somer'])for(let i=0;i<16;i++){
   const e={type:'s6lancer',x:220,y:240,hp:100,maxhp:100,_fb2Stealth:{role,direction:'south',[motion]:{t:i/16*(motion==='roll'?.46:.62),dur:motion==='roll'?.46:.62,dir:1}}};ap10StealthDraw(e);out.push({role,motion,i,key:e._p2StealthKey});}return out;}''')
  bad=[x for x in q if x['key']!=f"p2_stealth_{x['motion']}_{x['role']}_{x['i']:02d}"]
  check('Live Stage6 fighter renderer selects all128 correct role/move views without a shape transform',len(q)==128 and not bad,bad)
  p.evaluate('()=>{GP4.route="left";GP4.routeReady=true;GP4.stage6Only=true;gp4QuickEncounter();story=null;boss.enter=false;whvAceSpawn(boss);boss._whv.mode="ace";const A=boss._whv.ace;A.st="fight";A.x=worldWidth()/2;A.y=VH*.35;A.vx=A.vy=0;A.rollCd=A.somerCd=A.dashCd=999;A.desp=null;A.inverted=false;A.somer=null;A.roll={t:0,x0:A.x,dir:1};}')
  roll=[]
  for i in range(12):
   frames(2);roll.append(p.evaluate('boss._whv.ace._p2MotionKey'))
  p.screenshot(path=str(OUT/'elite-live-roll.png'))
  check('Harrier elite controller actually advances the new rigid roll views during its existing dodge',len(set(roll))>=10 and all(x and 'stealth_roll_blue' in x for x in roll),roll)
  p.evaluate('()=>{const A=boss._whv.ace;A.roll=null;A.somer={t:0,y0:A.y};}')
  somer=[]
  for i in range(16):
   frames(2);somer.append(p.evaluate('boss._whv.ace._p2MotionKey'))
  p.screenshot(path=str(OUT/'elite-live-somersault.png'))
  check('Harrier elite controller advances the new front/rear/belly somersault views',len(set(somer))>=12 and all(x and 'stealth_somer_blue' in x for x in somer),somer)
  q=p.evaluate('''()=>{const A=boss._whv.ace;A.roll=A.somer=null;A.inverted=false;A.vx=200;whvDrawAce(boss);const bank=A._p2MotionKey;A.inverted=true;A.vx=0;whvDrawAce(boss);return {bank,inverted:A._p2MotionKey};}''')
  check('Elite fast banking and inverted posture also avoid the old warped bank plates',q['bank']=='p2_stealth_roll_blue_01' and q['inverted']=='p2_stealth_roll_blue_08',q)
  scene(6)
  p.evaluate('()=>{s6OpeningInit();const O=s6Opening;O.phase="flyover";O.t=3.1;O.allT=30;O.carrierJets=[{x:worldWidth()/2-70,y:VH*.45,age:.45,side:-1},{x:worldWidth()/2+70,y:VH*.45,age:.68,side:1}];drawWorld(0);}')
  q=p.evaluate('s6Opening.carrierJets.map(j=>j._p2MotionKey)');p.screenshot(path=str(OUT/'carrier-live-rolls.png'))
  check('Both carrier-launched fighters use drawn rotational views in the actual opening cinematic',len(q)==2 and all('stealth_roll_blue' in x for x in q),q)
  scene(2)
  p.evaluate('()=>{special={pilot:"maverick",t:8,dur:15,mavCharging:true,mavCharge:MAV_FULL*.55};drawWorld(0);}')
  q=p.evaluate('P2MC.draws.maverick||0');p.screenshot(path=str(OUT/'maverick-live-green-charge.png'))
  check('Maverick forms the new green sphere in the actual player charge draw',q>0,q)
  p.evaluate('()=>{special.mavCharge=MAV_FULL;drawWorld(0);releaseHelix(MAV_FULL);special.mavCharging=false;}');frames(4)
  q=p.evaluate('()=>({rounds:pBullets.filter(q=>q.kind==="venomx"&&q._isBall).map(q=>({full:q._full,y:q.y,air:q._air})),draws:P2MC.draws.maverick})');p.screenshot(path=str(OUT/'maverick-live-overdrive-flight.png'))
  check('Full-charge release travels as the animated purple/blue sphere, retaining the real helix projectile',bool(q['rounds']) and all(x['full'] for x in q['rounds']) and q['draws']>4,q)
  q=p.evaluate('''()=>{const read=XART.get,draw=ctx.drawImage,seen=[];let key;try{XART.get=function(k){key=k;return read.apply(this,arguments);};ctx.drawImage=function(im,...args){seen.push({key,args});return draw.call(this,im,...args);};for(let i=0;i<32;i++)drawHelixLance(200,220,100,true,i,1,1,true);return seen;}finally{XART.get=read;ctx.drawImage=draw;}}''')
  check('Travelling helix ball displays every one of the32 overdrive poses at a constant registered size',len(q)==32 and len({x['key'] for x in q})==32 and all(x['key'].startswith('p2_maverick_full_') and x['args']==q[0]['args'] for x in q),q[:2])
  p.evaluate('()=>{special=null;boss=subBoss=null;bossActive=subBossActive=false;atomBooms=[];s67Nukes=[];atomFlash=0;ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,ctx.canvas.width,ctx.canvas.height);av3Beam(ctx,220,480,-Math.PI/2,400,104,"fire",.2);ctx.restore();}')
  q=p.evaluate('()=>({root:P2.draws.fireRoot,tip:P2.draws.fireTip,beam:P2.draws.fireBeam})');p.screenshot(path=str(OUT/'complete-fire-native.png'))
  check('Actual fire renderer draws the flowing core connection and new organic terminal crown together',all((q.get(k) or 0)>0 for k in ['root','tip','beam']),q)
  scene(2,'lizzie');p.evaluate('()=>{atomBlast(worldWidth()/2,VH*.8);atomFlash=0;}')
  atomic=[]
  for i in range(32):
   p.evaluate('i=>{atomBooms[0].t=(i+.5)/32*atomBooms[0].dur;drawWorld(0);}',i)
   atomic.append(image_from_canvas(p));p.wait_for_timeout(3)
  atomic[0].save(OUT/'atomic-live.gif',save_all=True,append_images=atomic[1:],duration=60,loop=0)
  atomic[14].save(OUT/'atomic-live-peak.png')
  check('Actual atomic strike renders all32 progressively expanding and dispersing poses',p.evaluate('(P2.draws.atom||0)>=32'))
  # Compare palettes with the source through the GAME canvas, never .src or identity.
  q=p.evaluate('''()=>{const read=(key,pad,bg)=>{ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.fillStyle=bg;ctx.fillRect(0,0,288,288);ctx.drawImage(XART.get(key),pad,pad);const p=ctx.getImageData(0,0,288,288).data.slice();ctx.restore();return p;};let diff=0,bounds=0;for(let n=0;n<32;n++){const a=read(P2_ART.jace[n].key,16,'#000'),b=read(P2_ART.maverick[n].key,0,'#000'),c=read(P2_ART.maverick_full[n].key,0,'#000'),aw=read(P2_ART.jace[n].key,16,'#fff'),bw=read(P2_ART.maverick[n].key,0,'#fff'),cw=read(P2_ART.maverick_full[n].key,0,'#fff');for(let i=0;i<a.length;i+=4){const ya=.2126*a[i]+.7152*a[i+1]+.0722*a[i+2],yb=.2126*b[i]+.7152*b[i+1]+.0722*b[i+2],yc=.2126*c[i]+.7152*c[i+1]+.0722*c[i+2];if(Math.max(Math.abs(ya-yb),Math.abs(ya-yc))>1.8)diff++;const aa=255-(aw[i]+aw[i+1]+aw[i+2]-a[i]-a[i+1]-a[i+2])/3,ba=255-(bw[i]+bw[i+1]+bw[i+2]-b[i]-b[i+1]-b[i+2])/3,ca=255-(cw[i]+cw[i+1]+cw[i+2]-c[i]-c[i+1]-c[i+2])/3;if(Math.max(Math.abs(aa-ba),Math.abs(aa-ca))>1.5)bounds++;}}return {luminanceOutliers:diff,alphaOutliers:bounds};}''')
  check('Both Maverick palettes retain Jace sphere luminance and physical coverage in native pixels',q['luminanceOutliers']==0 and q['alphaOutliers']==0,q)
  check('No page, console, renderer or missing-asset errors',not errors,errors);br.close()
except Exception as e:
 errors.append(type(e).__name__+': '+str(e));print(errors[-1],flush=True)
finally:
 stop();report=dict(passed=sum(q['passed'] for q in checks),failed=sum(not q['passed'] for q in checks),checks=checks,errors=errors)
 (OUT/'report.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(dict(passed=report['passed'],failed=report['failed'],errors=errors)),flush=True)
sys.exit(1 if errors or report['failed'] else 0)
