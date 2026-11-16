from pathlib import Path
from playwright.sync_api import sync_playwright
import sys,json,base64,hashlib
R=Path(__file__).resolve().parents[1];O=R/'_shots/cockpit_castB_1115';F=O/'films';F.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
RECORD="""async part=>{
 const ac=Snd._audioCtx();await ac.resume();const dest=ac.createMediaStreamDestination(),anal=ac.createAnalyser();aq112Bus().output.connect(dest);aq112Bus().output.connect(anal);anal.fftSize=2048;const bins=new Float32Array(2048);
 const out=document.createElement('canvas');out.width=1824;out.height=1024;const g=out.getContext('2d');g.imageSmoothingEnabled=false;const stream=out.captureStream(30);for(const t of dest.stream.getAudioTracks())stream.addTrack(t);
 const rec=new MediaRecorder(stream,{mimeType:'video/webm;codecs=vp8,opus',videoBitsPerSecond:3500000,audioBitsPerSecond:96000}),chunks=[];rec.ondataavailable=e=>{if(e.data.size)chunks.push(e.data)};
 const done=new Promise(resolve=>rec.onstop=()=>{const f=new FileReader();f.onload=()=>resolve(f.result);f.readAsDataURL(new Blob(chunks,{type:'video/webm'}));});
 let start=performance.now(),peak=0,frames=0,prior='',tagAt=0,stages=[],samples=[],seen=new Set(),endAt=null,selected=false,mapChoiceAt=null,faceSamples=[],faceSeen=new Set();
 function layers(){return ['screen','hud-top','hud-bot','equipcv'].map(id=>document.getElementById(id)).filter(Boolean).map(c=>{let opacity=1;for(let p=c;p;p=p.parentElement){const s=getComputedStyle(p);if(s.display==='none'||s.visibility==='hidden')opacity=0;opacity*=Number(s.opacity);}return{c,r:c.getBoundingClientRect(),opacity};}).filter(v=>v.opacity>0&&v.r.width>0&&v.r.height>0);}
 rec.start();await new Promise(resolve=>{const timer=setInterval(()=>{const now=performance.now();loop(now);frames++;const l=layers();g.globalAlpha=1;g.fillStyle='#000';g.fillRect(0,0,1824,1024);
 if(l.length){const x=Math.min(...l.map(v=>v.r.left)),y=Math.min(...l.map(v=>v.r.top)),w=Math.max(...l.map(v=>v.r.right))-x,h=Math.max(...l.map(v=>v.r.bottom))-y,k=Math.min(1824/w,1024/h),ox=(1824-w*k)/2,oy=(1024-h*k)/2;for(const v of l){g.globalAlpha=v.opacity;g.drawImage(v.c,ox+(v.r.left-x)*k,oy+(v.r.top-y)*k,v.r.width*k,v.r.height*k);}g.globalAlpha=1;}
 anal.getFloatTimeDomainData(bins);for(const v of bins)peak=Math.max(peak,Math.abs(v));const r=campaign.stage6Fate;
 const phase=part==='city'&&state===GS.STAGESEL?(CITY16.travel?.done?'stage7-ready':'chibi-flight'):state===GS.STAGESEL&&r?(!r.transitSeen?'transit':!r.messageSeen?'password':!r.awardNotified?'achievement':'choice'):'';
 const tag=state+':'+(BOFCinematicDirector.current?.id||'')+':'+(BOFCinematicDirector.current?.beats[BOFCinematicDirector.current.i]?.id||(BOFCinematicDirector.current?'LINE-'+BOFCinematicDirector.current.i:''))+':'+phase+':'+(s6Wing?.fake?'flyover':s6Wing?.choice?'route-choice':'')+':'+run.stage+':'+(drawLaunch._phase||'');
 const scene=BOFCinematicDirector.current,beat=scene?.beats[scene.i];if(beat&&scene.t>1&&!faceSeen.has(tag)){faceSeen.add(tag);faceSamples.push({tag,who:beat.who,text:beat.text,people:beat.people,locations:beat.fpLocations,faces:(CM3.last?.shot===beat.id?CM3.last.faces:[])?.map(f=>({pilot:f.pilot,key:f.key,family:f.family,artFamily:f.artFamily,assetPath:f.assetPath,assetSha256:f.assetSha256,frame:f.frame,loading:!!f.loading}))});}
 if(tag!==prior){stages.push({tag,at:(now-start)/1000});prior=tag;tagAt=now;}
 if(now-tagAt>750&&!seen.has(tag)){seen.add(tag);samples.push({tag,at:(now-start)/1000,image:out.toDataURL('image/png')});}
 if(part==='split'&&!selected&&s6Wing?.choice&&!BOFCinematicDirector.live&&(s6Wing.frChoice?.t||s6Wing.choiceT)>1.1){selected=true;fr27ChooseRoute(s6Wing,'left');}
 if(part==='city'&&state===GS.STAGESEL&&campaign.cityRescue16?.travelSeen&&!selected){if(mapChoiceAt===null)mapChoiceAt=now;if(now-mapChoiceAt>1400){selected=true;Input.injectTap('enter');}}
 const ended=part==='city'?state===GS.PLAY&&run.stage===7&&!BOFCinematicDirector.live&&!story:part==='split'?selected&&s6Wing?.route==='left'&&!BOFCinematicDirector.live:state===GS.STAGESEL&&r?.awardNotified;
 if(ended&&endAt===null)endAt=now;if(endAt!==null&&now-endAt>(part==='city'?1700:700)||now-start>220000){clearInterval(timer);resolve();}
 },1000/60);});rec.stop();const video=await done;aq112Bus().output.disconnect(dest);aq112Bus().output.disconnect(anal);stream.getTracks().forEach(t=>t.stop());return{video,seconds:(performance.now()-start)/1000,frames,peak,stages,samples,faceSamples};
}"""
core=['assets/game.js','_BUILD_SOURCE/test_fl.js','assets/crossed_fate_1115.js','assets/crossed_fate_art_1115.js','assets/city_rescue_1115.js','assets/city_rescue_art_1115.js','assets/pursuit_trace_art_1115.js','assets/front_pilots_1111.js','assets/cockpit_talk_1114.js','assets/cockpit_talk_art_1114.js','index.html']
report={'source':str(R),'pilot':'cole','difficulty':'furious','scope':'Cole/Furious native city-Harrier completion checkpoint. Scripted native Retina/missile damage exhausts the real Harrier/Nightwing/death/result owners before recording. The full city debrief, Bulletalica reveal, native chibi map flight, native Enter Stage7 selection, Stage7 card, approach, sewer descent and launch play without skipping dialogue. Capture composites visible native playfield/HUD canvases. No unassisted campaign-win claim.','coreBefore':{n:hashlib.sha256((R/n).read_bytes()).hexdigest()for n in core},'clips':[],'errors':[]}
with sync_playwright()as w:
 b=w.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required'])
 for part in ['city']:
  p=b.new_page(viewport={'width':1440,'height':1000});p.set_default_timeout(240000);errors=[]
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None);p.on('response',lambda r:errors.append(str(r.status)+' '+r.url)if r.status>=400 else None)
  p.goto('http://127.0.0.1:8765/index.html?castB-record='+part);p.wait_for_function('window.__bofFrames>6');p.evaluate(shoot.TRAP_RAF)
  p.add_script_tag(content=(R/'_BUILD_SOURCE/balance_lab_1007.js').read_text(encoding='utf8'))
  p.evaluate("part=>{GP4.route=null;GP4.routeReady=false;BAL7.setup({stage:6,kind:part==='rebels'?'rebelsquad':'warhive',pilot:'cole',diff:'furious',mode:'campaign',fire:false});player.invuln=999;campaign.rank={1:'A',2:'A',3:'A',4:'A',5:'A'};campaign.unlockedMax=6;s6WingInit();s6Wing.route=part==='rebels'?'right':'left';s6Wing.fakeDone=true;}",part)
  p.wait_for_function("part=>{stageLoadTick();rg4Warm();return city16Warm()&&fate15Warm()&&stageLoadInfo(6).ready&&(part==='rebels'||fb112Ready())&&ph8Keys(6).every(k=>XART.rdy(k));}",arg=part,polling=50)
  if part=='split':
   p.evaluate("()=>{boss=null;bossActive=false;bossDefeated=false;BOFCinematicDirector.cancel();story=null;AP10_X.intro=null;CA111.active=null;CA111.completed=new Set(['pair-top','pair-bottom','nuclear','laser']);s6Opening=null;run._mission29OpeningDone=true;stageTimer=80;stagePlan=[];spawnClock=9999;s6WingInit();s6WingLaunch(4,true);s6Wing.all=true;s6Wing.beats=3;s6Wing.fake={t:0};s6Wing.fakeDone=false;s6Wing.postMiniT=5;s6Wing.supplyIndex=3;s6Wing.route=null;Audio.startMusic('stage6');Input.clearTaps();}")
  elif part=='city':
   # Actual city checkpoint: native Harrier -> Nightwing -> full death/results.
   p.evaluate("()=>{boss=null;bossActive=false;BOFCinematicDirector.cancel();story=null;AP10_X.intro=null;campaign.stageX1004={route:'left',target:'harrier',done:false};campaign.cityRescue16=null;GP4.route='left';GP4.routeReady=true;GP4.stageX=true;GP4.stageXRoute='left';run._gp4StageX='left';}")
   p.evaluate("()=>{cf4LaunchX();}")
   for i in range(1800):
    p.evaluate(shoot.STEP,6);p.wait_for_timeout(1)
    if p.evaluate('!!boss'):break
   assert p.evaluate("run._gp4StageX==='left'&&boss?.kind==='warhive'&&!boss?._fb112")
   for i in range(3600):
    p.evaluate("()=>{if(boss&&!boss.dead)for(const t of _lockTargets().slice())if((t===boss||t._retinaOwner===boss)&&!t.dead)retinaMissileDamage(t,1e6);}")
    p.evaluate(shoot.STEP,6);p.wait_for_timeout(1)
    if p.evaluate('state===GS.STAGECLEAR'):break
   assert p.evaluate('state===GS.STAGECLEAR&&run._city16Defeat?.verified')
   p.evaluate("()=>{computeStageResults();scLeaveStage(drawStageClear._res);}")
   p.wait_for_function("()=>BOFCinematicDirector.current?.id==='post-city16'&&d1110Ready(BOFCinematicDirector.current.d1110Keys)",polling=50)
   p.wait_for_function('()=>{map4eWarm();return fury14MapReady();}',polling=50)
  else:
   if part=='storm':p.evaluate("()=>{B._fb112.phase='recover';B._fb112.wait=999;B._tc119.flow=null;B._tc119.di=0;B.y=180;B.enter=false;for(const part of [...B._fb112.parts,B._fb112.core]){let n=0;while(part.hp>0&&n++<500){const at=fb112PartPoint(B,part);efxClock+=1/60;fb112Damage(B,1e6,at.x,at.y,part);}}}")
   else:
    p.evaluate("()=>{for(let i=0;i<B._rebels.ships.length;i++){const q=B._rebels.ships[i];if(q.key==='nyx'){ny46Hidden(q);rd21Reveal(q,'retina');for(let f=0;f<85;f++){efxClock+=1/60;rebelSquadTick(B,1/60);}}let n=0;while(!q.dead&&q.hp>0&&n++<160){B._rebels.hit=i;efxClock+=1/30;rebelSquadDamage(B,1e6);}}}")
    for i in range(450):
     p.evaluate(shoot.STEP,6)
     if p.evaluate('!!run._stage6FateDefeat'):break
     p.wait_for_timeout(1)
   assert p.evaluate('run._stage6FateDefeat?.verified===true')
   p.evaluate("()=>{scLeaveStage({bonus:500,rank:'A'});}")
   p.wait_for_function('()=>d1110Ready(BOFCinematicDirector.current.d1110Keys)',polling=50)
   p.wait_for_function('()=>{map4eWarm();return fury14MapReady();}',polling=50)
  p.evaluate('()=>{warmStage(7);ls112Warm(7);}')
  p.wait_for_function('()=>{const n=run.stage;try{run.stage=7;stageLoadTick();ls112Warm(7);}finally{run.stage=n;}return stageLoadInfo(7).ready&&ls112Keys(7).every(k=>XART.rdy(k));}',polling=50)
  p.evaluate('()=>{Input.clearTaps();Input.mouse.down=false;last=performance.now();}')
  print('RECORDING '+part,flush=True);r=p.evaluate(RECORD,part)
  (F/(part+'.webm')).write_bytes(base64.b64decode(r.pop('video').split(',')[1]));shots=[]
  for i,s in enumerate(r.pop('samples')):
   fn=part+'-sample-%02d.png'%i;(O/fn).write_bytes(base64.b64decode(s.pop('image').split(',')[1]));shots.append({**s,'file':fn})
  r.update({'part':part,'errors':errors,'shots':shots,'end':p.evaluate('({state,stage:run.stage,brief:run._sewerBriefed17,player:{x:player.x,y:player.y,alive:player.alive},receipt:campaign.stage6Fate||null,choice:FATE15.lastChoice,events:FATE15.events,points:achievementPoints(),city:campaign.cityRescue16,cap:campaign.unlockedMax})')})
  assert not errors and r['peak']>.001
  if part=='city':assert r['end']['state']=='play'and r['end']['stage']==7 and r['end']['brief']and r['end']['city']['travelSeen']
  elif part=='split':assert r['end']['choice']['left']=='STORM CANNON'
  else:assert r['end']['state']=='stagesel'and r['end']['receipt']['verified']and r['end']['receipt']['awardNotified']
  report['clips'].append(r);report['errors']+=errors;(O/'recording.json').write_text(json.dumps(report,indent=2),encoding='utf8')
  print(json.dumps({'part':part,'seconds':r['seconds'],'peak':r['peak'],'errors':errors}),flush=True);p.close()
 b.close()
report['coreAfter']={n:hashlib.sha256((R/n).read_bytes()).hexdigest()for n in core};assert report['coreBefore']==report['coreAfter']
(O/'recording.json').write_text(json.dumps(report,indent=2),encoding='utf8');print('Full native Stage X to7 sequence captured with native audio and visible HUD layers.',flush=True)
