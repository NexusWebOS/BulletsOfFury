from pathlib import Path
import ast,json,time,base64,subprocess
import imageio_ffmpeg
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/rebel_wall_1026/stunt_video';O.mkdir(parents=True,exist_ok=True)
def strings(file):
 return [n.value for n in ast.walk(ast.parse((R/file).read_text(encoding='utf8'))) if isinstance(n,ast.Constant) and isinstance(n.value,str)]
SETUP=next(s for s in strings('_BUILD_SOURCE/probe_feedback_1002.py') if s.startswith('c=>{ht27Stop'))
INIT=next(s for s in strings('_BUILD_SOURCE/probe_rebel_balance_1019.py') if s.startswith('gang=>{window.R='))
AV=next(s for s in strings('_BUILD_SOURCE/record_chronos_original_spin_1025.py') if s.startswith('async()=>{') and 'window.avStats' in s)
AV=AV[:AV.index("   diffKey='furious'")]+"}"
port,stop=shoot.serve(str(R));errors=[]
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1280,'height':800});p.set_default_timeout(180000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>5');p.mouse.click(3,3);p.evaluate(shoot.TRAP_RAF)
  p.evaluate('()=>{run.stage=6;stageLoadBegin(6);rr26Warm();}')
  p.wait_for_function("()=>{stageLoadTick();return stageLoadReady(6)&&XART.rdy('rr26_wall')&&XART.rdy('rr26_box')}")
  p.evaluate(SETUP,dict(stage=6,kind='rebelsquad',diff='normal',pilot='cole'));p.evaluate(INIT,True)
  p.evaluate("""()=>{G.rescueDone=false;G.rescueAt=7;G.rd21.next=14;player.invuln=999999;player.fireCd=999999;for(const q of R.ships){q.x=camLeftX()+viewW()/2+(q.i-2)*76;q.y=PLAY.y+95+(q.i%2)*45;q.mode='fight';q.warp=0;q.rg4.cd=3+q.i;}const j=R.ships.find(q=>q.key==='jace');j.rg4.armed='helix';j.rg4.cd=1;const k=R.ships.find(q=>q.key==='kaia');k.rg4.armed='rockets';k.rg4.cd=2;const ro=R.ships.find(q=>q.key==='rook');ro.rg4.armed='slug';ro.rg4.cd=.5;const vo=R.ships.find(q=>q.key==='voss');vo.rg4.armed='fusion';vo.rg4.cd=4;rr26Warm();window.reviewCheckpoint='Central wall: solid divider / two-way reflection / 1015 glow';}""")
  p.wait_for_function('()=>REBEL_KEYS.every(k=>XART.rdy(AM13_ART[k].heading.key))')
  raw=O/'rebel-review.webm';f=raw.open('wb');p.expose_function('saveAVChunk',lambda x:f.write(base64.b64decode(x)))
  p.evaluate('()=>{window.requestAnimationFrame=window.__bofRealRAF;}');p.evaluate(AV);p.evaluate('()=>requestAnimationFrame(loop)')
  for i in range(45):
   p.wait_for_timeout(1000)
   p.evaluate('()=>{player.invuln=999999;player.fireCd=999999;}')
   if i in [2,9,16,28,40]:p.screenshot(path=str(O/f'review-{i}.png'))
  stats=p.evaluate("""async()=>{await new Promise(r=>{avRecorder.onstop=r;avRecorder.stop()});await avPending;avLive=false;return {...avStats,events:RR26.events,wall:!!G.rr26.wall,glow:PXG.log.pxg_rr26_wall_glow,hum:{ready:Snd.loops.rr26WallHum?.el.readyState,time:Snd.loops.rr26WallHum?.el.currentTime,on:Snd.loops.rr26WallHum?.on},boxes:s6Wing.boxes.map(o=>({key:o.key,wall:o._rr26Wall,hp:o.hp})),radio:G.rr26.queue,allies:s6Wing.ships.map(q=>({key:q.key,hp:q.hp}))};}""");f.close();b.close()
finally:stop()
mp4=O/'rebel-review.mp4';subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-v','error','-y','-i',str(raw),'-vf','fps=30','-c:v','libx264','-preset','fast','-crf','20','-c:a','aac','-pix_fmt','yuv420p',str(mp4)],check=True)
(O/'recording.json').write_text(json.dumps(dict(stats=stats,errors=errors),indent=2));print(json.dumps(dict(peak=stats['peak'],events=stats['events'],boxes=stats['boxes'],errors=errors)))
