"""Native commit-cue tests; delayed ordinary movement, no evasion or shields."""
from pathlib import Path
import argparse,base64,json,sys,http.server,time
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
ap=argparse.ArgumentParser();ap.add_argument('--candidate');ap.add_argument('--out',default='warning_after');a=ap.parse_args()
O=R/'_shots/maneuver_safety_1007'/a.out;O.mkdir(parents=True,exist_ok=True)
http.server.SimpleHTTPRequestHandler.log_message=lambda *args:None
port,stop=shoot.serve(str(R));rows=[];errors=[]
TEST=r'''c=>{BAL7.setup({stage:c.stage||4,kind:'damkeeper',diff:c.diff,pilot:'juggernaut',level:0,seed:7});boss=null;bossActive=false;subBoss=null;subBossActive=false;enemies=[];eBullets=[];pBullets=[];stagePlan=[];stageTimer=0;groundTargetingReset();player.x=worldWidth()*c.position;player.y=VH-105;player.dead=false;player.invuln=0;run.shield=0;player.roll=player.somer=null;const g=groundTargetingSpawn({kind:c.kind,track:true,x:player.x,y:player.y});let cue=null,moveAt=null,minMargin=999,lockedX=null,movedAfterCue=false;const dt=1/c.fps;for(let i=0;i<Math.ceil((g.warn+g.active+1)*c.fps)&&!g.dead&&!player.dead;i++){for(const k of Object.keys(Input.keys))Input.keys[k]=false;Input.clearTaps?.();if(cue===null&&groundTargetingPhase(g)>=.5){cue=g.t;lockedX=g.x;}if(cue!==null&&Math.abs(g.x-lockedX)>.001)movedAfterCue=true;if(!c.stationary&&cue!==null&&g.t>=cue+c.reaction){for(const k of keybindFor(1)[c.position>.5?'left':'right'])if(!k.startsWith('pad_'))Input.keys[k]=true;if(moveAt===null)moveAt=g.t;}combatFrame(dt);if(g.t>=g.warn+.08)minMargin=Math.min(minMargin,Math.abs(player.x-g.x)-g.radius);}return {...c,survived:!player.dead,minMargin,cue,moveAt,movedAfterCue,warn:g.warn,trackFor:g.trackFor,budget:g._safetyBudget};}'''
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(args=['--mute-audio']);p=b.new_page();p.route('**/*',lambda r:r.continue_() if r.request.url.startswith(('http://127.0.0.1:','data:','blob:')) else r.abort());p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None);p.on('response',lambda r:errors.append(f'{r.status} {r.url}') if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html?quality=performance');p.wait_for_function('()=>window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF);p.add_script_tag(path=str(R/'_BUILD_SOURCE/balance_lab_1007.js'))
  if a.candidate:p.add_script_tag(path=a.candidate)
  for diff,reaction in [('easy',.45),('normal',.38),('hard',.32),('furious',.28)]:
   p.evaluate("d=>BAL7.setup({stage:4,kind:'damkeeper',diff:d})",diff)
   deadline=time.monotonic()+90
   while time.monotonic()<deadline:
    p.evaluate('()=>{stageLoadTick();drawWorld(0);}');p.wait_for_timeout(35)
    if p.evaluate('()=>stageLoadInfo(run.stage).ready'):break
   for kind in ['missile','lava','glacial','lightning','water']:
    for fps in [30,60,120]:
     for position in [.15,.5,.85]:rows.append(p.evaluate(TEST,dict(diff=diff,kind=kind,fps=fps,position=position,reaction=reaction)))
    rows.append(p.evaluate(TEST,dict(diff=diff,kind=kind,fps=60,position=.5,reaction=reaction,stationary=True)))
   print(diff,'complete',flush=True)
  # Visible native states from the actual shared renderer.
  p.evaluate("()=>{BAL7.setup({stage:4,kind:'stormsovereign',diff:'normal'});boss=null;bossActive=false;enemies=[];stagePlan=[];groundTargetingReset();window.G=groundTargetingSpawn({kind:'lightning',x:player.x,y:player.y});}")
  for name,ratio in [('tracking',.5),('committed',1.1),('red',2)]:
   p.evaluate("v=>{G.t=v==='tracking'?G._safetyCommit*.5:v==='committed'?G._safetyCommit+(G.warn-G._safetyCommit)*.25:G.warn-.01;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}",name)
   (O/(name+'.png')).write_bytes(base64.b64decode(p.evaluate("()=>cv.toDataURL().split(',')[1]")))
  b.close()
finally:stop()
report={'rows':rows,'errors':errors,'movingPass':sum(r['survived'] for r in rows if not r.get('stationary')),'movingTotal':sum(not r.get('stationary',False) for r in rows),'controlsHit':sum(not r['survived'] for r in rows if r.get('stationary')),'minMargin':min(r['minMargin'] for r in rows if not r.get('stationary'))}
(O/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='rows'}));assert not errors
assert report['movingPass']==report['movingTotal'] and report['controlsHit']==20
assert not any(r['movedAfterCue'] for r in rows)
