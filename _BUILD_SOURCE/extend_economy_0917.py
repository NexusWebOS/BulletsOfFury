#!/usr/bin/env python3
"""extend_economy_0917.py - section 372 gains the boss drop, the 250 pickup and the STYLISH award.

The probes drive these in real Chromium; these are the RULES, pinned where the rest of the economy's
rules live, so a later drop cannot quietly undo one. Two are source pins and say why:

  - stylishCheck must be called IN FRONT OF the loop's `invuln>0` return. That ordering IS the
    measurement ("a round that would have impacted you"), and after the return it can never fire.
  - the award is flagged on the MANOEUVRE object, which is what makes it one per roll rather than one
    per round - a roll through twenty rounds would otherwise pay more than the level converts.

⚠ Source pins strip comments (section 47's trap, self-inflicted twice in this repo): the notes
explaining each fix name the thing being tested.
"""
import os
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
p = os.path.join(ROOT, '_BUILD_SOURCE', 'test_economy_0917.cjs')
s = open(p, 'rb').read().decode('utf-8')
nl = '\r\n' if '\r\n' in s else '\n'
Q = chr(34)
if 'STYLISH_SCORE' in s:
    print('already extended'); raise SystemExit(0)

def rep(a, b, n=1):
    global s
    a = a.replace('\n', nl); b = b.replace('\n', nl)
    c = s.count(a)
    assert c == n, 'anchor found %d times (wanted %d): %r' % (c, n, a[:80])
    s = s.replace(a, b)

BLOCK = (
    '\n'
    '  /* ---- where a COMBINATION comes from (Mike, 0917) ---- */\n'
    '  /* "you dont unlock all these weapon combination upgrades. Your going to make powerup upgrade0s\n'
    '     for these new weapon types that drop from the boss when they die at each level, and thats how\n'
    '     we gain new combinations and such." Driven on the real boss death by probe_bossdrop_0917.py. */\n'
    '  var bd=strip(R(' + Q + 'String(bossDie)' + Q + '));\n'
    '  ok(/forgeBossDrop\\(/.test(bd), '
    "'every boss death drops a combination - bossDie calls forgeBossDrop');\n"
    '  ok(/_drawY/.test(bd.slice(Math.max(0,bd.indexOf(' + "'forgeBossDrop'" + ')-120), bd.indexOf(' + "'forgeBossDrop'" + ')+160)),\n'
    "     'at the DRAWN position, not the logical one - a boss y can sit below the playfield');\n"
    '  R(' + Q + 'var __ownC=achievementState.owned; achievementState.owned={}; run.stage=1;' + Q + ');\n'
    '  ok(R(' + Q + "forgeComboCandidates().length>0 && forgeComboCandidates().every(function(c){ return !forgeComboOwned(c.elem,c.w); })" + Q + '),\n'
    "     'the candidates are pairs the player does NOT own - a boss never hands over what you have');\n"
    '  ok(R(' + Q + "(function(){ var c=forgeComboRoll(); return !!c && !!INFUSIONS[c.elem] && forgeCanTake(c.w); })()" + Q + '),\n'
    "     'and the roll always names a real element on a forgeable slot');\n"
    '  R(' + Q + "forgeComboGrant('fire',0);" + Q + ');\n'
    '  ok(R(' + Q + "forgeComboOwned('fire',0) && !forgeComboOwned('fire',1) && !forgeComboOwned('ice',0)" + Q + '),\n'
    "     'a grant owns exactly ONE pair - a combination is ELEMENT x WEAPON, not an element');\n"
    '  ok(R(' + Q + "achievementState.owned[forgeComboId('fire',0)].cost===undefined && furiousSpent()===0 && forgeUpgradesBought()===0" + Q + '),\n'
    "     'it carries NO cost, so a reward can neither read as spending nor advance the price ladder');\n"
    '  ok(R(' + Q + "(function(){ var v=achievementNormalize(JSON.parse(JSON.stringify(achievementState))); return !!v.owned[forgeComboId('fire',0)] && v.owned[forgeComboId('fire',0)].cost==null; })()" + Q + '),\n'
    "     'and it survives a save/load round trip, still with no cost - which is what PERMANENT means');\n"
    '  R(' + Q + 'achievementState.owned=__ownC;' + Q + ');\n'
    '\n'
    '  /* ---- what a pickup and a dodge are worth ---- */\n'
    '  /* "Collecting items, powerups and special abilities also gives you points like 250 each.\n'
    '     Somersalting, or barrel rolling before a projectile would0ve impacted you grants you a\n'
    "     'Stylish!' award of 500 points\" */\n"
    '  ok(R(' + Q + 'PICKUP_SCORE===250 && STYLISH_SCORE===500' + Q + '), '
    "'a pickup is 250 and a STYLISH dodge is 500');\n"
    '  ok(/PICKUP_SCORE/.test(strip(R(' + Q + 'String(applyPowerup)' + Q + '))),\n'
    "     'the pickup is scored inside applyPowerup, which every collection route passes - crate,\\n"
    "      capsule and missile box reach it from elsewhere and the old award at the touch test missed them');\n"
    '  var ue=strip(R(' + Q + 'String(updateEffects)' + Q + '));\n'
    '  var _sc=ue.indexOf(' + "'stylishCheck'" + '), _iv=ue.indexOf(' + "'player.invuln>0'" + ');\n'
    '  ok(_sc>=0 && _iv>=0 && _sc<_iv,\n'
    "     'stylishCheck runs IN FRONT OF the loop0s invuln return - a roll spares you by setting invuln,\\n"
    "      so the round that would have hit is only visible on that side of it');\n"
    '  ok(/_styl/.test(strip(R(' + Q + 'String(stylishAward)' + Q + '))),\n'
    "     'the award is flagged on the MANOEUVRE, so it is one per roll and not one per round');\n"
    '  ok(/worldXformEscape/.test(strip(R(' + Q + 'String(stylishDraw)' + Q + '))),\n'
    "     'and it is drawn in SCREEN space - a world coordinate would put it off centre on a wide stage');\n"
)

ANCHOR = '  /* ---- the seams ---- */\n'
rep(ANCHOR, BLOCK.replace('0s', chr(39) + 's').replace('0ve', chr(39) + 've') + '\n' + ANCHOR)

open(p, 'wb').write(s.encode('utf-8'))
print('section 372 now pins the boss drop, the 250 pickup and the STYLISH award')
