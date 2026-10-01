from pathlib import Path
import sys,json,base64,http.server,hashlib
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];O=R/'_shots/realm_combat_0930';O.mkdir(exist_ok=True,parents=True)
sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot as sh
http.server.SimpleHTTPRequestHandler.log_message=lambda *a,**k:None
SETUP=(Path(__file__).parent/'probe_realm_0930.py').read_text(encoding='utf-8').split('SETUP="""')[1].split('"""')[0]
errors=[];rows=[]
def ck(v,n):rows.append({'ok':bool(v),'name':n});print(('OK ' if v else 'FAIL ')+n,flush=True)
def shot(p,n):
 p.evaluate('()=>{player.invuln=0;drawWorld(0);}');(O/(n+'.png')).write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')))
port,stop=sh.serve(str(R))
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);p=b.new_page(viewport={'width':1000,'height':1000});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:500]) if m.type=='error' or 'draw error' in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);p.wait_for_function('()=>window.__bofFrames>3',timeout=120000);p.evaluate(sh.TRAP_RAF);p.evaluate(SETUP)
  p.wait_for_function("()=>Object.keys(REALM30_ART).every(k=>XART.rdy('r30_'+k))",timeout=60000)
  p.evaluate('()=>{boss._r30.mode="fight";boss.enter=false;boss._r30.cd=999;}')
  for dk in ['normal','hard','furious','insanity']:
   result=p.evaluate("""dk=>{diffKey=dk;DIFF=DIFFS[dk];r30Form(boss,2);boss.enter=false;const S=boss._r30;S.mode='fight';S.cd=999;
    const v=r30Parts(boss).find(v=>v.p.id==='core'),hp=boss.hp;_lastHitX=v.x;_lastHitY=v.y;const hit=bossHitTest(v.x,v.y);hitBoss(7);
    const damage=boss.hp<hp;S.shield=S.shieldMax=10;bossHitTest(v.x,v.y);const before=boss.hp;hitBoss(3);const shield=S.shield<10&&boss.hp===before;modularHit(100);
    const layers=boss.maxhp/S.base;return {hit,damage,shield,broken:S.shield===0,layers};}""",dk)
   ck(all(result[k] for k in ['hit','damage','shield','broken']) and result['layers']==4,dk+' real boss-hit routing, shield and four health layers');print(result,flush=True)
  p.evaluate('()=>{boss._r30.cd=999;boss._r30.seq=2;r30Attack(boss);}')
  for i in range(5):
   p.evaluate('()=>{for(let i=0;i<90;i++){player.invuln=100;updatePlay(1/60);if(i%15===0)drawWorld(1/60);}}');shot(p,'wall_live_'+str(i))
  r=p.evaluate('()=>({walls:enemies.filter(e=>e._r30Wall&&!e.dead).length,valid:enemies.every(e=>Number.isFinite(e.x)&&Number.isFinite(e.y)),state,mode:boss._r30.mode,t:boss._r30.clock})');print(r,flush=True);ck(r['valid'] and r['state']=='play','native update loop keeps wall and boss coordinates valid')
  # Real lock candidates and their registered impact closures, no direct HP fixture edits.
  r=p.evaluate("""()=>{r30Form(boss,0);boss._r30.mode='fight';boss.enter=false;boss._r30.shield=0;const ts=retinaBossTargets(boss),hp=boss.hp;ts[0]._retinaHit(9);return {count:ts.length,damage:boss.hp<hp,finite:ts.every(t=>Number.isFinite(t.x)&&Number.isFinite(t.y))};}""")
  ck(r['count']==3 and r['damage'] and r['finite'],'Retina locks three moving modules and missiles damage them')
  for target in ['module','shield','wall']:
   r=p.evaluate("""kind=>{r30Form(boss,0);boss._r30.mode='fight';boss._r30.cd=999;boss.enter=false;boss.flash=0;enemies=[];eBullets=[];pBullets=[];run.bombs=20;run.missileTier='standard';run.weapon=0;run.forge={};run.infusion=null;special=null;
    player.x=boss.x;player.y=VH-110;player.invuln=100;
    if(kind==='shield')boss._r30.shield=boss._r30.shieldMax=100;
    if(kind==='wall')r30Wall(boss,'datawall');
    const t=kind==='wall'?enemies.find(e=>e._r30Wall):retinaBossTargets(boss)[0],hp=kind==='shield'?boss._r30.shield:kind==='wall'?t.hp:boss.hp;
    const valid=retinaTargetValid(t),fired=useBomb(t),trail=[];for(let i=0;i<160;i++){player.invuln=100;updatePlay(1/60);if(i<4||i%20===0){const q=pBullets.find(q=>q.kind==='gmiss');trail.push({i,x:t.x,y:t.y,dead:t.dead,valid:retinaTargetValid(t),hp:t.hp,q:q?{x:q.x,y:q.y,dead:q.dead,target:q.tgt===t}:null});}}
    const after=kind==='shield'?boss._r30.shield:kind==='wall'?t.hp:boss.hp;return {fired,before:hp,after,damage:after<hp,valid,trail:kind==='wall'?trail:[]};}""",target)
   ck(r['fired'] and r['damage'],'launched homing missile reaches '+target+' through native updatePlay');print(r,flush=True)
  for w in [0,3,5,7]:
   r=p.evaluate("""w=>{r30Form(boss,0);boss._r30.mode='fight';boss._r30.cd=999;boss.enter=false;enemies=[];eBullets=[];pBullets=[];run.weapon=w;run.wlevel=3;run.forge={};run.infusion=null;special=null;player.x=boss.x;player.y=VH-120;const hp=boss.hp;
    for(let i=0;i<120;i++){if(i%6===0)pShoot();player.invuln=100;updatePlay(1/60);}return{before:hp,after:boss.hp,damage:boss.hp<hp};}""",w)
   ck(r['damage'],'native primary weapon '+str(w)+' damages the modular host');print(r,flush=True)
  p.evaluate('()=>{r30Form(boss,2);boss._r30.mode="fight";boss.enter=false;boss._r30.shield=boss._r30.shieldMax=100;}');shot(p,'fitted_shield')
  p.evaluate('()=>{boss._lastPart={id:"shield"};modularHit(60);}');shot(p,'cracked_shield')
  p.evaluate('()=>modularHit(60)');shot(p,'broken_shield')
  p.evaluate('()=>{enemies=[];r30Wall(boss,"binarywall");boss._r30.shield=0;}');shot(p,'intact_wall')
  p.evaluate('()=>{const e=enemies.find(e=>e._r30Wall);hitEnemy(e,e.maxhp*.6);}');shot(p,'cracked_wall')
  p.evaluate('()=>{const e=enemies.find(e=>e._r30Wall);hitEnemy(e,e.maxhp);}');shot(p,'broken_wall')
  # An attack runs normally while the actual updatePlay path advances bullets and controls.
  p.evaluate('()=>{enemies=[];eBullets=[];boss._r30.seq=6;r30Attack(boss);}')
  for i in range(8):p.evaluate('()=>{for(let i=0;i<60;i++){player.invuln=100;updatePlay(1/60);drawWorld(1/60);}}')
  ck(p.evaluate('()=>eBullets.every(q=>Number.isFinite(q.x)&&Number.isFinite(q.y))'),'native code-rain projectiles remain finite')
  r=p.evaluate('()=>({bytes:ROT5.bytes,budget:ROT5.budget,draws:ROT5.draws,fallbacks:ROT5.fallbacks})');print(r,flush=True);ck(r['bytes']<=r['budget'],'rotation memory stays within 48 MiB budget')
  # Normal steering samples for every pilot; evasion retains the original authored reel.
  p.evaluate('()=>{run.stage=1;run.spaceMode=false;gravityMode=null;boss=null;bossActive=false;player.dead=false;player.roll=0;player.somer=0;}')
  r=p.evaluate("""()=>PILOTS.map(p=>{run.pilot=p.key;return {pilot:p.key,neutral:_shipFrameKey(p.key)==='ship_'+p.key,left:rot5Index(-Math.PI/12),right:rot5Index(Math.PI/12)};})""")
  ck(all(q['neutral'] and q['left']==69 and q['right']==3 for q in r),'all nine pilots steer with neutral hull and matching clockwise headings')
  ck(not errors,'no native page or draw errors');print('ERRORS',errors[:10],flush=True);b.close()
finally:stop();(O/'verification.json').write_text(json.dumps({'checks':rows,'errors':errors},indent=2))
sys.exit(0 if rows and all(v['ok'] for v in rows) and not errors else 1)
