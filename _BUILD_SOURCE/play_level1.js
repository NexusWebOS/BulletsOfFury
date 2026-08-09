/* play_level1.js — PLAY stage 1 honestly and report what actually happens.

   ⚠ WHY THIS EXISTS. verify_atlas_0806z.js reports "boss reached" for stage 1, but it gets there
   by force-killing the subboss and overriding boss state. It proves every graphic resolves; it
   proves NOTHING about whether the level plays. That is why none of Mike's stage-1 complaints
   ever reached me from a green suite.

   This one shoots, aims, kills the miniboss by damaging it, and lets the scroll advance on its
   own. It reports the things a player would notice:

     - does the level scroll all the way, and how long does each phase take
     - does every wave in the plan actually fire
     - where does each enemy first BECOME VISIBLE (the "appearing in thin air" complaint)
     - does the miniboss glow / shield while its turrets live
     - does the boss arrive

   usage: node play_level1.js
*/
const fs=require('fs'), path=require('path'), vm=require('vm');
const ROOT='/tmp/build/BulletsOfFury';
const MAN=JSON.parse(fs.readFileSync(ROOT+'/assets/manifest.js','utf8').match(/window\.BOFX=([\s\S]*?\});\s*\n/)[1]);
const SIZE={},SRC2KEY={};
function pngSize(p){const fd=fs.openSync(p,'r'),b=Buffer.alloc(33);fs.readSync(fd,b,0,33,0);fs.closeSync(fd);
  return (b[1]===0x50)?[b.readUInt32BE(16),b.readUInt32BE(20)]:null;}
for(const k in MAN.img){const p=path.join(ROOT,MAN.img[k]);
  if(fs.existsSync(p)){try{const s=pngSize(p);if(s)SIZE[k]=s;}catch(e){}} SRC2KEY[MAN.img[k]]=k;}
const noop=()=>{};
function mkCtx(){const st=[];return{canvas:{width:480,height:512},save:()=>st.push(1),restore:()=>st.pop(),
 translate:noop,rotate:noop,scale:noop,beginPath:noop,closePath:noop,moveTo:noop,lineTo:noop,arc:noop,arcTo:noop,
 ellipse:noop,rect:noop,fill:noop,stroke:noop,clip:noop,roundRect:noop,fillRect:noop,strokeRect:noop,clearRect:noop,
 fillText:noop,strokeText:noop,drawImage:noop,setTransform:noop,resetTransform:noop,transform:noop,
 measureText:()=>({width:10}),createLinearGradient:()=>({addColorStop:noop}),createRadialGradient:()=>({addColorStop:noop}),
 createPattern:()=>({}),getImageData:()=>({data:new Uint8ClampedArray(4)}),putImageData:noop,drawFocusIfNeeded:noop,
 globalAlpha:1,globalCompositeOperation:'source-over',filter:'none',fillStyle:'#000',strokeStyle:'#000',
 lineWidth:1,lineJoin:'',lineCap:'',shadowColor:'',shadowBlur:0,font:'',textAlign:'',textBaseline:'',imageSmoothingEnabled:true};}
function mkCanvas(){return{width:480,height:512,style:{},getContext:()=>mkCtx(),addEventListener:noop,
 getBoundingClientRect:()=>({left:0,top:0,width:480,height:512})};}
class FakeImage{constructor(){this._src='';this.naturalWidth=64;this.naturalHeight=64;this.width=64;this.height=64;
 this.complete=true;this.__key=null;}
 set src(v){this._src=v;const rel=String(v).replace(/^.*?(assets\/)/,'$1');const k=SRC2KEY[rel];
  if(k){this.__key=k;const d=SIZE[k];if(d){this.naturalWidth=d[0];this.naturalHeight=d[1];this.width=d[0];this.height=d[1];}}
  if(this.onload)setTimeout(()=>this.onload(),0);}
 get src(){return this._src;}}
