const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const GAME = path.join(ROOT, 'assets', 'game.js');
const TEST = path.join(ROOT, '_BUILD_SOURCE', 'test_fl.js');
const RECOVERY = path.join(ROOT, '_shots', 'shared_nonlaser_warning_0915', 'recovery');

function count(s, needle) {
  let n = 0, i = 0;
  while ((i = s.indexOf(needle, i)) !== -1) { n++; i += needle.length; }
  return n;
}
function replaceOnce(s, before, after, label) {
  const n = count(s, before);
  if (n !== 1) throw new Error(`${label}: expected exactly one match, found ${n}`);
  return s.replace(before, after);
}

fs.mkdirSync(RECOVERY, {recursive: true});
let game = fs.readFileSync(GAME, 'utf8');
let testRaw = fs.readFileSync(TEST, 'utf8');
let test = testRaw.replace(/\r\n/g, '\n');
if (game.includes('\r\n')) throw new Error('assets/game.js is not LF-only before patch');
if (!testRaw.includes('\r\n') || testRaw.replace(/\r\n/g, '').includes('\n')) {
  throw new Error('_BUILD_SOURCE/test_fl.js is not CRLF-only before patch');
}
fs.writeFileSync(path.join(RECOVERY, 'game_before.js'), game, 'utf8');
fs.writeFileSync(path.join(RECOVERY, 'test_before.js'), testRaw, 'utf8');

game = replaceOnce(game,
`    // Once the charge locks, this fixed lane is the player's guaranteed dodge window.
    if(b._ovState==='chargeTell' && b._chargeTell && b._chargeTell.locked){
      const lane=b._chargeTell.lane, p=clamp(b._ovChargeGlow||0,0,1);
      ctx.save(); ctx.globalCompositeOperation='lighter'; ctx.globalAlpha=0.16+0.30*p;
      ctx.fillStyle='#57ff79';
      for(let ly=0;ly<VH;ly+=24) ctx.fillRect(lane-2,ly,4,12);
      ctx.fillStyle='rgba(225,255,229,0.34)'; ctx.fillRect(lane-11,0,2,VH); ctx.fillRect(lane+9,0,2,VH);
      ctx.restore();
    }
`,
`    // The shared authored FOV owns the whole warning: green tracking, yellow commitment, then
    // flashing red immediately before the ram. Its overhead alert uses the same phase clock.
    if(b._ovState==='chargeTell' && b._chargeTell){
      const T=b._chargeTell, p=clamp(T.t/T.dur,0,1), hub=ovMount(b,0,4);
      combatWarningDraw(b,{x:hub[0],y:hub[1],ex:T.lane,ey:VH,progress:p,width:42});
    }
`, 'Overlord warning renderer');

game = replaceOnce(game,
`function ovStartChargeTell(b){
  b._ovState='chargeTell';
  b._chargeTell={t:0,dur:b._enraged?0.86:1.08,lane:clamp(player.x,72,VW-72),locked:false,pulse:0};
  b._ovChargeGlow=0;
`,
`function ovStartChargeTell(b){
  b._ovState='chargeTell';
  b._chargeTell={t:0,dur:b._enraged?0.86:1.08,lane:clamp(player.x,72,VW-72),locked:false,pulse:0};
  l23FovWarm();
  b._ovChargeGlow=0;
`, 'Overlord warning warmup');

game = replaceOnce(game,
`  if(S==='chargeTell'){
    const T=b._chargeTell; T.t+=dt; T.pulse=(T.pulse||0)-dt;
    const p=clamp(T.t/T.dur,0,1);
`,
`  if(S==='chargeTell'){
    const T=b._chargeTell; T.t+=dt; T.pulse=(T.pulse||0)-dt;
    const p=clamp(T.t/T.dur,0,1);
    combatWarningTick(b,'overlord-charge',T.t,T.dur);
`, 'Overlord warning tick');

game = replaceOnce(game,
`/* TELEGRAPH: hold the pattern for a beat and show where it is coming from. */
function bossTelegraph(b, x, y, dur, col){
  if(!b) return;
  b._tel = {x:x, y:y, t:0, dur:dur||0.45, col:col||'#ff6a4a'};
}
function bossTelegraphDraw(dt){
  const b=(typeof boss!=='undefined')?boss:null;
  if(!b || !b._tel) return;
  const T=b._tel; T.t+=dt;
  if(T.t>=T.dur){ b._tel=null; return; }
  const k=T.t/T.dur, r=10+34*k;
  ctx.save();
  ctx.globalAlpha=0.30+0.45*(1-k);
  ctx.strokeStyle=T.col; ctx.lineWidth=2;
  ctx.beginPath(); ctx.arc(T.x, T.y, r, 0, TAU); ctx.stroke();
  ctx.globalAlpha=0.22+0.30*(1-k);
  ctx.beginPath(); ctx.arc(T.x, T.y, r*0.55, 0, TAU); ctx.stroke();
  ctx.restore();
}
`,
`/* Dangerous attacks use combatWarningTick/combatWarningDraw. The retired generic ring advanced
   simulation from drawBossInner and was shadowed by the mech renderer below, so it never warned. */
`, 'unreachable legacy boss telegraph');

