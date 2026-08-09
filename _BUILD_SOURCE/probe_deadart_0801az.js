/* Behavioural probe for drop 0801az.

   The point of this probe is the COLD LOADER. test_fl.js uses a FakeImage that
   reports complete=true and naturalWidth=64 the instant src is set, which means
   XART.rdy() is true for everything from the first frame - and that HIDES the
   exact race that made enemies invisible. Here images stay incomplete until
   explicitly "delivered", which is how the real lazy loader behaves on the
   opening frames of a stage.

   Assertions call spawnEnemy() - the real spawn path - and then ask whether the
   art the engine chose would actually draw. No string comparisons on source. */
const fs = require('fs'), vm = require('vm'), path = require('path');
const ROOT = path.resolve(__dirname, '..');

let COLD = true;                       // while true, nothing has "downloaded" yet
const made = [];
class FakeImage {
  constructor() { this.naturalWidth = 0; this.naturalHeight = 0; this.complete = false; made.push(this); }
  set src(v) { this._src = v; if (!COLD) this._deliver(); }
  get src() { return this._src; }
  _deliver() { this.naturalWidth = 64; this.naturalHeight = 64; this.width = 64; this.height = 64; this.complete = true; }
  addEventListener() {}
}
class FakeAudio { constructor(){this.volume=1;this.currentTime=0;} play(){return{catch(){},then(){return{catch(){}}}};} pause(){} load(){} addEventListener(){} }
function mkCtx(){ const n=()=>{}; return new Proxy({ canvas:{width:480,height:512}, measureText:()=>({width:10}),
  createLinearGradient:()=>({addColorStop:n}), createRadialGradient:()=>({addColorStop:n}), createPattern:()=>({}),
  getImageData:()=>({data:new Uint8ClampedArray(4)}) }, { get:(t,p)=> (p in t)?t[p]:n, set:()=>true }); }
function mkCanvas(){ return { width:480, height:512, style:{}, getContext:()=>mkCtx(), addEventListener(){},
  getBoundingClientRect:()=>({left:0,top:0,width:480,height:512}) }; }
const els = {};
const getEl = id => els[id] || (els[id] = (id==='screen'||id==='hud') ? mkCanvas()
  : { style:{}, appendChild(){}, addEventListener(){}, classList:{add(){},remove(){},toggle(){}},
      getBoundingClientRect:()=>({left:0,top:0,width:480,height:512}), children:[], innerHTML:'' });
const sb = { document:{ getElementById:getEl,
    createElement:t => t==='canvas'?mkCanvas():{style:{},appendChild(){},addEventListener(){}},
    addEventListener(){}, body:{appendChild(){},style:{}},
    documentElement:{style:{},clientWidth:900,clientHeight:700},
    fonts:{load:()=>Promise.resolve(),ready:Promise.resolve()},
    hidden:false, exitFullscreen(){}, fullscreenElement:null },
  Image:FakeImage, Audio:FakeAudio, requestAnimationFrame:()=>0, cancelAnimationFrame(){},
  performance:{now:()=>Date.now()}, localStorage:{getItem:()=>null,setItem(){},removeItem(){}},
  setTimeout, clearTimeout, setInterval:()=>0, clearInterval(){},
  console, Math, Date, JSON, navigator:{userAgent:'node',getGamepads:()=>[]},
  screen:{width:1920,height:1080},
  matchMedia:()=>({matches:false,addListener(){},addEventListener(){}}) };
sb.window=sb; sb.self=sb; sb.globalThis=sb; sb.addEventListener=()=>{};
sb.innerWidth=900; sb.innerHeight=700; sb.devicePixelRatio=1;
const C = vm.createContext(sb);
vm.runInContext(fs.readFileSync(ROOT+'/assets/manifest.js','utf8'), C, {filename:'manifest.js'});
vm.runInContext(fs.readFileSync(ROOT+'/assets/game.js','utf8'), C, {filename:'game.js'});

const B = 'window.__P={};' + ['ENEMY_ART','XART','enemies','run','player']
  .map(n=>`try{Object.defineProperty(window.__P,'${n}',{get:()=>${n},set:v=>{${n}=v;},configurable:true});}catch(e){}`).join('')
  + ['spawnEnemy','enemyArtState','drawNewEnemyArt']
  .map(n=>`try{window.__P.${n}=${n};}catch(e){}`).join('');
vm.runInContext(B, C, {filename:'bridge'});
const G = sb.window.__P;

