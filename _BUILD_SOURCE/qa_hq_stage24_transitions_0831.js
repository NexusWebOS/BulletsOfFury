const fs = require('fs');
const vm = require('vm');

const src = fs.readFileSync('assets/game.js', 'utf8');
const checks = [];

function ok(name, pass, detail = '') {
  checks.push({ name, pass: !!pass, detail });
  if (!pass) throw new Error(`${name}${detail ? `: ${detail}` : ''}`);
}

function pngInfo(path) {
  const b = fs.readFileSync(path);
  ok(`${path} is a PNG`, b.toString('ascii', 1, 4) === 'PNG');
  return { width: b.readUInt32BE(16), height: b.readUInt32BE(20), colorType: b[25] };
}

const hq = pngInfo('assets/game/cinematic/hq_command_deck_v2.png');
ok('HQ cinematic plate is full-resolution 4:3', hq.width === 1448 && hq.height === 1086,
  `${hq.width}x${hq.height}`);
ok('HQ cinematic plate is registered', /cut_furyhq_command_center[^\n]*hq_command_deck_v2\.png/.test(src));
ok('Decker owns the ensemble centre', /decker:320/.test(src));
ok('Every portrait receives a contour-following black edge', /xartTint\(pk,'#000000',1\)/.test(src));
ok('Dialogue body uses a bright ramp and four-way outline',
  /DIALOGUE_BODY_COLOR='#f7f9ff'/.test(src) &&
  (src.match(/msgText\(_part[^\n]*'#000000'/g) || []).length >= 4 &&
  /msgText\(_part,_cx,_yy,_H,DIALOGUE_BODY_COLOR/.test(src));

ok('Stage 2 miniboss and boss HP floors are raised',
  /const BOSS_HP_FLOOR=\[800,1750,/.test(src) && /const MINIBOSS_HP_FLOOR=\[900,1500,/.test(src));
ok('Stage 2 fire barrier blocks damage before hull routing',
  /function magmaWardBarrierDamage\([\s\S]*?if\(!H\|\|!H\.active\)return false;[\s\S]*?return true;\s*\}/.test(src));
ok('Both Stage 2 ships initialize the persistent fire barrier',
  /kind==='magmaward'\|\|kind==='infernoreaver'/.test(src) && /magmaWardBarrierInit\(b\)/.test(src));
ok('Stage 2 flames use only outboard hardpoints', /holdSlot=\(step&1\)\?'R':'L'/.test(src));

const safeFn = src.match(/function l2FlameSafeLength\(m,ang,want\)\{[\s\S]*?\n\}/);
ok('Stage 2 bottom-safe flame function is present', !!safeFn);
const sandbox = { VH: 480, clamp: (v, a, b) => Math.max(a, Math.min(b, v)), Math };
vm.runInNewContext(`${safeFn[0]}; this.safe = l2FlameSafeLength;`, sandbox);
for (const degrees of [-35, 0, 35]) {
  const a = Math.PI / 2 + degrees * Math.PI / 180;
  const m = { x: 320, y: 120 };
  const len = sandbox.safe(m, a, 340);
  ok(`Stage 2 flame preserves bottom refuge at ${degrees} degrees`,
    m.y + Math.sin(a) * len <= 342.001, `endpoint=${m.y + Math.sin(a) * len}`);
}

for (let i = 0; i < 8; i++) {
  const path = `assets/game/stage4_warfare/s4w_spread_round_${String(i).padStart(2, '0')}.png`;
  const p = pngInfo(path);
  ok(`Stage 4 projectile frame ${i} is normalized transparent 96x96`,
    p.width === 96 && p.height === 96 && p.colorType === 6,
    `${p.width}x${p.height} colorType=${p.colorType}`);
}
ok('Stage 4 miniboss helpers accept shield and hull damage',
  /function stage4MiniDroneDamage/.test(src) && /stage4MiniDroneDamage\(b,d,dmg\)/.test(src));
ok('Stage 4 boss helpers accept damage regardless of carrier shield',
  /function stage4CoreTurretDamage/.test(src) && /shield is[\s\S]*?independent of the carrier/.test(src));
ok('Stage 4 helpers draw blue shield and green hull bars',
  /ctx\.fillStyle='#28a9ff'/.test(src) && /ctx\.fillStyle='#3fe875'/.test(src));
ok('Stage 4 blue spread wall is disabled after helper unlock',
  /coreUnlocked\)return;/.test(src) && (src.match(/stage4CoreBossSpreadTick\(/g) || []).length === 1);

ok('Stage 5 sky crossfades into space during gravity assembly',
  /if\(p==='scatter'\)return \.08\+\.22/.test(src) &&
  /if\(p==='pixelglow'\)return \.60\+\.30/.test(src) &&
  /ctx\.globalAlpha=p\*p\*\(3-2\*p\)/.test(src));
ok('Stage 5 sky travel is lengthened', /SEG_B3\+SEG_B1\+240/.test(src));
ok('Stage 6 launch and gameplay share the same sky sampler',
  /bg6LoopDraw\(im,STAGE6_TRANSITION_SKY,scroll\|\|0,VW,VH,0\)/.test(src));
ok('Stage 6 carries launch scroll directly into gameplay',
  /_stage6SkyScroll=drawLaunch\._bgScroll/.test(src));
ok('Stage 6 bypasses brake and settle pauses',
  /if\(_s6\)\{drawLaunch\._phase='cd'/.test(src));

console.log(JSON.stringify({ pass: true, checks }, null, 2));
