module.exports=function testSonic(vm,ctxv,ok){
  console.log('=== 371. COLE\'S SONIC BOOM - the deadly version (0917) ===');
  /* Mike, 0917: "I also need Cole's Sonic Wave/Boom to be upgraded and feel/sound and work like a
     deadly sonic sound attack."

     Measured in real Chromium by probe_sonic_0917.py (12/0): a FULL release asks for coleSonicFull,
     the wavefront is drawn with rzb_sonic_wave by KEY, the release ring with rzb_sonic_ring, three
     drones in a column each take the full-charge hit and are SHOVED back up the screen. This section
     pins the SHAPE in the vm. Source pins strip comments (section 47's trap). */
  var strip=function(s){return String(s).replace(/\/\*[\s\S]*?\*\//g,'').replace(/\/\/.*$/gm,'');};
  var R=function(js){ return vm.runInContext(js,ctxv); };

  ok(R("SONIC_DMG===11"), 'SONIC_DMG is 11 (was 7): a full charge is 26, a tap 7');
  var rel=strip(R("String(sonicRelease)"));
  ok(/weaponFeedbackSound\(\s*p>=0?\.98\s*\?\s*'coleSonicFull'\s*:\s*'coleSonicHalf'/.test(rel),
     'sonicRelease PLAYS the dedicated cue - coleSonicFull on a full charge, coleSonicHalf otherwise (the old local cue was never called)');
  ok(/colePressureRelease/.test(rel), 'and still plays the pressure-release feedback under it');
  ok(/sonicTrail\.push\(\{[^}]*boom:\s*true/.test(rel), 'the release pushes a BOOM entry on the trail (the ring that grows off the hull)');
  ok(/shake\s*=\s*Math\.max\(\s*shake\s*,\s*4\s*\+\s*p\s*\*\s*11\s*\)/.test(rel), 'the release kicks the camera in proportion to the charge');

  var front=strip(R("String(sonicDrawFront)"));
  ok(/weaponFeedbackArt\(\s*'rzb_sonic_wave'/.test(front), "the wavefront is the Razorback's authored pressure arc, rzb_sonic_wave");
  ok(/Math\.PI\s*,\s*true\s*\)/.test(front), 'rotated to lead upward and drawn additive');
  ok(/nsw_ring_3/.test(front), 'with the old nsw_ring_3 as the fallback while the plate decodes');

  /* the trail draw honours the boom entry with rzb_sonic_ring */
  var src=strip(R("String(typeof sonicTrailDraw==='function'?sonicTrailDraw:function(){})"));
  if(!/rzb_sonic_ring/.test(src)){
    /* the trail is drawn inline; find the owner by the boom test */
    src=strip(R("(function(){ var names=Object.getOwnPropertyNames(this); for(var i=0;i<names.length;i++){ var f=this[names[i]]; if(typeof f==='function'){ var s=String(f); if(s.indexOf('s.boom')>=0 && s.indexOf('rzb_sonic_ring')>=0) return s; } } return ''; }).call(this)"));
  }
  ok(/if\(\s*s\.boom\s*\)/.test(src) && /weaponFeedbackArt\(\s*'rzb_sonic_ring'/.test(src),
     'the trail draw grows rzb_sonic_ring off the hull for a boom entry');

  /* the hit branch shoves ordinary hulls */
  var play=strip(R("String(updatePlay)"));
  ok(/e\.y\s*-=\s*6\s*\+\s*14\s*\*\s*clamp\(\s*b\._p\s*\|\|\s*0\s*,\s*0\s*,\s*1\s*\)/.test(play),
     'a pierced ordinary hull is SHOVED back up the screen, 6 + 14 x charge px');

  /* the cues are registered in the code-owned sound block, with TAME rows */
  ok(R("!!(BOFA&&BOFA.sfx&&/cole_sonic_full\\.wav$/.test(String(BOFA.sfx.coleSonicFull||''))&&/cole_sonic_half\\.wav$/.test(String(BOFA.sfx.coleSonicHalf||'')))"),
     'coleSonicFull / coleSonicHalf point at the generated wavs');
  ok(R("(function(){ try{ var T=Snd.TAME; return !!(T&&T.coleSonicFull&&T.coleSonicFull.min>0&&T.coleSonicHalf&&T.coleSonicHalf.min>0); }catch(_){ return false; } })()"),
     'both carry a TAME row with a retrigger gate (the only gate in the engine)');
  var warm=strip(R("String(typeof warmPilot==='function'?warmPilot:function(){})"));
  ok(/rzb_sonic_wave/.test(R("(function(){ var s=''; var names=Object.getOwnPropertyNames(this); for(var i=0;i<names.length;i++){ var f=this[names[i]]; if(typeof f==='function'){ var t=String(f); if(t.indexOf(\"XART.rdy('rzb_sonic_wave')\")>=0) s+=t; } } return s; }).call(this)")),
     "Cole's warm touches rzb_sonic_wave so the first boom of a run is not drawn through the fallback");
};
