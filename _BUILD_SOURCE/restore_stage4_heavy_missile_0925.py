"""Keep the heavy jet's distinctive authored missile behavior with its new pod."""
from pathlib import Path
p=Path(__file__).resolve().parents[1]/'assets/game.js'
b=p.read_bytes()
a=b"fire(p,a+side*.10,2.15,'s4rocket'"
assert b.count(a)==1,b.count(a)
b=b.replace(a,b"fire(p,a+side*.10,2.15,'s4missile'",1)
assert b'\r\n' not in b
p.write_bytes(b)
print('Stage 4 heavy jet retains its own missile projectile family')
