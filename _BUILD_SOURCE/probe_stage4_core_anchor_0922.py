"""Real Chromium: camera-only scrolling and boss motion must preserve core offsets."""
import sys,json,base64
from pathlib import Path
sys.path.insert(0,str(Path('_BUILD_SOURCE').resolve()))
from shoot import GAME,serve,SETUP,STEP,TRAP_RAF
from playwright.sync_api import sync_playwright
O=Path('_shots/stage4_core_anchor_0922');O.mkdir(exist_ok=True)
port,stop=serve(GAME);r={};errors=[]
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--mute-audio'])
  pg=br.new_context(storage_state={'cookies':[],'origins':[]},viewport={'width':1280,'height':1080}).new_page()
  pg.on('pageerror',lambda e:errors.append(str(e)))
  pg.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  pg.goto(f'http://127.0.0.1:{port}/index.html');pg.wait_for_function('()=>(window.__bofFrames|0)>4');pg.evaluate(TRAP_RAF)
  def ev(s,arg=None):return pg.evaluate(s,arg)
  def cap(n):(O/(n+'.png')).write_bytes(base64.b64decode(ev('()=>cv.toDataURL().split(",")[1]')))
  ev(SETUP,{'state':'PLAY','stage':4,'pilot':'cole','invuln':True})
  ev('''()=>{diffKey='furious';DIFF=DIFFS.furious;run.stage=4;curStage=STAGES[3];
    stagePlan=[];waveIdx=999;_adaptiveSpawnT=999;spawnClock=9999;enemies=[];eBullets=[];pBullets=[];powerups=[];
    subBoss=null;subBossActive=false;spawnBoss('stormsovereign');boss.enter=false;boss.x=worldWidth()/2;
    boss.y=boss._s4war.homeY;boss._drawY=boss.y;boss._noHit=false;player.invuln=1e9;
    stage4ShieldSyncNodes(boss);window.anchorOffsets=boss._s4war.shield.nodes.map(n=>({x:n.x-boss.x,y:n.y-boss.y}));
    for(let i=0;i<16;i++)XART.rdy('s4w_power_node_'+i);
    for(let i=0;i<12;i++){XART.rdy('s4w_boss_energized_'+i);XART.rdy('s4w_lightning_shield_'+i);}
    XART.rdy(SHIPBOSS[boss._ship].key);}''')
  pg.wait_for_function("()=>Array.from({length:16},(_,i)=>XART.rdy('s4w_power_node_'+i)).every(Boolean)&&XART.rdy(SHIPBOSS[boss._ship].key)&&XART.rdy('s4w_lightning_shield_0')&&XART.rdy('s4w_boss_energized_0')")
  r['camera']=[]
  for cx in [0,100,200,0]:
   r['camera'].append(ev('''(cx)=>{camX=cx;scroll+=400;player.x=cx+VW*.65;
     for(let i=0;i<30;i++)stage4ShieldTick(boss,1/60);
     drawWorld(0);return {camera:camX,boss:{x:boss.x,y:boss.y},nodes:boss._s4war.shield.nodes.map(n=>({x:n.x,y:n.y}))};}''',cx))
   cap('camera_'+str(cx))
  r['motion']=ev('''()=>{boss.x+=61;boss.y+=37;boss._drawY=boss.y;stage4ShieldTick(boss,1/60);
    const after=boss._s4war.shield.nodes.map((n,i)=>({dx:n.x-boss.x-anchorOffsets[i].x,dy:n.y-boss.y-anchorOffsets[i].y}));
    drawWorld(0);return after;}''')
  cap('boss_moved')
  r['rearm']=ev('''()=>{const H=boss._s4war.shield;H.active=false;for(const n of H.nodes)n.dead=true;
    stage4ShieldBeginRearm(boss,.75);stage4WarfareTick(boss,.1);
    return H.nodes.map((n,i)=>({dx:n.x-boss.x-anchorOffsets[i].x,dy:n.y-boss.y-anchorOffsets[i].y}));}''')
  r['hitboxes']=ev('''()=>{const H=boss._s4war.shield;H.active=true;H.rearming=false;
    return H.nodes.map(n=>({point:stage4ShieldNodeAt(boss,n.x,n.y,0)===n,
      beam:stage4ShieldBeamNodes(boss,n.x,4,0,VH+500).includes(n)}));}''')
  # Native update ordering: parent movement must not leave components one frame behind.
  r['nativeMaxOffsetError']=ev('''()=>{let max=0;for(let i=0;i<240;i++){
    camX=(i%120)*1.5;player.x=camX+VW*.6;stage4WarfareTick(boss,1/60);
    boss._s4war.shield.nodes.forEach((n,k)=>{max=Math.max(max,Math.abs(n.x-boss.x-anchorOffsets[k].x),Math.abs(n.y-boss.y-anchorOffsets[k].y));});}
    return max;}''')
  ev('()=>{boss._drawY=boss.y;drawWorld(0);}');cap('live_update')
  r['errors']=errors;br.close()
finally:stop()
(O/'results.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
assert not errors,errors
assert all(q['nodes']==r['camera'][0]['nodes'] for q in r['camera'])
assert all(abs(q['dx'])<1e-7 and abs(q['dy'])<1e-7 for q in r['motion']+r['rearm'])
assert all(q['point'] and q['beam'] for q in r['hitboxes'])
assert r['nativeMaxOffsetError']<1e-7
