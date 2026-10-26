"""Audible native Furious pickup/fire plus clearly labelled rage checkpoints."""
from pathlib import Path
import ast,base64,json,time,subprocess
import imageio_ffmpeg
from playwright.sync_api import sync_playwright
from shoot import serve
R=Path(__file__).resolve().parents[1];O=R/'_shots/chronos_volley_1025/video';O.mkdir(parents=True,exist_ok=True)
def script(file,needle):
 return next(n.args[0].value for n in ast.walk(ast.parse((R/file).read_text(encoding='utf8'))) if isinstance(n,ast.Call) and n.args and isinstance(n.args[0],ast.Constant) and isinstance(n.args[0].value,str) and needle in n.args[0].value)
record=script('_BUILD_SOURCE/record_chronos_original_spin_1025.py','window.avStats=').replace('rec.start(1000);','window.startAV=()=>{window.avStartMs=performance.now();rec.start(1000)};')
seed=script('_BUILD_SOURCE/audit_chronos_aura_gun_1025.py','window.seedGun=')
errors=[];timeline=[];port,stop=serve(str(R))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1280,'height':800})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' or 'draw error' in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>5',timeout=180000);p.mouse.click(3,3)
  p.evaluate('()=>{run.stage=5;stageLoadBegin(5);bi24Warm();ht23Warm();ch23Warm();UI20.warm();c25Warm();c26Warm();c27Warm();c29Warm();c30Warm();c32Warm();}')
  p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(5)&&bi24Warm()&&ht23Warm()&&ch23Warm()&&c25Warm()&&c26Warm()&&c27Warm()&&c29Warm()&&c30Warm()&&c32Warm()&&UI20_KEYS.every(k=>XART.rdy(k))}',timeout=180000)
  raw=O/'review.webm';f=raw.open('wb');p.expose_function('saveAVChunk',lambda b:f.write(base64.b64decode(b)));p.evaluate(record)
  p.evaluate("()=>{spawnBoss('chromehammer');debugFight.spawned=true;warnT=0;bossActive=true;}");p.evaluate(seed)
  p.evaluate("""()=>{const h=boss._hammer;h.c29Break=null;h.c30=null;h.hb20Pickup=null;h.hb20PickupDone=true;h.frArmor.hp=0;boss.hp=boss.maxhp*.15;h.hammerDestroyed=false;h.state='hammer';h.mode='hammer';h.c27RagePending=false;boss.x=340;boss.y=250;window.reviewCheckpoint='15% HP checkpoint: rage charge, foreground and background palm volleys';startAV();}""")
  start=time.monotonic();phase=0;last=None;move=None
  while time.monotonic()-start<32:
   t=time.monotonic()-start
   desired='a' if int(t/2)%2 else 'd'
   if move!=desired:
    if move:p.keyboard.up(move)
    p.keyboard.down(desired);move=desired
   q=p.evaluate("""()=>({videoSeconds:(performance.now()-avStartMs)/1000,state:boss._hammer.state,t:boss._hammer.t,pickup:boss._hammer.hb20Pickup?.t,bodyFrame:ch23Armed(boss)?ch23BodyFrame(boss):null,rotor:ch23Armed(boss)?ch23GunFrame(boss):null,rev:boss._hammer.ch23Rev,red:hf22Red(boss),pose:ha21Blue(boss)?.kind,auraDraws:C27.auraDraws,checkpoint:window.reviewCheckpoint,playerDead:player.dead,radio:ui20Radio(),depth:boss._hammer.c30?.volley?.depth,scale:hammerDepthScale(boss),handShots:C32.events.filter(e=>e.type==='palm-shot').length})""");q['videoSeconds']=round(q['videoSeconds'],3);timeline.append(q)
   p.evaluate("window.reviewCheckpoint=boss._hammer._hf22Charge?'15% HP checkpoint: full rage charge':boss._hammer.c30?.volley?'Red rage: '+boss._hammer.c30.volley.depth+' palm laser barrage':'Red rage: two-handed red-white energy wave'")
   if q['state']!=last:
    last=q['state'];print(json.dumps(dict(time=round(t,2),state=last,red=q['red'])),flush=True)
    p.screenshot(path=str(O/f'{phase}-{last}.png'))
   p.wait_for_timeout(130)
  if move:p.keyboard.up(move)
  stats=p.evaluate("""async()=>{await new Promise(r=>{avRecorder.onstop=r;avRecorder.stop()});await avPending;avLive=false;return{...avStats,events:HT23.events,commitmentEvents:C29.events,gunEvents:CH23.events,rageEvents:C27.events,palmEvents:C32.events,god:DBGT.god,deaths:DBGT.stats?.deaths}}""");f.close();br.close()
finally:stop()
video=O/'chronos-volley.mp4'
subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-v','error','-y','-i',str(raw),'-vf','fps=30','-af','volume=0.78','-c:v','libx264','-preset','fast','-crf','19','-c:a','aac','-b:a','160k','-pix_fmt','yuv420p','-movflags','+faststart',str(video)],check=True)
report=dict(difficulty='furious',invulnerable=True,route='Furious focused native rage review:15% charge, foreground alternating/dual palm volleys, background palm volleys, existing red-white wave, repeat. Checkpoint changes are explicitly labelled. Not a continuous full-fight clear.',audio=stats,errors=errors,timeline=timeline,video=str(video.relative_to(R)))
(O/'review.json').write_text(json.dumps(report,indent=2),encoding='utf8');print(json.dumps(dict(video=str(video),audioPeak=stats['peak'],errorCount=len(errors),firstError=errors[0] if errors else None)),flush=True)
