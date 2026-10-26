"""Continuous native Stage5 Furious recording with shared-mixer game audio.
Canvas composition copies the visible game/HUD canvases at their DOM positions;
no attack, state, dialogue or pose injections are used in the gameplay capture.
"""
from pathlib import Path
import base64,json,time,subprocess
import imageio_ffmpeg
from playwright.sync_api import sync_playwright
from shoot import serve
R=Path(__file__).resolve().parents[1];O=R/'_shots/chronos_contract_1025';O.mkdir(exist_ok=True)
port,stop=serve(str(R));errors=[];timeline=[]
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1280,'height':800})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' or 'draw error' in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>5',timeout=180000);p.mouse.click(3,3)
  p.evaluate('()=>{run.stage=5;stageLoadBegin(5);bi24Warm();ht23Warm();ch23Warm();UI20.warm();c25Warm();}')
  p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(5)&&bi24Warm()&&ht23Warm()&&ch23Warm()&&c25Warm()&&UI20_KEYS.every(k=>XART.rdy(k))}',timeout=180000)
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
    const d=new Float32Array(analyser.fftSize);analyser.getFloatTimeDomainData(d);for(const v of d)avStats.peak=Math.max(avStats.peak,Math.abs(v));requestAnimationFrame(render);
   }render();window.avCanvas=c;
   const stream=c.captureStream(30);for(const t of mix.stream.getAudioTracks())stream.addTrack(t);
   const rec=window.avRecorder=new MediaRecorder(stream,{mimeType:'video/webm;codecs=vp9,opus',videoBitsPerSecond:6500000,audioBitsPerSecond:160000});window.avPending=Promise.resolve();
   rec.ondataavailable=e=>{if(!e.data.size)return;avPending=avPending.then(async()=>{const b=new Uint8Array(await e.data.arrayBuffer());let t='';for(let i=0;i<b.length;i+=32768)t+=String.fromCharCode(...b.subarray(i,i+32768));await saveAVChunk(btoa(t));});};rec.start(1000);
   diffKey='furious';debugStartFight({stage:5,role:'boss',kind:'chromehammer',name:'Chronos'},{pilot:'cole'});player.invuln=999;
  }""")
  started=time.monotonic();move=None;firing=False;last='';next_move=0;missile_at=0
  while time.monotonic()-started<150:
   t=time.monotonic()-started;p.evaluate('player.invuln=999')
   if t>=next_move:
    aim=p.evaluate("()=>({x:player.x,target:c25Counter(boss)?hammerHeadPoint(boss).x:boss&&!boss.dead?boss.x+Math.sin(efxClock*.9)*65:340})")
    wanted='d' if aim['x']<aim['target']-12 else 'a' if aim['x']>aim['target']+12 else None
    if move!=wanted:
     if move:p.keyboard.up(move)
     if wanted:p.keyboard.down(wanted)
     move=wanted
    next_move=t+.3
   if t>26 and not firing:p.keyboard.down('j');firing=True
   r=p.evaluate("""()=>({time:efxClock,state:boss?._hammer?.state,hp:boss?.hp,armor:fr27Armor(boss)?.hp,radio:ui20Radio(),counter:c25Counter(boss),knock:boss?._hammer?.c25Knock?.t,scroll:_stage5SpaceScroll,player:{x:player.x,y:player.y},boss:{x:boss?.x,y:boss?.y}})""");r['videoSeconds']=round(t,3);timeline.append(r)
   # Missile is a normal input during the exposed charging window.
   if r['counter'] and t>missile_at and p.evaluate('Math.abs(player.x-hammerHeadPoint(boss).x)<24'):p.keyboard.press('k');missile_at=t+.8
   key=json.dumps([r['state'],(r.get('radio') or {}).get('who'),(r.get('radio') or {}).get('text')])
   if key!=last:
    print(json.dumps(r),flush=True);last=key
    if r['state'] in ['fr_activation','storm_raise','fr_stun']:p.screenshot(path=str(O/('gameplay-'+r['state']+f'-{int(t)}.png')))
   p.wait_for_timeout(300)
  p.keyboard.up('j')
  if move:p.keyboard.up(move)
  stats=p.evaluate("""async()=>{await new Promise(r=>{avRecorder.onstop=r;avRecorder.stop()});await avPending;avLive=false;return{...avStats,events:C25.events};}""");f.close();p.screenshot(path=str(O/'gameplay-end.png'));br.close()
finally:stop()
mp4=O/'stage5-furious-with-audio.mp4';subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-y','-loglevel','error','-i',str(raw),'-vf','fps=30','-af','volume=0.78','-c:v','libx264','-preset','fast','-crf','19','-c:a','aac','-b:a','160k','-pix_fmt','yuv420p','-movflags','+faststart',str(mp4)],check=True)
report=dict(difficulty='furious',pilot='cole',invulnerable=True,route='Continuous native debug boss entrance and combat, normal movement/fire/missile input; no state or animation injection.',audio=stats,errors=errors,timeline=timeline,video=str(mp4.relative_to(R)))
(O/'gameplay-recording.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf8');print(json.dumps(dict(video=str(mp4),peak=stats['peak'],errors=errors)),flush=True)
