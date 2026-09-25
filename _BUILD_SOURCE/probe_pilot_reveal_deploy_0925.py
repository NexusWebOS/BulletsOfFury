"""Confirm one pilot-screen press finishes card reveal and starts deployment."""
import base64,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import shoot as sh
from playwright.sync_api import sync_playwright

out=Path('_shots/pilot_reveal_deploy_0925');out.mkdir(parents=True,exist_ok=True)
port,stop=sh.serve(sh.GAME);errors=[]
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--disable-gpu','--no-sandbox','--mute-audio'])
  pg=br.new_page(viewport={'width':1100,'height':1200})
  pg.on('pageerror',lambda e:errors.append(str(e)))
  pg.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  pg.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load')
  pg.wait_for_function('()=>(window.__bofFrames|0)>4');pg.evaluate(sh.TRAP_RAF)
  pg.evaluate("()=>{run.mode='arcade';}")
  pg.evaluate(sh.SETUP,{'state':'PILOT','pilot':'axel'})
  pg.evaluate(sh.STEP,8)
  result=pg.evaluate("""()=>{const before={done:!!(pcard&&pcard.done),pending:pilotPending};
    if(!pcard)pcStart(PILOTS[pilotIndex].key);
    pcard.done=false;pcard.phase='text';pcard.typed=0;
    const old=Input.tap;Input.tap=k=>k==='enter';
    try{drawPilot(1/60);}finally{Input.tap=old;}
    return {before,after:{done:pcard.done,phase:pcard.phase,pending:pilotPending,
      index:pilotIndex,state:state===GS.PILOT?'PILOT':state}};}""")
  png=pg.evaluate("()=>document.querySelector('#screen').toDataURL('image/png')")
  (out/'deploy.png').write_bytes(base64.b64decode(png.split(',',1)[1]))
  report={'result':result,'errors':errors};(out/'report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
  assert not errors and result['after']['done'] and result['after']['phase']=='hold'
  assert result['after']['pending'] is not None
  br.close()
finally:stop()
