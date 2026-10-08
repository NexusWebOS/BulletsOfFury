module.exports=function(vm,c,ok){
 const fs=require('fs'),path=require('path');
 vm.runInContext(fs.readFileSync(path.join(__dirname,'../assets/maneuver_safety_1007.js'),'utf8'),c,{filename:'maneuver_safety_1007.js'});
 const tests=JSON.parse(vm.runInContext(`JSON.stringify((()=>{
 const out={},saved={diffKey,stage:run.stage,state,updatePlay,clear:Input.clearTaps};
 try{
  for(const diff of ['easy','normal','hard','furious'])for(const stage of [1,4,8])for(const kind of Object.keys(GROUND_TARGETING_PRESETS)){
   diffKey=diff;run.stage=stage;const q=groundTargetingSpawn({kind});const p=MANEUVER_SAFETY_1007.profiles[diff];
   const remaining=q.warn+.08-q.warn*q.trackFor;
   out[diff+' stage '+stage+' '+kind+' has reaction and travel room']=remaining+1e-9>=p.reaction+(q.radius+p.pad)/MANEUVER_SAFETY_1007.slowSpeed+2/30;
   q.t=q.warn*q.trackFor;out[diff+' stage '+stage+' '+kind+' yellow agrees with aim lock']=Math.abs(groundTargetingPhase(q)-.5)<1e-9;
  }
  const fixed=groundTargetingSpawn({kind:'lava',track:false,warn:.35});fixed._fztEye=true;fixed.t=.175;
  out['linked fixed-position eye beam keeps authored timing']=fixed.warn===.35&&groundTargetingPhase(fixed)===.5;
  const rig={x:340,w:264,_s4war:{shield:{active:true,nodes:[{x:136,dead:false},{x:544,dead:false}]},coreTurrets:[]}};
  out['ram warning includes the live generators beyond its shield']=maneuverRamWidth(rig)===486;
  rig._s4war.shield.nodes.forEach(n=>n.dead=true);
  out['broken generators no longer enlarge the ram warning']=Math.abs(maneuverRamWidth(rig)-359.76)<1e-7;
  rig._s4war.shield.active=false;
  out['unshielded ram warning covers the complete hull']=maneuverRamWidth(rig)===270;
  for(const diff of ['easy','normal','hard','furious']){diffKey=diff;out[diff+' edge ram gets extra time to clear its swept path']=maneuverRamWarm(rig,.78,{tx:100,ox:340})>maneuverRamWarm(rig,.78,{tx:340,ox:340})+1;}
  const rawWarn=combatWarningDraw,rawFx=er28Draw,seen=[];
  combatWarningDraw=(b,q)=>seen.push(q);er28Draw=()=>{};
  try{const b={_er26:{mode:'recover',t:.5,warm:1,warnings:[{x:340,y:100,angle:Math.PI/2,width:486,progress:.4,laneShape:'line'}]},_mr27:{ram1002:{state:'tell'}}};
   er26Draw(b);out['damaged-weapon ram is visibly warned even in the outer recover state']=seen.some(q=>q.fieldOnly&&q.width===486&&q.laneShape==='line');
   seen.length=0;b._mr27.ram1002.state='return';er26Draw(b);out['ordinary recovery does not retain a stale ram corridor']=seen.length===0;
  }finally{combatWarningDraw=rawWarn;er28Draw=rawFx;}
  let calls=0,elapsed=0,clears=0;updatePlay=dt=>{calls++;elapsed+=dt;};Input.clearTaps=()=>{clears++;};state=GS.PLAY;
  for(const fps of [30,60,120,144]){combatClockReset();calls=0;elapsed=0;for(let i=0;i<fps*3;i++)combatFrame(1/fps);
   out[fps+' Hz executes exactly 180 combat ticks in three seconds']=calls===180&&Math.abs(elapsed-3)<1e-8;
  }
  combatClockReset();calls=0;combatFrame(1/120);out['half-frame preserves pending input until a combat tick']=calls===0&&BOF_COMBAT_CLOCK.steps===0;combatFrame(1/120);out['next half-frame runs one tick']=calls===1;
  for(const dt of [NaN,-1,Infinity,5]){calls=0;combatFrame(dt);out['invalid/background interval '+String(dt)+' discards debt']=calls===0&&BOF_COMBAT_CLOCK.debt===0;}
  combatClockReset();calls=0;combatFrame(.20);out['catch-up is bounded to three simulation ticks']=calls===3;
  state=GS.TITLE;combatFrame(.02);out['menus discard combat debt']=BOF_COMBAT_CLOCK.debt===0;
  state=GS.PLAY;calls=0;updatePlay=()=>{calls++;state=GS.TITLE;};combatFrame(.05);out['transition stops catch-up immediately']=calls===1&&BOF_COMBAT_CLOCK.debt===0;
 }finally{diffKey=saved.diffKey;run.stage=saved.stage;state=saved.state;updatePlay=saved.updatePlay;Input.clearTaps=saved.clear;groundTargetingReset();combatClockReset();}
 return out;
})())`,c));
 for(const [name,value]of Object.entries(tests))ok(value,name);
};