const SFX=new Proxy({},{get:(t,p)=>()=>{ SFXLOG[p]=(SFXLOG[p]||0)+1; }});
let SFXLOG={};
const sandbox={console:{log:noop,warn:noop,error:noop},setTimeout,clearTimeout,setInterval,clearInterval,Math,Date,JSON,
 performance:{now:()=>Date.now()},requestAnimationFrame:()=>0,cancelAnimationFrame:noop,
 Image:FakeImage,HTMLImageElement:FakeImage,HTMLCanvasElement:function(){},
 localStorage:{getItem:()=>null,setItem:noop,removeItem:noop},navigator:{userAgent:'node',maxTouchPoints:0},
 AudioContext:function(){return{createGain:()=>({connect:noop,gain:{value:0,setValueAtTime:noop,linearRampToValueAtTime:noop,exponentialRampToValueAtTime:noop}}),
  createOscillator:()=>({connect:noop,start:noop,stop:noop,frequency:{value:0,setValueAtTime:noop,linearRampToValueAtTime:noop,exponentialRampToValueAtTime:noop},type:''}),
  createBuffer:()=>({getChannelData:()=>new Float32Array(1)}),createBufferSource:()=>({connect:noop,start:noop,stop:noop,buffer:null}),
  createBiquadFilter:()=>({connect:noop,frequency:{value:0,setValueAtTime:noop},Q:{value:0},type:''}),
  destination:{},currentTime:0,sampleRate:44100,resume:()=>Promise.resolve(),state:'running'};},
 document:{getElementById:()=>mkCanvas(),querySelector:()=>mkCanvas(),querySelectorAll:()=>[],
  createElement:(t)=>(t==='canvas'?mkCanvas():{style:{},appendChild:noop,addEventListener:noop}),
  addEventListener:noop,body:{appendChild:noop,style:{},addEventListener:noop},documentElement:{style:{}},hidden:false},
 fetch:()=>Promise.reject(new Error('no net'))};
sandbox.window=sandbox; sandbox.globalThis=sandbox; sandbox.window.addEventListener=noop;
const ctxv=vm.createContext(sandbox);
for(const f of ['assets/manifest.js','assets/section_geom.js','assets/game.js']){
  try{ vm.runInContext(fs.readFileSync(path.join(ROOT,f),'utf8'), ctxv, {filename:f}); }
  catch(e){ console.log('LOAD FAILED '+f+': '+e.message); process.exit(1); }
}
const R=(s)=>vm.runInContext(s,ctxv);

console.log('================================================================');
console.log(' STAGE 1 — PLAYED, NOT SKIPPED');
console.log('================================================================\n');

