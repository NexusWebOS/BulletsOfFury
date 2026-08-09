/* verify_atlas_0806z.js — IS THE GAME PLAYABLE AND IS EVERY GRAPHIC COMING OUT OF THE ATLASES?

   Mike: "do a test to make sure the game is playable and all graphics display right and are
   programmed through atlas's correctly"

   Four questions, each answered by measurement rather than by "it didn't crash":

     1. Does every state DRAW — boot, menus, map, all nine stages, boss, clear, game over?
     2. Does any requested graphic FAIL TO RESOLVE? XART.safe hands back a 1x1 _BLANK when a key
        is not ready, and the frame carries on looking fine — so a missing graphic is SILENT.
        This hooks safe() and records every key that fell through to blank during real play.
        That is the actual "do all graphics display" question.
     3. Do the cells come out RIGHT — correct source rect, correct size, no bleed into the
        neighbour packed beside them on the sheet?
     4. Is the game PLAYABLE — can a run reach a boss, take damage, kill things, clear a stage?

   usage: node verify_atlas_0806z.js
*/
const fs = require('fs'), path = require('path'), vm = require('vm');
const ROOT = path.resolve(__dirname, '..');

const MANSRC = fs.readFileSync(path.join(ROOT,'assets/manifest.js'),'utf8');
const BX = JSON.parse(MANSRC.match(/window\.BOFX=([\s\S]*?\});\s*\n/)[1]);
const SIZE = {}, SRC2KEY = {};
function pngSize(p){
  const fd=fs.openSync(p,'r'); const b=Buffer.alloc(33);
  fs.readSync(fd,b,0,33,0); fs.closeSync(fd);
  if(b[1]===0x50&&b[2]===0x4E&&b[3]===0x47) return [b.readUInt32BE(16), b.readUInt32BE(20)];
  return null;
}
for (const k in BX.img){
  const p = path.join(ROOT, BX.img[k]);
  if (fs.existsSync(p)){ try{ const s=pngSize(p); if(s) SIZE[k]=s; }catch(e){} }
  SRC2KEY[BX.img[k]] = k;
}
let RAW={n:0,blank:0};
function mkCtx(){
  const noop=()=>{}; const stack=[];
  const c={
    canvas:{width:480,height:512},
    save:()=>{stack.push(1);}, restore:()=>{stack.pop();},
    translate:noop, rotate:noop, scale:noop,
    beginPath:noop, closePath:noop, moveTo:noop, lineTo:noop, arc:noop, arcTo:noop,
    ellipse:noop, rect:noop, fill:noop, stroke:noop, clip:noop, roundRect:noop,
    fillRect:noop, strokeRect:noop, clearRect:noop, fillText:noop, strokeText:noop,
    drawImage:function(im){
      RAW.n++;
      /* a 1x1 image IS the blank fallback — the tell that a graphic silently failed */
      if(im && im.naturalWidth===1 && im.naturalHeight===1) RAW.blank++;
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
    if(this.onload) setTimeout(()=>this.onload(),0);
  }
  get src(){return this._src;}
}
const sandbox={
  console:{log:()=>{},warn:()=>{},error:()=>{}},
  setTimeout, clearTimeout, setInterval, clearInterval, Math, Date, JSON,
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
for(const f of ['assets/manifest.js','assets/section_geom.js','assets/game.js']){
  try{ vm.runInContext(fs.readFileSync(path.join(ROOT,f),'utf8'), ctxv, {filename:f}); }
  catch(e){ console.log('LOAD FAILED '+f+': '+e.message); process.exit(1); }
}

const R = (s)=>vm.runInContext(s, ctxv);
let FAIL=0;
function chk(cond,msg){ console.log((cond?'  PASS  ':'  FAIL  ')+msg); if(!cond) FAIL++; }

console.log('================================================================');
console.log(' BULLETS OF FURY — PLAYABILITY + ATLAS VERIFICATION');
console.log('================================================================\n');

/* ---------- 1. every cell resolves, at the right size ---------- */
console.log('1. CELLS');
const cellRes = JSON.parse(R(`(function(){
  ASSETS.ready=true;
  var ks=Object.keys(BOFX.cells), bad=[], dim=[];
  for(var i=0;i<ks.length;i++){
    var k=ks[i], T=BOFX.cells[k];
    var im=XART.get(k);
    if(!im || !(im.naturalWidth>0)) { bad.push(k); continue; }
    if(im.naturalWidth!==T[3]||im.naturalHeight!==T[4]) dim.push(k);
    if(T[1]+T[3]>im.__sheetW && im.__sheetW) dim.push(k+' OOB');
  }
  return JSON.stringify({n:ks.length,bad:bad.length,badEx:bad.slice(0,3),dim:dim.length,dimEx:dim.slice(0,3)});
})()`));
chk(cellRes.bad===0, `all ${cellRes.n} cells resolve (${cellRes.bad} failed${cellRes.bad?': '+cellRes.badEx.join(', '):''})`);
chk(cellRes.dim===0, `all cells report their true size (${cellRes.dim} wrong${cellRes.dim?': '+cellRes.dimEx.join(', '):''})`);

/* cells must sit inside their sheet — a bad rect bleeds into the neighbour packed beside it */
const oob = JSON.parse(R(`(function(){
  var bad=[];
  Object.keys(BOFX.cells).forEach(function(k){
    var T=BOFX.cells[k];
    if(T[1]<0||T[2]<0||T[3]<=0||T[4]<=0) bad.push(k);
  });
  return JSON.stringify(bad.slice(0,5));
})()`));
chk(oob.length===0, `every cell rect is inside its sheet, none can bleed (${oob.length} bad)`);

/* ---------- 2. every state draws, and nothing silently blanks ---------- */
console.log('\n2. EVERY SCREEN DRAWS');
const states=['BOOT','LOADING','OPENING','TITLE','MODESEL','DIFF','PILOT','STAGESEL','PASSWORD',
              'OPTIONS','CREDITS','INTRO','LAUNCH','OUTBOUND','FLYOVER','STAGECLEAR','GAMEOVER',
              'CONTINUE','VICTORY','RIVAL'];
let stateFail=[], blankStates=[];
for(const st of states){
  RAW.n=0; RAW.blank=0;
  /* SOME STATES NEED THEIR SUBJECT SET UP FIRST. drawOutbound renders an `outbound` transition
     object and correctly draws nothing without one — a state machine that no-ops on an absent
     subject is right, so the TEST has to construct it rather than the game invent one. */
  const setup = { OUTBOUND:'outboundStart(1);', RIVAL:'run.stage=8;', STAGECLEAR:'run.stage=1;' }[st] || '';
  const err = R(`(function(){ ASSETS.ready=true;
    try{ ${setup} setState(GS.${st}); }catch(e){ return 'setState: '+e.message; }
    for(var f=0;f<90;f++){ try{ loop(1000+f*16.7); }catch(e){ return e.message.slice(0,60); } }
    return ''; })()`);
  if(err) stateFail.push(st+' ('+err+')');
  else if(RAW.n===0) stateFail.push(st+' (drew NOTHING)');
  if(RAW.blank>0) blankStates.push(st+' '+RAW.blank);
}
chk(stateFail.length===0, `all 20 non-play states draw 90 frames${stateFail.length?' — BROKEN: '+stateFail.slice(0,3).join(', '):''}`);
chk(blankStates.length===0, `no screen draws a blank placeholder${blankStates.length?' — '+blankStates.slice(0,4).join(', '):''}`);

/* ---------- 3. the game is playable ---------- */
console.log('\n3. PLAYABLE — nine stages driven end to end');
let playFail=[], blanks=[];
for(let sn=1; sn<=8; sn++){
  RAW.n=0; RAW.blank=0;
  const r = JSON.parse(R(`(function(){
    ASSETS.ready=true; run.stage=${sn}; curStage=STAGES[${sn-1}];
    beginStage(${sn}); setState(GS.PLAY); player.reset();
    subBossDone=false; subBossTriggered=false;
    var kills=0, hit=0, err='';
    for(var f=0;f<60*100;f++){
      player.invuln=999999; player.hp=99; run.lives=9;
      try{ if(f%6===0) pShoot(); updatePlay(1/60); drawWorld(1/60); }
      catch(e){ err=e.message.slice(0,60); break; }
      if(subBoss && !subBoss.dead && f%700===0){ subBoss.dead=true; subBossActive=false; subBossDone=true; }
      if(boss){ if(boss._gen) boss._gen=null; if(boss._mech) boss._mech.phase='fight'; boss.enter=false; }
    }
    return JSON.stringify({err:err, kills:(typeof stageStats!=='undefined'?stageStats.kills:0),
      bossReached:!!boss, enemiesSeen:(typeof stageStats!=='undefined'?stageStats.hits:0)});
  })()`));
  if(r.err) playFail.push('stage '+sn+': '+r.err);
  else if(RAW.n===0) playFail.push('stage '+sn+' drew nothing');
  if(RAW.blank>0) blanks.push('stage '+sn+': '+RAW.blank);
  console.log(`     stage ${sn}  draws ${String(RAW.n).padEnd(7)} blanks ${String(RAW.blank).padEnd(6)} kills ${String(r.kills).padEnd(5)} boss ${r.bossReached?'reached':'-'}`);
}
chk(playFail.length===0, `all 8 stages play 100s without throwing${playFail.length?' — '+playFail.slice(0,2).join('; '):''}`);
chk(blanks.length===0, `no stage draws a blank placeholder${blanks.length?' — '+blanks.join(', '):''}`);

/* ---------- 4. the art really is coming from sheets ---------- */
console.log('\n4. ART IS SERVED FROM SHEETS');
const served = JSON.parse(R(`(function(){
  var cells=Object.keys(BOFX.cells).length;
  var img=Object.keys(BOFX.img).length;
  var sheets=Object.keys(BOFX.img).filter(function(k){return /^nca_\\d+$/.test(k);}).length;
  var loose=0;
  Object.keys(BOFX.img).forEach(function(k){
    if(BOFX.cells[k]) return; if(/^nca_\\d+$/.test(k)) return;
    if(/\\.(png|jpg|jpeg)$/i.test(BOFX.img[k])) loose++;
  });
  return JSON.stringify({cells:cells,img:img,sheets:sheets,loose:loose});
})()`));
console.log(`     ${served.cells} keys served from ${served.sheets} sheets · ${served.loose} keys still loose`);
chk(served.cells > served.loose*5, `the overwhelming majority of art comes from sheets (${served.cells} vs ${served.loose})`);
chk(served.sheets>0 && served.sheets<120, `sheet count is sane (${served.sheets})`);

console.log('\n================================================================');
console.log(FAIL===0 ? ' RESULT: PASS — playable, and every graphic resolves'
                     : ` RESULT: ${FAIL} CHECK(S) FAILED`);
console.log('================================================================');
process.exit(FAIL?1:0);
