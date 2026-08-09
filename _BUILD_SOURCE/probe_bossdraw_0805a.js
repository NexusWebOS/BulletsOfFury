/* probe_bossdraw_0805a.js — WHICH BOSSES ACTUALLY PUT PIXELS ON SCREEN?

   Mike: "I cant see any bosses on screen except for the helicopter boss."

   Reasoning from source said drawBossSprite's fallbacks all point at missing art.
   This measures it instead: boots the real manifest + section_geom + game.js with
   real PNG dimensions, spawns each stage's boss through the real spawnBoss(), runs
   the real drawBoss(), and counts drawImage calls with a resolved art key.

   A boss that emits 0 keyed draws is invisible in the game. That is the number.

   usage: node probe_bossdraw_0805a.js
*/
const fs = require('fs'), path = require('path'), vm = require('vm');
const ROOT = path.resolve(__dirname, '..');

const MAN = JSON.parse(fs.readFileSync(path.join(ROOT,'assets/manifest.js'),'utf8')
  .match(/window\.BOFX=([\s\S]*?\});/)[1]);
const SIZE = {}, SRC2KEY = {};
function readPngSize(p){
  const b = fs.readFileSync(p);
  if (b.length>24 && b[12]===0x49 && b[13]===0x48) return [b.readUInt32BE(16), b.readUInt32BE(20)];
  return [64,64];
}
for (const k in MAN.img){
  const p = path.join(ROOT, MAN.img[k]);
  if (fs.existsSync(p)){ try{ SIZE[k]=readPngSize(p); }catch(e){} }
  SRC2KEY[MAN.img[k]] = k;
}

const REC = [];
let recording = false;

function mkCtx(){
  const noop=()=>{}; const stack=[];
  const c={
    canvas:{width:480,height:512},
    save:()=>{stack.push({a:c.globalAlpha,op:c.globalCompositeOperation});},
    restore:()=>{const s=stack.pop(); if(s){c.globalAlpha=s.a;c.globalCompositeOperation=s.op;}},
    translate:noop, rotate:noop, scale:noop,
    beginPath:noop, closePath:noop, moveTo:noop, lineTo:noop, arc:noop, arcTo:noop,
    ellipse:noop, rect:noop, fill:noop, stroke:noop, clip:noop, roundRect:noop,
    fillRect:noop, strokeRect:noop, clearRect:noop, fillText:noop, strokeText:noop,
    drawImage:function(im,a,b,w,h){
      if(recording) REC.push({key:(im&&im.__key)||null, x:a,y:b,w:w,h:h, alpha:c.globalAlpha});
    },
    setTransform:noop, resetTransform:noop, transform:noop,
    measureText:()=>({width:10}),
    createLinearGradient:()=>({addColorStop:noop}),
    createRadialGradient:()=>({addColorStop:noop}),
    createPattern:()=>({}),
    getImageData:()=>({data:new Uint8ClampedArray(4)}),
    putImageData:noop, drawFocusIfNeeded:noop,
    globalAlpha:1, globalCompositeOperation:'source-over', filter:'none',
    fillStyle:'#000', strokeStyle:'#000', lineWidth:1, lineJoin:'', lineCap:'',
    shadowColor:'', shadowBlur:0, font:'', textAlign:'', textBaseline:'',
    imageSmoothingEnabled:true,
  };
  return c;
}
function mkCanvas(){
  return {width:480,height:512,style:{},getContext:()=>mkCtx(),
    addEventListener:()=>{}, getBoundingClientRect:()=>({left:0,top:0,width:480,height:512})};
}
class FakeImage{
  constructor(){this._src='';this.naturalWidth=64;this.naturalHeight=64;
    this.width=64;this.height=64;this.complete=true;this.__key=null;}
  set src(v){
    this._src=v;
    const rel=String(v).replace(/^.*?(assets\/)/,'$1');
    const k=SRC2KEY[rel];
    if(k){ this.__key=k; const d=SIZE[k];
      if(d){this.naturalWidth=d[0];this.naturalHeight=d[1];this.width=d[0];this.height=d[1];} }
    else if(/master/.test(v)){this.naturalWidth=800;this.naturalHeight=4800;}
    if(this.onload) setTimeout(()=>this.onload(),0);
  }
  get src(){return this._src;}
}

