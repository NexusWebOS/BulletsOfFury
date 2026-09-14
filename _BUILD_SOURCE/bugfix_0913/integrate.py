"""Install the code-owned finite beam helpers, pellet predicate and nuclear retrigger fix."""
from pathlib import Path
root=Path(__file__).resolve().parents[2]
p=root/'assets/game.js';g=p.read_bytes().decode('utf-8')
def change(old,new):
    global g
    if new in g:return
    assert g.count(old)==1,(old[:100],g.count(old))
    g=g.replace(old,new)
marker='/* Finite held-beam intersections:'
block=(Path(__file__).parent/'beam.js').read_text(encoding='utf-8')+'\n'
end=g.index('function subBossHit(x, y)')
if marker in g:
    start=g.index(marker);g=g[:start]+block+g[end:]
else:g=g[:end]+block+g[end:]
change("  if(b._jcGhost) return false; // safe scripted fly-through: neither body nor bullets collide",
       "  if(b._jcGhost) return false; // safe scripted fly-through: neither body nor bullets collide\n  if(b._rzb) return razorbackPartAt(b,x,y)!==null;")
change("        if(b._sbt<=0 && sy<=b.bot && Math.abs(b.x-subBoss.x)<(subBoss.w/2+b.w/2)){ hitSubBoss(b.dmg, b.x, sy); weaponHitSfx('laser'); b._sbt=0.05; }",
       """        if(b._sbt<=0&&(subBoss._rzb||subBoss._tempestDuo)){
          const impact=subBossBeamImpact(subBoss,b);
          if(impact){hitSubBoss(b.dmg,impact.x,impact.y);weaponHitSfx('laser');b._sbt=0.05;}
        }else if(b._sbt<=0 && sy<=b.bot && Math.abs(b.x-subBoss.x)<(subBoss.w/2+b.w/2)){ hitSubBoss(b.dmg, b.x, sy); weaponHitSfx('laser'); b._sbt=0.05; }""")
change("    nuclearDetonate: {g:0.66, lp:4200, min:1.80},",
       "    nuclearDetonate: {g:0.66, lp:4200, min:0.12}, // distinct Cole impacts must not lose the middle boom")
p.write_bytes(g.replace('\r\n','\n').encode('utf-8'))
print('Installed finite beam routing, exposed Razorback pellet collision and nuclear impact retrigger fix.')
