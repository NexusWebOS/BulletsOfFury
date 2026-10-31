from pathlib import Path
import sys,json,http.server,hashlib,math
from PIL import Image
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];W=R/'_shots/luminaire_plasma_1031';W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'))
from shoot import serve,STEP
from barrage_review_common_1025 import boot
http.server.ThreadingHTTPServer.request_queue_size=256;checks=[];errors=[];runs=[]
def ck(n,v,d=None):
 checks.append(dict(name=n,passed=bool(v),data=d));(W/'checks.json').write_text(json.dumps(checks,indent=2));print('PASS'if v else'FAIL',n,str(d)[:500]if not v else'',flush=True);assert v,(n,d)
A=json.loads((R/'assets/game/levels/stage_08/boss/luminaire_plasma_1031/manifest.json').read_text())
ck('Seven authored banks contain192 even fixed-cell frames and editable sources',len(A['banks'])==7 and sum(a['frames']for a in A['banks'].values())==192 and all(a['w']%2==a['h']%2==0 and(R/'assets/game/levels/stage_08/boss/luminaire_plasma_1031'/(n+'.aseprite')).exists()for n,a in A['banks'].items()))
ck('All page dimensions fit4096px and preserve full fixed cells',all(max(Image.open(R/p['path']).size)<=4096 and Image.open(R/p['path']).size==(a['w']*a['cols'],a['h']*math.ceil(p['frames']/a['cols']))for a in A['banks'].values()for p in a['pages']))
SETUP="""([rank,pilot])=>{diffKey=rank;run.pilot=pilot;run.speed=0;run.armor=run.shield=0;spawnBoss('vileexistence');window.B=boss;const J=j3State(B);for(const i of V18.forms)if(i!==0)J.hp[i]=0;v18Enter(B,2,0);B._r30.mode='fight';B.enter=B._noHit=false;player.reset();player.x=worldWidth()/2;player.y=VH-65;player.dead=player.out=false;player.invuln=0;player.roll=player.somer=null;run.speed=run.armor=run.shield=0;DBGT.god=false;eBullets.length=0;RD97.events=[];for(const k of Object.keys(Input.keys))Input.keys[k]=false;setState(GS.PLAY);window.P=rd78Start(B);window.hp97=B.hp;}"""
port,stop=serve(str(R))
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=boot(br.new_context(viewport={'width':1280,'height':800}),port,8,errors,'boss')
  p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(8)&&rd97Keys().every(k=>XART.rdy(k))}',timeout=180000)
  p.evaluate("()=>{window.old97=0;const f=rd78Blit;rd78Blit=function(n){if(['warning','blast','recovery'].includes(n))old97++;return f.apply(this,arguments)};}")
  ck('Old Luminaire warning and flood pages are not queued',p.evaluate("(()=>{const keys=_stageLoads[8].keys;return rd78Keys().length===0&&Object.values(RD78_ART.banks).flatMap(a=>a.pages.map(p=>p.key)).every(k=>!keys.includes(k))})()"))
  def step(n):
   for i in range(0,n,12):
    e=p.evaluate(STEP,min(12,n-i));assert not e,e;p.wait_for_timeout(1)
  def shot(name):p.evaluate('()=>{drawWorld(0);SC12.refresh();__bofFit()}');p.screenshot(path=str(W/(name+'.png')))
  for rank in ['normal','hard','furious']:
   for pilot in ['cole','juggernaut','yuri']:
    p.evaluate(SETUP,[rank,pilot]);land=p.evaluate('({...P.land})');saw=set();complete=False
    for i in range(100):
     p.evaluate("()=>{Input.keys.w=player.y>RD97_ART.safeY+2;Input.keys.s=player.y<RD97_ART.safeY-2;}");step(5)
     q=p.evaluate('({t:P.t,phase:P.phase,dead:player.dead,hits:P.hits.size,x:player.x,y:player.y,hp:B.hp,land:P.land,radius:P.radius,active:!!rd78Act(B)})');saw.add(q['phase'])
     if rank=='furious'and pilot=='cole':
      tag={'cast':'01-chest-charge','flight':'02-thrown-orb','arming':'03-ground-mine','rise':'04-rising-dome','crest':'05-clear-top'}
      if q['phase']in tag and q['phase']not in getattr(step,'shots',set()):
       step.shots=getattr(step,'shots',set())|{q['phase']};shot(tag[q['phase']])
     if not q['active']:complete=True;break
    label=rank+' '+pilot;ck(label+' reaches the clear top by ordinary movement without GOD or upgrades',complete and not q['dead']and q['hits']==0 and q['y']<=75 and 'crest'in saw and 'recover'in saw,q)
    ck(label+' keeps the landing point and native HP unchanged',q['land']==land and p.evaluate('B.hp===hp97'))
    runs.append(dict(rank=rank,pilot=pilot,result=q))
  p.evaluate(SETUP,['furious','cole']);step(32);shot('charge-ground-retina');first=p.evaluate('({...P.land})');p.evaluate('player.x+=100');step(38);q=p.evaluate('({phase:P.phase,land:P.land,orb:rd97Orb(B,P)})');ck('Retina commits before release and never chases the player',q['land']==first and q['phase']=='flight',q)
  step(29);shot('mine-landed');ck('Orb becomes a harmless arming mine at the marked floor point',p.evaluate('P.landed&&P.phase==="arming"&&!player.dead&&!rd78Inside(P,player.x,player.y)'))
  p.evaluate('window.t97=P.t;window.phase97=P.phase;setState(GS.PAUSE)');step(55);ck('Pause freezes mine arming and growth',p.evaluate('P.t===t97&&P.phase===phase97'));p.evaluate('setState(GS.PLAY)')
  # Move this fixture out of danger and inspect the fully grown field.
  p.evaluate('player.x=P.land.x;player.y=RD97_ART.safeY');step(185);shot('full-plasma-dome')
  ck('Giant half-dome has a clear upper band and dangerous lower floor',p.evaluate('P.phase==="crest"&&!rd78Inside(P,P.land.x,70)&&rd78Inside(P,P.land.x,350)&&rd78Inside(P,P.land.x,VH-10)&&P.radius>370'))
  ck('Dome rise radii are monotonically larger from the fixed base',all(a['radius']<b['radius']for a,b in zip(A['banks']['rise']['poses'],A['banks']['rise']['poses'][1:])))
  ck('Only the actual landing Retina and new generated effects draw',p.evaluate('old97===0&&RD97.draws.retina>0&&RD97.draws.cast>0&&RD97.draws.flight>0&&RD97.draws.mine>0&&RD97.draws.rise>0&&RD97.draws.crest>0&&RD97.draws.fall>0'))
  for name,x,y in [('centre',340,445),('south-edge',340,502)]:
   p.evaluate(SETUP,['furious','cole']);p.evaluate('([x,y])=>{player.x=x;player.y=y}',[x,y]);step(220);ck(name+' cannot hide inside/below the detonating mine',p.evaluate('RD97.events.some(e=>e.event==="plasma-contact"&&e.dead)'))
  p.evaluate(SETUP,['furious','cole']);step(145);p.evaluate('window.draw97=JSON.stringify(RD97.draws);v18Clear(B)');step(3);ck('Cancellation removes every mine/dome draw immediately',p.evaluate('!rd78Act(B)&&JSON.stringify(RD97.draws)===draw97'))
  ck('Cancellation stops long charge/release voices',p.evaluate('RD78.cues.every(k=>Snd.pools[k].slots.every(s=>!s?.el||s.el.paused))'))
  p.evaluate(SETUP,['furious','cole']);p.evaluate('()=>{v18Clear(B);B._r30.v18.rd78Decisions=0;window.book97=[];for(let i=0;i<3;i++){v18StartAttack(B);book97.push(B._r30.v18.attack.type);v18Clear(B)}}');ck('Two native claw combos still precede each plasma Luminaire',p.evaluate('book97.join(",")==="rd88-extended-claws,rd88-extended-claws,luminaire"'),p.evaluate('book97'))
  p.evaluate(SETUP,['furious','cole']);step(38);p.evaluate('()=>{window.rig97=v18Rig(B);const part=B.parts.find(p=>p.id==="left");B._lastPart=part;modularHit(part.hp)}');ck('Breaking an arm uses the native whole-part owner and removes its hit target',p.evaluate('B.parts.find(p=>p.id==="left").destroyed&&!v18Rig(B).some(v=>v.p.id==="left")'))
  p.evaluate('()=>{v18Clear(B);B._r30.mode="fight";B.enter=B._noHit=false;window.P=rd78Start(B);B._lastPart=B.parts[0];modularHit(B.hp)}');step(150);ck('Native final-main-life defeat cancels the mine',p.evaluate('!rd78Act(B)&&B.hp===0&&B._r30.mode==="dr5Death"'))
  p.evaluate(SETUP,['furious','cole']);p.evaluate('spawnBoss("vileexistence");window.B=boss');ck('Retry restores normal first-host ownership with no mine',p.evaluate('!rd78Own(B)&&!rd78Act(B)&&j3State(B).encounter===0'))
  ck('No native browser or rendering errors',not errors,errors);br.close()
finally:stop()
ck('Core game source remains unchanged',hashlib.sha256((R/'assets/game.js').read_bytes()).hexdigest()=='024a0933c5729b6afa2a6e88864574636293bdb535d9f4e5eb91d36bb98509de');(W/'runs.json').write_text(json.dumps(runs,indent=2));print('RESULT',len(checks),'checks passed')
