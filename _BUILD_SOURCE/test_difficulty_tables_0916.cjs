module.exports=function testDifficultyTables(vm,ctxv,ok){
  console.log('=== 366. every difficulty has a row in every per-difficulty table ===');
  /* \u26a0 THIS SECTION EXISTS BECAUSE ADDING INSANITY (0916) SILENTLY MADE IT THE EASIEST SETTING
     IN THREE PLACES. `FODDER_DIFF` is read as `FODDER_DIFF[k] || 1`, and DRONE_TELL / DRONE_RECOVER
     both fall back to `.normal` by name - so a difficulty with no row gets NORMAL's numbers, which
     on the hardest setting in the game means softer fodder and LONGER warnings than HARD. Nothing
     throws, nothing logs, and the run simply plays wrong.

     Every one of these is a hand-written map keyed by difficulty, which this file's history says is
     the shape that goes stale: `_selfPat`, the edge-pin exemption list, the enemy-separation list.
     The durable fix is not remembering - it is this assertion. */
  var keys=vm.runInContext("Object.keys(DIFFS)",ctxv);
  var tables=['FODDER_DIFF','DRONE_TELL','DRONE_RECOVER','ARCADE_STOCK','DIFF_META','EVADE_DIFF','BOSS_DENY_DIFF'];
  tables.forEach(function(t){
    var missing=vm.runInContext("Object.keys(DIFFS).filter(function(k){return "+t+"[k]==null;})",ctxv);
    ok(missing.length===0, t+' has a row for every difficulty'+(missing.length?' (missing '+missing.join(',')+')':''));
  });
  ok(keys.indexOf('insanity')>=0,'INSANITY is one of them');

  /* and it is genuinely the hardest, rather than merely the newest */
  ok(vm.runInContext("DIFFS.insanity.ebSpeed>DIFFS.furious.ebSpeed&&DIFFS.insanity.eFire>DIFFS.furious.eFire&&DIFFS.insanity.eHp>DIFFS.furious.eHp&&DIFFS.insanity.density>DIFFS.furious.density",ctxv),
     'INSANITY is harder than FURIOUS on every axis the table carries');
  ok(vm.runInContext("FODDER_DIFF.insanity>FODDER_DIFF.furious&&DRONE_TELL.insanity<DRONE_TELL.furious&&DRONE_RECOVER.insanity<DRONE_RECOVER.furious",ctxv),
     'and in the three tables that used to fall back to NORMAL');
  ok(vm.runInContext("DIFFS.insanity.continues===0&&DIFFS.insanity.startLives===1",ctxv),
     'one life and no continues');

  /* \u26a0 THE RANK LADDER REPLACED AN EQUALITY LADDER THAT LEFT THE TOP WITH NOTHING.
     `diffKey==='furious'` granted an INSANITY boss kill no award at all. */
  ok(vm.runInContext("(function(){var w=diffKey;diffKey='insanity';var r=achievementNormalOrHigher();diffKey=w;return r;})()",ctxv),
     'INSANITY counts as normal-or-higher, so its runs earn stage awards');
  ok(vm.runInContext("difficultyRank('insanity')>difficultyRank('furious')&&difficultyRank('furious')>difficultyRank('hard')",ctxv),
     'and the ranks order the whole ladder');
  /* ⚠ COMMENTS STRIPPED, AND NOT AS A FORMALITY: the note beside this very fix quotes the string
     the assertion looks for ("diffKey==='furious'"), so an unstripped read FAILS on the code that
     is correct. Section 47 recorded this trap and 0906e recorded doing it again. */
  var src=String(vm.runInContext("String(achievementEncounterDefeat)",ctxv))
            .replace(/\/\*[\s\S]*?\*\//g,'').replace(/\/\/.*$/gm,'');
  ok(src.indexOf("difficultyRank")>=0 && src.indexOf("diffKey==='furious'")<0,
     'the boss grant is ranked, not an equality ladder');

  /* the fifth button is bought, never granted, and it is ABSENT rather than disabled */
  ok(vm.runInContext("!!FURIOUS_SHOP.insanity_mode&&FURIOUS_SHOP.insanity_mode.cost>0",ctxv),
     'INSANITY is a shop item with a price');
  ok(vm.runInContext("DIFF_KEYS.indexOf('insanity')>=0&&diffList().indexOf('insanity')<0",ctxv),
     'and until it is bought it is absent from the list the screen walks, not drawn-and-disabled');
  /* Mike, 0916: "Can you also remake our other difficulty options please ... I would like each to
     feature Faces that go from Normal to Under Pressure to Furious to Insanity's Death." All five
     are generated now, and all five ship as LOOSE FILES under _0916 keys - diff_easy..diff_furious
     are CELLS on ui_menu_1, and a cell is checked BEFORE the loose-file cache (0912m), so
     registering under those names would be ignored and the screen would quietly go on drawing the
     old plates with nothing failing. */
  ok(vm.runInContext("Object.keys(DIFF_META).every(function(k){return /_0916$/.test(DIFF_META[k].img);})",ctxv),
     'every difficulty draws its 0916 plate');
  ok(vm.runInContext("Object.keys(DIFF_META).every(function(k){return /diff_0916/.test(String(XART._src[DIFF_META[k].img]||''));})",ctxv),
     'and each is registered as a loose file under a key no atlas cell owns');
  ok(vm.runInContext("Object.keys(DIFF_META).every(function(k){return !(XART.cells&&XART.cells[DIFF_META[k].img]);})",ctxv),
     'with no cell shadowing any of them');

  /* \u26a0 SPENT IS DERIVED FROM WHAT IS OWNED, NEVER STORED. Two numbers describing one fact drift
     the moment anything writes one without the other. */
  ok(vm.runInContext("(function(){var src=String(furiousSpent);return src.indexOf('owned')>=0;})()",ctxv),
     'what has been spent is summed from what is owned');
  ok(vm.runInContext("furiousBalance()===achievementPoints()-furiousSpent()",ctxv),
     'and the balance is earned minus spent by construction');

  /* ---- THE FURIOUS VAULT: the screen that makes any of this reachable (0916) ---- */
  /* ⚠ UNTIL THIS SCREEN EXISTED NOTHING COULD BE BOUGHT AT ALL. The ledger, the prices and the
     INSANITY unlock were all provably correct and a real player could reach none of them, because
     furiousBuy had no caller outside code. A system with no surface is indistinguishable from one
     that was never built - the same hole ACH-02 found in the achievement registry. */
  ok(vm.runInContext("GS.VAULT==='vault'&&typeof drawVault==='function'&&typeof vaultOpen==='function'",ctxv),
     'the vault is a state with a screen');
  ok(vm.runInContext("String(drawScene).indexOf('GS.VAULT')>=0",ctxv),
     'and the dispatcher routes it');
  ok(vm.runInContext("(function(){vaultOpen();return vault.rows.length===furiousShopIds().length;})()",ctxv),
     'it lists every catalogue row, none hidden');

  /* ⚠ A ROW THAT CANNOT DELIVER MUST NOT SELL. Taking the points for a video that does not exist
     is worse than not listing it: the player is out the points with nothing to show, and the refund
     path is exactly the bookkeeping the derived balance exists to avoid. */
  ok(vm.runInContext("Object.keys(FURIOUS_SHOP).filter(function(k){return FURIOUS_SHOP[k].kind==='media';}).length>=4",ctxv),
     'the vault carries the behind-the-scenes rows Mike asked for');
  ok(vm.runInContext("Object.keys(FURIOUS_SHOP).filter(function(k){return FURIOUS_SHOP[k].kind==='media';}).every(function(k){return !furiousSellable(k);})",ctxv),
     'and none of them is sellable while its media is still null');
  ok(vm.runInContext("(function(){var b=furiousBalance();var r=furiousBuy('vault_bof2');return r==='pending'&&furiousBalance()===b;})()",ctxv),
     'buying one is refused as PENDING and costs nothing');
  ok(vm.runInContext("Object.keys(FURIOUS_SHOP).every(function(k){return furiousSellable(k)||!!FURIOUS_SHOP[k].pending;})",ctxv),
     'and every unsellable row carries the line that says what it is waiting for');

  /* ⚠ THE VAULT IS ON ITS OWN BUTTON. Confirm already cycles the FILTER on the gallery, and one
     button doing two jobs is a shape this file has been bitten by more than once. */
  var av=String(vm.runInContext("String(drawAwards)",ctxv)).replace(/\/\*[\s\S]*?\*\//g,'').replace(/\/\/.*$/gm,'');
  ok(av.indexOf('GS.VAULT')>=0 && av.indexOf('keybind.charge')>=0,
     'the gallery opens it on its own button, not on confirm');
};
