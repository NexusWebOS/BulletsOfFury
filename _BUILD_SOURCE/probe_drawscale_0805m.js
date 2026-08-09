/* probe_drawscale_0805m.js — WHERE IS THE 2.9 GB ACTUALLY GOING?

   The box/pill atlas (0805l) got 7.9x not from packing but from the discovery that the art was
   stored ~10x larger than it is ever drawn. That was one folder. This asks the same question of
   the whole library, from real gameplay rather than from guesswork.

   For every drawImage during a driven playthrough of all nine stages it records the DRAWN
   rectangle against the STORED rectangle, then reports the keys wasting the most decoded RAM.

   drawImage has three signatures and only the middle one was handled by the older probes:
       drawImage(im, dx, dy)                                  -> drawn at natural size
       drawImage(im, dx, dy, dw, dh)                          -> dw,dh is the draw size
       drawImage(im, sx, sy, sw, sh, dx, dy, dw, dh)          -> the LAST pair is the draw size
   Reading arguments 4 and 5 on a 9-arg call gives the SOURCE rect, which would have made every
   atlas blit look correctly sized. arguments.length is the only safe discriminator.

   usage: node probe_drawscale_0805m.js
*/
const fs = require('fs'), path = require('path'), vm = require('vm');
const ROOT = path.resolve(__dirname, '..');

const MAN = JSON.parse(fs.readFileSync(path.join(ROOT,'assets/manifest.js'),'utf8')
  .match(/window\.BOFX=([\s\S]*?\});/)[1]);
const SIZE = {}, SRC2KEY = {};
function pngSize(p){
  const fd=fs.openSync(p,'r'); const b=Buffer.alloc(33);
  fs.readSync(fd,b,0,33,0); fs.closeSync(fd);
  if(b[1]===0x50&&b[2]===0x4E&&b[3]===0x47) return [b.readUInt32BE(16), b.readUInt32BE(20)];
  return null;
}
for (const k in MAN.img){
  const p = path.join(ROOT, MAN.img[k]);
  if (fs.existsSync(p)){ try{ const s=pngSize(p); if(s) SIZE[k]=s; }catch(e){} }
  SRC2KEY[MAN.img[k]] = k;
}

