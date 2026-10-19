'use strict';
module.exports=function(vm,c,ok){
 console.log('=== 387. Machine gun upgrades retain every round and fire from the nose ===');
 const result=JSON.parse(vm.runInContext(`JSON.stringify((()=>{
  const out={};ht27Stop();coopOn=false;run.mode='arcade';run.pilot='cole';beginStage(1);state=GS.PLAY;
  BOFCinematicDirector.cancel();story=fb2Talk=special=null;player.reset();player.dead=player.out=false;
  run.spaceMode=false;run.gravityShipReady=false;gravityMode=null;run.sonicT=run.dkT=0;
  run.weapon=0;run.forge={};run.infusion=null;run.wvars=[];run.loadout=[0];
  boss=subBoss=null;bossActive=subBossActive=false;enemies=[];stagePlan=[];
  function fire(lv){run.wlevel=lv;run.wlevels[0]=lv;pBullets=[];wm26Releases=[];pShoot();return pBullets.filter(b=>b.kind==='mg'&&!b._cal50);}
  for(let lv=0;lv<=5;lv++){
   let count=true,nose=true,flash=true;
   for(const p of PILOTS){run.pilot=p.key;pilotIndex=PILOTS.indexOf(p);player.x=240;player.y=360;
    const origin=wm26PlayerNose(),rounds=fire(lv),xs=rounds.map(b=>b.x);
    count=count&&rounds.length===lv+1;
    nose=nose&&rounds.length>0&&Math.abs(xs.reduce((s,x)=>s+x,0)/rounds.length-origin.x)<1e-8&&
     Math.max(...xs)-Math.min(...xs)<=20&&rounds.every(b=>b.y===origin.y-6&&b.vx===0&&b.vy===-9&&b.dmg===2+Math.floor(lv/2));
    const f=wm26Releases.filter(f=>f.player);
    flash=flash&&f.length===1&&f[0].x===origin.x&&f[0].y===origin.y;
   }
   out['All nine pilots L'+lv+' fire '+(lv+1)+' actual MG projectiles']=count;
   out['All nine pilots L'+lv+' launch a tight, symmetric nose row with native speed/damage']=nose;
   out['All nine pilots L'+lv+' use one muzzle flash at that same nose']=flash;
  }
  run.pilot='cole';pilotIndex=PILOTS.findIndex(p=>p.key==='cole');
  run.forge={0:{elem:'wind',lv:3}};run.infusion={elem:'wind',lv:3};
  const forged=fire(3);out['A forged Wind MG retains its full level-plus-one row and element']=forged.length===4&&forged.every(b=>b._inf==='wind');
  run.forge={};run.infusion=null;run.weapon=7;let chain=true;
  for(let lv=1;lv<=5;lv++){run.wlevel=run.wlevels[7]=lv;pBullets=[];wm26Releases=[];pShoot();
   chain=chain&&pBullets.length===(lv===1?1:2)&&pBullets.every(b=>b._cal50&&b._chaingun)&&wm26Releases.length===0;}
  out['The separate chaingun retains its pod count and never creates an MG nose flash']=chain;
  run.weapon=0;return out;
 })())`,c));
 for(const [name,passed]of Object.entries(result))ok(passed,name);
};
