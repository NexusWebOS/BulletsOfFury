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

  /* ---- the layout (Mike, 0916): "4 large boxes for th weapon icons, 4 rectangle boxes next to
     the large boxes". The page lays out its OWN rows - the debrief's stat bays are thin strips and
     a box the height of one reads as an icon with a border, which is what the first cut shipped. */
  ok(vm.runInContext('typeof UNLOCK_ROWS==="object"&&UNLOCK_ROWS.h>0.30',ctxv),
     'the rows own a tall region of the plate, not a 0.0526 stat bay (h=' +
     vm.runInContext('UNLOCK_ROWS.h',ctxv) + ')');
  const du=vm.runInContext('drawUnlocks.toString()',ctxv).replace(/\/\*[\s\S]*?\*\//g,'').replace(/\/\/.*/g,'');
  ok(/UNLOCK_ROWS/.test(du), 'the draw reads that region');
  /* ⚠ REPOINTED (Mike, 0916: "make it a flexible scrollable section ... show just 1, just 2, just
     3"). This required `i<UNLOCK_MAX` - four sockets drawn whether or not they held a weapon - and
     that is the behaviour he replaced: one unlock is now ONE row. The section draws what it has and
     scrolls past UNLOCK_VIEW. */
  ok(vm.runInContext('UNLOCK_VIEW===4 && UNLOCK_MAX>=UNLOCK_VIEW',ctxv),
     'four rows are VISIBLE and the table may carry more (view ' + vm.runInContext('UNLOCK_VIEW',ctxv) +
     ', cap ' + vm.runInContext('UNLOCK_MAX',ctxv) + ')');
  ok(/k<view/.test(du.replace(/\s+/g,'')) && /U\.scroll/.test(du),
     'it draws only the rows it has, from the scroll offset');
  ok(/RH-pitch\*view/.test(du.replace(/\s+/g,'')),
     'and centres the block, so one unlock is one row in the middle rather than a quarter-height box');
  ok(/scroll:0/.test(vm.runInContext('unlocksStart.toString()',ctxv).replace(/\s+/g,'')),
     'the page starts at the top of its list');
  /* ⚠ menuUp/menuDown CONSUME their tap, so both must be read before either is acted on - the
     trap CLAUDE.md records as `menuLeft()||menuRight()` always resolving to +1. */
  const inp=du.replace(/\s+/g,'');
  ok(/_mUp=\(Input\.menuUp\?/.test(inp) && /_mDn=\(Input\.menuDown\?/.test(inp),
     'up and down are each read exactly once, into locals');
  ok(inp.indexOf('_mDn=(Input.menuDown') < inp.indexOf('if(_maxS>0)'),
     'and both are read BEFORE either is acted on');
  /* the brief fits its bay: stageFitH solves one line's WIDTH, stageWrapCount gives the row count */
  ok(/stageWrapCount/.test(du), 'the stage-clear message is fitted by row COUNT, not just by width');
  ok(/rx2\+rw2\/2-fw\/2\+sw\/2/.test(du.replace(/\s+/g,'')),
     'the name is centred on the whole string, so the typewriter does not walk it sideways');
  ok(!/slots\[i\*2\]/.test(du), 'it no longer borrows the thin stat bays');

  /* ⚠ THIS PIN USED TO REQUIRE `box=rh`, A SQUARE. Mike overruled it in the same breath as
     asking for the plate's own art: "I meant 4 of these like this" - and the piece he cropped is
     1.24:1. Forcing it square would distort an authored bevel, which is what the art rules exist
     to prevent, so the pin now defends the ART's aspect rather than the shape the last cut had.
     (CLAUDE.md: when an assertion fails after a deliberate change, read it before fixing code.) */
  ok(vm.runInContext('typeof UNLOCK_ART==="object"&&UNLOCK_ART.box.length===4&&UNLOCK_ART.strip.length===4',ctxv),
     'the row is built from the plate\'s own box and strip rects');
  const slots=vm.runInContext('JSON.stringify([SC_SLOTS_FULL.rank,SC_SLOTS_FULL.rankword])',ctxv);
  ok(slots===vm.runInContext('JSON.stringify([UNLOCK_ART.box,UNLOCK_ART.strip])',ctxv),
     'and they are the RANK bay and its word strip, so the rows and the debrief cannot disagree');
  ok(/unlockPanel\(pl/.test(du), 'the panels are BLITTED from the plate, not drawn');
  ok(/boxAsp/.test(du) && /rh\*boxAsp/.test(du.replace(/\s+/g,'')),
     'the box is the row height at the authored aspect - large, and never a distorted bevel');
  const up=vm.runInContext('unlockPanel.toString()',ctxv);
  ok(/slice/.test(up) && (up.match(/drawImage/g)||[]).length>=4,
     'the strip is 3-sliced so its rounded caps are not stretched into ovals');
  ok(/globalAlpha=0/.test(du.replace(/\s+/g,'')) && /scale\(sxk,1\)/.test(du.replace(/\s+/g,'')),
     'the icon is STRETCHED to fill the box, its width measured by a draw at alpha 0');
  ok(!/a\*\(r\?1:0\./.test(du.replace(/\s+/g,'')),
     'and every socket is opaque - a dimmed one shows the baked bays through itself');
};
