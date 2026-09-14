// ===== 307. HARD/FURIOUS LIFE UP PROBABILITIES, 0914 =====
console.log('=== 307. Life Up difficulty bonus ===');
{
 const result=JSON.parse(vm.runInContext(`(function(){
  const save={diffKey,mode:run.mode,powerups,random:Math.random,seen:stageStats.pickupsSeen};const o={};
  try{
   function roll(key,a,b,force){diffKey=key;powerups=[];let n=0;Math.random=()=>n++===0?a:b;dropPowerup(240,100,force);return powerups.map(p=>p.kind).join(',');}
   for(const mode of ['campaign','arcade']){
    run.mode=mode;
    for(const k of ['hard','furious']){
     diffKey=k;o[mode+k+'StageBonus']=Math.abs(lifeDropChance(.02)-.025)<1e-12;
     o[mode+k+'ExtraLife']=roll(k,.10249,.4)==='life'&&roll(k,.10251,.4)==='';
     o[mode+k+'AmmoShield']=roll(k,.05,.3)==='bomb'&&roll(k,.05,.8)==='shield'&&roll(k,.05,.95)==='life';
    }
   }
   for(const k of ['easy','normal']){diffKey=k;o[k+'Unchanged']=lifeDropChance(.02)===.02&&roll(k,.10001,.95)===''&&roll(k,.05,.95)==='life';}
   o.forcedSingle=roll('furious',.99,.99,'life')==='life'&&powerups.length===1;
   return JSON.stringify(o);
  }finally{diffKey=save.diffKey;run.mode=save.mode;powerups=save.powerups;Math.random=save.random;stageStats.pickupsSeen=save.seen;}
 })()`,ctxv));
 for(const k of Object.keys(result))ok(result[k],'Life Up bonus: '+k);
}
