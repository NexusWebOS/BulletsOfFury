"""Real engine followup release, warnings and two-player targeting fixtures."""
from pathlib import Path
import json,sys,base64
from playwright.sync_api import sync_playwright
sys.path.insert(0,str(Path(__file__).resolve().parent));import shoot as sh
R=Path(__file__).resolve().parents[1];O=R/'_shots/finale_ai_1006';O.mkdir(exist_ok=True)
SETUP=(R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text(encoding='utf-8').split('SETUP="""')[1].split('"""')[0]
checks=[];errors=[];coverage=[];port,stop=sh.serve(str(R))
def ck(v,n):checks.append({'ok':bool(v),'name':n});print(('PASS ' if v else 'FAIL ')+n,flush=True)
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox']);p=br.new_page()
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' or 'draw error' in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);p.wait_for_function('()=>window.__bofFrames>4',timeout=120000);p.evaluate(sh.TRAP_RAF);p.evaluate('()=>r30Warm()')
  p.wait_for_function('()=>Object.values(FMC_ART).every(a=>XART.rdy(a.key))',timeout=120000)
  for form in [1,2,3,4,6,7]:
   p.evaluate(SETUP,{'stage':8,'kind':'vileexistence','pilot':'yuri','diff':'furious'})
   p.evaluate('(i)=>{j3Encounter(B,2);j3Mimic(B,i);on5FightStart(B);window.J=j3State(B);window.S=B._r30;window.D=gd4Create(B,i);D.aa5Cd=0;F6.events=[];window.released=false;}',form)
   for i in range(40):
    p.evaluate('()=>{for(let j=0;j<10;j++){updatePlay(.05);if(eBullets.some(q=>q._f6Owner===B))released=true;}ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}')
    p.wait_for_timeout(4)
    if p.evaluate('()=>released'):break
   ck(p.evaluate('()=>released'),f'copy {form} really releases its newly warned authored ordnance')
   data=p.evaluate('()=>({keys:fmcRig(B).map(v=>v.key),events:F6.events,shots:eBullets.filter(q=>q._f6Owner===B).map(q=>({kind:q._finale1003b,module:q._fmcModule,x:q.x,y:q.y}))})');coverage.append({'form':form,**data})
   (O/f'followup-{form}.png').write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')))
  p.evaluate(SETUP,{'stage':8,'kind':'vileexistence','pilot':'yuri','diff':'furious'})
  ck(p.evaluate('()=>{j3Encounter(B,2);coopOn=true;player2.reset();player.dead=player2.dead=false;player.x=110;player2.x=370;B._r30.f6Seat=0;const a=f6Target(B),b=f6Target(B);const ok=a.seat===1&&b.seat===2&&a.x===110&&b.x===370&&_seat===1;coopOn=false;return ok;}'),'co-op alternates live pilot targets and restores the active seat')
  ck(not errors,'zero followup browser or renderer errors');br.close()
finally:
 stop();(R/'docs/qa/finale_followups_1006.json').write_text(json.dumps({'checks':checks,'errors':errors,'coverage':coverage,'limitations':'Protected native fixtures, not an unassisted clear.'},indent=2),encoding='utf-8')
if errors or any(not q['ok'] for q in checks):raise SystemExit(1)
