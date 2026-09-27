"""Diagnose ordinary projectile access to all Sovereign generators."""
import ast,json,http.server
from pathlib import Path
import shoot as sh
from playwright.sync_api import sync_playwright
tree=ast.parse(Path('_BUILD_SOURCE/probe_polish_0927b.py').read_text(encoding='utf-8'))
SETUP=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id=='SETUP')
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
port,stop=sh.serve(sh.GAME);errors=[];rows=[]
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);p=br.new_page()
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('()=>window.__bofFrames>5');p.evaluate(sh.TRAP_RAF)
  for index in range(4):
   p.evaluate(SETUP,{'stage':4,'kind':'stormsovereign','mini':False,'diff':'normal'})
   rows.append(p.evaluate("""index=>{B.enter=false;B._noHit=false;B.x=worldWidth()/2;B.y=190;const R=B._er26;R.from={x:B.x,y:B.y};R.to={...R.from};R.mode='recover';R.dur=999;R.t=0;B._drawY=B.y;stage4ShieldSyncNodes(B);const H=B._s4war.shield,n=H.nodes[index];const before=H.nodes.map(n=>({x:n.x,y:n.y,hp:n.hp}));const y0=Math.min(VH-20,n.y+160);let fieldHits=0,nodeHits=0;const deflect=stage4ShieldDeflectBullet;stage4ShieldDeflectBullet=function(b,q){const r=deflect(b,q);if(r)fieldHits++;return r;};try{for(let i=0;i<120;i++){if(i%6===0)pBullets.push({kind:'mg',x:n.x,y:y0,w:4,h:12,dmg:8,vx:0,vy:-8,t:0,lv:3});updatePlay(1/60);}}finally{stage4ShieldDeflectBullet=deflect;}return {index,boss:{x:B.x,y:B.y,w:B.w,r:B.w*.67},y0,before,after:H.nodes.map(n=>({x:n.x,y:n.y,hp:n.hp,dead:n.dead})),fieldHits};}""",index))
  br.close()
finally:stop()
out={'rows':rows,'errors':errors};Path('_shots/overnight_0927/sovereign-access.json').write_text(json.dumps(out,indent=2),encoding='utf-8');print(json.dumps(out,indent=2))
assert not errors
