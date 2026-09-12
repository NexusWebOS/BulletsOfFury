/* brother-test.cjs - the light-gray brother's flight rules, driven through full showcase runs.
   Run: node brother-test.cjs   (the black ship keeps its own test: node interceptor-test.cjs)

   Mike: "diagonal motions and vertical motions and horizontal motions, but overall flys across the screen up
   and down, side to side off screen and returning to flake you out."
   Every claim is measured on the simulation, frame by frame. */
const {Brother}=require('./engine-brother.js');
const {Jet}=require('./engine.js');
const fails=[];
const ok=(c,m)=>{ if(c) console.log('  ok  '+m); else { fails.push(m); console.log('  FAIL '+m); } };
const COMBAT=['chase','hell','pursuit','frenzy'];

function lcg(seed){ let s=seed>>>0; return ()=>{ s=(Math.imul(s,1664525)+1013904223)>>>0; return s/4294967296; }; }

function run(seed){
  const g=new Brother(lcg(seed));
  const input={demo:true};
  const tally={diagonal:0,x:0,y:0}, runs={}, phases=new Set();
  let prev={x:g.boss.x,y:g.boss.y}, rot=0, nan=0, hitOffscreen=0, offFrames=0, warnedReturns=0, unwarnedReturns=0;
  let wasOff=true, lastWarnT=-9, steps=0, maxX=-1e9, minX=1e9, maxY=-1e9, minY=1e9;
  for(steps=0; steps<120*900 && !['victory','defeat'].includes(g.phase); steps++){
    const warnBefore=!!g.entryWarn;
    g.step(1/120,input);
    phases.add(g.phase);
    if(g.run) runs[g.run]=(runs[g.run]||0)+1;
    if(g.entryWarn||warnBefore) lastWarnT=g.time;
    const inCombat=COMBAT.includes(g.phase);
    if(inCombat){
      const dx=Math.abs(g.boss.x-prev.x)>1e-6, dy=Math.abs(g.boss.y-prev.y)>1e-6;
      if(dx&&dy) tally.diagonal++; else if(dx) tally.x++; else if(dy) tally.y++;
      const off=g.offscreen();
      if(off){ offFrames++; if(g.vulnerable) hitOffscreen++; }
      if(!off&&wasOff&&steps>240){ if(g.time-lastWarnT<2.2) warnedReturns++; else unwarnedReturns++; }
      wasOff=off;
      maxX=Math.max(maxX,g.boss.x); minX=Math.min(minX,g.boss.x); maxY=Math.max(maxY,g.boss.y); minY=Math.min(minY,g.boss.y);
    }
    if(g.boss.a!==0) rot++;
    if(!Number.isFinite(g.boss.x)||!Number.isFinite(g.boss.y)) nan++;
    prev={x:g.boss.x,y:g.boss.y};
  }
  return {g,tally,runs,phases,rot,nan,hitOffscreen,offFrames,warnedReturns,unwarnedReturns,steps,minX,maxX,minY,maxY};
}

console.log('=== the light-gray brother ===');
for(const seed of [9271, 1337, 42]){
  const r=run(seed), g=r.g;
  console.log('seed '+seed+': phase '+g.phase+' after '+(r.steps/120).toFixed(1)+'s  moves '+JSON.stringify(r.tally)+
              '  exits '+(g.exits||0)+'  feints '+g.feints+'  bounces '+g.bounces+'  runs '+JSON.stringify(r.runs));
  ok(r.tally.diagonal>600, 'seed '+seed+': it flies DIAGONALLY ('+r.tally.diagonal+' frames)');
  ok(r.tally.x>120, 'seed '+seed+': and purely HORIZONTALLY ('+r.tally.x+' frames)');
  ok(r.tally.y>120, 'seed '+seed+': and purely VERTICALLY ('+r.tally.y+' frames)');
  ok((g.exits||0)>=8, 'seed '+seed+': it leaves the screen again and again ('+(g.exits||0)+' exits)');
  ok(r.minX<-60&&r.maxX>960&&r.minY<-60&&r.maxY>1060, 'seed '+seed+': off every edge - left, right, top and bottom (x '+r.minX.toFixed(0)+'..'+r.maxX.toFixed(0)+', y '+r.minY.toFixed(0)+'..'+r.maxY.toFixed(0)+')');
  ok(r.warnedReturns>=6&&r.unwarnedReturns===0, 'seed '+seed+': every return is announced by an entry warning first ('+r.warnedReturns+' warned, '+r.unwarnedReturns+' unwarned)');
  ok(g.feints>=1, 'seed '+seed+': it flakes you out with mid-run V-turns ('+g.feints+')');
  ok(r.hitOffscreen===0, 'seed '+seed+': it cannot be damaged while off-screen ('+r.hitOffscreen+' vulnerable frames off-screen)');
  ok(r.rot===0, 'seed '+seed+': it never yaws, rotates or flips');
  ok(r.nan===0, 'seed '+seed+': every position stays finite');
  ok(['chase','pursuit','hell','frenzy','death','escape'].every(p=>r.phases.has(p)), 'seed '+seed+': all four combat phases, the death and the escape play');
  ok(!r.phases.has('overtake')&&!r.phases.has('return'), 'seed '+seed+': the player-moving overtake/return beats never run');
  ok(g.phase==='victory', 'seed '+seed+': the showcase reaches victory');
}

/* the four apertures still work on the brother */
{
  const g=new Brother(lcg(7)); g.enter('chase'); g.boss.x=450; g.boss.y=300; g.vulnerable=true;
  for(let i=0;i<30;i++) g.damageTurret(0,13);
  ok(g.rig[0].hp===0 && g.ports(-1).every(q=>q.id!==0), 'a destroyed aperture stops firing on the brother too');
}
/* and the black ship is untouched - still one axis per step */
{
  const g=new Jet(lcg(5)); let diag=0, p={x:g.boss.x,y:g.boss.y};
  for(let i=0;i<120*60&&g.phase!=='victory';i++){ g.step(1/120,{demo:true}); if(Math.abs(g.boss.x-p.x)>1e-6&&Math.abs(g.boss.y-p.y)>1e-6&&COMBAT.includes(g.phase)) diag++; p={x:g.boss.x,y:g.boss.y}; }
  ok(diag===0, 'the BLACK ship still moves on exactly one axis per step ('+diag+' diagonal frames)');
}

console.log('\n'+(fails.length?'FAIL: '+fails.length+' failed':'PASS: the light-gray brother flies diagonal, vertical and horizontal runs across and off every edge, returns after honest warnings, feints, and is killable.'));
process.exit(fails.length?1:0);
