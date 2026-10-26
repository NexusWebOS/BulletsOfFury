"""Short audible checkpoints reached by native simulation; no HP/phase writes.
Each checkpoint then runs at real speed with an explicitly invulnerable input bot.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
from shoot import serve,TRAP_RAF,STEP
from record_furious_789_1025 import CAPTURE
import argparse,base64,json,subprocess,time,re,http.server
import imageio_ffmpeg

R=Path(__file__).resolve().parents[1];O=R/'_shots/bullethell_1025/video';O.mkdir(parents=True,exist_ok=True)
FF=imageio_ffmpeg.get_ffmpeg_exe()
cap=CAPTURE.replace("const entry=debugFightFor(cfg.stage,'boss');","const entry=debugFightFor(cfg.stage,cfg.role);")
cap=cap.replace("debugStartFight(entry,{pilot:'cole',record:false});DBGT.god=true;DBGT.speed=1;player.invuln=0;","DBGT.god=true;DBGT.speed=1;player.invuln=0;")
cap=cap.replace("A.tick++;","""A.tick++;
  if(cfg.checkpoint){const b=cfg.role==='mini'?subBoss:boss,P=b?._bh25;
   for(const k of ['a','d','w','s','j','k','c'])K[k]=false;
   const tx=(P?.escapeX??worldWidth()/2)+Math.sin(elapsed*.58)*48,ty=VH-65;
   K.a=player.x>tx+5;K.d=player.x<tx-5;K.w=player.y>ty+5;K.s=player.y<ty-5;return;}
