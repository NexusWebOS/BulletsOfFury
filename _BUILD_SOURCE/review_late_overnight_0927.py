"""Real-time Chromium clips with captured game audio. Inspection fixtures, not wins."""
import ast,base64,json,http.server,sys
from pathlib import Path
import shoot as sh
from playwright.sync_api import sync_playwright
OUT=Path('_shots/overnight_0927/late-review');OUT.mkdir(parents=True,exist_ok=True)
tree=ast.parse(Path('_BUILD_SOURCE/probe_polish_0927b.py').read_text(encoding='utf-8'))
SETUP=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id=='SETUP')
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
port,stop=sh.serve(sh.GAME);errors=[];report=[]
CASES=[
 {'name':'furnace-core','stage':2,'kind':'infernoreaver','mini':False,'diff':'hard','seconds':32,'setup':"furnaceSync(B);B.x=worldWidth()/2;B.y=150;B._fz.pools.left=B._fz.pools.right=0;furnaceEnter(B,'core');B._fz.trans=0;if(B._mwBarrier)B._mwBarrier.active=false;"},
 {'name':'furnace-detached-head','stage':2,'kind':'infernoreaver','mini':False,'diff':'furious','seconds':32,'setup':"furnaceSync(B);B.x=worldWidth()/2;B.y=150;B._fz.pools.left=B._fz.pools.right=B._fz.pools.body=0;furnaceEnter(B,'head');B._fz.trans=0;if(B._mwBarrier)B._mwBarrier.active=false;"},
 {'name':'tidal-sentinels','stage':9,'kind':'tidalfusion','mini':False,'diff':'furious','seconds':30,'setup':""},
 {'name':'toxic-shield','stage':7,'kind':'sludgeemperor','mini':False,'diff':'hard','seconds':26,'setup':"s7mInit(B);B._be=null;B._s7FinalNoBar=false;B.x=worldWidth()/2;B.y=175;for(const p of B._s7mod.parts)if(!p.id.startsWith('gun'))p.hp=0;B._s7mod.seq=0;s7mSet(B,'recover');"},
 {'name':'razorback-reference','stage':1,'kind':'razorback','mini':True,'diff':'normal','seconds':40,'setup':""},
 {'name':'helicopter-reference','stage':1,'kind':'damkeeper','mini':False,'diff':'furious','seconds':70,'setup':""},
 {'name':'furnace-head','stage':2,'kind':'infernoreaver','mini':False,'diff':'hard','seconds':50,'setup':""},
 {'name':'frost-nuclear','stage':3,'kind':'frostcruiser','mini':True,'diff':'furious','seconds':55,'setup':""},
 {'name':'cryo-nuclear','stage':3,'kind':'cryospear','mini':False,'diff':'furious','seconds':55,'setup':""},
 {'name':'olive-warden','stage':4,'kind':'olivewarden','mini':True,'diff':'hard','seconds':40,'setup':""},
 {'name':'caustic-tank','stage':7,'kind':'dualscoopdredger','mini':True,'diff':'hard','seconds':40,'setup':""},
 {'name':'toxic-legged','stage':7,'kind':'sludgeemperor','mini':False,'diff':'furious','seconds':45,'setup':""},
 {'name':'magma-furious','stage':2,'kind':'magmaward','mini':True,'diff':'furious','seconds':40,'setup':""},
 {'name':'magma-normal','stage':2,'kind':'magmaward','mini':True,'diff':'normal','seconds':35,'setup':""},
 {'name':'rival-crew','stage':6,'kind':'rebelsquad','mini':False,'diff':'normal','seconds':30,'setup':"run.mode='campaign';run.pilot='cole';pilotIndex=PILOTS.findIndex(p=>p.key==='cole');campaign.unlockedMax=8;campaign.rivalScattered=true;campaign.rivalDefeated=[false,false,false,false,false];openStageSelect(8,{});stateT=2;Input.injectTap('arrowdown');Rival24.mapInput();Input.injectTap('enter');Rival24.mapInput();Input.injectTap('enter');Rival24.selectDraw(.1);Input.injectTap('arrowright');Rival24.selectDraw(.1);Input.injectTap('enter');Rival24.selectDraw(.1);Input.injectTap('enter');Rival24.selectDraw(.1);window.B=boss;setState(GS.PLAY);story=null;s6Opening=null;Rival24.active.music=true;Snd.stopMusic();Snd.setVol('music',0);Snd.loopStopAll();"},
 {'name':'sovereign-helpers','stage':4,'kind':'stormsovereign','mini':False,'diff':'hard','seconds':24,'setup':"B.enter=false;B._noHit=false;B.x=worldWidth()/2;B.y=B._er26.home;B._er26.from={x:B.x,y:B.y};B.hp=B.maxhp*.45;stage4ShieldSyncNodes(B);stage4CoreTurretSpawnMissing(B,.5);B._s4war.shieldThresholdIndex=2;er26Set(B,'escort-crossfire');"},
 {'name':'tempest-normal','stage':6,'kind':'tempestbrothers','mini':True,'diff':'normal','seconds':40,'setup':"s6Opening=null;stageTimer=34;s6WingLaunch(2,false);s6Wing.beats=1;"},
 {'name':'toxic-core-laser','stage':7,'kind':'sludgeemperor','mini':False,'diff':'normal','seconds':16,'setup':"s7mInit(B);B._be=null;B._s7FinalNoBar=false;B.x=worldWidth()/2;B.y=175;for(const p of B._s7mod.parts)p.hp=0;B._s7mod.shield=0;B._s7mod.seq=0;s7mSet(B,'laser');"},
 {'name':'toxic-core-guns','stage':7,'kind':'sludgeemperor','mini':False,'diff':'hard','seconds':16,'setup':"s7mInit(B);B._be=null;B._s7FinalNoBar=false;B.x=worldWidth()/2;B.y=175;for(const p of B._s7mod.parts)if(!p.id.startsWith('gun'))p.hp=0;B._s7mod.shield=0;B._s7mod.seq=0;s7mSet(B,'aim');"}
]
if len(sys.argv)>1:
 CASES=[c for c in CASES if c['name'] in sys.argv[1:]]
 if (OUT/'report.json').exists():report=json.loads((OUT/'report.json').read_text(encoding='utf-8'))['clips'];report=[r for r in report if r['name'] not in sys.argv[1:]]
