from pathlib import Path
import sys,json,http.server
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1] if Path(__file__).parent.name=='_BUILD_SOURCE' else Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury');W=R/'_shots/dracodia_luminaire_1030' if Path(__file__).parent.name=='_BUILD_SOURCE' else Path(__file__).parent;W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'))
from shoot import serve,STEP
from barrage_review_common_1025 import boot
http.server.ThreadingHTTPServer.request_queue_size=256;errors=[];checks=[];states=[];port,stop=serve(str(R))
def check(n,v):checks.append({'name':n,'passed':bool(v)});print(('PASS 'if v else'FAIL ')+n,flush=True)
SETUP="""rank=>{diffKey=rank;spawnBoss('vileexistence');window.B=boss;const J=j3State(B);for(const i of V18.forms)if(i!==0)J.hp[i]=0;v18Enter(B,2,0);B._r30.mode='fight';B.enter=B._noHit=false;player.dead=false;player.out=false;player.invuln=0;player.roll=player.somer=null;run.armor=0;run.shield=0;DBGT.god=true;RD78.events=[];window.P=rd78Start(B);for(const k of Object.keys(Input.keys))Input.keys[k]=false;}"""
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=boot(br.new_context(viewport={'width':1280,'height':800}),port,8,errors,'boss')
  for rank in ['normal','hard','furious']:
   for side in ['left','right']:
    p.evaluate(SETUP,rank);q=p.evaluate("side=>{DBGT.god=false;player.x=P.home.x;player.y=VH-65;window.goal={x:P.left+(side==='left'?166:514),y:226};window.hpBefore=B.hp;return{goal,tell:P.tell,hp:B.hp}}",side)
    # Real movement inputs: leave the southern position and reach the safe pocket during charge.
    for i in range(150):
     p.evaluate("()=>{Input.keys.a=player.x>goal.x+3;Input.keys.d=player.x<goal.x-3;Input.keys.w=player.y>goal.y+3;Input.keys.s=player.y<goal.y-3;}");p.evaluate(STEP,1)
    p.evaluate('()=>{for(const k of ["a","d","w","s"])Input.keys[k]=false;}')
    before=p.evaluate('({x:player.x,y:player.y,dead:player.dead,inside:rd78Inside(P,player.x,player.y),hp:B.hp})');label=rank+' '+side
    check(label+' pocket is reachable by ordinary inputs before release',not before['dead']and not before['inside']and abs(before['x']-q['goal']['x'])<8 and abs(before['y']-226)<8)
    p.evaluate(STEP,round((q['tell']-2.5+.35)*60));blast=p.evaluate('({dead:player.dead,phase:P.phase,hits:P.hits.size,hp:B.hp,x:player.x,y:player.y})')
    check(label+' survives the actual live blast without GOD',not blast['dead']and blast['phase']=='blast'and blast['hits']==0)
    check(label+' preserves the native boss HP pool',blast['hp']==q['hp'])
    if rank=='furious':p.screenshot(path=str(W/('safe-'+side+'-blast.png')))
    p.evaluate(STEP,145);check(label+' finishes with native combat unlocked',p.evaluate('!rd78Act(B)&&B._r30.mode==="fight"&&!B._noHit'))
    states.append({'rank':rank,'side':side,'before':before,'blast':blast})
  # Unsafe center and lower floor are genuinely dangerous; not a screen-only effect.
  for name,x,y in [('center',340,226),('south',166,450)]:
   p.evaluate(SETUP,'furious');p.evaluate('([x,y])=>{DBGT.god=false;player.x=P.left+x;player.y=y;}',[x,y]);p.evaluate(STEP,240)
   check(name+' danger invokes native death at release',p.evaluate("player.dead&&RD78.events.some(e=>e.event==='luminaire-contact'&&e.dead)"))
  p.evaluate(SETUP,'furious');p.evaluate(STEP,180);p.screenshot(path=str(W/'charged-warning.png'))
  check('Charge warning does not damage the player',p.evaluate("!player.dead&&!RD78.events.some(e=>e.event==='luminaire-contact')"))
  before=p.evaluate('P.t');p.evaluate("setState('paused')");p.evaluate(STEP,90);check('Pause freezes the charge and field',p.evaluate('P.t')==before);p.evaluate('setState(GS.PLAY)')
  q=p.evaluate('({insideCenter:rd78Inside(P,340,226),insideSouth:rd78Inside(P,166,450),leftClear:!rd78Inside(P,166,226),rightClear:!rd78Inside(P,514,226),fieldWidth:RD78_ART.world[0],world:worldWidth()})')
  check('Warning/damage geometry spans the whole scrolling arena',all(q[k]for k in ['insideCenter','insideSouth','leftClear','rightClear'])and q['fieldWidth']==q['world'])
  p.evaluate('()=>{window.cached=v18Rig(B);window.reused=v18Rig(B);window.oldX=B.x;B.x+=2;window.moved=v18Rig(B);B.x=oldX;}')
  check('Repeated weapon samples share exact same-frame geometry',p.evaluate('cached===reused&&cached[0].p===B.parts.find(p=>p.id===cached[0].p.id)'))
  check('World movement immediately invalidates cached geometry',p.evaluate('moved!==cached&&moved[0].ax===oldX+2'))
  p.evaluate(STEP,40)
  check('Fully expanded red warning holds before the release',p.evaluate("RD78.lastWarningFrame===RD78_ART.banks.warning.frames-1&&P.phase==='charge'&&P.t<P.tell"))
  p.evaluate("()=>{B._lastPart=B.parts.find(q=>q.id==='left');modularHit(B._lastPart.hp);}")
  check('Breaking an arm during charge uses complete authored-part breakup',p.evaluate("B.parts.find(q=>q.id==='left').destroyed&&RD78.events.some(e=>e.event==='charge-claw-break')"))
  check('Destroyed anatomy immediately invalidates the hit cache',p.evaluate("!v18Rig(B).some(v=>v.p.id==='left')"))
  p.evaluate("()=>{v18Clear(B);B._r30.mode='fight';B.enter=B._noHit=false;}")
  check('Cancellation removes the field immediately',p.evaluate('!rd78Act(B)'))
  check('Cancellation stops pending charge and release voices',p.evaluate("RD78.cues.every(k=>Snd.pools[k].slots.every(s=>!s?.el||s.el.paused))"))
  # Scheduler leaves both ninja orders in the book before inserting Luminaire.
  p.evaluate(SETUP,'furious');p.evaluate('()=>{v18Clear(B);B._r30.v18.rd78Decisions=0;window.book=[];for(let i=0;i<3;i++){v18StartAttack(B);book.push(B._r30.v18.attack.type);v18Clear(B);}}')
  check('Attack book alternates two claw combos then Luminaire',p.evaluate('book.join(",")==="rd77-ninja,rd77-ninja,luminaire"'))
  p.evaluate(SETUP,'furious');p.evaluate('()=>{v18Clear(B);rd77Start(B);window.P=rd77Act(B);}')
  p.evaluate(STEP,160)
  q=p.evaluate('''()=>{const reference=RD78.base.rig(B).slice().reverse();let compared=0,mismatch=0;for(let y=20;y<510;y+=13)for(let x=10;x<worldWidth();x+=13){const expected=reference.find(v=>!v.p.destroyed&&v19AtRect(v,x,y))?.p;const actual=r30At(B,x,y);compared++;if((expected?.id||null)!==(actual?.id||null))mismatch++;}const a=v18Rig(B),z=v18Rig(B);window.clawCache=a;return{compared,mismatch,reused:a===z,stage:P.stage};}''')
  check('Cached ninja geometry matches original alpha hit results across the arena',q['compared']>1000 and q['mismatch']==0)
  check('Repeated claw hit queries reuse the same pose',q['reused'])
  p.evaluate(STEP,1)
  check('Claw animation/movement invalidates the pose cache',p.evaluate('v18Rig(B)!==clawCache'))
  p.evaluate("()=>{B._lastPart=B.parts.find(q=>q.id==='left');modularHit(B._lastPart.hp);}")
  check('Mid-slash destruction immediately removes cached claw geometry',p.evaluate("!v18Rig(B).some(v=>v.p.id==='left')"))
  p.evaluate(SETUP,'furious');p.evaluate("()=>{B._lastPart=B.parts[0];modularHit(B.hp);}");p.evaluate(STEP,150)
  check('Native boss defeat cancels Luminaire and reaches final destruction',p.evaluate("!rd78Act(B)&&B._r30.mode==='dr5Death'&&B.hp===0"))
  p.evaluate(SETUP,'furious');p.evaluate("()=>{spawnBoss('vileexistence');window.B=boss;}");check('Retry retains original first-host ownership',p.evaluate('!rd78Own(B)&&j3State(B).encounter===0'))
  check('Retry also stops the retired casting voices',p.evaluate("RD78.cues.every(k=>Snd.pools[k].slots.every(s=>!s?.el||s.el.paused))"))
  check('Original generated orb and authored field banks drew in-game',p.evaluate('RD78.draws.orb_charge>0&&RD78.draws.blast>0&&RD78.draws.warning>0'))
  check('No browser or native draw errors',not errors);br.close()
finally:stop();(W/'checks.json').write_text(json.dumps({'checks':checks,'states':states,'errors':errors},indent=2))
assert all(c['passed']for c in checks),[c['name']for c in checks if not c['passed']]
