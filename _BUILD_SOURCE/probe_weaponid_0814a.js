/* ============================================================
   THE WEAPON IDENTITY PROBE (drop 0814a) — Mike's items 1, 2 and 3.

   All three reports are one defect: what a pilot is HOLDING was never recorded, so every
   surface re-derived it from pilot + stage and got an answer that moves. This drives the real
   engine in test_fl.js's vm and asks the questions Mike's sentences ask.

   ⚠ THIS PROVES STATE, NOT PIXELS. CLAUDE.md rule 2. `probe_weaponid_0814a.py` is the pixel
   half — it drives real Chromium and reads the nts_ art off the canvas. A green run here with a
   red run there means the logic is right and the art is not reaching the screen, which is the
   single most common failure shape in this file's history.

       node _BUILD_SOURCE/probe_weaponid_0814a.js
   ============================================================ */
const fs = require('fs');
const path = require('path');

const src = fs.readFileSync(path.join(__dirname, 'test_fl.js'), 'utf8');
const CUT = "const G = sandbox.window.__B;";
const i = src.indexOf(CUT);
if (i < 0) { console.error('probe_weaponid: test_fl.js bootstrap marker moved'); process.exit(2); }

const tail = `
;return { run: (code) => vm.runInContext(code, ctxv) };
`;
const boot = new Function('require', '__dirname', '__filename',
  src.slice(0, i) + tail);
const E = boot(require, __dirname, path.join(__dirname, 'test_fl.js'));

let pass = 0, fail = 0;
function ok(cond, msg, got) {
  if (cond) { pass++; }
  else { fail++; console.log('  FAIL  ' + msg + (got !== undefined ? '   got: ' + JSON.stringify(got) : '')); }
}
function section(n) { console.log('\n== ' + n + ' =='); }

/* put the engine in a known state: a live run, a chosen pilot, a chosen stage, a held variant */
function setup(pilot, stage, slot, variant, level) {
  E.run(`
    run.mode='arcade'; run.pilot=${JSON.stringify(pilot)}; run.stage=${stage};
    run._dbgIce=false; run._dbgFire=false; run._dbgFrzOrb=false;
    run.wlevels=[0,0,0,0,0,0]; run.wvars=[null,null,null,null,null,null];
    run.weapon=${slot}; run.wlevels[${slot}]=${level || 3}; run.wlevel=${level || 3};
    ${variant ? `run.wvars[${slot}]=${JSON.stringify(variant)};` : ''}
    pBullets.length=0; particles.length=0;
  `);
}

// ---------------------------------------------------------------- item 1
section('ITEM 1 — the flamethrower and the ice breath are two attacks');

setup('freezer', 2, 4, 'flamethrower');
ok(E.run('flameIsIce()') === false, 'freezer holding a FLAMETHROWER does not breathe ice', E.run('flameIsIce()'));
ok(E.run("attackElement('flame')") === 'fire', "...and its element is fire", E.run("attackElement('flame')"));
ok(E.run("weaponIconKey(4,3)") === 'micon_firewall_3', '...and it wears the flamethrower icon', E.run('weaponIconKey(4,3)'));
ok(E.run("weaponDisplayName(4)") === 'FLAMETHROWER', '...and it is announced as FLAMETHROWER', E.run('weaponDisplayName(4)'));

setup('freezer', 2, 4, 'icebreath');
ok(E.run('flameIsIce()') === true, 'freezer holding ICE BREATH does breathe ice');
ok(E.run("attackElement('flame')") === 'ice', '...and its element is ice');
ok(E.run("weaponIconKey(4,3)") === 'micon_icebreath_3', '...and it wears the ice breath icon', E.run('weaponIconKey(4,3)'));
ok(E.run("weaponDisplayName(4)") === 'ICE BREATH', '...and it is announced as ICE BREATH');

