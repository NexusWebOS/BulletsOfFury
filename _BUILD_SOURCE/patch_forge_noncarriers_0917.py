#!/usr/bin/env python3
"""
patch_forge_noncarriers_0917.py - the last three weapon types can be forged too.

Mike, 0917, listing the equip rule: "you may only equip 1 weapon type of each type - I.E 1 machine gun
upgrade type, 1 laser upgrade type, 1 orb upgrade type, 1 spread upgrade, 1 missile upgrade,
1 flamethrower/ice breath/ other types upgrade."

That last clause is the FLAMETHROWER / ICE BREATH (slot 4), LASER MIST (6) and the LIGHTNING ORB (8),
and 0917 listed all three as CANNOT TAKE AN ELEMENT. The reason recorded at INFUSION_CARRIERS was that
their rounds are not carriers - which was read off the KIND table rather than off the code. Measured:

  slot 4  flameFire pushes  {kind:'flame', pierce:true, ...} INTO pBullets, and the bullet loop's own
          flame branch calls hitEnemy with _dmgBullet still set to it - throttled by FLAME_TICK, which
          clears its _hit ledger, so one infusion hit per enemy per tick and not per frame
  slot 6  laserMistTick(b,dt) is called FROM the bullet loop and calls hitEnemy(hit, b.dmg); the round
          dies on its hit, so one infusion hit per lance
  slot 8  yuriLightningOrbTick likewise, through hitOnce, so one per target

So all three already reach `infusionOnHit` through the ONE hook the Forge was built on, and nothing new
is invented for the round - which is the same relationship every other forged weapon has. What they do
NOT get is the palette swap: each has its own authored draw, so the element rides them as the aura, the
trail and the on-hit effect rather than as a recolour. That is stated in the doc rather than hidden.

⚠ THE FLAME IS A COLUMN, NOT A ROUND. Its h is flameReach(lv) - 200+px - so the round aura plate would
size off that and paint a giant blob. It takes the beam's column path instead.
⚠ AND THE STAMP MUST NOT OVERWRITE THE FLAME'S OWN _el. flameFire re-asserts _el every weapon beat, and
elementMultiplier reads it: a flamethrower forged with ICE must stay a FIRE weapon that also chills.

Every edit is anchored on a single line of assets/game.js (LF) and refuses if the anchor is not found
exactly once.
"""
import os
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
p = os.path.join(ROOT, 'assets', 'game.js')
s = open(p, 'rb').read().decode('utf-8')
assert '\r\n' not in s, 'game.js is LF'
if 'FORGE_TAB_NAME' in s:
    print('already patched'); raise SystemExit(0)

def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, 'anchor found %d times (wanted %d): %r' % (c, n, old[:90])
    s = s.replace(old, new)

# ---- 1. the three kinds become carriers ------------------------------------------------------------
rep("const INFUSION_CARRIERS={mg:1,spread:1,beam:1,missile:1,orb:1,shard:1};\n",
    "/* ⚠ READ OFF THE MUZZLES, NOT OFF A MEMORY (0917). The first cut of this table listed six kinds and\n"
    "   the Forge told the player that the flamethrower, laser mist and the lightning orb 'CANNOT TAKE AN\n"
    "   ELEMENT'. All three push real rounds into pBullets and all three damage through hitEnemy while\n"
    "   `_dmgBullet` still names them, so they reach infusionOnHit through the same one hook - the flame on\n"
    "   its FLAME_TICK ledger, the mist and the bolt once per target. Mike's own equip rule names them:\n"
    "   \"1 flamethrower/ice breath/ other types upgrade\". They take the element as the aura, the trail and\n"
    "   the on-hit effect; each has its own authored draw, so none of them takes the palette swap. */\n"
    "const INFUSION_CARRIERS={mg:1,spread:1,beam:1,missile:1,orb:1,shard:1,\n"
    "                         flame:1,lasermist:1,yuriLightningOrb:1,yuriLightningBolt:1};\n")

# ---- 2. the stamp leaves the flame's own element alone ----------------------------------------------
rep("      if(b._inf==='fire') b._el='fire'; else if(b._inf==='ice') b._el='ice';\n",
    "      /* ⚠ NEVER ON THE FLAME: flameFire re-asserts _el every weapon beat and elementMultiplier reads\n"
    "         it, so a FLAMETHROWER forged with ice must stay a fire weapon that also chills (0917). */\n"
    "      if(b.kind!=='flame'){ if(b._inf==='fire') b._el='fire'; else if(b._inf==='ice') b._el='ice'; }\n")

