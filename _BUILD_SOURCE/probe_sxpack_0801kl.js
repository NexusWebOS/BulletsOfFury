/* probe_sxpack_0801kl.js — RECORD WHAT sxPackDraw ACTUALLY DRAWS

   "A harness pass is not a game pass" is trap #1 in the passover, and the reason
   is right here in the mock: FakeImage reports 64x64 for every asset and
   complete=true for every key, so a draw path can look perfectly healthy while
   emitting garbage geometry.

   This probe boots the REAL manifest + section_geom + game.js, but with:
     - image dimensions read from the actual PNGs on disk
     - a ctx that RECORDS every drawImage(key, dx,dy,dw,dh, alpha)
   then spawns the glacier rail, drives it through real damage via hitSubBoss,
   and dumps the call list as JSON. render_sxpack_0801kl.py replays that JSON
   into a PNG, so what gets eyeballed is the output of the shipping code and not
   a reimplementation of it.

   usage: node probe_sxpack_0801kl.js > /tmp/sxpack.json
*/
const fs = require('fs'), path = require('path'), vm = require('vm');
const ROOT = path.resolve(__dirname, '..');

// ---- real dimensions, straight off disk
const manSrc = fs.readFileSync(path.join(ROOT, 'assets/manifest.js'), 'utf8');
const MAN = JSON.parse(manSrc.match(/window\.BOFX=([\s\S]*?\});/)[1]);
const SIZE = {}, SRC2KEY = {};
let pngSize;
try { pngSize = require('image-size'); } catch (e) { pngSize = null; }
function readPngSize(p) {
  const b = fs.readFileSync(p);
  if (b.length > 24 && b[12] === 0x49 && b[13] === 0x48) {         // IHDR
    return [b.readUInt32BE(16), b.readUInt32BE(20)];
  }
  return [64, 64];
}
for (const k in MAN.img) {
  const p = path.join(ROOT, MAN.img[k]);
  if (fs.existsSync(p)) { try { SIZE[k] = readPngSize(p); } catch (e) {} }
  SRC2KEY[MAN.img[k]] = k;
}

const REC = [];
let recording = false;
function keyOf(im) { return (im && im.__key) || null; }

function mkCtx() {
  const noop = () => {};
  /* save/restore are REAL here, not noops. The suite's mock stubs them out, which
     lets globalAlpha set inside one draw leak into the next — the recorded body
     plates came back at alpha 0.18 purely from the previous frame's smoke. That is
     a measurement artifact and it would have made this probe lie about the picture,
     so the stack is implemented properly. */
  const stack = [];
  const c = {
    canvas: { width: 480, height: 512 },
    save: () => { stack.push({ a: c.globalAlpha, op: c.globalCompositeOperation }); },
    restore: () => { const s = stack.pop(); if (s) { c.globalAlpha = s.a; c.globalCompositeOperation = s.op; } },
    translate: noop, rotate: noop, scale: noop,
    beginPath: noop, closePath: noop, moveTo: noop, lineTo: noop, arc: noop, arcTo: noop,
    ellipse: noop, rect: noop, fill: noop, stroke: noop, clip: noop, roundRect: noop,
    fillRect: noop, strokeRect: noop, clearRect: noop, fillText: noop, strokeText: noop,
    drawImage: function (im, a, b, w, h) {
      if (recording) {
        REC.push({ key: keyOf(im), x: a, y: b, w: w, h: h,
                   alpha: c.globalAlpha, op: c.globalCompositeOperation });
      }
    },
    setTransform: noop, resetTransform: noop, transform: noop,
    measureText: () => ({ width: 10 }),
    createLinearGradient: () => ({ addColorStop: noop }),
    createRadialGradient: () => ({ addColorStop: noop }),
    createPattern: () => ({}),
    getImageData: () => ({ data: new Uint8ClampedArray(4) }),
    putImageData: noop, drawFocusIfNeeded: noop,
    globalAlpha: 1, globalCompositeOperation: 'source-over', filter: 'none',
    fillStyle: '#000', strokeStyle: '#000', lineWidth: 1, lineJoin: '', lineCap: '',
    shadowColor: '', shadowBlur: 0, font: '', textAlign: '', textBaseline: '',
    imageSmoothingEnabled: true,
  };
  return c;
}
function mkCanvas() {
  return { width: 480, height: 512, style: {}, getContext: () => mkCtx(),
    addEventListener: () => {}, getBoundingClientRect: () => ({ left: 0, top: 0, width: 480, height: 512 }) };
}
class FakeImage {
  constructor() { this._src=''; this.naturalWidth=64; this.naturalHeight=64;
                  this.width=64; this.height=64; this.complete=true; this.__key=null; }
  set src(v) {
    this._src = v;
    const rel = String(v).replace(/^.*?(assets\/)/, '$1');
    const k = SRC2KEY[rel];
    if (k) { this.__key = k;
      const d = SIZE[k];
      if (d) { this.naturalWidth=d[0]; this.naturalHeight=d[1]; this.width=d[0]; this.height=d[1]; } }
    else if (/master/.test(v)) { this.naturalWidth=800; this.naturalHeight=4800; }
    if (this.onload) setTimeout(() => this.onload(), 0);
  }
  get src() { return this._src; }
}

