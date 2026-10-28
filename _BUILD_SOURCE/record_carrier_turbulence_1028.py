"""Native Furious Carrier life: input-only aiming, normal allies, GOD observer.
No enemy HP, phase or timer writes. Input prioritizes the two fans and briefly
releases player fire after each break and hull exposure to show the feedback.
"""
from pathlib import Path
import json,time,base64,re,subprocess,http.server,hashlib
from playwright.sync_api import sync_playwright
import imageio_ffmpeg,shoot,numpy as np
from record_furious_789_1025 import CAPTURE

R=Path(__file__).resolve().parents[1];O=R/'_shots/carrier_turbulence_1028/video';O.mkdir(parents=True,exist_ok=True);F=O/time.strftime('%H%M%S');F.mkdir()
cap=CAPTURE[:CAPTURE.index(" diffKey='furious';debugUnlocked=true;")]+"""diffKey='furious';run.ngplus=false;debugUnlocked=true;debugStartFight({stage:6,role:'boss',kind:'warhive'},{pilot:'cole',record:false});DBGT.god=true;DBGT.speed=1;player.invuln=0;spawnBoss('warhive');debugFight.spawned=true;warnT=0;BOFCinematicDirector.cancel();setState(GS.PLAY);bossActive=true;s6Opening=fb2Talk=fb2Intro=null;return{native:true};}"""
cap=cap.replace("list=list.filter(t=>t.y>=PLAY.y-180&&t.y<VH-20);","""list=list.filter(t=>t.y>=PLAY.y-180&&t.y<VH-20);
 const fan=b?._carrier17?.parts.find(p=>p.kind==='fan'&&!p.dead);if(fan)list=list.filter(t=>t._retinaId==='harrier '+fan.id);""")
cap=cap.replace("A.targetInfo=target?", """const mask=b?._hc32?.fanMask||0;if(mask!==A.fanMask){A.fanMask=mask;A.pauseUntil=elapsed+(mask===3?1.4:.9);}if(b?._hc32?.exposed&&!A.hullSeen){A.hullSeen=true;A.pauseUntil=elapsed+2.4;}if(elapsed<(A.pauseUntil||0)){K.j=K.c=false;}
  A.targetInfo=target?""")
errors=[];timeline=[];http.server.ThreadingHTTPServer.request_queue_size=256;port,stop=shoot.serve(str(R));FF=imageio_ffmpeg.get_ffmpeg_exe()
try:
 with sync_playwright()as pw:
  browser=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required','--disable-background-timer-throttling','--disable-renderer-backgrounding']);p=browser.new_page(viewport={'width':1280,'height':800});p.set_default_timeout(180000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'or'draw error'in m.text else None);p.on('response',lambda r:errors.append(str(r.status)+' '+r.url)if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/');p.wait_for_function('window.__bofFrames>5');p.mouse.click(3,3);p.evaluate('()=>{run.stage=6;stageLoadBegin(6)}');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(6)&&hc32Warm()}')
  with(F/'capture.webm').open('wb')as raw:
   p.expose_function('saveCaptureChunk',lambda s:raw.write(base64.b64decode(s)));p.evaluate(cap,dict(stage=6));last=None;completed=None;nextProgress=10
   while True:
    p.wait_for_timeout(220)
    row=p.evaluate("""()=>{const b=boss,C=b?._carrier17,S=b?._hc32,W=b?._whv;return{seconds:(performance.now()-captureStart)/1000,hp:b?.hp,max:b?.maxhp,mode:W?.mode,phase:C?.phase,ace:W?.ace?._nw28?.mode,down:S?.motion?.down||0,motion:S?.motion,mask:S?.fanMask,exposed:S?.exposed,core:S?.core,frame:hc32HeatFrame(b),fall:!!b?._s6CarrierFall,parts:C?.parts.map(p=>({id:p.id,hp:p.hp,max:p.maxhp,dead:p.dead})),frames:captureStats.frames,botErrors:reviewBot.errors}}""");timeline.append(row)
    (F/'live.json').write_text(json.dumps(row,indent=2))
    if row['seconds']>=nextProgress:print(json.dumps(dict(progress=round(row['seconds'],1),hp=row.get('hp'),phase=row.get('phase'),mask=row.get('mask'))),flush=True);nextProgress+=10
    tag=(row.get('mask'),row.get('exposed'),row.get('mode'),row.get('ace'))
    if tag!=last:print(json.dumps(dict(seconds=round(row['seconds'],2),mask=row.get('mask'),exposed=row.get('exposed'),mode=row.get('mode'),ace=row.get('ace'))),flush=True);last=tag
    if row.get('mode')=='ace'and row.get('ace')=='fight'and completed is None:completed=row['seconds']
    if completed is not None and row['seconds']-completed>1.0 or row['seconds']>180 or row['seconds']>12 and row.get('mode')is None or errors:break
   data=p.evaluate("async()=>{reviewBot.enabled=false;for(const k of ['a','d','w','s','j','k','c'])Input.keys[k]=false;await new Promise(r=>{reviewRecorder.onstop=r;reviewRecorder.stop()});await capturePending;captureLive=false;return{seconds:(performance.now()-captureStart)/1000,sound:captureStats,events:HC32.events,botErrors:reviewBot.errors};}")
  browser.close()
