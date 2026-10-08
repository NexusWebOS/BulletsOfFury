"""Commit-cue reaction and escape-margin audit with real player movement/collision."""
from pathlib import Path
import sys,json,argparse,http.server,base64
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
a=argparse.ArgumentParser();a.add_argument('--out',default='warning_before');a=a.parse_args();O=R/'_shots/maneuver_safety_1007'/a.out;O.mkdir(parents=True,exist_ok=True)
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None;port,stop=shoot.serve(str(R));errors=[];rows=[]
TEST=r'''c=>{BAL7.setup({stage:1,kind:'damkeeper',diff:c.diff,pilot:c.pilot||'juggernaut',level:0,seed:7});boss=null;bossActive=false;subBoss=null;subBossActive=false;enemies=[];eBullets=[];pBullets=[];stagePlan=[];stageTimer=0;groundTargetingReset();player.x=worldWidth()/2;player.y=VH-105;player.dead=false;player.invuln=0;run.shield=0;player.roll=player.somer=null;const g=groundTargetingSpawn({kind:c.kind,track:true,...(c.warn?{warn:c.warn}:{}),...(c.radius?{radius:c.radius}:{}),x:player.x,y:player.y});let firstDamage=null,minMargin=999,moveAt=null;const dt=1/(c.fps||60);for(let i=0;i<240&&!g.dead&&!player.dead;i++){for(const k of Object.keys(Input.keys))Input.keys[k]=false;Input.clearTaps?.();if(!c.stationary&&g.t>=g.warn*.5+c.reaction){for(const k of keybindFor(1).left)if(!k.startsWith('pad_'))Input.keys[k]=true;if(moveAt==null)moveAt=g.t;}updatePlay(dt);if(g.t>=g.warn+.08){const gap=Math.abs(player.x-g.x)-g.radius;minMargin=Math.min(minMargin,gap);if(firstDamage==null)firstDamage=g.t;}}ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);return {...c,survived:!player.dead,margin:minMargin,moveAt,firstDamage,warn:g.warn,trackFor:g.trackFor,playerSpeed:playerBaseSpeed()*60};}'''
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch();p=b.new_page();p.route('**/*',lambda q:q.continue_() if q.request.url.startswith(('http://127.0.0.1:','data:','blob:')) else q.abort());p.on('pageerror',lambda e:errors.append(str(e)));p.goto(f'http://127.0.0.1:{port}/index.html?quality=performance');p.wait_for_function('()=>window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF);p.add_script_tag(path=str(R/'_BUILD_SOURCE/balance_lab_1007.js'))
  for diff in ['easy','normal','hard','furious']:
   for kind in ['missile','lava','glacial','lightning','water']:
    for reaction in [.20,.30,.40]:rows.append(p.evaluate(TEST,{'diff':diff,'kind':kind,'reaction':reaction}))
    rows.append(p.evaluate(TEST,{'diff':diff,'kind':kind,'reaction':.30,'stationary':True}))
  b.close()
finally:stop()
(O/'report.json').write_text(json.dumps({'rows':rows,'errors':errors},indent=2));print(json.dumps({'cases':len(rows),'movingDeaths':[r for r in rows if not r.get('stationary') and not r['survived']],'tightMargins':[r for r in rows if not r.get('stationary') and r['survived'] and r['margin']<12],'controlsHit':sum(not r['survived'] for r in rows if r.get('stationary')),'errors':errors}));assert not errors
