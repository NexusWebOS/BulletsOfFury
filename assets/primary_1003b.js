"use strict";
/* Stage progression owns the primary upgrade, including passwords and old saves.
   Mike's October 3 rule includes Cole. A deliberate loadout choice is persistent. */
const PRIMARY1003B={unlocked:chaingunIsUnlocked,begin:beginStage,start:startRun,
 snapshot:campSnapshot,apply:campApply,pool:crateWeaponPool,forms:weaponBaseForms,
 select:weaponFormSelect,sync:chaingunMGSync};
function primary1003bEligible(){return !!run&&((run.stage>=6&&run.stage<=8)||run.stage===5&&!!run._earnedUnlocks?.chaingun);}
chaingunColeExempt=function(){return false;};
chaingunIsUnlocked=function(){return primary1003bEligible()||PRIMARY1003B.unlocked();};
chaingunSeedLoadout=function(){
 if(!primary1003bEligible())return;
 (run._earnedUnlocks||(run._earnedUnlocks={})).chaingun=true;
 const chosen=run._primary1003b==='mg'?0:7,other=chosen===7?0:7;
 if(Array.isArray(run.loadout)&&run.loadout.length){
  const i=run.loadout.indexOf(other);if(i>=0)run.loadout[i]=chosen;
  run.loadout=[...new Set(run.loadout)];
  if(!run.loadout.includes(chosen)&&run.loadout.length<FORGE_LOADOUT_MAX)run.loadout.push(chosen);
 }
 run._chainSeeded=true;
};
chaingunReplacesMG=function(){return primary1003bEligible()&&run.stage>=6&&run._primary1003b!=='mg'&&!spaceWeaponsActive();};
chaingunMGSync=function(){
 if(chaingunReplacesMG()&&run.wlevels){run.wlevels[7]=Math.max(1,run.wlevels[0]|0,run.wlevels[7]|0);chaingunSeedLoadout();}
 return PRIMARY1003B.sync.apply(this,arguments);
};
function primary1003bApply(){
 if(!primary1003bEligible())return;
 chaingunSeedLoadout();chaingunMGSync();
 for(const side of ['left','right'])XART.rdy('repair30_chaingun_mount_'+_pilotKey()+'_'+side);
 XART.rdy('repair30_chaingun_barrel_top');
}
beginStage=function(n){const r=PRIMARY1003B.begin.apply(this,arguments);for(const seat of seatList())withSeat(seat,primary1003bApply);return r;};
startRun=function(){delete run._primary1003b;if(typeof run2!=='undefined')delete run2._primary1003b;return PRIMARY1003B.start.apply(this,arguments);};
campSnapshot=function(){const s=PRIMARY1003B.snapshot.apply(this,arguments);s.primary1003b=run._primary1003b==='mg'?'mg':'chain';return s;};
campApply=function(s){
 if(!s||s.v!==CAMP_SAVE_VER)return false;
 run._primary1003b=s.primary1003b==='mg'?'mg':'chain';
 const r=PRIMARY1003B.apply.apply(this,arguments);if(r)primary1003bApply();return r;
};
crateWeaponPool=function(all){const p=PRIMARY1003B.pool.apply(this,arguments);if(!primary1003bEligible()||spaceWeaponsActive())return p;
 const chosen=run._primary1003b==='mg'?0:7;return [...new Set(p.map(w=>w===0||w===7?chosen:w).concat(chosen))];};
weaponBaseForms=function(w){
 const out=PRIMARY1003B.forms.apply(this,arguments);
 if((w===0||w===7)&&primary1003bEligible())out.push({kind:'primary1003b',id:w===7?'mg':'chain',name:w===7?'MACHINE GUN':'ANCHORED CHAINGUN',key:weaponIconKey(w===7?0:7,1)});
 return out;
};
weaponFormSelect=function(w,opt){
 if(opt?.kind!=='primary1003b')return PRIMARY1003B.select.apply(this,arguments);
 if(!primary1003bEligible()||![0,7].includes(w)||!['mg','chain'].includes(opt.id))return 'locked';
 run._primary1003b=opt.id;chaingunSeedLoadout();
 const chosen=opt.id==='mg'?0:7,lv=Math.max(1,run.wlevels[0]|0,run.wlevels[7]|0);
 run.wlevels[0]=run.wlevels[7]=lv;
 if(run.weapon===0||run.weapon===7){run.weapon=chosen;run.wlevel=lv;forgeApply();}
 run._wbag=[];
 if(loadoutScr){loadoutScr.pool=crateWeaponPool(true);loadoutScr.sel=Math.max(0,run.loadout.indexOf(chosen));loadoutScr.vsel=0;loadoutScr.previewId=null;}
 return 'ok';
};
// The remaining sewer pods now use selected, authored mutants on the same wave beats.
Object.assign(MM1003_SLOTS[7],{s7canister:'hexpyre',s7mine:'impharrow'});
