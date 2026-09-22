"""Wire the authored toxic machine round with exact, LF-safe replacements."""
from pathlib import Path

path = Path('assets/game.js')
data = path.read_bytes()
assert b'\r\n' not in data

old = b"  X._src['cfx_stage7_warden_shell']='assets/game/combat_final/stage7_warden_toxic_pressure_shell_spritecook.png';"
new = old + b"\n  X._src['cfx_stage7_warden_machine_round']='assets/game/combat_final/stage7_warden_toxic_machine_round_0920.png';"
assert data.count(old) == 1
data = data.replace(old, new, 1)

old = b"  if(b._s7warden){\n    const role=b._s7warden,mul=b.szMul||1;"
new = b"""  if(b._s7warden){
    if(b._s7Chain){
      const key='cfx_stage7_warden_machine_round';if(!XART.rdy(key))return false;
      ctx.save();ctx.translate(b.x,b.y);ctx.rotate(Math.atan2(b.vy||1,b.vx||0));
      ctx.imageSmoothingEnabled=false;ctx.drawImage(XART.get(key),-17,-8.5,34,17);ctx.restore();
      return true;
    }
    const role=b._s7warden,mul=b.szMul||1;"""
assert data.count(old) == 1
data = data.replace(old, new, 1)
assert b'\r\n' not in data
path.write_bytes(data)
print('Wired authored Stage 7 machine round; LF preserved')
