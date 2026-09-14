from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).parent
before=ROOT/'_shots/missile_supplies_0914/test.before.js';path=ROOT/'_BUILD_SOURCE/test_fl.js'
s=before.read_bytes().decode('utf-8').replace('\r\n','\n')
changes={
"r6.indexOf('missilepack20')>=0 && r6.indexOf('missilepack35')>=0":"r6.indexOf('missilepack20')>=0 && r6.indexOf('missilepack35')<0",
"stage 6 rolls the 20 and the 35":"stage 6 rolls x20 and retires the x35 RNG supply",
"r8.indexOf('missilepack20')<0 && r8.indexOf('missilepack35')<0":"r8.indexOf('missilepack20')<0 && r8.indexOf('missilepack35')<0",
"the 20 and 35 are stage 6 only":"stage 8 excludes the smaller x20 and retired x35 packs",
"r5.indexOf('missilepack20')<0 && r5.indexOf('missilepack35')<0 && r5.indexOf('missilepack50')<0":"r5.indexOf('missilepack20')>=0 && r5.indexOf('missilepack35')<0 && r5.indexOf('missilepack50')<0",
"an ungated stage rolls only the original 2/5/10 packs":"stage 5 rolls x20 alongside x5/x10 without stage-8 prizes",
"_anyHundred.length===0":"_anyHundred.length===1&&r8.indexOf('missilepack100')>=0&&r5.indexOf('missilepack100')<0&&r6.indexOf('missilepack100')<0",
"the 100 crate NEVER spawns from a stage roll — cinematic only":"x100 normal ammo rolls only on stage 8; cinematic grants remain available"
}
for a,b in changes.items():
 assert s.count(a)==1,(s.count(a),a)
 s=s.replace(a,b,1)
anchor="console.log('\\n============================================');"
assert s.count(anchor)==1
s=s.replace(anchor,(HERE/'tests.js').read_text(encoding='utf-8')+'\n'+anchor)
expected=s.replace('\n','\r\n').encode('utf-8')
if path.read_bytes()not in[before.read_bytes(),expected]:raise ValueError('Subsequent suite edits present')
path.write_bytes(expected)
