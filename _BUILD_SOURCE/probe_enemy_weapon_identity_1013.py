from pathlib import Path
import sys,json
from playwright.sync_api import sync_playwright
R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
O=R/'_shots/enemy_weapon_identity_1013';O.mkdir(parents=True,exist_ok=True)
rows=[];native=[];interrupts=[];errors=[];port,stop=shoot.serve(str(R))
PREP=r'''c=>{diffKey=c.d;DIFF=DIFFS[c.d];story=null;debugFight=null;waveIdx=999;spawnClock=9999;subBossTriggered=true;subBossDone=true;subBossActive=false;bossActive=false;warnT=0;if(wfx)wfx.fseq=null;stageTimer=1;VP12.next=9999;CP12.next=9999;enemies=[];eBullets=[];pBullets=[];particles=[];wm26Releases=[];EP13.owner=null;EP13.next=9999;EP13.clock=10;EP13.events=[];player.dead=false;player.invuln=1e9;player.x=camLeftX()+VW*.5;player.y=PLAY.y+PLAY.h*.83;for(const k in Input.keys)delete Input.keys[k];window.unit=spawnEnemy(c.type,camLeftX()+VW*.5,PLAY.y+PLAY.h*.22,{});const e=unit;e.hp=e.maxhp=50000;e._ai27={seen:1,visible:true,flinch:0};e._stagger=0;e._s8Act=null;e._s9Act=null;e._s8Roll=null;if(e._mm1003)e._mm1003.phase='rest';window.identityShots=[];window.identityMuzzles={};window.identityShardDraws=0;window.identityBeamFrames=0;window.identityWrongMuzzles=[];}'''
INSTRUMENT=r'''()=>{const shot=eShootT;eShootT=function(x,y,a,s,kind,o){const b=shot.apply(this,arguments),e=o?.owner||ep13NativeOwner;if(e===window.unit&&b&&!b.dead){let gun=null,error=null;if(e._mm1003){for(const p of e._mm1003.parts){if(p.kind!=='gun'||p.dead)continue;const m=mm1003Pose(e,p),d=Math.hypot(x-m.mx,y-m.my);if(error===null||d<error){error=d;gun=p.id;}}}identityShots.push({kind:b.kind,s9a:b._s9a||null,x,y,a,gun,mountError:error,boss:!!b._boss});}return b;};const draw=wm26Draw;wm26Draw=function(g,f,...args){const r=draw.call(this,g,f,...args);if(r)identityMuzzles[f]=(identityMuzzles[f]||0)+1;return r;};const emit=wm26Emit;wm26Emit=function(e,x,y,a,f,...args){if(e===window.unit&&e._s9void==='s9beacon'&&f!=='crystal')identityWrongMuzzles.push(f);return emit.call(this,e,x,y,a,f,...args);};const shards=s9aProjectileDraw;s9aProjectileDraw=function(b){const r=shards.apply(this,arguments);if(r&&b._ep13Crystal)identityShardDraws++;return r;};const play=updatePlay;updatePlay=function(dt){const r=play.apply(this,arguments);if(window.unit&&ep13Beam(unit))identityBeamFrames++;return r;};}'''
try:
 with sync_playwright() as pw:
  for browser_name in ['msedge','chrome','firefox']:
   browser=pw.firefox.launch() if browser_name=='firefox' else pw.chromium.launch(channel=browser_name,args=['--mute-audio'])
   p=browser.new_page(viewport={'width':1440,'height':1000});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:print(m.text,flush=True) if m.text.startswith('WRONG') else None);p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);p.wait_for_function('window.__bofFrames>4',timeout=90000);p.evaluate(shoot.TRAP_RAF);p.evaluate('()=>{window.identityShots=[];window.identityMuzzles={};window.identityShardDraws=0;window.identityBeamFrames=0;window.identityWrongMuzzles=[];}');p.evaluate(INSTRUMENT)
   for stage,typ,kind in [(7,'mm1003_riflelocust','rifle'),(9,'s9beacon','shards')]:
    p.evaluate(shoot.SETUP,{'state':'PLAY','stage':stage,'pilot':'cole','invuln':True});p.wait_for_function('(n)=>{stageLoadTick();ep13Warm();return stageLoadReady(n)&&ep13ReadyArt()&&XART.rdy("warpprismshard_0")&&XART.rdy("warpcrystalimpact_0")&&XART.rdy("weapon_muzzle_rotary_0")}',arg=stage,timeout=180000)
    for difficulty in (['easy','normal','hard','furious'] if browser_name=='msedge' else ['furious']):
     p.evaluate(PREP,{'d':difficulty,'type':typ});p.evaluate('()=>ep13Start(unit,"charge")')
     actual=p.evaluate('unit._ep13.kind');assert actual==kind,(typ,actual)
     for i in range(60):
      err=p.evaluate(shoot.STEP,4);assert not err,err;p.wait_for_timeout(1)
      if i in [20,23,27] and difficulty=='furious' and browser_name=='msedge':p.screenshot(path=str(O/f'{typ}-{i}.png'))
     row=p.evaluate('()=>({kind:unit._ep13?.kind,shots:identityShots,muzzles:identityMuzzles,shardDraws:identityShardDraws,beamFrames:identityBeamFrames,events:EP13.events,flagRestored:!unit._ep13,ownerGone:!EP13.owner})');row.update(browser=browser_name,difficulty=difficulty,type=typ);rows.append(row)
     assert row['shots'] and row['beamFrames']==0 and row['flagRestored'] and row['ownerGone'],row
     if kind=='rifle':
      assert all(s['kind']=='mg' and s['mountError']<.001 for s in row['shots']),row
      assert len(set(s['gun'] for s in row['shots']))==2 and row['muzzles'].get('mg',0)>0,row
      assert len(row['shots'])=={'easy':6,'normal':8,'hard':10,'furious':12}[difficulty],row
     else:assert all(s['kind']=='warpshard' and s['s9a']=='warpshard' and not s['boss'] for s in row['shots']) and row['shardDraws']>0 and row['muzzles'].get('crystal',0)>0 and not row['muzzles'].get('missile') and not row['muzzles'].get('mg'),row
     print('pattern',browser_name,difficulty,typ,len(row['shots']),row['muzzles'],'PASS',flush=True)
    # Exercise original controllers after upgraded-pattern recovery, including queued closures.
    p.evaluate(PREP,{'d':'normal','type':typ});p.evaluate('()=>{if(unit._mm1003){unit._mm1003.cd=0;unit._mm1003.phase="rest";}else unit._fcd=0;}')
    for i in range(120):
     err=p.evaluate(shoot.STEP,4);assert not err,err;p.wait_for_timeout(1)
    row=p.evaluate('()=>({shots:identityShots,muzzles:identityMuzzles,shardDraws:identityShardDraws,beamFrames:identityBeamFrames,wrongMuzzles:identityWrongMuzzles})');row.update(browser=browser_name,type=typ);native.append(row)
    assert row['shots'] and row['beamFrames']==0,row
    if kind=='rifle':assert all(s['kind']=='mg' and s['mountError']<.001 for s in row['shots']) and row['muzzles'].get('mg',0)>0,row
    else:assert all(s['kind']=='warpshard' and s['s9a']=='warpshard' for s in row['shots']) and row['muzzles'].get('crystal',0)>0 and row['shardDraws']>0 and not row['wrongMuzzles'],row
    print('native',browser_name,typ,len(row['shots']),'PASS',flush=True)
    if kind=='rifle':
     for side in [-1,1]:
      p.evaluate(PREP,{'d':'furious','type':typ});p.evaluate('(side)=>{ep13Start(unit,"rifle");unit._mm1003.parts.find(p=>p.kind==="gun"&&p.side===side).dead=true;}',side)
      for i in range(50):
       err=p.evaluate(shoot.STEP,4);assert not err,err
      r=p.evaluate('()=>({shots:identityShots,aliveGun:unit._mm1003.parts.find(p=>p.kind==="gun"&&!p.dead).id,beam:!!ep13Beam(unit)})');assert r['shots'] and all(s['gun']==r['aliveGun'] for s in r['shots']) and not r['beam'],r;interrupts.append({'browser':browser_name,'test':'single surviving gun','sideDestroyed':side,'shots':len(r['shots'])})
     p.evaluate(PREP,{'d':'furious','type':typ});r=p.evaluate('()=>{ep13Start(unit,"rifle");unit._mm1003.parts.filter(p=>p.kind==="gun").forEach(p=>p.dead=true);ep13Tick(unit,1/60);return {cancelled:!unit._ep13,noShots:!identityShots.length};}');assert all(r.values()),r;interrupts.append({'browser':browser_name,'test':'both barrels destroyed',**r})
    p.evaluate(PREP,{'d':'furious','type':typ});r=p.evaluate('()=>{ep13Start(unit,"charge");unit._ep13.t=unit._ep13.profile.tell;ep13Tick(unit,1/60);const before=identityShots.length;enemyShieldStunStart(unit,{max:20,once:false},null,true);updatePlay(1/60);return {released:before>0,cancelled:!unit._ep13,noNewShots:identityShots.length===before,muzzlesHidden:wm26Releases.filter(f=>f.owner===unit).every(f=>!wm26Point(f))};}');assert all(r.values()),r;interrupts.append({'browser':browser_name,'type':typ,'test':'shield break cancels weapon',**r})
   browser.close()
finally:stop()
result={'patterns':rows,'nativeControllers':native,'interruptions':interrupts,'errors':errors};(O/'verification.json').write_text(json.dumps(result,indent=2));assert not errors,errors
print('PASS',len(rows),'pattern runs',len(native),'native controller runs',len(interrupts),'interruptions',flush=True)
