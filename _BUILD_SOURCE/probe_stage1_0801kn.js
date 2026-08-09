/* probe_stage1_0801kn.js — MEASURE WHAT STAGE 1 ACTUALLY DOES

   Mike, again: sideways bullets instead of machine guns, circular loops he has
   banned twice, jets entering from a side edge but facing south, tanks in the
   wrong place, turrets he cannot reach.

   Every one of those has been "fixed" before by reading code. This does not read
   code. It boots the real game, runs stage 1 forward frame by frame, and records
   for every enemy that spawns:

     type, pattern, spawn point, whether it ever fires
     the path it walks (so a circular loop is detected as a loop, by measuring
       total heading change - a full circle is 360 degrees of turn)
     its drawn facing angle vs its actual direction of travel
     every projectile it emits: kind, direction, speed

   Output is JSON. Nothing here trusts a table; a wave that is authored but never
   reached, or a pattern that is overwritten after spawn, shows up as the measured
   value being different from the authored one.

   usage: node probe_stage1_0801kn.js [stageNum] > /tmp/stage1.json
*/
const fs = require('fs'), path = require('path'), vm = require('vm');
const ROOT = path.resolve(__dirname, '..');
const STAGE = parseInt(process.argv[2] || '1', 10);
const SECS  = parseInt(process.argv[3] || '95', 10);
const FIGHT = process.argv.indexOf('--fight')>=0;

const MAN = JSON.parse(fs.readFileSync(path.join(ROOT, 'assets/manifest.js'), 'utf8')
  .match(/window\.BOFX=([\s\S]*?\});/)[1]);
const SIZE = {}, SRC2KEY = {};
function pngSize(p) {
  try { const b = fs.readFileSync(p);
    if (b.length > 24 && b[12] === 0x49 && b[13] === 0x48) return [b.readUInt32BE(16), b.readUInt32BE(20)];
  } catch (e) {}
  return [64, 64];
}
for (const k in MAN.img) { const p = path.join(ROOT, MAN.img[k]);
  if (fs.existsSync(p)) SIZE[k] = pngSize(p);
  SRC2KEY[MAN.img[k]] = k; }

function mkCtx() {
  const noop = () => {}; const stack = [];
  const c = { canvas: { width: 480, height: 512 },
    save: () => stack.push({ a: c.globalAlpha }), restore: () => { const s = stack.pop(); if (s) c.globalAlpha = s.a; },
    translate: noop, rotate: noop, scale: noop, beginPath: noop, closePath: noop, moveTo: noop,
    lineTo: noop, arc: noop, arcTo: noop, ellipse: noop, rect: noop, fill: noop, stroke: noop,
    clip: noop, roundRect: noop, fillRect: noop, strokeRect: noop, clearRect: noop, fillText: noop,
    strokeText: noop, drawImage: noop, setTransform: noop, resetTransform: noop, transform: noop,
    measureText: () => ({ width: 10 }),
    createLinearGradient: () => ({ addColorStop: noop }), createRadialGradient: () => ({ addColorStop: noop }),
    createPattern: () => ({}), getImageData: () => ({ data: new Uint8ClampedArray(4) }), putImageData: noop,
    globalAlpha: 1, globalCompositeOperation: 'source-over', filter: 'none', fillStyle: '#000',
    strokeStyle: '#000', lineWidth: 1, lineJoin: '', lineCap: '', shadowColor: '', shadowBlur: 0,
    font: '', textAlign: '', textBaseline: '', imageSmoothingEnabled: true };
  return c;
}
function mkCanvas() { return { width: 480, height: 512, style: {}, getContext: () => mkCtx(),
  addEventListener: () => {}, getBoundingClientRect: () => ({ left: 0, top: 0, width: 480, height: 512 }) }; }
