module.exports=function testEconomy(vm,ctxv,ok){
  console.log('=== 372. THE SCORE EXCHANGE and THE ARMORY - score -> Furious Points -> Forge levels (0917) ===');
  /* Mike, 0917: "Furious Points are the answer to incentivise playing the game on higher difficulties and
     other pilots, and your Score Points in-game. Yes, the high-score points now become useful instead of
     a show off. You use your high score points to purchase Furious Points. All icons here should get
     their level 1-5 upgrade generated variants, and upgraded projectiles and more. Also, you may only
     equip 1 weapon type of each type."

     Driven on the live screens by probe_armory_0917.py. This section pins the RULES in the vm on a
     fresh profile, and restores the profile after. Source pins strip comments (section 47's trap). */
  var strip=function(s){return String(s).replace(/\/\*[\s\S]*?\*\//g,'').replace(/\/\/.*$/gm,'');};
  var R=function(js){ return vm.runInContext(js,ctxv); };

  /* ---- the numbers ---- */
  ok(R("SCORE_BANK_RATE===1000 && SCORE_BANK_NEW_PILOT===1.5"), '1 FURIOUS PT per 1,000 weighted score; a pilot\'s first banked run pays x1.5');
  ok(R("DIFF_ORDER.every(function(k){ return typeof SCORE_BANK_DIFF[k]==='number'; })"),
     'SCORE_BANK_DIFF has a row for EVERY difficulty (the per-difficulty-table rule of section 366)');
  ok(R("DIFF_ORDER.every(function(k,i){ return i===0 || SCORE_BANK_DIFF[k]>SCORE_BANK_DIFF[DIFF_ORDER[i-1]]; })"),
     'and it rises with the difficulty - harder flies pay more, which is the incentive');
  ok(R("FORGE_LEVEL_COST[2]<FORGE_LEVEL_COST[3] && FORGE_LEVEL_COST[3]<FORGE_LEVEL_COST[4] && FORGE_LEVEL_COST[4]<FORGE_LEVEL_COST[5] && !FORGE_LEVEL_COST[1]"),
     'FORGE_LEVEL_COST prices levels II..V, rising, and level I has no price (it is earned in play)');
  ok(R("INFUSION_MAX===5 && INFUSION_PICKUP_MAX===3"), 'five levels; a field pickup stops at three');

  /* ---- a fresh profile, restored at the end ---- */
  R("var __asSave=achievementState; achievementState=achievementEmpty();");
  ok(R("furiousBalance()===0 && scoreBankCredit()===0 && scoreBankQuote()===0"), 'a fresh profile has no points, no credit, nothing to exchange');
  R("var d1=scoreBankDeposit(100000,'hard','cole');");
  ok(R("d1 && d1.credit===225000 && d1.dm===1.5 && d1.pm===1.5"), 'a 100,000 HARD run on a new pilot banks 225,000 credit (x1.5 difficulty, x1.5 first run on Cole)');
  R("var d2=scoreBankDeposit(100000,'hard','cole');");
  ok(R("d2.credit===150000 && d2.pm===1"), 'the second run on the same pilot pays x1.5 only (no new-pilot bonus)');
  R("var d3=scoreBankDeposit(100000,'furious','yuri');");
  ok(R("d3.credit===300000"), 'a FURIOUS run on a new pilot banks x2 x1.5 = 300,000');
  ok(R("scoreBankCredit()===675000 && scoreBankQuote()===675 && furiousBalance()===0"), 'credit sums, the quote is credit / 1000, and nothing reaches the balance until it is EXCHANGED');
  ok(R("scoreBankDeposit(0,'hard','cole')===null && scoreBankCredit()===675000"), 'a zero score deposits nothing');
  ok(R("scoreBankExchange()===675 && furiousBalance()===675 && scoreBankCredit()===0 && furiousExchanged()===675"),
     'the exchange buys 675 points, the balance follows, and the credit is spent - the ledger entry is what the balance sums');
  ok(R("scoreBankExchange()==='empty'"), 'with nothing left the exchange refuses with a word');
  R("scoreBankDeposit(1500,'normal','cole');");
  ok(R("scoreBankExchange()===1 && scoreBankCredit()===500"), 'credit below one point stays in the bank (1,500 -> 1 point, 500 kept)');

  /* ---- the Armory: levels bought per weapon x element, sequentially ---- */
  ok(R("forgeOwnedLevel('fire',0)===1 && forgeLevelCost('fire',0)===FORGE_LEVEL_COST[2]"), 'nothing owned: INCENDIARY SLUGS is level 1 and the next level costs FORGE_LEVEL_COST[2]');
  ok(R("forgeLevelBuy('fire',0)==='ok' && forgeOwnedLevel('fire',0)===2 && furiousBalance()===676-FORGE_LEVEL_COST[2]"), 'buying level II spends its price and the level is owned');
  ok(R("forgeLevelBuy('fire',0)==='ok' && forgeOwnedLevel('fire',0)===3"), 'level III next');
  ok(R("forgeLevelBuy('fire',0)==='poor' && forgeOwnedLevel('fire',0)===3"), 'level IV is refused as poor when the balance is short, and nothing changes');
  ok(R("forgeOwnedLevel('fire',1)===1 && forgeOwnedLevel('ice',0)===1"), 'the levels are per WEAPON x ELEMENT - NAPALM FAN and CRYO SLUGS are untouched');
  ok(R("forgeLevelBuy('fire',4)==='unknown' && forgeLevelBuy('bogus',0)==='unknown'"), 'a weapon that cannot take an element, or an element that does not exist, is unknown');
  R("scoreBankDeposit(5000000,'insanity','falva'); scoreBankExchange();");
  ok(R("forgeLevelBuy('fire',0)==='ok' && forgeLevelBuy('fire',0)==='ok' && forgeOwnedLevel('fire',0)===5 && forgeLevelBuy('fire',0)==='maxed'"),
     'IV, then V, then maxed');
  ok(R("furiousSpent()===FORGE_LEVEL_COST[2]+FORGE_LEVEL_COST[3]+FORGE_LEVEL_COST[4]+FORGE_LEVEL_COST[5]"), 'what was spent is the sum of the levels owned, at the prices they were bought at');
  /* the profile survives a save/load round trip with the forge levels and the bank intact */
  ok(R("(function(){ var v=achievementNormalize(JSON.parse(JSON.stringify(achievementState))); return v.owned[forgeLevelId('fire',0,5)] && v.owned[forgeLevelId('fire',0,2)].cost===FORGE_LEVEL_COST[2] && v.bank && v.bank.exchanges.length===3 && v.bank.pilots.cole===3; })()"),
     'achievementNormalize keeps the forge levels (by pattern) and the bank with its exchange ledger');

  /* ---- the Forge opens a weapon at its owned level; a pickup never lifts past III ---- */
  R("run.forge={}; run.forgeElems={}; run.forgeCombos=2; run.forgeRespecs=2; run.weapon=0; run.infusion=null; run.ngplus=false; forgeDiscover('fire');");
  ok(R("forgeCombine(0,'fire')==='ok' && run.forge[0].lv===5 && run.infusion && run.infusion.lv===5"), 'combining fire on the machine gun opens it at the OWNED level (V) and the held weapon takes it');
  ok(R("weaponIconKey(0,1)==='micon_forge_fire_0_5'"), 'and the badge is the level-V plate');
  R("infusionGrant('fire');");
  ok(R("run.infusion.lv===5"), 'a fire pickup in the field never lowers a forged V');
  R("run.infusion={elem:'ice',lv:3,hits:0}; infusionGrant('ice');");
  ok(R("run.infusion.lv===3"), 'and a pickup never lifts an element past III - IV and V are the Armory\'s');
  R("run.infusion={elem:'ice',lv:1,hits:0}; infusionGrant('ice');");
  ok(R("run.infusion.lv===2"), 'while below III a pickup still levels as it always did');
  ok(R("infusionLabel('fire',5)==='FIREBURST' && infusionLabel('fire',3)==='FIREBURST'"), 'the named combination keeps its name at IV and V');

  /* ---- one upgrade per weapon TYPE, by construction ---- */
  R("run.forgeCombos=2; forgeDiscover('ice'); forgeCombine(0,'ice');");
  ok(R("Object.keys(run.forge).length===1 && run.forge[0].elem==='ice'"), 'a second element on the same slot REPLACES the first - a slot holds exactly one upgrade');
  ok(R("Object.keys(run.forge).every(function(k){ return FORGE_WEAPONS.indexOf(+k)>=0; })"), 'and every forge key is a weapon slot, so there is one upgrade per weapon type');

  /* ---- the seams ---- */
  ok(/scoreBankDepositRun\(\)/.test(strip(R("String(triggerGameOver)"))) && /scoreBankDepositRun\(\)/.test(strip(R("String(triggerVictory)"))),
     'a run banks its score at BOTH ends - game over and victory');
  R("run._bankedOnce=false; run._banked=null; run.score=12345; var before=scoreBankCredit(); scoreBankDepositRun(); scoreBankDepositRun();");
  ok(R("scoreBankCredit()-before===Math.round(12345*SCORE_BANK_DIFF[diffKey]*(achievementState.bank.pilots[run.pilot]>1?1:1.5))"), 'scoreBankDepositRun deposits ONCE per run, weighted by the live difficulty');
  ok(R("vaultRows()[0].exchange===true && vaultRows()[vaultRows().length-1].armory===true"), 'the VAULT lists the EXCHANGE first and THE ARMORY last');
  ok(R("GS.ARMORY==='armory' && typeof drawArmory==='function' && typeof armoryOpen==='function'"), 'the ARMORY is a state with a draw');
  ok(/case GS\.ARMORY:\s*return drawArmory\(dt\)/.test(strip(R("String(drawScene)"))), 'and drawScene dispatches it');
  ok(/armoryOpen\('forge'\)/.test(strip(R("String(drawForge)"))), 'the Forge opens the Armory (RETINA) and it returns to the Forge');
  ok(/_il>INFUSION_PICKUP_MAX/.test(strip(R("String(updatePlay)"))) && /b\.kind!=='beam'/.test(strip(R("String(updatePlay)"))),
     'above the pickup ceiling the round is scaled at its stamp site, and the reused beam is left alone');
  ok(R("Object.keys(INFUSIONS).every(function(e){ return [0,1,2,3,5,7].every(function(w){ return [2,3,4,5].every(function(l){ return !!XART._src['micon_forge_'+e+'_'+w+'_'+l]; }); }); })"),
     'every level II..V badge is registered for every element x forgeable weapon (216 keys)');
  R("achievementState=__asSave; run.forge={}; run.infusion=null; run._bankedOnce=false; run._banked=null;");
};
