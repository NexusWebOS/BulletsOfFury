module.exports=function(vm,ctxv,ok){
 /* 1021 - Mike: "can you improve and upgrade my boss mode and debug modes please?" The toolkit
    (assets/debug_tools_1021.js): GOD at the playerHit funnel, a speed scale on the fixed 60 Hz
    clock (the old timeScale slider was reset by updatePlay every frame), freeze/step, INSANITY in
    the debug menu. Real-Chromium proof with busted arms: _BUILD_SOURCE/probe_debug_tools_1021.py. */
 console.log('=== 388. Debug toolkit: GOD, a real speed scale, freeze/step, INSANITY in debug ===');
 const fs=require('fs'),path=require('path');
 vm.runInContext(fs.readFileSync(path.join(__dirname,'..','assets','debug_tools_1021.js'),'utf8'),ctxv);
 const r=JSON.parse(vm.runInContext(`JSON.stringify((()=>{
  const o={}, wasU=debugUnlocked; debugUnlocked=true;
  o.loaded=!!(window.DBGT && window.BOSSMODE && BOSSMODE.tools);
  const L0=run.lives, inv0=player.invuln, dead0=player.dead, sh0=run.shield;
  player.dead=false; player.invuln=0; run.shield=0;
  DBGT.god=true; playerHit(); o.godLives=run.lives===L0 && !player.dead; o.godInv=player.invuln;
  DBGT.god=false;
  /* speed: count updatePlay calls the clock makes for 60 frames of 1/60 */
  const up=updatePlay, st=state; let n=0; updatePlay=function(){ n++; }; state=GS.PLAY;
  const run60=()=>{ n=0; combatClockReset(); for(let i=0;i<60;i++) combatFrame(1/60); return n; };
  DBGT.speed=1; o.t1=run60(); DBGT.speed=0.5; o.t05=run60(); DBGT.speed=2; o.t2=run60();
  DBGT.speed=1; DBGT.frozen=true; o.tf=run60(); DBGT.step=1; o.tstep=run60(); DBGT.frozen=false;
  debugUnlocked=false; DBGT.speed=0.5; o.unarmed=run60(); DBGT.speed=1;
  updatePlay=up; state=st;
  BOSSMODE.setTimeScale(0.4); o.slider=DBGT.speed; o.ts=timeScale; BOSSMODE.setTimeScale(1);
  o.diffs=DIFF_KEYS.slice();
  o.menuSrc=/const ds=DIFF_KEYS/.test(drawDebugMenu.toString().replace(/\\/\\*[\\s\\S]*?\\*\\//g,''));
  run.lives=L0; player.invuln=inv0; player.dead=dead0; run.shield=sh0; debugUnlocked=wasU;
  return o;})())`,ctxv));
 ok(r.loaded,'the toolkit loads and hangs its surface on BOSSMODE.tools');
 ok(r.godLives,'GOD refuses a real playerHit');
 ok(r.godInv===0,'GOD leaves the invuln timer alone, so the ship never blinks ('+r.godInv+')');
 ok(r.t1===60&&r.t05===30&&r.t2===120,'the fixed clock runs speed x 60 ticks a second (1x '+r.t1+', 0.5x '+r.t05+', 2x '+r.t2+')');
 ok(r.tf===0&&r.tstep===1,'frozen runs 0 ticks, and a step runs exactly one ('+r.tf+', '+r.tstep+')');
 ok(r.unarmed===60,'outside debug the speed scale does nothing - a normal game is untouched ('+r.unarmed+')');
 ok(Math.abs(r.slider-0.4)<1e-9&&r.ts===1,'the editor SPEED slider sets the scale and no longer fights updatePlay for timeScale');
 ok(r.diffs.includes('insanity')&&r.menuSrc,'the debug menu cycles every difficulty in DIFF_KEYS, INSANITY included');
};
