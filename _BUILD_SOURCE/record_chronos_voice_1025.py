"""Audible native Furious pickup/fire plus clearly labelled rage checkpoints."""
from pathlib import Path
import ast,base64,json,time,subprocess
import imageio_ffmpeg
from playwright.sync_api import sync_playwright
from shoot import serve
R=Path(__file__).resolve().parents[1];O=R/'_shots/chronos_voice_1025/video';O.mkdir(parents=True,exist_ok=True)
def script(file,needle):
 return next(n.args[0].value for n in ast.walk(ast.parse((R/file).read_text(encoding='utf8'))) if isinstance(n,ast.Call) and n.args and isinstance(n.args[0],ast.Constant) and isinstance(n.args[0].value,str) and needle in n.args[0].value)
record=script('_BUILD_SOURCE/record_chronos_original_spin_1025.py','window.avStats=').replace('rec.start(1000);','window.startAV=()=>{window.avStartMs=performance.now();rec.start(1000)};')
record=record.replace('player.invuln=0;', 'player.invuln=0;run.spaceLevels=[5,5,5];run.spaceWeapon=1;window.reviewCheckpoint="Furious full fight - invulnerable capture, level 5 Fusion loadout";')
errors=[];timeline=[];port,stop=serve(str(R))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1280,'height':800})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' or 'draw error' in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>5',timeout=180000);p.mouse.click(3,3)
  p.evaluate('()=>{run.stage=5;stageLoadBegin(5);bi24Warm();ht23Warm();ch23Warm();UI20.warm();c25Warm();c26Warm();c27Warm();c29Warm();c30Warm();c32Warm();}')
  p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(5)&&bi24Warm()&&ht23Warm()&&ch23Warm()&&c25Warm()&&c26Warm()&&c27Warm()&&c29Warm()&&c30Warm()&&c32Warm()&&UI20_KEYS.every(k=>XART.rdy(k))}',timeout=180000)
  raw=O/'full-fight.webm';f=raw.open('wb');p.expose_function('saveAVChunk',lambda b:f.write(base64.b64decode(b)));p.evaluate(record);p.evaluate('startAV()');print('Capture started',flush=True)
  start=time.monotonic();last=None;move=None;firing=False;dead_at=None;rage_at=None;last_missile=0;scanning=False
  while time.monotonic()-start<900:
   t=time.monotonic()-start
   p.evaluate('player.invuln=999')
   q=p.evaluate("""()=>{const b=boss,h=b?._hammer;return{videoSeconds:(performance.now()-avStartMs)/1000,state:h?.state,hp:b?.hp,maxhp:b?.maxhp,armor:b?fr27Armor(b)?.hp:0,gun:h?.chainHP,dead:!!b?.dead,game:state,radio:ui20Radio(),intro:fb2IntroActive(),x:player.x,target:b?(c25Counter(b)?hammerHeadPoint(b).x:c29Gun(b)?ch23Mount(b).x:b.x):player.x,red:!!h?._hf22Red,charge:!!h?._hf22Charge,scale:b?hammerDepthScale(b):1,storm:C33.lastDraw,scroll:_stage5SpaceScroll}}""");timeline.append(q)
   (O/'telemetry.json').write_text(json.dumps(q),encoding='utf8')
   config=json.loads((O/'controls.json').read_text()) if (O/'controls.json').exists() else {}
   if config.get('stop'):break
   scan=q['state']=='chaingun' or config.get('scan',False)
   if scan!=scanning:
    (p.keyboard.down if scan else p.keyboard.up)('c');scanning=scan
   if q['dead'] and dead_at is None:dead_at=t
   if q['red'] and not q['charge'] and rage_at is None:rage_at=t
   # Keep firing off for one full rage rotation so both depths and wave are visible.
   wantfire=t%config.get('cycle',1.2)<config.get('hold',.85) and t>26 and not q['intro'] and not q['dead'] and not (rage_at is not None and t-rage_at<23)
   if wantfire!=firing:
    (p.keyboard.down if wantfire else p.keyboard.up)('j');firing=wantfire
   desired='d' if q['x']<q['target']-9 else 'a' if q['x']>q['target']+9 else None
   if move!=desired:
    if move:p.keyboard.up(move)
    if desired:p.keyboard.down(desired)
    move=desired
   if t-last_missile>2 and q['state'] in ['storm_raise','chaingun']:p.keyboard.press('k');last_missile=t
   key=(q['state'],(q['radio'] or {}).get('text'))
   if key!=last:
    print(json.dumps(q),flush=True);last=key
    p.screenshot(path=str(O/f"phase-{len(timeline)}-{q['state']}.png"))
   if dead_at is not None and t-dead_at>9:break
   if t>40 and q['game'] not in ['play','PLAY'] and not q['state']:break
   p.wait_for_timeout(150)
  p.keyboard.up('j');p.keyboard.up('c')
  if move:p.keyboard.up(move)
  stats=p.evaluate("""async()=>{await new Promise(r=>{avRecorder.onstop=r;avRecorder.stop()});await avPending;avLive=false;return{...avStats,cues:C33.events,god:DBGT.god,deaths:DBGT.stats?.deaths,dialogue:HT23.events}}""");f.close();br.close()
finally:stop()
video=O/'chronos-full-fight.mp4'
subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-v','error','-y','-i',str(raw),'-vf','fps=30','-af','volume=0.78','-c:v','libx264','-preset','fast','-crf','21','-c:a','aac','-b:a','160k','-pix_fmt','yuv420p','-movflags','+faststart',str(video)],check=True)
report=dict(difficulty='furious',invulnerable=True,loadout='level5 Fusion start',route='Continuous native encounter from alert/dialogue, no HP or phase injections. Invulnerable input-driven capture.',defeated=dead_at is not None,audio=stats,errors=errors,timeline=timeline,video=str(video.relative_to(R)))
(O/'review.json').write_text(json.dumps(report,indent=2),encoding='utf8');print(json.dumps(dict(video=str(video),defeated=dead_at is not None,audioPeak=stats['peak'],errors=errors)),flush=True)
