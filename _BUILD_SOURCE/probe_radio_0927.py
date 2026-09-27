"""Native HUD radio geometry, paging and special-priority check."""
import ast, base64, http.server, json
from pathlib import Path
import shoot as sh
from playwright.sync_api import sync_playwright

OUT=Path('_shots/overnight_0927/radio');OUT.mkdir(parents=True,exist_ok=True)
tree=ast.parse(Path('_BUILD_SOURCE/probe_polish_0927b.py').read_text(encoding='utf-8'))
SETUP=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id=='SETUP')
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
port,stop=sh.serve(sh.GAME);errors=[];report={}
def shot(p,name):
 (OUT/(name+'.png')).write_bytes(base64.b64decode(p.evaluate('()=>{ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);return ctx.canvas.toDataURL();}').split(',')[1]))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);p=br.new_page(viewport={'width':1100,'height':1100})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('()=>window.__bofFrames>5');p.evaluate(sh.TRAP_RAF)
  p.evaluate(SETUP,{'stage':6,'kind':'tempestbrothers','mini':True,'diff':'normal'})
  p.evaluate("()=>{s6Opening=null;stageTimer=34;special=null;s6Wing.beats=1;story=null;commPortrait('decker','idle');dialogueFrame('DECKER','#7bd4ff');}")
  for _ in range(6):p.evaluate('()=>{for(let i=0;i<60;i++)updatePlay(1/60);ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}') ;p.wait_for_timeout(50)
  p.wait_for_function("()=>bmfReady('dialogue')&&XART.rdy(commPortrait('decker','idle'))")
  report=p.evaluate("""()=>{story=null;special=null;s6WingSay('DECKER','WATCH THEIR NOSES. MOVE OUT OF THE MARKED LANE WHEN THE WARNING LOCKS. YOUR WING IS STILL WITH YOU.');const L=s6Wing.line,pages=s6WingRadioPages(L);const r=bottomHudLayout().ability;L.t=pages[0].text.length/34+1;return {rect:r,rail:bottomHudLayout().rail,pages,full:L.full,visible:s6WingRadioVisible()};}""")
  shot(p,'page-one')
  report['second']=p.evaluate("()=>{const L=s6Wing.line,p=s6WingRadioPages(L);L.t=p[0].dur+p[1].text.length/34+1;return {page:1,t:L.t};}")
  shot(p,'page-two')
  report['priority']=p.evaluate("()=>{const t=s6Wing.line.t;special={pilot:'maverick',t:8,dur:10};s6WingRadioTick(s6Wing,3);return {hidden:!s6WingRadioVisible(),paused:s6Wing.line.t===t};}")
  shot(p,'special-priority')
  report['resume']=p.evaluate("()=>{special=null;const L=s6Wing.line,t=L.t;s6WingRadioTick(s6Wing,.1);return {visible:s6WingRadioVisible(),advanced:Math.abs(L.t-t-.1)<1e-8};}")
  report['finished']=p.evaluate("()=>{s6WingRadioTick(s6Wing,100);return !s6Wing.line;}")
  br.close()
finally:stop()
report['errors']=errors;(OUT/'report.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report,indent=2))
assert not errors
assert report['priority']['hidden'] and report['priority']['paused'] and report['resume']['advanced'] and report['finished']
assert ' '.join(p['text'].replace('\n',' ') for p in report['pages'])==report['full']
assert report['rect']['y']>=report['rail']['y'] and report['rect']['y']+report['rect']['h']<=report['rail']['y']+report['rail']['h']
