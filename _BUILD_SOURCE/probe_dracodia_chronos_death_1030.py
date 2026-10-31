from pathlib import Path
import sys,json,http.server
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];W=R/'_shots/dracodia_chronos_1030/death';W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import serve,STEP
from barrage_review_common_1025 import boot
http.server.ThreadingHTTPServer.request_queue_size=256;errors=[];port,stop=serve(str(R))
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=boot(br.new_context(viewport={'width':1280,'height':800}),port,8,errors,'boss');p.evaluate("""()=>{window.B=boss;v18Enter(B,2,8);B._r30.mode='fight';B.enter=false;B._noHit=false;window.Q=hb20State(B);const J=j3State(B);for(const k in J.hp)if(+k!==8)J.hp[k]=0;Q.chrome=Q.rage=true;Q.ragePool=B.hp;B._lastPart=Q.parts[0];window.deathTrace=[];const error=console.error;console.error=function(){deathTrace.push({mode:B._r30.mode,form:B._r30.v18.form,dead:B.dead,clock:efxClock,error:[...arguments].map(String).join(' ')});return error.apply(this,arguments);};modularHit(B.hp);}""")
  for i in range(18):p.evaluate(STEP,30)
  q=p.evaluate('({trace:deathTrace,mode:B._r30.mode,dead:B.dead,form:B._r30.v18.form,hp:B.hp,parts:B.parts.map(p=>({id:p.id,hp:p.hp})),events:RD74.events.filter(e=>e.event==="reform-anatomy")})');checks=[dict(name='Native copied-life defeat and final reform have no draw errors',passed=not q['trace']and not errors),dict(name='Final reform restores native core/left/right anatomy',passed=[p['id']for p in q['parts']]==['core','left','right']),dict(name='Reform does not refill boss or part HP',passed=q['hp']==0 and all(p['hp']==0 for p in q['parts'])),dict(name='Native final-death progression continues',passed=q['mode']=='dr5Death')];(W/'death-check.json').write_text(json.dumps({'checks':checks,'result':q,'errors':errors},indent=2));print(json.dumps(checks),flush=True);assert all(c['passed']for c in checks);br.close()
finally:stop()
