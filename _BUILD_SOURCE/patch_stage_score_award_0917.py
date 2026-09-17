#!/usr/bin/env python3
"""patch_stage_score_award_0917.py - the stage-score achievement Mike's income model assumes.

Mike, 0917, listing what a player should plausibly earn on Level 1: "finishing on insanity, hard,
normal, easy, defeating the level without dying and earning a set amount of points thats 75% of what
you could accuimalate if you were to kill all enemies, collect as many items, powerups etc."

That last one did not exist. The registry had STAGE CLEAR, NO DEATH and MISSILE DISCIPLINE and no
score award at all - and his whole "1-4 achievements on Level 1 alone, therefore price an upgrade at
1000" argument rests on it being there.

⚠ THE MAXIMUM IS MEASURED FROM THE STAGE, NEVER HAND-WRITTEN. A table of per-stage score ceilings
would be wrong the day a wave is re-tuned, and wrong silently - the award would quietly become
trivial or impossible. `stageStats.scoreMax` accumulates what the stage actually PUT ON THE FIELD:
every enemy's own score as it spawns, every pickup at PICKUP_SCORE as it appears, and the boss bonus
when the boss dies. So it re-derives itself for any roster, any difficulty and any wave change.

⚠ AND IT IS ACCUMULATED AT `enemies.push`, THE ONE PLACE EVERY SPAWN PATH CONVERGES. `spawnEnemy`
has several exits and a switch that overwrites earlier assignments - this file's first standing rule -
and the drone path increments `spawned` before its object even exists, so the counter beside it is
not a safe hook for anything that needs `e.score`.

⚠ THE SHARE IS A CONSTANT, `STAGE_SCORE_SHARE`, because Mike named 75% and a number nobody can find
is a number nobody can tune.

⚠ AND THE BONUS SCORE THE PLAYER EARNS ON TOP - the kill chain, the STYLISH award - is NOT in the
maximum. It makes the bar easier to clear, which is correct: skilful play should clear it, and a
ceiling that included every bonus would demand a perfect run rather than a thorough one.
"""
import os
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
p = os.path.join(ROOT, 'assets', 'game.js')
s = open(p, 'rb').read().decode('utf-8')
assert '\r\n' not in s, 'game.js is LF'
if 'STAGE_SCORE_SHARE' in s:
    print('already patched'); raise SystemExit(0)

def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, 'anchor found %d times (wanted %d): %r' % (c, n, old[:90])
    s = s.replace(old, new)

# ---- 1. the definitions -------------------------------------------------------------------------
rep("    add('stage_nomissile_'+n,'Stage '+n+' Missile Discipline',100,'BOF_STAGE_'+n+'_NO_MISSILE',{family:'stage_nomissile',stage:n});\n",
    "    add('stage_nomissile_'+n,'Stage '+n+' Missile Discipline',100,'BOF_STAGE_'+n+'_NO_MISSILE',{family:'stage_nomissile',stage:n});\n"
    "    /* Mike, 0917: \"earning a set amount of points thats 75% of what you could accuimalate if you\n"
    "       were to kill all enemies, collect as many items, powerups etc.\" The ceiling is measured from\n"
    "       the stage itself (stageStats.scoreMax), never from a table that a wave re-tune would rot. */\n"
    "    add('stage_score_'+n,'Stage '+n+' Thorough',200,'BOF_STAGE_'+n+'_SCORE',{family:'stage_score',stage:n});\n")

# ---- 2. the ceiling ------------------------------------------------------------------------------
rep("let stageStats={kills:0,shots:0,hits:0,livesStart:3,scoreStart:0,spawned:0,deaths:0,missiles:0,dmgDealt:0,dmgTaken:0,\n",
    "/* WHAT THE STAGE PUT ON THE FIELD (0917) - the denominator of the THOROUGH award. Accumulated as\n"
    "   things appear, so it re-derives itself for any roster, difficulty or wave change. */\n"
    "const STAGE_SCORE_SHARE=0.75;\n"
    "function stageScoreOffer(n){ try{ if(typeof stageStats!=='undefined' && stageStats.scoreMax!=null) stageStats.scoreMax+=Math.max(0,n|0); }catch(_ss){} }\n"
    "let stageStats={kills:0,shots:0,hits:0,livesStart:3,scoreStart:0,spawned:0,deaths:0,missiles:0,dmgDealt:0,dmgTaken:0,scoreMax:0,\n")
