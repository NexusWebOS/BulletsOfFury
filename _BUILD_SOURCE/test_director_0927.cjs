module.exports=function(vm,ctxv,ok){
 const fs=require('fs'),path=require('path');
 for(const f of ['director_art_0927.js','combat_director_0927.js'])vm.runInContext(fs.readFileSync(path.join(__dirname,'../assets',f),'utf8'),ctxv,{filename:f});
 console.log('=== Director muzzle, modular rupture and Furious Tempest contracts ===');
 const results=JSON.parse(vm.runInContext(`JSON.stringify((()=>{
  const out={};
  for(const [kind,family]of Object.entries({machinegun:'mg',chaingun:'chaingun',spread:'spread',shotgun:'shotgun',magma:'fire',icebreath:'ice',yuribolt:'lightning',acid:'toxic',laser:'laser',orb:'orb',sonic:'sonic',shadow:'void',missile:'missile',roller:'roller',helix:'helix',venomx:'helix',plasma:'orb'}))out[kind+' owns its muzzle silhouette']=wm26Family(kind)===family;
  const harrier={};chaosHarrierFlash(harrier,'left_missile_bay',Math.PI/2,'missile');chaosHarrierFlash(harrier,'nose',Math.PI/2,'plasma');
  out['Harrier preserves missile and plasma muzzle types']=harrier._chFlashes[0].family==='missile'&&harrier._chFlashes[1].family==='plasma';
  const owner={x:160,y:130},part={},shape={x:180,y:145,w:70,h:60};_xChain=[];
  out['Module rupture starts once']=d27ModuleRupture(owner,part,shape,'red')&&!d27ModuleRupture(owner,part,shape,'red');
  out['Large module schedules eighteen staggered blasts']=_xChain.length===18&&new Set(_xChain.map(q=>q.t)).size===18;
  out['Cascade uses existing explosion families']=_xChain.every(q=>/^nxp_/.test(q.fam)&&q.module&&q.owner===owner);
  owner.x+=35;tickBlastChains(.01);out['Rupture stays with moving hardpoint']=_xChain.every(q=>q.x===owner.x+q.ox&&q.y===owner.y+q.oy);
  for(let i=0;i<20;i++)d27ModuleRupture(owner,{},shape,'red');out['Simultaneous module cascades are bounded']=_xChain.filter(q=>q.module).length===144;
  const stage=run.stage;run.stage++;tickBlastChains(.01);out['Changing stage clears module cascade']=!_xChain.some(q=>q.module);run.stage=stage;
  let hardCharge;
  for(const diff of ['easy','normal','hard','furious']){diffKey=diff;DIFF=DIFFS[diff];run.mode='arcade';run.stage=5;curStage=STAGES[4];spawnSubBoss__inner('spacebomber');const b=subBoss;
   siegeBomberSet(b,'charge');if(diff==='hard')hardCharge=b._bomber.dur;
   out[diff+' gets intended Tempest variant']=b._bomber.variant===(['hard','furious'].includes(diff)?1:0);
   if(diff==='furious'){out['Furious has shorter readable charge']=b._bomber.dur<hardCharge&&b._bomber.dur>1;out['Furious keeps a bomb escape lane']=b._bomber.safeLane>=0&&b._bomber.safeLane<5;out['Furious receives Crimson identity']=b.name==='TEMPEST CRIMSON ECLIPSE';}
  }
  return out;
 })())`,ctxv));
 for(const [name,result]of Object.entries(results))ok(result,name);
 const art=JSON.parse(vm.runInContext('JSON.stringify(DIRECTOR_ART)',ctxv));
 for(const [name,reel]of Object.entries(art.reels))ok(reel.frames.length===6&&fs.existsSync(path.join(__dirname,'..',art.sheets[reel.sheet].path)),name+' has six generated frames on a shipped sheet');
};