const sandbox = {
  console, setTimeout, clearTimeout, setInterval, clearInterval, Math, Date, JSON,
  performance: { now: () => Date.now() },
  requestAnimationFrame: () => 0, cancelAnimationFrame: () => {},
  Image: FakeImage, HTMLImageElement: FakeImage, HTMLCanvasElement: function(){},
  localStorage: { getItem: () => null, setItem: () => {}, removeItem: () => {} },
  navigator: { userAgent: 'node', maxTouchPoints: 0 },
  AudioContext: function(){ return { createGain:()=>({connect:()=>{},gain:{value:0,setValueAtTime:()=>{},linearRampToValueAtTime:()=>{},exponentialRampToValueAtTime:()=>{}}}),
    createOscillator:()=>({connect:()=>{},start:()=>{},stop:()=>{},frequency:{value:0,setValueAtTime:()=>{},linearRampToValueAtTime:()=>{},exponentialRampToValueAtTime:()=>{}},type:''}),
    createBuffer:()=>({getChannelData:()=>new Float32Array(1)}), createBufferSource:()=>({connect:()=>{},start:()=>{},stop:()=>{},buffer:null}),
    createBiquadFilter:()=>({connect:()=>{},frequency:{value:0,setValueAtTime:()=>{}},Q:{value:0},type:''}),
    destination:{}, currentTime:0, sampleRate:44100, resume:()=>Promise.resolve(), state:'running' }; },
  document: {
    getElementById: () => mkCanvas(), querySelector: () => mkCanvas(),
    querySelectorAll: () => [], createElement: (t) => (t === 'canvas' ? mkCanvas() : { style: {}, appendChild(){}, addEventListener(){} }),
    addEventListener: () => {}, body: { appendChild(){}, style:{}, addEventListener(){} },
    documentElement: { style: {} }, hidden: false,
  },
  fetch: () => Promise.reject(new Error('no net')),
};
sandbox.window = sandbox;
sandbox.globalThis = sandbox;
sandbox.window.addEventListener = () => {};
const ctxv = vm.createContext(sandbox);

function run(f) {
  try { vm.runInContext(fs.readFileSync(path.join(ROOT, f), 'utf8'), ctxv, { filename: f }); }
  catch (e) { console.error('[load ' + f + '] ' + e.message); process.exit(1); }
}
run('assets/manifest.js');
run('assets/section_geom.js');
run('assets/game.js');

// Force every pack + smoke key to be "decoded" so rdy() is honest about art that exists.
vm.runInContext(`
  (function(){
    var ks=Object.keys(window.BOFX.img).filter(function(k){
      return /^(nglr_|nobd_|smk_)/.test(k); });
    ks.forEach(function(k){ try{ XART._touch(k); }catch(e){} });
  })();
`, ctxv);

const frames = {};
function capture(label, setup) {
  vm.runInContext(setup, ctxv);
  REC.length = 0; recording = true;
  vm.runInContext(`sxPackDraw(subBoss, 0.016);`, ctxv);
  recording = false;
  frames[label] = REC.slice();
}

const spawn = `
  run.stage=3; curStage=STAGES[2];
  subBoss=null; subBossActive=false; spawnSubBoss('glacierrail');
  subBoss.enter=false; subBoss.x=240; subBoss.y=170; subBoss.flash=0;
  subBoss._sx.t=0.6;
`;
capture('intact', spawn);

