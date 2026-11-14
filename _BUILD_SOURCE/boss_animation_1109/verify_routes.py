from pathlib import Path
import sys,ast,json
R=Path(__file__).resolve().parents[2];W=Path(__file__).resolve().parent;O=R/'_shots/boss_animation_1109';sys.path.insert(0,str(R/'_BUILD_SOURCE'))
from shoot import serve,STEP
from barrage_review_common_1025 import boot
from playwright.sync_api import sync_playwright
seed=next(n.args[0].value for n in ast.walk(ast.parse((W/'verify.py').read_text()))if isinstance(n,ast.Call)and n.args and isinstance(n.args[0],ast.Constant)and isinstance(n.args[0].value,str)and 'window.seed119='in n.args[0].value)
errors=[];checks=[]
def ck(n,v,data=None):checks.append(dict(name=n,passed=bool(v),data=data));print(('PASS 'if v else'FAIL ')+n,str(data)[:250]if not v else'',flush=True)
port,stop=serve(str(R))
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=boot(br.new_context(viewport={'width':1280,'height':800}),port,5,errors,'boss');p.wait_for_function('()=>{stageLoadTick();return ba119Warm(5)}',polling=50,timeout=180000);p.evaluate(seed)
  for mode in ['giant','storm']:
   q=p.evaluate("""mode=>{seed119('furious','regular');const h=B._hammer;h.giantLeft=1;
    if(mode==='giant'){B.y=viewTopY()+135;hammerState(B,'giant_dive');}else{h.mode='storm';h.stormCycle=0;h.stormRecovery=null;hammerStormTarget(B);}
    let origin=null,drift=0,count=0,done=false;const poses=new Set();for(let i=0;i<650;i++){updateBoss(1/60);const P=h.c27Combo||h._hf22StormPair;if(P?.ba119){count++;origin??={x:B.x,y:B.y};drift=Math.max(drift,Math.hypot(B.x-origin.x,B.y-origin.y));const q=ha21Blue(B);if(q)poses.add(q.a.bank+':'+q.a.frame);}else if(origin){done=true;break;}}return{mode,origin,drift,count,done,poses:poses.size,contacts:BA119.events.filter(e=>e.type==='planted-contact')};}""",mode)
   ck('Stage5 '+mode+' uses planted second-down + left + right',len(q['contacts'])==3,q)
   ck('Stage5 '+mode+' never hops or retargets between contacts',q['drift']<.01 and q['count']>20,q)
   ck('Stage5 '+mode+' completes and returns to native recovery',q['done']and q['poses']>=30,q)
  p.evaluate("seed119('furious','regular');hammerState(B,'recover');B._hammer._hj22Pair=hj22Pair(B,'blue',{x:player.x,y:player.y});B._hammer._hj22Pair.clock=.52;B._hammer.t=.52")
  q=p.evaluate("""()=>{const P=B._hammer._hj22Pair,x=B.x,y=B.y,t=P.clock;setState(GS.PAUSE);return{x,y,t};}""");p.evaluate(STEP,20)
  ck('Pause freezes planted animation and position',p.evaluate('([x,y,t])=>B.x===x&&B.y===y&&B._hammer._hj22Pair.clock===t',[q['x'],q['y'],q['t']]))
  p.evaluate('setState(GS.PLAY)')
  # Same-frame normal/white masks: use an actual foreground native damage call.
  q=p.evaluate("""()=>{seed119('furious','regular');hammerState(B,'warn');B._hammer.t=.35;B._noHit=false;const a=ha21Blue(B).a;let pt=null;for(let y=230;y<350&&!pt;y++){const r=a.spans[y];for(let k=0;k<r.length;k+=2)if(r[k]<288&&r[k+1]>288){pt={x:B.x+288-a.pivot[0],y:B.y+y-a.pivot[1]};break;}}const before=B.hp;_dmgSrc='bullet';_dmgBullet={kind:'s1bullet',x:pt.x,y:pt.y};const hit=bossHitTest(pt.x,pt.y);if(hit)hitBoss(3);_dmgSrc=null;_dmgBullet=null;return{hit,damage:before-B.hp,flash:B.flash,pt};}""")
  ck('Stage5 actual foreground projectile contact damages and flashes new body',q['hit']and q['damage']>0 and q['flash']>0,q)
  ck('All new red-material hammer poses keep native red energy artwork',p.evaluate("()=>['blue-overhead','blue-sides','blue-right'].every(n=>BA119_ART[n].meta.every((m,f)=>{const a=ba119Row(n,f,'red');return !!BOFX.cells[a.key]&&!!BOFX.cells[a.white]}))"))
  q=p.evaluate("()=>{seed119('furious','regular');hammerState(B,'hammer');B._hammer.attackCycle=0;B._hammer.comboPending=false;for(let i=0;i<12;i++)updateBoss(1/60);return{state:B._hammer.state,offset:B._sg26?.offset,planted:!!ba119Planted(B)};}")
  ck('Normal space hover resumes outside the planted window',not q['planted']and abs(q.get('offset',0))>.0001,q)
  ck('No browser/renderer errors',not errors,errors);br.close()
finally:stop()
(O/'route-checks.json').write_text(json.dumps(dict(checks=checks,errors=errors),indent=2));print(json.dumps({'failed':[c['name']for c in checks if not c['passed']],'errors':errors}),flush=True)
