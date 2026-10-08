"""Drive the shipped main loop at different display rates in three real browsers."""
from pathlib import Path
import sys,json,http.server,time,base64,argparse
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
ap=argparse.ArgumentParser();ap.add_argument('--smoke',action='store_true');ap.add_argument('--out',default='clock');a=ap.parse_args();O=R/'_shots/maneuver_safety_1007'/a.out;O.mkdir(parents=True,exist_ok=True)
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None;port,stop=shoot.serve(str(R));rows=[];errors=[];checks=[]
TEST=r'''c=>{BAL7.setup({stage:1,kind:'damkeeper',diff:c.diff,pilot:c.pilot,level:0,seed:11});boss=null;bossActive=false;subBoss=null;subBossActive=false;stagePlan=[];enemies=[];eBullets=[];groundTargetingReset();player.x=200;player.y=VH-90;player._px=player.x;player._py=player.y;player.invuln=0;stateT=0;combatClockReset();for(const k of keybindFor(1).right)if(!k.startsWith('pad_'))Input.keys[k]=true;const q={kind:'mg',x:650,y:100,vx:0,vy:2,w:4,h:10,t:0};eBullets.push(q);let now=performance.now();last=now;const ticks=BOF_COMBAT_CLOCK.total;for(let i=0;i<c.fps/2;i++){now+=1000/c.fps;loop(now);}return {...c,steps:BOF_COMBAT_CLOCK.total-ticks,x:player.x,y:player.y,bulletY:q.y,stageTimer,stateT,alive:!player.dead};}'''
try:
 with sync_playwright() as pw:
  for browser in ['chromium','firefox','webkit']:
   b=getattr(pw,browser).launch();p=b.new_page();p.set_default_timeout(120000);p.route('**/*',lambda r:r.continue_() if r.request.url.startswith(('http://127.0.0.1:','data:','blob:')) else r.abort());p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None);p.on('response',lambda r:errors.append(f'{r.status} {r.url}') if r.status>=400 else None)
   p.goto(f'http://127.0.0.1:{port}/index.html?quality=performance');p.wait_for_function('()=>window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF);p.add_script_tag(path=str(R/'_BUILD_SOURCE/balance_lab_1007.js'))
   p.evaluate("()=>BAL7.setup({stage:1,kind:'damkeeper',diff:'normal'})");deadline=time.monotonic()+90
   while time.monotonic()<deadline:
    p.evaluate('()=>{stageLoadTick();drawWorld(0);}');p.wait_for_timeout(35)
    if p.evaluate('()=>stageLoadInfo(1).ready'):break
   pilots=p.evaluate('()=>PILOTS.map(p=>p.key)') if browser=='chromium' and not a.smoke else ['juggernaut']
   for diff in ['easy','normal','hard','furious']:
    for pilot in pilots:
     group=[]
     for fps in [30,60,120,144]:
      row=p.evaluate(TEST,dict(diff=diff,pilot=pilot,fps=fps));row['browser']=browser;rows.append(row);group.append(row)
     checks.append({'name':f'{browser} {diff} {pilot} movement and projectile timing','pass':all(r['steps']==30 and abs(r['x']-group[0]['x'])<.001 and abs(r['bulletY']-group[0]['bulletY'])<.001 and r['alive'] for r in group)})
   tap=p.evaluate(r'''()=>{BAL7.setup({stage:1,kind:'damkeeper',diff:'normal'});boss=null;bossActive=false;enemies=[];stagePlan=[];player._rollCool=0;player.roll=null;player._tapL=performance.now()/1000;Input.clearTaps();Input.injectTap(keybindFor(1).left.find(k=>!k.startsWith('pad_')));combatClockReset();let n=performance.now();last=n;loop(n+1000/120);const before=!!player.roll;loop(n+2000/120);return {before,after:!!player.roll};}''')
   checks.append({'name':browser+' 120 Hz input edge survives until tick','pass':not tap['before'] and tap['after'],'evidence':tap})
   (O/(browser+'.png')).write_bytes(base64.b64decode(p.evaluate("()=>cv.toDataURL().split(',')[1]")));b.close();print(browser,'complete',flush=True)
finally:stop()
(O/'report.json').write_text(json.dumps({'rows':rows,'checks':checks,'errors':errors},indent=2));print('rows',len(rows),'checks',len(checks),'failures',[c for c in checks if not c['pass']],'errors',errors);assert all(c['pass'] for c in checks) and not errors
