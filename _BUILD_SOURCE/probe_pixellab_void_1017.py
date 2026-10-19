"""Native Chromium: portal lifecycles/pivots/seams and all three arena phases."""
from pathlib import Path
import argparse,base64,hashlib,io,json,sys
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright
import shoot
ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path,default=ROOT/'_shots/pixellab_void_1017/native');args=parser.parse_args();OUT=args.out;OUT.mkdir(parents=True,exist_ok=True)
checks=[];errors=[];measure={}
def check(name,ok,data=None):
 checks.append({'name':name,'passed':bool(ok),'data':data});print(('PASS ' if ok else 'FAIL ')+name+((' '+json.dumps(data)) if not ok else ''),flush=True)
def decode(data):return np.asarray(Image.open(io.BytesIO(base64.b64decode(data.split(',')[1]))).convert('RGB')).astype(float)
port,stop=shoot.serve(str(ROOT))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=br.new_page(viewport={'width':1440,'height':1000});p.set_default_timeout(180000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:750]) if m.type=='error' or 'draw error' in m.text else None);p.on('response',lambda r:errors.append(str(r.status)+' '+r.url) if r.status>=400 else None)
  index=(ROOT/'index.html').read_bytes()
  if b'assets/pixellab_void_1017.js' not in index:
   tag=b'<script src="assets/wind_refit_1017.js?v=assault-1017"></script>'
   needle=tag+(b'\r\n' if tag+b'\r\n' in index else b'\n')
   addition=b'<script src="assets/pixellab_void_art_1017.js?v=pixellab-1017"></script>\n<script src="assets/pixellab_void_1017.js?v=pixellab-1017"></script>\n'
   assert index.count(needle)==1
   index=index.replace(needle,needle+addition)
   (OUT/'candidate-index.html').write_bytes(index)
   p.route('**/index.html*',lambda route:route.fulfill(body=index,content_type='text/html'))
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4&&typeof VOID17!=="undefined"');p.evaluate(shoot.TRAP_RAF)
  p.evaluate('()=>{v17Warm(8);}');p.wait_for_function('()=>v17Keys(8).map(k=>XART.rdy(k)).every(Boolean)')
  check('Every new portal, arena and code asset decodes through native XART',True)
  p.evaluate('''()=>{window.px17Keys=new Set();const get=XART.get;XART.get=function(k){if(k.startsWith('pxv17_'))px17Keys.add(k);return get.apply(this,arguments);};
   window.px17Render=(bank,phase,t,options={})=>{ctx.setTransform(SS,0,0,SS,0,0);ctx.globalAlpha=1;ctx.globalCompositeOperation='source-over';ctx.fillStyle='#101c27';ctx.fillRect(0,0,VW,VH);const pose=PL11.sample(bank,phase,t,options);PL11.draw(ctx,pose,VW/2,VH/2,360,k=>XART.get(k));return cv.toDataURL();};}''')
  for bank in ['blue_rift','red_rift','green_rift','black_void']:
   row=p.evaluate('''b=>{const a=PL11_ART[b],f=['form','loop','close'].flatMap(ph=>a[ph].frames);return{count:f.length,geometry:f.every(q=>q.w===320&&q.h===320&&q.pivot[0]===160&&q.pivot[1]===160),stages:['form','loop','close'].map(ph=>a[ph].frames.length)};}''',bank)
   check(bank+' uses three 16–32-pose even banks with one fixed pivot',all(16<=n<=32 for n in row['stages']) and row['geometry'],row)
   for phase in ['form','loop','close']:
    frames=[]
    n=p.evaluate('([b,ph])=>PL11_ART[b][ph].frames.length',[bank,phase])
    for i in range(n):
     raw=decode(p.evaluate('([b,ph,i,n])=>px17Render(b,ph,ph==="loop"?i/(n/1.6):i/(n-1)*1.6,{duration:1.6,blend:false})',[bank,phase,i,n]))
     frames.append(hashlib.sha256(raw.tobytes()).hexdigest())
     if i%8==7:p.wait_for_timeout(5)
    check(bank+'/'+phase+' draws at least sixteen distinct native poses',len(set(frames))>=16)
   cycle=1.6
   a=decode(p.evaluate('b=>px17Render(b,"loop",1.5999)',bank));b=decode(p.evaluate('b=>px17Render(b,"loop",1.6001)',bank));gap=float(abs(a-b).mean())
   raw1=decode(p.evaluate('b=>px17Render(b,"loop",(PL11_ART[b].loop.frames.length-1)/PL11_ART[b].loop.fps,{blend:false})',bank));raw2=decode(p.evaluate('b=>px17Render(b,"loop",0,{blend:false})',bank));rawgap=float(abs(raw1-raw2).mean())
   check(bank+' has a continuous rendered loop boundary',gap<max(.02,rawgap*.10),{'boundary':gap,'hardSwitch':rawgap})
   a=decode(p.evaluate('b=>px17Render(b,"form",1.6)',bank));b=decode(p.evaluate('b=>px17Render(b,"loop",0)',bank));c=decode(p.evaluate('b=>px17Render(b,"close",0)',bank))
   check(bank+' formation, loop and closure share the exact open pose',np.array_equal(a,b) and np.array_equal(b,c))
   hole=[]
   for t in [0,.4,.8,1.2]:
    im=decode(p.evaluate('([b,t])=>px17Render(b,"loop",t)',[bank,t]));hole.append(int(im[im.shape[0]//2,im.shape[1]//2].max()))
   check(bank+' black aperture remains opaque throughout its loop',max(hole)<8,hole)
   check(bank+' opens circularly and one-shots clamp after completion',p.evaluate('b=>PL11.sample(b,"form",.8).rotation>3&&PL11.sample(b,"form",99).done&&PL11.sample(b,"close",99).done&&!PL11.sample(b,"loop",99).done',bank))
   p.evaluate('b=>px17Render(b,"loop",.4)',bank);p.screenshot(path=str(OUT/(bank+'-native.png')))
  row=p.evaluate('()=>({keys:px17Keys.size,expected:Object.values(PXV17_ART.portals).reduce((s,b)=>s+PL11.phases.reduce((n,ph)=>n+b[ph].frames.length,0),0)})');check('The real renderer consumes every generated portal key',row['keys']==row['expected'],row)
  def setup(stage):
   p.evaluate(shoot.SETUP,dict(state='PLAY',stage=stage,pilot='cole',invuln=True));p.wait_for_function('()=>{stageLoadTick();return stageLoadInfo(run.stage).ready;}')
   p.evaluate('''()=>{BOFCinematicDirector.cancel();story=fb2Talk=s6Opening=null;stagePlan=[];enemies=[];eBullets=[];pBullets=[];boss=null;bossActive=false;subBoss=null;subBossActive=false;subBossDone=true;player.invuln=9999;camX=0;}''')
  def ticks(n):
   for i in range(0,n,12):
    err=p.evaluate(shoot.STEP,min(12,n-i))
    if err:errors.append(err)
    p.wait_for_timeout(5)
  def snap(name):
   p.evaluate('()=>{shake=0;ctx.setTransform(SS,0,0,SS,0,0);if(state===GS.WARPENTRY)drawL78Entry(0);else drawWorld(0);SC12.refresh();window.__bofFit();}');p.screenshot(path=str(OUT/(name+'.png')))
  setup(7);p.evaluate('()=>{mapScroll=s7mEndScroll();spawnBoss("sludgeemperor");s7mInit(boss);v17Warm(7);VOID17.portals=[];}')
  observed=set()
  for count,name in [(220,'stage7-portal-forming'),(220,'stage7-portal-open'),(160,'stage7-portal-closing')]:
   ticks(count);snap(name);observed.update(p.evaluate('VOID17.portals.filter(q=>q.bank==="green_rift").map(q=>q.phase)'))
  check('Stage 7 native entrance reaches all three authored lifecycle phases',observed=={'form','loop','close'},sorted(observed))
  check('Stage 7 boss entrance uses green portals exclusively',p.evaluate('VOID17.portals.length>0&&VOID17.portals.every(q=>q.bank==="green_rift")'))
  p.evaluate('()=>{s7mSet(boss,"portal-volley");}');ticks(120);snap('stage7-attack-rifts');check('Stage 7 attack portals use the new green bank',p.evaluate('VOID17.portals.some(q=>q.bank==="green_rift"&&q.size===96)'))
  p.evaluate('()=>{s7mSet(boss,"dead");VOID17.portals=[];}');observed=set();sizes=set()
  for count,name in [(185,'stage7-escape-forming'),(40,'stage7-escape-open'),(65,'stage7-escape-closing')]:
   ticks(count);snap(name);observed.update(p.evaluate('VOID17.portals.map(q=>q.phase)'));sizes.update(p.evaluate('VOID17.portals.map(q=>q.size)'))
  check('Stage 7 native escape uses all three authored lifecycle phases',observed=={'form','loop','close'},sorted(observed))
  check('The portal the pilot flies into on Stage 7 is green',p.evaluate('VOID17.portals.length>0&&VOID17.portals.every(q=>q.bank==="green_rift")'))
  check('Stage 7 escape retains one canvas size instead of shrinking its idle picture',len(sizes)==1 and next(iter(sizes))>200,sorted(sizes))
  setup(8);p.evaluate('()=>{l78EntryStart();setState(GS.WARPENTRY);VOID17.portals=[];}');observed=set();sizes=set()
  for count,name in [(60,'stage8-arrival-forming'),(40,'stage8-arrival-open'),(105,'stage8-arrival-closing')]:
   ticks(count);snap(name);observed.update(p.evaluate('VOID17.portals.map(q=>q.phase)'));sizes.update(p.evaluate('VOID17.portals.map(q=>q.size)'))
  check('Stage 8 native arrival uses all three authored lifecycle phases',observed=={'form','loop','close'},sorted(observed))
  check('Stage 8 arrival is red throughout formation, idle and closure',p.evaluate('VOID17.portals.length>0&&VOID17.portals.every(q=>q.bank==="red_rift")'))
  check('Stage 8 arrival retains one canvas size while the authored aperture closes',len(sizes)==1 and next(iter(sizes))>200,sorted(sizes))
  p.evaluate('()=>{l78entry=null;run._l78Entry=0;setState(GS.PLAY);spawnBoss(curStage.boss);boss.enter=false;r30Warm();v17Warm(8);}');p.wait_for_function('()=>v17Keys(8).map(k=>XART.rdy(k)).every(Boolean)')
  for phase in [0,1,2]:
   p.evaluate('''n=>{j3Encounter(boss,n);const D=dr5State(boss);D.introSeen=true;D.introWanted=false;D.radio=null;boss._r30.mode='fight';boss.enter=false;boss._r30.attack=null;boss._r30.cd=999;const Q=v17Clock(boss);Q.transition=2;Q.combat=0;Q.t=12;}''',phase)
   snap('arena-'+str(phase+1)+'-battle')
   row=p.evaluate('''()=>{const q=v17Clock(boss),before=q.t;for(let i=0;i<8;i++)v17ArenaDraw(boss);return{phase:VOID17.last.phase,paused:q.t===before,code:VOID17.draws.code};}''')
   check('Arena '+str(phase+1)+' renders its own plate and draw calls do not advance time',row['phase']==phase and row['paused'],row)
   p.evaluate('()=>{boss._r30.attack=null;boss._r30.cd=999;}');ticks(250);snap('arena-'+str(phase+1)+'-code-awake')
   check('Arena '+str(phase+1)+' code illuminates during native combat',p.evaluate('VOID17.last.awake===1&&VOID17.draws.code>0'))
   row=p.evaluate('''()=>{const before=ctx.getImageData(0,0,ctx.canvas.width,ctx.canvas.height).data;return{points:VOID17.last.points.map(p=>p.depth),center:VOID17.last.left+VOID17.last.w/2};}''')
   check('Arena '+str(phase+1)+' has three distinct parallax depths',len(set(row['points']))==3,row)
   for fit in [False,True]:
    p.evaluate('''fit=>{VIEW_FIT=fit;camX=Math.max(0,worldWidth()-viewW());ctx.setTransform(SS,0,0,SS,0,0);ctx.fillStyle='#ff00ff';ctx.fillRect(0,0,VW,VH);ctx.save();const z=viewZoom();ctx.scale(z,z);ctx.translate(-camLeftX(),VH*(1-z)/z);v17ArenaDraw(boss);ctx.restore();}''',fit)
    image=decode(p.evaluate('cv.toDataURL()'));magenta=(image[:,:,0]>240)&(image[:,:,1]<20)&(image[:,:,2]>240)
    check('Arena '+str(phase+1)+' covers the visible field at '+str(fit)+' fit',not magenta.any(),{'uncovered':int(magenta.sum())})
  p.evaluate('()=>{boss._r30.mode="escape";}');check('Escape/continue scenes retain their existing environment',p.evaluate('!v17Active(boss)'))
  rows=[]
  p.evaluate('()=>{const D=dr5State(boss);D.radio=null;D.introWanted=false;D.introSeen=true;dr5Ships(boss);}')
  for mode,t,expected in [('dr5Portal',1,'form'),('dr5Portal',3,'loop'),('dr5Portal',7,'close'),('reunion',.4,'loop'),('reunion',1.5,'close')]:
   p.evaluate('''([mode,t])=>{boss._r30.mode=mode;boss._r30.t=t;dr5State(boss).deathStarted=mode==='reunion';VOID17.portals=[];}''',[mode,t])
   snap('stage8-'+mode+'-'+expected);row=p.evaluate('VOID17.portals.at(-1)||null');rows.append(row)
   check('Stage 8 '+mode+' '+expected+' uses its red native portal',row is not None and row['bank']=='red_rift' and row['phase']==expected,row)
  row=p.evaluate('''()=>{const out=[];for(const bank of ['blue_rift','green_rift','red_rift']){const pose=PL11.sequence(bank,2.7,{form:2,loop:4.2,close:1.4}),r=v17Route(bank,pose);out.push({bank:r.bank,phase:r.pose.phase,progress:(r.pose.from+r.pose.mix)/PL11_ART[r.bank].loop.frames.length,original:(pose.from+pose.mix)/PL11_ART[bank].loop.frames.length});}return out;}''')
  check('All ordinary Stage 8 rift routes resolve red without resetting loop phase',all(r['bank']=='red_rift' and abs(r['progress']-r['original'])<1e-9 for r in row),row)
  p.evaluate('''()=>{j3Encounter(boss,1);boss._r30.mode='dr5Reform';j3State(boss).pt11Portal={x:boss.x,y:boss.y,t:2.7,size:340};VOID17.portals=[];}''');snap('stage8-purple-reform')
  check('Stage 8 reformation uses the replacement purple-black rift',p.evaluate('VOID17.portals.some(q=>q.bank==="black_void")&&PL11_ART.black_void.derivedFrom==="blue_rift"'))
  p.evaluate('''()=>{window.B=boss;j3Encounter(B,2);const dr=dr5State(B);dr.introWanted=false;dr.introSeen=true;j3Mimic(B,8);on5FightStart(B);story=fb2Talk=null;BOFCinematicDirector.cancel();B.x=worldWidth()/2;B.y=PLAY.y+167;B._drawY=B.y;const D=gd4Create(B,8);D.p.x=B.x;D.p.y=B.y;D.p._hammer.hammerDestroyed=false;D.p._hammer.hammerHP=D.p._hammer.hammerMax;D.p._hammer.state='hammer';B.parts.find(q=>q.id==='hammer').destroyed=false;hc7Warm();hc7RiftStart(B);VOID17.portals=[];}''')
  p.wait_for_function('()=>Object.values(HC7_ART).flat().map(a=>XART.rdy(a.key)).every(Boolean)')
  rows=[]
  for phase,t in [('raise',1.8),('active',.6),('recover',.3)]:
   p.evaluate('''([phase,t])=>{const C=B._r30.hc7Rift;C.phase=phase;C.t=t;}''',[phase,t]);snap('chromium-rift-'+phase)
   rows.append(p.evaluate('()=>({pose:VOID17.portals.at(-1),size:B._r30.hc7Rift.radius*2})'))
  check('Chromium spell uses separate authored form, loop and closing reels',[r['pose']['phase'] for r in rows]==['form','loop','close'],rows)
  check('Chromium spell retains a fixed physical draw canvas during formation and closure',all(r['pose']['size']==r['size'] for r in rows),rows)
  q=p.evaluate('''()=>{const C=B._r30.hc7Rift;C.phase='active';C.t=.6;const D=gd4Create(B,8),v=r30Parts(B).find(q=>q.p.id==='hammer');B._lastPart=v.p;const before=D.p._hammer.hammerHP;modularHit(1);return{targetable:hammerWeaponTargetable(D.p),damage:before-D.p._hammer.hammerHP,alive:!!B._r30.hc7Rift};}''')
  check('Existing cast module remains targetable and takes real damage',q['targetable'] and q['damage']>0 and q['alive'],q)
  if p.evaluate('Object.keys(PXV17_ART.wind||{}).length===3'):
   setup(1);p.wait_for_function('()=>WP11_KEYS.map(a=>XART.rdy(a.key)).every(Boolean)')
   rows=p.evaluate('''()=>{const rows=[];for(const [family,kind] of [['bullets','mg'],['spread','spread'],['heavy','mg']]){const keys=new Set();let widest=0,tallest=0;const oldGet=XART.get,oldDraw=ctx.drawImage;let key=null;
    XART.get=function(k){const im=oldGet.apply(this,arguments);key=k;return im;};ctx.drawImage=function(){if(key?.startsWith('pxv17_wind'))keys.add(key);key=null;return oldDraw.apply(this,arguments);};
    for(let i=0;i<16;i++){ctx.canvas.width=ctx.canvas.width;ctx.setTransform(1,0,0,1,0,0);const b={kind,_cal50:family==='heavy',_inf:'wind',_infLv:5,x:240,y:300,vx:0,vy:-8,t:i/16,w:12,h:24};wp11Draw(b);const data=ctx.getImageData(0,0,ctx.canvas.width,ctx.canvas.height).data;let minX=9999,maxX=0,minY=9999,maxY=0;for(let y=0;y<ctx.canvas.height;y++)for(let x=0;x<ctx.canvas.width;x++){const k=(y*ctx.canvas.width+x)*4;if(data[k]+data[k+1]+data[k+2]>65){minX=Math.min(minX,x);maxX=Math.max(maxX,x);minY=Math.min(minY,y);maxY=Math.max(maxY,y);}}widest=Math.max(widest,maxX-minX+1);tallest=Math.max(tallest,maxY-minY+1);}
    XART.get=oldGet;ctx.drawImage=oldDraw;rows.push({family,keys:keys.size,widest,tallest});}return rows;}''')
   for row in rows:check(row['family']+' Wind rounds use all16 PixelLab frames and stay small at max level',row['keys']==16 and row['widest']<=23 and row['tallest']<=23,row)
   p.evaluate('''()=>{pBullets=['mg','spread','mg'].map((kind,i)=>({kind,_cal50:i===2,_inf:'wind',_infLv:5,x:worldWidth()/2-65+i*65,y:330,vx:0,vy:-8,t:.4,w:12,h:24,dmg:1}));}''');snap('wind-small-rounds')
  check('Maverick homing lasers still cannot receive Wind',p.evaluate('wp11Family({kind:"mavlaser",_inf:"wind"})===null'))
  check('No page, console or asset errors',not errors,errors);br.close()
finally:stop()
(OUT/'verification.json').write_text(json.dumps({'checks':checks,'errors':errors,'passed':sum(q['passed'] for q in checks),'failed':sum(not q['passed'] for q in checks)},indent=2)+'\n')
print('SUMMARY',sum(q['passed'] for q in checks),'passed',sum(not q['passed'] for q in checks),'failed',len(errors),'browser errors')
sys.exit(1 if errors or any(not q['passed'] for q in checks) else 0)
