#!/usr/bin/env python3
"""
patch_armory_locked_0917.py - the ARMORY says which combinations are still the boss's to give.

`forgeLevelBuy` already refuses an unowned pair with 'locked' (patch_forge_bossdrop_0917). Without
this the screen would refuse it under NOT AVAILABLE and go on printing a price beside it, which is
the shape of a bug rather than a rule: the player would read a number, press FIRE, and be told no.

  - a row for a pair that has not been earned draws DIM, says BOSS DROP, and shows NO price
  - FIRE on it says where the pair comes from, in words, and plays the refusal
  - the tab's own subtitle counts how many of its nine elements are earned, so a player standing on
    the FLAME tab can see there are eight more without walking every row

⚠ THE ROW IS NOT HIDDEN. A combination you have not earned yet is the thing this screen exists to
make you want; hiding it would make the Armory look empty on a fresh profile and teach nothing.
"""
import os
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
p = os.path.join(ROOT, 'assets', 'game.js')
s = open(p, 'rb').read().decode('utf-8')
assert '\r\n' not in s, 'game.js is LF'
if 'r.earned' in s:
    print('already patched'); raise SystemExit(0)

def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, 'anchor found %d times (wanted %d): %r' % (c, n, old[:90])
    s = s.replace(old, new)

# ---- the row carries whether the pair has been earned -------------------------------------------
rep("    return {elem:e,w:w,name:(FORGE_NAMES[e]&&FORGE_NAMES[e][w])||(INFUSIONS[e].name+' '+WEAPONS[w]),lv:lv,cost:forgeLevelCost(e,w),\n"
    "            open:infusionGateOpen(e),gate:INFUSIONS[e].gate||null};\n",
    "    /* `earned` is Mike's 0917 rule on the row: the COMBINATION comes off a boss, the LEVELS are\n"
    "       what this screen sells. A row that has not been earned shows no price, because there is\n"
    "       nothing here to buy for it yet. */\n"
    "    const earned=(typeof forgeComboOwned==='function')?forgeComboOwned(e,w):true;\n"
    "    return {elem:e,w:w,name:(FORGE_NAMES[e]&&FORGE_NAMES[e][w])||(INFUSIONS[e].name+' '+WEAPONS[w]),lv:lv,\n"
    "            cost:earned?forgeLevelCost(e,w):0,earned:earned,\n"
    "            open:infusionGateOpen(e),gate:INFUSIONS[e].gate||null};\n")

# ---- the buy says where a combination comes from --------------------------------------------------
rep("  const res=forgeLevelBuy(r.elem,w);\n",
    "  if(!r.earned){ armorySay('EARN '+String(r.name).toUpperCase()+' FROM A BOSS FIRST'); try{ Audio.SFX.blocked&&Audio.SFX.blocked(); }catch(_ab3){} return 'locked'; }\n"
    "  const res=forgeLevelBuy(r.elem,w);\n")
rep("  else armorySay('NOT AVAILABLE');\n",
    "  else if(res==='locked') armorySay('EARN '+String(r.name).toUpperCase()+' FROM A BOSS FIRST');\n"
    "  else armorySay('NOT AVAILABLE');\n")

# ---- the row draws dim, says BOSS DROP, and prints no price ---------------------------------------
rep("    ctx.save(); ctx.globalAlpha=r.open?1:0.35;\n",
    "    ctx.save(); ctx.globalAlpha=(r.open&&r.earned)?1:0.35;\n")
rep("    const col=!r.open?'#6a7180':(r.lv>=INFUSION_MAX?'#8de23a':(bal>=r.cost?'#ffd24a':'#b06a6a'));\n",
    "    const col=(!r.open||!r.earned)?'#6a7180':(r.lv>=INFUSION_MAX?'#8de23a':(bal>=r.cost?'#ffd24a':'#b06a6a'));\n")
rep("    const sub=!r.open?(r.gate==='ngplus'?'NEW GAME + ONLY':'AFTER STAGE 9'):('LEVEL '+r.lv+(r.lv>=INFUSION_MAX?'  -  MAX':('  -  NEXT: LEVEL '+(r.lv+1))));\n",
    "    const sub=!r.open?(r.gate==='ngplus'?'NEW GAME + ONLY':'AFTER STAGE 9')\n"
    "            : !r.earned?'BOSS DROP'\n"
    "            : ('LEVEL '+r.lv+(r.lv>=INFUSION_MAX?'  -  MAX':('  -  NEXT: LEVEL '+(r.lv+1))));\n")
rep("    if(r.open && r.lv<INFUSION_MAX){ const pt=String(r.cost);\n",
    "    if(r.open && r.earned && r.lv<INFUSION_MAX){ const pt=String(r.cost);\n")

open(p, 'wb').write(s.encode('utf-8'))
print('patched: armory rows show BOSS DROP, no price, and refuse with words')
