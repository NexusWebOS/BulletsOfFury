"""Let disabled sentinels' hit flash expire during fusion, not freeze white."""
from pathlib import Path
p=Path(__file__).resolve().parents[1]/'assets/game.js'
b=p.read_bytes()
def sub(a,c):
    global b
    x=a.encode();assert b.count(x)==1,(a,b.count(x))
    b=b.replace(x,c.encode(),1)
sub("  const F=b._s9fusion;if(!F)return false;\n  /* ⚠ THE RING OUTLIVES",
    "  const F=b._s9fusion;if(!F)return false;\n"
    "  for(const w of [F.left,F.right])if(w.flash>0)w.flash=Math.max(0,w.flash-dt);\n"
    "  /* ⚠ THE RING OUTLIVES")
sub("      if(w.flash>0)w.flash=Math.max(0,w.flash-dt);\n      w.spin=",
    "      w.spin=")
assert b'\r\n' not in b
p.write_bytes(b)
print('Fusion hit flashes now decay in both twin and fuse phases')
