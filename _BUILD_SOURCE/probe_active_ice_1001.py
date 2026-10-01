from pathlib import Path
import sys,ast,json,base64,http.server
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'))
import shoot as sh
from playwright.sync_api import sync_playwright
tree=ast.parse((R/'_BUILD_SOURCE/probe_encounter_feedback_1001.py').read_text())
SETUP=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SETUP' for t in n.targets))
O=R/'_shots/encounter_feedback_1001';errors=[];port,stop=sh.serve(str(R));http.server.SimpleHTTPRequestHandler.log_message=lambda *a,**k:None
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(args=['--no-sandbox']);p=b.new_page()
  p.add_init_script("Object.defineProperty(navigator,'getGamepads',{value:()=>[]});")
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' or 'draw error' in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);p.wait_for_function('()=>window.__bofFrames>4',timeout=120000);p.evaluate(sh.TRAP_RAF)
  p.evaluate("()=>{er26Warm();for(const k of Object.keys(MR27_ART))XART.rdy('mr27_'+k);for(let i=0;i<8;i++)XART.rdy('mwfx_fireball_'+i);}")
  p.wait_for_function("()=>XART.rdy('mr27_rime')&&XART.rdy('l23fx_rime_laser_6')&&XART.rdy('mwfx_fireball_3')",timeout=120000)
  p.evaluate(SETUP,{'stage':3,'kind':'cryospear','diff':'normal'})
  p.evaluate("()=>{B._er26.neutralOpening=false;B._er26.form='neutral';er26Set(B,'cannon-relay');for(let i=0;i<200;i++){er26Tick(B,1/60);mr27Tick(B,1/60);}story=null;shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}")
  p.wait_for_timeout(300)
  p.evaluate('()=>{ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}')
  (O/'cryospear-active-beams.png').write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')))
  beam=p.evaluate('()=>({family:B._l23Beam.family,released:B._l23Beam.released,t:B._l23Beam.t,slots:B._l23Beam.slots,mounts:B._l23Beam.slots.map(s=>shipBossMount(B,s))})')
  p.evaluate("()=>{B._l23Beam=null;eBullets=[];for(let i=0;i<5;i++){er26Shot(B,'C',Math.PI/2,0,{large:i%2===0});const q=eBullets[eBullets.length-1];q.x=camLeftX()+50+i*90;q.y=300+(i%2)*65;q.t=.2+i*.08;}ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}")
  p.wait_for_timeout(200)
  p.evaluate('()=>{ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}')
  (O/'stage3-black-blue-rounds.png').write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')))
  out={'beam':beam,'errors':errors};(O/'active-ice.json').write_text(json.dumps(out,indent=2));print(json.dumps(out));b.close()
finally:stop()
