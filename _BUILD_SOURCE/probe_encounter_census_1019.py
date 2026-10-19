"""Equal-window native campaign encounters; no player fire, live helpers/AI."""
from pathlib import Path
import argparse,ast,http.server,json,sys
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/overnight_combat_1019/encounters';O.mkdir(parents=True,exist_ok=True)
ap=argparse.ArgumentParser();ap.add_argument('--diffs',default='normal,hard,furious');ap.add_argument('--stages',default='1,2,3,4,5,6,7,8,9');ap.add_argument('--seconds',type=int,default=60);ap.add_argument('--kinds',default='');ap.add_argument('--label',default='');ap.add_argument('--seed',type=int);a=ap.parse_args()
if a.label:O=O/a.label;O.mkdir(exist_ok=True)
SETUP=next(ast.literal_eval(n.value) for n in ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text()).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SETUP' for t in n.targets))
roster={1:[('razorback',True),('damkeeper',False)],2:[('magmaward',True),('infernoreaver',False)],3:[('frostcruiser',True),('cryospear',False)],4:[('olivewarden',True),('stormsovereign',False)],5:[('siegebomber',True),('chromehammer',False)],6:[('siegefortress17',True),('warhive',False),('rebelsquad',False)],7:[('dualscoopdredger',True),('sludgeemperor',False)],8:[('heralddeath',True),('vileexistence',False)],9:[('voidhorizon',True),('tidalfusion',False)]}
rows=[];errors=[];port,stop=shoot.serve(str(R));http.server.ThreadingHTTPServer.request_queue_size=128
def save():
 (O/('report-'+a.diffs.replace(',','-')+'.json')).write_text(json.dumps(dict(seed=a.seed,method=f'Real Chromium, {a.seconds} simulated seconds after each native encounter is placed at its own entry anchor. Actual controllers/helpers, no player fire, visible protected pilot follows the same route. Includes native intros/armor charge. Initial-phase census; campaign films separately cover damage-driven phases. Beam frames are activity duration, not unique attack counts.',rows=rows,errors=errors),indent=2)+'\n',encoding='utf-8')
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=br.new_page(viewport=dict(width=1600,height=1000));p.set_default_timeout(180000)
  p.add_init_script("Object.defineProperty(navigator,'getGamepads',{value:()=>[]});")
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:700]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append(str(r.status)+' '+r.url.split('?')[0]) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
  # Read the existing native phase summary, without driving its pilot bot.
  phaseSource=(R/'_shots/playtest_full_1018/pilot.js').read_text();start=phaseSource.index('function full18Phase');end=phaseSource.index('\nfunction ',start+12)
  p.evaluate('window.full18Phase='+phaseSource[start:end])
  p.evaluate('''()=>{window.EC19={};const warning=combatWarningTick,draw=ctx.drawImage;combatWarningTick=function(owner,key,t,warm){if(EC19.live){EC19.firstWarning??=EC19.time;const tag=String(key),prior=EC19.warningCalls.find(q=>q.key===tag);if(prior)prior.warm=warm;else if(EC19.warningCalls.length<120)EC19.warningCalls.push({key:tag,time:EC19.time,warm});}return warning.apply(this,arguments);};
   window.ec19Step=n=>{for(let i=0;i<n;i++){EC19.time+=1/60;const t=EC19.time;player.invuln=1e9;Input.keys={};Input.mouse.down=false;
    if(!player._ra7Caught&&!player._ra7Thrown){player.x=camLeftX()+viewW()/2+Math.sin(t*.7)*Math.min(110,viewW()*.23);player.y=VH-105+Math.sin(t*.9)*25;}
    updatePlay(1/60);const phase=full18Phase(B)||B._er26?.mode||B.phase||'active';if(phase!==EC19.lastPhase){EC19.phases.push({time:t,phase});EC19.lastPhase=phase;}
    for(const b of eBullets)if(!EC19.seen.has(b)){EC19.seen.add(b);EC19.shots++;EC19.firstProjectile??=t;EC19.kinds[b.kind]=(EC19.kinds[b.kind]||0)+1;const speed=Math.hypot(b.vx||0,b.vy||0);if(Number.isFinite(speed))EC19.maxSpeed=Math.max(EC19.maxSpeed,speed);}
    const F=B._fz,donor=j3State(B)?.gp4Donors?.[B._r30?.v18?.form]?.p,DF=donor?._fz;
    const beams=[...orbBeams,...S81003.beams,...(typeof LL18==='undefined'?[]:LL18.beams),...(F?.beams||[]),...(DF?.beams||[]),...(B._r30?.v18?.beams||[])].filter(q=>!q.dead);
    if(beams.length){EC19.firstBeam??=t;EC19.beamFrames++;EC19.maxBeams=Math.max(EC19.maxBeams,beams.length);}
    for(const q of groundTargetingFx)if(!EC19.seenGround.has(q)){EC19.seenGround.add(q);EC19.ground++;EC19.firstGround??=t;}
    EC19.peakProjectiles=Math.max(EC19.peakProjectiles,eBullets.filter(b=>!b.dead).length);EC19.peakHelpers=Math.max(EC19.peakHelpers,enemies.filter(e=>!e.dead).length);
    const visible=B.x>=camLeftX()&&B.x<=camRightX()&&(B._drawY??B.y)>=PLAY.y&&(B._drawY??B.y)<=VH;if(visible){EC19.firstCenterVisible??=t;EC19.visibleFrames++;}
    if(i%12===0)drawWorld(1/60);
    if(!Number.isFinite(B.x)||!Number.isFinite(B.y)||!Number.isFinite(B.hp)){EC19.nonFinite=true;return;}
   }};
   window.ec19Result=()=>({...EC19,seen:undefined,seenGround:undefined,final:{state,hp:B.hp,max:B.maxhp,dead:B.dead,phase:full18Phase(B),x:B.x,y:B.y},runtime:{shoulder:typeof SG19!=='undefined',stealth:typeof SK19!=='undefined',rebel:typeof RBAL19!=='undefined',herald:typeof HD19!=='undefined',hammer:typeof HM19!=='undefined'}}); }''')
  for stage in map(int,a.stages.split(',')):
   for kind,mini in roster[stage]:
    if a.kinds and kind not in a.kinds.split(','):continue
    for diff in a.diffs.split(','):
     print('RUN',stage,kind,diff,flush=True)
     if a.seed is not None:p.evaluate('s=>{Math.random=()=>{s=(Math.imul(s,1664525)+1013904223)>>>0;return s/4294967296;};}',a.seed)
     p.evaluate(SETUP,dict(stage=stage,kind=kind,mini=mini,diff=diff,pilot='cole'))
     p.wait_for_function('()=>{stageLoadTick();if(run.stage===8)v18Warm();return stageLoadReady(run.stage)&&bmfReady("game")}',polling=50)
     p.evaluate('''()=>{VP12.next=CP12.next=EP13.next=SEWER17.next=HM17.next=TARGET17.nextTank=999999;spawnClock=999999;stagePlan=[];subBossTriggered=aminiTriggered=true;subBossDone=true;warnT=0;warnKind=null;bossWarned=false;bossDefeated=false;stageTimer=0;BOFCinematicDirector.cancel();AP10_X.intro=null;story=fb2Talk=fb2Intro=thaw=s6Opening=null;H3.release=false;H3.ending=null;P2M.active=null;run.shield=0;run.sonicT=run.dkT=0;special=thunderStorm=null;run._megaShield=false;run.spaceMode=[5,9].includes(run.stage);player.fireCd=999999;powerups=[];eBullets=[];pBullets=[];
      EC19={live:true,time:0,firstWarning:null,firstProjectile:null,firstBeam:null,firstGround:null,firstCenterVisible:null,warningCalls:[],phases:[],shots:0,kinds:{},maxSpeed:0,peakProjectiles:0,peakHelpers:0,ground:0,beamFrames:0,maxBeams:0,visibleFrames:0,seen:new WeakSet(),seenGround:new WeakSet()};SC12.refresh();__bofFit();}''')
     for sec in range(a.seconds):
      for batch in range(5):p.evaluate('ec19Step(12)');p.wait_for_timeout(5)
      if sec in [4,14,a.seconds-1]:
       p.evaluate('shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);SC12.refresh();__bofFit();');p.screenshot(path=str(O/f'{stage}-{kind}-{diff}-{sec+1:02}.jpg'),type='jpeg',quality=80)
      if p.evaluate('!!EC19.nonFinite'):break
     metrics=p.evaluate('ec19Result()');rows.append(dict(stage=stage,kind=kind,role='mini' if mini else 'boss',difficulty=diff,metrics=metrics));save()
     print('END',stage,kind,diff,json.dumps({k:metrics.get(k) for k in ['firstWarning','firstProjectile','firstBeam','shots','beamFrames','ground','peakProjectiles','peakHelpers','nonFinite']}),flush=True)
  br.close()
finally:stop();save()
print(json.dumps(dict(cases=len(rows),errors=errors)),flush=True);sys.exit(bool(errors) or any(r['metrics'].get('nonFinite') for r in rows))
