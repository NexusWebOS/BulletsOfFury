from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).parent
before=ROOT/'_shots/pause_menu_0914/test.before.js';path=ROOT/'_BUILD_SOURCE/test_fl.js'
s=before.read_bytes().decode('utf-8').replace('\r\n','\n')
anchor="console.log('\\n============================================');";assert s.count(anchor)==1
s=s.replace(anchor,(HERE/'tests.js').read_text(encoding='utf-8')+'\n'+anchor)
expected=s.replace('\n','\r\n').encode('utf-8')
if path.read_bytes()not in[before.read_bytes(),expected]:raise ValueError('Subsequent suite edits present')
path.write_bytes(expected)
