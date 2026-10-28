"""Audible native Dracodia rebirth checkpoint, including all lightning and reveal.

Native damage starts the checkpoint; no animation timers or phases are skipped.
"""
from barrage_review_common_1025 import ROOT,boot,advance
from shoot import serve
from record_furious_789_1025 import CAPTURE
from playwright.sync_api import sync_playwright
from PIL import Image,ImageDraw
from pathlib import Path
from uuid import uuid4
import json,base64,subprocess,re,argparse
import imageio_ffmpeg

ap=argparse.ArgumentParser();ap.add_argument('--depth',action='store_true');ap.add_argument('--climax',action='store_true');ap.add_argument('--strikes',action='store_true');ap.add_argument('--polish',action='store_true');ap.add_argument('--dna',action='store_true');ap.add_argument('--palette',action='store_true');args=ap.parse_args();args.dna=args.dna or args.palette;args.polish=args.polish or args.dna;args.strikes=args.strikes or args.polish;args.climax=args.climax or args.strikes;args.depth=args.depth or args.climax
OUT=ROOT/('_shots/dracodia_palette_1026/video'if args.palette else'_shots/dracodia_dna_1026/video'if args.dna else'_shots/dracodia_polish_1026/video'if args.polish else'_shots/dracodia_strikes_1026/video'if args.strikes else'_shots/dracodia_climax_1026/video'if args.climax else'_shots/dracodia_depth_1026/video'if args.depth else'_shots/dracodia_transformation_1025')/('take-'+uuid4().hex[:8]);OUT.mkdir(parents=True,exist_ok=True)
FF=imageio_ffmpeg.get_ffmpeg_exe();errors=[];assets=[];timeline=[]
cap=CAPTURE.replace("debugStartFight(entry,{pilot:'cole',record:false});DBGT.god=true;DBGT.speed=1;player.invuln=0;","DBGT.god=true;DBGT.speed=1;player.invuln=0;")
cap=cap.replace('A.tick++;',"A.tick++;for(const key of ['a','d','w','s','j','k','c'])K[key]=false;return;")
cap=cap.replace('INVULNERABLE INPUT BOT / NATIVE HP & PHASES','TRANSFORMATION CHECKPOINT / NATIVE ANIMATION & AUDIO')
snap="""()=>{const S=boss._r30,R=S.v18.rb23Rebirth,F=typeof RD26==='undefined'?null:RD26.fx;return{seconds:(performance.now()-captureStart)/1000,nativeTime:efxClock,sceneTime:S.t,mode:S.mode,encounter:j3State(boss).encounter,bolts:R?.bolts,download:S78.downloadLast,dna:typeof RD28==='undefined'?null:RD28.last,intro:typeof RD27==='undefined'?null:RD27.intro,effects:F?{front:F.front.length,back:F.back.length,strikes:F.strikes.length,clock:F.clock,ambientLanes:F.strikes.filter(s=>s.kind==='ambient').map(s=>s.lane)}:null,events:RB23.events.length,frames:captureStats.frames};}"""
port,stop=serve(str(ROOT))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required','--disable-background-timer-throttling','--disable-renderer-backgrounding']);bc=br.new_context(viewport={'width':1280,'height':800})
  p=boot(bc,port,8,errors,'boss');p.on('response',lambda r:assets.append(str(r.status)+' '+r.url)if r.status>=400 else None)
  p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(8)&&v18Warm()&&bi24Warm()&&r25Warm(8)}',timeout=180000)
  if not advance(p,"boss._r30.mode==='fight'&&j3State(boss).encounter===0",1000,12):raise RuntimeError('Native first-host checkpoint was not reached')
  p.evaluate('RB23.events=[];S78.events=[]')
  fixture=False;armStage=0
  with(OUT/'capture.webm').open('wb') as raw:
   p.expose_function('saveCaptureChunk',lambda data:raw.write(base64.b64decode(data)))
   p.evaluate('()=>{window.requestAnimationFrame=window.__bofRealRAF;last=performance.now();requestAnimationFrame(loop);}')
   p.evaluate(cap,{'stage':8});print('RECORD Dracodia full lightning transformation',flush=True)
   while True:
    p.wait_for_timeout(200);q=p.evaluate(snap);timeline.append(q)
    if args.polish and armStage<2 and q['seconds']>=(1.2 if armStage==0 else 2.4):
     p.evaluate("""(id)=>{const p=boss.parts.find(p=>p.id===id);boss._lastPart=p;modularHit(p.hp+1);}""",'left'if armStage==0 else'right');armStage+=1
    if not fixture and q['seconds']>=(2.8 if args.polish else 1.2):
     fixture=p.evaluate("""()=>{for(const p of boss.parts.filter(p=>p.id!=='core')){boss._lastPart=p;modularHit(p.hp+1);}const p=boss.parts.find(p=>p.id==='core');boss._lastPart=p;modularHit(p.hp+1);return boss._r30.mode==='dr5er23rebirth';}""")
     if not fixture:raise RuntimeError('Native damage failed to start rebirth')
     print('Native rebirth started',flush=True)
    if (not args.polish and q['seconds']>=36)or(args.polish and q['seconds']>36 and q['mode']=='fight')or q['seconds']>=125 or errors:break
   sound=p.evaluate("""async()=>{reviewBot.enabled=false;for(const k of ['a','d','w','s','j','c'])Input.keys[k]=false;await new Promise(r=>{reviewRecorder.onstop=r;reviewRecorder.stop();});await capturePending;captureLive=false;return captureStats;}""")
   p.screenshot(path=str(OUT/'final.png'))
  events=p.evaluate('({rebirth:RB23.events,review:S78.events,polish:typeof RD27===\"undefined\"?null:RD27.audio,speech:DR5.events})');br.close()
