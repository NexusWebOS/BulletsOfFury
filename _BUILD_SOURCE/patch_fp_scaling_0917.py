#!/usr/bin/env python3
"""
patch_fp_scaling_0917.py - Mike's numbers: what the pool is made of, and what an upgrade costs.

Mike, 0917:
  "Achievement points are also tied to this. It is expected that most players will unlock at least
   1-4 achievements on Level 1 alone ... Collecting items, powerups and special abilities also gives
   you points like 250 each. Somersalting, or barrel rolling before a projectile would've impacted
   you grants you a 'Stylish!' award of 500 points ... Therefore, scale our new system to start with
   each upgrade at about 1000. Once you do so, the points to unlock your next weapon type or upgrade
   goes up by 25%. Easy simple scaling."

WHAT CHANGES

1. THE POOL IS ACHIEVEMENT POINTS PLUS WHAT THE LEVELS CONVERTED. "Achievement points are also tied
   to this" - his earlier "these are not to be purchased through the achievement system" was about
   the SHOP being the Vault and the Armory rather than the awards gallery, and that still holds:
   the gallery sells nothing. It is the income that is shared.
   ⚠ AND HIS OWN ARITHMETIC IS THE CHECK ON THE PRICE. Read off ACHIEVEMENT_DEFS, a first Stage 1
   clear plausibly pays STAGE 1 CLEAR 10 + NO DEATH 200 + MISSILE DISCIPLINE 100 + a HARD BOSS 200
   = 510, or 1,010 with the FURIOUS boss instead - i.e. "1-4 achievements on Level 1 alone" lands
   within a rounding error of one 1,000-point upgrade, which is exactly the pace he describes.

2. ONE GLOBAL COST CURVE, NOT A PER-LEVEL TABLE. The first upgrade is FORGE_UPGRADE_BASE (1,000) and
   every purchase raises the NEXT one by FORGE_UPGRADE_STEP (x1.25): 1,000 / 1,250 / 1,560 / 1,950 /
   2,440 ... The old FORGE_LEVEL_COST priced by which LEVEL was being bought, so buying level II on a
   tenth weapon cost the same 150 as the first - the curve he asked for is about how many upgrades
   you have BOUGHT, not which rung one of them is on.
   ⚠ ROUNDED TO THE NEAREST TEN so the price reads as a price. The exact curve is 1562.5 and 1953.125
   at the third and fourth steps; ten holds the ladder inside 0.2% of x1.25 and keeps every number on
   screen legible, which "easy simple scaling" is asking for.
   ⚠ AND ONLY A PAID PURCHASE ADVANCES IT. A combination earned from a boss is free (his previous
   message), so counting it would make earning one QUIETLY RAISE the price of everything else - a
   reward that charges you. The curve counts what is in `owned` at a price.

3. THE PRICE PAID IS STILL RECORDED PER PURCHASE, which is what makes a moving curve safe: an
   existing profile's spend cannot be re-priced by a later change to the base or the step.

Every edit is anchored on a single line of assets/game.js (LF) and refuses if the anchor is not
found exactly once.
"""
import os
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
p = os.path.join(ROOT, 'assets', 'game.js')
s = open(p, 'rb').read().decode('utf-8')
assert '\r\n' not in s, 'game.js is LF'
if 'FORGE_UPGRADE_BASE' in s:
    print('already patched'); raise SystemExit(0)

def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, 'anchor found %d times (wanted %d): %r' % (c, n, old[:90])
    s = s.replace(old, new)

