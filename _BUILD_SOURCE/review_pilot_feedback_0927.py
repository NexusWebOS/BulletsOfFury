"""Real-time native Chromium feedback clips; empty encounter fixtures, not campaign runs."""
import ast,base64,http.server,json
from pathlib import Path
from playwright.sync_api import sync_playwright
import shoot as sh

OUT=Path('_shots/pilot_feedback_0927');OUT.mkdir(exist_ok=True,parents=True)
def constant(file,key):
 tree=ast.parse(Path(file).read_text(encoding='utf-8'))
 return next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(getattr(t,'id',None)==key for t in n.targets))
RESET=constant('_BUILD_SOURCE/verify_weapon_feedback_0926.py','RESET')
CAPTURE=constant('_BUILD_SOURCE/review_overnight_0927.py','CAPTURE')
CAPTURE=CAPTURE.replace('window.captureBins=', 'window.captureGain=C.createGain();captureGain.gain.value=.4;captureGain.connect(captureAudio);captureGain.connect(captureAnalyser);window.captureBins=').replace('this._bofNode.connect(captureAudio);this._bofNode.connect(captureAnalyser);','this._bofNode.connect(captureGain);').replace('n.connect(captureAudio);n.connect(captureAnalyser);','n.connect(captureGain);')
CASES=[{'name':'single-muzzles','seconds':12,'stage':1,'pilot':'cole'},
       {'name':'ice-breath','seconds':8,'stage':2,'pilot':'freezer','weapon':4},
       {'name':'acceleration','seconds':16,'stage':1,'pilot':'cole'}]
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
port,stop=sh.serve(sh.GAME);errors=[];report=[]
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required'])
  p=br.new_page(viewport={'width':1100,'height':1050});p.set_default_timeout(90000)
  p.on('pageerror',lambda e:errors.append(str(e)))
  p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('()=>window.__bofFrames>4');p.evaluate(sh.TRAP_RAF);p.evaluate(CAPTURE)
  p.evaluate('()=>{window.feedbackReset='+RESET+';wm26Warm();furyShipWarm();XART.rdy("ice_breath_0927");}')
  p.wait_for_function("()=>furyShipReady()&&XART.rdy('ice_breath_0927')&&Object.keys(DIRECTOR_ART.sheets).every(k=>XART.rdy('d27_'+k))")
  for c in CASES:
   p.evaluate(sh.SETUP,{'state':'PLAY','stage':c['stage'],'pilot':c['pilot'],'invuln':False});p.evaluate(RESET,c)
   p.evaluate("c=>{run.stage=c.stage;curStage=STAGES[c.stage-1];if(c.pilot==='freezer')run.wvars[4]='icebreath';timeScale=1;player._thrustPower=0;player._spaceMuzzle=0;run.wlevel=5;run.wlevels=WEAPONS.map(()=>5);for(const k of Object.keys(Input.keys))Input.keys[k]=false;Snd.stopMusic();Snd.setVol('music',0);Snd.setVol('sfx',.65);Snd.loopStopAll();capturePeak=0;}",c)
   p.evaluate(sh.STEP,4);p.wait_for_timeout(500);p.evaluate(sh.STEP,4)
   print('RECORD',c['name'],flush=True)
   r=p.evaluate("""async c=>{
    const stream=ctx.canvas.captureStream(30);for(const a of captureAudio.stream.getAudioTracks())stream.addTrack(a.clone());
    const rec=new MediaRecorder(stream,{mimeType:'video/webm;codecs=vp8,opus',videoBitsPerSecond:1700000,audioBitsPerSecond:96000}),chunks=[];
    rec.ondataavailable=e=>{if(e.data.size)chunks.push(e.data)};
    const done=new Promise(resolve=>rec.onstop=()=>{const f=new FileReader();f.onload=()=>resolve(f.result);f.readAsDataURL(new Blob(chunks,{type:'video/webm'}));});
    let last=-1,switched=false;const snaps=[],samples=[],start=performance.now();capturePeak=0;rec.start();
    await new Promise(resolve=>{const timer=setInterval(()=>{
     const now=performance.now(),t=(now-start)/1000;for(const k of Object.keys(Input.keys))Input.keys[k]=false;player.invuln=0;powerups=[];
     if(c.name==='single-muzzles'){const i=Math.min(3,Math.floor(t/3));if(i!==last){last=i;run.weapon=[0,1,2,7][i];pBullets=[];wm26Releases=[];run._chainHeat=run._chainOverheat=0;}for(const k of keybind.fire)Input.keys[k]=true;}
     if(c.name==='ice-breath')for(const k of keybind.fire)Input.keys[k]=true;
     if(c.name==='acceleration'){
      if(t>=8&&!switched){switched=true;run.stage=5;curStage=STAGES[4];gravityMode=GRAVITY_SHIP_ACTIVE;run.spaceMode=true;run.gravityShipReady=true;run.spaceWeapon=0;run.spaceLevels=[3,3,3];player.x=worldWidth()/2;player.y=350;camX=player.x-VW/2;player._thrustPower=0;}
      const s=t%8;for(const k of keybind.up)Input.keys[k]=(s>1&&s<2.2)||(s>5.4&&s<6.6);for(const k of keybind.down)Input.keys[k]=s>3.2&&s<4.4;
      if(switched)for(const k of keybind.fire)Input.keys[k]=s<7;
     }
     loop(now);captureAnalyser.getFloatTimeDomainData(captureBins);for(const x of captureBins)capturePeak=Math.max(capturePeak,Math.abs(x));
     if(snaps.length<4&&t>(snaps.length+1)*c.seconds/5){snaps.push(ctx.canvas.toDataURL());samples.push({t,thrust:player._thrustPower||0,space:run.spaceMode,zoom:viewZoom(),flashes:wm26Releases.length});}
     if(t>=c.seconds){clearInterval(timer);resolve();}
    },1000/60);});
    rec.stop();const video=await done;stream.getTracks().forEach(t=>t.stop());for(const k of Object.keys(Input.keys))Input.keys[k]=false;
    return {video,snaps,samples,audioPeak:capturePeak};
   }""",c)
   (OUT/(c['name']+'.webm')).write_bytes(base64.b64decode(r.pop('video').split(',')[1]))
   for i,s in enumerate(r.pop('snaps')):(OUT/f"{c['name']}-clip-{i}.png").write_bytes(base64.b64decode(s.split(',')[1]))
   report.append({**c,**r})
  br.close()
finally:stop()
(OUT/'clips.json').write_text(json.dumps({'clips':report,'errors':errors},indent=2),encoding='utf-8')
print(json.dumps({'clips':report,'errors':errors},indent=2))
assert not errors,errors
assert all(0<r['audioPeak']<1 for r in report),report
assert all(all(s['zoom']==1 for s in r['samples']) for r in report)
