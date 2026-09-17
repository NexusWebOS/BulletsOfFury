#!/usr/bin/env python3
"""repoint_economy_0917.py - section 372 onto Mike's ladder and the boss-drop combinations.

Three of its pins described rules Mike has since replaced, and each is repointed onto what he
actually said rather than worked around:

  FORGE_LEVEL_COST        -> ONE ladder, 1,000 at x1.25 ("scale our new system to start with each
                             upgrade at about 1000 ... goes up by 25%")
  "awards are not a currency" -> the two incomes ADD ("Achievement points are also tied to this")
  forgeDiscover licenses  -> a combination is earned from a boss ("thats how we gain new combinations")
"""
import os
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
p = os.path.join(ROOT, '_BUILD_SOURCE', 'test_economy_0917.cjs')
s = open(p, 'rb').read().decode('utf-8')
nl = '\r\n' if '\r\n' in s else '\n'

def rep(a, b, n=1):
    global s
    a = a.replace('\n', nl); b = b.replace('\n', nl)
    c = s.count(a)
    assert c == n, 'anchor found %d times (wanted %d): %r' % (c, n, a[:80])
    s = s.replace(a, b)

rep('''  ok(R("FORGE_LEVEL_COST[2]<FORGE_LEVEL_COST[3] && FORGE_LEVEL_COST[3]<FORGE_LEVEL_COST[4] && FORGE_LEVEL_COST[4]<FORGE_LEVEL_COST[5] && !FORGE_LEVEL_COST[1]"),
     'FORGE_LEVEL_COST prices levels II..V, rising, and level I has no price');
''', '''  /* Mike, 0917: "scale our new system to start with each upgrade at about 1000. Once you do so, the
     points to unlock your next weapon type or upgrade goes up by 25%. Easy simple scaling." */
  ok(R("FORGE_UPGRADE_BASE===1000 && FORGE_UPGRADE_STEP===1.25 && typeof FORGE_LEVEL_COST==='undefined'"),
     'ONE LADDER from 1,000 at x1.25 - the per-level price table it replaces is gone');
  ok(R("[0,1,2,3,4].map(function(n){return forgeUpgradeCost(n);}).join(',')==='1000,1250,1560,1950,2440'"),
     'and it reads 1000 / 1250 / 1560 / 1950 / 2440 - rounded to the ten so a price reads as a price');
  ok(R("(function(){ for(var n=0;n<8;n++){ var a=forgeUpgradeCost(n), b=forgeUpgradeCost(n+1); if(Math.abs(b/a-1.25)>0.01) return false; } return true; })()"),
     'every rung is within 1 percent of exactly 25 percent more than the one below it');
''')

rep('''  /* ⚠ ACHIEVEMENT POINTS ARE NOT A CURRENCY (Mike: "These are not to be purchased through the
     achievement system"). A profile rich in awards can still buy nothing. */
  R("achievementState.unlocked={run_no_continue:{at:1}};");
  ok(R("achievementPoints()===1000 && furiousBalance()===0"),
     'a profile holding 1,000 ACHIEVEMENT points has a FURIOUS balance of 0 - the awards are a record, not a currency');
  R("achievementState=achievementEmpty();");
''', '''  /* THE POOL IS BOTH INCOMES (Mike, 0917: "Achievement points are also tied to this"). His earlier
     "not ... through the achievement system" is about the SHOP - the awards gallery still sells
     nothing, the Vault and the Armory do. */
  R("achievementState.unlocked={run_no_continue:{at:1}};");
  ok(R("achievementPoints()===1000 && furiousBalance()===1000"),
     'an award pays into the same balance a level converts into - 1,000 points is one first upgrade');
  R("furiousConvertLevel(1, 2000);");
  ok(R("furiousBalance()===1002 && furiousConverted()===2"),
     'and the two incomes ADD: 1,000 from the awards plus 2 from a 2,000-point level');
  R("achievementState=achievementEmpty();");
''')

