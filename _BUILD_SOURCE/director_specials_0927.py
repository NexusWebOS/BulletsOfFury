"""Native special/element muzzle coverage with actual input, SFX and rendering."""
import ast,base64,http.server,json
from pathlib import Path
from playwright.sync_api import sync_playwright
import shoot as sh
OUT=Path('_shots/director_0927');OUT.mkdir(exist_ok=True,parents=True)
def constant(file,key):
 tree=ast.parse(Path(file).read_text(encoding='utf-8'))
 return next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(getattr(t,'id',None)==key for t in n.targets))
RESET=constant('_BUILD_SOURCE/verify_weapon_feedback_0926.py','RESET')
CAPTURE=constant('_BUILD_SOURCE/review_overnight_0927.py','CAPTURE')
# Capture-only headroom: the game itself and its gain settings are unchanged.
CAPTURE=CAPTURE.replace('window.captureBins=', 'window.captureGain=C.createGain();captureGain.gain.value=.4;captureGain.connect(captureAudio);captureGain.connect(captureAnalyser);window.captureBins=').replace('this._bofNode.connect(captureAudio);this._bofNode.connect(captureAnalyser);','this._bofNode.connect(captureGain);').replace('n.connect(captureAudio);n.connect(captureAnalyser);','n.connect(captureGain);')
scenes=[{'pilot':'maverick','seconds':4,'special':True,'hold':2.2,'expect':['laser','helix']},
 {'pilot':'falva','seconds':7,'special':True,'hold':5.2,'expect':['roller']},
 {'pilot':'decker','seconds':3,'expect':['shotgun']},
 {'pilot':'freezer','weapon':4,'seconds':3,'expect':['ice']},
 {'pilot':'yuri','seconds':3,'special':True,'expect':['lightning']},
 {'pilot':'cole','weapon':4,'seconds':3,'expect':['fire']}]
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
port,stop=sh.serve(sh.GAME);errors=[]
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1100,'height':1050});p.set_default_timeout(90000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('()=>window.__bofFrames>4');p.evaluate(sh.TRAP_RAF);p.evaluate(CAPTURE)
  p.evaluate('()=>{window.directorSpecialReset='+RESET+';}');p.evaluate('()=>wm26Warm()')
  p.wait_for_function("()=>Object.keys(DIRECTOR_ART.sheets).every(k=>XART.rdy('d27_'+k))")
  p.evaluate(sh.SETUP,{'state':'PLAY','stage':4,'pilot':'cole','invuln':True})
  result=p.evaluate("""async scenes=>{
   const stream=ctx.canvas.captureStream(30);for(const a of captureAudio.stream.getAudioTracks())stream.addTrack(a.clone());
   const rec=new MediaRecorder(stream,{mimeType:'video/webm;codecs=vp8,opus',videoBitsPerSecond:1700000,audioBitsPerSecond:96000}),chunks=[];
   rec.ondataavailable=e=>{if(e.data.size)chunks.push(e.data)};
   const done=new Promise(resolve=>rec.onstop=()=>{const f=new FileReader();f.onload=()=>resolve(f.result);f.readAsDataURL(new Blob(chunks,{type:'video/webm'}));});
   const original=wm26Draw,rows=[];let current=null;
   wm26Draw=function(...args){if(current)current.families.add(args[1]);return original(...args);};
   const start=performance.now(),total=scenes.reduce((n,s)=>n+s.seconds,0);let si=-1;capturePeak=0;rec.start();
   try{await new Promise(resolve=>{const timer=setInterval(()=>{
    const now=performance.now(),elapsed=(now-start)/1000;let local=elapsed,i=0;
    for(;i<scenes.length-1&&local>=scenes[i].seconds;i++)local-=scenes[i].seconds;const c=scenes[i];
    if(si!==i){si=i;if(special)endSpecial();directorSpecialReset(c);run.stage=4;curStage=STAGES[3];story=null;s6Opening=null;s6Wing=null;run.forge={};run.forgeForms={};
      Snd.stopMusic();Snd.setVol('music',0);Snd.setVol('sfx',.65);Snd.loopStopAll();if(c.special)startSpecial();
      if(c.pilot==='decker'){run.dkT=15;dkAmmo=3;dkReload=0;}if(c.pilot==='freezer')run.wvars[4]='icebreath';
      current={...c,families:new Set(),snaps:[]};rows.push(current);}
    player.invuln=0;powerups=[];Input.keys.arrowleft=Input.keys.arrowright=false;
    for(const k of keybind.fire)Input.keys[k]=local<(c.hold||c.seconds)||(c.pilot==='maverick'&&local>3.05&&local<3.13);loop(now);
    captureAnalyser.getFloatTimeDomainData(captureBins);for(const x of captureBins)capturePeak=Math.max(capturePeak,Math.abs(x));
    if(current.snaps.length<2&&local>(current.snaps.length+1)*c.seconds/3)current.snaps.push(ctx.canvas.toDataURL());
    if(elapsed>=total){clearInterval(timer);for(const k of keybind.fire)Input.keys[k]=false;resolve();}
   },1000/60);});}finally{wm26Draw=original;}
   rec.stop();const video=await done;stream.getTracks().forEach(t=>t.stop());return {video,seconds:total,audioPeak:capturePeak,sfxVolume:.65,captureGain:.4,scenes:rows.map(r=>({...r,families:[...r.families]}))};
  }""",scenes)
  (OUT/'player-specials.webm').write_bytes(base64.b64decode(result.pop('video').split(',')[1]))
  for s in result['scenes']:
   for i,img in enumerate(s.pop('snaps')):(OUT/f"special-{s['pilot']}-{i}.png").write_bytes(base64.b64decode(img.split(',')[1]))
  result['errors']=errors;(OUT/'specials.json').write_text(json.dumps(result,indent=2),encoding='utf-8');br.close()
finally:stop()
print(json.dumps(result,indent=2))
assert not errors,errors
assert all(set(s['expect']).issubset(s['families']) for s in result['scenes']),result['scenes']
assert 0<result['audioPeak']<1
