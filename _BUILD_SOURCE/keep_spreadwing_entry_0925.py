"""Allow Stage 8's spread-wing crossers to enter from their authored side lanes."""
from pathlib import Path

p=Path('assets/game.js');b=p.read_bytes();assert b'\r\n' not in b
old=(b"      || (e.pattern==='jetflyby' && e._phase!=='exit');\n"
     b"    if(!_racerEntering && (e.y>VH+80 || e.x<-80 || e.x>((typeof worldWidth==='function')?worldWidth():VW)+80)) e.dead=true;")
new=(b"      || (e.pattern==='jetflyby' && e._phase!=='exit')\n"
     b"      || (e._s8mega==='s8spread' && ((e._side>0&&e.x<0)||\n"
     b"          (e._side<0&&e.x>((typeof worldWidth==='function')?worldWidth():VW))));\n"
     b"    if(!_racerEntering && (e.y>VH+80 || e.x<-80 || e.x>((typeof worldWidth==='function')?worldWidth():VW)+80)) e.dead=true;")
assert b.count(old)==1;p.write_bytes(b.replace(old,new))