rep('''  R("achievementState=achievementEmpty(); furiousConvertLevel(1, 676000); run.forge={}; run.forgeElems={}; forgeDiscover('fire'); forgeDiscover('ice');");
  ok(R("furiousBalance()===676"), 'a 676,000-point level is 676 FURIOUS PTS to spend');
  ok(R("forgeOwnedLevel('fire',0)===1 && forgeLevelCost('fire',0)===FORGE_LEVEL_COST[2]"), 'nothing owned: INCENDIARY SLUGS is level 1 and the next level costs FORGE_LEVEL_COST[2]');
  ok(R("forgeLevelBuy('fire',0)==='ok' && forgeOwnedLevel('fire',0)===2 && furiousBalance()===676-FORGE_LEVEL_COST[2]"), 'buying level II spends its price and the level is owned');
  ok(R("forgeLevelBuy('fire',0)==='ok' && forgeOwnedLevel('fire',0)===3"), 'level III next');
  ok(R("forgeLevelBuy('fire',0)==='poor' && forgeOwnedLevel('fire',0)===3"), 'level IV is refused as poor when the balance is short, and nothing changes');
''', '''  R("achievementState=achievementEmpty(); furiousConvertLevel(1, 3600000); run.forge={}; run.forgeElems={};");
  /* [!] THE ARMORY SELLS LEVELS OF COMBINATIONS YOU ALREADY OWN, AND OWNING ONE IS THE BOSS0S JOB
     (Mike, 0917: "you dont unlock all these weapon combination upgrades ... drop from the boss when
     they die at each level"). A level of a pair you cannot use is an undeliverable sale, which is
     the rule the Vault already follows. */
  ok(R("forgeLevelBuy('fire',0)==='locked' && furiousSpent()===0"),
     'a LEVEL of a combination that has not been earned is refused, and takes nothing');
  R("forgeComboGrant('fire',0); forgeComboGrant('ice',0); forgeComboGrant('fire',1);");
  ok(R("furiousBalance()===3600 && forgeUpgradesBought()===0"),
     'the combinations were EARNED, so the balance is untouched and the ladder has not moved');
  ok(R("forgeOwnedLevel('fire',0)===1 && forgeLevelCost('fire',0)===1000"),
     'nothing bought: INCENDIARY SLUGS is level 1 and the next level is the first rung');
  ok(R("forgeLevelBuy('fire',0)==='ok' && forgeOwnedLevel('fire',0)===2 && furiousBalance()===3600-1000"),
     'buying level II spends the rung and the level is owned');
  ok(R("forgeLevelCost('fire',0)===1250 && forgeLevelCost('ice',0)===1250"),
     'and the NEXT price rose 25 percent for EVERY row - one ladder, not one per weapon');
  ok(R("forgeLevelBuy('fire',0)==='ok' && forgeOwnedLevel('fire',0)===3"), 'level III next, at the risen price');
''')

rep('''  ok(R("furiousSpent()===FORGE_LEVEL_COST[2]+FORGE_LEVEL_COST[3]+FORGE_LEVEL_COST[4]+FORGE_LEVEL_COST[5]"), 'what was spent is the sum of the levels owned, at the prices they were bought at');
''', '''  ok(R("furiousSpent()===1000+1250+1560+1950"), 'what was spent is the sum of the RUNGS climbed, at the prices they were bought at');
  /* [!] THE PRICE PAID IS RECORDED PER PURCHASE, which is what makes a moving ladder safe: changing
     the base or the step later may not re-price what an existing profile already bought. */
  ok(R("(function(){ var v=achievementState.owned; return v[forgeLevelId('fire',0,2)].cost===1000 && v[forgeLevelId('fire',0,3)].cost===1250; })()"),
     'each level records the price it actually paid, not the price the ladder is at now');
''')

rep("v.owned[forgeLevelId('fire',0,2)].cost===FORGE_LEVEL_COST[2] &&",
    "v.owned[forgeLevelId('fire',0,2)].cost===1000 &&")

rep('''  R("run.forge={}; run.forgeElems={}; run.forgeCombos=2; run.forgeRespecs=2; run.weapon=0; run.infusion=null; run.ngplus=false; forgeDiscover('fire');");
''', '''  R("run.forge={}; run.forgeElems={}; run.forgeCombos=2; run.forgeRespecs=2; run.weapon=0; run.infusion=null; run.ngplus=false; forgeDiscover('toxic');");
  /* the fire pair was EARNED above; toxic has only been SEEN in the field, which is not the same thing */
  ok(R("forgeCombine(0,'toxic')==='locked'"), 'an element merely seen in the field cannot be welded on');
''')

rep('''  R("run.forgeCombos=2; forgeDiscover('ice'); forgeCombine(0,'ice');");
''', '''  R("run.forgeCombos=2; forgeCombine(0,'ice');");
''')

open(p, 'wb').write(s.encode('utf-8'))
print('section 372 repointed onto the ladder, the shared pool and the boss drop')
