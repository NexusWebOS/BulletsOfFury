"""Give sewer toxic craft a luminance-preserving green shield family."""
from pathlib import Path
p=Path(__file__).resolve().parents[1]/'assets/game.js'
b=p.read_bytes()
def sub(a,c):
    global b
    x=a.encode();assert b.count(x)==1,(a,b.count(x))
    b=b.replace(x,c.encode(),1)
sub("  bubble_fire: {kind:'bubble', prefix:'nes_bubble_fire', hit:3, tint:null},",
    "  bubble_fire: {kind:'bubble', prefix:'nes_bubble_fire', hit:3, tint:null},\n"
    "  bubble_toxic:{kind:'bubble', prefix:'nes_bubble', hit:0, tint:'#59ef45'},")
sub("  s7skimmer:    {stage:7,family:'bubble_fire',ratio:.34,drawScale:2.55,once:1},",
    "  s7skimmer:    {stage:7,family:'bubble_toxic',ratio:.34,drawScale:2.55,once:1},")
sub("  s7barge:      {stage:7,family:'bubble_fire',ratio:.32,drawScale:2.50,once:1},",
    "  s7barge:      {stage:7,family:'bubble_toxic',ratio:.32,drawScale:2.50,once:1},")
assert b'\r\n' not in b
p.write_bytes(b)
print('Toxic skimmer/barge shields now use green light on the existing authored circular shell')