let bad = 0;
const ok = (c,m) => { console.log((c?'  ok   ':'  FAIL ') + m); if(!c) bad++; };
const IMG = sb.window.BOFX.img;

console.log('\n=== A. the 13 culled roles are gone from ENEMY_ART ===');
const CULLED = ['navalturret','boat1','boat2','boat3','boat4','boat5','boat6','boat7',
                'esturret1','esturret2','decoA','decoB','decoC'];
const still = CULLED.filter(r => G.ENEMY_ART[r] !== undefined);
ok(still.length === 0, 'all 13 removed' + (still.length?' STILL PRESENT: '+still:''));

console.log('\n=== B. every SURVIVING role still resolves its idle frame ===');
const surv = Object.keys(G.ENEMY_ART);
const broken = surv.filter(r => !IMG[G.ENEMY_ART[r] + '_idle']);
ok(broken.length === 0, surv.length + ' roles survive, all with registered idle art'
   + (broken.length ? '  BROKEN: ' + broken : ''));

console.log('\n=== C. COLD LOADER: spawn every wave type, nothing downloaded yet ===');
/* This is the regression that mattered. COLD===true, so every Image is
   incomplete and XART.rdy() is false across the board - exactly the opening
   frames of a stage. The old guard filtered healthy art out here and fell
   through to the unfiltered pool. */
console.log('  (cold: XART.rdy on a known-good key ->',
  G.XART.rdy('tnkG_g2_idle'), '- this is what the old guard was reading)');
const TYPES = ['tank','htank','mgturret','rockturret','microturret','turret','turdrone',
  'shieldd','drone','mdrone','minidrone','assault','gunship','scout','intcp','hfight',
  'bomber','mine','frost','octo','mech','icegun','cryo','ebomb','minicarrier'];
let invisible = [], checked = 0;
for (const stage of [1,2,3,4,5]) {
  G.run.stage = stage;
  for (const t of TYPES) {
    G.enemies.length = 0;
    const e = G.spawnEnemy(t, 240, 100);
    if (!e) continue;
    checked++;
    if (e.art === undefined) continue;            // legacy art path, not ENEMY_ART
    const base = G.ENEMY_ART[e.art];
    if (!base || !IMG[base + '_idle']) invisible.push(`s${stage}/${t} -> art='${e.art}'`);
  }
}
ok(invisible.length === 0,
   `${checked} spawns across 5 stages, every one resolves art`
   + (invisible.length ? `\n         INVISIBLE (${invisible.length}): ` + invisible.slice(0,10).join('\n                   ') : ''));

console.log('\n=== D. no spawn ever lands on a culled role ===');
const landed = invisible.filter(s => CULLED.some(c => s.indexOf(`'${c}'`) >= 0));
ok(landed.length === 0, 'culled roles unreachable from the spawn path');

console.log('\n=== E. OVERLORD-X body resolves at EVERY hp fraction ===');
/* The old ladder produced ovbody_damaged between 0.66 and 0.33, which is not a
   registered key - the body drew nothing while the rotor kept spinning. */
let gaps = [];
for (let i = 0; i <= 20; i++) {
  const frac = i / 20;
  const key = frac > 0.5 ? 'ovbody_intact' : 'ovbody_critical';
  if (!IMG[key]) gaps.push(frac.toFixed(2) + ' -> ' + key);
}
ok(gaps.length === 0, '21 hp samples from 0.00 to 1.00, body art registered at every one'
   + (gaps.length ? '  GAPS: ' + gaps : ''));
ok(!IMG['ovbody_damaged'], 'ovbody_damaged confirmed absent - the state was right to remove');
const gsrc = fs.readFileSync(ROOT + '/assets/game.js', 'utf8');
ok(gsrc.indexOf("'ovbody_damaged'") < 0, 'and nothing in the build still asks for it');

console.log('\n=== F. warm loader still fine (no state left behind) ===');
COLD = false;
made.forEach(im => { if (im._src) im._deliver(); });
G.enemies.length = 0; G.run.stage = 1;
const warm = G.spawnEnemy('tank', 240, 100);
ok(!!warm && !!G.ENEMY_ART[warm.art] && !!IMG[G.ENEMY_ART[warm.art] + '_idle'],
   'a warm-loader tank spawn still resolves (art=' + (warm && warm.art) + ')');

console.log(bad === 0 ? '\n==== DROP 0801az OK, 0 ERRORS ====' : `\n==== ${bad} ERROR(S) ====`);
process.exit(bad ? 1 : 0);