/* "ice breath is exclusive to Freezer from level 2 onward" — both halves, every stage */
let leak = [], early = [];
for (let st = 1; st <= 9; st++) {
  for (const p of ['cole', 'lizzie', 'decker', 'axel', 'yuri', 'falva', 'maverick', 'juggernaut']) {
    E.run(`run.pilot=${JSON.stringify(p)}; run.stage=${st};`);
    // 200 rolls, because the stage 4+ arm is a coin
    for (let k = 0; k < 200; k++) if (E.run('weaponVariant(4)') === 'icebreath') { leak.push(p + '@' + st); k = 999; }
  }
  E.run(`run.pilot='freezer'; run.stage=${st};`);
  const seen = new Set();
  for (let k = 0; k < 200; k++) seen.add(E.run('weaponVariant(4)'));
  if (st <= 1 && seen.has('icebreath')) early.push(st);
  if (st === 2 && !seen.has('icebreath')) early.push('2-missing');
  if (st >= 4 && !seen.has('icebreath')) early.push(st + '-missing');
}
ok(leak.length === 0, 'no pilot but Freezer can EVER be dispensed ice breath, 9 stages x 8 pilots x 200 rolls', leak.slice(0, 5));
ok(early.length === 0, 'Freezer gets it from stage 2 onward and never before', early);

E.run("run.pilot='freezer'; run.stage=3;");
ok(E.run('weaponVariant(4)') === 'flamethrower',
  'stage 3 withholds ICE BREATH but still gives him the SLOT (it used to return null)', E.run('weaponVariant(4)'));

// ---------------------------------------------------------------- item 2
section('ITEM 2 — the orbs stop swapping');

setup('cole', 3, 5, 'fireorb');
const iconOnL3 = E.run('weaponIconKey(5,3)');
const fireOnL3 = E.run('orbIsFire()');
E.run('run.stage=4;');                       // carry it off the ice level
ok(E.run('weaponIconKey(5,3)') === iconOnL3,
  'a FIRE ORB carried off stage 3 keeps its icon', [iconOnL3, E.run('weaponIconKey(5,3)')]);
ok(E.run('orbIsFire()') === fireOnL3 && fireOnL3 === true,
  '...and keeps firing fire', [fireOnL3, E.run('orbIsFire()')]);

setup('cole', 4, 5, 'iceorb');
E.run('run.stage=3;');                       // carry an ice orb ONTO the ice level
ok(E.run('orbIsFire()') === false, 'an ICE ORB carried onto stage 3 is still an ice orb');
ok(E.run('weaponIconKey(5,3)') === 'micon_iceorb_3', '...and still wears the ice orb icon', E.run('weaponIconKey(5,3)'));

/* the flicker: the same pickup asked 240 times must answer identically */
E.run("run.pilot='freezer'; run.stage=5;");
const keys = new Set();
for (let k = 0; k < 240; k++) keys.add(E.run("weaponIconKey(4,3,{fixed:'icebreath'})"));
ok(keys.size === 1, 'a crate with a baked variant answers ONE icon over 240 frames', [...keys]);
const loose = new Set();
for (let k = 0; k < 240; k++) loose.add(E.run('weaponVariant(4)'));
ok(loose.size > 1, '...and the dispenser rule genuinely does re-roll, which is what made it flicker', [...loose]);

// ---------------------------------------------------------------- item 3
section('ITEM 3 — the fire-ice orb is its own weapon');

setup('freezer', 4, 5, 'fireice');
ok(E.run('orbIsFireIce()') === true, 'freezer holding FIREICE reports fireice');
ok(E.run("attackElement('orb')") === 'fireice', '...its element is fireice, not fire', E.run("attackElement('orb')"));
ok(E.run("weaponIconKey(5,3)") === 'micon_thermoshock_3', '...and it wears the thermoshock icon');
ok(E.run("weaponDisplayName(5)") === 'FIRE-ICE ORB', '...and is announced as FIRE-ICE ORB');

E.run('pBullets.length=0; pShoot();');
const orb = E.run("JSON.stringify(pBullets.filter(b=>b.kind==='orb').map(b=>({ts:b._ts})))");
ok(JSON.parse(orb).length === 1 && JSON.parse(orb)[0].ts === 1,
  'firing it puts a THERMOSHOCK orb in pBullets, not a plain one', orb);

E.run('pBullets.length=0; launchFireball(FRZ_ORB_FULL);');
const ball = JSON.parse(E.run("JSON.stringify(pBullets.map(b=>({k:b.kind,ts:b._ts,rays:b._rays})))"));
ok(ball.length === 1 && ball[0].ts === 1, 'a full charge launches the thermoshock ball, not a basic fireorb', ball);
ok(ball[0].rays === 8, '...and it still carries Mike\'s eight-way discharge', ball);

