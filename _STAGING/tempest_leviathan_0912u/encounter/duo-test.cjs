/* duo-test.cjs - the two Tempest Leviathan brothers fighting together (Stage 6), driven through full
   seeded showcase runs.  Run: node duo-test.cjs
   The single-ship tests still stand: node interceptor-test.cjs (black) and node brother-test.cjs (gray). */
const {Duo}=require('./engine-duo.js');
const fails=[];
const ok=(c,m)=>{ if(c) console.log('  ok  '+m); else { fails.push(m); console.log('  FAIL '+m); } };
const COMBAT=['chase','hell','pursuit','frenzy'];
function lcg(seed){ let s=seed>>>0; return ()=>{ s=(Math.imul(s,1664525)+1013904223)>>>0; return s/4294967296; }; }
const onScreen=(s)=>!(s.boss.x<-70||s.boss.x>970||s.boss.y<-80||s.boss.y>1080);

function run(seed){
  const d=new Duo(lcg(seed)), input={demo:true};
  let together=0, conflict=0, blackDiag=0, grayDiag=0, grayX=0, grayY=0, grayExits=0, wasOff=true, playerJump=0, rot=0, nan=0;
  let aloneFrames=0, steps=0, firstDownAt=null, bothDownAt=null;
  let prev={x:d.player.x,y:d.player.y};
  const maxStep=540/120*Math.SQRT2+1e-6;
  for(steps=0; steps<120*1500 && d.phase!=='victory' && d.phase!=='defeat'; steps++){
    d.step(1/120,input);
    const B=d.black, G=d.gray;
    if(!B.gone&&!G.gone&&COMBAT.includes(B.phase)&&COMBAT.includes(G.phase)&&onScreen(G)&&onScreen(B)) together++;
    if(!B.gone&&!G.gone&&B.state==='ram'&&G.state==='run'&&onScreen(G)) conflict++;
    if(!B.gone&&COMBAT.includes(B.phase)&&Math.abs(B.stepDX)>1e-6&&Math.abs(B.stepDY)>1e-6) blackDiag++;
    if(!G.gone&&COMBAT.includes(G.phase)){
      if(Math.abs(G.stepDX)>1e-6&&Math.abs(G.stepDY)>1e-6) grayDiag++; else if(Math.abs(G.stepDX)>1e-6) grayX++; else if(Math.abs(G.stepDY)>1e-6) grayY++;
      const off=!onScreen(G); if(off&&!wasOff) grayExits++; wasOff=off;
    }
    if(d.phase!=='escape'){ const mv=Math.hypot(d.player.x-prev.x,d.player.y-prev.y); if(mv>maxStep) playerJump++; }
    prev={x:d.player.x,y:d.player.y};
    if(d.alone) aloneFrames++;
    if(d.firstDown&&firstDownAt===null) firstDownAt=d.time;
    if(d.phase==='escape'&&bothDownAt===null) bothDownAt=d.time;
    for(const s of d.ships){ if(s.boss.a!==0) rot++; if(!Number.isFinite(s.boss.x)||!Number.isFinite(s.boss.y)) nan++; }
  }
  return {d,together,conflict,blackDiag,grayDiag,grayX,grayY,grayExits,playerJump,rot,nan,aloneFrames,steps,firstDownAt,bothDownAt};
}

console.log('=== the Tempest Leviathan brothers, together ===');
for(const seed of [9271,1337,42]){
  const r=run(seed), d=r.d;
  console.log('seed '+seed+': '+d.phase+' after '+(r.steps/120).toFixed(1)+'s  together '+r.together+'  first down '+d.firstDown+' @'+(r.firstDownAt||0).toFixed(1)+
              's  both down @'+(r.bothDownAt||0).toFixed(1)+'s  pincers '+d.pincers+'  holds '+d.holds+'  black deferrals '+(d.black.deferred||0)+
              '  gray moves diag/x/y '+r.grayDiag+'/'+r.grayX+'/'+r.grayY+'  gray exits '+r.grayExits);
  ok(r.together>1200, 'seed '+seed+': both brothers are in the fight and on screen together ('+r.together+' frames)');
  ok(r.conflict===0, 'seed '+seed+': the black ship never rams while its brother is crossing ('+r.conflict+' frames)');
  ok(d.holds>0, 'seed '+seed+': the brother waits off-screen while the black ship rams ('+d.holds+' held frames)');
  ok(d.pincers>0, 'seed '+seed+': the brother comes through underneath the black ship\'s laser lanes (PINCER x'+d.pincers+')');
  ok(r.blackDiag===0, 'seed '+seed+': the black ship keeps its one-axis flight inside the duo ('+r.blackDiag+' diagonal steps)');
  ok(r.grayDiag>400&&r.grayX>60&&r.grayY>60, 'seed '+seed+': the gray brother keeps its diagonal, horizontal and vertical runs');
  ok(r.grayExits>=6, 'seed '+seed+': and still leaves the screen and returns ('+r.grayExits+' exits)');
  ok(r.playerJump===0, 'seed '+seed+': nothing but the player\'s own input moves the player ('+r.playerJump+' jumps) - no overtake yank');
  ok(d.firstDown&&r.aloneFrames>120, 'seed '+seed+': when one brother falls the survivor fights on alone ('+d.firstDown+' first, '+(r.aloneFrames/120).toFixed(1)+'s alone)');
  ok(r.bothDownAt!==null&&r.bothDownAt>=r.firstDownAt, 'seed '+seed+': the escape plays once, after BOTH are down');
  ok(d.phase==='victory', 'seed '+seed+': the showcase reaches victory');
  ok(r.rot===0&&r.nan===0, 'seed '+seed+': neither ship rotates, and every position stays finite');
}
console.log('\n'+(fails.length?'FAIL: '+fails.length+' failed':'PASS: the brothers fight together - tag-team rams and crossings, pincers, vengeance, one escape.'));
process.exit(fails.length?1:0);
