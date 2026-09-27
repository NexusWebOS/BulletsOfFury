"""Real-time secret encounter and supplied remix. Invulnerability is a recording aid."""
import ast,base64,http.server,json
from pathlib import Path
from playwright.sync_api import sync_playwright
import shoot as sh

OUT=Path('_shots/hammer_time_ship_0927');OUT.mkdir(exist_ok=True,parents=True)
tree=ast.parse(Path('_BUILD_SOURCE/review_overnight_0927.py').read_text(encoding='utf-8'))
CAPTURE=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(getattr(t,'id',None)=='CAPTURE' for t in n.targets))
CAPTURE=CAPTURE.replace('window.captureBins=', 'window.captureGain=C.createGain();captureGain.gain.value=.4;captureGain.connect(captureAudio);captureGain.connect(captureAnalyser);window.captureBins=').replace('this._bofNode.connect(captureAudio);this._bofNode.connect(captureAnalyser);','this._bofNode.connect(captureGain);').replace('n.connect(captureAudio);n.connect(captureAnalyser);','n.connect(captureGain);')
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
port,stop=sh.serve(sh.GAME);errors=[]
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1100,'height':1050});p.set_default_timeout(90000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  # Keep the physical desktop controller from steering this keyboard-driven fixture.
  p.add_init_script("Object.defineProperty(navigator,'getGamepads',{value:()=>[]});")
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('()=>window.__bofFrames>4');p.evaluate(sh.TRAP_RAF);p.evaluate(CAPTURE)
  p.evaluate("()=>{setState(GS.PASSWORD);pwInput='HAMMER';submitPassword();diffKey='hard';DIFF=DIFFS.hard;pilotIndex=PILOTS.findIndex(p=>p.key==='cole');startRun(PENDING_STAGE);Snd.music.hammerTime.pause();Snd.setVol('music',.75);Snd.setVol('sfx',.35);}")
  p.wait_for_function("()=>Object.keys(HAMMER_TIME_ART.sheets).every(k=>XART.rdy('ht27_'+k))&&XART.rdy('arch_ship_transform')&&XART.rdy('arch_orbital_sweep_0926')&&furyShipReady()&&Snd.music.hammerTime.readyState>=3")
  r=p.evaluate("""async()=>{
   const stream=ctx.canvas.captureStream(30);for(const a of captureAudio.stream.getAudioTracks())stream.addTrack(a.clone());
   const rec=new MediaRecorder(stream,{mimeType:'video/webm;codecs=vp8,opus',videoBitsPerSecond:2200000,audioBitsPerSecond:160000}),chunks=[];
   rec.ondataavailable=e=>{if(e.data.size)chunks.push(e.data)};
   const done=new Promise(resolve=>rec.onstop=()=>{const f=new FileReader();f.onload=()=>resolve(f.result);f.readAsDataURL(new Blob(chunks,{type:'video/webm'}));});
   const m=Snd.music.hammerTime;m.currentTime=0;boss._hammerTime.clock=0;capturePeak=0;rec.start();updatePlay(0);await m.play();
   const intro={x:player.x,y:player.y,ammo:run.bombs,moved:false,shots:false,pause:false,release:null,helpers:0};const start=performance.now(),states=[],snaps=[],audio=[],lock={first:null,last:null,frames:0,moved:false,shots:false,ammo:false,pause:false},times=[1,2.8,5.5,6.2,7,10,15.9,17,20,25,34];let tag='',lockedPosition=null,lastSample=-1;
   await new Promise(resolve=>{const timer=setInterval(()=>{
    const now=performance.now(),t=m.currentTime;player.invuln=10;powerups=[];
    for(const k of Object.keys(Input.keys))Input.keys[k]=false;
    for(const a of [t%8<4?'left':'right','fire'])for(const k of keybind[a])Input.keys[k]=true;
    if(boss._hammerTime.mode==='intro'||t>=16&&t<24){for(const a of ['bomb','up'])for(const k of keybind[a])Input.keys[k]=true;setState('paused');}
    loop(now);
    const d=boss&&boss._hammerTime,current=d?d.mode+':'+boss._hammer.state:state;
    if(current!==tag){states.push({t:+t.toFixed(3),state:current,hp:boss?.hp});tag=current;}
    if(ht27Locked()){intro.moved=intro.moved||player.x!==intro.x||player.y!==intro.y;intro.shots=intro.shots||pBullets.length>0;intro.pause=intro.pause||state==='paused';}else if(intro.release===null){intro.release=t;intro.helpers=d.helpers.length;intro.remainingAmmo=run.bombs;}
    if(d?.locked){
     if(lock.first===null){lock.first=t;lockedPosition={x:player.x,y:player.y,ammo:run.bombs};}
     lock.last=t;lock.frames++;lock.moved=lock.moved||player.x!==lockedPosition.x||player.y!==lockedPosition.y;
     lock.shots=lock.shots||pBullets.length>0;lock.ammo=lock.ammo||run.bombs!==lockedPosition.ammo;lock.pause=lock.pause||state==='paused';
    }
    captureAnalyser.getFloatTimeDomainData(captureBins);let peak=0;for(const x of captureBins)peak=Math.max(peak,Math.abs(x));capturePeak=Math.max(capturePeak,peak);
    if(Math.floor(t)!==lastSample){lastSample=Math.floor(t);audio.push({t:+t.toFixed(2),peak});}
    if(snaps.length<times.length&&t>=times[snaps.length])snaps.push(ctx.canvas.toDataURL());
    if(t>=36||(now-start)>45000){clearInterval(timer);resolve();}
   },1000/60);});
   rec.stop();const video=await done;stream.getTracks().forEach(t=>t.stop());for(const k of Object.keys(Input.keys))Input.keys[k]=false;
   return {video,snaps,states,audio,audioPeak:capturePeak,lock,intro,seconds:m.currentTime,zoom:viewZoom(),stillPlaying:state===GS.PLAY,released:!ht27Locked(),fixture:'Hard difficulty; player invulnerability only; real-time native Chromium with supplied soundtrack'};
  }""")
  (OUT/'hammer-time.webm').write_bytes(base64.b64decode(r.pop('video').split(',')[1]))
  for i,s in enumerate(r.pop('snaps')):(OUT/f'clip-{i}.png').write_bytes(base64.b64decode(s.split(',')[1]))
  r['errors']=errors;br.close()
finally:stop()
(OUT/'clip.json').write_text(json.dumps(r,indent=2),encoding='utf-8');print(json.dumps(r,indent=2))
assert not errors,errors
assert r['seconds']>=36 and r['released'] and r['stillPlaying'] and r['zoom']==1
assert 0<r['audioPeak']<1 and all(q['peak']>.0001 for q in r['audio'] if 16<q['t']<24)
assert 16<=r['lock']['first']<16.2 and 23.8<r['lock']['last']<24.1
assert not any(r['lock'][k] for k in ['moved','shots','ammo','pause'])

assert 24<=r['intro']['release']<24.2
assert r['intro']['helpers']==4 and r['intro']['remainingAmmo']==r['intro']['ammo'] and not any(r['intro'][k] for k in ['moved','shots','pause'])
