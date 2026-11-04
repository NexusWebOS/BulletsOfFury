"use strict";
/* Four primary space guns; slot2 remains the independent Volley Missile rack.
   Supplied source poses stay static. Six baked brightness palettes are the only
   travel animation. Every facing/size is authored offline, source-over only. */
const SA114={base:{mode:spaceModeStage,level:spaceWeaponLevel,name:spaceWeaponName,icon:spaceWeaponIconKey,
 pickup:spaceWeaponPickupIndex,pool:crateWeaponPool,spawn:spawnContainer,break:breakContainer,
 fire:spaceWeaponFire,laser:spaceLaserFire,cadence:_weaponCadence,draw:drawBullets,icons:iconBlit,
 muzzle:spaceLaserMuzzleDraw,collection:polishCollection,snapshot:campSnapshot,apply:campApply,begin:beginStage},
 primary:[0,1,3,4],events:[],
 tiers:{spread:[{speed:12.8,damage:3.9,cadence:.28,width:7,height:20},{speed:13.6,damage:5.0,cadence:.26,width:8,height:24},{speed:14.4,damage:6.4,cadence:.24,width:9,height:28},{speed:15.2,damage:8.0,cadence:.22,width:10,height:31},{speed:16.0,damage:10.0,cadence:.20,width:11,height:34}],
 plasma:[{speed:8.0,damage:12,cadence:.34,width:16,height:16},{speed:8.6,damage:18,cadence:.32,width:19,height:19},{speed:9.2,damage:25,cadence:.30,width:23,height:23},{speed:9.8,damage:33,cadence:.28,width:26,height:26},{speed:10.4,damage:42,cadence:.26,width:30,height:30}]}};
