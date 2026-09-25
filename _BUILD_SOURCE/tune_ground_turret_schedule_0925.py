"""Place jungle emplacements after the coast rather than in the river approach."""
from pathlib import Path

p = Path(__file__).resolve().parents[1] / 'assets/game.js'
b = p.read_bytes()

def sub(a, c):
    global b
    x=a.encode(); assert b.count(x)==1,(a,b.count(x))
    b=b.replace(x,c.encode(),1)

sub("  const start=stageNum===6?end*.45:Math.max(7,end*.21);",
    "  const start=stageNum===1?Math.max(34,end*.60):\n"
    "    stageNum===6?end*.45:Math.max(7,end*.21);")
sub("  if(!run||run.stage!==stageNum||bossActive||subBossActive)return null;",
    "  if(!run||run.stage!==stageNum||bossActive||subBossActive)return null;\n"
    "  if(stageNum===1&&mapScroll<850)return null;")
assert b'\r\n' not in b
p.write_bytes(b)
print('Stage 1 ground turrets gated to the shoreline and later field')
