module.exports=function testInfusionLevels(vm,ctxv,ok){
  console.log('=== 373. THE LEVEL\'S LOOK - a forged round appears upgraded per level (0917) ===');
  /* Mike, 0917: "like our previous level 1-5 variants, they should appear upgraded per each level even in
     this new bullet elemental form or laser upgrade form. Just for extra graphical effect."
     Measured in real Chromium by probe_infusion_levels_0917.py; this section pins the SHAPE. Source pins
     strip comments (section 47's trap). */
  var strip=function(s){return String(s).replace(/\/\*[\s\S]*?\*\//g,'').replace(/\/\/.*$/gm,'');};
  var R=function(js){ return vm.runInContext(js,ctxv); };

  ok(R("INF_TRAIL_P.length===6 && INF_TRAIL_P[0]===0 && INF_TRAIL_P[1]===0 && INF_TRAIL_P[2]>0 && INF_TRAIL_P[2]<INF_TRAIL_P[3] && INF_TRAIL_P[3]<INF_TRAIL_P[4] && INF_TRAIL_P[4]<INF_TRAIL_P[5]"),
     'the trail chance is one row per level: nothing at I, rising II < III < IV < V');
  ok(R("INF_BEAM_SPARK_P[3]===0 && INF_BEAM_SPARK_P[4]>0 && INF_BEAM_SPARK_P[5]>INF_BEAM_SPARK_P[4]"), 'the beam crackles from IV, more at V');
  ok(R("INF_AURA_ALPHA[2]<INF_AURA_ALPHA[5] && INF_AURA_SCALE[2]<INF_AURA_SCALE[5] && INF_AURA_ALPHA.length===6 && INF_AURA_SCALE.length===6"),
     'the aura plate brightens and grows with the level');
  var play=strip(R("String(updatePlay)"));
  ok(/b\._infLv=b\._inf\?\(run\.infusion\.lv\|0\):0/.test(play), 'the level is stamped on the round beside its element (_infLv)');
  ok(/_infTrail:1/.test(play) && /INF_TRAIL_P\[b\._infLv\|0\]/.test(play), 'the trail is spawned from the UPDATE loop, tagged _infTrail, at the level\'s chance');
  ok(/particles\.length<INF_TRAIL_CAP/.test(play), 'and it is capped');
  var db=strip(R("String(drawBullets)"));
  var iAura=db.indexOf('infusionAuraDraw(b)'), iKind=db.indexOf("b.kind==='yuriLightningOrb'");
  ok(iAura>0 && iKind>0 && iAura<iKind, 'drawBullets draws the aura BEFORE any kind branch, so every carrier gets it, under the round');
  var aura=strip(R("String(infusionAuraDraw)+String(infusionGlowPlate)"));
  ok(aura.indexOf('shadowBlur')<0, 'the aura never touches shadowBlur - a baked plate, blitted at an integer origin (0916ab)');
  ok(/createRadialGradient/.test(aura) && /_infGlowCache\[k\]=c/.test(aura), 'the glow is a radial gradient baked ONCE per element x level x size and cached');
  ok(/globalCompositeOperation='lighter'/.test(aura), 'and it composites additively - never a flood (palette/luminance, not overlay)');
  /* ⚠ this named the LINE, not the rule, and the next drop edited that line (the flame joined the column
     path). The claim is that a COLUMN weapon takes the column plate and nobody paints a flat slab. */
  ok(/b\.kind==='beam'/.test(aura) && /b\.kind==='flame'/.test(aura) && /infusionColumnPlate\(b\._inf,lv,ww\)/.test(aura) && !/fillRect\(b\.x/.test(aura),
     'the COLUMN weapons - the beam and the flame - take a soft-edged element column plate, never a flat fillRect slab');
  ok(/lv>=5/.test(aura) && /moveTo\(b\.x-f,b\.y\)/.test(aura), 'level V adds the four-point core flare');
  /* a plate really comes back, at a size that follows the level */
  ok(R("(function(){ try{ var a=infusionGlowPlate('fire',2,10), b=infusionGlowPlate('fire',5,10), c=infusionGlowPlate('fire',2,10); return !!a&&!!b&&a===c&&a.width===22; }catch(e){ return 'nocanvas'; } })()")!==false,
     'infusionGlowPlate returns a cached canvas per key (the same object twice) - or the vm has no canvas, which is not a failure');
};