const sandbox={
  console, setTimeout, clearTimeout, setInterval, clearInterval, Math, Date, JSON,
  performance:{now:()=>Date.now()},
  requestAnimationFrame:()=>0, cancelAnimationFrame:()=>{},
  Image:FakeImage, HTMLImageElement:FakeImage, HTMLCanvasElement:function(){},
  localStorage:{getItem:()=>null,setItem:()=>{},removeItem:()=>{}},
  navigator:{userAgent:'node',maxTouchPoints:0},
  AudioContext:function(){return{createGain:()=>({connect:()=>{},gain:{value:0,setValueAtTime:()=>{},linearRampToValueAtTime:()=>{},exponentialRampToValueAtTime:()=>{}}}),
    createOscillator:()=>({connect:()=>{},start:()=>{},stop:()=>{},frequency:{value:0,setValueAtTime:()=>{},linearRampToValueAtTime:()=>{},exponentialRampToValueAtTime:()=>{}},type:''}),
    createBuffer:()=>({getChannelData:()=>new Float32Array(1)}), createBufferSource:()=>({connect:()=>{},start:()=>{},stop:()=>{},buffer:null}),
    createBiquadFilter:()=>({connect:()=>{},frequency:{value:0,setValueAtTime:()=>{}},Q:{value:0},type:''}),
    destination:{},currentTime:0,sampleRate:44100,resume:()=>Promise.resolve(),state:'running'};},
  document:{
    getElementById:()=>mkCanvas(), querySelector:()=>mkCanvas(),
    querySelectorAll:()=>[], createElement:(t)=>(t==='canvas'?mkCanvas():{style:{},appendChild(){},addEventListener(){}}),
    addEventListener:()=>{}, body:{appendChild(){},style:{},addEventListener(){}},
    documentElement:{style:{}}, hidden:false,
  },
  fetch:()=>Promise.reject(new Error('no net')),
};
sandbox.window=sandbox; sandbox.globalThis=sandbox; sandbox.window.addEventListener=()=>{};
const ctxv=vm.createContext(sandbox);
function run(f){
  try{ vm.runInContext(fs.readFileSync(path.join(ROOT,f),'utf8'), ctxv, {filename:f}); }
  catch(e){ console.error('[load '+f+'] '+e.message); process.exit(1); }
}
run('assets/manifest.js');
run('assets/section_geom.js');
run('assets/game.js');

// Decode EVERY key so rdy() answers honestly about art that genuinely exists on disk.
vm.runInContext(`Object.keys(window.BOFX.img).forEach(function(k){ try{ XART._touch(k); }catch(e){} });`, ctxv);

const STAGE_BOSS = [
  [1,'damkeeper','JUNGLE OVERLORD-X'],
  [2,'magmacolossus','MAGMA COLOSSUS'],
  [3,'cryobehemoth','CRYO BEHEMOTH'],
  [4,'warhawk','WARHAWK ARSENAL'],
  [5,'rampartzero','RAMPART ZERO'],
  [6,'stormsovereign','STORM SOVEREIGN'],
  [7,'toxicleviathan','TOXIC LEVIATHAN'],
  [8,'vileexistence','APOSTLE COCOON'],
];

console.log('stage  boss                  kind             keyed  uniq  flags                    top art key');
console.log('-----  --------------------  ---------------  -----  ----  -----------------------  -------------------------');

const summary=[];
for(const [sn,kind,label] of STAGE_BOSS){
  let flags='(spawn threw)', keyed=0, uniq=0, top='-';
  try{
    vm.runInContext(`
      run.stage=${sn}; curStage=STAGES[${sn-1}];
      boss=null; bossActive=true;
      spawnBoss('${kind}');
      if(boss){ boss.enter=false; boss.x=240; boss.y=170; boss.t=1.2; boss.flash=0;
                if(boss._gen) boss._gen.done=true; }
    `, ctxv);
    flags = vm.runInContext(`(function(){var b=boss; if(!b) return 'NO BOSS OBJECT';
      var f=[]; if(b._gen)f.push('_gen'); if(b._mech)f.push('_mech'); if(b._sx)f.push('_sx');
      if(b.modular)f.push('modular'); if(b.mega)f.push('mega');
      return f.length?f.join(','):'(none)';})()`, ctxv);

    REC.length=0; recording=true;
    vm.runInContext(`try{ drawBoss(); }catch(e){ window.__drawErr=e.message; }`, ctxv);
    recording=false;
    const err = vm.runInContext(`window.__drawErr||''`, ctxv);
    vm.runInContext(`window.__drawErr='';`, ctxv);

    const keys = REC.filter(r=>r.key).map(r=>r.key);
    keyed = keys.length;
    const set = [...new Set(keys)];
    uniq = set.length;
    top = set.slice(0,2).join(' ') || (err? 'ERR: '+err.slice(0,40) : '-');
  }catch(e){ top='SPAWN ERR: '+e.message.slice(0,40); }

  const mark = keyed===0 ? '  <<< INVISIBLE' : '';
  console.log(
    String(sn).padEnd(7) + label.padEnd(22) + kind.padEnd(17) +
    String(keyed).padEnd(7) + String(uniq).padEnd(6) + flags.padEnd(25) + top + mark);
  summary.push({sn,kind,label,keyed,uniq,flags,top});
}

console.log('');
const dead = summary.filter(s=>s.keyed===0);
console.log('INVISIBLE BOSSES: ' + dead.length + ' of ' + summary.length +
  (dead.length? '  -> ' + dead.map(s=>s.label).join(', ') : ''));
