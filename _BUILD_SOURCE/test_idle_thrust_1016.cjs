module.exports=function(vm,ctxv,ok){
 /* 1016 - Mike: "can you make our thrusters animate when were idle on all pilots?" The plume (pilot_feedback_0927.js)
    drew only above 2.5% throttle; idle now holds a breathing burn floor. Behaviour only. Real-Chromium proof with a
    busted arm: _BUILD_SOURCE/probe_idle_thrust_1016.py (pilot_feedback_0927.js is already loaded by section 0927). */
 console.log('=== 381. Idle thrusters: every pilot keeps a breathing burn at rest ===');
 const r=JSON.parse(vm.runInContext(`JSON.stringify((()=>{
  const o={},save=efxClock;player.dead=player.out=false;player._thrustPower=0;window.PF16_IDLE=undefined;
  const vals=[];for(let i=0;i<120;i++){efxClock=i/60;vals.push(pf27ThrustPower());}
  o.min=Math.min(...vals);o.max=Math.max(...vals);
  player._thrustPower=.9;efxClock=.3;o.moving=pf27ThrustPower();player._thrustPower=0;
  player.dead=true;o.dead=pf27ThrustPower();player.dead=false;
  player.out=true;o.out=pf27ThrustPower();player.out=false;
  window.PF16_IDLE=0;o.busted=pf27ThrustPower();window.PF16_IDLE=undefined;
  efxClock=save;return o;})())`,ctxv));
 ok(r.min>=.025,'an idle ship always clears the plume draw threshold (min '+r.min.toFixed(3)+')');
 ok(r.max-r.min>=.05,'the idle burn breathes over two seconds ('+r.min.toFixed(3)+'..'+r.max.toFixed(3)+')');
 ok(r.max<.3,'idle stays well under a real burn (max '+r.max.toFixed(3)+')');
 ok(r.moving>.85,'real throttle still rises above the idle floor ('+r.moving.toFixed(3)+')');
 ok(r.dead===0&&r.out===0,'a dead or out ship carries no idle burn');
 ok(r.busted===0,'the idle burn can be switched off (PF16_IDLE=0), so the probe busted arm is real');
};
