const fs = require('fs');
const vm = require('vm');

const src = fs.readFileSync('assets/game.js', 'utf8');
const checks = [];

function ok(name, pass, detail = '') {
  checks.push({ name, pass: !!pass, detail });
  if (!pass) throw new Error(`${name}${detail ? `: ${detail}` : ''}`);
}

function has(re) { return re.test(src); }

ok('Stage 1 Jungle Cruiser authored HP raised',
  has(/junglecruiser:\s*\{[^\n]*hp:900\b/));
ok('Stage 2 Magma Ward authored HP raised',
  has(/magmaward:\s*\{[^\n]*hp:1000\b/));
ok('Stage 1 and 2 encounter HP floors raised',
  has(/const MINIBOSS_HP_FLOOR=\[900,1100,650,820,1020,1260,1540,1860,2220\]/));

ok('Helix creates one shared encounter budget per ball',
  has(/function helixFlurrySpawn[\s\S]*?const budget=\{target:null,spent:0,cap:0\};[\s\S]*?helixWaveSpawn\(x, y, lv, full, 0, budget\)/));
ok('Queued Helix waves retain the same budget',
  has(/helixVolleyQ\.push\(\{[^\n]*budget:budget\}\)/));
ok('Every Helix lance receives the shared budget',
  has(/bossDmg:HELIX_FLURRY_BOSS,bossBudget:budget,pierceAll:true/));
ok('Boss and miniboss collision paths consume Helix budget',
  (src.match(/helixEncounterDamage\(b,(?:subBoss|boss),_raw[SB]d\)/g) || []).length >= 2);

const fnMatch = src.match(/function helixEncounterDamage\(b,target,raw\)\{[\s\S]*?\n\}/);
ok('Helix encounter limiter function found', !!fnMatch);
const sandbox = {};
vm.runInNewContext(`${fnMatch[0]}; this.limit = helixEncounterDamage;`, sandbox);
const budget = { target: null, spent: 0, cap: 0 };
const projectile = { _helixBossBudget: budget };
const boss = { maxhp: 1000 };
let dealt = 0;
for (let i = 0; i < 105; i++) dealt += sandbox.limit(projectile, boss, 90);
ok('One complete Helix family caps at exactly 25% boss HP', dealt === 250, `dealt=${dealt}`);
ok('Exhausted Helix family cannot damage the same boss again',
  sandbox.limit(projectile, boss, 90) === 0);

ok('Flamethrower loop uses the reviewed sample',
  has(/flameThrowerLoop:'assets\/game\/sounds\/reviewed_flamethrower_loop\.wav'/));
ok('Flamethrower loop is requested at full foreground gain',
  has(/Snd\.loopOn\(n,el==='ice'\?0\.90:1\.00\)/));
ok('Flamethrower start, loop, and end bypass the fragile WebAudio media graph',
  has(/flameThrowerStart:\s*\{g:1\.00, native:true\}/) &&
  has(/flameThrowerLoop:\s*\{g:1\.00, native:true\}/) &&
  has(/flameThrowerEnd:\s*\{g:0\.92, native:true\}/) &&
  has(/if\(cfg\.native \|\| !cfg\.lp \|\| A\._bad\[name\]\) return false/));

ok('Volcano Maw breath no longer routes through generic blue laser art',
  !/s2breath:'laser'/.test(src));
ok('Volcano Maw breath owns a red/orange/cream fire palette',
  has(/const _mawFire=b\.kind==='s2breath'/) &&
  has(/_mawFire\?'#ff321c':'#36dfff'/) &&
  has(/_mawFire\?'#ff981f':'#ffe34f'/) &&
  has(/_mawFire\?'#fff0b0':'#fffdf0'/));

for (const path of [
  'assets/game/sounds/reviewed_flamethrower_start.wav',
  'assets/game/sounds/reviewed_flamethrower_loop.wav',
  'assets/game/sounds/reviewed_flamethrower_end.wav'
]) ok(`Audio asset exists: ${path}`, fs.existsSync(path));

console.log(JSON.stringify({ pass: true, checks }, null, 2));
