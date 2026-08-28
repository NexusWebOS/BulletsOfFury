/* Visual proof: Maverick's normal Level-V laser uses one coherent seven-lance helix plate. */
(() => {
  player.reset();
  player.invuln = 1e9;
  player.x = VW * 0.5;
  player.y = VH * 0.82;
  run.pilot = 'maverick';
  run.weapon = 3;
  run.wlevel = 5;
  run.wlevels[3] = 5;
  pBullets.length = 0;
  enemies.length = 0;
  maverickLaserVolley(5, 4);
})()
