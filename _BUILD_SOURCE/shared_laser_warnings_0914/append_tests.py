from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).parent
before=ROOT/'_shots/shared_laser_warnings_0914/test.before.js';path=ROOT/'_BUILD_SOURCE/test_fl.js'
s=before.read_bytes().decode('utf-8').replace('\r\n','\n')
a='!!L23_FOV.rime && !L23_FOV.inferno && !L23_FOV.legion';b='!!L23_FOV.rime && !!L23_FOV.inferno && !!L23_FOV.legion';assert s.count(a)==1;s=s.replace(a,b)
# The original assertion label explicitly documented its now superseded scope.
s=s.replace('only the stage-3 (rime) laser wears the cones - the lava and legion lanes ship unchanged','all shared laser families use the color-changing combat FOV')
anchor="console.log('\\n============================================');";assert s.count(anchor)==1
s=s.replace(anchor,(HERE/'tests.js').read_text(encoding='utf-8')+'\n'+anchor)
expected=s.replace('\n','\r\n').encode('utf-8')
if path.read_bytes()not in[before.read_bytes(),expected,expected.replace(b"all shared laser families use the color-changing combat FOV",b"only the stage-3 (rime) laser wears the cones - the lava and legion lanes ship unchanged"),expected.replace(b"all shared laser families use the color-changing combat FOV",b"only the stage-3 (rime) laser wears the cones - the lava and legion lanes ship unchanged")]:raise ValueError('Subsequent suite edits present')
path.write_bytes(expected)