CAPTURE="""async()=>{const C=Snd._audioCtx();await C.resume();window.captureAudio=C.createMediaStreamDestination();window.captureAnalyser=C.createAnalyser();captureAnalyser.fftSize=1024;window.captureBins=new Float32Array(1024);window.capturePeak=0;window.captureCues=[];const cuePlay=Snd.play;Snd.play=function(n,v){captureCues.push({at:performance.now(),name:n});if(captureCues.length>80)captureCues.shift();return cuePlay.call(Snd,n,v);};
 const old=HTMLMediaElement.prototype.play;HTMLMediaElement.prototype.play=function(){try{if(!this._captureReady){if(this._bofNode){this._bofNode.connect(captureAudio);this._bofNode.connect(captureAnalyser);}else{const n=C.createMediaElementSource(this);n.connect(C.destination);n.connect(captureAudio);n.connect(captureAnalyser);this._captureSource=n;this._bofNode=n;}this._captureReady=true;}}catch(e){}return old.apply(this,arguments);};} """
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1100,'height':1100});p.set_default_timeout(90000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load');p.wait_for_function('()=>window.__bofFrames>5');p.evaluate(sh.TRAP_RAF);p.evaluate(CAPTURE)
  for c in CASES:
   print('RECORD',c['name'],flush=True)
   c0={**c,'kind':c['kind'] or 'vileexistence'};p.evaluate(SETUP,c0)
   p.evaluate("()=>{timeScale=1;special=null;run.sonicT=run.dkT=0;run.forge={};run.weapon=0;run.wlevel=3;run.wlevels=[3,1,1,1,1,1,0,0,0];run.spaceWeapon=0;run.spaceLevels=[3,3,3];for(const k of Object.keys(Input.keys))Input.keys[k]=false;Snd.stopMusic();Snd.setVol('music',0);Snd.loopStopAll();capturePeak=0;captureCues=[];}")
   if c['setup']:p.evaluate('()=>{'+c['setup']+'}')
   p.wait_for_timeout(550)
   r=p.evaluate("""async c=>{const stream=ctx.canvas.captureStream(30);for(const a of captureAudio.stream.getAudioTracks())stream.addTrack(a.clone());const rec=new MediaRecorder(stream,{mimeType:'video/webm;codecs=vp8,opus',videoBitsPerSecond:1700000,audioBitsPerSecond:96000}),chunks=[];rec.ondataavailable=e=>{if(e.data.size)chunks.push(e.data)};
    const done=new Promise(resolve=>rec.onstop=()=>{const f=new FileReader();f.onload=()=>resolve(f.result);f.readAsDataURL(new Blob(chunks,{type:'video/webm'}));});
    const seen=[],snaps=[],start=performance.now();let peakAt=0,peakCues=[],last='',maxEnemy=0,maxBullets=0,maxJump=0,old={x:player.x,y:player.y},finite=true;rec.start();
    await new Promise(resolve=>{const timer=setInterval(()=>{const now=performance.now(),t=(now-start)/1000;player.invuln=10;powerups=[];
     // Constant-speed lateral input makes camera stability visible; damage immunity is an inspection aid.
     const left=t%10<5;for(const [a,on] of [['left',left],['right',!left],['fire',c.name==='stage8-fleet'||c.name==='toxic-shield']])for(const k of keybindFor(1)[a]||[])if(!k.startsWith('pad_'))Input.keys[k]=on;
     loop(now);const tag=B._hammer?.state||B._er26?.mode||B._bomber?.mode||B._whv?.st||B._s7mod?.mode||B._tempestDuo?.ai?.black?.state||B._v24?.pattern?.type||B._rzb?.attack||B._ovState||B._late27?.mode||B._rebels?.ships.map(q=>q.mode).join('/')||B.phase||'fleet';if(tag!==last){seen.push({t:+t.toFixed(2),state:tag});last=tag;}
     maxJump=Math.max(maxJump,Math.hypot(player.x-old.x,player.y-old.y));old={x:player.x,y:player.y};maxEnemy=Math.max(maxEnemy,enemies.filter(e=>!e.dead).length);maxBullets=Math.max(maxBullets,eBullets.length);finite=finite&&eBullets.every(q=>Number.isFinite(q.x+q.y));
     captureAnalyser.getFloatTimeDomainData(captureBins);for(const x of captureBins)if(Math.abs(x)>capturePeak){capturePeak=Math.abs(x);peakAt=t;peakCues=captureCues.filter(q=>now-q.at<500).map(q=>q.name);}
     if(snaps.length<10&&t>c.seconds*(snaps.length+1)/11)snaps.push(ctx.canvas.toDataURL());
     if(t>=c.seconds){clearInterval(timer);resolve();}
    },1000/60);});rec.stop();const video=await done;stream.getTracks().forEach(t=>t.stop());for(const k of Object.keys(Input.keys))Input.keys[k]=false;return {video,seen,snaps,maxEnemy,maxBullets,maxJump,finite,audioPeak:capturePeak,peakAt,peakCues,musicGain:Snd.vol.music,zoom:viewZoom()};}""",c)
   (OUT/(c['name']+'.webm')).write_bytes(base64.b64decode(r.pop('video').split(',')[1]))
   for i,s in enumerate(r.pop('snaps')):(OUT/f"{c['name']}-{i}.png").write_bytes(base64.b64decode(s.split(',')[1]))
   report.append({**c,**r});(OUT/'report.json').write_text(json.dumps({'clips':report,'errors':errors},indent=2),encoding='utf-8')
  br.close()
finally:stop()
print(json.dumps({'clips':report,'errors':errors},indent=2));assert not errors,errors
assert all(c['finite'] and c['audioPeak']>.001 for c in report)
