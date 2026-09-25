"""Switch the Stage 8 intro to its recolored authored four-cell portal sheet."""
from pathlib import Path

path = Path('assets/game.js')
source = path.read_bytes()
assert b'\r\n' not in source
old = b"  for(const k of ['form2_body','form2_cannon_arm','form2_rocket_arm','portal_sheet','robot_takeover_sheet','weapons_sheet','shield_sheet','void_death_sheet','ground_portal_rise_sheet','ground_portal_beam_sheet'])X._src['vile24_'+k]=_vroot+k+'.png';\n"
new = (b"  for(const k of ['form2_body','form2_cannon_arm','form2_rocket_arm','robot_takeover_sheet','weapons_sheet','shield_sheet','void_death_sheet','ground_portal_rise_sheet','ground_portal_beam_sheet'])X._src['vile24_'+k]=_vroot+k+'.png';\n"
       b"  X._src.vile24_portal_sheet=_vroot+'portal_sheet_0925.png';\n")
assert source.count(old) == 1
path.write_bytes(source.replace(old, new))
