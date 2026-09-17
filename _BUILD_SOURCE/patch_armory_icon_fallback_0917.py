#!/usr/bin/env python3
"""
patch_armory_icon_fallback_0917.py - the ARMORY's rows for the three new slots drew NOTHING.

Measured (probe_iconfallback_0917.py, lit pixels through the real iconBlit onto a scratch canvas, so
"the trap missed" and "nothing drew" cannot be confused):

    slot 4  micon_firewall_3      2349 px      micon_forge_fire_4      0
    slot 6  micon_lasermist_3     1759 px      micon_forge_fire_6      0
    slot 8  micon_lightningorb_3  2101 px      micon_forge_fire_8      0

Both of the Armory row's branches build a `micon_forge_*` key, and those plates exist only for the six
slots whose sheets were generated - so every row on the FLAME, MIST and BOLT tabs was a hole, while the
weapon's own tier icon sat there working. That is this file's own "a family referenced by name is not a
family that exists, and the guards hide it", one drop later.

TWO FIXES, BOTH IN ONE PLACE:
  1. weaponIconKey takes `{bare:1}` to skip its forged branch, so the Armory can ask the ONE resolver
     for a weapon's own tier icon instead of rebuilding that logic (Maverick's laser, Freezer's orb and
     the variant families all live in there; a second table would be the two-tables-disagree trap).
  2. the Armory and the Forge warm the LASER MIST's own atlas. micon_lasermist_* is not on nia_icons,
     so iconBlit routes it to laserMistAtlasBlit, which returns null until `bof_laser_mist_weapon_atlas`
     is ready - touching the ICON key starts nothing. Exactly the 0916 unlock-page lesson.
"""
import os
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
p = os.path.join(ROOT, 'assets', 'game.js')
s = open(p, 'rb').read().decode('utf-8')
assert '\r\n' not in s, 'game.js is LF'
if 'opt && opt.bare' in s:
    print('already patched'); raise SystemExit(0)

def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, 'anchor found %d times (wanted %d): %r' % (c, n, old[:90])
    s = s.replace(old, new)

# ---- 1. one resolver, with a way to ask for the BARE weapon ------------------------------------------
rep("  if(typeof forgeEntry==='function'){ const _fe=forgeEntry(w); if(_fe && _fe.elem && XART._src){\n",
    "  /* `{bare:1}` asks for the weapon's OWN tier icon, forge or no forge - the ARMORY needs that for a row\n"
    "     whose element is not the one currently forged on the slot (0917). */\n"
    "  if(!(opt && opt.bare) && typeof forgeEntry==='function'){ const _fe=forgeEntry(w); if(_fe && _fe.elem && XART._src){\n")

# ---- 2. the Armory row falls back to it --------------------------------------------------------------
rep("    const ik='micon_forge_'+r.elem+'_'+w+(r.lv>1?'_'+r.lv:''), ih=rh*0.82, ix=x0+wdt*0.012+ih/2, iy=ry+rh/2;\n"
    "    ctx.save(); ctx.globalAlpha=r.open?1:0.35;\n"
    "    if(typeof iconBlit==='function'){ if(XART.rdy(ik)) iconBlit(ctx,ik,ix,iy,ih,true); else if(XART.rdy('micon_forge_'+r.elem+'_'+w)) iconBlit(ctx,'micon_forge_'+r.elem+'_'+w,ix,iy,ih,true); }\n",
    "    const ik='micon_forge_'+r.elem+'_'+w+(r.lv>1?'_'+r.lv:''), ih=rh*0.82, ix=x0+wdt*0.012+ih/2, iy=ry+rh/2;\n"
    "    ctx.save(); ctx.globalAlpha=r.open?1:0.35;\n"
    "    /* ⚠ THE LAST FALLBACK IS THE WEAPON'S OWN TIER ICON, AND IT IS NOT OPTIONAL. Both branches used to\n"
    "       build a micon_forge_* key, and those plates exist only for the six slots whose sheets were\n"
    "       generated - so every row on the FLAME, MIST and BOLT tabs drew a hole while the weapon's own icon\n"
    "       sat there working (measured: 0 lit px against 2349 / 1759 / 2101). */\n"
    "    if(typeof iconBlit==='function'){\n"
    "      const _bk=(typeof weaponIconKey==='function')?weaponIconKey(w,Math.max(1,Math.min(5,r.lv|0)),{bare:1}):null;\n"
    "      if(XART.rdy(ik)) iconBlit(ctx,ik,ix,iy,ih,true);\n"
    "      else if(XART.rdy('micon_forge_'+r.elem+'_'+w)) iconBlit(ctx,'micon_forge_'+r.elem+'_'+w,ix,iy,ih,true);\n"
    "      else if(_bk) iconBlit(ctx,_bk,ix,iy,ih,true);\n"
    "    }\n")

# ---- 3. both screens warm the mist's own atlas -------------------------------------------------------
rep("    for(const e of Object.keys(INFUSIONS)) for(const w of FORGE_WEAPONS) for(let l=1;l<=INFUSION_MAX;l++) XART.rdy('micon_forge_'+e+'_'+w+(l>1?'_'+l:'')); } }catch(_ao){}\n",
    "    for(const e of Object.keys(INFUSIONS)) for(const w of FORGE_WEAPONS) for(let l=1;l<=INFUSION_MAX;l++) XART.rdy('micon_forge_'+e+'_'+w+(l>1?'_'+l:''));\n"
    "    /* ⚠ micon_lasermist_* IS NOT ON nia_icons - iconBlit routes it to the mist's own atlas, which stays\n"
    "       null until that sheet is warmed. Touching the icon key starts nothing (0916's unlock page). */\n"
    "    for(let l=1;l<=5;l++){ XART.rdy('micon_firewall_'+l); XART.rdy('micon_icebreath_'+l); XART.rdy('micon_lightningorb_'+l); XART.rdy('micon_lasermist_'+l); }\n"
    "    if(typeof laserMistWarm==='function') laserMistWarm(); } }catch(_ao){}\n")
rep("function forgeStart(onDone){\n",
    "function forgeStart(onDone){\n"
    "  /* the loadout can hold the LASER MIST, whose icon needs its own sheet warmed or the box is a hole (0917) */\n"
    "  try{ if(typeof laserMistWarm==='function') laserMistWarm(); for(let _l=1;_l<=5;_l++) XART.rdy('micon_lasermist_'+_l); }catch(_fw){}\n")

open(p, 'wb').write(s.encode('utf-8'))
print('patched: weaponIconKey {bare}, armory row tier-icon fallback, mist atlas warmed on both screens')
