"""Verify the final death transition and tell-only knight warning pixels."""
from pathlib import Path
import json,base64
from playwright.sync_api import sync_playwright
import shoot as sh
R=Path(__file__).resolve().parents[1];O=R/'_shots/gameplay_audit_1004/cinematic';O.mkdir(parents=True,exist_ok=True)
SETUP=(R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text(encoding='utf-8').split('SETUP="""')[1].split('"""')[0]
errors=[];report={}
def frames(p,n,code):
 for i in range(0,n,20):
  p.evaluate('(n)=>{for(let i=0;i<n;i++){'+code+'}}',min(20,n-i));p.wait_for_timeout(8)
def shot(p,name):
 p.evaluate('()=>{ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}')
 (O/(name+'.png')).write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')))
port,stop=sh.serve(str(R))
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(args=['--no-sandbox']);p=b.new_page(viewport={'width':1100,'height':950})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' or 'draw error' in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);p.wait_for_function('()=>window.__bofFrames>4',timeout=120000);p.evaluate(sh.TRAP_RAF)
  p.evaluate('()=>{h3Warm();r30Warm();for(let i=0;i<16;i++)XART.rdy("nsd_ring_"+i);}')
  p.wait_for_function('()=>H3_ART.every(k=>XART.rdy("h3_"+k))&&Object.values(FMC_ART).every(a=>XART.rdy(a.key))',timeout=120000)
  p.evaluate(SETUP,{'stage':5,'kind':'chromehammer','diff':'furious'})
  p.evaluate('()=>{bossDie();}')
  report['death']=[];last=0
  for t in [1,3,5,6.2,7.7,8.5]:
   frames(p,round((t-last)*60),'updatePlay(1/60);');last=t;shot(p,'death-'+str(t))
   report['death'].append(p.evaluate('()=>({phase:H3.ending.phase,engineAge:H3.ending.engineDeath,bodyAge:B.dying,rings:_smokeRings.length,white:whiteBlast})'))
  p.evaluate(SETUP,{'stage':8,'kind':'vileexistence','diff':'furious'})
  p.evaluate('()=>{H3.ending=null;j3Encounter(B,2);j3Mimic(B,5);B._r30.mode="fight";const D=gd4Create(B,5);D.p._hammer.state="recover";D.p._hammer.t=.25;window.oldWarning= combatWarningDraw;window.warningCalls=0;combatWarningDraw=function(){warningCalls++;return oldWarning.apply(this,arguments);};}')
  shot(p,'knight-recover');report['recoverWarnings']=p.evaluate('()=>warningCalls')
  p.evaluate('()=>{j3State(B).gp4Donors[5].p._hammer.state="warn";warningCalls=0;}');shot(p,'knight-tell');report['tellWarnings']=p.evaluate('()=>warningCalls')
  b.close()
finally:stop()
report['errors']=errors;(O/'report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