SPACE_WEAPONS[2]='VOLLEY MISSILES';SPACE_WEAPONS[3]='SPREAD LASERS';SPACE_WEAPONS[4]='PLASMA CANNONS';
for(const B of Object.values(CF114_ART.banks))XART._src[B.key]=B.path;
for(const [key,M]of Object.entries(CF114_ART.icons))XART._src[key]=CF114_ART.banks[M['112']].path;
function sa114Ensure(){
 if(!Array.isArray(run.spaceLevels))run.spaceLevels=[1,1,1,0,0];
 while(run.spaceLevels.length<5)run.spaceLevels.push(0);
 for(let i=0;i<5;i++)run.spaceLevels[i]=clamp(Number.isFinite(+run.spaceLevels[i])?+run.spaceLevels[i]:(i<3?1:0),0,5);
 return run.spaceLevels;
}
function sa114Family(w=run.spaceWeapon){return w===3?'spread':w===4?'plasma':null;}
function sa114Log(event,data={}){SA114.events.push({event,t:efxClock,...data});if(SA114.events.length>256)SA114.events.shift();}
function cf114Blit(g,id,frame,x,y,pivot){const B=CF114_ART.banks[id];if(!B||!XART.rdy(B.key))return false;
 const n=clamp(frame|0,0,B.frames-1),p=pivot||B.pivot;
 g.drawImage(XART.get(B.key),(n%B.cols)*B.cw,Math.floor(n/B.cols)*B.ch,B.cw,B.ch,Math.round(x-p[0]),Math.round(y-p[1]),B.cw,B.ch);return true;
}
function cf114Frame(B,t,life){const times=B.durations,total=times.reduce((a,b)=>a+b,0),ms=life>0?clamp(t/life,0,.999999)*total:Math.max(0,t*1000);let at=0;
 for(let i=0;i<times.length;i++){at+=times[i];if(ms<at)return i;}return times.length-1;
}
function cf114Size(sizes,wanted){return sizes.reduce((a,b)=>Math.abs(b-wanted)<Math.abs(a-wanted)?b:a,sizes[0]);}
function sa114IconId(key,h){const M=CF114_ART.icons[key];if(!M)return null;const sizes=Object.keys(M).map(Number).sort((a,b)=>a-b);return M[String(sizes.filter(s=>s<=h+.01).pop()||sizes[0])];}
function sa114Icon(g,key,x,y,h,centred){const id=sa114IconId(key,h);if(!id)return null;const B=CF114_ART.banks[id];
 g.save();g.globalAlpha=1;g.globalCompositeOperation='source-over';g.shadowBlur=0;g.imageSmoothingEnabled=false;
 const ok=cf114Blit(g,id,0,centred?x:x+B.cw/2,centred?y:y+B.ch/2);g.restore();return ok?B.cw:null;
}
iconBlit=function(g,key,x,y,h,centred){if(CF114_ART.icons[key])return sa114Icon(g,key,x,y,h,centred);return SA114.base.icons.apply(this,arguments);};
spaceWeaponLevel=function(){sa114Ensure();return run.spaceWeapon>=3?run.spaceLevels[run.spaceWeapon]||0:SA114.base.level.apply(this,arguments);};
spaceWeaponName=function(){return sa114Family()?SPACE_WEAPONS[run.spaceWeapon]:SA114.base.name.apply(this,arguments);};
spaceWeaponIconKey=function(){return sa114Family()?'space_'+sa114Family()+'_icon_'+Math.max(1,spaceWeaponLevel()):SA114.base.icon.apply(this,arguments);};
function spaceWeaponIconFor(w,lv){return w===3||w===4?'space_'+sa114Family(w)+'_icon_'+clamp(lv||1,1,5):w===0?'space_laser_icon_'+lv:w===1?'space_fusion_icon_'+Math.max(1,lv):spaceVolleyIconKey(lv);}
function spacePickupLevel(w){sa114Ensure();return clamp((w>=3?(run.spaceLevels[w]||0):(run.spaceLevels[w]||1))+1,1,5);}
spaceWeaponPickupIndex=function(p){return Number.isInteger(p?.spaceType)&&p.spaceType>=0&&p.spaceType<5?p.spaceType:SA114.base.pickup.apply(this,arguments);};
crateWeaponPool=function(){return spaceWeaponsActive()?[0,1,2,3,4]:SA114.base.pool.apply(this,arguments);};
spawnContainer=function(){const first=powerups.length,out=SA114.base.spawn.apply(this,arguments);
 if(spaceWeaponsActive())for(let i=first;i<powerups.length;i++){const p=powerups[i];if(p.kind==='crate'&&Number.isInteger(p.wtype)&&p.wtype>=0&&p.wtype<5){p.spaceType=p.wtype;if(p.spaceType>=3)p.w=p.h=40;}}
 return out;
};
breakContainer=function(p){const first=powerups.length,out=SA114.base.break.apply(this,arguments);
 if(Number.isInteger(p?.spaceType))for(let i=first;i<powerups.length;i++)if(powerups[i].kind==='weapon'){powerups[i].spaceType=p.spaceType;if(p.spaceType>=3)powerups[i].w=powerups[i].h=28;}
 return out;
};
spaceModeStage=function(num){const before=run.spaceWeapon,L=sa114Ensure().slice(),was=!!run.spaceMode,out=SA114.base.mode.apply(this,arguments);sa114Ensure();
 if(num===5||num===9){run.spaceLevels[3]=L[3];run.spaceLevels[4]=L[4];if((before===3||before===4)&&L[before]>0)run.spaceWeapon=before;if(!was)run._wbag=null;}
 else if(was)run._wbag=null;return out;
};
function spacePrimaryCadence(w,lv){const f=sa114Family(w);return f?SA114.tiers[f][clamp(lv||1,1,5)-1].cadence:.24;}
function sa114Fire(family){if(ht27Locked())return;sa114Ensure();const lv=Math.max(1,spaceWeaponLevel()),D=SA114.tiers[family][lv-1],B=CF114_ART.banks[family+'_'+lv];
 let ports=spaceShipHardpoints(player.x,player.y,SPACE_SHIP_SIZE).laser;
 if(spaceAkimboActive())ports=[-.38,-.14,.14,.38].map((q,i)=>({x:player.x+q*SPACE_SHIP_SIZE,y:player.y-SPACE_SHIP_SIZE*.17,side:i<2?-1:1}));
 for(const p of ports)for(let d=0;d<(family==='spread'?3:1);d++){const offset=B.angles?.[d]||0,a=-Math.PI/2+offset;
  pBullets.push({kind:'spaceLaser',_cf114:family,x:p.x,y:p.y-6,vx:Math.cos(a)*D.speed,vy:Math.sin(a)*D.speed,w:D.width,h:D.height,dmg:D.damage,lv,t:0,
   side:p.side,_cf114Dir:d,_muzzleX:p.x,_muzzleY:p.y,_noArsenal:true});}
 player._spaceMuzzle=.13;player._spaceMuzzleLv=lv;spaceWeaponCue('spaceLaserCannon','laserCannon');
 sa114Log('fire',{family,lv,ports:ports.length,rounds:ports.length*(family==='spread'?3:1)});
}
spaceWeaponFire=function(){const f=sa114Family();if(f)return sa114Fire(f);return SA114.base.fire.apply(this,arguments);};
// Armory's native swap still calls the laser entry point for a tap weapon.
spaceLaserFire=function(){const f=sa114Family();if(f)return sa114Fire(f);return SA114.base.laser.apply(this,arguments);};
_weaponCadence=function(){const f=spaceWeaponsActive()&&sa114Family();return f?SA114.tiers[f][Math.max(1,spaceWeaponLevel())-1].cadence:SA114.base.cadence.apply(this,arguments);};
spaceLaserMuzzleDraw=function(g,lv,frame,x,y,size){const f=spaceWeaponsActive()&&sa114Family();if(!f)return SA114.base.muzzle.apply(this,arguments);
 g.save();g.globalAlpha=1;g.globalCompositeOperation='source-over';g.shadowBlur=0;g.imageSmoothingEnabled=false;cf114Blit(g,f+'_muzzle',clamp(frame,0,3),x,y);g.restore();
};
function sa114DrawRound(b){if(b.dead||b._launchDelay>0)return;
 const family=b._cf114,lv=clamp(b.lv||1,1,5);
 if(b.kind==='spaceImpact'){if(!b._quietVisual){const id=family+'_impact';const B=CF114_ART.banks[id];if(B)cf114Blit(ctx,id,cf114Frame(B,b.t,b.life),b.x,b.y);}return;}
 const id=family+'_'+lv,B=CF114_ART.banks[id],glow=Math.floor((b.t||0)*12)%6;
 cf114Blit(ctx,id,glow*(B.dirs||1)+(b._cf114Dir||0),b.x,b.y);
}
drawBullets=function(){const all=pBullets;pBullets=all.filter(b=>!b._cf114);try{SA114.base.draw.apply(this,arguments);}finally{pBullets=all;}
 ctx.save();ctx.globalAlpha=1;ctx.globalCompositeOperation='source-over';ctx.shadowBlur=0;ctx.imageSmoothingEnabled=false;
 for(const b of all)if(b._cf114)sa114DrawRound(b);ctx.restore();
};
polishCollection=function(){const rows=SA114.base.collection.apply(this,arguments),O=achievementState.owned||{};sa114Ensure();
 for(const space of[3,4])rows.push({w:0,elem:null,space,name:SPACE_WEAPONS[space],owned:!!O['arsenal_space_'+space]||run.spaceLevels[space]>0,key:spaceWeaponIconFor(space,1)});return rows;
};
campSnapshot=function(){const s=SA114.base.snapshot.apply(this,arguments);s.spaceArsenal={levels:sa114Ensure().slice(),weapon:SA114.primary.includes(run.spaceWeapon)?run.spaceWeapon:0,ground:run._groundLoadout?JSON.parse(JSON.stringify(run._groundLoadout)):null};return s;};
campApply=function(s){const ok=SA114.base.apply.apply(this,arguments);if(!ok)return ok;
 const A=s.spaceArsenal;run._groundLoadout=A?.ground&&typeof A.ground==='object'?JSON.parse(JSON.stringify(A.ground)):null;run.spaceLevels=Array.isArray(A?.levels)?A.levels.slice(0,5):[1,1,1,0,0];sa114Ensure();run.spaceWeapon=SA114.primary.includes(A?.weapon)&&run.spaceLevels[A.weapon]>0?A.weapon:0;return ok;
};
function sa114Warm(){for(const [id,B]of Object.entries(CF114_ART.banks))if(/^(spread|plasma)_(?:[1-5]|muzzle|impact)$/.test(id)||/^(spread|plasma)_icon_[1-5]_(?:32|36|40|hit)$/.test(id))XART.rdy(B.key);}
beginStage=function(){const out=SA114.base.begin.apply(this,arguments);if(run.stage===5||run.stage===9)sa114Warm();return out;};
globalThis.BOF_SPACE_ARSENAL_1104={state:SA114,art:CF114_ART,fire:sa114Fire,ensure:sa114Ensure};