class FakeImage {
  constructor(){ this._src=''; this.naturalWidth=64; this.naturalHeight=64; this.width=64; this.height=64; this.complete=true; this.__key=null; }
  set src(v){ this._src=v; const rel=String(v).replace(/^.*?(assets\/)/,'$1'); const k=SRC2KEY[rel];
    if(k){ this.__key=k; const d=SIZE[k]; if(d){ this.naturalWidth=d[0]; this.naturalHeight=d[1]; this.width=d[0]; this.height=d[1]; } }
    if(this.onload) setTimeout(()=>this.onload(),0); }
  get src(){ return this._src; }
}
const AC = function(){ return {
  createGain:()=>({connect:()=>{},gain:{value:0,setValueAtTime:()=>{},linearRampToValueAtTime:()=>{},exponentialRampToValueAtTime:()=>{}}}),
  createOscillator:()=>({connect:()=>{},start:()=>{},stop:()=>{},frequency:{value:0,setValueAtTime:()=>{},linearRampToValueAtTime:()=>{},exponentialRampToValueAtTime:()=>{}},type:''}),
  createBuffer:()=>({getChannelData:()=>new Float32Array(1)}), createBufferSource:()=>({connect:()=>{},start:()=>{},stop:()=>{},buffer:null}),
  createBiquadFilter:()=>({connect:()=>{},frequency:{value:0,setValueAtTime:()=>{}},Q:{value:0},type:''}),
  destination:{}, currentTime:0, sampleRate:44100, resume:()=>Promise.resolve(), state:'running' }; };
const sandbox = { console, setTimeout, clearTimeout, setInterval, clearInterval, Math, Date, JSON,
  performance:{now:()=>Date.now()}, requestAnimationFrame:()=>0, cancelAnimationFrame:()=>{},
  Image: FakeImage, HTMLImageElement: FakeImage, HTMLCanvasElement: function(){},
  localStorage:{getItem:()=>null,setItem:()=>{},removeItem:()=>{}},
  navigator:{userAgent:'node',maxTouchPoints:0}, AudioContext: AC, webkitAudioContext: AC,
  document:{ getElementById:()=>mkCanvas(), querySelector:()=>mkCanvas(), querySelectorAll:()=>[],
    createElement:(t)=>(t==='canvas'?mkCanvas():{style:{},appendChild(){},addEventListener(){}}),
    addEventListener:()=>{}, body:{appendChild(){},style:{},addEventListener(){}},
    documentElement:{style:{}}, hidden:false },
  fetch:()=>Promise.reject(new Error('no net')) };
sandbox.window = sandbox; sandbox.globalThis = sandbox; sandbox.window.addEventListener = () => {};
const ctxv = vm.createContext(sandbox);
function run(f){ try{ vm.runInContext(fs.readFileSync(path.join(ROOT,f),'utf8'), ctxv, {filename:f}); }
  catch(e){ console.error('[load '+f+'] '+e.message); process.exit(1); } }
run('assets/manifest.js'); run('assets/section_geom.js'); run('assets/game.js');

/* Drive the stage forward. The director is time-based, so the clock is advanced
   and the plan pumped exactly the way updatePlay does, without rendering. */
