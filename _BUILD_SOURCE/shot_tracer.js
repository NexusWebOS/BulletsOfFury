/* Finds WHICH function emits a unit's first shot, and from where.
   Written as a file rather than an inline -e so the escaping cannot corrupt it. */
const fs = require('fs'), vm = require('vm'), path = require('path');
const ROOT = path.join(__dirname, '..');

class FI {
  constructor(){ this.naturalWidth=64; this.naturalHeight=64; this.width=64; this.height=64; this.complete=true; }
  set src(v){ this._src=v; if(/master/.test(v)){ this.naturalWidth=800; this.naturalHeight=4800; } }
  get src(){ return this._src; } addEventListener(){}
}
class FA { constructor(){this.volume=1;} play(){return{catch(){},then(){return{catch(){}}}};} pause(){} load(){} addEventListener(){} }
function mkCtx(){ const f=()=>{}; return new Proxy({canvas:{width:480,height:512},measureText:()=>({width:20}),
  createLinearGradient:()=>({addColorStop:f}),createRadialGradient:()=>({addColorStop:f}),createPattern:()=>({}),
  getImageData:()=>({data:new Uint8ClampedArray(4)})},{get:(t,p)=>(p in t)?t[p]:f,set:()=>true}); }
function mkCanvas(){ return {width:480,height:512,style:{},getContext:()=>mkCtx(),addEventListener(){},
  getBoundingClientRect:()=>({left:0,top:0,width:480,height:512})}; }
const els={};
const getEl=id=>els[id]||(els[id]=(id==='screen'||id==='hud')?mkCanvas():{style:{},appendChild(){},addEventListener(){},
  classList:{add(){},remove(){},toggle(){}},getBoundingClientRect:()=>({left:0,top:0,width:480,height:512}),children:[],innerHTML:''});
const sb={document:{getElementById:getEl,createElement:t=>t==='canvas'?mkCanvas():{style:{},appendChild(){},addEventListener(){}},
  addEventListener(){},body:{appendChild(){},style:{}},documentElement:{style:{},clientWidth:900,clientHeight:700},
  fonts:{load:()=>Promise.resolve(),ready:Promise.resolve()},hidden:false,exitFullscreen(){},fullscreenElement:null},
  Image:FI,Audio:FA,requestAnimationFrame:()=>0,cancelAnimationFrame(){},performance:{now:()=>0},
  localStorage:{getItem:()=>null,setItem(){},removeItem(){}},setTimeout,clearTimeout,setInterval:()=>0,clearInterval(){},
  console,Math,Date,JSON,navigator:{userAgent:'node',getGamepads:()=>[]},screen:{width:1920,height:1080},
  matchMedia:()=>({matches:false,addListener(){},addEventListener(){}}),
  atob:b=>Buffer.from(b,'base64').toString('binary')};
sb.window=sb; sb.self=sb; sb.globalThis=sb; sb.addEventListener=()=>{};
sb.innerWidth=900; sb.innerHeight=700; sb.devicePixelRatio=1;

const C = vm.createContext(sb);
vm.runInContext(fs.readFileSync(path.join(ROOT,'assets/manifest.js'),'utf8'), C, {filename:'m'});
vm.runInContext(fs.readFileSync(path.join(ROOT,'assets/game.js'),'utf8'), C, {filename:'g'});
vm.runInContext('ASSETS.ready=true; beginStage(1); setState(GS.PLAY); player.reset(); player.x=240; player.y=430;', C);

// wrap every shot emitter; record the first caller only
const WRAP = ['eShoot','eShootT','eMissile','eTwinGuns','eShotAt','eFan','enemyLockOn'];
sb.__hit = null;
for (const n of WRAP) {
  if (typeof sb[n] !== 'function') continue;
  const orig = sb[n];
  sb[n] = function () {
    if (!sb.__hit) {
      let where = '';
      try { throw new Error(); } catch (e) {
        where = String(e.stack).split('\n').slice(2, 6)
          .map(l => { const m = l.match(/at ([A-Za-z0-9_$.]+)/); return m ? m[1] : ''; })
          .filter(Boolean).join(' < ');
      }
      sb.__hit = n + '   via   ' + where;
    }
    return orig.apply(null, arguments);
  };
}
// eBullets.push straight from a tick would bypass the emitters entirely
const origPush = vm.runInContext('eBullets.push', C);
vm.runInContext('eBullets.push=function(){ if(!window.__hit){ try{throw new Error();}catch(e){ window.__hit="eBullets.push   via   "+String(e.stack).split("\\n").slice(2,6).map(function(l){var m=l.match(/at ([A-Za-z0-9_$.]+)/); return m?m[1]:"";}).filter(Boolean).join(" < "); } } return Array.prototype.push.apply(this,arguments); };', C);

const S2 = ['ash','disc','lance','eye','cruc','carrier','skim'];
for (const t of (process.argv[2] ? [process.argv[2]] : ['drone','skimmer','barge','gunboat'])) {
  const st = S2.includes(t) ? 2 : 1;
  sb.__hit = null;
  vm.runInContext(`run.stage=${st}; curStage=STAGES[${st-1}]; enemies.length=0; eBullets.length=0; mapScroll=2200;`+
                  ` try{spawnEnemy(${JSON.stringify(t)},240,120);}catch(e){}`, C);
  if (!vm.runInContext('enemies.length', C)) { console.log('  ' + t + ': did not spawn'); continue; }
  let f = 0;
  for (; f < 300; f++) {
    vm.runInContext('updatePlay(1/60);', C);
    if (vm.runInContext('eBullets.length', C) > 0) break;
    if (!vm.runInContext('enemies.length', C)) break;
  }
  console.log('  ' + t.padEnd(10) + 'frame ' + String(f).padStart(3) + '   ' + (sb.__hit || '(no emitter caught)'));
}
