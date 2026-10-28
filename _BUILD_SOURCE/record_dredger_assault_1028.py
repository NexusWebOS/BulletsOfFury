"""Complete native Furious Dredger life; native inputs, HP, attack book and death.
An explicitly labelled invulnerable observer waits for the revised moves, then
uses native aiming/fire/missile inputs. No enemy HP, phase or timer writes.
"""
from pathlib import Path
import base64,json,http.server,time,subprocess,re
import imageio_ffmpeg
from playwright.sync_api import sync_playwright
from shoot import serve
from barrage_review_common_1025 import boot
from record_furious_789_1025 import CAPTURE

R=Path(__file__).resolve().parents[1];O=R/'_shots/dredger_assault_1028/video';O.mkdir(parents=True,exist_ok=True)
folder=O/time.strftime('%H%M%S');folder.mkdir();errors=[];timeline=[];FF=imageio_ffmpeg.get_ffmpeg_exe()
http.server.SimpleHTTPRequestHandler.protocol_version='HTTP/1.1';http.server.ThreadingHTTPServer.request_queue_size=128
cap=CAPTURE.replace("debugStartFight(entry,{pilot:'cole',record:false});DBGT.god=true;DBGT.speed=1;player.invuln=0;","DBGT.god=true;DBGT.speed=1;player.invuln=0;")
cap=cap.replace('const b=bossActive&&boss&&!boss.dead?boss:null;','const b=subBossActive&&subBoss&&!subBoss.dead?subBoss:null;')
cap=cap.replace('A.tick++;',r'''A.tick++;
 if(elapsed<20||!DC40.events.some(e=>e.event==='twin-turret-burst')){
  for(const k of ['a','d','w','s','j','k','c'])K[k]=false;
  const hx=worldWidth()/2,hy=VH-55;K.a=player.x>hx+5;K.d=player.x<hx-5;K.w=player.y>hy+5;K.s=player.y<hy-5;return;
 }
''')
cap=cap.replace('COLE / INVULNERABLE INPUT BOT / NATIVE HP & PHASES','DREDGER / INVULNERABLE INPUT BOT / NATIVE HP & ATTACK BOOK')
port,stop=serve(str(R))
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required','--disable-background-timer-throttling','--disable-renderer-backgrounding']);p=boot(br.new_context(viewport={'width':1280,'height':800}),port,7,errors,'mini')
  p.on('response',lambda r:errors.append('HTTP '+str(r.status)+' '+r.url.split('/')[-1])if r.status>=400 else None)
  p.wait_for_function('()=>Object.values(DC40_ART).every(a=>XART.rdy(a.key))',timeout=180000)
  initial=p.evaluate("()=>{const M=s7mInit(subBoss);return{hp:subBoss.hp,maxhp:subBoss.maxhp,mode:M.mode,weapon:run.weapon,level:run.wlevel};}")
  with(folder/'capture.webm').open('wb')as raw:
   p.expose_function('saveCaptureChunk',lambda b:raw.write(base64.b64decode(b)))
   p.evaluate('()=>{window.requestAnimationFrame=window.__bofRealRAF;last=performance.now();requestAnimationFrame(loop);}')
   p.evaluate(cap,{'stage':7});print('RECORD native Furious Dredger life',flush=True)
   ended=None
   while True:
    p.wait_for_timeout(450);q=p.evaluate("()=>{const b=subBoss,M=b?._s7mod;return{seconds:(performance.now()-captureStart)/1000,hp:b?.hp,maxhp:b?.maxhp,dead:b?.dead,mode:M?.mode,phase:M?.dc40?.phase,x:b?.x,y:b?.y,clock:M?.clock,track:M?.dc40Track,guns:M?.parts.map(p=>({id:p.id,hp:p.hp})),frames:captureStats.frames,audio:captureStats.peak,done:subBossDone,state};}");timeline.append(q)
    if q['done']and ended is None:ended=q['seconds']
    if ended is not None and q['seconds']-ended>2.2 or q['seconds']>220 or errors:break
    if len(timeline)%20==0:print(json.dumps(q),flush=True)
   sound=p.evaluate("async()=>{reviewBot.enabled=false;for(const k of ['a','d','w','s','j','c'])Input.keys[k]=false;await new Promise(r=>{reviewRecorder.onstop=r;reviewRecorder.stop();});await capturePending;captureLive=false;return captureStats;}")
   events=p.evaluate('DC40.events');bot=p.evaluate('reviewBot');p.screenshot(path=str(folder/'final.png'))
  br.close()
finally:stop()
video=folder/'dredger-furious.mp4'
subprocess.run([FF,'-v','error','-y','-threads','2','-i',str(folder/'capture.webm'),'-vf','fps=30','-c:v','libx264','-preset','fast','-crf','20','-c:a','aac','-b:a','160k','-pix_fmt','yuv420p','-movflags','+faststart',str(video)],check=True)
dec=subprocess.run([FF,'-hide_banner','-nostats','-threads','2','-i',str(video),'-af','volumedetect','-f','null','-'],capture_output=True,text=True);(folder/'decode.log').write_text(dec.stderr,encoding='utf8');pk=re.search(r'max_volume: ([\-\d.inf]+) dB',dec.stderr);peak=float(pk[1])if pk else-999
for i,at in enumerate([.2,5,8,11,15,20,25,32,40,50]):
 if at<timeline[-1]['seconds']:subprocess.run([FF,'-v','error','-y','-ss',str(at),'-i',str(video),'-frames:v','1',str(folder/f'decoded-{i}.png')],check=True)
names={e['event']for e in events};modes=sorted({q['mode']for q in timeline if q['mode']})
checks=dict(noErrors=not errors and not bot['errors']and not sound['tapErrors'],audible=peak>-60,unclipped=peak<0,fullDecode=dec.returncode==0,realTime=sound['frames']/timeline[-1]['seconds']>45,nativeDefeat=ended is not None,entireGunBudget=any(q['mode']=='dead'and all(p['hp']==0 for p in q['guns'])for q in timeline),ram='ram-release'in names,reverse='reverse-start'in names,opening='mid-screen-opening'in names,twins='twin-turret-burst'in names,topBarrage='top-cannon-wave'in names)
report=dict(video=video.relative_to(R).as_posix(),method=__doc__,initial=initial,timeline=timeline,sound=sound,events=events,errors=errors,bot=bot,modes=modes,decodedPeakDb=peak,checks=checks)
(folder/'report.json').write_text(json.dumps(report,indent=2),encoding='utf8');(O/'latest.json').write_text(json.dumps({'folder':folder.relative_to(R).as_posix()},indent=2),encoding='utf8')
print(json.dumps(dict(video=str(video),checks=checks,modes=modes)),flush=True)
raise SystemExit(0 if all(checks.values())else 1)