# ---- 3. the flame takes the COLUMN aura, not the round plate -----------------------------------------
rep("  if(b.kind==='beam'){\n    /* the element COLUMN under the authored beam, widening with the level; the authored plate draws over it */\n",
    "  if(b.kind==='beam'||b.kind==='flame'){\n"
    "    /* the element COLUMN under the authored beam or flame, widening with the level; the authored plate\n"
    "       draws over it. ⚠ THE FLAME IS A COLUMN AND ITS h IS flameReach(lv) - 200+px - so the round plate\n"
    "       would size off that and paint a blob the height of the screen (0917). */\n")
rep("    const top=(b.top!=null?b.top:PLAY.y), bot=(b.bot!=null?b.bot:(player.y-14)), bw=Math.max(6,b.w||14);\n",
    "    const top=(b.top!=null?b.top:PLAY.y), bot=(b.bot!=null?b.bot:(player.y-14)), bw=Math.max(6,b.w||14);\n"
    "    if(!(Math.abs(bot-top)>1)) return;\n")

# ---- 4. the three slots become forgeable ------------------------------------------------------------
rep("const FORGE_WEAPONS=Object.freeze([0,1,2,3,5,7]);\n",
    "/* 0917: 4 (flamethrower / ice breath), 6 (laser mist) and 8 (the lightning orb) joined once their\n"
    "   rounds were measured to be carriers - Mike's equip rule names them as an upgrade type of their own. */\n"
    "const FORGE_WEAPONS=Object.freeze([0,1,2,3,4,5,6,7,8]);\n"
    "/* the ARMORY's tab strip gets nine columns now, so a tab wears a SHORT name; the box under the Forge's\n"
    "   own loadout still uses the full one (WEAPONS / weaponDisplayName). */\n"
    "const FORGE_TAB_NAME=Object.freeze({0:'MG',1:'SPREAD',2:'MISSILE',3:'LASER',4:'FLAME',5:'ORB',6:'MIST',7:'CHAIN',8:'BOLT'});\n")

# ---- 5. names for the three new slots (anchored on each row's own gatling entry) ---------------------
NEW = {
 'INFERNO GATLING':  "4:'BLAST FURNACE', 6:'EMBER MIST',  8:'MAGMA SPHERE'",
 'HAIL GATLING':     "4:'ABSOLUTE ZERO', 6:'FROST MIST',  8:'HAIL SPHERE'",
 'STORM GATLING':    "4:'PLASMA JET',    6:'STORM MIST',  8:'TESLA SPHERE'",
 'PRISM GATLING':    "4:'SPECTRUM JET',  6:'PRISM MIST',  8:'PRISM SPHERE'",
 'VENOM GATLING':    "4:'VENOM JET',     6:'BLIGHT MIST', 8:'PLAGUE SPHERE'",
 'HAMMER GATLING':   "4:'PRESSURE JET',  6:'SHOCK MIST',  8:'IMPACT SPHERE'",
 'CHROME GATLING':   "4:'CHROME JET',    6:'MIRROR MIST', 8:'MIRROR SPHERE'",
 'TORRENT GATLING':  "4:'STEAM JET',     6:'TIDAL MIST',  8:'GEYSER SPHERE'",
 'VOID GATLING':     "4:'VOID JET',      6:'VOID MIST',   8:'VOID SPHERE'",
}
for gat, extra in NEW.items():
    rep("7:'%s'}" % gat, "7:'%s', %s}" % (gat, extra))

# ---- 6. the Armory's tabs use the short names --------------------------------------------------------
rep("    if(art){ const lb=String(WEAPONS[FORGE_WEAPONS[i]]||'').toUpperCase();\n",
    "    if(art){ const lb=String(FORGE_TAB_NAME[FORGE_WEAPONS[i]]||WEAPONS[FORGE_WEAPONS[i]]||'').toUpperCase();\n")

open(p, 'wb').write(s.encode('utf-8'))
print('patched: carriers +4, FORGE_WEAPONS 9 slots, names for 4/6/8, flame column aura, armory tabs')
