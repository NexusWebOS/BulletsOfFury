module.exports=function(vm,c,ok){
 const fs=require('fs'),path=require('path');
 if(vm.runInContext('typeof FT7',c)==='undefined')vm.runInContext(fs.readFileSync(path.join(__dirname,'../assets/finale_transform_1007.js'),'utf8'),c,{filename:'finale_transform_1007.js'});
 console.log('=== Opaque physical final-boss transformations and actual combat monologue ===');
 const out=JSON.parse(vm.runInContext(`JSON.stringify((()=>{
 const out={};ht27Stop();coopOn=false;run.pilot='cole';run.mode='campaign';diffKey='normal';DIFF=DIFFS.normal;beginStage(8);setState(GS.PLAY);player.reset();spawnBoss('vileexistence');BOFCinematicDirector.cancel();story=null;fb2Talk=null;
 const b=boss,S=b._r30,J=j3State(b);j3Encounter(b,2);dr5State(b).introSeen=true;dr5State(b).introWanted=false;
 const finish=()=>{for(let n=0;n<170&&S.mode!=='fight';n++)r30Tick(b,1/60);};
 out['all nine persistent form budgets remain present']=J.hp.length===9&&J.max.length===9;
 for(let i=0;i<9;i++){
  j3Mimic(b,i);on5FightStart(b);S.attack=null;S.shield=0;S.on5Shield=null;b._lastPart=b.parts[0];modularHit(37+i);
  const part=b.parts.find(p=>p.id!=='core'&&!p.destroyed);if(part){b._lastPart=part;modularHit(part.hp+1);}j3Save(b);
  const hp=J.hp.slice(),pieces=b.parts.slice(),health=b.hp;j3Morph(b,'home');const clock=S.clock,aa=J.aa5Clock;r30Tick(b,1/60);
  out['copy '+i+' retains one protected transition clock']=b.enter&&!r30Live(b)&&Math.abs(S.clock-clock-1/60)<1e-8&&Math.abs(J.aa5Clock-aa-1/60)<1e-8;
  const mark=S.clock,pools=JSON.stringify(J.hp);r30DrawBoss(b);r30DrawBoss(b);
  out['copy '+i+' render is opaque and cannot change health/time']=FT7.last.pieces.length>0&&FT7.last.pieces.every(v=>v.alpha===1&&v.id!==part?.id)&&S.clock===mark&&JSON.stringify(J.hp)===pools;
  finish();J.cursor=(i+8)%9;j3Morph(b,i);finish();
  out['copy '+i+' re-enters with the exact damaged modules and nine budgets']=J.mimic===i&&b.hp===health&&J.hp.every((v,k)=>v===hp[k])&&b.parts.every(p=>pieces.includes(p))&&!S.rewarded;
 }
 j3Home(b);S.mode='dr5Monologue';S.t=0;S.attack=null;dr5State(b).radio=null;const clock=S.clock,hp=JSON.stringify(J.hp),old=DR5.draws.parts||0;r30DrawBoss(b);
 out['monologue delegates its body to the live combat rig only']=FT7.last.combatBody&&(DR5.draws.parts||0)===old&&S.mode==='dr5Monologue'&&S.clock===clock&&hp===JSON.stringify(J.hp);
 const wanted=ft7Nodes(b).map(v=>v.key);out['talking body uses existing combat torso and articulated arms']=wanted.includes('colossus_body')&&wanted.includes('colossus_armL')&&wanted.includes('colossus_armR');
 const prior=FT7_BASE.draw;let delegated=0;FT7_BASE.draw=()=>delegated++;try{S.mode='dr5Death';r30DrawBoss(b);S.mode='fight';r30DrawBoss(b);S.mode='reunion';r30DrawBoss(b);}finally{FT7_BASE.draw=prior;}
 out['fight, final destruction and reward reunion keep their existing render owners']=delegated===3;
 beginStage(1);return out;
 })())`,c));for(const [name,value]of Object.entries(out))ok(value,name);
};
