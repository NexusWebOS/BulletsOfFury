'use strict';
module.exports=function(vm,ctx,ok){
 console.log('\n=== Shared early difficulty helpers (November14) ===');
 const q=vm.runInContext(`(()=>{const prior=diffKey;try{return ['easy','normal','hard','furious'].map(key=>{diffKey=key;return {key,health:difficultyHealthBaseline15(1050,600),module:difficultyHealthBaseline15(250,140),speed:turretSpeed15(100),interval:turretInterval15(1,.8)}})}finally{diffKey=prior}})()`,ctx);
 for(const [i,hp,part,speed,interval]of [[0,600,140,100,.8],[1,1050,250,100,1],[2,1208,288,115,1/1.15],[3,1389,331,132.25,1/1.3225]]){
  const r=q[i];ok(r.health===hp&&r.module===part,`${r.key}: real core/module health follows the shared compound15% rule or Easy's legacy value`);
  ok(Math.abs(r.speed-speed)<1e-9&&Math.abs(r.interval-interval)<1e-9,`${r.key}: tracking and firing rate share the same difficulty step`);
 }
 ok(vm.runInContext('difficultyHealth15(100,"normal")===100&&difficultyHealth15(100,"hard")===115&&difficultyHealth15(100,"furious")===132&&difficultyHealth15(0,"normal")===1',ctx),'explicit difficulty arguments and minimum health work before live tuning loads');
};
