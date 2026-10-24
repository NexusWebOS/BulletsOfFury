from pathlib import Path
from playwright.sync_api import sync_playwright
import sys,json
R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');W=Path(__file__).resolve().parent;sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
port,stop=shoot.serve(str(R))
try:
 with sync_playwright()as pw:
  b=pw.chromium.launch(channel='msedge');p=b.new_page();errors=[];p.on('pageerror',lambda e:errors.append(str(e)));p.goto(f'http://127.0.0.1:{port}');p.wait_for_function('window.__bofFrames>5');p.evaluate(shoot.TRAP_RAF)
  result=p.evaluate("""()=>{
 diffKey='furious';const checks={},data={};
 checks.sonicProtected=!enemyOrdnanceCanIntercept({kind:'sg10pressure',_sg10Unit:'sonic',_energyOrdnance:true});
 checks.physicalMissile=enemyOrdnanceCanIntercept({kind:'sg10missile'});
 debugStartFight({stage:2,role:'mini',kind:'magmaward',name:'reaver'},{pilot:'cole'});spawnSubBoss__inner('magmaward');let b=subBoss;b.enter=false;b._noHit=false;er23ReaverBudget(b);data.reaver=b._av3Reaver.parts.map(p=>({id:p.id,hp:p.hp}));
 const hp=b.hp;av3ReaverHit(b,999999,b.x,b.y,'core');checks.coreProtected=b.hp===hp&&!b.dead;
 for(const p of b._av3Reaver.parts.filter(p=>p.id!=='core')){av3ReaverHit(b,999999,b.x,b.y,p.id);}
 checks.allPartsRequired=b._av3Reaver.parts.filter(p=>p.id!=='core').every(p=>p.dead)&&!b.dead;
 data.reaverRemaining=b.hp;checks.budgetMatches=Math.abs(b.hp-av3Part(b,'core').hp)<.001;
 av3ReaverHit(b,999999,b.x,b.y,'core');checks.nativeReaverDeath=b.dead;
 for(const [stage,kind] of [[3,'frostcruiser'],[4,'olivewarden']]){
  debugStartFight({stage,role:'mini',kind,name:kind},{pilot:'cole'});spawnSubBoss__inner(kind);b=subBoss;b.enter=false;b._noHit=false;b.y=b.ty;b._drawY=b.y;
  b._mr27.parts.filter(p=>p.id.startsWith('gun')).forEach(p=>p.dead=true);
  checks[kind+'RearReach']=b._mr27.parts.filter(p=>p.id.startsWith('rocket')).every(p=>{const q=mr27Shape(b,p.id);return mr27At(b,q.x,q.y)===p.id&&mr27At(b,q.x,q.y+q.h*.5+8)!=='core';});
 }
 debugStartFight({stage:5,role:'boss',kind:'chromehammer',name:'chronos'},{pilot:'cole'});spawnBoss('chromehammer');b=boss;const h=b._hammer;h.state='hammer';h.t=0;b._noHit=false;player.invuln=0;b._fb2IntroSeen=true;fb2IntroStart(b);
 checks.introNoLock=!s6OpeningControlsLocked();checks.introHittable=!b._noHit;
 const q={kind:'mg',x:200,y:400,vx:0,vy:0,w:6,h:8,t:0};eBullets.push(q);ht23Say(b,'Test combat continues');updatePlay(1/60);const clock=h.t;for(let i=0;i<5;i++)updatePlay(1/60);
 checks.speechAdvancesCombat=h.t>clock;checks.speechKeepsRounds=eBullets.includes(q);data.chronos={state:h.state,clock:h.t,dialogue:BOFCinematicDirector.current?.id};
 hammerBoomerangRelease(b);const T=h.throw;hammerThrowReflect(b);checks.hammerReverses=T.phase==='hf22_orbit'&&!T.reflected&&T.er23Direction===-1;const x=T.x;hammerBoomerangTick(b,.1);checks.detachedBeforeRecall=T.phase==='hf22_orbit'&&T.x!==x;
 return {checks,data};
 }""")
  result['errors']=errors;(W/'native-contracts.json').write_text(json.dumps(result,indent=2));print(json.dumps(result));b.close()
finally:stop()