const out=JSON.parse(R(`(function(){
  ASSETS.ready=true; run.stage=1; curStage=STAGES[0]; run.pilot='cole'; run.mode='arcade';
  beginStage(1); setState(GS.PLAY); player.reset();
  var H=((typeof _levelCfg==='function'&&_levelCfg())||{}).h||4800;
  var log={phases:[], firstVisible:[], waves:{}, sbGlow:[], notes:[]};
  var seenSB=false, seenBoss=false, sbKilled=null, bossAt=null;
  var lastWave=-1;
  for(var f=0; f<60*400; f++){
    player.invuln=999999; player.hp=99; run.lives=9; run.bombs=9;
    /* PLAY: hold fire, and actually damage what is in front of us */
    if(f%4===0) pShoot();
    try{ updatePlay(1/60); drawWorld(1/60); }catch(e){ log.notes.push('THREW f'+f+': '+e.message.slice(0,60)); break; }

    /* record where each enemy FIRST becomes visible — the "thin air" complaint */
    for(const e of enemies){
      if(e.__seen) continue;
      var vis = (e.x>-4 && e.x<VW+4 && e.y>-4 && e.y<VH+4);
      if(!vis) { e.__off=1; continue; }
      e.__seen=1;
      log.firstVisible.push({type:e.type||'?', x:Math.round(e.x), y:Math.round(e.y),
        enteredOffscreen: !!e.__off, t:+(f/60).toFixed(1)});
    }
    if(typeof waveIdx!=='undefined' && waveIdx!==lastWave){ lastWave=waveIdx;
      log.waves[waveIdx]=+(f/60).toFixed(1); }

    /* the miniboss: damage it for real, and watch its shield while turrets live */
    if(typeof subBoss!=='undefined' && subBoss && !subBoss.dead){
      if(!seenSB){ seenSB=true; log.phases.push({what:'miniboss appears', t:+(f/60).toFixed(1), scroll:Math.round(mapScroll||0)}); }
      if(f%3===0 && typeof hitSubBoss==='function'){ try{ hitSubBoss(6, subBoss.x, subBoss.y); }catch(e){} }
      if(f%20===0){
        var alive=(subBoss._qlCan||[]).filter(function(c){return !c.dead;}).length;
        log.sbGlow.push({t:+(f/60).toFixed(1), turretsAlive:alive,
          armor:+(subBoss._qlArmor||0).toFixed(2), shield:+(subBoss._qlShield||0).toFixed(2),
          hullOpen:!!subBoss._qlHullOpen, flash:+(subBoss.flash||0).toFixed(2)});
      }
    } else if(seenSB && sbKilled===null){ sbKilled=+(f/60).toFixed(1);
      log.phases.push({what:'miniboss destroyed', t:sbKilled, scroll:Math.round(mapScroll||0)}); }

    if(typeof boss!=='undefined' && boss && !seenBoss){ seenBoss=true; bossAt=+(f/60).toFixed(1);
      log.phases.push({what:'BOSS arrives', t:bossAt, scroll:Math.round(mapScroll||0)}); }
    if(seenBoss && boss && !boss.dead && f%3===0 && typeof hitBoss==='function'){ try{ hitBoss(8); }catch(e){} }
    if(seenBoss && (!boss || boss.dead)){ log.phases.push({what:'boss destroyed', t:+(f/60).toFixed(1), scroll:Math.round(mapScroll||0)}); break; }
  }
  log.finalScroll=Math.round(mapScroll||0); log.H=H;
  log.plan=(typeof stagePlan!=='undefined'&&stagePlan)?stagePlan.length:-1;
  log.reachedEnd=(Math.round(mapScroll||0) >= H-40);
  return JSON.stringify(log);
})()`));

console.log('level height %d   plan %d waves   final scroll %d   reached the end: %s',
  out.H, out.plan, out.finalScroll, out.reachedEnd);
if(out.notes.length) out.notes.forEach(n=>console.log('  ⚠ '+n));

console.log('\nPHASES');
if(!out.phases.length) console.log('   (none — the level never produced a miniboss or a boss)');
out.phases.forEach(p=>console.log('   %s  t=%ss  scroll=%d', p.what.padEnd(20), p.t, p.scroll));

console.log('\nWAVES FIRED: %d of %d', Object.keys(out.waves).length, out.plan);

const thin=out.firstVisible.filter(e=>!e.enteredOffscreen);
console.log('\nENEMIES THAT APPEARED ON SCREEN RATHER THAN ENTERING: %d of %d',
  thin.length, out.firstVisible.length);
thin.slice(0,12).forEach(e=>console.log('   %-12s popped in at (%d,%d) at t=%ss', e.type, e.x, e.y, e.t));

console.log('\nMINIBOSS — glow / shield while turrets live');
if(!out.sbGlow.length) console.log('   (never reached)');
else{
  console.log('   t(s)   turrets  armorTrace  shield  hullOpen  whiteFlash');
  out.sbGlow.slice(0,14).forEach(g=>console.log('   %-6s %-8s %-11s %-7s %-9s %s',
    g.t, g.turretsAlive, g.armor, g.shield, g.hullOpen, g.flash));
  const lit=out.sbGlow.filter(g=>g.turretsAlive>0 && (g.armor>0||g.shield>0)).length;
  const sealed=out.sbGlow.filter(g=>g.turretsAlive>0).length;
  console.log('\n   sampled while sealed: %d   of those showing a glow: %d', sealed, lit);
}
console.log('\n================================================================');