finally:stop()
mp4=OUT/'dracodia-final-transformation.mp4'
subprocess.run([FF,'-v','error','-y','-threads','2','-i',str(OUT/'capture.webm'),'-vf','fps=30','-c:v','libx264','-preset','fast','-crf','19','-c:a','aac','-b:a','160k','-pix_fmt','yuv420p','-movflags','+faststart',str(mp4)],check=True)
dec=subprocess.run([FF,'-hide_banner','-nostats','-threads','2','-i',str(mp4),'-af','volumedetect','-f','null','-'],capture_output=True,text=True);(OUT/'decode.log').write_text(dec.stderr,encoding='utf8')
peak=re.search(r'max_volume: ([\-\d.inf]+) dB',dec.stderr);db=float(peak[1])if peak else-999
fall=next(q['seconds']-q['sceneTime']for q in timeline if q['mode']=='dr5er23rebirth')
chapters={'collapse':fall,'symbiote':fall+10.6,'download':fall+14.5,'lightning':fall+14.02,'storm':fall+24.1,'complete':fall+25.22,'reveal':fall+29.6}
if args.climax:chapters.update({'complete':fall+25.22,'peak-flash':fall+25.75,'clearing-light':fall+27.2})
if args.polish:
 chapters.update({'left-arm-break':1.45,'right-arm-break':2.65})
 roar=next(e for e in events['speech']if e['event']=='dracodiaShriek')
 chapters['closing-roar']=next((q['seconds']for q in timeline if q['mode']=='dr5Monologue'and q['sceneTime']>=roar['t']+1.5),timeline[-1]['seconds']-1)
if args.dna:chapters.update({'code-first-rises':fall+6.5,'dna-forms-skeleton':fall+11.5,'code-converges':fall+14.6})
shots=[]
for label,at in chapters.items():
 f=OUT/(label+'.png');subprocess.run([FF,'-v','error','-y','-threads','2','-ss',str(at),'-i',str(mp4),'-frames:v','1',str(f)],check=True);shots.append((label,f))
checks={'noPageOrConsoleErrors':not errors,'noAssetErrors':not assets,'fullDecode':dec.returncode==0,'audible':db>-60,'realTimeFrames':sound['frames']/timeline[-1]['seconds']>45,
 'nativeDamageStartsCheckpoint':fixture,'all24LightningBeats':sum(e['event']=='corrupted-lightning'for e in events['rebirth'])==24,
 'downloadCompletes':any(q.get('download',{}).get('progress',0)>=1 for q in timeline if q.get('download')),
 'finalArenaRevealed':any(q['encounter']==2 and q['mode']=='dr5Monologue'for q in timeline),
 'nativeLightningAudioPlayed':all(sound['playing'].get(k,0)>0 for k in ['rd27Lightning','bossWeaponCharge','expBig']),
 'nativeFinalBodyDownloaded':any(q.get('download',{}).get('source')=='native-colossus'for q in timeline if q.get('download')),
 'downloadEnergyReplacesTeleportCue':sound['playing'].get('combatEnergy0927',0)>0 and not sound['playing'].get('teleportIn',0)}