""")
cap=cap.replace("' / FURIOUS / COLE / INVULNERABLE INPUT BOT / NATIVE HP & PHASES / '","' / FURIOUS / NATIVE CHECKPOINT / INVULNERABLE DODGE BOT / '")
snap="""()=>{const b=bhActor,P=b._bh25;return{seconds:(performance.now()-captureStart)/1000,stage:run.stage,hp:b.hp,kind:P?.kind,phase:P?.phase,wave:P?.wave,live:eBullets.filter(q=>q._bh25Owner===b&&!q.dead).length,events:BH25.events.filter(e=>e.event==='section-complete').length,frames:captureStats.frames,audioPeak:captureStats.peak,godBlocks:DBGT.stats?.godBlocks||0};}"""
parser=argparse.ArgumentParser();parser.add_argument('--fights',default=','.join(f'{n}-mini'for n in range(1,10))+',7-boss,8-boss');args=parser.parse_args()
http.server.SimpleHTTPRequestHandler.protocol_version='HTTP/1.1'
http.server.ThreadingHTTPServer.request_queue_size=128
port,stop=serve(str(R));reports=[]
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required','--disable-background-timer-throttling','--disable-renderer-backgrounding'])
  browser_context=br.new_context(viewport={'width':1280,'height':800})
  for token in args.fights.split(','):
   a,role=token.split('-');stage=int(a);native_role='boss'if role=='final'else role;folder=O/token
   if folder.exists():folder=O/(token+'-'+time.strftime('%H%M%S'))
   folder.mkdir();errors=[];timeline=[];p=browser_context.new_page()
   p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text+' '+json.dumps(m.location))if m.type=='error'or'draw error'in m.text else None)
   p.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5&&typeof BH25!=="undefined"',timeout=180000);p.mouse.click(3,3);p.evaluate(TRAP_RAF)
   p.evaluate("""([stage,role])=>{debugUnlocked=true;diffKey='furious';debugStartFight(debugFightFor(stage,role),{pilot:'cole'});if(role==='mini')spawnSubBoss(debugFightFor(stage,role).kind);else spawnBoss(debugFightFor(stage,role).kind);debugFight.spawned=true;warnT=0;DBGT.god=true;DBGT.speed=1;player.x=worldWidth()/2;player.y=VH-65;BOFCinematicDirector.cancel();setState(GS.PLAY);for(const k of Object.keys(Input.keys))Input.keys[k]=false;BH25.events=[];window.bhActor=role==='mini'?subBoss:boss;}""",[stage,native_role])
   p.wait_for_function('(n)=>{stageLoadTick();return stageLoadReady(n)}',arg=stage,timeout=180000)
   if stage==6:p.wait_for_function('()=>{sc13Warm();return SC13.keys.every(k=>XART.rdy(k))}',timeout=180000)
   if role=='final':p.evaluate("()=>{v18Enter(boss,2,0);boss._r30.v18.arenaPhase=2;v18Fight(boss);boss.enter=false;boss._noHit=false;BOFCinematicDirector.cancel();}")
   found=False
   for batch in range(2400):
    p.evaluate(STEP,5)
    if p.evaluate('!!bhActor._bh25'):
     found=True;break
    if batch%12==0:p.wait_for_timeout(1)
   if not found:raise RuntimeError('Native checkpoint not reached '+token)
   initial=p.evaluate('({nativeTime:efxClock,hp:bhActor.hp,maxhp:bhActor.maxhp,kind:bhActor._bh25.kind,events:BH25.events})')
   with(folder/'capture.webm').open('wb')as raw:
    p.expose_function('saveCaptureChunk',lambda b:raw.write(base64.b64decode(b)))
    p.evaluate('()=>{window.requestAnimationFrame=window.__bofRealRAF;last=performance.now();requestAnimationFrame(loop);}')
    use_cap=cap.replace('NATIVE CHECKPOINT','FINAL FORM FIXTURE')if role=='final'else cap
    p.evaluate(use_cap,{'stage':stage,'role':native_role,'checkpoint':True})
    print('RECORD',token,initial['kind'],flush=True)
    while True:
     p.wait_for_timeout(250);q=p.evaluate(snap);timeline.append(q)
     if errors or q['seconds']>22 or q['events']and q['seconds']>12:break
    sound=p.evaluate("""async()=>{reviewBot.enabled=false;for(const k of ['a','d','w','s','j','c'])Input.keys[k]=false;await new Promise(r=>{reviewRecorder.onstop=r;reviewRecorder.stop();});await capturePending;captureLive=false;return captureStats;}""")
    p.screenshot(path=str(folder/'final.png'))
   events=p.evaluate('BH25.events');p.close()
   mp4=folder/'barrage.mp4'
   subprocess.run([FF,'-v','error','-y','-threads','2','-i',str(folder/'capture.webm'),'-vf','fps=30','-c:v','libx264','-preset','fast','-crf','20','-c:a','aac','-b:a','160k','-pix_fmt','yuv420p','-movflags','+faststart',str(mp4)],check=True)
   dec=subprocess.run([FF,'-hide_banner','-nostats','-threads','2','-i',str(mp4),'-af','volumedetect','-f','null','-'],capture_output=True,text=True);(folder/'decode.log').write_text(dec.stderr,encoding='utf8')
   pk=re.search(r'max_volume: ([\-\d.inf]+) dB',dec.stderr);peak=float(pk[1])if pk else-999
   for index,at in enumerate([.7,2.3,3.8,5.3,7.0,9.5]):subprocess.run([FF,'-v','error','-y','-threads','2','-ss',str(at),'-i',str(mp4),'-frames:v','1',str(folder/f'decoded-{index}.png')],check=True)
   method='Native final-form fixture selected with v18Enter; native HP retained, real-time invulnerable input bot.'if role=='final'else __doc__
   report=dict(stage=stage,role=role,kind=initial['kind'],video=mp4.relative_to(R).as_posix(),method=method,initial=initial,timeline=timeline,events=events,sound=sound,errors=errors,decodedPeakDb=peak,checks=dict(nativeSectionComplete=any(e['event']=='section-complete'for e in events),noErrors=not errors,fullDecode=dec.returncode==0,audible=peak>-60,realTimeFrames=sound['frames']/timeline[-1]['seconds']>45))
   (folder/'report.json').write_text(json.dumps(report,indent=2),encoding='utf8');reports.append(report)
   print('DONE',token,json.dumps(report['checks']),flush=True)
  br.close()
finally:
 stop();(O/'recordings.json').write_text(json.dumps(reports,indent=2),encoding='utf8')
raise SystemExit(0 if all(all(r['checks'].values())for r in reports)else 1)