/* NATIVE SCALE: drawW == the pack canvas width, so no resampling happens and the
   composite can be diffed against assembled_intact pixel-for-pixel. */
capture('native_scale', spawn + `subBoss.w=234/1.02; subBoss.h=subBoss.w;`);

capture('damaged_all', spawn + `
  for(var p in subBoss._sx.hp){ subBoss._sx.hp[p]=subBoss._sx.max[p]*0.50; }
`);

capture('critical_all', spawn + `
  for(var p in subBoss._sx.hp){ subBoss._sx.hp[p]=subBoss._sx.max[p]*0.20; }
`);

capture('turrets_blown', spawn + `
  ['left_weapon_pod','right_weapon_pod','turret_core'].forEach(function(p){
    subBoss._sx.hp[p]=0; subBoss._sx.dead[p]=true; });
  subBoss._sx.hp['hull']=subBoss._sx.max['hull']*0.45;
  subBoss._sx.hp['front_weapon']=subBoss._sx.max['front_weapon']*0.30;
`);

// --- behavioural facts worth asserting alongside the picture
const facts = {};
facts.weapons_live_intact = JSON.parse(vm.runInContext(
  spawn + `JSON.stringify(sxLiveWeapons(subBoss))`, ctxv));
facts.weapons_after_left_pod = JSON.parse(vm.runInContext(
  spawn + `subBoss._sx.dead['left_weapon_pod']=true; JSON.stringify(sxLiveWeapons(subBoss))`, ctxv));
facts.hit_attribution = JSON.parse(vm.runInContext(spawn + `
  (function(){
    var G=sxPackGeom('grf'), out={};
    for(var pt in G.sections){
      var c=G.sections[pt].c;
      var hx=subBoss.x+c[0]*subBoss.w, hy=subBoss.y+c[1]*subBoss.h;
      var before={}; for(var p in subBoss._sx.hp) before[p]=subBoss._sx.hp[p];
      sxHit(subBoss, 5, hx, hy);
      var hit=null;
      for(var p in subBoss._sx.hp) if(subBoss._sx.hp[p]<before[p]) hit=p;
      out[pt]=hit;
    }
    return JSON.stringify(out);
  })()
`, ctxv));
facts.flash_on_hit = JSON.parse(vm.runInContext(spawn + `
  (function(){
    var G=sxPackGeom('grf'), c=G.sections['left_track'].c;
    sxHit(subBoss, 5, subBoss.x+c[0]*subBoss.w, subBoss.y+c[1]*subBoss.h);
    return JSON.stringify(subBoss._sx.flash||{});
  })()
`, ctxv));

// ---- HITMAP: which part is hit at each point, old 40px circle vs new boxes
facts.hitmap = JSON.parse(vm.runInContext(spawn + `
 (function(){
   var b=subBoss, out={grid:[], oldHits:0, newHits:0, parts:{}, w:b.w, h:b.h};
   for(var gy=b.y-160; gy<=b.y+160; gy+=8){
     for(var gx=b.x-140; gx<=b.x+140; gx+=8){
       var oldHit = ((b.x-gx)*(b.x-gx)+(b.y-gy)*(b.y-gy)) < 40*40;
       var pt = subBossHitPart(gx,gy);
       if(oldHit) out.oldHits++;
       if(pt){ out.newHits++; out.parts[pt]=(out.parts[pt]||0)+1;
               out.grid.push([gx-b.x, gy-b.y, pt]); }
     }
   }
   return JSON.stringify(out);
 })()
`, ctxv));
// furthest distance from centre at which each turret can be hit
facts.turretReach = JSON.parse(vm.runInContext(spawn + `
 (function(){
   var b=subBoss, out={};
   ['left_weapon_pod','right_weapon_pod','turret_core','front_weapon','hull'].forEach(function(pt){
     var best=0;
     for(var gy=b.y-200; gy<=b.y+200; gy+=4)
       for(var gx=b.x-200; gx<=b.x+200; gx+=4)
         if(subBossHitPart(gx,gy)===pt) best=Math.max(best, Math.round(Math.hypot(gx-b.x,gy-b.y)));
     out[pt]=best;
   });
   return JSON.stringify(out);
 })()
`, ctxv));
process.stdout.write(JSON.stringify({ frames, facts }, null, 1));
