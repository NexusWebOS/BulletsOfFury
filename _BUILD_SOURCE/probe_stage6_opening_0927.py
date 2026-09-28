import base64,json,sys,http.server
from pathlib import Path
from playwright.sync_api import sync_playwright
import shoot as sh
ROOT=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path(sh.GAME)
OUT=Path(sh.GAME)/'_shots/repair_0927';OUT.mkdir(parents=True,exist_ok=True)
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
port,stop=sh.serve(str(ROOT));errors=[];report={}
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(args=['--no-sandbox','--mute-audio','--autoplay-policy=no-user-gesture-required'])
  p=b.new_page(viewport={'width':1100,'height':1200});p.set_default_timeout(120000)
  p.on('pageerror',lambda e:errors.append(str(e)))
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('()=>window.__bofFrames>4');p.evaluate(sh.TRAP_RAF);p.wait_for_timeout(50)
  p.evaluate("()=>{run.pilot='yuri';pilotIndex=PILOTS.findIndex(p=>p.key==='yuri');run.mode='arcade';beginStage(6);story=null;stagePlan=[];waveIdx=999;enemies=[];player.invuln=0;player._spawnClearT=0;setState(GS.LAUNCH);window.openingBeeps=0;Audio.SFX.retinaLockBeep=()=>window.openingBeeps++;}")
  p.evaluate('()=>{window.qaS6Step=()=>{updatePlay(1/60);drawWorld(1/60);};}')
  p.wait_for_function("()=>['ship_yuri','whv_ace','nhud_bar','retm_0'].every(k=>XART.rdy(k))")
  def snap(name):
   p.evaluate('()=>{const inv=player.invuln;player.invuln=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);player.invuln=inv;}')
   (OUT/(name+'.png')).write_bytes(base64.b64decode(p.evaluate('()=>ctx.canvas.toDataURL()').split(',')[1]))
  report['entry']=p.evaluate("()=>{drawLaunch(1/60);return{state,who:s6Opening.radio.who,locked:s6OpeningControlsLocked(),alpha:s6OpeningHudAlpha(),y:player.y};}")
  report['flyin']=p.evaluate("()=>{let maxStep=0,prev=player.y;for(let i=0;i<200;i++){window.qaS6Step();maxStep=Math.max(maxStep,Math.abs(player.y-prev));prev=player.y;}return{maxStep,y:player.y,alpha:s6OpeningHudAlpha(),enemies:enemies.length,scroll:_stage6SkyScroll};}")
  snap('stage6-locked-dialogue')
  p.evaluate('()=>{for(let i=0;i<140;i++)window.qaS6Step();}')
  report['threat']=p.evaluate("()=>({who:s6Opening.radio.who,beeps:window.openingBeeps,lock:playerLocks[0]?.state,from:playerLocks[0]?.acquireFrom,age:playerLocks[0]?.t})")
  snap('stage6-descending-retina')
  p.evaluate('()=>{for(let i=0;i<325;i++)window.qaS6Step();}')
  report['maverick']=p.evaluate("()=>({who:s6Opening.radio.who,text:s6Opening.radio.full,lock:playerLocks[0]?.state,beeps:window.openingBeeps})")
  snap('stage6-cloaking-radio')
  p.evaluate('()=>{for(let i=0;i<720;i++)window.qaS6Step();}')
  snap('stage6-uncloaking-pass')
  p.evaluate('()=>{while(s6Opening.launched<2)window.qaS6Step();}')
  report['launch']=p.evaluate("()=>({phase:s6Opening.phase,locked:s6OpeningControlsLocked(),shots:s6Opening.shots.map(m=>({vx:m.vx,vy:m.vy,y:m.y,lock:m._lockId})),beeps:window.openingBeeps})")
  snap('stage6-upward-missiles')
  report['curve']=p.evaluate("()=>{player.invuln=999;const trail=[];for(let i=0;i<50;i++){window.qaS6Step();if(i%15===0)trail.push(s6Opening.shots.map(m=>({x:m.x,y:m.y,vx:m.vx,vy:m.vy,dead:!!m.dead})));}return trail;}")
  snap('stage6-curving-missiles')
  report['impact']=p.evaluate("()=>{const m=s6Opening.shots.find(m=>!m.dead);if(!m)return{missing:true};const before=explosions.length;pBullets.push({x:m.x,y:m.y,vx:0,vy:0,w:60,h:60,dmg:1,kind:'bullet',life:2,t:0});window.qaS6Step();return{dead:m.dead,impact:m._impactDone,explosions:explosions.length-before};}")
  snap('stage6-missile-interception')
  report['errors']=errors;(OUT/'stage6-opening-probe.json').write_text(json.dumps(report,indent=2));b.close()
finally:stop()
print(json.dumps(report,indent=2))
assert not errors,errors
assert report['entry']['locked'] and report['entry']['alpha']<.02
assert report['flyin']['maxStep']<2 and report['flyin']['alpha']==1 and report['flyin']['enemies']==0
assert report['threat']['who']=='COLE' and report['threat']['from'] and report['threat']['beeps']>0
assert report['maverick']['who']=='MAVERICK' and report['maverick']['lock']=='arming'
assert len(report['launch']['shots'])==2 and all(m['vy']<0 and m['lock'] for m in report['launch']['shots'])
assert any(m['vy']>0 and not m['dead'] for frame in report['curve'] for m in frame)
assert report['impact']['dead'] and report['impact']['impact'] and report['impact']['explosions']>0
