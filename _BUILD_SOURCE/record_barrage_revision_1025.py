"""Audible, real-time native checkpoints. No enemy HP or phase writes.

The player uses GOD and native movement only; Stage6 companions fight normally.
"""
from barrage_review_common_1025 import ROOT,OUT,boot,advance
from record_furious_789_1025 import CAPTURE
from shoot import serve,STEP
from playwright.sync_api import sync_playwright
from PIL import Image,ImageDraw
import argparse,time,json,base64,subprocess,re
import imageio_ffmpeg

FF=imageio_ffmpeg.get_ffmpeg_exe();folder=OUT/'video';folder.mkdir(exist_ok=True)
CASES={
 'frost':(3,"reviewActor._bh25?.kind==='frost'",14),
 'battery':(6,"reviewActor._cargo13.ready&&reviewActor._cargo13.mode==='batteries'&&!sc13Open(reviewActor)",14),
 'reactor':(6,"reviewActor._bh25?.kind==='fortress'",15),
 'turrets':(7,"reviewActor._bh25?.kind==='dredger'&&!reviewActor._bh25.dorsal",15),
 'dorsal':(7,"!!reviewActor._bh25?.dorsal",17),
 'herald':(8,"reviewActor._bh25?.kind==='herald'",52)}
cap=CAPTURE.replace("const entry=debugFightFor(cfg.stage,'boss');","const entry=debugFightFor(cfg.stage,'mini');")
cap=cap.replace("debugStartFight(entry,{pilot:'cole',record:false});DBGT.god=true;DBGT.speed=1;player.invuln=0;","DBGT.god=true;DBGT.speed=1;player.invuln=0;")
cap=cap.replace('A.tick++;',"""A.tick++;
  for(const key of ['a','d','w','s','j','k','c'])K[key]=false;
  const checkpointActor=subBoss,P=checkpointActor?._bh25,Q=checkpointActor?._hd1003?._hb25;
  const dodgeX=Math.max(camLeftX()+50,Math.min(camRightX()-50,(P?.escapeX??Q?.escapeX??worldWidth()/2)+Math.sin(elapsed*.60)*34)),dodgeY=VH-66;
  K.a=player.x>dodgeX+5;K.d=player.x<dodgeX-5;K.w=player.y>dodgeY+5;K.s=player.y<dodgeY-5;
  return;
""")
cap=cap.replace('INVULNERABLE INPUT BOT / NATIVE HP & PHASES','NATIVE CHECKPOINT / INVULNERABLE DODGE BOT')
SNAP="""()=>{const b=reviewActor,P=b._bh25,Q=b._hd1003?._hb25;return{seconds:(performance.now()-captureStart)/1000,nativeTime:efxClock,state,hp:b.hp,dead:b.dead,kind:P?.kind,phase:P?.phase,wave:P?.wave,dorsal:!!P?.dorsal,flight:Q?{kind:Q.kind,phase:Q.phase,pass:Q.pass}:null,coreOpen:b._cargo13?sc13Open(b):null,gunCount:b._cargo13?.guns.filter(g=>!g.dead).length,live:eBullets.filter(q=>!q.dead&&(q._bh25Owner===b||q._heraldOwner1003===b)).length,events:HB25.events,sections:BH25.events.filter(e=>e.event==='section-complete').length,frames:captureStats.frames,audioPeak:captureStats.peak};}"""
ap=argparse.ArgumentParser();ap.add_argument('--cases',default=','.join(CASES));args=ap.parse_args()
port,stop=serve(str(ROOT));reports=[]
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required','--disable-background-timer-throttling','--disable-renderer-backgrounding']);bc=br.new_context(viewport={'width':1280,'height':800})
  for key in args.cases.split(','):
   stage,expression,seconds=CASES[key];take=folder/(key+'-'+time.strftime('%H%M%S'));take.mkdir();errors=[];assets=[];timeline=[]
   p=boot(bc,port,stage,errors);p.on('response',lambda r:assets.append(str(r.status)+' '+r.url)if r.status>=400 else None)
   if not advance(p,expression,3200 if stage==6 else 1200,5):raise RuntimeError('Native checkpoint not reached: '+key)
   initial=p.evaluate('({hp:reviewActor.hp,maxhp:reviewActor.maxhp,nativeTime:efxClock,state,events:BH25.events})')
   p.evaluate('HB25.events=[]')
   with(take/'capture.webm').open('wb') as raw:
    p.expose_function('saveCaptureChunk',lambda data:raw.write(base64.b64decode(data)))
    p.evaluate('()=>{window.requestAnimationFrame=window.__bofRealRAF;last=performance.now();requestAnimationFrame(loop);}')
    p.evaluate(cap,{'stage':stage})
    print('RECORD '+key,flush=True)
    while True:
     p.wait_for_timeout(250);q=p.evaluate(SNAP);timeline.append(q)
     if q['seconds']>=seconds or errors:break
    sound=p.evaluate("""async()=>{reviewBot.enabled=false;for(const k of ['a','d','w','s','j','c'])Input.keys[k]=false;await new Promise(r=>{reviewRecorder.onstop=r;reviewRecorder.stop();});await capturePending;captureLive=false;return captureStats;}""")
    p.screenshot(path=str(take/'final.png'))
   events=p.evaluate('({barrage:BH25.events,herald:HB25.events})');p.close()
   mp4=take/(key+'.mp4')
   subprocess.run([FF,'-v','error','-y','-threads','2','-i',str(take/'capture.webm'),'-vf','fps=30','-c:v','libx264','-preset','fast','-crf','20','-c:a','aac','-b:a','160k','-pix_fmt','yuv420p','-movflags','+faststart',str(mp4)],check=True)
   dec=subprocess.run([FF,'-hide_banner','-nostats','-threads','2','-i',str(mp4),'-af','volumedetect','-f','null','-'],capture_output=True,text=True);(take/'decode.log').write_text(dec.stderr,encoding='utf8')
   peak=re.search(r'max_volume: ([\-\d.inf]+) dB',dec.stderr);db=float(peak[1])if peak else-999
   for i,at in enumerate([.7,2.4,4.0,6,9,min(seconds-1,12)]):subprocess.run([FF,'-v','error','-y','-threads','2','-ss',str(at),'-i',str(mp4),'-frames:v','1',str(take/f'decoded-{i}.png')],check=True)
   complete=any(e['event']=='flight-complete'and e.get('kind')=='bomber'for e in events['herald'])if key=='herald'else True
   checks={'noPageOrConsoleErrors':not errors,'noAssetErrors':not assets,'fullDecode':dec.returncode==0,'audible':db>-60,'realTimeFrames':sound['frames']/timeline[-1]['seconds']>45,'requestedCheckpoint':initial['hp']>0,'completeBomber':complete}
   if key=='battery':checks['noBatteryBulletHell']=not any(q['kind']=='fortress' and q['gunCount']>0 for q in timeline if q.get('kind'))
   if key=='reactor':checks['reactorOnly']=all(q['gunCount']==0 for q in timeline if q.get('kind')=='fortress')
   report={'case':key,'stage':stage,'video':mp4.relative_to(ROOT).as_posix(),'method':__doc__,'initial':initial,'timeline':timeline,'events':events,'sound':sound,'decodedPeakDb':db,'errors':errors,'assetErrors':assets,'checks':checks}
   (take/'report.json').write_text(json.dumps(report,indent=2),encoding='utf8');reports.append(report)
   print('DONE '+key+' '+json.dumps(checks),flush=True)
  br.close()
finally:
 stop();(folder/('recordings-'+time.strftime('%H%M%S')+'.json')).write_text(json.dumps(reports,indent=2),encoding='utf8')
raise SystemExit(0 if all(all(q['checks'].values())for q in reports)else 1)
