from pathlib import Path
import hashlib,sys
R=Path(__file__).resolve().parents[2];H=Path(__file__).parent;O=R/'_shots/retina_targets_0914';p=R/'assets/game.js';before=O/'game.before.js'
if not before.exists():before.write_bytes(p.read_bytes());(O/'test.before.js').write_bytes((R/'_BUILD_SOURCE/test_fl.js').read_bytes())
s=before.read_bytes().decode('utf-8')
def rep(a,b):
 global s
 assert s.count(a)==1,(s.count(a),a[:100]);s=s.replace(a,b,1)
a=s.index('function _lockTargets(){');z=s.index('function cycleLock(){',a);s=s[:a]+(H/'engine.js').read_text(encoding='utf-8-sig').replace('\r\n','\n')+s[z:]
rep('if(!t || t.dead){ r.target=null; r.phase=null; return; }','if(!retinaTargetValid(t)){ r.target=null; r.phase=null; return; }')
rep("const tgt=(retina.target && !retina.target.dead)?retina.target:null;\n  pBullets.push({kind:'gmiss'", "const tgt=retinaTargetValid(retina.target)?retina.target:null;\n  pBullets.push({kind:'gmiss'")
rep('      const t=b.tgt;\n      const tx=', '      const t=retinaTargetValid(b.tgt)?b.tgt:null;\n      if(!t)b.tgt=null;\n      const tx=')
rep("if(t&&!t.dead){ if(t===boss) hitBoss(b.dmg); else if(typeof subBoss!=='undefined'&&t===subBoss) hitSubBoss(b.dmg, b.x, b.y); else hitEnemy(t,b.dmg); }",'if(t&&!t.dead)retinaMissileDamage(t,b.dmg,b);')
rep('t!==boss && dist2(boss.x,boss.y,b.x,b.y)<110*110','t!==boss && (!t||t._retinaOwner!==boss) && dist2(boss.x,boss.y,b.x,b.y)<110*110')
rep('t!==subBoss && dist2(subBoss.x,subBoss.y,b.x,b.y)<110*110','t!==subBoss && (!t||t._retinaOwner!==subBoss) && dist2(subBoss.x,subBoss.y,b.x,b.y)<110*110')
a=s.index("    if(b.kind==='missile'){",s.index("if(b.kind==='gmiss'||b.kind==='nukem')"));z=s.index('      let ang=Math.atan2',a)
s=s[:a]+"    if(b.kind==='missile'){\n      b.t=(b.t||0)+dt;\n      let tx=null,ty=null,best=1e9;\n      for(const t of _lockTargets()){const d=Math.hypot(t.x-b.x,t.y-b.y);if(d<best){best=d;tx=t.x;ty=t._drawY!=null?t._drawY:t.y;}}\n"+s[z:]
rep('    boom:            {g:0.62, lp:4400, min:0.45},','    expBig:          {g:0.40, lp:4600, min:0.20}, // measured death bursts previously clipped when overlapping\n    expSmall:        {g:0.55, lp:5200, min:0.06},\n    boom:            {g:0.62, lp:4400, min:0.45},')
rep('      a.push(boss);', '      for(const t of retinaBossTargets(boss))if(a.indexOf(t)<0)a.push(t);')
rep('    else a.push(subBoss);', '    else a.push(...retinaBossTargets(subBoss));')
rep('  if(spaceShootableContainer(t)){', '  if(t._retinaOwner){retinaMissileDamage(t,dmg,b);}\n  else if(spaceShootableContainer(t)){')
expected=s.encode('utf-8');dest=O/'game.expected.js'if '--dry-run'in sys.argv else p
if dest==p and p.read_bytes()not in[before.read_bytes(),expected]:raise ValueError('Subsequent runtime edits present')
dest.write_bytes(expected);print(hashlib.sha256(expected).hexdigest())
