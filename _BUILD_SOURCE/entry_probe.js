/* ============================================================================
   entry_probe.js — measures how many frames pass before a unit's FIRST shot.

   WHY THIS EXISTS
   My previous probe pre-seeded the very timers it was measuring (E.fireCd=0,
   E._fcd=0.001). On the generic path that was harmless — the gate ran first and
   overwrote it. On the sewer path I had just moved the initialiser INSIDE the
   gate, so pre-seeding bypassed the gate entirely and every volcanic unit
   reported "frame 0". I then believed the probe over the code and concluded I
   had broken the roster.

   THE RULE THIS ENFORCES ON ITSELF: touch nothing. Spawn the unit, run the real
   update loop, watch eBullets. If a unit is slow to fire because its natural
   cooldown is long, that is a true reading, not something to "fix" by poking it.

   Usage:  node _BUILD_SOURCE/entry_probe.js
   ============================================================================ */
const fs = require('fs'), vm = require('vm'), path = require('path');
const ROOT = path.join(__dirname, '..');

class FI {
  constructor() { this.naturalWidth = 64; this.naturalHeight = 64; this.width = 64; this.height = 64; this.complete = true; }
  set src(v) { this._src = v; if (/master/.test(v)) { this.naturalWidth = 800; this.naturalHeight = 4800; } }
  get src() { return this._src; }
  addEventListener() {}
}
class FA {
  constructor() { this.volume = 1; }
  play() { return { catch() {}, then() { return { catch() {} }; } }; }
  pause() {} load() {} addEventListener() {}
}
function mkCtx() {
  const f = () => {};
  return new Proxy({
    canvas: { width: 480, height: 512 }, measureText: () => ({ width: 20 }),
    createLinearGradient: () => ({ addColorStop: f }), createRadialGradient: () => ({ addColorStop: f }),
    createPattern: () => ({}), getImageData: () => ({ data: new Uint8ClampedArray(4) })
  }, { get: (t, p) => (p in t) ? t[p] : f, set: () => true });
}
function mkCanvas() {
  return { width: 480, height: 512, style: {}, getContext: () => mkCtx(), addEventListener() {},
           getBoundingClientRect: () => ({ left: 0, top: 0, width: 480, height: 512 }) };
}
const els = {};
const getEl = id => els[id] || (els[id] = (id === 'screen' || id === 'hud') ? mkCanvas() : {
  style: {}, appendChild() {}, addEventListener() {},
  classList: { add() {}, remove() {}, toggle() {} },
  getBoundingClientRect: () => ({ left: 0, top: 0, width: 480, height: 512 }), children: [], innerHTML: ''
});
const sb = {
  document: { getElementById: getEl, createElement: t => t === 'canvas' ? mkCanvas() : { style: {}, appendChild() {}, addEventListener() {} },
    addEventListener() {}, body: { appendChild() {}, style: {} },
    documentElement: { style: {}, clientWidth: 900, clientHeight: 700 },
    fonts: { load: () => Promise.resolve(), ready: Promise.resolve() },
    hidden: false, exitFullscreen() {}, fullscreenElement: null },
  Image: FI, Audio: FA, requestAnimationFrame: () => 0, cancelAnimationFrame() {},
  performance: { now: () => 0 }, localStorage: { getItem: () => null, setItem() {}, removeItem() {} },
  setTimeout, clearTimeout, setInterval: () => 0, clearInterval() {},
  console, Math, Date, JSON, navigator: { userAgent: 'node', getGamepads: () => [] },
  screen: { width: 1920, height: 1080 },
  matchMedia: () => ({ matches: false, addListener() {}, addEventListener() {} }),
  atob: b => Buffer.from(b, 'base64').toString('binary')
};
sb.window = sb; sb.self = sb; sb.globalThis = sb; sb.addEventListener = () => {};
sb.innerWidth = 900; sb.innerHeight = 700; sb.devicePixelRatio = 1;

const C = vm.createContext(sb);
vm.runInContext(fs.readFileSync(path.join(ROOT, 'assets/manifest.js'), 'utf8'), C, { filename: 'm' });
vm.runInContext(fs.readFileSync(path.join(ROOT, 'assets/game.js'), 'utf8'), C, { filename: 'g' });
vm.runInContext('ASSETS.ready=true; beginStage(1); setState(GS.PLAY); player.reset(); player.x=240; player.y=430;', C);

const S2 = ['ash', 'disc', 'lance', 'eye', 'cruc', 'carrier', 'skim'];
const TYPES = ['racer', 'intcp', 'bomber', 'topgun', 'drone', 'mdrone', 'turdrone',
  'jungletank', 'tank', 'htank', 'stationship', 'sideswirl', 'jetflyby',
  'skimmer', 'barge', 'gunboat', 'skim', 'ash', 'disc', 'lance', 'eye', 'cruc', 'carrier'];

console.log('FRAMES UNTIL FIRST SHOT — nothing pre-seeded, real update loop\n');
console.log('  unit          frames   verdict');
const early = [], never = [];
for (const t of TYPES) {
  const st = S2.includes(t) ? 2 : 1;
  /* THE STAGE PLAN KEEPS SPAWNING. My first version measured "frames until
     eBullets is non-empty" while updatePlay carried on running the wave plan
     behind it — so the reading was the first shot from ANY enemy on the level,
     not the one under test. That is how a clean drone reported frame 12.
     Emptying the plan isolates the unit. */
  vm.runInContext(`run.stage=${st}; curStage=STAGES[${st - 1}]; enemies.length=0; eBullets.length=0; mapScroll=2200;` +
                  ` if(typeof stagePlan!=='undefined') stagePlan.length=0;` +
                  ` try{spawnEnemy(${JSON.stringify(t)},240,120);}catch(e){}`, C);
  if (!vm.runInContext('enemies.length', C)) continue;
  // deliberately touch NOTHING on the spawned unit
  let f = 0, fired = false;
  for (; f < 400; f++) {
    vm.runInContext('updatePlay(1/60);', C);
    if (vm.runInContext('eBullets.length', C) > 0) { fired = true; break; }
    if (!vm.runInContext('enemies.length', C)) break;
  }
  let verdict;
  if (!fired) { verdict = 'never fired on screen'; never.push(t); }
  else if (f < 20) { verdict = '<== BEFORE FRAME 20'; early.push(`${t}@${f}`); }
  else verdict = 'ok';
  console.log('  ' + t.padEnd(13) + String(fired ? f : '-').padStart(5) + '   ' + verdict);
}
console.log();
console.log(early.length === 0
  ? `  PASS — nothing fires before frame 20 (${never.length} never fired: ${never.join(', ') || 'none'})`
  : `  FAIL — early: ${early.join(', ')}`);
process.exit(early.length === 0 ? 0 : 1);
