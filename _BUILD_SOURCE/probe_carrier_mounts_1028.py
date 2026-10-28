"""Measured Carrier wing mounts, native render/flash checks and focused replay.

Fixture selects two native laser launchers once. Other weapons and bay flight
are held for this mounting review; no part HP/attack timers are written during
the real-time recording. This is a visual checkpoint, not a complete fight.
"""
from pathlib import Path
import base64,json,subprocess,time,re,http.server
from PIL import Image
import numpy as np
from playwright.sync_api import sync_playwright
import imageio_ffmpeg,shoot
from record_furious_789_1025 import CAPTURE

R=Path(__file__).resolve().parents[1]
O=R/'_shots/carrier_mounts_1028';O.mkdir(parents=True,exist_ok=True)
F=O/time.strftime('%H%M%S');F.mkdir()
checks=[];errors=[]
def check(name,passed,data=None):
 checks.append(dict(name=name,passed=bool(passed),data=data))
 (O/'checks.json').write_text(json.dumps(dict(checks=checks,errors=errors),indent=2))
 assert passed,name

for state in ['closed','open']:
 a=np.array(Image.open(R/f'assets/game/shared/combat/encounter_revision_1027/clean_whv_{state}_w.png').convert('RGBA'))
 check(f'Both complete turret bases rest on opaque {state} metal panels',all(np.all(a[y-16:y+17,x-16:x+17,3]==255)for x,y in [(152,164),(360,164)]))

s=(R/'assets/carrier_turret_sockets_1028.js').read_text();sockets=json.loads(s[s.index('{'):s.rindex('}')+1]);source=np.array(Image.open(R/sockets['source']).convert('RGBA'))
touches=[]
for f,(x,y)in enumerate(sockets['muzzles']):
 left=f%8*72;top=f//8*72;ix=int(x);iy=int(y);touches.append(bool(np.any(source[top+iy-2:top+iy+3,left+ix-2:left+ix+3,3]>=128)))
check('All256 measured rotation/recoil mouths touch actual authored barrel pixels',len(touches)==256 and all(touches))

