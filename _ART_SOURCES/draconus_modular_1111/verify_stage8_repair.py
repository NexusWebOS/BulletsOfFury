from pathlib import Path
import sys,json,hashlib
from playwright.sync_api import sync_playwright
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');O=W.parents[1]/'outputs/Draconus-rotor-and-full-stages';sys.path.insert(0,str(R/'_BUILD_SOURCE'))
from shoot import serve
from barrage_review_common_1025 import boot
sys.stdout.reconfigure(encoding='utf-8');errors=[];checks=[]
def ck(name,ok,data=None):
 checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS 'if ok else'FAIL ')+name,flush=True)
port,stop=serve(str(R))
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True);context=br.new_context(viewport={'width':1280,'height':800});p=boot(context,port,8,errors,'boss');p.on('console',lambda m:errors.append(m.text)if'update error'in m.text or'draw error'in m.text else None)
  p.wait_for_function('()=>{stageLoadTick();if(stageLoadReady(8))updatePlay(0);return stageLoadReady(8)&&!bp119Pending()&&dgm1111Warm()}',timeout=180000)
  q=p.evaluate('''()=>{window.B=boss;BOFCinematicDirector.cancel();v18Enter(B,0);B._r30.mode='fight';B.enter=B._noHit=B.dead=false;const targets=retinaBossTargets(B);window.oldHostTargets=[...(B._retinaDynamic||[])];window.armTarget=oldHostTargets.find(t=>t._retinaId==='rb23-left')||oldHostTargets.find(t=>t.kind==='arm');return{targets:targets.length,cached:oldHostTargets.length,arm:!!armTarget};}''')
  ck('Native host exposes real cached arm descriptors',q['targets']>0 and q['arm'],q)
  q=p.evaluate('''()=>{v18Enter(B,2,6);B._r30.mode='fight';B.enter=B._noHit=B.dead=false;let throws=false;try{void armTarget.hp}catch(e){throws=String(e).includes('bounds')}const kept=(B._retinaDynamic||[]).includes(armTarget);return{throws,kept,form:B._r30.v18.form};}''')
  ck('Reproduced obsolete-host socket getter after actual Archon transition',q['throws']and q['kept']and q['form']==6,q)
  q=p.evaluate('''()=>{const lists=pr118PartLists(B),all=lists.flat();pr118BossFlash();return{proxies:all.filter(p=>p._retinaOwner).length,physical:all.includes(B.parts[0]),unique:new Set(all).size===all.length,hp:B.hp};}''')
  ck('Flash polling excludes target descriptors and keeps unique physical pools',q['proxies']==0 and q['physical']and q['unique'],q)
  q=p.evaluate('''()=>{const hp=B.hp,part=B.parts[0],ph=part.hp,last=part._pr118LastHit;for(let i=0;i<180;i++){efxClock+=1/60;pr118BossFlash()}return{same:hp===B.hp&&ph===part.hp,noPhantom:last===part._pr118LastHit};}''')
  ck('Repeated snapshots neither change HP nor fabricate hits',q['same']and q['noPhantom'],q)
  q=p.evaluate('''()=>{const part=B.parts[0];efxClock+=1;part.hp-=10;B.hp-=10;const hp=B.hp,ph=part.hp;pr118BossFlash();return{shown:part.flash>0,hpSame:B.hp===hp&&part.hp===ph};}''')
  ck('Genuine part damage still flashes independently without changing damage',q['shown']and q['hpSame'],q)
  q=p.evaluate('''()=>{const out=[];for(const f of V18.forms){v18Enter(B,2,f);B._r30.mode='fight';B.enter=B._noHit=B.dead=false;retinaBossTargets(B);for(let i=0;i<10;i++){pr118BossFlash();updateBoss(1/60)}out.push({form:f,hp:B.hp,finite:Number.isFinite(B.hp)})}return out;}''')
  ck('Real boss updates and feedback survive copied-form changes',all(x['finite']for x in q),q)
  ck('No native browser/update/draw exceptions',not errors,errors);br.close()
finally:stop()
report=dict(checks=checks,errors=errors,repairHash=hashlib.sha256((R/'assets/playtest_repairs_1108.js').read_bytes()).hexdigest());(O/'stage8-repair-verification.json').write_text(json.dumps(report,indent=2));assert all(c['passed']for c in checks)and not errors
