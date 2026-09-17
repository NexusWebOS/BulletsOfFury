#!/usr/bin/env python3
"""
patch_fp_per_level_0917.py - Furious Points come from the SCORE, converted at the end of every level.

Mike, 0917, correcting the economy: "These are not to be purchased through the achievement system.
1000 score points is the equivilent of 1 Furious Point for conversion. At the end of each level, your
Maintain your 'Score Points' as a high score record keeper, but at the end of each level, your 'points'
convert into FP = Furious Points. Thats how to make this balanced to start off."

WHAT CHANGES
  - the balance is CONVERTED - SPENT. `achievementPoints()` is no longer a term in it: the awards are a
    record of what you have done, not a currency, and the Armory is not paid out of them.
  - the conversion happens at the END OF EVERY LEVEL, on that level's OWN score (run.score minus the
    stage's scoreStart, plus the second seat in co-op), at a flat 1,000 : 1. It is NOT the whole run and
    NOT at game over.
  - THE SCORE IS NEVER SPENT. It keeps climbing and remains the high-score record - the conversion only
    READS the level's delta. "Maintain your Score Points as a high score record keeper."
  - the remainder CARRIES to the next level rather than evaporating, so two 900-point levels are worth a
    point between them. A conversion that silently drops 90% of a level is not a conversion.
  - the score BANK, its difficulty/new-pilot weighting and the VAULT's manual EXCHANGE row all go: they
    were the run-end design this replaces. `scoreBankDepositRun` leaves triggerGameOver/triggerVictory.

⚠ THE LEDGER IS STILL A LEDGER (0916's rule, unchanged): what has been converted is the SUM of the
per-level entries, never a counter, so the balance cannot disagree with the levels that earned it.

Every edit is anchored on a single line of assets/game.js (LF) and refuses if the anchor is not found
exactly once.
"""
import os
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
p = os.path.join(ROOT, 'assets', 'game.js')
s = open(p, 'rb').read().decode('utf-8')
assert '\r\n' not in s, 'game.js is LF'
if 'FURIOUS_SCORE_RATE' in s:
    print('already patched'); raise SystemExit(0)

def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, 'anchor found %d times (wanted %d): %r' % (c, n, old[:90])
    s = s.replace(old, new)

# ---- 1. the conversion replaces the bank -------------------------------------------------------------
OLD_BANK_START = "const SCORE_BANK_RATE=1000;"
i = s.index(OLD_BANK_START)
j = s.index("function forgeLevelId(elem,w,lv){", i)
NEW = r"""/* 1,000 SCORE = 1 FURIOUS POINT, CONVERTED AT THE END OF EVERY LEVEL (Mike, 0917). Flat: no difficulty
   or pilot weighting in the rate - a harder run earns more because it SCORES more, which is the same
   incentive without a second dial to tune. */
const FURIOUS_SCORE_RATE=1000;
const FORGE_LEVEL_COST=Object.freeze({2:150, 3:300, 4:600, 5:1000});
const FORGE_LEVEL_ID_RE=/^forge_[a-z]+_[0-9]_L[2-9]$/;
function furiousLedger(){ if(!achievementState.fp) achievementState.fp={carry:0,levels:[]}; return achievementState.fp; }
/* the SUM of the per-level entries - never a stored counter (0916's rule) */
function furiousConverted(){ let n=0; const L=achievementState.fp; if(L&&L.levels) for(const e of L.levels) n+=e.fp|0; return n; }
function furiousCarry(){ return (achievementState.fp&&achievementState.fp.carry)|0; }
/* the level's OWN score -> points. The remainder carries; run.score is never touched, because it is the
   high-score record. Returns the entry, or null when the level scored nothing. */
function furiousConvertLevel(stage,score){
  score=Math.max(0,score|0);
  const L=furiousLedger(), pool=(L.carry|0)+score;
  const fp=Math.floor(pool/FURIOUS_SCORE_RATE);
  L.carry=pool-fp*FURIOUS_SCORE_RATE;
  if(!fp && !score) return null;
  const e={stage:stage|0, score:score, fp:fp, at:Date.now()};
  L.levels.push(e); achievementSave();
  return e;
}
/* one conversion per level, whichever end of the stage reaches it first */
function furiousConvertStage(){
  if(!run||run._fpLevelDone) return run?run._fpLevel:null;
  run._fpLevelDone=true;
  let d=(run.score|0)-((stageStats&&stageStats.scoreStart)|0);
  if(typeof coopActive==='function'&&coopActive()&&typeof run2!=='undefined'&&run2)
    d+=(run2.score|0)-((typeof stageStats2!=='undefined'&&stageStats2&&stageStats2.scoreStart)|0);
  run._fpLevel=furiousConvertLevel(run.stage, d);
  return run._fpLevel;
}
"""
s = s[:i] + NEW + s[j:]

# ---- 2. the balance no longer counts achievement points ----------------------------------------------
rep("function furiousBalance(){return achievementPoints()+((typeof furiousExchanged==='function')?furiousExchanged():0)-furiousSpent();}",
    "/* ⚠ ACHIEVEMENT POINTS ARE NOT A CURRENCY (Mike, 0917: \"These are not to be purchased through the\n"
    "   achievement system\"). They stay a record of what has been done and are shown on the gallery; the\n"
    "   spendable balance is what the LEVELS converted, less what has been spent. */\n"
    "function furiousBalance(){return ((typeof furiousConverted==='function')?furiousConverted():0)-furiousSpent();}")

