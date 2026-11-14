from pathlib import Path
import ast,sys,json
from playwright.sync_api import sync_playwright
R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');W=Path(__file__).resolve().parent;sys.path.insert(0,str(R/'_BUILD_SOURCE'))
from shoot import serve
from barrage_review_common_1025 import boot
seed=next(n.args[0].value for n in ast.walk(ast.parse((W.parent/'BOF-Boss-Strike-1109b/verify.py').read_text()))if isinstance(n,ast.Call)and n.args and isinstance(n.args[0],ast.Constant)and isinstance(n.args[0].value,str)and 'window.seed119='in n.args[0].value)
errors=[];port,stop=serve(str(R))
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=boot(br.new_context(viewport={'width':1280,'height':800}),port,5,errors,'boss')
  p.wait_for_function('()=>{stageLoadTick();return ba119Warm(5)}',polling=50,timeout=180000);p.evaluate(seed)
  p.evaluate('''()=>{const hold=Input.hold;Input.hold=function(...a){return a.includes('fire')?false:hold.apply(this,a)};seed119('furious','regular');B.flash=0;B._lastPart=null;for(const p of B.parts||[])p.flash=0;
  window.FlashTrace={sets:[],marks:[],paints:[],frames:[]};let flash=B.flash;Object.defineProperty(B,'flash',{configurable:true,get(){return flash},set(v){if(v>0&&FlashTrace.sets.length<250)FlashTrace.sets.push({value:v,clock:efxClock,stack:new Error().stack.split('\\n').slice(1,6).join('\\n')});flash=v}});
  const hit=markHit;markHit=function(o,...a){if(o===B)FlashTrace.marks.push({clock:efxClock,hp:B.hp,stack:new Error().stack.split('\\n').slice(1,5).join('\\n')});return hit.call(this,o,...a)};
  const paint=c26Paint;c26Paint=function(a,x,y,k,rot,f){if(a?._ba119&&FlashTrace.paints.length<1000)FlashTrace.paints.push({clock:efxClock,flash:f,body:B.flash,part:B._lastPart?.flash,hp:B.hp,state:B._hammer.state,key:a.key});return paint.apply(this,arguments)};
  function observe(){FlashTrace.frames.push({clock:efxClock,hp:B.hp,flash:B.flash,part:B._lastPart?.flash,shots:pBullets.length,state:B._hammer.state});if(FlashTrace.frames.length<500)requestAnimationFrame(observe)};
  requestAnimationFrame=__bofRealRAF;requestAnimationFrame(loop);requestAnimationFrame(observe);}''')
  p.wait_for_timeout(5000);q=p.evaluate('FlashTrace');q['feedback']=p.evaluate('''()=>{const child={hp:100,flash:0},b={hp:400,_targets:{items:[]},parts:[child]};b._targets.items=[b,child,child];const lists=pr118PartLists(b);const aliasOK=lists.flat().length===1&&lists[0][0]===child;const noHit=B.flash===0;markHit(B,.16);const hitFlash=B.flash>0;for(let i=0;i<30;i++)updateBoss(1/60);const expires=B.flash===0;B._lastPart=null;B.flash=0;delete B._pr118Hp;pr118BossFlash();B.hp-=10;efxClock+=.2;pr118BossFlash();return{aliasOK,noHit,hitFlash,expires,realDamageFlash:B.flash>0};}''');q['errors']=errors;(W/'flash-fixed.json').write_text(json.dumps(q,indent=2),encoding='utf8');p.screenshot(path=str(W/'flash-fixed-end.png'));br.close()
finally:stop()
white=[p for p in q['paints']if(p.get('flash')or 0)>0]
print(json.dumps(dict(feedback=q['feedback'],paints=len(q['paints']),white=len(white),marks=q['marks'][:4],sets=q['sets'][:5],errors=errors)),flush=True)
