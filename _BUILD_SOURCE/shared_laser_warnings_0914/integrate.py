from pathlib import Path
import sys,hashlib
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).parent
before=ROOT/'_shots/shared_laser_warnings_0914/game.before.js';path=ROOT/'assets/game.js'
s=before.read_bytes().decode('utf-8')
def replace(a,b):
 global s
 assert s.count(a)==1,(s.count(a),a[:100])
 s=s.replace(a,b,1)
replace('const L23_FOV = { rime: {far: 2.0, minFar: 64} };','const L23_FOV = {rime:{far:2.0,minFar:64},inferno:{far:2.0,minFar:64},legion:{far:2.0,minFar:64}};')
replace("  opts=opts||{};\n  b._l23Beam={family:family", "  opts=opts||{};\n  if(!L23_FOV[family])L23_FOV[family]=L23_FOV.rime; // engine rule: future laser families inherit combat FOV\n  b._l23Beam={family:family")
replace("im=wall?(xartPalette(key,'#143ca8')||XART.get(key)):XART.get(key)","im=wall?(xartTint(key,'#10328a',.72)||XART.get(key)):XART.get(key)")
a="ctx.drawImage(im,-B.width/2,0,B.width,len);}ctx.restore();"
b="ctx.drawImage(im,-B.width/2,0,B.width,len);if(wall){const core=XART.get(key);ctx.drawImage(core,-B.width*.065,0,B.width*.13,len);}}ctx.restore();"
replace(a,b)
expected=s.encode('utf-8');out=ROOT/'_shots/shared_laser_warnings_0914/game.expected.js'if '--dry-run'in sys.argv else path
if out==path and path.read_bytes()not in[before.read_bytes(),expected]:raise ValueError('Subsequent edits present')
out.write_bytes(expected);print(hashlib.sha256(expected).hexdigest())
