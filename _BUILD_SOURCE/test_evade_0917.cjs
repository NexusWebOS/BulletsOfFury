module.exports=function testEvade(vm,ctxv,ok){
  console.log('=== 369. incoming-fire evasion for ordinary air units (0917) ===');
  /* Mike, 0917: "continue improving my boss and enemy AI". Driven in real Chromium by
     probe_evade_0917.py (11/0): a stage-2 drone holds its lane on EASY and NORMAL, commits one
     sidestep on INSANITY that STICKS through the live loop, rolls inward at the edge, never as a tank.
     This pins the shape. */
  var strip=function(s){return String(s).replace(/\/\*[\s\S]*?\*\//g,'').replace(/\/\/.*$/gm,'');};
  ok(vm.runInContext("EVADE_DIFF.easy===0&&EVADE_DIFF.normal===0",ctxv),
     'EASY and NORMAL never evade - the stages Mike tuned play exactly as before');
  ok(vm.runInContext("EVADE_DIFF.hard>0&&EVADE_DIFF.furious>EVADE_DIFF.hard&&EVADE_DIFF.insanity>EVADE_DIFF.furious&&EVADE_DIFF.insanity<=1",ctxv),
     'HARD < FURIOUS < INSANITY, a share of threat reads');
  ok(vm.runInContext("Object.keys(DIFFS).every(function(k){return k in EVADE_DIFF;})",ctxv),
     'every difficulty has a row (no fallback-to-normal hole - the INSANITY lesson)');
  var el=strip(vm.runInContext("String(enemyEvadeEligible)",ctxv));
  ok(el.indexOf("_vkind==='tank'")>=0 && el.indexOf('_droid')>=0 && el.indexOf('isSetPiece(')>=0 && el.indexOf('xelite_')>=0 && el.indexOf('isJetEnemy(')>=0,
     'eligible = an air unit that is not a tank, a droid (own evade), an ace (own evade) or a set piece');
  /* the enemy loop that ticks the burn and the poison lives in _newWeaponTick, not updatePlay */
  var loop=strip(vm.runInContext("String(_newWeaponTick)",ctxv));
  ok(loop.indexOf('enemyEvadeTick(e, dt)')>=0 && loop.indexOf('dkBurnTick(e, dt)')>=0, 'ticked from the one enemy loop the burn and poison already use');
  var tk=strip(vm.runInContext("String(enemyEvadeTick)",ctxv));
  ok(/b\.kind==='beam'/.test(tk) && /_child/.test(tk) && /\(b\.vy\|\|0\)<0/.test(tk),
     'a threat is a RISING player round that is not the beam and not a shard');
  ok(/_evCd\s*=\s*rnd\(/.test(tk), 'a read costs a beat whether it commits or not, and a roll ends on a cooldown');

  /* BOSS DENIAL - the same shape on the boss side (probe_bossdeny_0917.py) */
  ok(vm.runInContext("BOSS_DENY_DIFF.easy===0&&BOSS_DENY_DIFF.normal===0&&BOSS_DENY_DIFF.hard>0&&BOSS_DENY_DIFF.insanity>=BOSS_DENY_DIFF.furious",ctxv),
     'boss denial: EASY/NORMAL keep the authored beat; HARD and up pick against the player');
  var at=strip(vm.runInContext("String(shipBossAttack)",ctxv));
  ok((at.match(/bossDenies\(\)/g)||[]).length===3 && /_denied='ember'/.test(at) && /_denied='lance'/.test(at) && /_denied='siege'/.test(at),
     'the ember doorway, the lance safe lane and the siege half are the three denial picks');
  ok(/gap=\(playerLane\(cols\)\+Math\.floor\(cols\/2\)\)%cols/.test(at) && /safe=\(pl\+1\+\(step%2\)\)%3/.test(at),
     'the doorway opens OPPOSITE the player and the safe lane is never the player\'s - the shape of each pattern is untouched');
};