if args.depth:
 active=[q for q in timeline if q['mode']=='dr5er23rebirth'and 23.5<q['sceneTime']<25.2]
 checks.update({'actualDepthPoses':len({q['download']['depthFrame']for q in timeline if q['mode']=='dr5er23rebirth'and 18<q['sceneTime']<25.2})>=6,'uprightFormingBody':all(q['download']['angle']==0 for q in active),
  'swirlAndDownwardStrikes':all(q['effects']['front']>0 and q['effects']['back']>0 and q['effects']['strikes']>0 for q in active)})
if args.climax:
 active=[q['download']for q in timeline if q['mode']=='dr5er23rebirth'and 14.05<q['sceneTime']<25.6]
 checks.update({'acceleratingUntilFlash':all(z['rotationRate']>a['rotationRate']and z['rotationTurns']>a['rotationTurns']for a,z in zip(active,active[1:])),
  'noFullBodyBeforeFlash':all(not q['fullForm']and q['nativeBlend']==0 and q['materialProgress']<1 for q in active),
  'fullBodyAfterPeakFlash':any(q['download']['fullForm']for q in timeline if q['mode']=='dr5er23rebirth'and 25.6<q['sceneTime']<28.5),
  'strikesAcrossScreen':len({lane for q in timeline if q.get('effects')for lane in q['effects'].get('ambientLanes',[])})>=8})
if args.strikes:
 late=[q['effects']['clock']for q in timeline if q['mode']=='dr5er23rebirth'and 23<q['sceneTime']<25.6 and q['effects'].get('clock')]
 checks.update({'strikeCadenceAcceleratesIndependently':len(late)>4 and all(z['rate']>a['rate']for a,z in zip(late,late[1:]))and late[-1]['rate']>19,
  'spiralBuildsFromDownloadStart':any(q['effects']['front']+q['effects']['back']>0 for q in timeline if q['mode']=='dr5er23rebirth'and 14<=q['sceneTime']<15)})
if args.polish:
 audio=events['polish'];gains=[q['strength']for q in audio];intro=[q['intro']for q in timeline if q.get('intro')and 7<q['sceneTime']<14]
 checks.update({'formationThunderStrengthBuilds':len(gains)>50 and all(z>a for a,z in zip(gains,gains[1:])),
  'everyStrikeMixerReleaseAccepted':all(q['played']for q in audio),
  'steppedSkeletonVisibility':min(q['alpha']for q in intro)==.25 and max(q['alpha']for q in intro)==1 and len({q['frame']for q in intro})>=20,
  'singleClosingRoar':len([e for e in events['speech']if e['event']=='dracodiaShriek'])==1 and timeline[-1]['mode']=='fight'})
if args.dna:
 forming=[q['dna']for q in timeline if q.get('dna')and 8<q['sceneTime']<13.5]
 handoff=[q['dna']for q in timeline if q.get('dna')and 14<q['sceneTime']<15.8]
 checks.update({'livingCodeDuringColesReaction':any(q.get('dna')for q in timeline if 6.4<q['sceneTime']<7),
  'doubleHelixAndFluidLobes':bool(forming)and all(q['front']>10 and q['back']>10 and q['rungs']==9 and len(q['blobs'])==14 for q in forming),
  'codeInsideSkeletalSilhouette':any(q['skin']>.08 for q in forming),
  'codeConvergesIntoDownload':bool(handoff)and handoff[-1]['absorb']>.85 and handoff[-1]['alpha']<.15,
  'codeClearsAfterItsConvergence':all(q.get('dna')is None for q in timeline if q['mode']=='dr5er23rebirth'and q['sceneTime']>=16)})
report={'video':mp4.relative_to(ROOT).as_posix(),'timeline':timeline,'events':events,'sound':sound,'decodedPeakDb':db,'checks':checks,'errors':errors,'assetErrors':assets,'chapters':chapters,'method':__doc__}
(OUT/'report.json').write_text(json.dumps(report,indent=2),encoding='utf8');(OUT.parent/'latest.json').write_text(json.dumps({'folder':str(OUT),'report':str(OUT/'report.json')},indent=2),encoding='utf8')
im=Image.new('RGB',(1280,((len(shots)+2)//3)*285),(5,10,17));g=ImageDraw.Draw(im)
for i,(label,f)in enumerate(shots):im.paste(Image.open(f).convert('RGB').resize((426,266)),((i%3)*426,(i//3)*285));g.text(((i%3)*426+3,(i//3)*285+266),label,fill='white')
im.save(OUT/'contact.jpg')
print(json.dumps({'checks':checks,'seconds':timeline[-1]['seconds'],'peakDb':db,'folder':str(OUT),'chapters':chapters}),flush=True)
raise SystemExit(0 if all(checks.values())else 1)
