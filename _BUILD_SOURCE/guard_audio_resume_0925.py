"""Keep the final combined Audio.resume wrapper nonthrowing too."""
from pathlib import Path
p=Path(__file__).resolve().parents[1]/'assets/game.js'
b=p.read_bytes()
a=b'  Audio.resume=function(){if(_synthResume)_synthResume();Snd.resume();};'
c=b'  Audio.resume=function(){try{if(_synthResume)_synthResume();}catch(_){}try{Snd.resume();}catch(_){} };'
assert b.count(a)==1,b.count(a)
b=b.replace(a,c,1)
assert b'\r\n' not in b
p.write_bytes(b)
print('Final Audio.resume wrapper catches both backend failures')
