"""Natural-frame Campaign/Arcade encounter parity and co-op pressure audit."""
import json, sys, hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[2]
O=R/'_shots/arcade_natural_parity_0915';O.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
from playwright.sync_api import sync_playwright
checks=[];errors=[]
def ok(v,name,detail=None):
    checks.append({'name':name,'ok':bool(v),'detail':detail})
    print(('ok  ' if v else 'FAIL ')+name+((' — '+str(detail)) if detail else ''),flush=True)
port,stop=shoot.serve(str(R))
with sync_playwright() as p:
    b=p.chromium.launch(args=['--no-sandbox','--mute-audio','--autoplay-policy=no-user-gesture-required'])
    pg=b.new_page(viewport={'width':1100,'height':1000})
    pg.on('pageerror',lambda e:errors.append('page '+str(e)))
    pg.on('console',lambda m:errors.append('console '+m.text) if m.type=='error' else None)
    pg.goto('http://127.0.0.1:%d/index.html'%port,wait_until='load',timeout=120000)
    pg.wait_for_function('()=>(window.__bofFrames|0)>4',timeout=120000)
    pg.evaluate(shoot.TRAP_RAF)
    pg.evaluate("""()=>{
      __auto=function(){};debugFight=null;_coleScene=0;pilotIndex=PILOTS.findIndex(p=>p.key==='cole');
      window.__parityRun=function(mode,stage,coop){
        const encounterSeed=(0x51f15e^(stage*0x9e3779b9))>>>0;
        let seed=encounterSeed;
        const priorRandom=Math.random;
        Math.random=function(){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed/4294967296;};
        try{
          coopOn=!!coop;run.mode=mode;diffKey='normal';DIFF=difficultyForRun(mode,'normal');
          run.lives=99;run2.lives=99;run.bombs=20;run2.bombs=20;run.contUsed=0;
          beginStage(stage);setState(GS.PLAY);storySkip();player.invuln=1e9;player2.invuln=1e9;
          // Campaign starts its entry radio inside beginStage; Arcade skips it there. Presentation
          // may consume random values, so begin the encounter comparison from the same PRNG state.
          seed=encounterSeed;
          _adaptiveSpawnT=1e9; // compare the authored encounter; the adaptive lane is shared and separately invariant.
          const trace=[],seenBoss=[],seenMini=[];
          let frames=0,lastWave=-1;
          for(;frames<4200;frames++){
            updatePlay(.10);drawWorld(.10);
            for(const e of enemies){
              if(e.__paritySeen)continue;e.__paritySeen=1;
              trace.push([e.kind||'',e.type||'',e.pattern||'',e.art||'',e.behav||'',!!e._dr]);
            }
            enemies.length=0;eBullets.length=0;pBullets.length=0;powerups.length=0;
            if(subBossActive&&subBoss&&!subBoss.__parityDone){
              seenMini.push([subBoss.kind||'',subBoss.name||'',!!subBoss._ship,!!subBoss._mech,!!subBoss.modular]);
              subBoss.__parityDone=1;subBoss.dead=true;subBossActive=false;subBossDone=true;warnT=0;warnKind=null;
            }
            if(bossActive&&boss&&!boss.__parityDone){
              seenBoss.push([boss.kind||'',boss.name||'',!!boss._ship,!!boss._mech,!!boss.modular,!!boss._hammer,!!boss._s7warden]);
              boss.__parityDone=1;break;
            }
            if(state!==GS.PLAY)setState(GS.PLAY);
          }
          return {stage,mode,coop,frames,waveIdx,waves:stagePlan.length,trace,mini:seenMini,boss:seenBoss,
                  stageTimer:+stageTimer.toFixed(2),bossWarned,subBossDone};
        }finally{Math.random=priorRandom;coopOn=false;}
      };
    }""")
    rows=[]
    for stage in range(1,10):
        pg.evaluate('s=>warmStage(s)',stage);pg.wait_for_timeout(500)
        campaign=pg.evaluate('s=>__parityRun("campaign",s,false)',stage)
        arcade=pg.evaluate('s=>__parityRun("arcade",s,false)',stage)
        rows.append({'stage':stage,'campaign':campaign,'arcade':arcade})
        # Stage 5's asteroid field intentionally substitutes random small comets for some rock
        # slots. Asset decode changes presentation RNG timing, so compare its scheduled roster
        # exactly while requiring the environmental comet family in both modes.
        ct=[x for x in campaign['trace'] if not (stage==5 and x[1]=='cometsm')]
        at=[x for x in arcade['trace'] if not (stage==5 and x[1]=='cometsm')]
        ccom=sum(1 for x in campaign['trace'] if x[1]=='cometsm')
        acom=sum(1 for x in arcade['trace'] if x[1]=='cometsm')
        same=ct==at and (stage!=5 or (ccom>0 and acom>0))
        detail=('%d authored + %d/%d random comets / %d waves'%(len(at),ccom,acom,arcade['waves'])
                if stage==5 else '%d units / %d waves'%(len(at),arcade['waves']))
        ok(same,'Stage %d authored enemy arrivals match'%stage,detail)
        ok(campaign['mini']==arcade['mini'],'Stage %d miniboss route matches'%stage,str(arcade['mini']))
        ok(campaign['boss']==arcade['boss'] and len(arcade['boss'])==1,'Stage %d boss route matches and arrives'%stage,str(arcade['boss']))
        ok(campaign['waveIdx']==campaign['waves']==arcade['waveIdx']==arcade['waves'],'Stage %d consumes every authored wave before boss'%stage,
           '%d/%d'%(arcade['waveIdx'],arcade['waves']))
    # Co-op uses the same authored families. Every other scheduled wave is repeated by design.
    coop_rows=[]
    for stage in range(1,10):
        solo=rows[stage-1]['arcade'];co=pg.evaluate('s=>__parityRun("arcade",s,true)',stage);coop_rows.append(co)
        sf={tuple(x) for x in solo['trace']};cf={tuple(x) for x in co['trace']}
        ok(sf==cf,'Stage %d co-op duplicates pressure without inventing enemy families'%stage,
           '%d solo / %d co-op'%(len(solo['trace']),len(co['trace'])))
        ok(co['mini']==solo['mini'] and co['boss']==solo['boss'],'Stage %d co-op keeps the same miniboss and boss identities'%stage)
        ok(co['waveIdx']==co['waves'],'Stage %d co-op consumes every authored wave'%stage,'%d/%d'%(co['waveIdx'],co['waves']))
    loop_error=pg.evaluate('()=>window.__err||null')
    ok(not errors and not loop_error,'zero page, console and controlled-loop errors')
    b.close()
stop()
result={'runtimeSha256':hashlib.sha256((R/'assets/game.js').read_bytes()).hexdigest(),'checks':checks,'errors':errors,'loopError':loop_error,'stages':rows,'coop':coop_rows}
(O/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
n=sum(c['ok'] for c in checks);print('%d passed / %d failed'%(n,len(checks)-n),flush=True)
if n!=len(checks):raise SystemExit(1)
