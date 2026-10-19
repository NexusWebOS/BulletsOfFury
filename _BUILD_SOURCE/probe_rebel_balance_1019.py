"""Native five-on-five audit. Full allied AI, protected route bot, no win claim."""
from pathlib import Path
import argparse,ast,base64,http.server,json,sys
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/overnight_combat_1019/rebels';O.mkdir(parents=True,exist_ok=True)
ap=argparse.ArgumentParser();ap.add_argument('--tag',default='before');ap.add_argument('--seconds',type=int,default=90);ap.add_argument('--difficulties',default='normal,hard,furious');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--arm',choices=['baseline','candidate'],default='candidate');ap.add_argument('--captures',choices=['full','minimal'],default='full');ap.add_argument('--furious-heavy-slots',type=int,choices=[-1,0,1,2,3],default=-1);a=ap.parse_args()
SETUP=next(ast.literal_eval(n.value) for n in ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text()).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SETUP' for t in n.targets))
errors=[];cases=[];http.server.ThreadingHTTPServer.request_queue_size=128
port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=br.new_page(viewport=dict(width=1600,height=1000));p.set_default_timeout(180000)
  p.add_init_script("Object.defineProperty(navigator,'getGamepads',{value:()=>[]});")
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:700]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append(str(r.status)+' '+r.url.split('?')[0]) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
  p.evaluate('''()=>{window.RB19={};const round=rg4Round,attack=rg4Attack,shot=eShootT;
   rg4Round=function(){const q=round.apply(this,arguments);if(RB19.live&&q){RB19.rounds.push({time:RB19.time,pilot:q.owner?.key,kind:q.kind,gun:!!q._ra4Gun,speed:Math.hypot(q.vx,q.vy)});}return q;};
   rg4Attack=function(q,R,G){const old=q.rg4?.act,r=attack.apply(this,arguments),A=q.rg4?.act;if(RB19.live&&A&&A!==old)RB19.attacks.push({time:RB19.time,pilot:q.key,kind:A.kind,warm:A.warm,target:A.target?.key});return r;};
   eShootT=function(){const q=shot.apply(this,arguments);if(RB19.live&&q)RB19.shots++;return q;};
   const hit=playerHit;playerHit=function(source){if(!RB19.live)return hit.apply(this,arguments);if(player.dead||player.invuln>0||RB19.time<(RB19.hurtUntil||0))return;RB19.hits.push({time:RB19.time,source:String(source||''),x:player.x,y:player.y});RB19.hurtUntil=RB19.time+.95;player.invuln=57;};
   window.rb19Step=n=>{for(let i=0;i<n;i++){if(state!==GS.PLAY||B.dead){RB19.ended={time:RB19.time,state,bossDead:B.dead};return;}
    RB19.time+=1/60;const t=RB19.time;Input.keys={};Input.mouse.down=false;player.dead=player.out=false;
    if(!player._ra7Caught&&!player._ra7Thrown){player.x=camLeftX()+viewW()/2+Math.sin(t*.70)*Math.min(130,viewW()*.27);player.y=VH-100+Math.sin(t*.93)*27;}
    updatePlay(1/60);
    const now=B._rebels.gang1004;if(!now){RB19.lostOwner=true;return;}
    const acts=B._rebels.ships.filter(q=>!q.dead&&q.rg4?.act&&q.rg4.act.phase!=='recover');
    const eb=eBullets.filter(q=>!q.dead),pb=pBullets.filter(q=>!q.dead),ord=now.ord.filter(q=>!q.dead);
    RB19.peakEnemy=Math.max(RB19.peakEnemy,eb.length+ord.length);RB19.peakFriendly=Math.max(RB19.peakFriendly,pb.length);RB19.peakActive=Math.max(RB19.peakActive,acts.length);
    for(const q of B._rebels.ships){const A=q.rg4?.act;if(A&&A!==q._rb19Tracked){q._rb19Tracked=A;A._rb19WarmStart=t;}if(A&&A.phase!==A._rb19Phase){if(A.phase==='fire'||A.phase==='cast')RB19.releases.push({time:t,pilot:q.key,kind:A.kind,warm:A.warm,observed:t-A._rb19WarmStart});A._rb19Phase=A.phase;}}
    if(i%12===0){drawWorld(1/60);SC12.refresh();}
    if(Math.floor(t*4)>RB19.sampleN){RB19.sampleN=Math.floor(t*4);const near=eb.filter(q=>Math.hypot(q.x-player.x,q.y-player.y)<85).length;RB19.peakNear=Math.max(RB19.peakNear,near);
     RB19.samples.push({time:+t.toFixed(3),enemy:eb.length,ord:ord.length,friendly:pb.length,near,act:acts.map(q=>q.key+':'+q.rg4.act.kind+':'+q.rg4.act.phase),scene:now.scene?.kind||null,allies:(s6Wing?.ships||[]).filter(q=>q.hp>0&&q.phase!=='leave').length,rebel:B._rebels.ships.filter(q=>!q.dead).length});}
   }};}''')
  for diff in a.difficulties.split(','):
   for gang in [False,True]:
    name=diff+('-gang' if gang else '-opening')
    p.evaluate('''o=>{window.RBAL19_OFF=o.arm==='baseline'?1:0;if(o.heavySlots>=0)RBAL19.cfg.furious.heavySlots=o.heavySlots;if(o.seed){let x=o.seed>>>0;Math.random=()=>{x^=x<<13;x^=x>>>17;x^=x<<5;return(x>>>0)/4294967296;};}}''',dict(arm=a.arm,seed=a.seed,heavySlots=a.furious_heavy_slots))
    p.evaluate(SETUP,dict(stage=6,kind='rebelsquad',diff=diff,pilot='cole'))
    p.evaluate('''gang=>{window.R=B._rebels;rf28Init(B,R);R.frIntro={done:true};B.enter=B._noHit=false;window.G=rg4Init(B);H3.release=false;H3.ending=null;fb2Talk=fb2Intro=thaw=s6Opening=null;BOFCinematicDirector.cancel();AP10_X.intro=null;story=null;P2M.active=null;
     rg4Warm();s6WingInit();s6WingLaunch(4,true);s6Wing.beats=3;s6Wing.all=true;s6Wing.fakeDone=true;s6Wing.route='right';s6Wing.choice=false;s6Wing.boxes=[];s6Wing.supplyIndex=3;
     for(const q of s6Wing.ships)q.phase='fight';
     G.gang=gang;G.scene=null;G.rescueDone=true;G.rescueAt=Infinity;G.releaseAt=1.2;
     // Controlled gang case starts with the real gang director and all five foes
     // alive. Opening case preserves natural supply pickups. Allies remain live.
     if(gang)for(const q of R.ships){q.rg4.cd=1.4+q.i*1.65;q.rg4.armed=ra4AttackKind(q,G);}
     VP12.next=CP12.next=EP13.next=SEWER17.next=HM17.next=TARGET17.nextTank=999999;stagePlan=[];spawnClock=999999;subBossTriggered=aminiTriggered=true;warnT=0;warnKind=null;
     player.invuln=0;run.spaceMode=false;run.shield=0;special=thunderStorm=null;run.sonicT=run.dkT=0;run.weapon=0;run.wlevel=0;player.fireCd=999999;powerups=[];eBullets=[];pBullets=[];
     RB19={live:true,time:0,shots:0,hits:[],rounds:[],attacks:[],releases:[],samples:[],sampleN:-1,peakEnemy:0,peakFriendly:0,peakNear:0,peakActive:0};SC12.refresh();__bofFit();}''',gang)
    p.wait_for_function('()=>{stageLoadTick();rg4Warm();return stageLoadReady(6)&&XART.rdy(RA7.sheet)&&XART.rdy("ra4_ui")&&bmfReady("game")}',polling=50)
    for sec in range(a.seconds):
     for batch in range(5):p.evaluate('rb19Step(12)');p.wait_for_timeout(5)
     if sec in ([4,a.seconds-1] if a.captures=='minimal' else [4,11,24,44,69,a.seconds-1]):
      p.evaluate('shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);SC12.refresh();__bofFit();');p.screenshot(path=str(O/f'{a.tag}-{name}-{sec+1:03}.png'))
     if p.evaluate('!!RB19.ended||RB19.lostOwner'):break
    row=p.evaluate('''()=>({diff:diffKey,gang:G.gang,metrics:RB19,allies:s6Wing.ships.map(q=>({key:q.key,hp:q.hp,phase:q.phase,canBeHit:q.canBeHit})),rebels:R.ships.map(q=>({key:q.key,hp:q.hp,max:q.max,dead:q.dead,act:q.rg4.act?.kind})),events:G.events,airEvents:RA7.events})''');row['initialGang']=gang;row['protectedBot']='Scripted route, no player fire, full allied AI. Collision exposures throttled to 0.95s; invulnerability uses 57 native frames. Not human survival evidence.'
    row['initialSeed']=a.seed;row['arm']=a.arm;row['furiousHeavySlots']=p.evaluate('RBAL19.cfg.furious.heavySlots');row['seedCaveat']='Same starting RNG seed, native live AI. Different attack branches consume random numbers differently; trajectories are not paired after divergence.'
    cases.append(row);(O/(a.tag+'-report.json')).write_text(json.dumps(dict(cases=cases,errors=errors),indent=2)+'\n')
    m=row['metrics'];print(json.dumps(dict(case=name,seconds=m['time'],enemyPeak=m['peakEnemy'],friendlyPeak=m['peakFriendly'],nearPeak=m['peakNear'],activePeak=m['peakActive'],contacts=len(m['hits']),attacks=len(m['attacks']),releases=len(m['releases']),aliveAllies=sum(q['hp']>0 and q['phase']!='leave' for q in row['allies']))),flush=True)
  br.close()
finally:stop()
print(json.dumps(dict(cases=len(cases),errors=errors)),flush=True);sys.exit(bool(errors))
