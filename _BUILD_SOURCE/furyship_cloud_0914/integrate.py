from pathlib import Path
import hashlib
R=Path(__file__).resolve().parents[2];H=Path(__file__).parent;O=R/'_shots/furyship_cloud_0914';p=R/'assets/game.js'
b=(O/'game.before.js').read_bytes();assert hashlib.sha256(b).hexdigest()=='3fc67f9238c635ee3367f574a2a57bd2a1094ffadcf52aae1b7e76de59a02e45'
s=b.decode('utf-8')
def edit(a,z):
 global s
 assert s.count(a)==1,(a[:100],s.count(a));s=s.replace(a,z)
edit(" {key:'hull',x:0,y:13},{key:'nose',x:0,y:-27}",""" {key:'hull',x:0,y:13},{key:'nose',x:0,y:-27},
 {key:'nose',x:-31,y:-14,partScale:.72},{key:'nose',x:31,y:-14,partScale:.72},
 {key:'engine_left',x:-21,y:28,partScale:.8},{key:'engine_right',x:21,y:28,partScale:.8},
 {key:'hull',x:-14,y:-7,partScale:.65},{key:'hull',x:14,y:-7,partScale:.65}""")
edit("for(const q of FURY_KIT)for(const v of FURY_VIEWS)FURY_KEYS.push(q.key+'_'+v);","for(const q of FURY_KIT)for(const v of FURY_VIEWS)if(!FURY_KEYS.includes(q.key+'_'+v))FURY_KEYS.push(q.key+'_'+v);")
edit("radius=(125+(i%3)*20)*scale;","radius=(92+(i%2)*45)*scale;")
edit("px=ox+Math.cos(angle)*90*scale*s;py=oy+Math.sin(angle)*60*scale*s+35*scale*s*s;","px=ox+Math.cos(angle)*28*scale*s;py=oy+Math.sin(angle)*25*scale*s+12*scale*s*s;")
edit("   const opacity=snap>.78?1-(snap-.78)/.22:1;","   const opacity=snap>.78?1-(snap-.78)/.22:1;\n   const pieceSize=size*(q.partScale||1)*lerp(1.65,1,snap);")
# Restrict sizing substitution to the component block, leaving the full hull unchanged.
a=s.index('   if(locked)furyShipBlit');z=s.index('   ctx.restore();',a)
s=s[:a]+s[a:z].replace('0,0,size,size,pilot','0,0,pieceSize,pieceSize,pilot')+s[z:]
edit("x,y,size*2.6,size*1.65,.65,phase!=='snap'","x,y,size*1.22,size*.82,.48,phase!=='snap'")
edit("x,y,size*2.1,size*1.4,.8,false","x,y,size*1.12,size*.8,.6,false")
edit('function drawLaunch(dt){', (H/'intro.js').read_text(encoding='utf-8')+"\nfunction drawLaunch(dt){\n  if(run.stage===5&&!furyLegacyShip){furyIntroDraw(Math.max(0,dt||0));return;}")
expected=s.encode('utf-8');assert b'\r\n'not in expected
assert p.read_bytes() in [b,expected,(O/'game.expected.js').read_bytes()if(O/'game.expected.js').exists()else b],'Concurrent runtime changes'
p.write_bytes(expected);(O/'game.expected.js').write_bytes(expected)
print(hashlib.sha256(expected).hexdigest())
