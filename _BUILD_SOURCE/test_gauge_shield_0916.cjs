module.exports=function testGaugeShield(vm,ctxv,ok){
  console.log('=== 363. the gauges: a centred label, the shield\'s own bar, our own fills (0916) ===');
  /* Mike, 0916: "text in boss bars and min boss bars shold centered all around including
     vertically. Shield should get it's own shield like boss bar, not the same as the boss bar. our
     own custom solid/shield fills too. and Shield should be colored Blue as text."
     Measured in real Chromium by probe_gauge_0916.py (25/0): both labels 0.00px off their socket's
     vertical centre, the SHIELD label reading (137,192,213) against BOSS at (197,176,128), and the
     shield bar drawing its own frame, tab and fill keys in a live Stage-2 fight. */

  /* the socket the label is centred in - measured off the plate, not the plate's own middle */
  ok(vm.runInContext('BMTAB.in && BMTAB.in.dx===5 && BMTAB.in.dy===5 && BMTAB.in.w===194 && BMTAB.in.h===25',ctxv),
     'the tab carries its measured socket (5,5 194x25 of a 204x30 plate)');
  const tab=vm.runInContext('drawBossTab.toString()',ctxv).replace(/\/\*[\s\S]*?\*\/|\/\/[^\n]*/g,'');
  ok(/BMTAB\.in/.test(tab), 'the label is laid out from that socket');
  ok(/lcy\s*=\s*iy\s*\+\s*ih\s*\/\s*2/.test(tab.replace(/\s+/g,' ').replace(/ /g,'')) || /lcy=iy\+ih\/2/.test(tab.replace(/\s+/g,'')),
     'and centred on it vertically - stageText takes the CENTRE of the cap box');
  ok(!/ty\+th\*0\.72/.test(tab), 'the old 0.72-of-the-tab baseline is gone');

  /* blue, and only for the shield */
  ok(vm.runInContext("bmbarTabColour('shield')!==bmbarTabColour('boss')",ctxv), 'the shield label has its own colour');
  const c=vm.runInContext("bmbarTabColour('shield')",ctxv);
  const r=parseInt(c.slice(1,3),16), g=parseInt(c.slice(3,5),16), b=parseInt(c.slice(5,7),16);
  ok(b>r*1.4 && b>=g, 'and it is BLUE (' + c + ')');
  ok(vm.runInContext("bmbarTabLabel('shield')==='SHIELD'&&bmbarTabLabel('boss')==='BOSS'&&bmbarTabLabel('mini')==='MINI BOSS'",ctxv),
     'the three labels are categories, not boss names (0910c stands)');

  /* the shield's OWN bar */
  const sb=vm.runInContext('drawShieldBarArt.toString()',ctxv).replace(/\/\*[\s\S]*?\*\/|\/\/[^\n]*/g,'');
  ok(/bmbar_frame_shield/.test(sb), 'the shield bar prefers its own frame');
  ok(/bmbar_frame_shield_v2/.test(sb)&&!/bmbar_frame_boss/.test(sb)&&/return false/.test(sb),
     'and falls back to the drawn shield gauge while its own v2 plate decodes');
  ok(/bmbar_tab_shield/.test(tab), 'the shield tab is its own plate too');

  /* our own fills */
  ok(vm.runInContext("bmbarShieldFillKey(0.95)==='bmbar_sf2_over'&&bmbarShieldFillKey(0.7)==='bmbar_sf2_hex'"+
                     "&&bmbarShieldFillKey(0.3)==='bmbar_sf2_plasma'&&bmbarShieldFillKey(0.05)==='bmbar_sf2_low'",ctxv),
     'the four shield charge states pick our own fills');
  const bf=vm.runInContext('bmbarFill.toString()',ctxv).replace(/\/\*[\s\S]*?\*\/|\/\/[^\n]*/g,'');
  ok(/bmbar_fill_solid/.test(bf), 'the boss HP bar takes our own SOLID fill');
  ok(/bmbar_fill_seg/.test(bf), 'with the hazard-stripe plate kept as the one-key way back');

  /* the art is registered, at the geometry the draw assumes */
  const cell=(k)=>vm.runInContext("JSON.stringify((typeof BOFX!=='undefined'&&BOFX.cells&&BOFX.cells['"+k+"'])||null)",ctxv);
  ok(/"ui_bossbar",\d+,\d+,700,33/.test(cell('bmbar_frame_shield')), 'bmbar_frame_shield is a 700x33 cell like the bar it replaces');
  ok(/"ui_bossbar",\d+,\d+,204,30/.test(cell('bmbar_tab_shield')), 'bmbar_tab_shield is a 204x30 cell like the other tabs');
  ok(/"ui_bossbar",\d+,\d+,578,13/.test(cell('bmbar_fill_solid')), 'bmbar_fill_solid seats in the same 578x13 well');
  ok(['over','hex','plasma','low'].every(function(n){ return /"ui_bossbar",\d+,\d+,578,13/.test(cell('bmbar_sf2_'+n)); }),
     'and all four shield fills do too');

  /* warmed with the stage - rdy is false on its first call, and that call starts the load */
  const wm=vm.runInContext('bossBarWarm.toString()',ctxv);
  ok(/bmbar_frame_shield/.test(wm)&&/bmbar_tab_shield/.test(wm)&&/bmbar_fill_solid/.test(wm)&&/bmbar_sf2_over/.test(wm),
     'every new plate is warmed with the stage, not first asked for when a shield drops');
};
