/* Four additional general-game awards. The original frozen registry and save
 * schema stay intact; this bank extends their public functions and gallery. */
(function(root){
 'use strict';
 const STORE='bof_general_achievements_1011';
 const defs=[
  {id:'general_ace_squadron',title:'Ace Squadron',desc:'Clear missions as three different pilots.',points:100,icon:0},
  {id:'general_battle_hardened',title:'Battle Hardened',desc:'Clear ten missions.',points:100,icon:1},
  {id:'general_flawless_fury',title:'Flawless Fury',desc:'Clear three consecutive missions without a death.',points:150,icon:2},
  {id:'general_combined_arms',title:'Combined Arms',desc:'Reach maximum level with three different weapons.',points:100,icon:3}
 ].map(d=>Object.freeze({...d,family:'general',steamKey:'BOF_'+d.id.toUpperCase(),plaque:'bof_general_badge_'+d.icon}));
 const registry=Object.fromEntries(defs.map(d=>[d.id,d]));
 const load=()=>{try{const d=JSON.parse(localStorage.getItem(STORE));if(d?.unlocked&&typeof d.unlocked==='object')return Object.assign({pilots:{},weapons:{},clears:0,streak:0},d);}catch(e){}return{unlocked:{},pilots:{},weapons:{},clears:0,streak:0};};
 let data=load();const seen=new WeakSet();
 const save=()=>{try{localStorage.setItem(STORE,JSON.stringify(data));return true;}catch(e){return false;}};
 const service=root.BOF_GENERAL_ACHIEVEMENTS={defs,
  list(){return defs.map(d=>({...d,unlocked:!!data.unlocked[d.id],unlockedAt:data.unlocked[d.id]?.at||null,meta:data.unlocked[d.id]?.meta||null}));},
  points(){return defs.reduce((n,d)=>n+(data.unlocked[d.id]?d.points:0),0);},
  unlock(id,meta){const d=registry[id];if(!d||data.unlocked[id])return false;data.unlocked[id]={at:Date.now(),meta:meta||{}};const persisted=save();const notice={...d,persisted};if(typeof achToastPush==='function')achToastPush(notice);if(root.TD){root.TD.Frontend?.generalToast?.(d);root.TD.Audio.play('achievement',.65);}root.dispatchEvent(new CustomEvent('bof-achievement',{detail:notice}));return true;},
  reportClear(meta){if(!meta||!meta.pilot||!Number.isFinite(meta.deaths))return;data.clears++;data.pilots[meta.pilot]=true;if(meta.pilot2)data.pilots[meta.pilot2]=true;data.streak=meta.deaths===0?data.streak+1:0;if(Object.keys(data.pilots).length>=3)this.unlock(defs[0].id,meta);if(data.clears>=10)this.unlock(defs[1].id,meta);if(data.streak>=3)this.unlock(defs[2].id,meta);save();},
  reportWeapon(weapon,level,meta){if(!Number.isInteger(weapon)||weapon<0||weapon>6||level<5||data.weapons[weapon])return;data.weapons[weapon]=true;if(Object.keys(data.weapons).length>=3)this.unlock(defs[3].id,meta);save();},
  reload(){data=load();return this.list();},snapshot(){return JSON.parse(JSON.stringify(data));}
 };
 if(typeof XART!=='undefined')defs.forEach(d=>{XART._src[d.plaque]='expansion/topdown/art/menu_1011/od_general_'+d.icon+'.png';});
 if(typeof achievementList==='function'){
  const list=achievementList,definition=achievementDefinition,points=achievementPoints,unlocked=achievementUnlocked,unlock=achievementUnlock,plaque=achPlaqueKey,reload=achievementReload,profile=achievementProfileSnapshot;
  achievementList=function(){return list().concat(service.list());};
  achievementDefinition=function(id){return registry[id]||definition(id);};
  achievementPoints=function(){return points()+service.points();};
  achievementUnlocked=function(id){return registry[id]?!!data.unlocked[id]:unlocked(id);};
  achievementUnlock=function(id,meta){return registry[id]?service.unlock(id,meta):unlock(id,meta);};
  achPlaqueKey=function(d){return d?.plaque||plaque(d);};
  achievementProfileSnapshot=function(){const p=profile();Object.assign(p.unlocked,data.unlocked);return p;};
  achievementReload=function(){service.reload();return reload();};
  // Place the new 150/100 point family after the original 200 point families,
  // retaining the original ordering of every existing award.
  const gallery=awardsRows;
  awardsRows=function(){const all=gallery(),extra=all.filter(d=>d.family==='general').sort((a,b)=>b.points-a.points||a.title.localeCompare(b.title)),rows=all.filter(d=>d.family!=='general'),at=rows.findIndex(d=>['stage_nomissile','stage_clear','weapon_max'].includes(d.family));rows.splice(at<0?rows.length:at,0,...extra);return rows;};
  const stage=achievementStageComplete,weapon=achievementWeaponMax;
  achievementStageComplete=function(n,one,two){const r=stage.apply(this,arguments);if(one&&typeof one==='object'&&!seen.has(one)){seen.add(one);service.reportClear({pilot:run.pilot,pilot2:two&&run.pilot2,stage:n,deaths:(one.deaths||0)+(two?.deaths||0),mode:run.mode,difficulty:diffKey});}return r;};
  achievementWeaponMax=function(w,level){const r=weapon.apply(this,arguments);service.reportWeapon(w|0,level,achievementMeta({weapon:w|0}));return r;};
 }
 root.addEventListener('bof-overdrive-clear',e=>service.reportClear(e.detail));
}(window));