game = replaceOnce(game,
`  /* TELEGRAPH FIRST, under everything else — the wind-up ring has to be visible before the shots
     it warns about. A pattern the player cannot read is not difficulty, it is noise. */
  if(typeof bossTelegraphDraw==='function') bossTelegraphDraw(1/60);
`,
`  /* Attack-owned warning draws happen below the owning hull, using their simulation clocks. */
`, 'render-time legacy warning tick');

game = replaceOnce(game, 'function bossTelegraph(b,K){', 'function mechBossTelegraph(b,K){', 'mech telegraph declaration');
game = replaceOnce(game, "if(K.phase==='fight'){ bossTelegraph(b,K); mechCoreGlow", "if(K.phase==='fight'){ mechBossTelegraph(b,K); mechCoreGlow", 'mech telegraph call');

game = replaceOnce(game,
`function combatWarningTick(owner,id,elapsed,duration){
  if(!owner)return;const warnings=owner._combatWarnings||(owner._combatWarnings={});
  let B=warnings[id];
  if(!B||elapsed<B.t)B=warnings[id]={t:0,warm:duration,released:false};
  B.t=elapsed;B.warm=duration;l23WarnSound(B);
}
`,
`function combatWarningTick(owner,id,elapsed,duration){
  if(!owner)return;const warnings=owner._combatWarnings||(owner._combatWarnings={});
  let B=warnings[id];
  if(!B||elapsed<B.t){B=warnings[id]={t:0,warm:duration,released:false};l23FovWarm();}
  B.t=elapsed;B.warm=duration;B.released=elapsed>=duration;l23WarnSound(B);
}
`, 'shared warning lifecycle');

test = replaceOnce(test,
`  ok(vm.runInContext("typeof bossTelegraph==='function' && typeof bossTelegraphDraw==='function'", ctxv), 'patterns telegraph before they fire');
  var _gP=fs.readFileSync(ROOT+'/assets/game.js','utf8');
  ok(_gP.indexOf('TELEGRAPH FIRST, under everything else')>0, 'and the wind-up draws beneath the boss so it is visible');
`,
`  ok(vm.runInContext("typeof combatWarningTick==='function' && typeof combatWarningDraw==='function' && typeof mechBossTelegraph==='function'", ctxv), 'patterns use the shared authored warning rule before they fire');
  var _gP=fs.readFileSync(ROOT+'/assets/game.js','utf8');
  ok((_gP.match(/function bossTelegraph\\s*\\(/g)||[]).length===0&&_gP.indexOf('function mechBossTelegraph(b,K)')>0,
     'the mech telegraph has a distinct owner and cannot shadow the shared warning rule');
`, 'legacy test assertion');

test = replaceOnce(test,
`    +"for(var i=0;i<35;i++)updateOverlordX(b,1/60);var lane=b._chargeTell.lane,locked=b._chargeTell.locked,glow=b._ovChargeGlow;"
    +"player.x=410;for(var j=0;j<16;j++)updateOverlordX(b,1/60);var held=b._chargeTell.lane;"
`,
`    +"for(var i=0;i<35;i++)updateOverlordX(b,1/60);var lane=b._chargeTell.lane,locked=b._chargeTell.locked,glow=b._ovChargeGlow,warn=b._combatWarnings&&b._combatWarnings['overlord-charge'];"
    +"player.x=410;for(var j=0;j<16;j++)updateOverlordX(b,1/60);var held=b._chargeTell.lane;"
`, 'Overlord test warning capture');

test = replaceOnce(test,
`    +"return JSON.stringify({lane:lane,held:held,locked:locked,glow:glow,state:b._ovState,x:b.x});})()",ctxv));
  ok(_charge265.locked&&_charge265.glow>0.45&&Math.abs(_charge265.held-_charge265.lane)<0.01,
`,
`    +"return JSON.stringify({lane:lane,held:held,locked:locked,glow:glow,warn:warn?{t:warn.t,warm:warn.warm,arrow:warn._arrowN}:null,state:b._ovState,x:b.x});})()",ctxv));
  ok(_charge265.warn&&_charge265.warn.t>0.5&&_charge265.warn.warm===1.08&&_charge265.warn.arrow>=1,
     'the Overlord charge advances the shared green-yellow-red FOV and synchronized alert clock');
  ok(_charge265.locked&&_charge265.glow>0.45&&Math.abs(_charge265.held-_charge265.lane)<0.01,
`, 'Overlord test warning assertion');

if (game.includes('\r\n')) throw new Error('patch introduced CRLF into assets/game.js');
test = test.replace(/\r?\n/g, '\r\n');
fs.writeFileSync(GAME, game, 'utf8');
fs.writeFileSync(TEST, test, 'utf8');
console.log('patched shared non-laser warning foundation');
