"""October 11: actual Chromium encounter ownership, art, damage and transitions."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import shoot,json,sys
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'_shots/playthrough_1011/encounters';OUT.mkdir(parents=True,exist_ok=True)
checks=[];errors=[]
def check(name,passed,data=None):
 checks.append(dict(name=name,passed=bool(passed),data=data));print(('PASS ' if passed else 'FAIL ')+name+((' '+json.dumps(data)) if not passed else ''),flush=True)
port,stop=shoot.serve(str(ROOT))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--mute-audio','--autoplay-policy=no-user-gesture-required'])
  p=br.new_page(viewport=dict(width=1280,height=1000));p.set_default_timeout(120000)
  p.on('pageerror',lambda e:errors.append(str(e)))
  p.on('console',lambda m:errors.append(m.text[:700]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append('HTTP '+str(r.status)+': '+r.url) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
  def scene(n):
   p.evaluate(shoot.SETUP,dict(state='PLAY',stage=n,pilot='maverick',invuln=True))
   p.wait_for_function('n=>{stageLoadTick();return stageLoadInfo(n).ready}',arg=n,polling=50)
   p.evaluate('''()=>{diffKey='furious';DIFF=difficultyForRun('arcade','furious');coopOn=false;BOFCinematicDirector.cancel();story=null;fb2Talk=null;s6Opening=null;H3.release=false;H3.ending=null;stagePlan=[];enemies=[];pBullets=[];eBullets=[];special=null;boss=null;bossActive=false;subBoss=null;subBossActive=false;subBossDone=true;player.invuln=1e9;camX=0;}''')
  def frames(n):
   for start in range(0,n,20):
    r=p.evaluate(shoot.STEP,min(20,n-start))
    if r:errors.append(r);break
    p.wait_for_timeout(3)
  def snap(name):
   p.evaluate('()=>{story=fb2Talk=null;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);drawHUDStrip(hudctx);fb9HudSplit();window.__bofFit();}')
   p.screenshot(path=str(OUT/(name+'.png')))
  scene(3);p.evaluate("()=>{spawnSubBoss__inner('frostcruiser');subBoss.enter=false;subBoss.x=240;subBoss.y=205;subBoss._drawY=205;er26Set(subBoss,'elite-beam1002');}")
  frames(30)
  # This fixture starts directly inside the miniboss encounter; discard the
  # stage-entry coolant dialogue and frame the carrier in the actual camera.
  p.evaluate('()=>{thaw=null;subBoss.x=camLeftX()+viewW()/2;}')
  snap('ice-carrier-modular')
  q=p.evaluate('''()=>{const b=subBoss;return {parts:b._mr27.parts.map(q=>{const p=mr27Shape(b,q.id);return{id:q.id,hp:q.hp,x:p.x,y:p.y,rot:p.rot,muzzle:p.muzzle};}),draws:PT11.draws.ice_parts,skin:b._mr27.skin};}''')
  check('New ice carrier draws four independent weapons on its new hull',q.get('draws',0)>0 and len(q['parts'])==4,q)
  q=p.evaluate('''()=>{const b=subBoss,g=mr27Part(b,'gunL'),p=mr27Shape(b,'gunL'),other=mr27Part(b,'gunR'),hp=other.hp;b._noHit=false;b.enter=false;
   const id=mr27At(b,p.x,p.y);mr27Damage(b,g.hp+10,p.x,p.y);return{id,dead:g.dead,other:other.hp===hp,can:mr27CanFire(b,'L'),muzzle:shipBossMount(b,'R')};}''')
  check('Destroying the actual left cannon disables that cannon alone',q['id']=='gunL' and q['dead'] and q['other'] and not q['can'],q)
  snap('ice-carrier-left-destroyed')
  scene(4);p.evaluate("spawnBoss('stormsovereign')");frames(220)
  p.evaluate("()=>{boss.enter=false;er26Set(boss,'ap10-stormburst');}");frames(104);snap('storm-lightning-charge');frames(140)
  q=p.evaluate("AP10_E.history.filter(q=>q.event.startsWith('sovereign'))")
  check('Storm cannon reaches the native lightning release and midair burst',all(any(v['event']==e for v in q) for e in ['sovereign-fusion-charge','sovereign-fusion-release','sovereign-fusion-midburst']),q)
  q=p.evaluate('''()=>{const b=boss;stage4ShieldSyncNodes(b);const before=b._s4war.shield.nodes.map(q=>({x:q.x,y:q.y}));b.x+=40;b.y+=30;stage4ShieldSyncNodes(b);const after=b._s4war.shield.nodes.map(q=>({x:q.x,y:q.y}));return JSON.stringify(before)===JSON.stringify(after);}''')
  check('Generator objectives stay stationary when the boss moves',q)
  p.evaluate('''()=>{const b=boss,H=b._s4war.shield;H.active=H.rearming=false;b.hp=b.maxhp*.25;stage4ShieldBeginRearm(b,.25);}''')
  frames(160);snap('storm-south-exit');frames(210);snap('storm-northbound-pursuit');frames(290)
  q=p.evaluate("()=>({q:boss._s4war._pt11Chase,shield:boss._s4war.shield.active,rearm:boss._s4war.shield.rearming,nohit:boss._noHit,mode:boss._er26.mode,events:PT11.events.filter(e=>e.event.startsWith('storm-'))})")
  check('Final quarter exits south, pursues north and returns to a damageable fight',q['q']['done'] and q['q']['wave']>0 and not q['shield'] and not q['rearm'] and not q['nohit'],q)
  scene(5);p.evaluate('''()=>{spawnBoss(curStage.boss);const b=boss,h=b._hammer;b.enter=b.dead=b._noHit=false;b.hp=b.maxhp=6000;b.x=240;b.y=190;
   b._fb2IntroSeen=b._cin30Spoke=true;h.balance0922=h.gp4FailsafeSeen=h._fb2RageDone=h.intro1002=true;h.frRecovery=h.phasePending=h.openingJump1003=false;h.recovery=null;h.mode='storm';
   h.frArmor={hp:3000,max:3000,t:0,active:true,activated:true,half:true,barrier:0,checkpoints:[.75,.5,.35,.15],rage:false};h.state='hammer';}''')
  snap('hammer-new-reactor')
  q=p.evaluate('''()=>{const b=boss,h=b._hammer,max=h.chainMax;hammerBossModuleBreak(b,'chaingun');return{max,part:powerups.some(p=>p.kind==='pt11chain'),voice:PT11.radio?.text};}''')
  check('Strengthened chaingun drops one recoverable part during combat',q['max']>175 and q['part'] and bool(q['voice']),q)
  snap('hammer-salvage')
  q=p.evaluate('''()=>{const b=boss,h=b._hammer;h.state='storm_stun';h.t=0;b.x=-50;const hp=b.hp,damage=hammerBossDamage(b,30);for(let i=0;i<110;i++)hammerBossTick(b,1/60);return{damage,hp:b.hp===hp,state:h.state,x:b.x,ghost:pt11HammerGhost(b)};}''')
  check('Electrified recovery rejects damage without healing and returns on-screen',q['damage']==0 and q['hp'] and q['state']!='storm_stun' and q['x']>=100,q)
  q=p.evaluate('''()=>{const b=boss,h=b._hammer;h.state='storm_rebuild';h.t=.5;const p=powerups.find(p=>p.kind==='pt11chain');const old=run.weapon;applyPowerup(p);return{got:chaingunIsUnlocked(),held:run.weapon===old};}''')
  check('Collected salvage unlocks the weapon without switching the space loadout',q['got'] and q['held'],q)
  p.evaluate('''()=>{const b=boss,h=b._hammer;h.state='storm_wave';h.t=1;h._pt11Ghost=false;b._noHit=false;b.x=240;b.y=190;h.stormHome={x:b.x,y:b.y};hammerStormTarget(b);hammerStormImpact(b);window.reviewCounter=hc11BeginCounter(b,{x:340,y:220,seat:1});hc11CounterTick(b,reviewCounter,1.1);}''')
  snap('hammer-side-slide')
  q=p.evaluate('''()=>({scale:reviewCounter.scale,y:reviewCounter.y,ox:reviewCounter.oy,land:reviewCounter.land.y,committed:hammerStrikeCommitted(boss)})''')
  check('Upper-half counter slides at full scale instead of retreating into the background',q['scale']>=1 and q['committed'] and min(q['ox'],q['land'])-1<=q['y']<=max(q['ox'],q['land'])+1,q)
  scene(2);p.evaluate("()=>{spawnBoss(curStage.boss);boss.enter=false;boss._fz.phase='head';boss._fz.a=0;boss._fz.t=2;}")
  p.evaluate('''()=>{ctx.setTransform(SS,0,0,SS,0,0);ctx.fillStyle='#101825';ctx.fillRect(0,0,VW,VH);for(let i=0;i<16;i++)fztHeadDraw(65+(i%4)*116,73+Math.floor(i/4)*116,i/15,0,1,1.10);}''')
  p.locator('#screen').screenshot(path=str(OUT/'furnace-head-16.png'))
  check('Furnace head uses all sixteen authored frames',p.evaluate('PT11.draws.furnace_head>=16'))
  check('No page, console or asset errors',not errors,errors);br.close()
finally:stop()
report=dict(passed=sum(q['passed'] for q in checks),failed=sum(not q['passed'] for q in checks),checks=checks,errors=errors)
(OUT/'report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(dict(passed=report['passed'],failed=report['failed'],errors=errors)),flush=True)
sys.exit(1 if report['failed'] else 0)
