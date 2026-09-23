"""Real Chromium: modular guns, warning/laser separation, lock, release and encounter cycle."""
import base64,json,sys,http.server
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'))
from shoot import GAME,SETUP,TRAP_RAF,serve
from playwright.sync_api import sync_playwright
OUT=ROOT/'_shots/harrier_round_muzzle_0923';OUT.mkdir(exist_ok=True)
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
port,stop=serve(GAME);errors=[]
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);pg=br.new_page(viewport={'width':1100,'height':1200})
  pg.on('pageerror',lambda e:errors.append(str(e)));pg.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  pg.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load');pg.wait_for_function('()=>window.__bofFrames>4')
  pg.evaluate(TRAP_RAF);pg.evaluate(SETUP,{'state':'PLAY','stage':5,'pilot':'cole','invuln':True})
  pg.evaluate("""()=>{diffKey='furious';DIFF=DIFFS.furious;run.spaceMode=true;story=null;stagePlan=[];enemies=[];eBullets=[];pBullets=[];powerups=[];
    boss=null;spawnSubBoss('chaosharrier');subBoss.enter=false;subBoss.x=240;subBoss.y=150;subBoss._chVisible=true;subBoss._chCollision=true;
    player.x=240;player.y=440;player.invuln=1e9;player.dead=false;camX=0;
    window.advanceHarrier=(seconds)=>{for(let t=0;t<seconds-1e-8;t+=1/120){subBoss.t+=1/120;chaosHarrierUpdate(subBoss,1/120);}};
    window.beginHarrier=(state)=>{eBullets=[];subBoss._chFlashes=[];chaosHarrierBegin(subBoss,state);advanceHarrier(1/120);};
    // Capture the resolved key inside the game's own drawImage call, including cached canvases.
    window.harrierDraws=[];const get=XART.get;let key='';XART.get=function(k){key=k;return get.call(this,k)};
    const draw=ctx.drawImage;ctx.drawImage=function(...a){harrierDraws.push({key,args:a.slice(1),matrix:Array.from([ctx.getTransform().a,ctx.getTransform().b,ctx.getTransform().c,ctx.getTransform().d,ctx.getTransform().e,ctx.getTransform().f])});return draw.apply(this,a)};
    l23FovWarm();for(const c of ['green','yellow','red'])XART.rdy('bmfx_alert_'+c+'_danger');
  }""")
  pg.wait_for_function("()=>['hull','gun','emitter','thruster'].every(p=>[0,1,2,3].every(f=>XART.rdy('ch2_'+p+'_'+f)))&&XART.rdy('ch_charge_2')&&XART.rdy('ch_sidelaser_1')&&XART.rdy('ch_beam_1')&&XART.rdy('bmfx_alert_red_danger')&&[0,1,2,3,4,5,6,7].every(f=>XART.rdy('laser_round_muzzle_'+f))",timeout=30000)
  def shot(name):
   pg.evaluate('()=>{shake=0;subBoss.flash=0;harrierDraws=[];drawWorld(0)}')
   data=pg.evaluate("document.getElementById('screen').toDataURL('image/png').split(',')[1]")
   (OUT/(name+'.png')).write_bytes(base64.b64decode(data))
   return pg.evaluate("()=>({oldLance:harrierDraws.filter(q=>/^ch_lance_/.test(q.key)).length,beams:harrierDraws.filter(q=>/^ch_(sidelaser|beam)_/.test(q.key)).length,hardware:harrierDraws.filter(q=>/^ch2_gun_/.test(q.key)).length,warnings:harrierDraws.filter(q=>/bmfx_(alert|fov)/.test(q.key)).length})")
  result={}
  pg.evaluate("()=>beginHarrier('side')")
  pg.evaluate("()=>advanceHarrier(chaosHarrierWarm('side')*.20)");result['green']=shot('01_green_warning')
  pg.evaluate("()=>advanceHarrier(chaosHarrierWarm('side')*.35)");result['yellow']=shot('02_yellow_warning')
  locked=pg.evaluate("()=>JSON.stringify(subBoss._chTell.paths)")
  pg.evaluate("()=>{player.x=400;advanceHarrier(chaosHarrierWarm('side')*.25)}")
  assert pg.evaluate("()=>JSON.stringify(subBoss._chTell.paths)")==locked
  result['red']=shot('03_red_locked')
  assert all(result[k]['beams']==0 and result[k]['oldLance']==0 and result[k]['hardware']==2 for k in ['green','yellow','red']),result
  pg.evaluate("()=>advanceHarrier(.30)");result['sideFire']=shot('04_modular_side_fire')
  assert result['sideFire']['beams']==1 and result['sideFire']['oldLance']==0,result
  assert pg.evaluate("()=>JSON.stringify(subBoss._chTell.paths)")==locked
  pg.evaluate("()=>advanceHarrier(.7)");result['cooldown']=shot('05_beams_off')
  assert result['cooldown']['beams']==0
  for state in ['plasma','missile','beam','salvo']:
   pg.evaluate('(s)=>beginHarrier(s)',state)
   pg.evaluate('(s)=>advanceHarrier(chaosHarrierWarm(s)*.75)',state)
   assert pg.evaluate('()=>eBullets.length===0&&!subBoss._chSideOn&&!subBoss._chBeamActive'),state
   shot(state+'_warning')
   pg.evaluate('(s)=>advanceHarrier(chaosHarrierWarm(s)*.25+.02)',state)
   result[state]=shot(state+'_fire')
   if state in ['beam','salvo']:assert result[state]['beams']==1,result
   else:assert pg.evaluate('()=>eBullets.length')>0,state
  result['damage']=pg.evaluate("""()=>{beginHarrier('beam');advanceHarrier(chaosHarrierWarm('beam')*.80);
    const real=playerHit;let hits=0;playerHit=()=>{hits++};player.invuln=0;
    const q=subBoss._chTell.paths[0],p=chaosHarrierPoint(subBoss,q.slot);player.x=p.x+Math.cos(q.a)*220;player.y=p.y+Math.sin(q.a)*220;
    advanceHarrier(.01);const warningHits=hits;advanceHarrier(.3);const beamHits=hits;
    player.x-=140;advanceHarrier(.1);const safe=hits===beamHits;
    playerHit=real;player.invuln=1e9;return {warningHits,beamHits,safe};}""")
  assert result['damage']['warningHits']==0 and result['damage']['beamHits']>0 and result['damage']['safe'],result['damage']
  # Run complete authored warp / pinned attack cycles with real rendering and allow asset decode.
  pg.evaluate("()=>{player.x=240;subBoss._chWarpCount=0;subBoss._chStandLeft=0;subBoss._chStandStep=0;chaosHarrierFinish(subBoss);window.sequence=[];window.lastHarrier='';}")
  for i in range(12):
   pg.evaluate("""()=>{for(let n=0;n<240;n++){const b=subBoss;b.t+=1/60;chaosHarrierUpdate(b,1/60);
     if(b._chState!==lastHarrier){sequence.push(b._chState);lastHarrier=b._chState;}}
     drawWorld(0);} """);pg.wait_for_timeout(20)
  result['sequence']=pg.evaluate('()=>sequence')
  assert all(s in result['sequence'] for s in ['warpout','warpin','plasma','missile','side','beam','salvo']),result['sequence']
  result['difficulty']={}
  for difficulty in ['easy','normal','hard','furious']:
   result['difficulty'][difficulty]=pg.evaluate("""(d)=>{diffKey=d;DIFF=DIFFS[d];beginHarrier('plasma');
     advanceHarrier(chaosHarrierWarm('plasma')-.03);const early=eBullets.length;
     advanceHarrier(1.4);const count=eBullets.length;
     subBoss._chStandLeft=1;subBoss._chStandStep=2;chaosHarrierSelect(subBoss);
     return {early,count,finisher:subBoss._chState};}""",difficulty)
   expected=8 if difficulty=='furious' else (6 if difficulty=='hard' else 4)
   assert result['difficulty'][difficulty]=={'early':0,'count':expected,'finisher':'salvo' if difficulty in ['hard','furious'] else 'beam'}
  result['mounts']=pg.evaluate("""()=>{beginHarrier('side');advanceHarrier(.65);const b=subBoss,p=chaosHarrierPoint(b,'left_cannon');
    b.x+=20;b.y+=15;const q=chaosHarrierPoint(b,'left_cannon');return {dx:q.x-p.x,dy:q.y-p.y};}""")
  assert abs(result['mounts']['dx']-20)<.001 and abs(result['mounts']['dy']-15)<.001
  # Every salvo emitter warns independently, then owns exactly one beam and one live muzzle.
  pg.evaluate("()=>{diffKey='furious';DIFF=DIFFS.furious;beginHarrier('salvo');window.salvoSeen=[];window.salvoWarnings=[];window.maxLasers=0;window.anchorError=0;window.orbitSamples=[];}")
  for frame in range(85):
   sample=pg.evaluate("""()=>{advanceHarrier(.075);const b=subBoss,q=b._chActiveLaser,W=b._chTell;
     if(W&&b._chT<W.warm&&!salvoWarnings.includes(W.slot))salvoWarnings.push(W.slot);
     orbitSamples.push([b.x,b.y]);harrierDraws=[];drawWorld(0);
     const beams=harrierDraws.filter(d=>/^ch_(beam|sidelaser)_/.test(d.key));maxLasers=Math.max(maxLasers,beams.length);
     if(q){
       const muzzle=harrierDraws.find(d=>/^laser_round_muzzle_/.test(d.key));
       if(!muzzle)throw Error('Missing single muzzle flash');
       const laser=beams[0];if(!laser)throw Error('Missing beam');
       anchorError=Math.max(anchorError,Math.hypot(laser.matrix[4]-muzzle.matrix[4],laser.matrix[5]-muzzle.matrix[5]));
       const frame=chaosHarrierWeaponFrame(b,q.slot);
       const hardware=harrierDraws.find(d=>q.slot==='nose'?d.key==='ch2_emitter_'+frame:d.key==='ch2_gun_'+frame);
       const tip=q.slot==='nose'?[64,219]:[[104,213],[103,214],[104,210],[103,220]][frame];
       const x=tip[0]+hardware.args[0],y=tip[1]+hardware.args[1],m=hardware.matrix;
       anchorError=Math.max(anchorError,Math.hypot(m[0]*x+m[2]*y+m[4]-muzzle.matrix[4],m[1]*x+m[3]*y+m[5]-muzzle.matrix[5]));
       if(!salvoSeen.includes(q.slot)){salvoSeen.push(q.slot);return q.slot;}
     }return null;}""")
   if sample:shot('sequential_'+sample)
   pg.wait_for_timeout(2)
  result['salvo']=pg.evaluate("()=>({shots:salvoSeen,warnings:salvoWarnings,maxLasers,anchorError,orbitTravel:Math.max(...orbitSamples.map(p=>p[0]))-Math.min(...orbitSamples.map(p=>p[0]))})")
  assert result['salvo']['shots']==['left_cannon','nose','right_cannon'],result['salvo']
  assert result['salvo']['warnings']==result['salvo']['shots'],result['salvo']
  assert result['salvo']['maxLasers']==1 and result['salvo']['anchorError']<.001 and result['salvo']['orbitTravel']>25,result['salvo']
  pg.evaluate("()=>{beginHarrier('salvo');advanceHarrier(1.1);subBoss.dead=true;}")
  result['dead']=shot('dead_no_lasers');assert result['dead']['beams']==0 and result['dead']['warnings']==0
  assert not errors,errors
  result['errors']=errors;(OUT/'results.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2));br.close()
finally:stop()
