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
  ok(R("FURIOUS_SCORE_RATE===1000"), '1 FURIOUS PT per 1,000 score - flat, no difficulty or pilot weighting in the rate');
  ok(R("typeof SCORE_BANK_RATE==='undefined' && typeof scoreBankExchange==='undefined'"),
     'the run-end score BANK and its manual EXCHANGE are gone - the conversion is automatic at the end of every level (Mike, 0917)');
  /* Mike, 0917: "scale our new system to start with each upgrade at about 1000. Once you do so, the
     points to unlock your next weapon type or upgrade goes up by 25%. Easy simple scaling." */
  ok(R("FORGE_UPGRADE_BASE===1000 && FORGE_UPGRADE_STEP===1.25 && typeof FORGE_LEVEL_COST==='undefined'"),
     'ONE LADDER from 1,000 at x1.25 - the per-level price table it replaces is gone');
  ok(R("[0,1,2,3,4].map(function(n){return forgeUpgradeCost(n);}).join(',')==='1000,1250,1560,1950,2440'"),
     'and it reads 1000 / 1250 / 1560 / 1950 / 2440 - rounded to the ten so a price reads as a price');
  ok(R("(function(){ for(var n=0;n<8;n++){ var a=forgeUpgradeCost(n), b=forgeUpgradeCost(n+1); if(Math.abs(b/a-1.25)>0.01) return false; } return true; })()"),
     'every rung is within 1 percent of exactly 25 percent more than the one below it');
  ok(R("INFUSION_MAX===5 && INFUSION_PICKUP_MAX===3"), 'five levels; a field pickup stops at three');

  /* ---- a fresh profile, restored at the end ---- */
  R("var __asSave=achievementState; achievementState=achievementEmpty();");
  ok(R("furiousBalance()===0 && furiousConverted()===0 && furiousCarry()===0"), 'a fresh profile has no points and nothing carried');
  /* THE POOL IS BOTH INCOMES (Mike, 0917: "Achievement points are also tied to this"). His earlier
     "not ... through the achievement system" is about the SHOP - the awards gallery still sells
     nothing, the Vault and the Armory do. */
  R("achievementState.unlocked={run_no_continue:{at:1}};");
  ok(R("achievementPoints()===1000 && furiousBalance()===1000"),
     'an award pays into the same balance a level converts into - 1,000 points is one first upgrade');
  R("furiousConvertLevel(1, 2000);");
  ok(R("furiousBalance()===1002 && furiousConverted()===2"),
     'and the two incomes ADD: 1,000 from the awards plus 2 from a 2,000-point level');
  R("achievementState=achievementEmpty();");

  /* ---- the level converts its own score, and the score is never spent ---- */
  R("var e1=furiousConvertLevel(1, 2500);");
  ok(R("e1 && e1.fp===2 && e1.stage===1 && furiousBalance()===2"), 'a 2,500-point level converts to 2 FURIOUS PTS');
  ok(R("furiousCarry()===500"), 'and the 500 remainder CARRIES rather than evaporating');
  R("var e2=furiousConvertLevel(2, 600);");
  ok(R("e2.fp===1 && furiousCarry()===100 && furiousBalance()===3"), 'the carry pays out on the next level: 500 + 600 = 1 more point, 100 kept');
  ok(R("furiousConverted()===3 && achievementState.fp.levels.length===2"),
     'what has been converted is the SUM of the per-level entries, never a stored counter');
  ok(R("(function(){ var v=achievementNormalize(JSON.parse(JSON.stringify(achievementState))); return v.fp.levels.length===2 && v.fp.carry===100; })()"),
     'and the ledger survives a save/load round trip');

  /* ---- the level end is what calls it, on the level's OWN score, once ---- */
  var cs=strip(R("String(computeStageResults)"));
  ok(/furiousConvertStage\(\)/.test(cs), 'the STAGE CLEAR is where the conversion happens - not game over, not victory');
  ok(!/furiousConvert/.test(strip(R("String(triggerGameOver)"))) && !/furiousConvert/.test(strip(R("String(triggerVictory)"))),
     'neither end of the RUN converts anything - that was the design this replaces');
  R("achievementState=achievementEmpty(); run.stage=3; run.score=12000; run._fpLevelDone=false; stageStats.scoreStart=9000; var before=run.score; var l=furiousConvertStage();");
  ok(R("l && l.fp===3 && l.score===3000"), "it converts THIS LEVEL's delta (12,000 - 9,000 = 3,000 -> 3 pts), not the whole run");
  ok(R("run.score===before"), 'and the SCORE ITSELF IS NEVER SPENT - it stays the high-score record');
  ok(R("furiousConvertStage()===l && furiousConverted()===3"), 'a second call in the same level converts nothing twice');
  var bs=strip(R("String(beginStage)"));
  ok(/_fpLevelDone=false/.test(bs), 'and the next level may convert again');

  /* ---- the Armory: levels bought per weapon x element, sequentially ---- */
  /* 676 points is what 676,000 of a level's score converts to - there is no other way in now */
  R("achievementState=achievementEmpty(); furiousConvertLevel(1, 3600000); run.forge={}; run.forgeElems={};");
  /* [!] THE ARMORY SELLS LEVELS OF COMBINATIONS YOU ALREADY OWN, AND OWNING ONE IS THE BOSS DROP
     (Mike, 0917: "you dont unlock all these weapon combination upgrades ... drop from the boss when
     they die at each level"). A level of a pair you cannot use is an undeliverable sale, which is
     the rule the Vault already follows. */
  ok(R("forgeLevelBuy('fire',0)==='locked' && furiousSpent()===0"),
     'a LEVEL of a combination that has not been earned is refused, and takes nothing');
  R("forgeComboGrant('fire',0); forgeComboGrant('ice',0); forgeComboGrant('fire',1);");
  ok(R("furiousBalance()===3600 && forgeUpgradesBought()===0"),
     'the combinations were EARNED, so the balance is untouched and the ladder has not moved');
  ok(R("forgeOwnedLevel('fire',0)===1 && forgeLevelCost('fire',0)===0"),
     'combined weapons expose one form and no tier price');
  ok(R("forgeLevelBuy('fire',0)==='maxed' && forgeOwnedLevel('fire',0)===1 && furiousBalance()===3600"),
     'retired combination tier purchases cannot charge the player');
  ok(R("forgeLevelBuy('fire',99)==='unknown' && forgeLevelBuy('bogus',0)==='unknown'"),
     'invalid recipe purchases still refuse');
  R("achievementState.owned[forgeLevelId('fire',0,2)]={cost:1000};achievementState.owned[forgeLevelId('fire',0,5)]={cost:1950};");
  ok(R("forgeOwnedLevel('fire',0)===1 && furiousSpent()===2950"),
     'old paid-tier receipts remain in the ledger without creating numbered forms');
  ok(R("(function(){var v=achievementNormalize(JSON.parse(JSON.stringify(achievementState)));return v.owned[forgeLevelId('fire',0,2)].cost===1000;})()"),
     'normalizing a legacy profile preserves historical purchases');
  R("run.forge={};run.forgeForms={};run.forgeElems={};run.forgeCombos=2;run.forgeRespecs=2;run.weapon=0;run.infusion=null;run.ngplus=false;forgeDiscover('toxic');");
  ok(R("forgeCombine(0,'toxic')==='ok'"),'a discovered element can be combined once');
  ok(R("forgeCombine(0,'fire')==='ok' && run.forge[0].lv===1 && run.infusion.lv===1"),
     'legacy paid levels do not change the first-level combination');
  ok(R("forgeCombine(0,'fire')==='owned' && run.forgeCombos===0"),
     'duplicate detection applies even after the stage combine allowance is spent');

  /* ---- one upgrade per weapon TYPE, by construction ---- */
  R("run.forgeCombos=2; forgeCombine(0,'ice');");
  ok(R("Object.keys(run.forge).length===1 && run.forge[0].elem==='ice' && run.forgeForms[0].fire && run.forgeForms[0].ice"), 'a second element becomes active while the first crafted form remains selectable');
  ok(R("Object.keys(run.forge).every(function(k){ return FORGE_WEAPONS.indexOf(+k)>=0; })"), 'and every forge key is a weapon slot, so there is one upgrade per weapon type');


  /* ---- where a COMBINATION comes from (Mike, 0917) ---- */
  /* "you dont unlock all these weapon combination upgrades. Your going to make powerup upgrades
     for these new weapon types that drop from the boss when they die at each level, and thats how
     we gain new combinations and such." Driven on the real boss death by probe_bossdrop_0917.py. */
  var bd=strip(R("String(bossDie)"));
  ok(/forgeBossDrop\(/.test(bd), 'every boss death drops a combination - bossDie calls forgeBossDrop');
  ok(/_drawY/.test(bd.slice(Math.max(0,bd.indexOf('forgeBossDrop')-120), bd.indexOf('forgeBossDrop')+160)),
     'at the DRAWN position, not the logical one - a boss y can sit below the playfield');
  R("var __ownC=achievementState.owned; achievementState.owned={}; run.forgeElems={}; run.stage=1;");
  ok(R("forgeComboRoll().elem==='kinetic' && forgeComboRoll().w==null"),
     'the boss roll is the stage element, with no weapon preselected');
  R("forgeComboGrant('fire',0);");
  ok(R("FORGE_WEAPONS.every(function(w){ return forgeComboOwned('fire',w); }) && !forgeComboOwned('ice',0)"),
     'one boss-earned element is licensed on every weapon slot');
  ok(R("achievementState.owned[forgeElementId('fire')].cost===undefined && furiousSpent()===0 && forgeUpgradesBought()===0"),
     'the global element carries NO cost, so a reward cannot read as spending or advance the ladder');
  ok(R("(function(){ var v=achievementNormalize(JSON.parse(JSON.stringify(achievementState))); return !!v.owned[forgeElementId('fire')] && v.owned[forgeElementId('fire')].cost==null; })()"),
     'the global element survives a profile round trip with no cost');
  R("achievementState.owned=__ownC;");

  /* ---- what a pickup and a dodge are worth ---- */
  /* "Collecting items, powerups and special abilities also gives you points like 250 each.
     Somersalting, or barrel rolling before a projectile would've impacted you grants you a
     'Stylish!' award of 500 points" */
  ok(R("PICKUP_SCORE===250 && STYLISH_SCORE===500"), 'a pickup is 250 and a STYLISH dodge is 500');
  ok(/PICKUP_SCORE/.test(strip(R("String(applyPowerup)"))),
     'the pickup is scored inside applyPowerup, which every collection route passes - crate,\n      capsule and missile box reach it from elsewhere and the old award at the touch test missed them');
  /* ⚠ THE ENEMY-BULLET LOOP IS INLINE IN updatePlay, NOT IN updateEffects - the first cut of this
     pin read the wrong function and failed on correct code. And indexOf alone is not enough:
     updatePlay tests player.invuln in several earlier places, so the pin asks that the FIRST
     invuln return AFTER the hook is the one sitting right next to it. */
  var up=strip(R("String(updatePlay)"));
  var _sc=up.indexOf('stylishCheck'), _iv=up.indexOf('player.invuln>0', _sc);
  ok(_sc>=0 && _iv>_sc && (_iv-_sc)<260,
     'stylishCheck runs IN FRONT OF the bullet loop invuln return - a roll spares you by setting invuln, so the round that would have hit is only visible on that side of it');
  ok(/_styl/.test(strip(R("String(stylishAward)"))),
     'the award is flagged on the MANOEUVRE, so it is one per roll and not one per round');
  ok(/worldXformEscape/.test(strip(R("String(stylishDraw)"))),
     'and it is drawn in SCREEN space - a world coordinate would put it off centre on a wide stage');

  /* ---- the seams ---- */
  ok(R("vaultRows().length===furiousShopIds().length+1 && vaultRows()[vaultRows().length-1].armory===true && !vaultRows().some(function(r){return r.exchange;})"),
     'the VAULT has no EXCHANGE row any more - the catalogue, then THE ARMORY');
  ok(R("GS.ARMORY==='armory' && typeof drawArmory==='function' && typeof armoryOpen==='function'"), 'the ARMORY is a state with a draw');
  ok(/case GS\.ARMORY:\s*return drawArmory\(dt\)/.test(strip(R("String(drawScene)"))), 'and drawScene dispatches it');
  ok(/armoryOpen\('forge'\)/.test(strip(R("String(drawForge)"))), 'the Forge opens the Armory (RETINA) and it returns to the Forge');
  ok(/_il>INFUSION_PICKUP_MAX/.test(strip(R("String(updatePlay)"))) && /b\.kind!=='beam'/.test(strip(R("String(updatePlay)"))),
     'above the pickup ceiling the round is scaled at its stamp site, and the reused beam is left alone');
  ok(R("Object.keys(INFUSIONS).every(function(e){ return FORGE_WEAPONS.every(function(w){ return [2,3,4,5].every(function(l){ return !!XART._src['micon_forge_'+e+'_'+w+'_'+l]; }); }); })"),
     'every level II..V badge is registered for EVERY element x forgeable weapon - all nine slots (324 keys of the 405-badge set)');
  R("achievementState=__asSave; run.forge={}; run.infusion=null; run._bankedOnce=false; run._banked=null;");
};
