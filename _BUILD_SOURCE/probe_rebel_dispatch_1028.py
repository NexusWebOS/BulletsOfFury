"""Exercise native personal-book scheduling and actual entry-frame rendering."""
from pathlib import Path
import ast, json
from playwright.sync_api import sync_playwright
import shoot

R = Path(__file__).resolve().parents[1]
O = R / '_shots/stage6_9_refresh_1028/dispatch'
O.mkdir(parents=True, exist_ok=True)
setup = next(ast.literal_eval(n.value) for n in ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text(encoding='utf-8')).body
             if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'SETUP' for t in n.targets))
port, stop = shoot.serve(str(R))
checks, errors, frames = {}, [], []
try:
    with sync_playwright() as pw:
        browser = pw.chromium.launch(channel='msedge', headless=True)
        p = browser.new_page(viewport={'width':1280, 'height':800})
        p.set_default_timeout(180000)
        p.on('pageerror', lambda e: errors.append(str(e)))
        p.on('console', lambda m: errors.append(m.text) if m.type == 'error' or 'draw error' in m.text else None)
        p.goto(f'http://127.0.0.1:{port}/index.html')
        p.wait_for_function('window.__bofFrames>4')
        p.evaluate(shoot.TRAP_RAF)
        p.evaluate('()=>{run.stage=6;stageLoadBegin(6)}')
        p.evaluate(setup, dict(stage=6,kind='rebelsquad',diff='furious',pilot='cole'))
        p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(6)}')
        checks['allFiveEntryRenderersBeforeAttackState'] = p.evaluate('''()=>{
          B._rebels.frIntro={done:true};ctx.save();ctx.setTransform(SS,0,0,SS,0,0);ctx.fillStyle='#07111a';ctx.fillRect(0,0,VW,VH);
          try{for(const q of B._rebels.ships){const prior=q.rg4;delete q.rg4;q.x=70+q.i*85;q.y=130;
            try{fr27RebelDrawShip(q)}finally{if(prior)q.rg4=prior}}
            return true;
          }finally{ctx.restore()}
        }''')
        p.screenshot(path=str(O/'all-five-entry.png'))
        p.evaluate('''()=>{
          window.R=B._rebels;rf28Init(B,R);R.frIntro={done:true};B.enter=B._noHit=false;
          window.G=rg4Init(B);G.age=0;G.scene=null;G.gang=true;G.rescueDone=true;G.releaseAt=0;G.rd21.next=9;
          H3.release=false;H3.ending=null;fb2Talk=fb2Intro=thaw=s6Opening=null;BOFCinematicDirector.cancel();AP10_X.intro=null;story=null;P2M.active=null;
          s6WingInit();s6WingLaunch(4,true);s6Wing.all=true;s6Wing.route='right';for(const q of s6Wing.ships)q.phase='fight';
          player.invuln=999999;player.fireCd=999999;pBullets=[];eBullets=[];RD42.events=[];
          for(const q of R.ships){q.mode='fight';q.warp=0;q.rg4.act=null;q.rg4.cd=1.4+q.i*.4;q.x=camLeftX()+viewW()/2+(q.i-2)*76;q.y=PLAY.y+95+(q.i%2)*45;}
          window.dispatchProbe={ticks:0,seen:{},overlaps:0};SC12.refresh();__bofFit();
        }''')
        for second in range(300):
            sample = p.evaluate('''()=>{
              for(let i=0;i<60;i++){
                rebelSquadTick(B,1/60);dispatchProbe.ticks++;
                for(const q of R.ships)if(q.rg4?.act){const k=q.key+':'+q.rg4.act.kind;dispatchProbe.seen[k]??=dispatchProbe.ticks/60;}
                const active=R.ships.filter(q=>q.rg4?.act&&q.rg4.act.phase!=='recover');
                if(active.length>1)dispatchProbe.overlaps++;
              }
              if(dispatchProbe.ticks%300===0){ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);SC12.refresh();__bofFit();}
              return {...dispatchProbe,events:RD42.events.slice(-8)}
            }''')
            if second in [14,44,89,179,299]:
                frames.append(sample)
                p.screenshot(path=str(O/f'native-{second+1:03}.png'))
            p.wait_for_timeout(5)
        final = p.evaluate('({probe:dispatchProbe,events:RD42.events,hp:R.ships.map(q=>({key:q.key,hp:q.hp,cd:q.rg4.cd,armed:q.rg4.armed}))})')
        seen = final['probe']['seen']
        checks['allFiveNativeBooksStart'] = all(any(k.startswith(pilot+':') for k in seen) for pilot in ['voss','nyx','rook','kaia','jace'])
        checks['rookDashAndSpinReachNativeSchedule'] = 'rook:rk38dash' in seen and 'rook:rk38spin' in seen
        checks['noOverlappingHeavySpecials'] = final['probe']['overlaps'] == 0
        checks['allPilotsRemainNativeLive'] = all(q['hp']>0 for q in final['hp'])
        checks['noRendererOrBrowserErrors'] = not errors
        browser.close()
finally:
    stop()
result = dict(checks=checks,errors=errors,final=final,samples=frames)
(O/'report.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(dict(checks=checks,errors=errors,seen=final['probe']['seen'])))
raise SystemExit(0 if all(checks.values()) else 1)