/* the rays alternate fire and ice — that is what the four+four shard plates are for.

   ⚠ TWO PROBE FAULTS HERE, BOTH MINE, BOTH WORTH KEEPING.
   1. THE BULLET LOOP IS INLINE IN `updatePlay`. `updateBullets` is not a name in this engine
      and calling it threw, so the ball has to be flown by the real update over a live stage.
   2. AND READING THE SURVIVORS AT THE END MEASURES NOTHING. The discharge takes 8 x 0.3s and
      then the ball detonates and every ray leaves the screen, so at frame 200 `pBullets` is
      correctly EMPTY — my first cut read that as "no rays fired". Rays are ACCUMULATED as they
      appear instead, which is the quantity under test. */
E.run(`
  ASSETS.ready=true; run.stage=4; beginStage(4); setState(GS.PLAY); player.reset();
  run.pilot='freezer'; run.weapon=5; run.wlevels=[0,0,0,0,0,3]; run.wlevel=3;
  run.wvars=[null,null,null,null,null,'fireice'];
  pBullets.length=0; launchFireball(FRZ_ORB_FULL);
  window.__rays=[];
  for(let i=0;i<180;i++){
    updatePlay(1/60);
    for(const b of pBullets) if(b.kind==='firray' && !b.__seen){ b.__seen=1; window.__rays.push({el:b._el, ts:b._ts}); }
  }
`);
const rays = JSON.parse(E.run('JSON.stringify(window.__rays)'));
ok(rays.length === 8, 'the discharge fires all eight rays', rays.length);
ok(rays.every(r => r.ts === 1), '...all of them carrying the thermoshock flag', rays);
const els = rays.map(r => r.el);
ok(els.filter(e => e === 'fire').length === 4 && els.filter(e => e === 'ice').length === 4,
  '...four flame and four frost, alternating — the pack is authored four of each', els);

/* a plain fireball must be untouched by all of this */
setup('freezer', 3, 5, 'fireorb');
E.run('pBullets.length=0; launchFireball(FRZ_ORB_FULL);');
const plain = JSON.parse(E.run("JSON.stringify(pBullets.map(b=>({k:b.kind,ts:b._ts})))"));
ok(plain.length === 1 && !plain[0].ts, 'the plain FIREBALL is unchanged — no _ts, same weapon Mike signed off', plain);

// ---------------------------------------------------------------- the art exists
section('THE nts_ PACK IS REGISTERED (it was never referenced before this drop)');
const need = [];
for (let k = 0; k < 12; k++) need.push('nts_orb_' + k);
for (let k = 0; k < 8; k++) need.push('nts_shard_' + k);
for (let k = 0; k < 8; k++) need.push('nts_burst_' + k);
for (let k = 0; k < 4; k++) need.push('nts_chg_' + k, 'nts_rel_' + k, 'nts_imp_' + k);
const missing = need.filter(k => E.run(`!!(BOFX.img[${JSON.stringify(k)}])`) !== true);
ok(missing.length === 0, need.length + ' thermoshock keys all resolve to a sheet', missing);

// ---------------------------------------------------------------- the leak
section('THE PARTICLE EXPIRY RUNS BEFORE ANYTHING CAN SKIP IT');
E.run(`
  particles.length=0;
  particles.push({x:10,y:10,vx:0,vy:0,t:0,life:0.10,r:12,_fbDecal:1,_fbRot:0,color:'#f80'});
  particles.push({x:10,y:10,vx:0,vy:0,t:0,life:0.10,r:12,_iceChip:1,_icSz:4,_icRot:0,_icSpin:0});
  tsFx(10,10,'imp',80);
  for(let i=0;i<120;i++) updateEffects(1/60);
`);
ok(E.run('particles.length') === 0,
  '_fbDecal, _iceChip and the new _tsFx all drain to zero after 2s (they used to live forever)',
  E.run('particles.length'));

console.log('\n' + pass + ' passed, ' + fail + ' failed');
process.exit(fail ? 1 : 0);
