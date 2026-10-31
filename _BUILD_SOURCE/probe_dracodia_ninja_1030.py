from pathlib import Path
import sys,json,http.server
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1] if Path(__file__).parent.name=='_BUILD_SOURCE' else Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury');W=R/'_shots/dracodia_ninja_1030' if Path(__file__).parent.name=='_BUILD_SOURCE' else Path(__file__).parent;W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'))
from shoot import serve,STEP
from barrage_review_common_1025 import boot
http.server.ThreadingHTTPServer.request_queue_size=256;errors=[];checks=[];states=[];port,stop=serve(str(R))
def check(n,v):checks.append({'name':n,'passed':bool(v)});print(('PASS 'if v else'FAIL ')+n,flush=True)
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=boot(br.new_context(viewport={'width':1280,'height':800}),port,8,errors,'boss')
  for rank in ['normal','hard','furious']:
   for seq in [0,1]:
    q=p.evaluate('''([rank,seq])=>{diffKey=rank;spawnBoss('vileexistence');window.B=boss;const J=j3State(B);for(const i of V18.forms)if(i!==0)J.hp[i]=0;v18Enter(B,2,0);B._r30.mode='fight';B.enter=B._noHit=false;B._r30.v18.rd77Seq=seq;player.invuln=0;RD77.events=[];v18StartAttack(B);window.P=B._r30.v18.attack;return{hp:B.hp,marks:JSON.stringify(P.marks),order:P.order};}''',[rank,seq]);label=rank+' order'+str(seq)
    check(label+' chooses physical claw combo',p.evaluate("P._rd77&&P.type==='rd77-ninja'"))
    p.evaluate(STEP,60);back=p.evaluate('({mode:P.stage,depth:P.depth,noHit:B._noHit,targets:retinaBossTargets(B).length,hp:B.hp,marks:JSON.stringify(P.marks)})')
    check(label+' background cannot be damaged or Retina locked',back['depth']<.85 and back['noHit']and back['targets']==0)
    p.evaluate('()=>{B._lastPart=B.parts[0];modularHit(10000);}')
    check(label+' background hit keeps HP',p.evaluate('B.hp')==q['hp'])
    check(label+' ground warning never chases after commitment',back['marks']==q['marks'])
    p.evaluate(STEP,58);landing=p.evaluate('({stage:P.stage,depth:P.depth,noHit:B._noHit,targets:retinaBossTargets(B).length,rig:v18Rig(B).length,rounds:eBullets.filter(q=>q._v18Owner===B).length})')
    check(label+' foreground has real hit/Retina geometry',landing['depth']==1 and not landing['noHit']and landing['targets']==3)
    if rank=='furious':p.screenshot(path=str(W/('landing-order'+str(seq)+'.png')))
    p.evaluate(STEP,42);side=p.evaluate('({stage:P.stage,bank:P.bank,frame:P.frame,x:B.x,y:B.y})')
    if rank=='furious':p.screenshot(path=str(W/('slash-order'+str(seq)+'.png')))
    p.evaluate(STEP,180);end=p.evaluate('({events:RD77.events,attack:B._r30.v18.attack?.type,hp:B.hp,parts:B.parts.map(p=>({id:p.id,hp:p.hp})),rounds:eBullets.filter(q=>q._v18Owner===B).length})')
    slashes=[e['side']for e in end['events']if e['event']=='jump-slash'];expected=q['order'][:1 if rank=='normal'else 2]
    check(label+' completes expected alternating slash sequence',slashes[:len(expected)]==expected)
    check(label+' does not emit the old bullet barrage',end['rounds']==0 and all(e.get('type')not in ['heartSpores','spiralLightning']for e in end['events']))
    check(label+' leaves native boss HP unchanged without hits',end['hp']==q['hp'])
    states.append({'rank':rank,'seq':seq,'back':back,'landing':landing,'side':side,'end':end})
  # A severed arm must leave both graphics and contact geometry, through real native damage.
  p.evaluate("()=>{v18Clear(B);B._r30.mode='fight';B.enter=B._noHit=false;v18StartAttack(B);B._lastPart=B.parts.find(q=>q.id==='left');modularHit(B._lastPart.hp);}")
  check('Native limb break removes complete claw geometry',p.evaluate("B.parts.find(p=>p.id==='left').destroyed&&!v18Rig(B).some(v=>v.p.id==='left')"))
  check('Limb breakup uses authored-position explosions',p.evaluate("RD77.events.some(e=>e.event==='whole-claw-break')"))
  p.evaluate("()=>{v18Clear(B);B._r30.mode='fight';B.enter=B._noHit=false;B._lastPart=B.parts.find(q=>q.id==='right');modularHit(B._lastPart.hp);v18StartAttack(B);}")
  check('Armless body falls back to its physical core missiles',p.evaluate("B._r30.v18.attack?.type==='coreMissiles'"))
  # Retry and non-owned encounter identity must retain their owners.
  p.evaluate("()=>{spawnBoss('vileexistence');window.B=boss;}")
  check('Retry discards physical combo',p.evaluate('!rd77Act(B)&&j3State(B).encounter===0'))
  p.evaluate("()=>{v18Enter(B,2,8);B._r30.mode='fight';B.enter=B._noHit=false;}")
  check('Corrupted Chronos stays on its own regenerated controller',p.evaluate('!rd77Own(B)&&rd74Own(B)'))
  check('Authored pose frames were actually drawn',p.evaluate('RD77.draws')>0)
  check('No browser or native draw errors',not errors);br.close()
finally:stop();(W/'checks.json').write_text(json.dumps({'checks':checks,'states':states,'errors':errors},indent=2))
assert all(c['passed']for c in checks),[c['name']for c in checks if not c['passed']]
