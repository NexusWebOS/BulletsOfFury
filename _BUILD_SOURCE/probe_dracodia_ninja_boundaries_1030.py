from pathlib import Path
import sys,json,http.server
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1] if Path(__file__).parent.name=='_BUILD_SOURCE' else Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury');W=R/'_shots/dracodia_ninja_1030' if Path(__file__).parent.name=='_BUILD_SOURCE' else Path(__file__).parent;W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'))
from shoot import serve,STEP
from barrage_review_common_1025 import boot
http.server.ThreadingHTTPServer.request_queue_size=256;checks=[];errors=[];port,stop=serve(str(R))
def check(n,v):checks.append({'name':n,'passed':bool(v)});print(('PASS 'if v else'FAIL ')+n,flush=True)
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=boot(br.new_context(viewport={'width':1280,'height':800}),port,8,errors,'boss')
  setup="""()=>{spawnBoss('vileexistence');window.B=boss;const J=j3State(B);for(const i of V18.forms)if(i!==0)J.hp[i]=0;v18Enter(B,2,0);B._r30.mode='fight';B.enter=B._noHit=false;v18StartAttack(B);window.P=rd77Act(B);RD77.events=[];}"""
  p.evaluate(setup);p.evaluate(STEP,80);before=p.evaluate('P.t');p.evaluate("setState('paused')");p.evaluate(STEP,120)
  check('Pause freezes the offscreen leap',p.evaluate('P.t')==before)
  p.evaluate('setState(GS.PLAY)');p.evaluate(STEP,78)
  check('Resume continues into the same committed combo',p.evaluate("rd77Act(B)===P&&P.index===1"))
  # Destroy the striking arm during its actual left slash, through native modular damage.
  p.evaluate("()=>{B._lastPart=B.parts.find(p=>p.id==='left');modularHit(B._lastPart.hp);window.atBreak=RD77.events.length;}")
  p.evaluate(STEP,38)
  check('Broken striking claw cancels its pending landing impact',p.evaluate("!RD77.events.slice(atBreak).some(e=>e.event==='landing-impact'&&e.index===1)"))
  check('Destroyed claw is absent from the authored attack rig',p.evaluate("!v18Rig(B).some(v=>v.p.id==='left')"))
  p.evaluate('()=>{v18Clear(B);B._r30.mode="fight";B.enter=B._noHit=false;v18StartAttack(B);window.P=rd77Act(B);}')
  check('A one-clawed fighter chooses only its surviving arm',p.evaluate("P.order.every(side=>side==='right')"))
  # Real alpha contact invokes the native death path when GOD/armor/shields are off.
  p.evaluate(setup);p.evaluate(STEP,160)
  q=p.evaluate("""()=>{const v=v18Rig(B).find(v=>v.p.id===P.order[P.index-1]),a=v.a;let y=a.spans.findIndex(r=>r.length),x=a.spans[y][0];DBGT.god=false;player.invuln=0;player.roll=player.somer=null;run.armor=0;run.shield=0;player.x=v.ax+a.offset[0]+x;player.y=v.ay+a.offset[1]+y;P.contacts.clear();rd77Touch(B,P);return{dead:player.dead,events:RD77.events.slice(-3)};}""")
  check('Physical claw alpha contact reaches native playerHit',any(e['event']=='claw-contact'for e in q['events']))
  check('Physical claw can kill through the normal death system',q['dead'])
  p.evaluate('()=>{DBGT.god=true;spawnBoss("vileexistence");window.B=boss;}')
  check('Retry removes both combo and committed warnings',p.evaluate('!rd77Act(B)&&!B._r30.v18.attack'))
  p.evaluate("""()=>{const J=j3State(B);v18Enter(B,2,0);J.modules[0].find(q=>q.id==='left').destroyed=true;J.modules[0].find(q=>q.id==='left').hp=0;v18Enter(B,2,6);B._r30.mode='fight';B.enter=B._noHit=false;B.hp=0;r30Break(B);}""");p.evaluate(STEP,560)
  check('Defeated copy still downloads into an intact main-body ninja fight',p.evaluate("B._r30.mode==='fight'&&B._r30.v18.form===0&&B.parts.every(p=>!p.destroyed)&&!!rd77Act(B)"))
  p.evaluate("""()=>{spawnBoss('vileexistence');window.B=boss;v18Enter(B,2,8);const J=j3State(B);for(const i of V18.forms)if(i!==8)J.hp[i]=0;B._r30.mode='fight';B.enter=B._noHit=false;const Q=hb20State(B);Q.chrome=Q.rage=true;Q.ragePool=B.hp;B._lastPart=Q.parts[0];modularHit(B.hp);}""");p.evaluate(STEP,540)
  check('The exhausted final copied life still reaches native final destruction',p.evaluate("B._r30.mode==='dr5Death'&&B.hp===0&&B.parts.map(p=>p.id).join(',')==='core,left,right'"))
  check('No native/browser errors',not errors);br.close()
finally:stop();(W/'boundary-checks.json').write_text(json.dumps({'checks':checks,'errors':errors},indent=2))
assert all(c['passed']for c in checks),[c['name']for c in checks if not c['passed']]