const STAT = {};            // key -> {n, maxDW, maxDH, w, h}
let recording = false;
function note(key, dw, dh){
  if(!key) return;
  let s = STAT[key];
  if(!s){ const d=SIZE[key]||[0,0]; s=STAT[key]={n:0,maxDW:0,maxDH:0,w:d[0],h:d[1]}; }
  s.n++;
  if(dw>s.maxDW) s.maxDW=dw;
  if(dh>s.maxDH) s.maxDH=dh;
}

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
    drawImage:function(im){
      if(!recording) return;
      const key=(im&&im.__key)||null;
      let dw,dh;
      /* THE SIGNATURE MATTERS. On a 9-arg call arguments[3],[4] are the SOURCE rect — reading
         those would make every atlas blit look perfectly sized and hide the very thing this
         probe exists to find. */
      if(arguments.length>=9){ dw=arguments[7]; dh=arguments[8]; }
      else if(arguments.length>=5){ dw=arguments[3]; dh=arguments[4]; }
      else { dw=(im&&(im.naturalWidth||im.width))||0; dh=(im&&(im.naturalHeight||im.height))||0; }
      note(key, Math.abs(dw)||0, Math.abs(dh)||0);
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
vm.runInContext(`Object.keys(window.BOFX.img).forEach(function(k){ try{ XART._touch(k); }catch(e){} });`, ctxv);

// ---- drive every stage, with and without a boss, so as much art as possible is exercised
recording = true;
for (let sn=1; sn<=9; sn++){
  try{
    vm.runInContext(`
      ASSETS.ready=true;
      run.stage=${sn}; curStage=STAGES[${Math.min(sn,8)-1}];
      beginStage(${Math.min(sn,8)}); setState(GS.PLAY); player.reset();
      subBossDone=false; subBossTriggered=false;
      for(var f=0; f<60*95; f++){
        player.invuln=999999; player.hp=99; run.lives=9;
        if(f%7===0) pShoot();
        updatePlay(1/60); drawWorld(1/60);
        if(subBoss && !subBoss.dead && f%600===0){ subBoss.dead=true; subBossActive=false; subBossDone=true; }
        if(boss){ if(boss._gen) boss._gen=null; if(boss._mech) boss._mech.phase='fight'; boss.enter=false; }
      }
    `, ctxv);
  }catch(e){ console.error('stage '+sn+': '+e.message); }
}
recording = false;

// ---- report
const rows = Object.keys(STAT).map(k=>{
  const s=STAT[k];
  if(!s.w||!s.h||!s.maxDW||!s.maxDH) return null;
  const stored=s.w*s.h, drawn=s.maxDW*s.maxDH;
  return {k, n:s.n, w:s.w, h:s.h, dw:Math.round(s.maxDW), dh:Math.round(s.maxDH),
          ratio:stored/Math.max(1,drawn), wasteMB:(stored-Math.min(stored,drawn*4))*4/1e6, storedMB:stored*4/1e6};
}).filter(Boolean);

console.log('keys observed drawing: ' + rows.length);
console.log('');
console.log('OVERSIZED ART — stored much larger than it is ever drawn');
console.log('(cap suggestion = 2x the largest drawn size, the rule that gave 7.9x on the box/pill sheet)');
console.log('');
console.log('  storedMB  stored px    max drawn   ratio   draws  key');
console.log('  --------  -----------  ----------  ------  -----  ---------------------------');
rows.sort((a,b)=>b.wasteMB-a.wasteMB);
for(const r of rows.slice(0,30)){
  console.log('  '+r.storedMB.toFixed(2).padStart(8)+'  '+
    (r.w+'x'+r.h).padEnd(13)+(r.dw+'x'+r.dh).padEnd(12)+
    (r.ratio.toFixed(1)+'x').padEnd(8)+String(r.n).padEnd(7)+r.k);
}

// family roll-up: where the recoverable memory actually sits
const fam={};
for(const r of rows){
  const f=r.k.replace(/[0-9]+$/,'').replace(/_[0-9]+_[0-9]+$/,'').replace(/_$/,'');
  const g=fam[f]||(fam[f]={storedMB:0,save:0,n:0,worst:0});
  g.storedMB+=r.storedMB; g.n++;
  if(r.ratio>2){ g.save += r.storedMB*(1-1/Math.min(r.ratio,64)*4); }
  if(r.ratio>g.worst) g.worst=r.ratio;
}
const fr=Object.keys(fam).map(f=>({f,...fam[f]})).filter(x=>x.storedMB>0.4);
fr.sort((a,b)=>b.storedMB-a.storedMB);
console.log('');
console.log('BY FAMILY (only families over 0.4 MB of observed decoded art)');
console.log('  storedMB   keys  worst ratio  family');
console.log('  --------   ----  -----------  -------------------------');
for(const g of fr.slice(0,22)){
  console.log('  '+g.storedMB.toFixed(2).padStart(8)+'   '+String(g.n).padEnd(6)+
    (g.worst.toFixed(1)+'x').padEnd(13)+g.f);
}
fs.writeFileSync('/tmp/drawscale.json', JSON.stringify(rows));
const totStored=rows.reduce((a,r)=>a+r.storedMB,0);
const over2=rows.filter(r=>r.ratio>=2), over4=rows.filter(r=>r.ratio>=4);
console.log('');
console.log('observed decoded total : '+totStored.toFixed(1)+' MB across '+rows.length+' keys');
console.log('  stored >=2x drawn    : '+over2.length+' keys, '+over2.reduce((a,r)=>a+r.storedMB,0).toFixed(1)+' MB');
console.log('  stored >=4x drawn    : '+over4.length+' keys, '+over4.reduce((a,r)=>a+r.storedMB,0).toFixed(1)+' MB');
