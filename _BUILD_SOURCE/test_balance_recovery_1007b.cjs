module.exports=function(vm,c,ok,source='../assets/balance_recovery_1007b.js'){
 const fs=require('fs'),path=require('path');
 vm.runInContext(fs.readFileSync(path.resolve(__dirname,source),'utf8'),c,{filename:'balance_recovery_1007b.js'});
 const checks=JSON.parse(vm.runInContext(`JSON.stringify((()=>{
  const out={},save={diffKey,stage:run.stage,dropPowerup,playerDead:player.dead,er26Station,stage4ShieldTick,er26CoreTick,hc1007Cancel};
  const drops=[];
  try{
   for(const difficulty of ['easy','normal','hard','furious']){
    diffKey=difficulty;run.stage=2;
    for(const attack of ['spin900','sweep','rotor']){
     const start=attack==='sweep'?1.05:1,F={attack,at:start,beams:[],tells:[]},C=balanceFlameCycle(F);
     const sample=t=>{F.at=start+t;F.beams=[];F.tells=[];fztBeam(F,120,100,0,430,25,'flame');return{beams:F.beams.slice(),tells:F.tells.slice()};};
     let q=sample(C.on/2);out[difficulty+' '+attack+' active flame keeps authored width']=q.beams.length===1&&Math.abs(q.beams[0].width-25*FZT_S)<1e-8;
     q=sample(C.on+C.fade/2);out[difficulty+' '+attack+' fading hitbox matches the shrinking drawing']=q.beams.length===1&&Math.abs(q.beams[0].width-12.5*FZT_S)<1e-7;
     q=sample(C.on+C.fade+C.gap/2);out[difficulty+' '+attack+' crossing interval has no beam or stale warning']=q.beams.length===0&&q.tells.length===0;
     q=sample(C.on+C.fade+C.gap+C.warn/2);out[difficulty+' '+attack+' next burst is visibly warned before damage']=q.beams.length===0&&q.tells.length===1&&Math.abs(q.tells[0].progress-.5)<1e-7;
     q=sample(C.cycle+.05);out[difficulty+' '+attack+' next burst is still dangerous']=q.beams.length===1;
     run.stage=8;q=sample(C.on+C.fade+C.gap/2);out[difficulty+' '+attack+' finale donor keeps its late-game flame']=q.beams.length===1;run.stage=2;
    }
    const P=MANEUVER_SAFETY_1007.profiles[difficulty],b={_hammer:{whirl:{l:24,r:worldWidth()-24,dir:1,pass:1,passes:2}}};
    hammerWhirlLane(b,false);
    out[difficulty+' follow-up whirlwind allows reaction and ordinary escape']=b._hammer.whirl.warm>=P.reaction+(102+10+P.pad)/(MANEUVER_SAFETY_1007.slowSpeed*1.35)+.099;
   }
   dropPowerup=(x,y,kind)=>drops.push({x,y,kind});
   const b={x:worldWidth()/2,y:180};
   out['earned break produces ordinary weapon and shield pickups']=balanceMilestone(b,'arm',true)&&drops.length===2&&drops[0].kind==='weapon'&&drops[1].kind==='shield';
   out['regeneration cannot farm the same reward']=!balanceMilestone(b,'arm',true)&&drops.length===2;
   out['different earned milestones remain independent']=balanceMilestone(b,'core',false)&&drops.length===3;
   out['donor proxy cannot mint campaign rewards']=!balanceMilestone({_gp4Host:b},'arm',true)&&drops.length===3;
   out['deferred finale reward does not drop during transformation']=balanceMilestone(b,'form-0',true,true)&&drops.length===3&&b._balancePending1007.length===1;
   const oldTick=BALANCE_MILESTONE_BASE.tick;
   try{
    BALANCE_MILESTONE_BASE.tick=()=>{};b._r30={mode:'transform1003j'};r30Tick(b,1/60);
    out['cinematic holds earned supplies']=b._balancePending1007.length===1&&drops.length===3;
    b._r30.mode='fight';player.dead=true;r30Tick(b,1/60);
    out['dead pilot does not lose the queued recovery reward']=b._balancePending1007.length===1&&drops.length===3;
    player.dead=false;r30Tick(b,1/60);r30Tick(b,1/60);
    out['return to fight releases deferred supplies once']=drops.length===5&&b._balancePending1007.length===0;
   }finally{BALANCE_MILESTONE_BASE.tick=oldTick;}

   for(const difficulty of ['easy','normal','hard','furious'])for(const stage of [2,4,5]){
    diffKey=difficulty;run.stage=stage;const f=BALANCE_HP_1007[stage][difficulty];
    const target={hp:1000,maxhp:1000,...(stage===2?{_furnace:true,_fz:{hpSync:true,pools:{left:200,right:200,body:400,head:200},max:{left:200,right:200,body:400,head:200}},_mwBarrier:{hp:250,maxhp:250}}:stage===4?{_ship:'stormsovereign',_mr27:{parts:[{hp:100,max:100},{hp:200,maxhp:200}]}}:{_hammer:{frArmor:{hp:600,max:600}}})};
    balanceEncounterBudget(target);balanceEncounterBudget(target);
    out[difficulty+' stage '+stage+' encounter budget applies only once']=target.hp===Math.round(1000*f)&&target.maxhp===Math.round(1000*f);
    if(stage===2)out[difficulty+' furnace pools and barrier agree with the hull budget']=target._fz.pools.body===Math.round(400*f)&&target._fz.max.body===Math.round(400*f)&&target._mwBarrier.maxhp===Math.round(250*f);
    if(stage===4)out[difficulty+' Sovereign weapon pools share its hull budget']=target._mr27.parts[0].max===Math.round(100*f)&&target._mr27.parts[1].maxhp===Math.round(200*f);
    if(stage===5)out[difficulty+' existing Chromium armor keeps the matching budget']=target._hammer.frArmor.max===Math.round(600*f);
   }
   run.stage=8;diffKey='furious';const donor={_furnace:true,hp:1000,maxhp:1000};balanceEncounterBudget(donor);
   out['finale copies do not inherit mid-campaign health reductions']=donor.hp===1000&&donor._balanceHealth1007==null;
   const oldWar=BALANCE_RECOVERY_1007B.base.war;
   try{
    let calls=0,attachments=0;BALANCE_RECOVERY_1007B.base.war=()=>{calls++;return 'normal';};
    er26Station=()=>340;stage4ShieldTick=()=>{attachments++;};er26CoreTick=()=>{attachments++;};hc1007Cancel=()=>{};
    const ship={x:500,y:365,dead:false,_ship:'stormsovereign',_mr27:{stun:1,ram1002:{}},_er26:{home:160,t:0,dur:0,warnings:[{}]}};
    er26WarTick(ship,.1);
    out['Sovereign retreats during an earned punish window']=ship.y===343&&ship.x===489;
    out['Sovereign recovery cancels offense and maintains attachments']=calls===0&&attachments===2&&!ship._mr27.ram1002&&ship._er26.warnings.length===0;
    ship._mr27.stun=0;out['Sovereign resumes its normal attack director']=er26WarTick(ship,.1)==='normal'&&calls===1;
   }finally{BALANCE_RECOVERY_1007B.base.war=oldWar;}
  }finally{diffKey=save.diffKey;run.stage=save.stage;dropPowerup=save.dropPowerup;player.dead=save.playerDead;er26Station=save.er26Station;stage4ShieldTick=save.stage4ShieldTick;er26CoreTick=save.er26CoreTick;hc1007Cancel=save.hc1007Cancel;}
  return out;
 })())`,c));
 for(const [name,value] of Object.entries(checks))ok(value,name);
};
