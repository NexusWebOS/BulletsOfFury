"""Native opening deliveries, all five enemy signatures and earned Mk II."""
from pathlib import Path
import sys,json
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
OUT=ROOT/'_shots/signature_specials_1011';OUT.mkdir(parents=True,exist_ok=True)
checks=[];errors=[]
def check(name,yes,data=None):
 checks.append(dict(name=name,passed=bool(yes),data=data));print(('PASS ' if yes else 'FAIL ')+name,flush=True)
port,stop=shoot.serve(str(ROOT))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch();p=br.new_page(viewport=dict(width=1100,height=950));p.set_default_timeout(120000)
  p.on('pageerror',lambda e:errors.append(str(e)))
  p.on('console',lambda m:errors.append(m.text[:800]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append('HTTP '+str(r.status)+': '+r.url) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
  def frames(n):
   for start in range(0,n,30):
    q=p.evaluate(shoot.STEP,min(30,n-start))
    if q:errors.append(q);break
    p.wait_for_timeout(3)
  def clear():
   p.evaluate("()=>{ht27Stop();BOFCinematicDirector.cancel();H3.ending=null;H3.release=false;AP10_X.intro=null;story=fb2Talk=s6Opening=null;stagePlan=[];spawnClock=9999;enemies=[];pBullets=[];eBullets=[];boss=null;bossActive=false;subBoss=null;subBossActive=false;subBossDone=true;special=null;FS11.pending=null;FS11.boxes=[];}")
  def first(pk,coop=False):
   p.evaluate('q=>{coopOn=q.coop;pilotIndex=PILOTS.findIndex(a=>a.key===q.pk);p2Index=PILOTS.findIndex(a=>a.key==="lizzie");run.pilot=q.pk;run.mode="arcade";startRun(1);BOFCinematicDirector.cancel();story=fb2Talk=null;s6Opening=null;H3.release=false;setState(GS.PLAY);player.invuln=1e9;if(q.coop)player2.invuln=1e9;stagePlan=[];enemies=[];spawnClock=9999;}',dict(pk=pk,coop=coop))
   p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(1)&&[run.pilot,...(coopActive()?[run2.pilot]:[])].every(pk=>fs11ArtReady(pk))}',polling=50)
  def capture(name):
   # Use a visible beat of the existing invulnerability blink. No painter or
   # sprite is replaced; the next real frame renders the protected ship.
   p.evaluate('()=>{player.invuln=40002;if(coopActive())player2.invuln=40002;}');frames(1)
   p.screenshot(path=str(OUT/(name+'.png')))
   p.evaluate('()=>{player.invuln=1e9;if(coopActive())player2.invuln=1e9;}')
  def exercise(pk,level):
   key=p.evaluate('keybind.fire.find(k=>/^[a-z]$/.test(k))||" "');key='Space' if key==' ' else key
   if pk in ['maverick','falva']:
    p.evaluate('pk=>{window.__signatureEmitted=null;const name=pk==="maverick"?"releaseHelix":"releaseRoller",original=window[name];window.__signatureRelease=original;window[name]=function(){const a=pk==="maverick"?pBullets:rollers,n=a.length,r=original.apply(this,arguments),b=a[n];if(b)window.__signatureEmitted={kind:b.kind||"roller",damage:b.dmg,level:b._fs11Level||1,full:pk==="maverick"?b._isBall:b.full};return r;};}',pk)
   p.keyboard.down(key);frames(330 if pk=='falva' else 144)
   if pk in ['maverick','falva']:capture(pk+('-enhanced-charge' if level==2 else '-base-charge'))
   p.keyboard.up(key);frames(3)
   if pk in ['maverick','falva']:
    q=p.evaluate('pk=>{const q=window.__signatureEmitted,name=pk==="maverick"?"releaseHelix":"releaseRoller";window[name]=window.__signatureRelease;return {shot:q,expected:(pk==="maverick"?60+Math.max(1,run.wlevels[run.weapon]||1)*10:12)*(fs11Active(pk)?1.25:1)};}',pk)
    check(pk+': keyboard hold and release emits its real level '+str(level)+' charged attack',q.get('shot') and q['shot']['level']==level and q['shot']['damage']==q['expected'] and q['shot']['full'],q)
  pilots=p.evaluate('Object.keys(FS11_UPGRADES)')
  for pk in pilots:
   clear();p.evaluate('FS11.receipt=null');first(pk)
   frames(150)
   before=p.evaluate('()=>({boxes:FS11.boxes.map(q=>({pilot:q.pilot,y:q.y,open:q.open})),special:special?.pilot,draws:FS11.draws.opening||0})')
   capture(pk+'-incoming')
   check(pk+': an authored unopened box visibly descends before activation',len(before['boxes'])==1 and before['boxes'][0]['pilot']==pk and not before['boxes'][0]['open'] and before['boxes'][0]['y']>0 and not before.get('special') and before['draws']>0,before)
   frames(390)
   q=p.evaluate('()=>({pilot:special?.pilot,dur:special?.dur,level:special?._fs11Level,boxes:FS11.boxes.length,grants:FS11.events.filter(a=>a.event==="opening-special-collected"&&a.pilot===run.pilot).length,name:ph8Values().name})')
   check(pk+': actual arrival and collection activates its own base special',q.get('pilot')==pk and q.get('dur')==15 and q.get('level')==1 and q['boxes']==0,q)
   exercise(pk,1);capture(pk+'-base')
  clear();first('cole',True);frames(540)
  q=p.evaluate('()=>({p1:special?.pilot,p2:FS11.seat2.special?.pilot,t1:special?.t,t2:FS11.seat2.special?.t,boxes:FS11.boxes.length})')
  check('Co-op independently collects Cole and Lizzie supplies without replacing either ability',q.get('p1')=='cole' and q.get('p2')=='lizzie' and q['boxes']==0,q)
  capture('coop-start')
  clear();p.evaluate(shoot.SETUP,dict(state='PLAY',stage=6,pilot='cole',invuln=True))
  p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(6)}',polling=50)
  clear()
  p.evaluate("()=>{coopOn=false;run.stage=6;run._gp4StageX='right';run.mode='campaign';FS11.receipt=null;FS11.events=[];spawnBoss('rebelsquad');const R=boss._rebels;R.frIntro={done:true};R.h3Intro=null;boss.enter=false;boss._noHit=false;bossDefeated=false;rg4Init(boss);s6WingInit();s6Wing.all=true;s6Wing.supplyIndex=3;H3.release=false;player.invuln=1e9;}")
  p.wait_for_function('()=>{rg4Warm();return XART.rdy("ra4_ui")&&XART.rdy("ra7_air")}',polling=50)
  check('Stage X arrival records the real boss but grants no enhanced ability',p.evaluate('FS11.proof?.ref===boss&&!fs11UnlockFromStageX()&&!fs11Enhanced()'))
  # Let the real scheduler choose, collect its personal boxes, charge and fire.
  captures=set()
  for i in range(160):
   frames(30)
   q=p.evaluate('()=>boss?._rebels?.ships.filter(q=>q.rg4?.act?._fs11Name&&q.rg4.act.phase!=="recover").map(q=>q.key)||[]')
   for pk in q:
    if pk not in captures:capture('rebel-'+pk);captures.add(pk)
   if p.evaluate('Object.keys(FS11_REBELS).every(pk=>RG4.events.some(e=>e.event==="specialRelease"&&e.pilot===pk&&e.kind===FS11_REBELS[pk].kind))'):break
  q=p.evaluate('()=>({started:FS11.events.filter(e=>e.event==="rebel-signature-start"),released:RG4.events.filter(e=>e.event==="specialRelease"),draws:FS11.draws})')
  for pk in ['voss','nyx','rook','kaia','jace']:
   kind=p.evaluate('pk=>FS11_REBELS[pk].kind',pk)
   check(pk+': real enemy AI collects, warns and releases its personal signature',any(e['pilot']==pk and e['kind']==kind for e in q['started']) and any(e['pilot']==pk and e['kind']==kind for e in q['released']) and q['draws'].get(pk,0)>0,q)
  # Damage the real pilot pools, then run their authored physical deaths. This
  # is an accelerated protected clear, not a natural human campaign win.
  # A gang guard absorbs a hit before hull damage. Repeat real hits while the
  # physical death/dialogue controllers finish, without setting dead or HP.
  for i in range(100):
   p.evaluate("()=>{if(!boss||boss.dead)return;const R=boss._rebels;for(const q of R.ships){if(q.dead)continue;R.hit=q.i;R.frHit=null;rebelSquadDamage(boss,100000);} }")
   frames(30)
   if p.evaluate('bossDefeated&&FS11.proof?.ref.dead'):break
  q=p.evaluate('()=>({dead:boss?.dead,hp:boss?.hp,defeated:bossDefeated,alive:boss?._rebels?.ships.filter(q=>!q.dead).map(q=>({key:q.key,hp:q.hp})),proof:FS11.proof?.ref===boss})')
  check('The actual Stage X encounter reaches its defeat state before the reward',q.get('dead') and q.get('hp',1)<=0 and q.get('defeated'),q)
  q=p.evaluate('()=>({earned:fs11UnlockFromStageX(),receipt:FS11.receipt,repeat:fs11UnlockFromStageX()})')
  check('Stage X defeat permanently earns Signature Mk II exactly once',q['earned'] and not q['repeat'] and q.get('receipt',{}).get('earned'),q)
  p.evaluate('ap10StageXReward();openStageSelect(7,{})');frames(15)
  p.wait_for_function('()=>{map4eWarm();mapgWarm();return XART.rdy("map4e_landscape")&&XART.rdy("mapg_briefing")&&bmfReady("game")&&bmfReady("dialogue")}',polling=50)
  frames(2);p.wait_for_timeout(5800);frames(2)
  q=p.evaluate('()=>({key:MAPG.typing?.key,count:MAPG.typing?.count,reward:!!AP10_X.reward})')
  expected_copy='STAGE X CLEAR - SIGNATURE MK II'+'ALL NINE PILOT SPECIALS ENHANCED. 20 SECOND WINDOWS. YOUR NEXT SPECIAL PICKUP USES MK II. AIR SUPERIORITY SUPPLIES ALSO AWARDED.'
  check('The actual campaign map visibly paints the Signature Mk II reward',q['key']=='fs11-mk2' and q['count']==len(expected_copy) and q['reward'],q)
  capture('stagex-reward')
  receipt=p.evaluate('FS11.receipt')
  for pk in pilots:
   clear();p.evaluate('q=>{FS11.receipt=q;}',receipt);first(pk);frames(540)
   q=p.evaluate('()=>({pilot:special?.pilot,dur:special?.dur,level:special?._fs11Level,name:ph8Values().name,strikes:special?.strikes,chain:run._chainLightningLevel,time:timeScale})')
   check(pk+': its next real opening pickup uses the earned Mk II upgrade',q.get('pilot')==pk and q.get('dur')==20 and q.get('level')==2 and 'MK II' in q['name'],q)
   q=p.evaluate('()=>{const icon=iconBlit,draw=hudctx.drawImage,expected=fs11IconKey(run.pilot);let calls=0,matched=0;try{hudctx.drawImage=function(){calls++;return draw.apply(this,arguments)};iconBlit=function(g,key){const n=calls,r=icon.apply(this,arguments);if(key===expected&&calls>n)matched++;return r;};drawHUDStrip(hudctx);return {expected,matched};}finally{iconBlit=icon;hudctx.drawImage=draw;}}')
   check(pk+': the actual HUD paints its native special icon',q['matched']>0,q)
   exercise(pk,2);capture(pk+'-enhanced')
  saved=p.evaluate('campSnapshot()');p.evaluate('FS11.receipt=null');p.evaluate('s=>campApply(s)',saved)
  check('The real campaign save/apply path retains the reward',p.evaluate('fs11Enhanced()'))
  p.reload();p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
  check('A fresh game boot restores the earned profile unlock',p.evaluate('fs11Enhanced()'))
  check('No page, console, asset or renderer errors',not errors,errors);br.close()
except Exception as e:errors.append(type(e).__name__+': '+str(e));print(errors[-1],flush=True)
finally:
 stop();report=dict(passed=sum(q['passed'] for q in checks),failed=sum(not q['passed'] for q in checks),checks=checks,errors=errors)
 (OUT/'report.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps({k:report[k] for k in ['passed','failed','errors']}),flush=True)
sys.exit(1 if errors or report['failed'] else 0)
