"""Native Chromium verification for stored bosses restored as field enemies.
Invulnerable fixture observations are not evidence of human clearability.
"""
from pathlib import Path
import ast,json,sys,http.server
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/late_legends_1018/native';O.mkdir(parents=True,exist_ok=True)
SETUP=next(ast.literal_eval(n.value) for n in ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text()).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SETUP' for t in n.targets))
checks=[];errors=[];rows=[];http.server.ThreadingHTTPServer.request_queue_size=128
def check(name,ok,data=None):
 checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name+((' '+json.dumps(data)) if not ok else ''),flush=True)
port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=br.new_page(viewport=dict(width=1600,height=900));p.set_default_timeout(180000)
  p.add_init_script("Object.defineProperty(navigator,'getGamepads',{value:()=>[]});")
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:700]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append(str(r.status)+' '+r.url.split('?')[0]) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4&&typeof LL18!=="undefined"');p.evaluate(shoot.TRAP_RAF);p.wait_for_timeout(35)
  p.evaluate("pilotIndex=PILOTS.findIndex(q=>q.key==='cole');run.pilot='cole';startRun(8)")
  p.evaluate('''()=>{window.llHits=0;playerHit=function(){llHits++;};window.llPixels=fn=>{ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);ctx.translate(-camX,0);fn();const a=Array.from(ctx.getImageData(0,0,cv.width,cv.height).data);ctx.restore();return a;};
   window.llChanged=(a,b)=>{let n=0;for(let i=0;i<a.length;i+=4)if(Math.max(Math.abs(a[i]-b[i]),Math.abs(a[i+1]-b[i+1]),Math.abs(a[i+2]-b[i+2]))>20)n++;return n;};
   window.llWarns=[];const warning=combatWarningDraw;combatWarningDraw=function(e,q){if(e?._ll18)llWarns.push({id:e._ll18.id,progress:q.progress,x:q.x,y:q.y,ex:q.ex,ey:q.ey});return warning.apply(this,arguments);};
   window.llEscortShots=[];const mega=s8MegaTick;s8MegaTick=function(e){const first=eBullets.length,r=mega.apply(this,arguments);if(e?._ll18Escort)for(const b of eBullets.slice(first))if(!b.dead)llEscortShots.push({type:e.type,kind:b.kind,x:b.x,y:b.y});return r;};
   window.llRealRounds=[];const round=ll18Shot;ll18Shot=function(){const b=round.apply(this,arguments);if(b&&!b.dead)llRealRounds.push(b);return b;};}''')
  def frames(n,extra=''):
   for i in range(0,n,12):
    p.evaluate('(n)=>{for(let i=0;i<n;i++){updatePlay(1/60);'+extra+'drawWorld(1/60);debugRecFrame();}}',min(12,n-i));p.wait_for_timeout(5)
  def snap(name):
   p.evaluate('()=>{shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);SC12.refresh();__bofFit();}');p.screenshot(path=str(O/(name+'.png')))
  def setup(stage,diff='normal'):
   p.evaluate(SETUP,dict(stage=stage,diff=diff,pilot='cole'))
   p.wait_for_function('(n)=>{stageLoadTick();return stageLoadReady(n)&&ll18Keys(n).every(k=>XART.rdy(k))&&bmfReady("game")}',arg=stage)
   p.evaluate('''()=>{s6Opening=null;story=fb2Talk=fb2Intro=null;BOFCinematicDirector.cancel();AP10_X.intro=null;P2M.active=null;H3.ending=null;H3.release=false;stagePlan=[];warnT=0;warnKind=null;
    subBossDone=true;subBossTriggered=aminiTriggered=true;VP12.next=CP12.next=EP13.next=SEWER17.next=TARGET17.nextTank=999999;
    player.x=worldWidth()/2;player.y=VH-70;player.invuln=0;run.shield=0;run.spaceMode=false;bossWarned=false;bossDefeated=false;
    for(const k of ['j','k','y','a','d','w','s'])Input.keys[k]=false;LL18.events=[];llWarns=[];llEscortShots=[];llRealRounds=[];__bofFit();}''')
  for diff in ['normal','hard','furious']:
   for kind in ['ll18raptor','ll18spear','ll18herald','ll18brood']:
    setup(8,diff);p.evaluate('(kind)=>window.E=spawnEnemy(kind,worldWidth()/2,viewTopY()-150,{})',kind)
    frames(660)
    row=p.evaluate('''()=>({diff:diffKey,kind:E.type,phase:E._ll18.phase,shots:E._ll18.shots,cycles:E._ll18.cycles,
     tell:LL18.events.filter(q=>q.event==='tell'),release:LL18.events.filter(q=>q.event==='release'),
     artillery:LL18.events.filter(q=>q.event==='ice-artillery'),launch:LL18.events.filter(q=>q.event==='scout-launch').length,
     draws:LL18.draws[E.type],warns:llWarns.length,hp:E.maxhp,seedControllers:Object.keys(E).filter(k=>/^_(s8mega|alien1003|frRealmAI|ep13|eb11|air17|modJet)$/.test(k)),
     escortAttacks:llEscortShots.length,body:{w:E._drawW,h:E._drawH,x:E.x,y:E.y,home:E._ll18.homeY,viewTop:viewTopY(),viewH:viewH()},boss:bossActive||subBossActive,retina:_lockTargets().some(t=>t===E||t.e===E||t.owner===E)})''')
    rows.append(row)
    check(diff+' '+kind+' has one owner and native pixels',row['draws']>10 and not row['seedControllers'] and not row['boss'],row)
    check(diff+' '+kind+' stays in its firing pocket',abs(row['body']['y']-row['body']['home'])<.01,row['body'])
    check(diff+' '+kind+' attacks repeatedly after warnings',len(row['release'])>=2 and len(row['tell'])>=2 and row['cycles']>=2 and all(q['warning']>=.7 for q in row['tell']),dict(release=len(row['release']),cycles=row['cycles'],shots=row['shots']))
    if kind=='ll18spear':check(diff+' ice fan and committed glacial targets both fire',row['shots']>=10 and bool(row['artillery']),row)
    if kind=='ll18brood':
     check(diff+' carrier launches real fighters which attack',row['launch']>=1 and row['escortAttacks']>0,row)
     escort=p.evaluate('''()=>{const e=enemies.find(e=>e._ll18Escort&&!e.dead);if(!e)return null;e.flash=0;const a=llPixels(()=>drawEnemy(e)),hp=e.hp;_dmgBullet={kind:'mg',x:e.x,y:e.y};hitEnemy(e,1);_dmgBullet=null;const b=llPixels(()=>drawEnemy(e));window.llEscort=e;return{pixels:llChanged(a,b),damage:hp-e.hp,flash:e.flash};}''')
     check(diff+' launched scout visibly flashes when damaged',escort and escort['pixels']>10 and escort['flash']>0 and escort['damage']>0,escort)
     frames(18);check(diff+' launched scout flash expires',p.evaluate('llEscort.flash<=0'))
    if kind in ['ll18raptor','ll18herald']:check(diff+' warned beam lanes are actually rendered',row['warns']>20,row['warns'])
    if diff=='furious':snap(kind+'-furious')
    bullet=p.evaluate('''()=>{if(!llRealRounds.length)return{pixels:0};const all=eBullets,b={...llRealRounds[0],x:worldWidth()/2,y:VH*.55,dead:false,t:.12};eBullets=[];const a=llPixels(()=>drawBullets());eBullets=[b];const c=llPixels(()=>drawBullets());eBullets=all;return{pixels:llChanged(a,c),kind:b.kind,realm:b._frRealm,toxic:!!b._s7modGun,ice:b._l23fx,herald:b._heraldProjectile};}''')
    check(diff+' '+kind+' actual emitted projectile has native authored pixels',bullet['pixels']>20,bullet)
    flash=p.evaluate('''()=>{window.scoreBefore=run.score;window.killsBefore=stageStats.kills;E.flash=0;const a=llPixels(()=>drawEnemy(E)),hp=E.hp;_dmgBullet={kind:'mg',x:E.x,y:E.y};hitEnemy(E,1);_dmgBullet=null;const c=llPixels(()=>drawEnemy(E));return{pixels:llChanged(a,c),damage:hp-E.hp,flash:E.flash};}''')
    check(diff+' '+kind+' native damage visibly flashes authored pixels',flash['pixels']>20 and flash['damage']>0 and flash['flash']>0,flash)
    frames(18);check(diff+' '+kind+' flash expires',p.evaluate('E.flash<=0'))
    if diff=='normal':
     p.evaluate('''()=>{enemies=[E];pBullets=[];eBullets=[];run.weapon=0;run.wvars[0]=null;run.wlevels[0]=run.wlevel=0;run.forge={};run.forgeForms={};run.infusion=null;run.loadout=[0];chaingunUnlocked=false;run._earnedUnlocks.chaingun=false;powerups=[];player.fireCd=0;Input.keys.j=true;window.beforeJ=E.hp;}''')
     frames(55,'player.x=E.x;player.y=E.y+150;powerups=[];');p.evaluate('Input.keys.j=false')
     check(kind+' actual centred J gun damages the veteran',p.evaluate('E.hp<beforeJ'),p.evaluate('({before:beforeJ,hp:E.hp})'))
    p.evaluate('''()=>{if(E._dyingT==null&&!E.dead){hitEnemy(E,1e7);hitEnemy(E,1e7);}}''');frames(45)
    death=p.evaluate('''()=>({gone:E.dead||!enemies.includes(E),score:run.score-scoreBefore,kills:stageStats.kills-killsBefore,clear:bossDefeated,boss:bossActive||subBossActive,continueReward:E._continueEligible,beams:LL18.beams.filter(b=>b.owner===E).length,targets:groundTargetingFx.filter(q=>q.owner===E&&!q.dead).length})''')
    check(diff+' '+kind+' dies once as an ordinary enemy without stage clear',death['gone'] and death['score']>0 and death['kills']==1 and not death['clear'] and not death['boss'] and not death['continueReward'] and death['beams']==0 and death['targets']==0,death)
  for kind in ['ll18raptor','ll18spear','ll18herald','ll18brood']:
   tier=[next(r for r in rows if r['diff']==d and r['kind']==kind) for d in ['normal','hard','furious']]
   check(kind+' health and first reaction escalate Normal / Hard / Furious',tier[0]['hp']<tier[1]['hp']<tier[2]['hp'] and tier[0]['release'][0]['reaction']>tier[1]['release'][0]['reaction']>tier[2]['release'][0]['reaction'],[dict(hp=r['hp'],reaction=r['release'][0]['reaction']) for r in tier])
  # The same stagger bug affected the delayed second aircraft in native waves.
  for diff in ['normal','hard','furious']:
   setup(8,diff);p.evaluate("window.E=spawnEnemy('s8interceptor',worldWidth()/2,viewTopY()-100,{_stagger:.45});E._ll18Escort={age:0};")
   frames(640)
   row=p.evaluate('({stagger:E._stagger,sequence:E._frRealmAI?.seq||0,shots:llEscortShots.length})')
   check(diff+' original delayed Stage 8 scout consumes stagger and fires',row['stagger']==0 and row['sequence']>=1 and row['shots']>0,row)
  for stage,kind in [(7,'mm1003_riflelocust'),(8,'mm1003_hexpyre')]:
   for diff in ['normal','hard','furious']:
    setup(stage,diff);p.evaluate('(kind)=>{window.E=spawnEnemy(kind,worldWidth()/2,viewTopY()-100,{_stagger:.45});EP13.next=0;EP13.events=[];}',kind)
    frames(780)
    row=p.evaluate('({stagger:E._stagger,cycles:E._ep13Cycles||0,releases:EP13.events.filter(e=>e.event==="release").length,attacks:EP13.events.filter(e=>e.event==="ring"||e.event==="rifle").length})')
    check(str(stage)+' '+diff+' delayed '+kind+' unlocks its advanced native attacks',row['stagger']==0 and row['cycles']>0 and row['releases']>0 and row['attacks']>0,row)
  # The timer repair touches the shared native fleet path. Verify actual hurt
  # pixels and expiry for every original roster slot, including its remap.
  for kind in p.evaluate('Object.keys(S8MEGA)'):
   setup(8,'furious');p.evaluate('(kind)=>{window.E=spawnEnemy(kind,worldWidth()/2,viewTopY()+120,{_stagger:.45});E._noHit=false;}',kind)
   p.wait_for_function('()=>llPixels(()=>drawEnemy(E)).some((v,i)=>i%4===3&&v>0)',timeout=180000)
   row=p.evaluate('''()=>{E.flash=0;if(E._mm1003)for(const p of E._mm1003.parts)p.flash=0;const part=E._mm1003?.parts.find(p=>!p.dead&&['gun','arm'].includes(p.kind)),m=part?mm1003PartCenter(E,part):{x:E.x,y:E.y};
    const a=llPixels(()=>drawEnemy(E)),hp=part?part.hp:E.hp;_dmgBullet={kind:'mg',x:m.x,y:m.y};hitEnemy(E,1);_dmgBullet=null;const b=llPixels(()=>drawEnemy(E));return{type:E.type,pixels:llChanged(a,b),flash:E.flash,part:part?.flash,damage:hp-(part?part.hp:E.hp)};}''')
   check(kind+' delayed roster slot visibly flashes on native damage',row['pixels']>10 and row['flash']>0,row)
   frames(22);check(kind+' hurt flash expires with its native owner',p.evaluate('E.flash<=0&&(!E._mm1003||E._mm1003.parts.every(p=>!p.flash))'))
  # Stage 7 introduces the green carrier / stored Raptor before Stage 8.
  for diff in ['normal','hard','furious']:
   setup(7,diff);p.evaluate("window.E=spawnEnemy('ll18brood',worldWidth()/2,viewTopY()-150,{})");frames(800)
   row=p.evaluate('''()=>({launch:LL18.events.filter(q=>q.event==='scout-launch').length,shots:E._ll18.shots,cycles:E._ll18.cycles,escortShots:llEscortShots.length,escorts:enemies.filter(e=>e._ll18Escort).map(e=>({type:e.type,sequence:e._frRealmAI?.seq||0}))})''')
   check('Stage 7 '+diff+' carrier brings firing Stage 8 scouts',row['launch']>0 and row['shots']>0 and row['escortShots']>0,row)
   if diff=='furious':snap('stage7-carrier-furious')
   p.evaluate('stageTimer=curStage.length-2');frames(160)
   check('Stage 7 '+diff+' approach cancels attacks and withdraws veterans',p.evaluate('LL18.beams.length===0&&E._ll18.phase==="leave"&&enemies.filter(e=>e._ll18Escort).every(e=>e._fcd>=900)'))
  # Observe authored stage wave plans under input; no boss or mini force kills.
  for stage in [7,8]:
   for diff in ['normal','hard','furious']:
    setup(stage,diff)
    p.evaluate('''()=>{stagePlan=buildStagePlan(run.stage);waveIdx=0;spawnClock=0;window.llCampaignSeen=new Set();window.llFamilySeen=new Set();window.llNativeTanks=[];window.llMax=0;player.invuln=0;Input.keys.j=true;run.weapon=0;run.wvars[0]=null;run.wlevels[0]=run.wlevel=3;run.forge={};run.forgeForms={};run.infusion=null;run.loadout=[0];}''')
    frames(3540,"for(const e of enemies){llFamilySeen.add(e.type);if(e._ll18)llCampaignSeen.add(e.type);if(e._modTank===7)llNativeTanks.push({x:e.x,l:sewer17Band(e).l,r:sewer17Band(e).r});}llMax=Math.max(llMax,enemies.filter(e=>ll18Alive(e)&&e._ll18).length);if(!bossActive&&!subBossActive){player.x=worldWidth()/2+Math.sin(LL18.clock*.8)*VW*.32;player.y=VH-60;}powerups=[];")
    row=p.evaluate('''()=>({stage:run.stage,diff:diffKey,seen:[...llCampaignSeen],families:[...llFamilySeen],max:llMax,cap:ll18Profile().cap,tanks:llNativeTanks.length,badTanks:llNativeTanks.filter(e=>e.x<e.l-.1||e.x>e.r+.1).length,timer:stageTimer,boss:bossActive,mini:subBossActive,events:LL18.events.filter(q=>q.event==='spawn'||q.event==='release')})''')
    check(str(stage)+' '+diff+' real plan reaches restored field veterans',len(row['seen'])>=(4 if stage==8 else 2) and row['max']<=row['cap'],dict(seen=row['seen'],max=row['max'],cap=row['cap'],timer=row['timer']))
    if stage==7:check(diff+' sewer tanks stay on centre floor during mixed waves',row['tanks']>0 and row['badTanks']==0,dict(samples=row['tanks'],outside=row['badTanks']))
    if stage==8:check(diff+' Blue Hybrid, Furnace Maw and Tentacle Cannon stay in the stage',all(k in row['families'] for k in ['mm1003_bluehybrid','mm1003_furnacemaw','s8tentacle']),row['families'])
    if stage==8:check(diff+' Stage8 director reserves room for the complete late fleet',p.evaluate('stageAiProfile(8).cap')==dict(normal=5,hard=7,furious=9)[diff])
    (O/(str(stage)+'-'+diff+'-waves.json')).write_text(json.dumps(row,indent=2))
    snap(str(stage)+'-'+diff+'-wave-end')
  check('native game page, console and asset responses are clean',not errors,errors)
  summary=dict(passed=sum(c['passed'] for c in checks),failed=sum(not c['passed'] for c in checks),checks=checks,rows=rows,errors=errors)
  (O/'results.json').write_text(json.dumps(summary,indent=2));print('SUMMARY '+json.dumps({k:summary[k] for k in ['passed','failed']}),flush=True)
  br.close()
finally:stop()
sys.exit(1 if errors or any(not c['passed'] for c in checks) else 0)
