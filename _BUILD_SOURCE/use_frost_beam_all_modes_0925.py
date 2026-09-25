"""Use the authored blue Frost Cruiser beam on Normal and Hard as well as Furious."""
from pathlib import Path

path = Path('assets/game.js')
data = path.read_bytes()
assert b'\r\n' not in data
old = b"  if(b._ship==='frostcruiser'&&XART._touch){XART._touch('fllaser_0');XART._touch('cfx_stage4_chain_lightning');}"
new = b"  if(b._ship==='frostcruiser'&&XART._touch){XART._touch('fllaser_0');XART._touch('cfx_stage4_chain_lightning');XART._touch('frost_furious_beam_0920');}"
assert data.count(old) == 1
data = data.replace(old, new)
old = b"  if(frost&&diffKey==='furious'){\n    const key='frost_furious_beam_0920';if(!XART.rdy(key))return;"
new = b"  if(frost){\n    // The authored blue ice shaft serves every difficulty; the green plate below belongs to the jungle ship.\n    const key='frost_furious_beam_0920';if(!XART.rdy(key))return;"
assert data.count(old) == 1
path.write_bytes(data.replace(old, new))
