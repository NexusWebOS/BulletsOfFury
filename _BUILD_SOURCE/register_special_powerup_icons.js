#!/usr/bin/env node
/* Register the generated 160px special-powerup plates and route Thermoshock tiers away
   from the stale packed cells to their corrected standalone files. */
const fs = require('fs');
const path = require('path');
const vm = require('vm');
const childProcess = require('child_process');

const ROOT = path.resolve(__dirname, '..');
const manifestPath = path.join(ROOT, 'assets', 'manifest.js');
const source = fs.readFileSync(manifestPath, 'utf8');
const context = {window:{}};
vm.runInNewContext(source, context);
const BOFX = context.window.BOFX;
/* Only replace the BOFX assignment. The manifest also owns BOF, BOFA, BOFTM, BOFTK,
   BOFFI, BOFPI, BOFRS, PEMB_INK and BOFQL; rewriting the file from BOFX alone deletes
   all of them. If repairing a file written by the earlier buggy version, recover the
   untouched namespace lines from HEAD before replacing BOFX. */
let container = source;
if (!context.window.BOFA) {
  container = childProcess.execFileSync('git', ['show', 'HEAD:assets/manifest.js'],
    {cwd:ROOT, encoding:'utf8', maxBuffer:64*1024*1024});
}

const files = {
  special_icon_axel_mega_shield: 'special_icon_axel_mega_shield.png',
  special_icon_freezer_time_freeze: 'special_icon_freezer_time_freeze.png',
  special_icon_freezer_thermoshock: 'special_icon_freezer_thermoshock.png',
  special_icon_juggernaut_wrecking_ball: 'special_icon_juggernaut_wrecking_ball.png',
  special_icon_maverick_helix_beam: 'special_icon_maverick_helix_beam.png',
  special_icon_lizzie_atom_bomb: 'special_icon_lizzie_atom_bomb.png',
  special_icon_falva_roller_ball: 'special_icon_falva_roller_ball.png',
  special_icon_cole_nuclear_warheads: 'special_icon_cole_nuclear_warheads.png',
  special_icon_decker_cloaking_system: 'special_icon_decker_cloaking_system.png',
  special_icon_yuri_chain_lightning: 'special_icon_yuri_chain_lightning.png',
};

const maverickLasers = Object.fromEntries(Array.from({length:5}, (_, index) => {
  const tier = index + 1;
  return [`micon_maverick_laser_${tier}`, `micon_maverick_laser_${tier}.png`];
}));
const maverickLances = Object.fromEntries(Array.from({length:5}, (_, index) => {
  const tier = index + 1;
  return [`mavlaser_lance_${tier}`, `mavlaser_lance_${tier}.png`];
}));

for (const [key, file] of Object.entries(files)) {
  BOFX.img[key] = `assets/game/special_icons/${file}`;
}
for (const [key, file] of Object.entries(maverickLasers)) {
  BOFX.img[key] = `assets/game/maverick_laser_icons/${file}`;
}
for (const key of Object.keys(BOFX.img)) {
  if (/^mavlaser_projectile_[1-5]$/.test(key)) delete BOFX.img[key];
}
for (const [key, file] of Object.entries(maverickLances)) {
  BOFX.img[key] = `assets/game/maverick_laser_icons/${file}`;
}
for (let tier=1; tier<=5; tier++) {
  delete BOFX.icons[`micon_thermoshock_${tier}`];
}

const bofxLine = `window.BOFX=${JSON.stringify(BOFX)};`;
if (!/^window\.BOFX=.*;$/m.test(container)) throw new Error('BOFX assignment missing from manifest container');
container = container.replace(/^window\.BOFX=.*;$/m, bofxLine);
fs.writeFileSync(manifestPath, container.endsWith('\n') ? container : container+'\n', 'utf8');
console.log(`registered ${Object.keys(files).length} special icons, ${Object.keys(maverickLasers).length} Maverick laser tiers and ${Object.keys(maverickLances).length} independent Maverick lance sprites; routed 5 Thermoshock tiers to standalone art`);
