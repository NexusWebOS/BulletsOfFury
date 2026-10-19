"""Delivered Stage6 review: enlarged carrier, live allies and Fortress reactor."""
from pathlib import Path
import sys,json,http.server
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/harrier_wing_1018/native';O.mkdir(parents=True,exist_ok=True)
checks=[];errors=[];http.server.ThreadingHTTPServer.request_queue_size=128
def check(name,ok,data=None):
 checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name+((' '+json.dumps(data)) if not ok else ''),flush=True)
port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=br.new_page(viewport=dict(width=1600,height=1000));p.set_default_timeout(180000)
  p.add_init_script("Object.defineProperty(navigator,'getGamepads',{value:()=>[]});")
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:700]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append(str(r.status)+' '+r.url.split('?')[0]) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/docs/previews/stage6_repair_1018/index.html?scene=mini')
  p.wait_for_function('document.querySelector("#status").textContent.startsWith("Fortress")');w=p.frames[1];w.evaluate(shoot.TRAP_RAF);p.wait_for_timeout(35)
  def frames(n):
   for i in range(0,n,12):w.evaluate(shoot.STEP,min(12,n-i));p.wait_for_timeout(5)
  def choose(mode):p.select_option('#scene',mode);p.wait_for_function('!busy')
  def quiet_wing():
   # Flash expiry needs a quiet hit window, rather than fresh allied impacts
   # extending the timer while the actual review wing continues shooting.
   w.evaluate('''()=>{pBullets=[];for(const q of s6Wing.ships){q.fcd=q.missileCd=q.specialCd=99;q.target=null;q.think=99;}}''')
  w.evaluate('''()=>{window.reviewPixels=fn=>{ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);ctx.translate(-camX,0);fn();const a=Array.from(ctx.getImageData(0,0,cv.width,cv.height).data);ctx.restore();return a;};window.reviewChanged=(a,b)=>{let n=0;for(let i=0;i<a.length;i+=4)if(Math.max(Math.abs(a[i]-b[i]),Math.abs(a[i+1]-b[i+1]),Math.abs(a[i+2]-b[i+2]))>20)n++;return n;};}''')
  frames(210);row=w.evaluate('''()=>({native:subBoss._cargo17Mini,radio:s6Wing.line?.full,age:s6Wing.line?.t,draws:S6R18.draws.radio,field:SC12.layout.field,mode:SC12.mode,isolated:__stage6RepairStorage})''')
  check('Review uses the actual Stage6 miniboss, full playfield and isolated saves',row['native'] and row['mode']=='sides' and row['isolated'] and row['field']['h']>800,row)
  check('Miniboss dialogue is visible in the actual side HUD and advances',row['draws']>0 and row['age']>.5 and 'SIX' in row['radio'],row)
  p.screenshot(path=str(O/'review-mini-dialogue.png'))
  before=w.evaluate('subBoss._cargo13.age');frames(90)
  check('Combat continues while the miniboss caption is displayed',w.evaluate('subBoss._cargo13.age')-before>1.4)
  choose('minicore');frames(65)
  quiet_wing()
  row=w.evaluate('''()=>{const b=subBoss,p=sc13Core(b);b.flash=b._cargo13.coreFl=0;const h=b._cargo13.core,a=reviewPixels(()=>warhiveDraw(b));b._cargo13.directId='core';hitSubBoss(1);const c=reviewPixels(()=>warhiveDraw(b));return{hp:h-b._cargo13.core,flash:b.flash,pixels:reviewChanged(a,c),open:sc13Open(b)};}''')
  check('Miniboss energy core takes damage and flashes actual pixels',row['open'] and row['hp']>0 and row['flash']>0 and row['pixels']>20,row)
  frames(25);check('Miniboss reactor hit flash expires',w.evaluate('subBoss.flash<=0'))
  p.screenshot(path=str(O/'review-mini-core.png'))
  choose('fan');frames(85);p.screenshot(path=str(O/'review-broken-fan.png'))
  check('Fan review produces attached smoke, explosions and momentum',w.evaluate('boss._carrier17.parts.find(p=>p.id==="L").dead&&S6R18.draws.smoke>0&&S6R18.draws.burst>0&&Math.abs(boss._s6r18.drift.x)>1'))
  choose('harrier');frames(390)
  row=w.evaluate('''()=>{const b=boss,W=b._whv,survivors=W.jets.slice(),lost=survivors[1],hp=survivors.filter(e=>e!==lost).map(e=>e.hp);killEnemy(lost);whvLaunchJet(b);whvJetsAlive(W);const newcomer=W.jets.find(e=>!survivors.includes(e));whvLaunchJet(b);return{slot:newcomer?._hwSlot,expected:lost._hwSlot,count:whvJetsAlive(W),cap:W.jetN,unique:new Set(W.jets.map(e=>e._hwSlot)).size,same:survivors.filter(e=>e!==lost).every((e,i)=>W.jets.includes(e)&&e.hp===hp[i])};}''')
  check('Replacement jets reuse a vacant slot without healing survivors or exceeding cap',row.get('slot')==row['expected'] and row['count']==row['cap'] and row['unique']==row['cap'] and row['same'],row)
  p.screenshot(path=str(O/'review-bays.png'))
  choose('harrier');frames(210)
  quiet_wing()
  row=w.evaluate('''()=>{const b=boss,C=b._carrier17,p=C.parts.find(p=>p.kind==='laser'&&!p.dead);p.flash=p.fl=0;const h=p.hp,a=reviewPixels(()=>warhiveDraw(b));C.direct=p.id;warhiveDamage(b,1);const c=reviewPixels(()=>warhiveDraw(b));window.reviewPart=p;return{damage:h-p.hp,flash:p.flash,pixels:reviewChanged(a,c),scale:C.hullScale,core:'reactor' in C,wing:s6Wing.ships.length};}''')
  check('Delivered Harrier has enlarged real modules, allied support and no energy core',not row['core'] and row['scale']==1.45 and row['wing']>0 and row['damage']>0 and row['flash']>0 and row['pixels']>20,row)
  frames(25);check('Enlarged Harrier module hit flash expires',w.evaluate('reviewPart.flash<=0'))
  p.screenshot(path=str(O/'review-harrier-modules.png'))
  choose('ace');frames(280)
  check('Ace review follows the real falling-carrier transition',w.evaluate('boss._whv.mode==="ace"&&!!boss._whv.ace&&!bossDefeated&&boss.name==="NIGHTWING ACE"'))
  p.screenshot(path=str(O/'review-blue-ace.png'))
  p.select_option('#flight','both');p.wait_for_function('!busy');choose('mini');frames(210)
  row=w.evaluate('''()=>({seats:seatList().length,pilots:seatList().map(s=>withSeat(s,()=>_pilotKey())),rows:SC12.layout.rows,line:s6Wing.line?.full,t:s6Wing.line?.t})''')
  check('Co-op miniboss retains live captions for both native HUD rows',row['seats']==2 and row['rows']==2 and row['t']>.5 and bool(row['line']),row)
  p.screenshot(path=str(O/'review-coop-mini.png'))
  p.set_viewport_size(dict(width=700,height=1000));frames(2)
  check('Compact HUD also displays live Stage6 radio',w.evaluate('SC12.mode==="compact"&&s6WingRadioVisible()'))
  p.screenshot(path=str(O/'review-compact-radio.png'))
  # Compatibility fixtures use the same production init path; no new scene
  # owner is installed on the StageX Harrier or the alternate Rebel branch.
  row=w.evaluate('''()=>{coopOn=false;run._gp4StageX='left';spawnBoss('warhive');const stageX=!!boss._whv&&!boss._carrier17&&!boss._cargo13&&!s6r18Owns(boss);run._gp4StageX=null;spawnBoss('rebelsquad');return{stageX,rebel:!!boss._rebels&&!boss._carrier17&&!boss._cargo13};}''')
  check('StageX legacy Harrier and the alternate Rebel branch keep their own controllers',row['stageX'] and row['rebel'],row)
  p.goto(f'http://127.0.0.1:{port}/docs/previews/stage6_repair_1018/index.html?scene=reactor')
  p.wait_for_function('()=>ready&&!busy')
  check('Old Harrier reactor URL resolves to the corrected carrier scene',p.evaluate('scene.value==="harrier"&&!document.querySelector("option[value=reactor]")&&new URLSearchParams(location.search).get("revision")==="harrier-wing-1018"'))
  check('Review has no native page, console, draw or missing-asset errors',not errors,errors[:20]);br.close()
finally:stop()
report=dict(checks=checks,passed=sum(c['passed'] for c in checks),failed=sum(not c['passed'] for c in checks),errors=errors)
(O/'review-report.json').write_text(json.dumps(report,indent=2));print(f"{report['passed']} passed / {report['failed']} failed",flush=True)
sys.exit(1 if report['failed'] else 0)