const result = vm.runInContext(`
(function(){
  var SECS=`+SECS+`, FIGHT=`+(FIGHT?1:0)+`;
  var _T=0; var PROBES=[]; var ARG_SECS=SECS; var ARG_FIGHT=FIGHT;
  var OUT={stage:${STAGE}, scrollTrace:[], enemies:{}, shots:[], patternsSeen:{}, spawnCalls:[], notes:[]};

  // ---- record every spawn, with the pattern it ENDED UP with (not the authored one)
  var _origSpawn = spawnEnemy;
  spawnEnemy = function(type,x,y,opt){
    var e = _origSpawn.apply(null, arguments);
    var got = enemies[enemies.length-1];
    OUT.spawnCalls.push({t:+(_T||0).toFixed(2), type:type, x:Math.round(x), y:Math.round(y),
                         askedPattern:(opt&&opt.pattern)||null,
                         gotPattern: got?got.pattern:null,
                         shoots: got?!!got.shoots:null,
                         fk: got?(got.fk||null):null});
    if(got){ PROBES.push(got.__probe={type:type, sx:x, sy:y, path:[], turn:0, net:0, lastAng:null, fired:0,
                         pattern:got.pattern, faceSamples:[]}); }
    return e;
  };

  // ---- attribute every shot to the enemy that fired it. Wrapping eShoot is the
  // only reliable way: bullets carry no source field.
  /* ATTRIBUTE BY ORIGIN, NOT BY A CURSOR. An earlier version set a _CUR variable
     from the per-enemy loop, but shots are emitted INSIDE updatePlay, before that
     loop runs, so _CUR was always one frame stale and pointed at the wrong enemy.
     A bullet spawns at its firer's position, so the nearest enemy to (x,y) at the
     moment of the call is the firer. Ties beyond 40px are recorded as unknown
     rather than guessed. */
  function _nearest(x,y){
    var best=null,bd=1e9;
    for(var i=0;i<enemies.length;i++){ var e=enemies[i];
      var dd=Math.hypot(e.x-x,e.y-y); if(dd<bd){bd=dd;best=e;} }
    if(best&&bd<40) return (best.__probe?best.__probe.type:best.type)||'?';
    if(typeof subBoss!=='undefined'&&subBoss&&Math.hypot(subBoss.x-x,subBoss.y-y)<160) return 'SUBBOSS';
    if(typeof boss!=='undefined'&&boss&&Math.hypot(boss.x-x,boss.y-y)<200) return 'BOSS';
    return 'unknown';
  }
  var _CUR=null;
  var _oShoot=eShoot;
  eShoot=function(x,y,ang,spd,kind){ var r=_oShoot.apply(null,arguments);
    var b=eBullets[eBullets.length-1]; if(b) b.__src=_nearest(x,y); return r; };
  if(typeof eTwinGuns==='function'){ var _oTwin=eTwinGuns;
    eTwinGuns=function(e,a){ _CUR=(e&&e.__probe)?e.__probe.type:(e&&e.type)||'?'; var n0=eBullets.length; var r=_oTwin.apply(null,arguments); for(var q=n0;q<eBullets.length;q++) eBullets[q].__src=_CUR; return r; }; }
  if(typeof eMissile==='function'){ var _oMis=eMissile;
    eMissile=function(){ var r=_oMis.apply(null,arguments);
      var b=eBullets[eBullets.length-1]; if(b) b.__src=_CUR; return r; }; }

  // ---- record every enemy projectile
  var _shotSeen={};
  function snapshotShots(){
    for(var i=0;i<eBullets.length;i++){
      var b=eBullets[i];
      if(b.__seen) continue; b.__seen=1;
      /* ovTwinMG and friends push straight into eBullets, bypassing eShoot, so those
         rounds arrive with no source. Attribute them at first sight instead — a bullet
         is still sitting on its muzzle the frame it appears. */
      if(!b.__src) b.__src=_nearest(b.x,b.y);
      var sp=Math.hypot(b.vx||0,b.vy||0);
      OUT.shots.push({kind:b.kind||'?', vx:+(b.vx||0).toFixed(2), vy:+(b.vy||0).toFixed(2),
                      spd:+sp.toFixed(2),
                      dir: Math.abs(b.vx||0) > Math.abs(b.vy||0)*1.5 ? 'SIDEWAYS' :
                           ((b.vy||0) > 0 ? 'down' : 'up'),
                      w:b.w||null, from:b.__src||null});
    }
  }

  run.stage=${STAGE}; curStage=STAGES[${STAGE}-1];
  beginStage(${STAGE});
  state='play';
  player.x=240; player.y=400;
  var dt=1/60, T=0; _T=0;
  /* THE LEVEL HAS TO SCROLL (drop 0801kn). mapScroll is advanced inside
     drawLevelMaster, NOT inside updatePlay — scroll progression is coupled to the
     draw path. Skipping rendering therefore froze mapScroll at 0, every terrain-gated
     ground wave refused forever, and the plan stalled at wave 6 of 15. That is why
     the tanks could never be measured and the boss was never reached.

     drawLevelMaster is called for real rather than incrementing a counter, so the
     probe inherits the actual rules — including the boss-hold that slows scroll to a
     stop during a miniboss. A faked number would have got the pacing wrong in exactly
     the place the tanks are timed to. */
  var _stall=0;
  for(var f=0; f<60*ARG_SECS; f++){
    T+=dt; _T=T;
    try{ drawLevelMaster(dt); }catch(e){ if(OUT.notes.length<6) OUT.notes.push('drawLevelMaster: '+e.message); }
    if(f%60===0) OUT.scrollTrace.push([Math.round(T), Math.round(typeof mapScroll!=='undefined'?mapScroll:-1), waveIdx]);
    try{ updatePlay(dt); }catch(e){ if(OUT.notes.length<6) OUT.notes.push('updatePlay: '+e.message); }
    /* THE PROBE HAS TO FIGHT. The level correctly stops scrolling while a miniboss is
       alive (the _bossHold rule in drawLevelMaster), so a probe that never shoots
       parks at the miniboss forever and can never reach the boss. Damage is applied
       through the real hitSubBoss/hitBoss entry points, aimed at each live section in
       turn, so the sectional destruction path is exercised rather than bypassed. */
    if(ARG_FIGHT){
      /* A PROBE THAT NEVER SHOOTS IS NOT A PLAYER. The dispatcher only releases the
         next wave while _liveN <= _dispatchAt, so enemies left alive pile up and the
         queue stalls — waveIdx sat at 7 of 15 for 200s and I nearly filed that as a
         game bug. It is an artifact of a probe that kills nothing. Regular enemies are
         cleared on a steady cadence so the level advances the way it does for a player
         who is actually fighting. */
      if(f%14===0){
        for(var _q=0;_q<enemies.length;_q++){
          var _e=enemies[_q];
          if(_e.dead||_e._tur||_e._bunker||_e._mini) continue;
          _e.hp=(_e.hp||1)-9;
          if(_e.hp<=0){ _e.dead=true; OUT.killed=(OUT.killed||0)+1; }
          break;                                   // one at a time, not a screen-clear
        }
      }
      if(typeof subBoss!=='undefined' && subBoss && subBossActive && !subBoss.dead && f%6===0){
        var _G=(typeof sxPackGeom==='function'&&subBoss._sx)?sxPackGeom(subBoss._sx.code):null;
        if(_G){ var _ks=Object.keys(_G.sections), _c=_G.sections[_ks[(f/6|0)%_ks.length]].c;
                hitSubBoss(14, subBoss.x+_c[0]*subBoss.w, subBoss.y+_c[1]*subBoss.h); }
        else if(subBoss._ql && subBoss._qlCan && subBoss._qlCan.length){
          /* THE QUADLASER SEALS ITS HULL until all four cannons are dead, so hitting the
             centre does literally nothing — hp sat at 185/185 for 200 seconds. The
             cannons carry their own hb boxes in the 384px SPRITE's space, so the probe
             converts one to world coords and hits THAT, the same way a player must. */
          var _SPR=384, _sc=(subBoss.w||196)/_SPR;
          var _live=subBoss._qlCan.filter(function(c){return !c.dead && c.hb;});
          var _t=_live.length?_live[(f/6|0)%_live.length]:null;
          if(_t){ var _hx=subBoss.x+((_t.hb[0]+_t.hb[2]/2)-_SPR/2)*_sc,
                      _hy=subBoss.y+((_t.hb[1]+_t.hb[3]/2)-_SPR/2)*_sc;
                  hitSubBoss(14,_hx,_hy); }
          else hitSubBoss(14, subBoss.x, subBoss.y);
        }
        else hitSubBoss(14, subBoss.x, subBoss.y);
        if(!OUT.sbKilled && subBoss.dead) OUT.sbKilled=+T.toFixed(1);
      }
      /* THE BOSS IS OBSERVED, NOT KILLED. Damaging it at 100dps ended the fight before
         it had fired anything — 0 boss shots recorded. It is left alone so its attack
         cycle can actually be measured, which is the whole point of reaching it. */
      if(typeof boss!=='undefined' && boss && bossActive && !boss.dead){
        if(!OUT.bossSeen) OUT.bossSeen=+T.toFixed(1);
        OUT.bossFrames=(OUT.bossFrames||0)+1;
      }
    }
    snapshotShots();
    for(var i=0;i<enemies.length;i++){
      var en=enemies[i]; if(!en.__probe) continue;
      var p=en.__probe;
      if(f%3===0) p.path.push([Math.round(en.x),Math.round(en.y)]);
      if(p.path.length>2){
        var A=p.path[p.path.length-3],B=p.path[p.path.length-2],C=p.path[p.path.length-1];
        var a1=Math.atan2(B[1]-A[1],B[0]-A[0]), a2=Math.atan2(C[1]-B[1],C[0]-B[0]);
        var dd=a2-a1; while(dd>Math.PI)dd-=2*Math.PI; while(dd<-Math.PI)dd+=2*Math.PI;
        /* 2px GATE, NOT 0.5px. At 0.5 a hovering unit's near-vertical bob flipped its
           heading +/-180deg on sub-pixel noise, and the flips accumulated one way — a
           stationary jet reported 7,830deg of net rotation and looked like a corkscrew
           in the numbers while flying a straight line on screen. Verified by plotting
           the paths. Anything below 2px of travel carries no reliable heading. */
        if(Math.hypot(C[0]-B[0],C[1]-B[1])>2.0){ p.turn+=Math.abs(dd); p.net=(p.net||0)+dd; }
      }
      var ang=Math.atan2(en.vy||0,en.vx||0);
      _CUR=p.type;
      p.lastAng=ang;
      if(f%15===0 && en.rot!=null){
        p.faceSamples.push({rot:+(en.rot||0).toFixed(2),
                            travel:+(Math.atan2(en.vy||0,en.vx||0)).toFixed(2)});
      }
    }
  }
  // collate
  var agg={};
  function collect(arr){ for(var i=0;i<arr.length;i++){ var p=arr[i]; if(!p) continue;
    var k=p.type;
    agg[k]=agg[k]||{n:0,turnDeg:[],netDeg:[],pattern:{},faceErr:[]};
    agg[k].n++;
    agg[k].turnDeg.push(Math.round(p.turn*180/Math.PI));
    agg[k].netDeg.push(Math.round((p.net||0)*180/Math.PI));
    agg[k].pattern[p.pattern]=(agg[k].pattern[p.pattern]||0)+1;
    for(var j=0;j<p.faceSamples.length;j++){
      var fs=p.faceSamples[j];
      var d=fs.rot-fs.travel; while(d>Math.PI)d-=2*Math.PI; while(d<-Math.PI)d+=2*Math.PI;
      agg[k].faceErr.push(Math.round(Math.abs(d)*180/Math.PI));
    }
  } }
  collect(PROBES);
  OUT.enemies=agg;
  OUT.worldWidths=(function(){var o={};for(var st=1;st<=9;st++){run.stage=st;
    try{ _wwCache={}; }catch(e){}
    o[st]=(typeof worldWidth==='function')?worldWidth():null;} run.stage=${STAGE}; return o;})();
  OUT.projUnknown=Object.keys((typeof window!=='undefined'&&window.__projUnknown)||{});
  OUT.sbState={exists:(typeof subBoss!=='undefined'&&!!subBoss),
               active:(typeof subBossActive!=='undefined')?!!subBossActive:null,
               dead:(typeof subBoss!=='undefined'&&subBoss)?!!subBoss.dead:null,
               hp:(typeof subBoss!=='undefined'&&subBoss)?subBoss.hp:null,
               maxhp:(typeof subBoss!=='undefined'&&subBoss)?subBoss.maxhp:null,
               enter:(typeof subBoss!=='undefined'&&subBoss)?subBoss.enter:null,
               code:(typeof subBoss!=='undefined'&&subBoss&&subBoss._sx)?subBoss._sx.code:null};
  OUT.bossState={exists:(typeof boss!=='undefined'&&!!boss),
                 active:(typeof bossActive!=='undefined')?!!bossActive:null};
  OUT.paths=PROBES.filter(function(p){return p.path.length>6;})
                  .map(function(p){return {type:p.type,pat:p.pattern,path:p.path};});
  OUT.scroll={mapScroll:Math.round(typeof mapScroll!=='undefined'?mapScroll:-1),
              onLand:(typeof _s1OnLandProbe==='function')?_s1OnLandProbe():null,
              waveIdx:(typeof waveIdx!=='undefined')?waveIdx:null,
              planLen:(typeof stagePlan!=='undefined'&&stagePlan)?stagePlan.length:null};
  return JSON.stringify(OUT);
})()
`, ctxv);

process.stdout.write(result);