finally:stop()
video=F/'carrier-turbulence.mp4';subprocess.run([FF,'-v','error','-y','-threads','2','-i',str(F/'capture.webm'),'-vf','fps=30','-c:v','libx264','-preset','fast','-crf','20','-c:a','aac','-b:a','160k','-pix_fmt','yuv420p','-movflags','+faststart',str(video)],check=True)
dec=subprocess.run([FF,'-hide_banner','-nostats','-threads','2','-i',str(video),'-af','volumedetect','-f','null','-'],capture_output=True,text=True);(F/'decode.log').write_text(dec.stderr);peak=float(re.search(r'max_volume: ([\-\d.inf]+) dB',dec.stderr)[1]);shots=[]
for name,predicate in [('one-side',lambda q:q['down']==1),('both-sides',lambda q:q['down']==2 and not q.get('exposed')),('full-red',lambda q:q.get('exposed')and q.get('frame',-1)>=12 and q['frame']<16 and not q['fall']),('native-fall',lambda q:q['fall']and q.get('mode')!='ace')]:
 rows=[q for q in timeline if predicate(q)]
 if rows:
  row=rows[min(len(rows)-1,3)];at=row['seconds'];subprocess.run([FF,'-v','error','-y','-ss',str(at),'-i',str(video),'-frames:v','1',str(F/(name+'.png'))],check=True);shots.append(dict(name=name,time=at))
# State and capture clocks differ by a frame. Choose the red still from actual
# decoded pixels so native white hit feedback cannot masquerade as red proof.
redProof=None;exposed=[q['seconds']for q in timeline if q.get('exposed')and not q['fall']]
if exposed:
 start=min(exposed);length=min(10,max(exposed)-start);scan=subprocess.Popen([FF,'-v','error','-ss',str(start),'-i',str(video),'-t',str(length),'-vf','fps=30,crop=600:500:320:75,scale=120:100','-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE);best=(0,start);index=0
 while True:
  buf=scan.stdout.read(120*100*3)
  if len(buf)<120*100*3:break
  pixels=np.frombuffer(buf,dtype=np.uint8).reshape(-1,3).astype(float);bright=np.max(pixels,axis=1)>45;red=(pixels[:,0]>pixels[:,1]*1.35)&(pixels[:,0]>pixels[:,2]*1.35)&(pixels[:,0]>70);score=float(np.sum(red)/max(1,np.sum(bright)));best=max(best,(score,start+index/30));index+=1
 scan.wait();redProof=dict(time=best[1],redFractionOfBrightROI=best[0])
 if best[0]>.3:
  subprocess.run([FF,'-v','error','-y','-ss',str(best[1]),'-i',str(video),'-frames:v','1',str(F/'full-red.png')],check=True)
  next(s for s in shots if s['name']=='full-red')['time']=best[1]
checks=dict(nativeCarrierCompleted=completed is not None,oneSideVisible=any(q['down']==1 for q in timeline),bothSidesVisible=any(q['down']==2 for q in timeline),wholeRedVisible=bool(redProof and redProof['redFractionOfBrightROI']>.3),nativeHullReserve=any(q.get('core',0)>0 and q.get('exposed')and not q['fall']for q in timeline),nativeFallAndNightwing=any(q['fall']for q in timeline)and completed is not None,decoded=dec.returncode==0,audibleUnclipped=-60<peak<0,realTime=data['sound']['frames']/data['seconds']>45,noErrors=not errors and not data['sound']['tapErrors']and not data['botErrors'])
report=dict(method=__doc__,video=video.relative_to(R).as_posix(),checks=checks,errors=errors,decodedPeakDb=peak,decodedRedProof=redProof,timeline=timeline,shots=shots,sourceSha256=hashlib.sha256((R/'assets/carrier_hull_1028.js').read_bytes()).hexdigest(),**data);(F/'report.json').write_text(json.dumps(report,indent=2));(O/'latest.json').write_text(json.dumps(dict(folder=F.relative_to(R).as_posix())))
print(json.dumps(dict(video=report['video'],checks=checks,seconds=data['seconds'],peak=peak)),flush=True);raise SystemExit(0 if all(checks.values())else 1)
