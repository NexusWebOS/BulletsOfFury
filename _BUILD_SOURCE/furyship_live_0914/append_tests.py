from pathlib import Path
R=Path(__file__).resolve().parents[2];H=Path(__file__).parent;O=R/'_shots/furyship_live_0914'
p=R/'_BUILD_SOURCE/test_fl.js';b=(O/'test.before.js').read_bytes();s=b.decode('utf-8').replace('\r\n','\n')
a='_space262.size===48 && Math.abs(_space262.lx-225.888)<0.02 && Math.abs(_space262.rx-254.112)<0.02 && Math.abs(_space262.y-391.888)<0.02'
assert s.count(a)==1;s=s.replace(a,'_space262.size===48 && Math.abs(_space262.lx-230.25)<0.02 && Math.abs(_space262.rx-249.75)<0.02 && Math.abs(_space262.y-392.125)<0.02')
s=s.replace('the recovered ship is 48px and its twin laser origins sit on the measured outer cannon pods','the frame-13 ship is 48px and its twin laser origins sit on the measured gun mouths')
s=s.replace('_gravityDraw256.indexOf("if(phase===\'pixelglow\')")>=0','_gravityDraw256.indexOf("if(!newFury&&phase===\'pixelglow\')")>=0')
s=s.replace('the snap resolves to the completed Fury hull before the pixel glow begins','the legacy snap retains its completed hull and white-raster pixel glow')
a="console.log('\\n============================================');";assert s.count(a)==1
s=s.replace(a,(H/'tests.js').read_text(encoding='utf-8')+'\n'+a)
x=s.replace('\n','\r\n').encode('utf-8');assert p.read_bytes() in [b,x,(O/'test.expected.js').read_bytes()];p.write_bytes(x)
(O/'test.expected.js').write_bytes(x)
