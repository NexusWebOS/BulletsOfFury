module.exports=function(vm,ctxv,ok){
 const fs=require('fs'),path=require('path');
 for(const file of ['s4_core_revival_art_1006.js','s4_core_revival_1006.js'])vm.runInContext(fs.readFileSync(path.join(__dirname,'../assets',file),'utf8'),ctxv,{filename:file});
 console.log('=== October 6 Stage 4 authored core revival ===');
 const rows=JSON.parse(vm.runInContext(`JSON.stringify((()=>{
 const o={};ht27Stop();debugFight=null;coopOn=false;run.mode='campaign';run.pilot='yuri';
 for(const diff of ['easy','normal','hard','furious']){
  diffKey=diff;DIFF=DIFFS[diff];beginStage(4);setState(GS.PLAY);player.reset();BOFCinematicDirector.cancel();story=null;spawnBoss('stormsovereign');
  const b=boss;b.enter=false;b._noHit=false;b.y=b._drawY=b._er26.home;const H=b._s4war.shield;
  o[diff+' active shield has no revival overlay']=!H.revival1006;
  H.nodes.forEach(n=>stage4ShieldDestroyNode(b,n));const hp=b.hp,shotCount=eBullets.length;
  const started=stage4ShieldBeginRearm(b,.75);o[diff+' successful threshold starts one owned revival']=started&&H.revival1006.t===0&&H.revival1006.cycle===H.cycle;
  const ref=H.revival1006;stage4ShieldBeginRearm(b,.75);o[diff+' failed duplicate rearm cannot restart the clip']=H.revival1006===ref;
  stage4ShieldTick(b,.30);o[diff+' effects share the existing rearm clock']=Math.abs(H.revival1006.t-H.rearmT)<1e-8&&H.rearming;
  stage4ShieldTick(b,.80);o[diff+' overlay does not delay four restored cores']=H.active&&!H.rearming&&H.nodes.every(n=>!n.dead&&n.materialize===1)&&b.hp===hp&&eBullets.length===shotCount;
  stage4ShieldTick(b,.40);o[diff+' revival expires without a loop']=H.revival1006===null;
  H.nodes.forEach(n=>stage4ShieldDestroyNode(b,n));stage4ShieldBeginRearm(b,.5);b.dead=true;stage4ShieldTick(b,.01);o[diff+' death cancels owned revival']=H.revival1006===null;
 }
 const b=boss;b.dead=false;const H=b._s4war.shield;H.rearming=false;H.active=false;stage4ShieldBeginRearm(b,.25);H.rearming=false;H.active=false;stage4ShieldTick(b,.01);
 o['inactive field cancels revive state']=H.revival1006===null;
 o['three clips each have four registered exact cells']=Object.values(S4REV1006_ART.clips).every(c=>c.frames.length===4&&c.frames.every(f=>f.rect.length===4&&f.offset.length===2));
 return o;
})())`,ctxv));for(const [name,value]of Object.entries(rows))ok(value,name);
 ok(fs.existsSync(path.join(__dirname,'../assets/game/s4_core_revival_1006/core_revival.png')),'generated revival PNG is deployed');
 ok(fs.existsSync(path.join(__dirname,'../_ART_SOURCES/s4_core_revival_1006/repair-prompt.txt')),'generated revival repair prompt is archived');
};
