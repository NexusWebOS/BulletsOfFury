"""Native pixels and real audio/weapon entry points for part-two presentation."""
from pathlib import Path
import sys,json
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
OUT=ROOT/'_shots/part2_1010/presentation';OUT.mkdir(parents=True,exist_ok=True)
checks=[];errors=[];shots=[]
def check(name,value,data=None):
 checks.append(dict(name=name,passed=bool(value),data=data));print(('PASS ' if value else 'FAIL ')+name,flush=True)
 if not value:print(json.dumps(data),flush=True)
port,stop=shoot.serve(str(ROOT))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--autoplay-policy=no-user-gesture-required'])
  p=br.new_page(viewport=dict(width=1600,height=900));p.set_default_timeout(120000)
  p.add_init_script("window.p2AudioPlays=[];const play=HTMLMediaElement.prototype.play;HTMLMediaElement.prototype.play=function(){p2AudioPlays.push({src:this.src.split('/').pop(),volume:this.volume,ready:this.readyState});return play.apply(this,arguments);};")
  p.on('pageerror',lambda e:errors.append(str(e)))
  p.on('console',lambda m:errors.append(m.text[:900]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append('HTTP '+str(r.status)+': '+r.url.split('?')[0]) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>3');p.evaluate(shoot.TRAP_RAF)
  def frames(n):
   for i in range(0,n,15):
    e=p.evaluate(shoot.STEP,min(15,n-i))
    if e:errors.append(e)
    p.wait_for_timeout(3)
  def snap(name):p.screenshot(path=str(OUT/(name+'.png')));shots.append(name+'.png')
  def scene(n,pk='lizzie'):
   p.evaluate('()=>{P2M.active=P2M.pending=P2M.choice=null;run.mode="arcade";coopOn=false;GP4.route=null;delete run._gp4StageX;}')
   p.evaluate(shoot.SETUP,dict(state='PLAY',stage=n,pilot=pk,invuln=True))
   p.wait_for_function('n=>{stageLoadTick();return stageLoadInfo(n).ready}',arg=n,polling=50)
   p.evaluate('()=>{BOFCinematicDirector.cancel();story=null;fb2Talk=null;s6Opening=null;H3.ending=null;H3.release=false;stagePlan=[];enemies=[];powerups=[];pBullets=[];eBullets=[];boss=subBoss=null;bossActive=subBossActive=false;subBossDone=true;player.invuln=1e9;player._spawnClearT=1e9;special=null;atomBooms=[];s67Nukes=[];atomFlash=0;run.dkT=0;run.sonicT=0;run.forge={};run.forgeForms={};run.infusion=null;run._spaceShadowHeld=false;}')
  scene(2)
  p.evaluate('()=>{Snd.prepare("av3_firewall_launch");Snd.prepare("enemyOrbImpact");window.p2Played=[];const fire=Audio.SFX.firewallArrive;Audio.SFX.firewallArrive=function(){p2Played.push("firewall-arrival");return fire.apply(this,arguments);};wfx.fseq={ph:"waves",t:0,shown:3,fired:0,lanes:[player.x-100,player.x,player.x+100],dir:[0,0,0],wave:null,_bt:[]};wfxUpdate(.016);}')
  p.wait_for_timeout(400);frames(15)
  q=p.evaluate('()=>({calls:p2Played,media:p2AudioPlays.filter(q=>/firewall_launch|fire_wave/.test(q.src)),pool:Snd.pools.av3_firewall_launch.slots.filter(q=>q?.attached).map(q=>({ready:q.el.readyState,volume:q.el.volume,error:q.el.error?.code,paused:q.el.paused,duration:q.el.duration}))})')
  check('The firewall arrival calls its real decoded non-muted sample on wave birth',bool(q['calls']) and bool(q['media']) and any(x['ready']>=3 and x['volume']>0 and not x.get('error') for x in q['pool']),q);snap('firewall-arrival')
  p.evaluate('()=>{wfx.fseq=null;const b={kind:"orb",x:player.x,y:player.y-120,lv:3,_el:"fire",w:52,h:52,shardN:5};fb10Blast(b,b.x,b.y,"impact");}')
  frames(13);snap('fire-orb-impact');q=p.evaluate('()=>({draws:P2.draws.orbBurst,event:P2.events.findLast(q=>q.event==="orb-impact")})');check('Fire Orb contact draws the opaque 32-pose impact at the actual hit point',q['draws']>0 and q['event']['element']=='fire',q)
  p.evaluate('()=>{const b={kind:"orb",x:player.x+80,y:player.y-150,lv:3,_el:"kinetic",w:52,h:52,shardN:7};fb10Blast(b,b.x,b.y,"impact");}')
  frames(13);snap('kinetic-orb-impact')
  p.evaluate('()=>{on5LaunchEncounter({stage:2,role:"boss",code:"BOSS2"});}')
  frames(180);q=p.evaluate('()=>({kind:boss.kind,furnace:!!boss._fz,draws:P2.draws.fireBeam})');snap('furnace-boss')
  p.evaluate('()=>{window.p2FurnacePos={x:boss.x,y:boss.y};const F=boss._fz;F.phase="core";F.trans=0;F.idx=1;F.attack="coreLaser";F.at=2.3;F.burstBeat=-1;F.pools.left=F.pools.right=0;boss._mwStun=0;story=null;fb2Talk=null;}')
  frames(8);snap('furnace-fire-laser');q=p.evaluate('()=>({beam:P2.draws.fireBeam,muzzle:P2.draws.fireMuzzle,root:P2.draws.fireRoot})');check('The real Furnace beam draws the32-frame column and16-frame flared core connection',(q.get('beam') or 0)>0 and (q.get('muzzle') or 0)>0 and (q.get('root') or 0)>0,q)
  scene(5)
  p.evaluate('()=>{run._spaceShadowHeld=true;window.p2Preview=forgePreviewNew(3,"ice",3);for(let i=0;i<55;i++)forgePreviewTick(p2Preview,260,300,1/60);}')
  q=p.evaluate('()=>({err:p2Preview.err,beams:p2Preview.bullets.filter(q=>q.kind==="beam").map(q=>({inf:q._inf,age:q._bt})),stage:run.stage,space:run.spaceMode,held:run._spaceShadowHeld})');check('The Ice Laser preview runs the real animated laser after a space stage and restores the live hull',not q['err'] and bool(q['beams']) and q['beams'][0]['age']>0 and q['stage']==5 and q['held'],q)
  p.evaluate('()=>{forgePreviewDraw(p2Preview,80,110,260,300);}');snap('ice-preview-after-space')
  p.evaluate('setState(GS.STAGECLEAR)');frames(40);snap('stage-clear-no-bottom-artifact');q=p.evaluate('()=>({hud:getComputedStyle(document.getElementById("hud-row")).visibility,state,stageClear:state===GS.STAGECLEAR})');check('Stage Clear hides the gameplay HUD before laying out its menu',q['stageClear'] and q['hud']=='hidden',q)
  scene(6)
  p.evaluate('()=>{GP4.route="right";GP4.routeReady=true;GP4.stage6Only=true;gp4QuickEncounter();}');frames(150)
  q=p.evaluate('()=>({friends:s6Wing.ships.map(q=>q.key),hostiles:boss._rebels.ships.map(q=>q.key),stormStory:storyPlay(6,"boss"),card:arcStageCard(6,"boss_warning")})');check('Rebel pursuit has four allies plus the player, five opponents and no storm-platform briefing',len(q['friends'])==4 and len(q['hostiles'])==5 and not q['stormStory'] and 'REBEL' in q['card'][0],q)
  for kind in ['cloak','helix','turbo']:
   p.evaluate('kind=>{const I=boss._rebels.h3Intro;I.i=I.rows.findIndex(q=>q.demo===kind);I.t=0;I.shown=0;I.showcase={fx:[],events:new Set(),slot:-1,current:null};}',kind)
   frames(55);snap('rebel-'+kind+'-charge');frames(150);snap('rebel-'+kind+'-release')
   q=p.evaluate('()=>{const D=boss._rebels.h3Intro.showcase.current;return {demo:D?.kind,released:D?.released,cloak:D?.q?.frCloak,ball:P2.draws.jace,turbo:AP10_EXTRA.draws.turbo,fx:boss._rebels.h3Intro.showcase.fx.map(q=>({kind:q.kind,vx:q.vx,vy:q.vy}))};}')
   check(kind+': the authored demo actually forms and releases',q.get('released') is True,q)
   if kind=='helix':check('Jace displays the new centered 32-frame molten ball',q.get('ball',0)>0,q)
   if kind=='turbo':check('Voss displays the onion-registered charge reel',q.get('turbo',0)>0,q)
  p.evaluate('()=>{const R=boss._rebels;R.frIntro.done=true;R.h3Intro.i=R.h3Intro.rows.length;H3.release=false;for(const q of R.ships){q.frCloak=0;q.rfHeading=null;q.x=q.homeX;q.y=q.homeY;q.cd=999;}}');frames(2)
  p.evaluate('()=>{const R=boss._rebels,G=rg4Init(boss);window.p2Gang=G;G.scene=null;G.rescueDone=false;rg4RescueStart(boss,G);const C=G.scene;C.castAt=C.age;C.i=2;C.t=.1;G.cloak=.15;G.shield=1;}');frames(35);snap('decker-personal-shield-wave')
  q=p.evaluate('()=>({scanner:p2Gang.scanner,members:p2Gang.members.map(q=>q.key),draws:P2.draws.shield})');check('Decker casts a visible personal shield on the five-ship formation',len(q['members'])==5 and q['draws']>0,q)
  p.evaluate('()=>{const C=p2Gang.scene;C.scanAt=C.age-2;C.revealAt=null;C.i=4;C.t=.8;p2Gang.cloak=1;}');frames(25);snap('kaia-teal-radar-scan');q=p.evaluate('()=>({scanner:p2Gang.scanner,color:RETINA_TINTS[p2Gang.scanner],draws:RG4.draws.scan})');check('Kaia scans the cloaked formation using her teal retinal art',q['scanner']=='kaia' and q['color']=='#25d9bd' and q['draws']>0,q)
  for who in ['NYX','KAIA','JACE','ROOK','DECKER','VOSS']:
   p.evaluate('who=>{p2Gang.scene=null;H3.release=false;window.p2Who=who;}',who)
   frames(1);p.evaluate('who=>{dlgBox({who,full:"TARGET CONFIRMED. WATCH YOUR SIX.",shown:"TARGET CONFIRMED. WATCH YOUR SIX.",forceShown:true,portraitKey:"rr_portrait_"+who.toLowerCase(),pw:VW*.94,ph:VH*.25,x:VW*.03,y:VH*.55});}',who);snap('radio-'+who.lower())
  scene(6)
  p.evaluate('()=>{GP4.route="left";GP4.routeReady=true;GP4.stage6Only=true;gp4QuickEncounter();storyPlay(6,"boss");}');frames(50);snap('harrier-pursuit')
  q=p.evaluate('()=>({allies:s6Wing.ships.length,briefing:story?.key,card:arcStageCard(6,"boss_warning")})');check('Harrier pursuit is solo and owns the weather briefing',q['allies']==0 and q['briefing']=='P2.S06.HARRIER' and 'HARRIER' in q['card'][0],q)
  p.evaluate('story=null');frames(2400);q=p.evaluate('()=>({frames:window.__bofFrames,boss:boss.kind,threats:PW5.threats.length,warningDraws:PW5.draws,errors:window.__bofDrawError?.toString()})');check('Harrier remains live through native laser closures and elite warnings',q['frames']>2400 and not q.get('errors'),q);snap('harrier-elite-warnings')
  check('No page, console, renderer or asset errors',not errors,errors);br.close()
except Exception as e:errors.append(type(e).__name__+': '+str(e));print(errors[-1],flush=True)
finally:
 stop();r=dict(passed=sum(q['passed'] for q in checks),failed=sum(not q['passed'] for q in checks),checks=checks,errors=errors,shots=shots)
 (OUT/'report.json').write_text(json.dumps(r,indent=2),encoding='utf-8');print(json.dumps(dict(passed=r['passed'],failed=r['failed'],errors=errors)),flush=True)
sys.exit(1 if errors or r['failed'] else 0)
