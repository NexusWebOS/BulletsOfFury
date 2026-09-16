module.exports=function testEscapeArrows(vm,ctxv,ok){
  console.log('=== 362. the Stage-4 giant strike: escape arrows, and the beat they flash on (S4-16) ===');
  /* Mike: "Authored left/right escape arrows: flipped pair, flashing with synchronized warning
     sounds for the giant strike." 8ed5f1a8 shipped this unverified and said so; verified in real
     Chromium by probe_escape_0916.py (16/16) - the arrows draw 234 times across a charge, two per
     lit frame, one mirrored, in both safe lanes, in seven bursts.

     ⚠⚠ AND THE SOUND HALF WAS BROKEN, WHICH IS WHY "synchronized" COULD NOT HAVE BEEN TRUE.
     l23WarnSound divides by `B.warm` - the field the beam warns carry - and the giant strike's
     object only had `charge`. NaN propagates: `n` is NaN, `n===B._arrowN` is false FOR EVER
     because NaN equals nothing including itself, and the `n>0` guard that limits the alert to one
     is false too. Measured on the shipped build: 279 alert calls across one five-second charge,
     against a design of ONE. After the fix: one, plus the separate red-phase danger alert. */
  const st=vm.runInContext('stage4GiantStrikeStart.toString()',ctxv).replace(/\/\*[\s\S]*?\*\/|\/\/[^\n]*/g,'');
  ok(/warm\s*:\s*S4_GIANT_STRIKE\.charge/.test(st),
     'the strike carries the `warm` l23WarnSound divides by, from the same number as its charge');

  /* the beep and the arrows must derive from ONE constant, which is what makes them one event */
  const dr=vm.runInContext('stage4GiantStrikeDraw.toString()',ctxv).replace(/\/\*[\s\S]*?\*\/|\/\/[^\n]*/g,'');
  ok(/L23_WARN_ARROWS/.test(dr), 'the arrow flash counts in L23_WARN_ARROWS, the same constant the beep does');
  ok(/warn_escape_arrow_0916/.test(dr), 'it draws the authored escape arrow plate');
  ok(/scale\(-1,1\)/.test(dr), 'the pair is ONE plate, mirrored - two files would be two things to keep in step');
  ok(vm.runInContext("typeof XART!=='undefined'&&!!XART._src['warn_escape_arrow_0916']",ctxv),
     'and that plate is registered');

  /* behavioural: the warn object the strike now builds gives a real arrow index and ONE alert */
  vm.runInContext("var _G362={t:0.10,charge:5,warm:5,released:false,_arrowN:-1,_warnSfx:0};l23WarnSound(_G362);",ctxv);
  ok(vm.runInContext('_G362._arrowN===0',ctxv), 'the first arrow is index 0, not NaN');
  vm.runInContext('var _n362=_G362._arrowN;l23WarnSound(_G362);',ctxv);
  ok(vm.runInContext('_G362._arrowN===_n362',ctxv), 'a second call on the same arrow does not re-fire');
  vm.runInContext('_G362.t=4.90;l23WarnSound(_G362);',ctxv);
  ok(vm.runInContext('_G362._arrowN===6',ctxv), 'the index advances with the charge (6 of 7 at 98%)');

  /* the regression itself: an object with no `warm` is what produced NaN, so prove the shape matters */
  vm.runInContext("var _B362={t:1,charge:5,released:false,_arrowN:-1,_warnSfx:0};l23WarnSound(_B362);",ctxv);
  ok(vm.runInContext('Number.isNaN(_B362._arrowN)',ctxv),
     'a warn object with no `warm` still produces NaN - which is why the field is pinned above');

  /* the strike is Furious-only and leaves the lanes the arrows point into */
  ok(vm.runInContext("/diffKey!=='furious'/.test(stage4GiantStrikeStart.toString())",ctxv),
     'the strike is Furious-only');
  ok(vm.runInContext('S4_GIANT_STRIKE.safeFrac===0.17',ctxv),
     'and it leaves 17% of the camera safe at each edge, which is where the arrows sit');
};
