"""Tempest offscreen-return warning duration and native authored pixels."""
import ast, base64, http.server, json
from pathlib import Path
import shoot as sh
from playwright.sync_api import sync_playwright
OUT=Path('_shots/overnight_0927/tempest-return');OUT.mkdir(parents=True,exist_ok=True)
tree=ast.parse(Path('_BUILD_SOURCE/probe_polish_0927b.py').read_text(encoding='utf-8'))
SETUP=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id=='SETUP')
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
port,stop=sh.serve(sh.GAME);errors=[];cases=[]
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);p=br.new_page(viewport={'width':1100,'height':1100})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('()=>window.__bofFrames>5');p.evaluate(sh.TRAP_RAF)
  for diff in ['normal','hard','furious']:
   p.evaluate(SETUP,{'stage':6,'kind':'tempestbrothers','mini':True,'diff':diff})
   p.evaluate("""()=>{s6Opening=null;stageTimer=34;s6Wing.beats=1;special=null;powerups=[];const D=B._tempestDuo;window.P=D.ships[0];const s=P._ai,J=P._jet;D.ships[1]._ai.gone=true;D.striker=P;D.ai.player={x:450,y:750};s.boss.x=300;s.boss.y=1150;s.vulnerable=false;s.phase='chase';s.state='strafe';J.active=true;J.state='offscreen-turn';J.t=0;J.returnFrom={x:s.boss.x,y:s.boss.y};J.reentry={x:500,y:300};J.angle=Math.atan2((300-1150)*TLV_KY,(500-300)*TLV_KX)+Math.PI/2;tempestBrothersSync(B);l23FovWarm();}""")
   p.wait_for_timeout(400)
   samples=[]
   for step in [tempest_step for tempest_step in [.18,.18]]:
    samples.append(p.evaluate("""dt=>{tempestJetTick(B,P,dt);tempestBrothersSync(B);ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);return {t:P._jet.t,state:P._jet.state,warning:tempestJetReturnWarning(P)};}""",step))
   (OUT/(diff+'.png')).write_bytes(base64.b64decode(p.evaluate('()=>ctx.canvas.toDataURL()').split(',')[1]))
   r=p.evaluate("""()=>{const dur=tempestJetReturnDuration();tempestJetTick(B,P,dur-P._jet.t-.01);const before=P._jet.state;tempestJetTick(B,P,.02);const after=P._jet.state;tempestJetTick(B,P,.30);return {dur,before,after,cleared:tempestJetReturnWarning(P)===null};}""")
   cases.append({'diff':diff,'samples':samples,**r})
  br.close()
finally:stop()
(OUT/'report.json').write_text(json.dumps({'cases':cases,'errors':errors},indent=2),encoding='utf-8');print(json.dumps({'cases':cases,'errors':errors},indent=2))
assert not errors
assert all(c['before']=='offscreen-turn' and c['after']=='return' and c['cleared'] for c in cases)
