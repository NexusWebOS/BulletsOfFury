"""Record native game selection and the shared Lizzie dialogue renderer."""
from pathlib import Path
import base64,json
from playwright.sync_api import sync_playwright
import shoot as sh
R=Path(__file__).resolve().parents[1];O=R/'_shots/map_briefing_1003g'
port,stop=sh.serve(str(R));errors=[]
def start(p):
 p.evaluate("()=>{window.movieChunks=[];window.movieRecorder=new MediaRecorder(cv.captureStream(24),{mimeType:'video/webm;codecs=vp9',videoBitsPerSecond:1600000});movieRecorder.ondataavailable=e=>{if(e.data.size)movieChunks.push(e.data);};movieRecorder.start();}")
def finish(p,name):
 data=p.evaluate("()=>new Promise(resolve=>{movieRecorder.onstop=()=>{const f=new FileReader();f.onload=()=>resolve(f.result.split(',')[1]);f.readAsDataURL(new Blob(movieChunks,{type:'video/webm'}));};movieRecorder.stop();})")
 (O/name).write_bytes(base64.b64decode(data))
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);p=b.new_page(viewport={'width':1366,'height':768})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('()=>window.__bofFrames>3',timeout=120000)
  p.evaluate("()=>{run.mode='campaign';run.pilot='lizzie';campaign.unlockedMax=8;campaign.rank={1:'S',2:'A'};campaign.bonusUnlocked=false;campaign.rivalScattered=false;openStageSelect(1,{});sselBoot=0;sselUnlockCine=null;cmap2Warm();mapgWarm();XART.rdy('dlg_rect_0914');}")
  p.wait_for_function("()=>cmap2Keys().every(k=>XART.rdy(k))&&XART.rdy('mapg_briefing')&&XART.rdy('comm_lizzie_talk-wide')&&XART.rdy('dlg_rect_0914')",timeout=60000)
  p.wait_for_timeout(1800);p.evaluate("()=>{MAPG.typing=null;}");start(p)
  for n in range(12):
   if n in [4,8]:p.evaluate("()=>Input.injectTap('arrowright')")
   p.wait_for_timeout(1000)
  finish(p,'map-motion.webm')
  p.evaluate(sh.TRAP_RAF);p.wait_for_timeout(80);p.evaluate("()=>{setState(GS.CUTSCENE);}");p.evaluate(sh.STEP,1)
  start(p)
  for n in range(175):
   p.evaluate("""n=>{ctx.setTransform(SS,0,0,SS,0,0);ctx.fillStyle='#071322';ctx.fillRect(0,0,cv.width/SS,VH);const text='Ready when you are. Pick our next target and let us give them something to remember.';const shown=text.slice(0,Math.min(text.length,Math.floor(n*.7)));dlgBox({who:'LIZZIE',full:text,shown,forceShown:true});const k=commPortrait('lizzie',shown.length<text.length?'talk':'idle');ctx.drawImage(XART.get(k),164,110,152,152);}""",n)
   p.wait_for_timeout(35)
  finish(p,'lizzie-motion.webm');(O/'motion-errors.json').write_text(json.dumps(errors),encoding='utf-8');b.close()
finally:stop()
print(json.dumps({'videos':['map-motion.webm','lizzie-motion.webm'],'errors':errors}))
assert not errors,errors