# ---- 3. the store keeps the ledger across a save ------------------------------------------------------
rep("  if(v.bank&&typeof v.bank==='object'){\n",
    "  if(v.fp&&typeof v.fp==='object'){\n"
    "    out.fp={carry:Math.max(0,v.fp.carry|0),levels:[]};\n"
    "    if(Array.isArray(v.fp.levels)) for(const e of v.fp.levels){ if(e&&Number.isFinite(e.fp)) out.fp.levels.push({stage:e.stage|0,score:e.score|0,fp:e.fp|0,at:e.at|0}); }\n"
    "  }\n"
    "  if(v.bank&&typeof v.bank==='object'){\n")
rep("function achievementProfileSnapshot(){return JSON.parse(JSON.stringify({version:achievementState.version,points:achievementPoints(),spent:furiousSpent(),exchanged:(typeof furiousExchanged==='function')?furiousExchanged():0,bank:achievementState.bank||null,",
    "function achievementProfileSnapshot(){return JSON.parse(JSON.stringify({version:achievementState.version,points:achievementPoints(),spent:furiousSpent(),converted:(typeof furiousConverted==='function')?furiousConverted():0,fp:achievementState.fp||null,")

# ---- 4. the level end converts ------------------------------------------------------------------------
rep("  achievementStageComplete(run.stage,stageStats,coop?stageStats2:null);\n",
    "  achievementStageComplete(run.stage,stageStats,coop?stageStats2:null);\n"
    "  if(typeof furiousConvertStage==='function') furiousConvertStage();   /* the level's score becomes FP (0917) */\n")
rep("  stageStats={kills:0,shots:0,hits:0,livesStart:run.lives,scoreStart:run.score,spawned:0,deaths:0,missiles:0,\n",
    "  if(run) run._fpLevelDone=false;   /* a new level may convert again (0917) */\n"
    "  stageStats={kills:0,shots:0,hits:0,livesStart:run.lives,scoreStart:run.score,spawned:0,deaths:0,missiles:0,\n")

# ---- 5. the run-end banking goes ----------------------------------------------------------------------
rep("  if(typeof scoreBankDepositRun==='function') scoreBankDepositRun();   /* the score becomes bank credit (0917) */\n", "")
rep("  if(typeof scoreBankDepositRun==='function') scoreBankDepositRun();\n", "")
rep("  /* the run's score just became bank credit - say so, with the weighting that made it (0917) */\n"
    "  if(run._banked&&run._banked.credit>0){ const B=run._banked; ctx.fillStyle='#8de23a'; ctx.font='bold 9px \"BOFmil\", monospace';\n"
    "    ctx.fillText('BANKED  '+pad(B.credit,8)+'  X'+B.dm+' '+String(B.diff||'').toUpperCase()+(B.pm>1?'  NEW PILOT X'+B.pm:''),VW/2,VH/2+44); }\n", "")

# ---- 6. the VAULT loses its manual exchange row -------------------------------------------------------
rep("  const credit=scoreBankCredit(), fp=scoreBankQuote();\n"
    "  const rows=[{id:'__exchange',exchange:true,name:'EXCHANGE SCORE  -  '+credit+' CREDIT',cost:0,kind:'exchange',owned:false,pending:null,\n"
    "               blurb:fp>0?('BUY '+fp+' FURIOUS PTS AT '+SCORE_BANK_RATE+' CREDIT EACH'):('EVERY RUN BANKS ITS SCORE - HARDER FLIES PAY MORE')}];\n",
    "  /* ⚠ NO EXCHANGE ROW (0917). The conversion is automatic at the end of every level, so there is\n"
    "     nothing here to press - the balance in the sub-header is the whole story. */\n"
    "  const rows=[];\n")
rep("  if(r.exchange){\n"
    "    const fp=scoreBankExchange();\n"
    "    if(fp==='empty'){ vaultSay('NOTHING TO EXCHANGE - FINISH A RUN FIRST'); try{ Audio.SFX.blocked&&Audio.SFX.blocked(); }catch(_ve1){} }\n"
    "    else { vaultSay('+'+fp+' FURIOUS PTS'); try{ Audio.SFX.select&&Audio.SFX.select(); }catch(_ve2){} }\n"
    "    vault.rows=vaultRows(); return fp==='empty'?'empty':'exchange';\n"
    "  }\n", "")
rep("    if(!r.owned && !r.pending && !r.armory){\n      const pt=r.exchange?('+'+scoreBankQuote()):String(r.cost);\n",
    "    if(!r.owned && !r.pending && !r.armory){\n      const pt=String(r.cost);\n")

# ---- 7. the Forge says what the level paid -------------------------------------------------------------
rep("    const l1='COMBINE  X'+(run.forgeCombos|0)+'      RE-SPEC  X'+(run.forgeRespecs|0)+'      LOADOUT  '+load.length+' OF '+FORGE_LOADOUT_MAX;\n",
    "    /* the level's own conversion, said where the player is standing when it happens (0917) */\n"
    "    const _fpL=(run._fpLevel&&run._fpLevel.fp>0)?('      FURIOUS  +'+run._fpLevel.fp):'';\n"
    "    const l1='COMBINE  X'+(run.forgeCombos|0)+'      RE-SPEC  X'+(run.forgeRespecs|0)+'      LOADOUT  '+load.length+' OF '+FORGE_LOADOUT_MAX+_fpL;\n")

open(p, 'wb').write(s.encode('utf-8'))
print('patched: per-level 1000:1 conversion, balance off achievements, bank/exchange removed, forge brief')