# ---- 1. the pool ------------------------------------------------------------------------------
rep("/* ⚠ ACHIEVEMENT POINTS ARE NOT A CURRENCY (Mike, 0917: \"These are not to be purchased through the\n"
    "   achievement system\"). They stay a record of what has been done and are shown on the gallery; the\n"
    "   spendable balance is what the LEVELS converted, less what has been spent. */\n"
    "function furiousBalance(){return ((typeof furiousConverted==='function')?furiousConverted():0)-furiousSpent();}",
    "/* THE POOL IS BOTH INCOMES (Mike, 0917: \"Achievement points are also tied to this\"). His earlier\n"
    "   \"these are not to be purchased through the achievement system\" is about the SHOP - the awards\n"
    "   gallery sells nothing, the Vault and the Armory do - and that is unchanged. What an award pays\n"
    "   and what a level converts land in the same balance, and the price ladder is sized against them:\n"
    "   a first Stage 1 clear pays 10 + 200 + 100 + 200 = 510 in awards, or 1,010 with the FURIOUS boss,\n"
    "   against a first upgrade of 1,000. */\n"
    "function furiousBalance(){return achievementPoints()+((typeof furiousConverted==='function')?furiousConverted():0)-furiousSpent();}")

# ---- 2. the curve replaces the table ------------------------------------------------------------
rep("const FORGE_LEVEL_COST=Object.freeze({2:150, 3:300, 4:600, 5:1000});\n",
    "/* ONE LADDER FOR EVERY UPGRADE (Mike, 0917: \"start with each upgrade at about 1000 ... the points\n"
    "   to unlock your next weapon type or upgrade goes up by 25%\"). The price is a function of how many\n"
    "   you have BOUGHT, not of which rung you are buying - so the tenth weapon's level II costs what the\n"
    "   ladder is up to, and never the 150 a per-level table would have charged for ever. */\n"
    "const FORGE_UPGRADE_BASE=1000, FORGE_UPGRADE_STEP=1.25, FORGE_UPGRADE_ROUND=10;\n")

rep("function forgeOwnedLevel(elem,w){ let lv=1; while(lv<INFUSION_MAX && furiousOwned(forgeLevelId(elem,w,lv+1))) lv++; return lv; }\n"
    "function forgeLevelCost(elem,w){ const lv=forgeOwnedLevel(elem,w); return lv>=INFUSION_MAX?0:(FORGE_LEVEL_COST[lv+1]|0); }\n",
    "function forgeOwnedLevel(elem,w){ let lv=1; while(lv<INFUSION_MAX && furiousOwned(forgeLevelId(elem,w,lv+1))) lv++; return lv; }\n"
    "/* ⚠ ONLY A PAID PURCHASE ADVANCES THE LADDER. A combination earned from a boss costs nothing, so\n"
    "   counting it would make a REWARD raise the price of everything else. `cost` is written by\n"
    "   furiousBuy and by nothing else, which is what separates the two. */\n"
    "function forgeUpgradesBought(){ let n=0; const O=achievementState.owned||{};\n"
    "  for(const id of Object.keys(O)) if(FORGE_LEVEL_ID_RE.test(id) && (O[id].cost|0)>0) n++;\n"
    "  return n; }\n"
    "function forgeUpgradeCost(n){\n"
    "  n=(n==null)?forgeUpgradesBought():Math.max(0,n|0);\n"
    "  const raw=FORGE_UPGRADE_BASE*Math.pow(FORGE_UPGRADE_STEP,n);\n"
    "  return Math.round(raw/FORGE_UPGRADE_ROUND)*FORGE_UPGRADE_ROUND;\n"
    "}\n"
    "function forgeLevelCost(elem,w){ const lv=forgeOwnedLevel(elem,w); return lv>=INFUSION_MAX?0:forgeUpgradeCost(); }\n")

rep("  const cost=FORGE_LEVEL_COST[lv+1]|0;",
    "  const cost=forgeUpgradeCost();")

# ---- 3. the header says what the pool and the ladder are ----------------------------------------
rep("   (FORGE_LEVEL_COST). ⚠ It does NOT sell the combinations themselves - those are earned from the boss",
    "   (forgeUpgradeCost, one rising ladder). ⚠ It does NOT sell the combinations themselves - those are earned from the boss")

open(p, 'wb').write(s.encode('utf-8'))
print('patched: balance = awards + converted - spent; one x1.25 upgrade ladder from 1000')