BOOT="""()=>{diffKey='furious';run.ngplus=false;debugUnlocked=true;debugStartFight({stage:6,role:'boss',kind:'warhive'},{pilot:'cole',record:false});DBGT.god=true;DBGT.speed=1;spawnBoss('warhive');debugFight.spawned=true;warnT=0;BOFCinematicDirector.cancel();setState(GS.PLAY);bossActive=true;s6Wing.ships=[];s6Wing.boxes=[];s6Opening=fb2Talk=fb2Intro=null;stagePlan=[];spawnClock=Infinity;subBossTriggered=aminiTriggered=true;for(const k of ['a','d','w','s','j','k','c'])Input.keys[k]=false;}"""
HOLD="""()=>{const b=boss,C=b._carrier17;enemies=[];powerups=[];pBullets=[];eBullets=[];subBoss=null;subBossActive=false;C.flight=999;C.bayOpen=false;const bay=s6r18State(b).bay;bay.mode='cool';bay.open=0;bay.t=0;for(const p of C.parts){p.phase='rest';p.t=0;p.cool=999;p.muzzleAge=99;}player.x=b.x;player.y=VH-70;player.fireCd=999;window.mountBoss=b;}"""
cap=CAPTURE[:CAPTURE.index(" diffKey='furious';debugUnlocked=true;")]+"return {capture:true};}"
cap=cap.replace('A.tick++;',"A.tick++;for(const k of ['a','d','w','s','j','k','c'])K[k]=false;return;")
cap=cap.replace('FURIOUS / COLE / INVULNERABLE INPUT BOT / NATIVE HP & PHASES','FURIOUS / CARRIER WING MOUNTS / NATIVE LASERS / INVULNERABLE OBSERVER')
http.server.ThreadingHTTPServer.request_queue_size=256
port,stop=shoot.serve(str(R));FF=imageio_ffmpeg.get_ffmpeg_exe()
try:
 with sync_playwright()as pw:
  b=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required','--disable-background-timer-throttling','--disable-renderer-backgrounding'])
  p=b.new_page(viewport={'width':1280,'height':800});p.set_default_timeout(180000)
  p.on('pageerror',lambda e:errors.append(str(e)))
  p.on('console',lambda m:errors.append(m.text)if m.type=='error'or'draw error'in m.text else None)
  p.on('response',lambda r:errors.append(str(r.status)+' '+r.url)if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/');p.wait_for_function('window.__bofFrames>5&&typeof HC32!=="undefined"');p.mouse.click(3,3)
  p.evaluate('()=>{run.stage=6;stageLoadBegin(6)}');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(6)&&hc32Warm()}');p.evaluate(shoot.TRAP_RAF)
  def step(n):
   for i in range(0,n,24):
    err=p.evaluate(shoot.STEP,min(24,n-i));assert not err,err;p.wait_for_timeout(1)
  def setup():
   p.evaluate(BOOT);step(220);p.evaluate(HOLD)
  setup()
  q=p.evaluate("""()=>{const b=boss;return b._carrier17.parts.filter(p=>p.kind==='laser').map(p=>({id:p.id,dx:p.dx,dy:p.dy,mount:roster17Mount(b,p),hit:roster17At(b,...Object.values(roster17Mount(b,p))),old:roster17At(b,b.x+Math.sign(p.dx)*80*WHV_S*roster17HullScale(b),b.y+24*WHV_S*roster17HullScale(b))}));}""")
  check('Two outward mounts keep their original independent hit IDs and vacate the old sockets',len(q)==2 and all(v['hit']==v['id']and v['old']!=v['id']for v in q),q)
  q=p.evaluate("""()=>{const b=boss,out=[],draw=ctx.drawImage,get=XART.get;let key='';XART.get=function(k){key=k;return get.apply(this,arguments)};ctx.drawImage=function(im,...args){if(key===ER28_ART.carrier_turret.key){const t=this.getTransform();out.push({args,transform:[t.a,t.d,t.e,t.f]});}return draw.call(this,im,...args)};try{roster17Draw(b)}finally{ctx.drawImage=draw;XART.get=get}return{out,expected:b._carrier17.parts.filter(p=>p.kind==='laser').map(p=>roster17Mount(b,p))};}""")
  # Verify real cell placements using their registered common pivot.
  pivot=p.evaluate('ER28_ART.carrier_turret.pivot')
  check('Actual authored turret cells draw at both new native pivots',len(q['out'])==2 and all(abs(v['args'][4]+pivot[0]-w['x'])<2 and abs(v['args'][5]+pivot[1]-(w['y']-4.1875*1.45))<2 for v,w in zip(q['out'],q['expected'])),q)
  for phase in ['tell','fire']:
   q=p.evaluate("""phase=>{const b=boss,C=b._carrier17,rows=[],base=phase==='tell'?combatWarningDraw:av3Beam;for(const p of C.parts.filter(p=>p.kind==='laser')){p.phase=phase;p.t=phase==='tell'?.7:.3;p.angle=p.er28Bearing=Math.PI/2+(p.id==='laser0'?.22:-.22);}if(phase==='tell')combatWarningDraw=function(part,o){if(part.kind==='laser')rows.push({id:part.id,x:o.x,y:o.y});return base.apply(this,arguments)};else av3Beam=function(c,x,y){rows.push({x,y});return base.apply(this,arguments)};try{roster17Draw(b)}finally{if(phase==='tell')combatWarningDraw=base;else av3Beam=base;}return{rows,ports:C.parts.filter(p=>p.kind==='laser').map(p=>roster17Muzzle(b,p))};}""",phase)
   check(f'Both native {phase} origins coincide with their relocated cannon mouths',len(q['rows'])==2 and all(abs(a['x']-c['x'])<.01 and abs(a['y']-c['y'])<.01 for a,c in zip(q['rows'],q['ports'])),q)
   p.evaluate('()=>drawScene(0)');p.screenshot(path=str(F/(phase+'.png')))
  p.evaluate(HOLD)
  sample="""()=>{const b=boss,p=b._carrier17.parts.find(p=>p.id==='laser0'),m=roster17Mount(b,p);ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);roster17Draw(b);ctx.restore();const a=ctx.getImageData(Math.round(m.x-28),Math.round(m.y-35),56,70).data;let white=0;for(let i=0;i<a.length;i+=4)if(a[i]>245&&a[i+1]>245&&a[i+2]>245)white++;return{white,hp:p.hp,flash:p.flash};}"""
  before=p.evaluate(sample);p.evaluate("()=>{boss._carrier17.direct='laser0';hitBoss(3)}");hit=p.evaluate(sample);step(20);after=p.evaluate(sample)
  check('Relocated laser takes native damage and visibly flashes white then expires',hit['hp']==before['hp']-3 and hit['white']>before['white']+30 and hit['flash']>0 and after['flash']==0 and after['white']<hit['white'],dict(before=before,hit=hit,after=after))
  q=p.evaluate("""()=>{const b=boss,C=b._carrier17,p=C.parts.find(p=>p.id==='laser0'),before=roster17Muzzle(b,p);b.x+=31;b.y+=13;roster17Sync(b);const after=roster17Muzzle(b,p),target=retinaBossTargets(b).find(t=>t._retinaId==='harrier laser0');return{dx:after.x-before.x,dy:after.y-before.y,target:target?{x:target.x,y:target.y}:null,mount:roster17Mount(b,p)};}""")
  check('Muzzle and native Retina follow the moved hull without detaching',abs(q['dx']-31)<.01 and abs(q['dy']-13)<.01 and abs(q['target']['x']-q['mount']['x'])<.01 and abs(q['target']['y']-q['mount']['y'])<.01,q)
  setup();p.evaluate("()=>{for(const p of boss._carrier17.parts.filter(p=>p.kind==='laser'))p.cool=.15;}")
  initial=p.evaluate('boss._carrier17.parts.map(p=>({id:p.id,hp:p.hp,max:p.maxhp}))')
  with(F/'capture.webm').open('wb')as raw:
   p.expose_function('saveCaptureChunk',lambda s:raw.write(base64.b64decode(s)))
   p.evaluate('()=>{window.requestAnimationFrame=window.__bofRealRAF;last=performance.now();requestAnimationFrame(loop)}');p.evaluate(cap,dict(stage=6))
   timeline=[]
   while True:
    p.wait_for_timeout(250);row=p.evaluate("()=>({seconds:(performance.now()-captureStart)/1000,parts:boss._carrier17.parts.filter(p=>p.kind==='laser').map(p=>({id:p.id,phase:p.phase,t:p.t,hp:p.hp,mount:roster17Mount(boss,p),muzzle:roster17Muzzle(boss,p)}))})");timeline.append(row)
    if row['seconds']>7.4 or errors:break
   data=p.evaluate("async()=>{reviewBot.enabled=false;await new Promise(r=>{reviewRecorder.onstop=r;reviewRecorder.stop()});await capturePending;captureLive=false;return{seconds:(performance.now()-captureStart)/1000,sound:captureStats,hp:boss._carrier17.parts.map(p=>({id:p.id,hp:p.hp,max:p.maxhp}))};}")
  b.close()
