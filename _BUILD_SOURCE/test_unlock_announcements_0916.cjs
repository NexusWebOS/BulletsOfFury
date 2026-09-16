module.exports=function testUnlockAnnouncements(vm,ctxv,ok){
  console.log('=== 361. the unlock page announces WHERE THE ENGINE GRANTS (0916) ===');
  /* Mike, 0916, answering the open question the resume note left: "announcement should be after
     stage 4 victory yes. The same should apply if you unlock the laser mist on stage 9 if you
     beat the level."

     So SC_UNLOCKS is not free-standing copy - it is keyed to the grant sites in bossDie, and
     these pins fail the day the two drift apart. Driven end to end in real Chromium by
     probe_unlocks_0916.py (26/26, with a busted arm). */
  const bd=vm.runInContext('bossDie.toString()',ctxv).replace(/\/\*[\s\S]*?\*\/|\/\/[^\n]*/g,'');

  /* ---- the grants themselves, read off the engine ---- */
  ok(/run\.stage===4[^;]*yuriLightningOrbGrantStage4/.test(bd),
     'the LIGHTNING ORB is granted on the stage-4 boss kill');
  ok(/run\.stage===9[^;]*laserMistUnlock/.test(bd),
     'LASER MIST is granted on the stage-9 boss kill');
  ok(/run\.stage===5[^;]*chaingunUnlock/.test(bd),
     'the CHAINGUN is granted on the stage-5 hammer kill');

  /* ---- and the announcements follow them, stage for stage ---- */
  const rows=(n,pk)=>vm.runInContext('JSON.stringify(unlockRowsFor('+n+",'"+pk+"'))",ctxv);
  ok(rows(4,'yuri').indexOf('LIGHTNING ORB')>=0, 'stage 4 announces it to Yuri');
  ok(rows(4,'cole')==='[]', 'and to nobody else - the grant needs Yuri in a seat');
  ok(rows(2,'yuri').indexOf('LIGHTNING ORB')<0,
     'stage 2 no longer promises Yuri a weapon he does not receive for two more stages');
  ok(rows(2,'yuri').indexOf('FIRE ORB')>=0, 'his stage-2 fire orb is untouched');
  ok(rows(2,'freezer').indexOf('THERMOSHOCK BALL')>=0, "Freezer's stage-2 row is untouched");
  ok(rows(9,'cole').indexOf('LASER MIST')>=0, 'stage 9 announces laser mist');
  ok(rows(9,'yuri').indexOf('LASER MIST')>=0, 'to every pilot - the flag is account-wide');
  ok(rows(9,'cole').indexOf('micon_lasermist_3')>=0, 'using the laser mist icon family');
  ok(rows(5,'cole').indexOf('CHAINGUN')>=0, 'stage 5 still announces the chaingun');
  ok(rows(3,'cole')==='[]', 'stage 3 still has no row, so no page appears (Mike has not said)');

  /* ---- stage 9 is the BONUS stage, so this page is not the campaign end ---- */
  ok(vm.runInContext('!!(STAGES[8]&&STAGES[8].bonus)&&CAMPAIGN_STAGES===8',ctxv),
     'stage 9 is the bonus stage and the campaign still ends at 8');

  /* ⚠ THE LASER MIST ICON IS NOT ON THE ICON SHEET. iconBlit routes micon_lasermist_* to
     laserMistAtlasBlit, which reads its own atlas, and XART.rdy is false on its FIRST call - so
     the page has to warm that sheet or it draws the name beside a hole, silently. */
  ok(/micon_lasermist[\s\S]{0,120}laserMistAtlasBlit/.test(vm.runInContext('iconBlit.toString()',ctxv)),
     'iconBlit routes the laser mist icon to its own atlas');
  const us=vm.runInContext('unlocksStart.toString()',ctxv);
  ok(/micon_lasermist/.test(us)&&/laserMistWarm/.test(us),
     'and unlocksStart warms that atlas, because touching the icon key starts nothing');
};
