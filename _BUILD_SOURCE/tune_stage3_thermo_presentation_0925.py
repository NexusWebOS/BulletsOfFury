"""Give the Furious boss warning its promised half-screen lock and clear the HUD."""
from pathlib import Path

path = Path('assets/stage3_thermo.js')
raw = path.read_bytes()
newline = b'\r\n' if b'\r\n' in raw else b'\n'
source = raw.replace(b'\r\n', b'\n')
def swap(old, new):
    global source
    assert source.count(old) == 1, (old, source.count(old))
    source = source.replace(old, new)

swap(b"b.name='THERNO, THE SHOCKBRINGER';b.w=262;b.h=280;b.ty=145;",
     b"b.name='THERNO, THE SHOCKBRINGER';b.w=262;b.h=280;b.ty=170;")
swap(b"const q=clamp((S.t-.15)/1.55,0,1),sz=role==='boss'?250:180;",
     b"const q=clamp((S.t-.15)/1.55,0,1),sz=role==='boss'?viewW()*.5:220;")
path.write_bytes(source.replace(b'\n', newline))