finally:stop()
video=F/'carrier-wing-mounts.mp4'
subprocess.run([FF,'-v','error','-y','-threads','2','-i',str(F/'capture.webm'),'-vf','fps=30','-c:v','libx264','-preset','fast','-crf','20','-c:a','aac','-b:a','160k','-pix_fmt','yuv420p','-movflags','+faststart',str(video)],check=True)
dec=subprocess.run([FF,'-hide_banner','-nostats','-threads','2','-i',str(video),'-af','volumedetect','-f','null','-'],capture_output=True,text=True);(F/'decode.log').write_text(dec.stderr)
peak=float(re.search(r'max_volume: ([\-\d.inf]+) dB',dec.stderr)[1])
check('Focused film retains native launcher HP throughout',initial==data['hp'])
check('Both relocated native lasers charge and fire during the replay',all(any(any(q['id']==key and q['phase']==phase for q in row['parts'])for row in timeline)for key in ['laser0','laser3']for phase in ['tell','fire']))
check('Replay fully decodes with audible unclipped native sound',dec.returncode==0 and -60<peak<0,dict(peak=peak))
check('Real-time capture and game have no browser/asset/audio errors',data['sound']['frames']/data['seconds']>45 and not errors and not data['sound']['tapErrors'],dict(fps=data['sound']['frames']/data['seconds'],errors=errors))
report=dict(method=__doc__,checks=checks,errors=errors,video=video.relative_to(R).as_posix(),timeline=timeline,decodedPeakDb=peak,**data)
(F/'report.json').write_text(json.dumps(report,indent=2));(O/'latest.json').write_text(json.dumps(dict(folder=F.relative_to(R).as_posix())))
print(json.dumps(dict(video=report['video'],checks=len(checks),passed=all(q['passed']for q in checks),seconds=data['seconds'],peak=peak)))
