module.exports=function(vm,ctxv,ok){
 const fs=require('fs'),path=require('path');
 vm.runInContext(fs.readFileSync(path.join(__dirname,'../assets/campaign_world_0930.js'),'utf8'),ctxv,{filename:'campaign_world_0930.js'});
 console.log('=== 384. Expanded campaign geography and fixed horizontal map flight ===');
 const out=JSON.parse(vm.runInContext(`JSON.stringify((()=>{
  const o={},save={cursor:sselCursor,ship:sselShip,boot:sselBoot,bonus:campaign.bonusUnlocked};
  sselBoot=0;sselCursor=1;sselShip=null;let left=false,right=false,valid=true;
  for(const stage of [1,4,7,3,6,2]){sselCursor=stage;for(let i=0;i<180;i++){sselShipUpdate(1/60);const q=sselShip;left||=q.face===-1;right||=q.face===1;valid&&=Math.abs(Math.abs(q.head)-Math.PI/2)<1e-8&&q.bank===0;}}
  o['diagonal travel and arrival never pivot the ship vertically']=valid&&left&&right;
  const dest=sselFlagXY(2);sselShip.x=dest.x;sselShip.y=dest.y+100;sselShip.face=-1;sselShipUpdate(1/60);
  o['vertical legs retain the last horizontal direction']=sselShip.face===-1;
  const hub=cmap2World('hub');o['HQ is at the exact centre of the expanded world']=hub.x===CM2_W/2&&hub.y===CM2_H/2;
  o['portal is far north of the main mission ring']=cmap2World(9).y<Math.min(...[1,2,3,4,5,6,7,8].map(s=>cmap2World(s).y))-150;
  campaign.bonusUnlocked=true;openStageSelect(9,{});o['reopening an unlocked portal selects Stage 9 rather than clamping to Stage 8']=sselCursor===9;
  campaign.bonusUnlocked=false;openStageSelect(9,{});o['a locked portal cannot be selected by opening the map']=sselCursor!==9;
  o['western frontier has no unlock or stage id']=MAP30.land.every(q=>!q.stage)&&!SSEL_POS.expansion;
  sselCursor=save.cursor;sselShip=save.ship;sselBoot=save.boot;campaign.bonusUnlocked=save.bonus;return o;
 })())`,ctxv));
 for(const [name,value]of Object.entries(out))ok(value,name);
};
