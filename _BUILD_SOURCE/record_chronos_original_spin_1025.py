"""Native two-handed spin review: explicit regular/chromium/red checkpoints.
Canvas composition copies the visible game/HUD canvases at their DOM positions;
Each material starts one whirlwind checkpoint, then native simulation runs.
"""
from pathlib import Path
import base64,json,time,subprocess
import imageio_ffmpeg
from playwright.sync_api import sync_playwright
from shoot import serve
R=Path(__file__).resolve().parents[1];O=R/'_shots/chronos_original_1025/video';O.mkdir(exist_ok=True,parents=True)
port,stop=serve(str(R));errors=[];timeline=[]
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1280,'height':800})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' or 'draw error' in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>5',timeout=180000);p.mouse.click(3,3)
  p.evaluate('()=>{run.stage=5;stageLoadBegin(5);bi24Warm();ht23Warm();ch23Warm();UI20.warm();c25Warm();c26Warm();c27Warm();}')
  p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(5)&&bi24Warm()&&ht23Warm()&&ch23Warm()&&c25Warm()&&c26Warm()&&c27Warm()&&UI20_KEYS.every(k=>XART.rdy(k))}',timeout=180000)
  raw=O/'furious-gameplay-audio.webm';f=raw.open('wb');p.expose_function('saveAVChunk',lambda b:f.write(base64.b64decode(b)))
  p.evaluate("""async()=>{
   const a=Snd._audioCtx();await a.resume();const mix=a.createMediaStreamDestination(),seen=new WeakSet();
   window.avStats={playing:{},peak:0,tapped:0};const analyser=a.createAnalyser();analyser.fftSize=1024;const captureGain=a.createGain();captureGain.gain.value=.55;analyser.connect(captureGain);captureGain.connect(mix);
   const nativePlay=HTMLMediaElement.prototype.play;HTMLMediaElement.prototype.play=function(){
    if(!seen.has(this)){
     try{if(this._bofNode)this._bofNode.connect(analyser);else{const n=a.createMediaElementSource(this);n.connect(a.destination);n.connect(analyser);}
      seen.add(this);avStats.tapped++;this.addEventListener('playing',()=>{const key=Object.entries(Snd.pools).find(([k,p])=>p.slots.some(s=>s?.el===this))?.[0]||Object.entries(Snd.music).find(([k,v])=>v===this)?.[0]||'loop';avStats.playing[key]=(avStats.playing[key]||0)+1;});
     }catch(e){avStats.tapError=String(e);}
    }return nativePlay.apply(this,arguments);
   };
   const c=document.createElement('canvas');c.width=1280;c.height=800;const g=c.getContext('2d');window.avLive=true;
   function render(){if(!avLive)return;g.fillStyle=getComputedStyle(document.body).backgroundColor;g.fillRect(0,0,1280,800);
    for(const v of document.querySelectorAll('canvas')){if(v===c||!v.width||!v.height)continue;const r=v.getBoundingClientRect(),s=getComputedStyle(v);if(!r.width||!r.height||r.right<=0||r.left>=1280||s.display==='none'||s.visibility==='hidden'||s.opacity==='0')continue;g.imageSmoothingEnabled=false;g.drawImage(v,r.x,r.y,r.width,r.height);}
    if(window.reviewCheckpoint){g.fillStyle='rgba(5,12,24,.90)';g.fillRect(310,754,660,36);g.fillStyle='#f1d27d';g.font='16px sans-serif';g.textAlign='center';g.fillText(reviewCheckpoint,640,778);}const d=new Float32Array(analyser.fftSize);analyser.getFloatTimeDomainData(d);for(const v of d)avStats.peak=Math.max(avStats.peak,Math.abs(v));requestAnimationFrame(render);
   }render();window.avCanvas=c;
   const stream=c.captureStream(30);for(const t of mix.stream.getAudioTracks())stream.addTrack(t);
   const rec=window.avRecorder=new MediaRecorder(stream,{mimeType:'video/webm;codecs=vp9,opus',videoBitsPerSecond:6500000,audioBitsPerSecond:160000});window.avPending=Promise.resolve();
   rec.ondataavailable=e=>{if(!e.data.size)return;avPending=avPending.then(async()=>{const b=new Uint8Array(await e.data.arrayBuffer());let t='';for(let i=0;i<b.length;i+=32768)t+=String.fromCharCode(...b.subarray(i,i+32768));await saveAVChunk(btoa(t));});};rec.start(1000);
   diffKey='furious';debugStartFight({stage:5,role:'boss',kind:'chromehammer',name:'Chronos'},{pilot:'cole'});debugUnlocked=true;DBGT.god=true;player.invuln=0;
  }""")
  p.evaluate("""()=>{spawnBoss('chromehammer');debugFight.spawned=true;warnT=0;bossActive=true;window.spinCheckpoint=mat=>{BOFCinematicDirector.cancel();fb2Intro=fb2Talk=null;HT23.speech.length=0;const b=boss,h=b._hammer;b.enter=b._noHit=b.dead=false;b.maxhp=11220;b.hp=b.maxhp;b.x=340;b.y=230;b._drawY=b.y;b.flash=0;b._gp4FlashNext=0;h.balance0922=true;h.ballSeen=h.whirlSeen=h.hb20PickupDone=true;h.mode='hammer';h.phaseTwo=false;h.hammerDestroyed=false;h.c27RagePending=false;h._hf22Red=mat==='red';h._hf22Charge=null;h.frArmor={hp:mat==='regular'?0:8415,max:8415,activated:true,active:true,t:0,flash:0,barrier:0,checkpoints:[.75,.5,.35]};h.recovery=h.c25Knock=h.hb20Pickup=h.c26Return=h.c27Combo=h.throw=null;h.phasePending=false;h._hj22Pair=h._hf22StormPair=null;eBullets=[];pBullets=[];enemies=[];l5Rocks=[];powerups=[];player.x=340;player.y=460;hammerState(b,'hammer');hammerWhirlStart(b);window.reviewCheckpoint='Two-handed spin checkpoint: '+mat+' armor';};spinCheckpoint('regular');}""")
  p.evaluate("""()=>{window.weaponDrawTrace={};const fn=ctx.drawImage;ctx.drawImage=function(im,...args){const key=HA21.tags.get(im);if(key&&/hammer|tool|hj22|ha21|hm10|fr27|c27/.test(key)){const k=(boss?._hammer?.state||'none')+':'+key;weaponDrawTrace[k]=(weaponDrawTrace[k]||0)+1;}return fn.call(this,im,...args)};}""")
  started=time.monotonic();move=None;firing=False;last='';next_move=0;missile_at=0;checkpoint=0
  while time.monotonic()-started<20:
   t=time.monotonic()-started;p.evaluate('DBGT.god=true;player.invuln=0')
   if t>=7 and checkpoint==0:
    checkpoint=1;p.evaluate("spinCheckpoint('chrome')")
   elif t>=14 and checkpoint==1:
    checkpoint=2;p.evaluate("spinCheckpoint('red')")
   if t>=next_move:
    aim=p.evaluate("()=>({x:player.x,target:c25Counter(boss)?hammerHeadPoint(boss).x:boss&&!boss.dead?boss.x+Math.sin(efxClock*.9)*65:340})")
    wanted='d' if aim['x']<aim['target']-12 else 'a' if aim['x']>aim['target']+12 else None
    if move!=wanted:
     if move:p.keyboard.up(move)
     if wanted:p.keyboard.down(wanted)
     move=wanted
    next_move=t+.3
   wantfire=False
   if wantfire and not firing:p.keyboard.down('j');firing=True
   elif not wantfire and firing:p.keyboard.up('j');firing=False
   r=p.evaluate("""()=>({time:efxClock,pose:boss?ha21Blue(boss)?.kind:null,state:boss?._hammer?.state,hp:boss?.hp,armor:fr27Armor(boss)?.hp,radio:ui20Radio(),checkpoint:window.reviewCheckpoint||null,counter:c25Counter(boss),knock:boss?._hammer?.c25Knock?.t,scroll:_stage5SpaceScroll,player:{x:player.x,y:player.y,dead:player.dead},boss:{x:boss?.x,y:boss?.y}})""");r['videoSeconds']=round(t,3);timeline.append(r)
   # Missile is a normal input during the exposed charging window.
   if r['counter'] and t>missile_at and p.evaluate('Math.abs(player.x-hammerHeadPoint(boss).x)<24'):p.keyboard.press('k');missile_at=t+.8
   key=json.dumps([r['state'],(r.get('radio') or {}).get('who'),(r.get('radio') or {}).get('text')])
   if key!=last:
    print(json.dumps(r),flush=True);last=key
    if r['state'] in ['fr_activation','storm_raise','fr_stun']:p.screenshot(path=str(O/('gameplay-'+r['state']+f'-{int(t)}.png')))
   p.wait_for_timeout(300)
  p.keyboard.up('j')
  if move:p.keyboard.up(move)
  stats=p.evaluate("""async()=>{await new Promise(r=>{avRecorder.onstop=r;avRecorder.stop()});await avPending;avLive=false;return{...avStats,weaponDrawTrace,events:C25.events,motionEvents:C26.events,depthEvents:C27.events,god:DBGT.god,godBlocks:DBGT.stats?.godBlocks,deaths:DBGT.stats?.deaths};}""");f.close();p.screenshot(path=str(O/'gameplay-end.png'));br.close()
finally:stop()
mp4=O/'two-handed-spin.mp4';subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-y','-loglevel','error','-i',str(raw),'-vf','fps=30','-af','volume=0.78','-c:v','libx264','-preset','fast','-crf','19','-c:a','aac','-b:a','160k','-pix_fmt','yuv420p','-movflags','+faststart',str(mp4)],check=True)
report=dict(difficulty='furious',pilot='cole',invulnerable=True,route='Explicit spin checkpoints: regular at0s, chromium at7s, red at14s. Native movement, attack clock, whole authored frames and sound; invulnerable observer. This is a focused animation review, not a continuous full boss fight.',audio=stats,errors=errors,timeline=timeline,video=str(mp4.relative_to(R)))
(O/'spin-recording.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf8');print(json.dumps(dict(video=str(mp4),peak=stats['peak'],errors=errors)),flush=True)

review=O/'two-handed-spin-review.mp4'
subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-v','error','-y','-ss','0.65','-i',str(mp4),'-t','19.6','-c:v','libx264','-preset','fast','-crf','19','-c:a','aac','-b:a','160k','-pix_fmt','yuv420p','-movflags','+faststart',str(review)],check=True)
