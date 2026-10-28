"""Focused live native-gun checkpoint: special selection held; native combat
feedback remains visible. Jace keeps the Normal tell/cooldown and live turrets.
All five normal/heavy gun selector slots are enabled only for this isolated fixture.
"""
from pathlib import Path
import ast,json,time,base64,subprocess,re
import imageio_ffmpeg
from playwright.sync_api import sync_playwright
import shoot
from record_furious_789_1025 import CAPTURE
R=Path(__file__).resolve().parents[1];O=R/'_shots/jace_turrets_1028/video';O.mkdir(parents=True,exist_ok=True);F=O/time.strftime('%H%M%S');F.mkdir()
def strings(file):return[n.value for n in ast.walk(ast.parse((R/file).read_text(encoding='utf8')))if isinstance(n,ast.Constant)and isinstance(n.value,str)]
SETUP=next(s for s in strings('_BUILD_SOURCE/probe_feedback_1002.py')if s.startswith('c=>{ht27Stop'))
INIT=next(s for s in strings('_BUILD_SOURCE/probe_rebel_balance_1019.py')if s.startswith('gang=>{window.R='))
cap=CAPTURE.replace("debugStartFight(entry,{pilot:'cole',record:false});DBGT.god=true;DBGT.speed=1;player.invuln=0;","DBGT.god=true;DBGT.speed=1;").replace("diffKey='furious';debugUnlocked=true;","diffKey='normal';debugUnlocked=true;")
cap=cap.replace('A.tick++;',"A.tick++;for(const k of ['a','d','w','s','j','k','c'])K[k]=false;return;")
cap=cap.replace('FURIOUS / COLE / INVULNERABLE INPUT BOT / NATIVE HP & PHASES','NORMAL / JACE TURRET ALIGNMENT / INVULNERABLE OBSERVER')
errors=[];FF=imageio_ffmpeg.get_ffmpeg_exe();port,stop=shoot.serve(str(R))
try:
 with sync_playwright()as pw:
  b=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1280,'height':800});p.set_default_timeout(180000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'or'draw error'in m.text else None);p.on('response',lambda r:errors.append(str(r.status)+' '+r.url)if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>5');p.mouse.click(3,3);p.evaluate(shoot.TRAP_RAF)
  p.evaluate('()=>{run.stage=6;stageLoadBegin(6);rr26Warm();}')
  p.evaluate(SETUP,dict(stage=6,kind='rebelsquad',diff='normal',pilot='cole'));p.evaluate(INIT,True)
  p.wait_for_function("()=>{stageLoadTick();rr26Warm();return stageLoadReady(6)&&Object.keys(JR36_TURRETS).every(k=>XART.rdy(k))&&XART.rdy('jr36_spin')}")
  p.evaluate("""()=>{G.releaseAt=G.rescueAt=G.rd21.next=999;G.rescueDone=true;G.rd21.fleet=null;G.rr26=rr26State(G);G.rr26.wall=null;RBAL19.cfg.normal.slots=5;RBAL19.cfg.normal.heavySlots=5;player.invuln=99999;player.fireCd=99999;for(const q of R.ships){q.x=camLeftX()+viewW()/2+(q.i-2)*76;q.y=PLAY.y+95+(q.i%2)*45;q.mode='fight';q.warp=0;q.rfHeading=Math.PI/2;q.rg4.cd=999;q.rg4.armed=null;q.rg4.act=null;q.rg4.gunCd=999;q.rg4._rbal19Gun=null;}for(const a of s6Wing.ships)a.fireCd=999; eBullets=[];pBullets=[];window.jace=R.ships.find(q=>q.key==='jace');jace.rg4.gunCd=0;window.jrMuzzleLog=[];const bullet=rr36Bullet;rr36Bullet=function(){const z=bullet.apply(this,arguments);if(!z.dead)jrMuzzleLog.push({seconds:(performance.now()-captureStart)/1000,...z._jr36Origin});return z;};}""")
  with(F/'capture.webm').open('wb')as raw:
   p.expose_function('saveCaptureChunk',lambda s:raw.write(base64.b64decode(s)));p.evaluate('()=>{window.requestAnimationFrame=window.__bofRealRAF;last=performance.now();requestAnimationFrame(loop);}')
   p.evaluate(cap,{'stage':6})
   while p.evaluate('(performance.now()-captureStart)/1000')<14 and not errors:p.wait_for_timeout(350)
   data=p.evaluate("async()=>{reviewBot.enabled=false;await new Promise(r=>{reviewRecorder.onstop=r;reviewRecorder.stop()});await capturePending;captureLive=false;return{seconds:(performance.now()-captureStart)/1000,sound:captureStats,muzzles:jrMuzzleLog,game:{state,arsenal:G.arsenal1004c,scene:G.scene,age:G.age,intro:R.frIntro,act:jace.rg4.act,gun:jace.rg4._rbal19Gun,dead:jace.dead,hp:jace.hp,heading:jace.rfHeading},events:RBAL19.events};}")
   (F/'capture-data.json').write_text(json.dumps(data,indent=2))
  b.close()
finally:stop()
video=F/'jace-turrets.mp4';subprocess.run([FF,'-v','error','-y','-threads','2','-i',str(F/'capture.webm'),'-vf','fps=30','-c:v','libx264','-preset','fast','-crf','20','-c:a','aac','-b:a','160k','-pix_fmt','yuv420p','-movflags','+faststart',str(video)],check=True)
dec=subprocess.run([FF,'-hide_banner','-nostats','-threads','2','-i',str(video),'-af','volumedetect','-f','null','-'],capture_output=True,text=True);(F/'decode.log').write_text(dec.stderr);pk=re.search(r'max_volume: ([\-\d.inf]+) dB',dec.stderr);peak=float(pk[1])if pk else-999
for side,name in [(-1,'port'),(1,'starboard')]:
 t=next((q['seconds']for q in data['muzzles']if q['side']==side),None)
 if t is not None:subprocess.run([FF,'-v','error','-y','-ss',str(t+.04),'-i',str(video),'-frames:v','1',str(F/(name+'.png'))],check=True)
checks=dict(noErrors=not errors and not data['sound']['tapErrors'],decoded=dec.returncode==0,audible=peak>-60,unclipped=peak<0,realTime=data['sound']['frames']/data['seconds']>45,bothTurrets={q['side']for q in data['muzzles']}=={-1,1},repeatedNativeFire=len(data['muzzles'])>=4)
report=dict(method=__doc__,video=video.relative_to(R).as_posix(),errors=errors,checks=checks,decodedPeakDb=peak,**data);(F/'report.json').write_text(json.dumps(report,indent=2));(O/'latest.json').write_text(json.dumps(dict(folder=F.relative_to(R).as_posix())))
print(json.dumps(dict(video=str(video),checks=checks,muzzles=data['muzzles'],peak=peak)),flush=True);raise SystemExit(0 if all(checks.values())else 1)
