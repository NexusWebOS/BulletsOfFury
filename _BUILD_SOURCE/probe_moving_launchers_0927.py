"""Native moving-launcher warning/release geometry, with actual game rendering."""
import ast,base64,http.server,json
from pathlib import Path
import shoot as sh
from playwright.sync_api import sync_playwright
OUT=Path('_shots/overnight_0927/moving-launchers');OUT.mkdir(parents=True,exist_ok=True)
tree=ast.parse(Path('_BUILD_SOURCE/probe_polish_0927b.py').read_text(encoding='utf-8'))
SETUP=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id=='SETUP')
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
port,stop=sh.serve(sh.GAME);errors=[];report={}
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);p=br.new_page(viewport={'width':1100,'height':1100})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('()=>window.__bofFrames>5');p.evaluate(sh.TRAP_RAF)
  p.evaluate(SETUP,{'stage':2,'kind':'magmaward','mini':True,'diff':'furious'})
  p.evaluate("""()=>{B.enter=false;B.x=worldWidth()/2;B.y=150;er26Init(B);er26Set(B,'charred-battery');er26Combat(B,.01);window.Q=polishLanes.slice();window.start=Q.map(q=>({x:q.x,y:q.y,angle:q.angle}));B.x-=72;B.y+=15;for(const q of Q)q.t=.6;for(let i=0;i<8;i++)XART.rdy('ship_cole_'+i);}""")
  for _ in range(8):
   p.evaluate('()=>{ctx.setTransform(SS,0,0,SS,0,0);drawWorld(.016);}')
   p.wait_for_timeout(100)
  (OUT/'magma-moved.png').write_bytes(base64.b64decode(p.evaluate('()=>ctx.canvas.toDataURL()').split(',')[1]))
  report['mounts']=p.evaluate("""()=>Q.map((q,i)=>{const mount=shipBossMount(B,q.mount);return {slot:q.mount,warning:{x:q.x,y:q.y},mount,match:Math.hypot(q.x-mount.x,q.y-mount.y)<.001,moved:Math.hypot(q.x-start[i].x,q.y-start[i].y)>60,angleCommitted:q.angle===start[i].angle};})""")
  report['release']=p.evaluate("""()=>{eBullets=[];polishCombatTick(1);return Q.map(q=>({slot:q.mount,shots:eBullets.filter(p=>Math.hypot(p.x-q.x,p.y-q.y)<.001).length}));}""")
  p.evaluate(SETUP,{'stage':5,'kind':'siegebomber','mini':True,'diff':'hard'})
  report['bomber']=p.evaluate("""()=>{B.enter=false;B.x=350;B.y=150;polishReset();eBullets=[];const q=polishLane(B,B.x+B.w*.42,B.y+15,Math.PI/2,{warn:1.1,speed:4.9});B.x-=46;B.y+=23;polishCombatTick(.8);const warningMatch=q.x===B.x+B.w*.42&&q.y===B.y+15;polishCombatTick(.4);return {warningMatch,releaseMatch:eBullets.length===1&&eBullets[0].x===q.x&&eBullets[0].y===q.y,committed:eBullets[0]?._committed};}""")
  report['errors']=errors;br.close()
finally:stop()
(OUT/'report.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report,indent=2))
assert not errors,errors
assert len(report['mounts'])==2 and all(x['match'] and x['moved'] and x['angleCommitted'] for x in report['mounts'])
assert all(x['shots']==5 for x in report['release'])
assert all(report['bomber'].values())
