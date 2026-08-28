/* Visual proof: Maverick's charged ball releases complete Level-V helix volleys radially. */
(() => {
  player.reset();
  player.invuln = 1e9;
  run.pilot = 'maverick';
  run.weapon = 3;
  run.wlevel = 5;
  run.wlevels[3] = 5;
  pBullets.length = 0;
  enemies.length = 0;
  helixVolleyQ.length = 0;
  atomFlash = 0;
  helixDetonate({
    x: VW * 0.5,
    y: VH * 0.50,
    lv: 5,
    kind: 'venomx',
    _charged: true,
    _full: true,
    w: 42,
    h: 70
  });
  /* Keep the gameplay readable in proof captures; the production detonation still owns its
     full-screen white flash. */
  atomFlash = 0;
})()
