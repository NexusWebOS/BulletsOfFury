from pathlib import Path
import sys,json
R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');W=Path(__file__).resolve().parent;O=W.parents[1]/'outputs/Three-way-hammer/password-handoff';O.mkdir(exist_ok=True,parents=True)
sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import serve
from barrage_review_common_1025 import boot
from playwright.sync_api import sync_playwright
errors=[];checks=[]
port,stop=serve(str(R))
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=boot(br.new_context(viewport={'width':1280,'height':800}),port,5,errors,'boss')
  p.wait_for_function('(s)=>{stageLoadTick();if(stageLoadReady(s))updatePlay(0);return stageLoadReady(s)&&!bp119Pending()}',arg=5,timeout=180000)
  p.evaluate("()=>{ht27Warm();}");p.wait_for_function("()=>{ht27Warm();return Object.keys(HAMMER_TIME_ART.sheets).every(k=>XART.rdy('ht27_'+k))&&XART.rdy('arch_ship_transform')}",timeout=120000)
  p.evaluate("()=>{BOFCinematicDirector.cancel();fb2Intro=fb2Talk=null;ht27Start();window.B=boss;B.x=worldWidth()/2;B.y=viewTopY()+210;B._noHit=false;DBGT.god=true;}")
  initial=p.evaluate("()=>{const d=B._hammerTime;d.mode='intro';d.musicStarted=true;d.shipFrame=15;d.helpers=[];const q=ha21Blue(B);return{mode:d.mode,pose:q?.kind,bank:q?.a.bank,campaignPose:!!q?.a.wholeGenerated};}")
  if '--diagnose'in sys.argv:
   p.evaluate("()=>{const old=ha21Blue;ha21Blue=function(b){if(b?._hammerTime&&b._hammerTime.mode!=='attack')return null;return old.apply(this,arguments)}}")
  for mode in ['intro','dance','break','attack']:
   r=p.evaluate("""mode=>{const d=B._hammerTime;d.mode=mode;d.clock=mode==='intro'?1:mode==='break'?16.3:12;d.t=.5;d.duration=2;d.helpers=[];d.reflections=[];d.energy=.3;d.musicStarted=true;d.shipFrame=15;d.locked=mode==='break';d.shield=mode==='break';B.x=worldWidth()/2;B.y=viewTopY()+210;hammerState(B,'warn');B._hammer.t=.5;const q=ha21Blue(B);const keys=[],old=ctx.drawImage;ctx.drawImage=function(im,...args){const k=HA21.tags.get(im);if(k)keys.push(k);return old.call(this,im,...args)};try{drawWorld(0)}finally{ctx.drawImage=old}return{mode,pose:q?.kind,bank:q?.a.bank,whole:!!q?.a.wholeGenerated,keys:keys.filter(k=>/ht27|ship_transform|ba119_blue/.test(k))};}""",mode)
   p.evaluate('()=>{SC12.refresh();__bofFit()}');p.screenshot(path=str(O/(mode+'.png')))
   passed=(r['whole']and r.get('bank','').startswith('blue-overhead'))if mode=='attack'else not r['whole']and (any('ship_transform'in k for k in r['keys'])if mode=='intro'else any('ht27_boss'in k for k in r['keys']))
   checks.append(dict(name='Password '+mode+' retains correct animation owner',passed=bool(passed),data=r));print(('PASS 'if passed else'FAIL ')+checks[-1]['name'],flush=True)
  br.close()
finally:stop()
name='diagnosis.json'if'--diagnose'in sys.argv else'checks.json';(O/name).write_text(json.dumps(dict(initial=initial,checks=checks,errors=errors),indent=2));assert not errors and all(c['passed']for c in checks),dict(errors=errors,failed=[c['name']for c in checks if not c['passed']])
