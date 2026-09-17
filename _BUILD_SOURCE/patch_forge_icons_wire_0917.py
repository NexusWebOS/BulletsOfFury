#!/usr/bin/env python3
"""
patch_forge_icons_wire_0917.py - the forged weapon icons reach every surface through weaponIconKey.

Mike, 0917: "I wanted weapon icons of each type after being upgraded with our element type, generate
those."

Two edits to assets/game.js (LF), each anchored on a single line:
  1. register micon_forge_<elem>_<slot> as loose XART files in the code-owned X._src block (the
     manifest is generated; a cell beats the loose-file cache, and these are NEW keys so nothing
     shadows them);
  2. weaponIconKey returns the forged key when forgeEntry(w) exists - after the space-weapon check
     and BEFORE the chaingun/lasermist branches, so slot 7 (a forgeable carrier) gets it too. With
     or without an opt: a crate for a forged slot dispenses the forged weapon (weaponDisplayName
     already answers the forged name either way), so its icon must agree.
     ⚠ Only when the plate is registered: a forged slot whose sheet never landed keeps its tier icon
     rather than drawing a hole.
"""
import os
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
p = os.path.join(ROOT, 'assets', 'game.js')
s = open(p, 'rb').read().decode('utf-8')
assert '\r\n' not in s, 'game.js is LF'

n1 = "  for(let i=1;i<=5;i++)X._src['micon_chaingun_'+i]=_archRoot+'chaingun_icon_'+i+'.png';\n"
add1 = n1 + ("  /* THE FORGE'S OWN ICONS (0917): one badge per element x forgeable slot, generated against the\n"
             "     authored badge strip (docs/proofs/forge_icons_0917). Loose files under NEW keys - a cell beats\n"
             "     the loose-file cache, so they could not share a tier icon's key. weaponIconKey prefers them\n"
             "     for a forged slot. */\n"
             "  for(const _fe of ['fire','ice','lightning','prism','toxic','kinetic','chrome','water','dark'])\n"
             "    for(const _fs of [0,1,2,3,5,7]) X._src['micon_forge_'+_fe+'_'+_fs]='assets/game/ui/forge_0917/micon_forge_'+_fe+'_'+_fs+'.png';\n")
assert s.count(n1) == 1, 'chaingun icon registration line not found once'
if 'micon_forge_' not in s:
    s = s.replace(n1, add1)

n2 = "  if(typeof spaceWeaponsActive==='function' && spaceWeaponsActive()) return spaceWeaponIconKey();\n  if(w===6)return 'micon_lasermist_'+clamp(lv||1,1,5);\n"
add2 = ("  if(typeof spaceWeaponsActive==='function' && spaceWeaponsActive()) return spaceWeaponIconKey();\n"
        "  /* a FORGED slot wears its element's badge on every surface - the Forge boxes, the HUD, the EQUIPPED\n"
        "     box, the falling crate (0917). Registered-or-nothing: an unregistered plate keeps the tier icon. */\n"
        "  if(typeof forgeEntry==='function'){ const _fe=forgeEntry(w); if(_fe && _fe.elem && XART._src && XART._src['micon_forge_'+_fe.elem+'_'+w]) return 'micon_forge_'+_fe.elem+'_'+w; }\n"
        "  if(w===6)return 'micon_lasermist_'+clamp(lv||1,1,5);\n")
assert s.count(n2) == 1, 'weaponIconKey head not found once'
if "micon_forge_'+_fe.elem" not in s:
    s = s.replace(n2, add2)

open(p, 'wb').write(s.encode('utf-8'))
print('patched: registration + weaponIconKey forge branch')
