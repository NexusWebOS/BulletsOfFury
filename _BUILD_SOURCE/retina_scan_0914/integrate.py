from pathlib import Path
import hashlib,sys
R=Path(__file__).resolve().parents[2];H=Path(__file__).parent;O=R/'_shots/retina_scan_0914';p=R/'assets/game.js';b=O/'game.before.js'
if not b.exists():b.write_bytes(p.read_bytes());(O/'test.before.js').write_bytes((R/'_BUILD_SOURCE/test_fl.js').read_bytes())
s=b.read_bytes().decode('utf-8')
def rep(a,z):
 global s
 assert s.count(a)==1,(s.count(a),a[:100]);s=s.replace(a,z,1)
rep('function cycleLock(){',(H/'engine.js').read_text(encoding='utf-8-sig').replace('\r\n','\n')+'\nfunction cycleLock(){')
rep('  const r=retina, t=r.target;\n  if(!retinaTargetValid(t))','  const r=retina, t=r.target;r.animT=(r.animT||0)+dt;\n  if(!retinaTargetValid(t))')
rep('    if(cHeld && fireHeld){','    const scans=player._retinaScan;\n    if(cHeld && fireHeld && !(scans&&(scans.queue||scans.marks.length))){')
rep('function useBomb(){','function useBomb(forcedTarget){')
rep('  const tgt=retinaTargetValid(retina.target)?retina.target:null;', '  const tgt=forcedTarget===undefined?(retinaTargetValid(retina.target)?retina.target:null):(retinaTargetValid(forcedTarget)?forcedTarget:null);')
rep('  if(tgt && !holding){ retina.target=null; retina.phase=null; }','  if(forcedTarget===undefined&&tgt && !holding){ retina.target=null; retina.phase=null; }')
rep('  updateRetina(dt); updatePlayerLocks(dt); updateSmokeTrails(dt);','  updateRetina(dt);for(const s of seatList())withSeat(s,()=>retinaScanTick(dt)); updatePlayerLocks(dt); updateSmokeTrails(dt);')
rep("    if(Input.tapSeat(_seat,'bomb')){", "    retinaScanHeldFire();\n    if(Input.tapSeat(_seat,'bomb')){")
rep('      if(!retinaFire() && !lizzieFire()){','      if(!retinaScanFire()&&!retinaFire() && !lizzieFire()){')
rep("if(Input.tapSeat(_seat,'retina')||(_seat===1&&Input.tap('l'))) cycleLock();", "/* Retina input runs before roll/somersault direction taps. */")
rep("    const _nowT=performance.now()/1000;", "    if(Input.tapSeat(_seat,'retina')||(_seat===1&&Input.tap('l'))){retinaScanClear();cycleLock();}\n    retinaScanInput();\n    const _nowT=performance.now()/1000;")
rep('  drawSmokeTrails(); drawRetina(); drawPlayerLocks();','  drawSmokeTrails(); drawRetina(); drawRetinaScans(); drawPlayerLocks();')
a=s.index('function drawRetina(){');z=s.index('function drawWarning(){',a);section=s[a:z].replace('performance.now()','((r.animT||0)*1000)');s=s[:a]+section+s[z:]
rep('function breakContainer(p){','function breakContainer(p){\n  retinaScanSupply(p);')
rep('function applyPowerup(p){','function applyPowerup(p){\n  if(p.kind===\'retinascan\'){run.retinaScan=true;if(typeof arcadeBanner===\'function\')arcadeBanner(\'RETINA SCAN UPGRADE\');if(Audio.SFX.select)Audio.SFX.select();return;}')
rep("    if(p.kind==='capsule'){ drawCapsule", "    if(p.kind==='retinascan'){retinaScanPickupDraw(p,yb);continue;}\n    if(p.kind==='capsule'){ drawCapsule")
assert s.count('  run.sonicT=0; run._sonicCd=0; run._lzCd=0;')==2
s=s.replace('  run.sonicT=0; run._sonicCd=0; run._lzCd=0;','  run.sonicT=0; run._sonicCd=0; run._lzCd=0;player._retinaScan=null;player2._retinaScan=null;')
rep('  run.contUsed=0;   // continue counter resets per RUN', '  run.retinaScan=false;run2.retinaScan=false;\n  run.contUsed=0;   // continue counter resets per RUN')
rep('    stage:run.stage, score:run.score, lives:run.lives, bombs:run.bombs,','    stage:run.stage, score:run.score, lives:run.lives, bombs:run.bombs,retinaScan:!!run.retinaScan,')
rep('  run.bombs=(s.bombs==null?2:s.bombs);','  run.bombs=(s.bombs==null?2:s.bombs);run.retinaScan=!!s.retinaScan;player._retinaScan=null;')
# Co-op equipment field ownership; scanners themselves live on each player.
rep("'pilot','missileLevel','wvars'", "'pilot','missileLevel','retinaScan','wvars'")
rep('  floaters.push({x,y,vy:-0.6,t:0,life:0.6,r:18,flashring:true,color:col});','  particles.push({x,y,vx:0,vy:0,t:0,life:.6,r:18,flashring:true,color:col}); // authored shock ring belongs to effects, not floating text')
a=s.index('function useBomb(forcedTarget){');z=s.index('/* ============================================================',a);part=s[a:z];assert part.count('Audio.SFX.weapon(); shake=')==1;part=part.replace('Audio.SFX.weapon(); shake=','if(forcedTarget!==undefined)(Audio.SFX.missile||Audio.SFX.weapon)();else Audio.SFX.weapon(); shake=');s=s[:a]+part+s[z:]
expected=s.encode('utf-8');dest=O/'game.expected.js'if '--dry-run'in sys.argv else p
if dest==p and p.read_bytes()not in[b.read_bytes(),expected]:raise ValueError('Subsequent runtime edits present')
dest.write_bytes(expected);print(hashlib.sha256(expected).hexdigest())
