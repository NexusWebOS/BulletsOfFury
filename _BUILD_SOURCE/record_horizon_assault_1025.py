"""Continuous audible Furious Event Horizon review; native HP, phases and inputs."""
from barrage_review_common_1025 import ROOT,boot
from shoot import serve
from record_furious_789_1025 import CAPTURE
from playwright.sync_api import sync_playwright
from pathlib import Path
import json,time,base64,subprocess,re
import imageio_ffmpeg

OUT=ROOT/'_shots/horizon_assault_1025/video'/time.strftime('%H%M%S');OUT.mkdir(parents=True,exist_ok=True)
FF=imageio_ffmpeg.get_ffmpeg_exe();errors=[];assets=[];timeline=[]
cap=CAPTURE.replace("const entry=debugFightFor(cfg.stage,'boss');","const entry=debugFightFor(cfg.stage,'mini');")
cap=cap.replace("debugStartFight(entry,{pilot:'cole',record:false});DBGT.god=true;DBGT.speed=1;player.invuln=0;","DBGT.god=true;DBGT.speed=1;player.invuln=0;")
cap=cap.replace('A.tick++;',"""A.tick++;
 for(const key of ['a','d','w','s','j','k','c'])K[key]=false;
 const targetX=(subBoss?._bh25?.escapeX??worldWidth()/2)+Math.sin(elapsed*.55)*40,targetY=VH-65;
 K.a=player.x>targetX+5;K.d=player.x<targetX-5;K.w=player.y>targetY+5;K.s=player.y<targetY-5;return;
""").replace('INVULNERABLE INPUT BOT / NATIVE HP & PHASES','NATIVE HP / INVULNERABLE DODGE BOT')
snap="""()=>{const b=reviewActor,H=b._eh25,Q=b._s9rift.s5924;return{seconds:(performance.now()-captureStart)/1000,nativeTime:efxClock,hp:b.hp,maxhp:b.maxhp,dead:b.dead,mode:Q.mode,x:b.x,y:b.y,eye:s5924Eye(b),spin:H.spin,rps:H.rps,spinning:H.spinning,bomb:H.bomb?.phase,barrage:b._bh25?.kind,events:EH25.events,frames:captureStats.frames};}"""
port,stop=serve(str(ROOT))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required','--disable-background-timer-throttling','--disable-renderer-backgrounding']);bc=br.new_context(viewport={'width':1280,'height':800})
  p=boot(bc,port,9,errors);p.on('response',lambda r:assets.append(str(r.status)+' '+r.url)if r.status>=400 else None)
  p.wait_for_function('()=>s5924Ready("black_spin")&&s5924Ready("black_charge")&&XART.rdy("bf22_water_orb")',timeout=180000)
  p.evaluate('EH25.events=[]');initial=p.evaluate('({hp:reviewActor.hp,maxhp:reviewActor.maxhp,time:efxClock})')
  with(OUT/'capture.webm').open('wb') as raw:
   p.expose_function('saveCaptureChunk',lambda data:raw.write(base64.b64decode(data)))
   p.evaluate('()=>{window.requestAnimationFrame=window.__bofRealRAF;last=performance.now();requestAnimationFrame(loop);}')
   p.evaluate(cap,{'stage':9});print('RECORD Event Horizon',flush=True)
   while True:
    p.wait_for_timeout(250);q=p.evaluate(snap);timeline.append(q)
    if q['seconds']>=45 or errors:break
   sound=p.evaluate("""async()=>{reviewBot.enabled=false;for(const k of ['a','d','w','s','j','c'])Input.keys[k]=false;await new Promise(r=>{reviewRecorder.onstop=r;reviewRecorder.stop();});await capturePending;captureLive=false;return captureStats;}""")
   p.screenshot(path=str(OUT/'final.png'))
  events=p.evaluate('EH25.events');br.close()
finally:stop()
mp4=OUT/'event-horizon-furious.mp4'
subprocess.run([FF,'-v','error','-y','-threads','2','-i',str(OUT/'capture.webm'),'-vf','fps=30','-c:v','libx264','-preset','fast','-crf','20','-c:a','aac','-b:a','160k','-pix_fmt','yuv420p','-movflags','+faststart',str(mp4)],check=True)
dec=subprocess.run([FF,'-hide_banner','-nostats','-threads','2','-i',str(mp4),'-af','volumedetect','-f','null','-'],capture_output=True,text=True);(OUT/'decode.log').write_text(dec.stderr,encoding='utf8')
peak=re.search(r'max_volume: ([\-\d.inf]+) dB',dec.stderr);db=float(peak[1])if peak else-999
for i,at in enumerate([2.4,4.0,8.9,10.1,15.3,20.0,28,30.5,40]):subprocess.run([FF,'-v','error','-y','-threads','2','-ss',str(at),'-i',str(mp4),'-frames:v','1',str(OUT/f'decoded-{i}.png')],check=True)
checks={'noPageOrConsoleErrors':not errors,'noAssetErrors':not assets,'fullDecode':dec.returncode==0,'audible':db>-60,'realTimeFrames':sound['frames']/timeline[-1]['seconds']>45,
 'nativeHpUnchanged':all(q['hp']==initial['hp']for q in timeline),'twoCompleteEnergyBombs':sum(e['event']=='bomb-complete'for e in events)>=2,'verticalFlight':max(q['y']for q in timeline)-min(q['y']for q in timeline if q['seconds']>2)>100,
 'eyeChargeLaunchAndImpactAudible':all(sound['playing'].get(k,0)>0 for k in ['bossWeaponCharge','combatOrb0927','warpBurst'])}
report={'video':mp4.relative_to(ROOT).as_posix(),'initial':initial,'timeline':timeline,'events':events,'sound':sound,'decodedPeakDb':db,'checks':checks,'errors':errors,'assetErrors':assets,'method':__doc__+' Only player damage is ignored; weapons are withheld for the full demonstration.'}
(OUT/'report.json').write_text(json.dumps(report,indent=2),encoding='utf8');(OUT.parent/'latest.json').write_text(json.dumps({'folder':str(OUT),'report':str(OUT/'report.json')},indent=2),encoding='utf8')
print(json.dumps({'checks':checks,'seconds':timeline[-1]['seconds'],'peakDb':db,'folder':str(OUT)}),flush=True)
raise SystemExit(0 if all(checks.values())else 1)
