from pathlib import Path
import hashlib,json,subprocess
R=Path(__file__).resolve().parents[2];W=Path(r'C:/Users/Mike/Documents/New project/BOF-Wave-Observe-1102');p=R/'assets/game.js';b=p.read_bytes();assert b'\r\n' not in b
(W/'game-before-exit.js').write_bytes(b)
status=subprocess.check_output(['git','status','--porcelain=v1','-uall'],cwd=R,text=True)
(W/'before-state.json').write_text(json.dumps({'core':hashlib.sha256(b).hexdigest(),'status':[{'code':s[:2],'path':s[3:]}for s in status.splitlines()]},indent=2))
a=b'    if(!_racerEntering && (e.y>VH+80 || e.x<-_sideCullPad || e.x>((typeof worldWidth===\'function\')?worldWidth():VW)+_sideCullPad)) e.dead=true;'
z=b'''    // A departing ground hull must clear in full; queued northern entries stay live.
    const _groundExit=typeof groundTrafficVehicle==='function'&&groundTrafficVehicle(e);
    const _bottomCullPad=_groundExit?Math.max(80,groundTrafficFootprint(e).h*.5+16):80;
    if(!_racerEntering && (e.y>VH+_bottomCullPad || e.x<-_sideCullPad || e.x>((typeof worldWidth==='function')?worldWidth():VW)+_sideCullPad)) e.dead=true;'''
assert b.count(a)==1;b=b.replace(a,z)
a=b'  e.y=clamp(e.y, minY, VH+80);'
z=b'''  // Keep the native exit reachable. Clamping at VH+80 made the >VH+80
  // offscreen cull impossible when a player watched a tank instead of killing it.
  const exitPad=typeof groundTrafficVehicle==='function'&&groundTrafficVehicle(e)?Math.max(80,groundTrafficFootprint(e).h*.5+16)+1:80;
  e.y=clamp(e.y, minY, VH+exitPad);'''
assert b.count(a)==1;b=b.replace(a,z);p.write_bytes(b)
print('Scoped ground departure repair; LF preserved. SHA256',hashlib.sha256(b).hexdigest())