rep("let stageStats2={kills:0,shots:0,hits:0,livesStart:3,scoreStart:0,spawned:0,deaths:0,missiles:0,dmgDealt:0,dmgTaken:0, pickups:0,",
    "let stageStats2={kills:0,shots:0,hits:0,livesStart:3,scoreStart:0,spawned:0,deaths:0,missiles:0,dmgDealt:0,dmgTaken:0,scoreMax:0, pickups:0,")
rep("  stageStats={kills:0,shots:0,hits:0,livesStart:run.lives,scoreStart:run.score,spawned:0,deaths:0,missiles:0,\n",
    "  stageStats={kills:0,shots:0,hits:0,livesStart:run.lives,scoreStart:run.score,spawned:0,deaths:0,missiles:0,scoreMax:0,\n")

# ---- 3. every enemy offers its score, at the one place every spawn path converges ------------------
rep("  enemies.push(e);\n  if(typeof stageStats!=='undefined') stageStats.spawned++;\n",
    "  enemies.push(e);\n"
    "  if(typeof stageScoreOffer==='function') stageScoreOffer(e.score||0);\n"
    "  if(typeof stageStats!=='undefined') stageStats.spawned++;\n")
rep("    enemies.push(e);\n",
    "    enemies.push(e);\n"
    "    if(typeof stageScoreOffer==='function') stageScoreOffer(e.score||0);\n")
rep("  enemies.push(c);\n",
    "  enemies.push(c);\n"
    "  if(typeof stageScoreOffer==='function') stageScoreOffer(c.score||0);\n")
rep("      for(const e of e0) enemies.push(e);\n",
    "      for(const e of e0){ enemies.push(e); if(typeof stageScoreOffer==='function') stageScoreOffer(e.score||0); }\n")

# ---- 4. a pickup that appears is points on offer too ---------------------------------------------
rep("  powerups.push({x,y,vy:1.1,t:0,kind,w:18,h:18,bob:rnd(0,TAU)});\n",
    "  powerups.push({x,y,vy:1.1,t:0,kind,w:18,h:18,bob:rnd(0,TAU)});\n"
    "  if(typeof stageScoreOffer==='function' && typeof PICKUP_SCORE==='number') stageScoreOffer(PICKUP_SCORE);\n")

# ---- 5. and the boss's own bonus ------------------------------------------------------------------
rep("  run.score+=5000*run.stage; eBullets.length=0;\n",
    "  run.score+=5000*run.stage;\n"
    "  if(typeof stageScoreOffer==='function') stageScoreOffer(5000*run.stage);   /* the boss bonus is on offer too (0917) */\n"
    "  eBullets.length=0;\n")

# ---- 6. the grant ---------------------------------------------------------------------------------
rep("  if(stats.every(s=>s&&!(s.missiles>0)))grant('stage_nomissile_'+stage);\n",
    "  if(stats.every(s=>s&&!(s.missiles>0)))grant('stage_nomissile_'+stage);\n"
    "  /* THOROUGH: this level's own score against what this level offered (Mike's 75%). The delta is\n"
    "     the same quantity furiousConvertStage converts, and in co-op both seats' work counts toward\n"
    "     one shared profile award - the same rule the other stage rows already follow. */\n"
    "  {\n"
    "    let got=0, offer=0;\n"
    "    if(one){ got+=(run.score|0)-((one.scoreStart)|0); offer+=(one.scoreMax)|0; }\n"
    "    if(two && typeof run2!=='undefined' && run2){ got+=(run2.score|0)-((two.scoreStart)|0); offer+=(two.scoreMax)|0; }\n"
    "    if(offer>0 && got>=offer*STAGE_SCORE_SHARE) grant('stage_score_'+stage);\n"
    "  }\n")

open(p, 'wb').write(s.encode('utf-8'))
print('patched: STAGE THOROUGH at 75% of a ceiling measured from the stage itself')
