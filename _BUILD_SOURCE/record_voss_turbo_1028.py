"""Native Stage6 scene and one selected Voss attack cycle. Invulnerable observer;
other special selections and allied autofire held for this focused animation
review. No Voss HP, phase or timer writes after selection.
"""
from pathlib import Path
import ast,json,time,base64,subprocess,re
from playwright.sync_api import sync_playwright
import imageio_ffmpeg,shoot
from record_furious_789_1025 import CAPTURE
R=Path(__file__).resolve().parents[1];O=R/'_shots/voss_turbo_1028/video';O.mkdir(parents=True,exist_ok=True);F=O/time.strftime('%H%M%S');F.mkdir()
def strings(f):return[n.value for n in ast.walk(ast.parse((R/f).read_text(encoding='utf8')))if isinstance(n,ast.Constant)and isinstance(n.value,str)]
BOOT=next(s for s in strings('_BUILD_SOURCE/record_rough_riders_guide_1028.py')if s.startswith('key=>{'))
cap=CAPTURE[:CAPTURE.index(" diffKey='furious';debugUnlocked=true;")]+" return {capture:true};}"
cap=cap.replace('A.tick++;',"A.tick++;for(const k of ['a','d','w','s','j','k','c'])K[k]=false;return;")
cap=cap.replace('FURIOUS / COLE / INVULNERABLE INPUT BOT / NATIVE HP & PHASES','FURIOUS / VOSS ATTACK CHECKPOINT / INVULNERABLE OBSERVER')
errors=[];timeline=[];port,stop=shoot.serve(str(R));FF=imageio_ffmpeg.get_ffmpeg_exe()
try:
 with sync_playwright()as pw:
  b=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required','--disable-background-timer-throttling','--disable-renderer-backgrounding']);p=b.new_page(viewport={'width':1280,'height':800});p.set_default_timeout(180000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'or'draw error'in m.text else None);p.on('response',lambda r:errors.append(str(r.status)+' '+r.url)if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>5');p.mouse.click(3,3);p.evaluate(shoot.TRAP_RAF);p.evaluate(BOOT,'voss')
  p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(6)&&Object.values(VS41_ART.banks).every(a=>XART.rdy(a.key))}')
  p.evaluate("""()=>{window.B=boss;window.R=B._rebels;window.G=R.gang1004;window.voss=R.ships.find(q=>q.key==='voss');G.scene=null;G.releaseAt=G.rescueAt=G.rd21.next=999;G.rebelBoxes=[];G.ord=[];for(const q of R.ships){q.mode='fight';q.warp=0;q.rg4.act=null;q.rg4.cd=q.rg4.gunCd=999;q.rg4.armed=null;q.rg4.supply=null;}s6WingInit();s6WingLaunch(4,true);s6Wing.beats=3;s6Wing.all=true;s6Wing.fakeDone=true;s6Wing.route='right';s6Wing.supplyIndex=3;s6Wing.boxes=[];for(const q of s6Wing.ships){q.phase='fight';q.x=camLeftX()+viewW()/2+(q.slot%2?1:-1)*(65+Math.floor(q.slot/2)*45);q.y=VH-100;q.gx=q.x;q.gy=q.y;q.fcd=999;}s6WingArsenal=function(){};voss.x=camLeftX()+viewW()*.30;voss.y=PLAY.y+135;voss.rfHeading=Math.PI/2;player.x=camLeftX()+viewW()/2;player.y=VH-65;VS41.events=[];rg4Attack(voss,R,G,'turbo');}""")
  with(F/'capture.webm').open('wb')as raw:
   p.expose_function('saveCaptureChunk',lambda s:raw.write(base64.b64decode(s)));p.evaluate('()=>{window.requestAnimationFrame=window.__bofRealRAF;last=performance.now();requestAnimationFrame(loop);}');p.evaluate(cap,{'stage':6});done=None
   while True:
    p.wait_for_timeout(300);row=p.evaluate("()=>({seconds:(performance.now()-captureStart)/1000,clock:G.age,phase:voss.rg4.act?.phase,kind:voss.rg4.act?.kind,x:voss.x,y:voss.y,scale:voss._rd21Scale,heading:voss.rfHeading,hp:voss.hp,frame:vs41Frame(voss),safe:vs41Safe(voss),orbs:G.ord.filter(o=>o._vs41Orb).length,frames:captureStats.frames,playerDead:player.dead})");timeline.append(row)
    if not row.get('phase')and done is None:done=row['seconds']
    if done is not None and row['seconds']-done>.9 or row['seconds']>23 or errors:break
   data=p.evaluate("async()=>{reviewBot.enabled=false;await new Promise(r=>{reviewRecorder.onstop=r;reviewRecorder.stop()});await capturePending;captureLive=false;return{seconds:(performance.now()-captureStart)/1000,sound:captureStats,events:VS41.events};}");(F/'capture-data.json').write_text(json.dumps(data,indent=2))
  b.close()
finally:stop()
video=F/'voss-turbo.mp4';subprocess.run([FF,'-v','error','-y','-threads','2','-i',str(F/'capture.webm'),'-vf','fps=30','-c:v','libx264','-preset','fast','-crf','20','-c:a','aac','-b:a','160k','-pix_fmt','yuv420p','-movflags','+faststart',str(video)],check=True)
dec=subprocess.run([FF,'-hide_banner','-nostats','-threads','2','-i',str(video),'-af','volumedetect','-f','null','-'],capture_output=True,text=True);(F/'decode.log').write_text(dec.stderr);pk=re.search(r'max_volume: ([\-\d.inf]+) dB',dec.stderr);peak=float(pk[1])if pk else-999
shots=[]
for phase,name in [('charge','cannon-charge'),('fire','twin-cannons'),('turbocharge','turbo-power'),('dash','overhead-south'),('north','north-return'),('approach','formation-return')]:
 rows=[q for q in timeline if q.get('phase')==phase]
 if rows:
  q=rows[len(rows)//2];t=q['seconds'];subprocess.run([FF,'-v','error','-y','-ss',str(t),'-i',str(video),'-frames:v','1',str(F/(name+'.png'))],check=True);shots.append(dict(phase=phase,name=name,time=t))
phases={q.get('phase')for q in timeline};checks=dict(noErrors=not errors and not data['sound']['tapErrors'],decoded=dec.returncode==0,audible=peak>-60,unclipped=peak<0,realTime=data['sound']['frames']/data['seconds']>45,bothCannons=any(e['event']=='twin-cannon'and e['count']==2 for e in data['events']),charge='turbocharge'in phases,northReturn='north'in phases,continuousTurns={'turn-north','turn-south'}.issubset(phases),recovery=done is not None,liveNativeScene=bool(timeline))
report=dict(method=__doc__,video=video.relative_to(R).as_posix(),errors=errors,checks=checks,decodedPeakDb=peak,timeline=timeline,shots=shots,**data);(F/'report.json').write_text(json.dumps(report,indent=2));(O/'latest.json').write_text(json.dumps(dict(folder=F.relative_to(R).as_posix())))
print(json.dumps(dict(video=str(video),checks=checks,peak=peak,duration=data['seconds'])),flush=True);raise SystemExit(0 if all(checks.values())else 1)
