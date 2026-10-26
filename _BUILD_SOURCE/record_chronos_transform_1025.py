"""Audible native Furious pickup/fire plus clearly labelled rage checkpoints."""
from pathlib import Path
import ast,base64,json,time,subprocess
import imageio_ffmpeg
from playwright.sync_api import sync_playwright
from shoot import serve
R=Path(__file__).resolve().parents[1];O=R/'_shots/chronos_transform_1025/video';O.mkdir(parents=True,exist_ok=True)
def script(file,needle):
 return next(n.args[0].value for n in ast.walk(ast.parse((R/file).read_text(encoding='utf8'))) if isinstance(n,ast.Call) and n.args and isinstance(n.args[0],ast.Constant) and isinstance(n.args[0].value,str) and needle in n.args[0].value)
record=script('_BUILD_SOURCE/record_chronos_original_spin_1025.py','window.avStats=').replace('rec.start(1000);','window.startAV=()=>{window.avStartMs=performance.now();rec.start(1000)};')
record=record.replace('player.invuln=0;', 'player.invuln=0;run.spaceLevels=[5,5,5];run.spaceWeapon=1;window.reviewCheckpoint="Rage showcase - native attacks after transformation checkpoint";')
errors=[];timeline=[];port,stop=serve(str(R))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1280,'height':800})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' or 'draw error' in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>5',timeout=180000);p.mouse.click(3,3)
  p.evaluate('()=>{run.stage=5;stageLoadBegin(5);bi24Warm();ht23Warm();ch23Warm();UI20.warm();c25Warm();c26Warm();c27Warm();c29Warm();c30Warm();c32Warm();}')
  p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(5)&&bi24Warm()&&ht23Warm()&&ch23Warm()&&c25Warm()&&c26Warm()&&c27Warm()&&c29Warm()&&c30Warm()&&c32Warm()&&UI20_KEYS.every(k=>XART.rdy(k))}',timeout=180000)
  raw=O/'full-fight.webm';f=raw.open('wb');p.expose_function('saveAVChunk',lambda b:f.write(base64.b64decode(b)));p.evaluate(record);p.evaluate('startAV()');print('Capture started',flush=True)
  seed=script('_BUILD_SOURCE/audit_chronos_aura_gun_1025.py','window.seedGun=')
  p.evaluate("()=>{spawnBoss('chromehammer');debugFight.spawned=true;warnT=0;bossActive=true;}")
  p.evaluate(seed)
  p.evaluate("()=>{seedGun();const h=boss._hammer;h.hb20Pickup=h.c29Break=h.c25Knock=h.recovery=null;h._hf22Red=false;h._hf22Charge=null;h.c30=null;boss.hp=boss.maxhp*.15;h.c27RagePending=true;boss.x=240;boss.y=190;hf22BeginBlueRage(boss);}")
  start=time.monotonic();last=None
  while time.monotonic()-start<50:
   p.evaluate('player.invuln=999;DBGT.god=true')
   q=p.evaluate("()=>({t:(performance.now()-avStartMs)/1000,state:boss._hammer.state,phase:boss._hammer.c30?.phase,depth:boss._hammer.c30?.volley?.depth,charge:!!boss._hammer._hf22Charge,transform:C43.lastCharge,throw:C43.lastThrow,orb:c42Active(boss),cycle:boss._hammer.c30?.cycle,storm:C33.lastDraw})");timeline.append(q)
   key=(q['state'],q.get('depth'))
   if key!=last:p.screenshot(path=str(O/f'phase-{len(timeline)}.png'));print(json.dumps(q),flush=True);last=key
   p.wait_for_timeout(150)
  stats=p.evaluate("async()=>{await new Promise(r=>{avRecorder.onstop=r;avRecorder.stop()});await avPending;avLive=false;return {...avStats,cues:C33.events}}")
  f.close();br.close()
finally:stop()
video=O/'rage-showcase.mp4'
subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-v','error','-y','-i',str(raw),'-vf','fps=30','-c:v','libx264','-preset','fast','-crf','21','-c:a','aac','-pix_fmt','yuv420p','-movflags','+faststart',str(video)],check=True)
checks={'transformation':any(q['charge'] for q in timeline),'foreground':any(q.get('depth')=='foreground' and q.get('phase')=='volley_fire' for q in timeline),'background':any(q.get('depth')=='background' and q.get('phase')=='volley_fire' for q in timeline),'orb_wave':any(q.get('phase')=='beam' for q in timeline),'hand_wave':any(q.get('phase')=='beam' and not q.get('orb') for q in timeline),'orb_blast':any(q.get('phase')=='beam' and q.get('orb') for q in timeline),'single_strike':all((q.get('storm') or {}).get('bolts',0)<=1 for q in timeline),'audio':stats['peak']>0,'no_errors':not errors}
(O/'review.json').write_text(json.dumps(dict(checks=checks,timeline=timeline,audio=stats,errors=errors),indent=2));print(checks,flush=True)
assert all(checks.values())
