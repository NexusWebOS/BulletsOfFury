"""Verify direct Harrier mount paths in the actual renderer."""
import ast,base64,http.server,json
from pathlib import Path
from playwright.sync_api import sync_playwright
import shoot as sh
OUT=Path('_shots/director_0927');errors=[];rows=[]
tree=ast.parse(Path('_BUILD_SOURCE/probe_polish_0927b.py').read_text(encoding='utf-8'))
SETUP=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(getattr(t,'id',None)=='SETUP' for t in n.targets))
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
port,stop=sh.serve(sh.GAME)
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);p=br.new_page();p.set_default_timeout(90000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('()=>window.__bofFrames>4');p.evaluate(sh.TRAP_RAF)
  p.evaluate(SETUP,{'stage':6,'mini':True,'kind':'chaosharrier','diff':'hard'})
  p.wait_for_function("()=>['ch2_hull_0','ch2_gun_0','ch2_emitter_0','ch2_thruster_0','d27_ballistic','d27_specialist','d27_energy'].every(k=>XART.rdy(k))")
  p.evaluate("()=>{story=null;s6Opening=null;s6Wing=null;B._chVisible=true;B._chState='idle';B.x=worldWidth()/2;B.y=B.ty=165;player.invuln=0;window.directorHarrierDraw=wm26Draw;window.directorFamilies=[];wm26Draw=function(...args){directorFamilies.push(args[1]);return directorHarrierDraw(...args);};}")
  for family,slot in [('missile','left_missile_bay'),('plasma','central_reactor'),('sidelaser','right_cannon')]:
   r=p.evaluate("""c=>{B._chFlashes=[];eBullets=[];directorFamilies=[];chaosHarrierShot(B,c.family,c.slot,Math.PI/2,3);for(const f of B._chFlashes)f.t=.05;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);return {source:c.family,slot:c.slot,rendered:[...new Set(directorFamilies)],png:ctx.canvas.toDataURL()};}""",{'family':family,'slot':slot})
   (OUT/f'harrier-{family}.png').write_bytes(base64.b64decode(r.pop('png').split(',')[1]));rows.append(r)
  br.close()
finally:stop()
report={'routes':rows,'errors':errors};(OUT/'harrier.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report,indent=2))
assert not errors,errors
assert all(expected in r['rendered'] for expected,r in zip(['missile','orb','laser'],rows))
