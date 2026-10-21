module.exports=function testEscapeArrows(vm,ctxv,ok){
  console.log('=== 362. the Stage-4 giant strike: FOV-only presentation and bounded warning audio ===');
  /* October 15: the FOV replaces the escape-arrow pair. Keep the original
     sound-shape regression: warm and charge must still use the same duration. */
  const st=vm.runInContext('stage4GiantStrikeStart.toString()',ctxv).replace(/\/\*[\s\S]*?\*\/|\/\/[^\n]*/g,'');
  ok(/warm\s*:\s*S4_GIANT_STRIKE\.charge/.test(st),
     'the strike carries the `warm` l23WarnSound divides by, from the same number as its charge');

  /* The native FOV owns the tell; no arrow/sign overlay can return. */
  const dr=vm.runInContext('stage4GiantStrikeDraw.toString()',ctxv).replace(/\/\*[\s\S]*?\*\/|\/\/[^\n]*/g,'');
  ok(/l23FovDraw/.test(dr), 'the strike paints the shared FOV');
  ok(!/warn_escape_arrow_0916/.test(dr), 'the strike does not draw an anchored escape arrow');
  ok(!/bmfx_alert_/.test(dr), 'the strike has no duplicate floating hazard sign');
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
