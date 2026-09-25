"""Stop pellets and Laser Mist spending hits on Razorback's sealed center plate."""
from pathlib import Path

p = Path('assets/game.js')
b = p.read_bytes()
assert b'\r\n' not in b
old = b"    if(R.pools.turret>0){ const rr=RZB_R.turret*(R.scale||1);\n      if((x-b.x)*(x-b.x)+(y-b.y)*(y-b.y)<rr*rr) return 'turret'; }\n    return null;"
new = b"    /* The central plate stays sealed until both exposed guns are broken.\n       Beam penetration has its own ordered part test. */\n    return null;"
assert b.count(old) == 1
p.write_bytes(b.replace(old,new))
