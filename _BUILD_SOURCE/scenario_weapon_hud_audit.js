/* Temporary audit scene: expose Cole's level-8 HUD/equipment rendering and
   representative pickup tiers without changing production state tables. */
(() => {
  run.pilot = 'cole';
  run.weapon = 0;
  run.wlevels = [8, 0, 0, 0, 0, 0];
  run.wlevel = 8;
  run.missileLevel = 4;
  run.bombs = 7;
  run.shield = 4;
  run.speedLevel = 3;
  enemies = [];
  eBullets = [];
  bullets = [];
  powerups = [
    {kind:'shield', x:55, y:220, vy:0, t:0, bob:0, w:18, h:18},
    {kind:'speed', x:110, y:220, vy:0, t:0, bob:0, w:18, h:18},
    {kind:'weapon', wtype:2, x:170, y:220, vy:0, t:0, bob:0, w:18, h:18},
    {kind:'missilepack2', x:240, y:220, vy:0, t:0, bob:0, w:18, h:18},
    {kind:'missilepack', x:320, y:220, vy:0, t:0, bob:0, w:18, h:18},
    {kind:'missilepack10', x:410, y:220, vy:0, t:0, bob:0, w:18, h:18}
  ];
  player.x = 240;
  player.y = 430;
  player.invuln = 1e9;
  pwTimer = -1e9;
  spTimer = -1e9;
  window.__qaTick = () => {
    enemies = [];
    eBullets = [];
    powerups.forEach((p, i) => {
      p.y = 220;
      p.x = [55, 110, 170, 240, 320, 410][i];
      p.vy = 0;
    });
  };
})();
