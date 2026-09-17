#!/usr/bin/env python3
"""
patch_forge_perslot_0917.py - the Forge's element list belongs to the SLOT the cursor is on.

A combination is an ELEMENT ON A SLOT (patch_forge_bossdrop_0917). The picker was still offering one
global list for every slot, so FIRE on the machine gun would have listed an element earned for the
LASER and then been refused by forgeCombine with 'locked' - a list that offers what the screen behind
it will not accept. Per slot, the list can only contain what that slot can actually take.

  - `disc` is `forgeElemsFor(selW)` once the cursor's slot is known, and the element strip's "known"
    highlight follows it, so the strip reads as this weapon's roster
  - the strip's caption says EARNED, and the empty-state lines name the BOSS rather than the field
  - forgeCombine's new 'locked' word gets its own sentence, in case any route reaches it

⚠ `disc` HAD TO MOVE BELOW `selW`, WHICH IS WHY THE F.esel CLAMP MOVED WITH IT. Clamping the element
cursor against a list computed before the slot is known is how a cursor ends up pointing past the end
of the list it is actually drawn against.
"""
import os
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
p = os.path.join(ROOT, 'assets', 'game.js')
s = open(p, 'rb').read().decode('utf-8')
assert '\r\n' not in s, 'game.js is LF'
if 'forgeElemsFor(selW)' in s:
    print('already patched'); raise SystemExit(0)

def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, 'anchor found %d times (wanted %d): %r' % (c, n, old[:90])
    s = s.replace(old, new)

rep("  const load=run.loadout||[], disc=forgeDiscovered();\n"
    "  F.sel=clamp(F.sel|0,0,Math.max(0,load.length-1));\n"
    "  F.esel=clamp(F.esel|0,0,Math.max(0,disc.length-1));\n"
    "  const selW=load.length?load[F.sel]:null;\n",
    "  const load=run.loadout||[];\n"
    "  F.sel=clamp(F.sel|0,0,Math.max(0,load.length-1));\n"
    "  const selW=load.length?load[F.sel]:null;\n"
    "  /* ⚠ THE ELEMENTS BELONG TO THE SLOT, NOT TO THE PROFILE (0917). A combination is earned per\n"
    "     element x weapon, so a global list would offer the laser's FIRE on the machine gun and then be\n"
    "     refused by forgeCombine - a list whose contents the screen behind it will not accept. */\n"
    "  const disc=(selW!=null && typeof forgeElemsFor==='function') ? forgeElemsFor(selW) : [];\n"
    "  F.esel=clamp(F.esel|0,0,Math.max(0,disc.length-1));\n")

# the empty states name where a combination comes from
rep("    else if(!disc.length) l2='NO ELEMENTS DISCOVERED YET - COLLECT THEM IN THE FIELD';\n",
    "    else if(!disc.length) l2='NO COMBINATIONS FOR THIS WEAPON YET - THEY DROP FROM BOSSES';\n")
rep("    const so=disc.length ? ('DISCOVERED: '+disc.map(function(e){ return INFUSIONS[e].name; }).join('  -  ')) : 'ELEMENTS APPEAR HERE AS YOU COLLECT THEM';\n",
    "    const so=disc.length ? ('EARNED FOR THIS WEAPON: '+disc.map(function(e){ return INFUSIONS[e].name; }).join('  -  ')) : 'BEAT A BOSS TO EARN A COMBINATION FOR THIS WEAPON';\n")
rep("        else if(!disc.length) forgeSay('MISSILES STAY MISSILES - NO ELEMENTS DISCOVERED YET','blocked');\n",
    "        else if(!disc.length) forgeSay('MISSILES STAY MISSILES - NO COMBINATION EARNED YET','blocked');\n")
rep("          else if(forgeCanTake(w) && !disc.length) forgeSay('NO ELEMENTS DISCOVERED YET','blocked');\n",
    "          else if(forgeCanTake(w) && !disc.length) forgeSay('NO COMBINATION FOR THIS WEAPON YET - BEAT A BOSS','blocked');\n")

# forgeCombine's new word gets a sentence
rep("      const el=disc[F.esel], r=forgeCombine(selW, el);\n",
    "      const el=disc[F.esel], r=forgeCombine(selW, el);\n"
    "      if(r==='locked') forgeSay('THAT COMBINATION HAS NOT BEEN EARNED YET','blocked');\n")

open(p, 'wb').write(s.encode('utf-8'))
print('patched: the Forge lists the elements earned for the slot under the cursor')
