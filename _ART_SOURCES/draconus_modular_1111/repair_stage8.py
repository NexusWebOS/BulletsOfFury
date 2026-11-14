from pathlib import Path
import hashlib,json,subprocess
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');p=R/'assets/playtest_repairs_1108.js';old=p.read_bytes();sha=lambda a:hashlib.sha256(a).hexdigest()
before=b"if(!q||typeof q!=='object'||!('hp' in q)||seen.has(q))continue;seen.add(q);parts.push(q);"
after=b"if(!q||typeof q!=='object'||q._retinaOwner||!('hp' in q)||seen.has(q))continue;seen.add(q);parts.push(q);"
if before in old:
 assert old.count(before)==1
 (W/'playtest_repairs_1108.before.js').write_bytes(old)
 new=old.replace(before,after)
 assert p.read_bytes()==old;p.write_bytes(new)
 (W/'stage8-repair.json').write_text(json.dumps(dict(file=str(p),before=sha(old),after=sha(new),change='Exclude cached Retina target descriptors from genuine damage-pool flash polling. Their getters can retain obsolete host sockets across a copied-form transition. Real child pools, HP, phase controllers and gun ownership are unchanged.'),indent=2))
else:assert after in old
subprocess.run(['node','--check',str(p)],check=True)
print('Repaired stale Retina descriptor polling in boss hit feedback; native damage/phase owners untouched.',flush=True)
