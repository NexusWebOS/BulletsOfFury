// ===== 303. SHARED LASER WARNING FAMILIES, 0914 =====
console.log('=== 303. shared laser warning families ===');
{
 var laser303=JSON.parse(vm.runInContext(`(function(){
   var out={},oldDead=player.dead;player.dead=true;
   for(var family of ['rime','inferno','legion','future']){
     var b={_ship:'rimewall',x:240,y:140,w:195,h:195,t:0};l23BossBeamStart(b,family,['C'],[Math.PI/2],.2,.5,.2,34);
     l23BossBeamTick(b,2.9);var before=b._l23Beam.released,warm=b._l23Beam.warm;
     l23BossBeamTick(b,.12);out[family]={before,warm,released:b._l23Beam.released,fov:!!L23_FOV[family]};
   }
   player.dead=oldDead;return JSON.stringify(out);
 })()`,ctxv));
 ok(Object.keys(laser303).every(k=>laser303[k].fov),'rime, inferno, legion and future laser families inherit the same color-warning geometry');
 ok(Object.keys(laser303).every(k=>laser303[k].warm>=3&&!laser303[k].before),'every shared laser retains a harmless three-second warning before release');
 ok(Object.keys(laser303).every(k=>laser303[k].released),'shared laser families still release after the full warning completes');
}
