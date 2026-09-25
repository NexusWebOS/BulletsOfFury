"""Make the sentinel merger an absorption, not two screen-filling deaths."""
from pathlib import Path
p=Path(__file__).resolve().parents[1]/'assets/game.js'
b=p.read_bytes()
a=("    w.disabled=true;explode(w.x,w.y,54,'blue');shake=Math.max(shake,7);\n"
   "    if(Audio.SFX&&Audio.SFX.expBig)Audio.SFX.expBig();")
c=("    w.disabled=true;w.flash=.10;shake=Math.max(shake,3);\n"
   "    /* These hulls are absorbed intact by the portal. A normal death blast\n"
   "       concealed the ring and painted two huge white ship silhouettes over\n"
   "       the fusion, even though neither sentinel has exploded. */\n"
   "    if(Audio.SFX&&Audio.SFX.shieldBreakCombat)Audio.SFX.shieldBreakCombat();")
assert b.count(a.encode())==1,b.count(a.encode())
b=b.replace(a.encode(),c.encode(),1)
assert b'\r\n' not in b
p.write_bytes(b)
print('Stage 9 disabled sentinels now visibly collapse into the authored portal')
