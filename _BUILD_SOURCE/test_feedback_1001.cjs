module.exports=function(vm,ctxv,ok){
 console.log('=== October 1. Opposing-element feedback ===');
 const out=JSON.parse(vm.runInContext(`(()=>{
  const saved={floaters,stage:run.stage,pilot:run.pilot,stageTimer};let o={};
  try{
   run.stage=2;run.pilot='cole';stageTimer=100;floaters=[];
   const e={x:180,y:150,hp:200,maxhp:200,_volc:true};
   const hit=()=>elementalDamageResult(e,'enemy',{_el:'ice'},20);
   o['ice weakness is +50%']=hit().dmg===30;
   o['critical text is blue']=floaters.length===1&&floaters[0].elementCrit&&floaters[0].color==='#83d9ff';
   for(let i=0;i<12;i++)hit();
   o['rapid fire keeps full damage without stacking text']=floaters.length===1&&hit().dmg===30;
   stageTimer+=.46;hit();o['sustained fire refreshes readable text']=floaters.length===2;
   const n=floaters.length;elementalDamageResult(e,'enemy',{},20);
   o['kinetic hit clears previous blue flash']=hitFlashColor(e)==='#ffffff'&&floaters.length===n;
   const locked={x:100,y:100,_volc:true,_noHit:true};elementalDamageResult(locked,'boss',{_el:'ice'},20);
   o['invulnerable transition emits no critical label']=floaters.length===n;
   run.stage=3;const b={x:200,y:150,_s3Nuclear:{mode:'ice'}};
   o['fire weakness is +50%']=elementalDamageResult(b,'boss',{_el:'fire'},20).dmg===30&&hitFlashColor(b)==='#ff3b30';
   b._s3Nuclear.mode='neutral';const count=floaters.length;
   o['neutral opening has no weakness label']=elementalDamageResult(b,'boss',{_el:'fire'},20).dmg===20&&hitFlashColor(b)==='#ffffff'&&floaters.length===count;
   return JSON.stringify(o);
  }finally{floaters=saved.floaters;run.stage=saved.stage;run.pilot=saved.pilot;stageTimer=saved.stageTimer;}
 })()`,ctxv));
 for(const [n,v] of Object.entries(out))ok(v,'Feedback 1001: '+n);
};
