"use strict";
/* Supplied ColeForge frames, metadata timing and fixed offline size variants.
   Native death chains, rings, shields, damage and warnings keep their owners. */
const CFX114={base:{effects:updateEffects,draw:drawEffects,smoke:drawSmokeTrails,ring:drawSmokeRings,
 shock:drawShockRings,death:unitDeathFX,explode,nuke:nukeAt,nukeDraw:drawNukeImpacts,atom:atomBlast,atomDraw:drawAtomBooms,
 enemyShield:drawEnemyShieldLayer,mega:axelMegaShieldDraw,flashes:drawNavalFlashes,
 atomic:ca111FX,atomicHit:ca111HazardTouches,begin:beginStage,powerups:drawPowerups},
 fx:[],seen:new WeakSet(),axel:new WeakMap(),serial:0,events:[],suppressNuke:0,
 sizes:{ring:[64,96,128,192,256,384,512],smoke:[24,40,64,96],column:[96,160,256],fire:[32,48,64,96],small:[24,40,64],dust:[32,64,96],atomic:[128,256,512],cole_nuke:[128,256,384]}};
function cfx114Log(event,data={}){CFX114.events.push({event,t:efxClock,...data});if(CFX114.events.length>256)CFX114.events.shift();}
function cfx114Id(kind,size){return kind+'_'+cf114Size(CFX114.sizes[kind],size);}
function cfx114Spawn(kind,x,y,size,opt={}){
 const id=cfx114Id(kind,size),B=CF114_ART.banks[id];if(!B)return null;
 const q={id,kind,x,y,t:0,life:opt.life||B.durations.reduce((a,b)=>a+b,0)/1000,owner:opt.owner,ox:opt.ox||0,oy:opt.oy||0,stage:run.stage};
 CFX114.fx.push(q);if(CFX114.fx.length>24){const i=CFX114.fx.findIndex(f=>f.kind==='small');CFX114.fx.splice(i<0?0:i,1);}XART.rdy(B.key);cfx114Log('spawn',{kind,id,x,y});return q;
}
updateEffects=function(dt){const out=CFX114.base.effects.apply(this,arguments);
 for(const f of CFX114.fx){f.t+=dt;if(f.owner&&!f.owner.dead){f.x=f.owner.x+f.ox;f.y=(f.owner._drawY??f.owner.y)+f.oy;}}
 CFX114.fx=CFX114.fx.filter(f=>f.t<f.life&&f.stage===run.stage);
 if(axelMegaShieldActive()){const A=CFX114.axel.get(player)||{age:0};A.age+=dt;CFX114.axel.set(player,A);}else CFX114.axel.delete(player);
 return out;
};
explode=function(x,y,size,palette,kind,fam,cls){const first=explosions.length,out=CFX114.base.explode.apply(this,arguments);
 if(CFX114.suppressNuke)for(let i=first;i<explosions.length;i++)explosions[i]._cf114Nuke=true;
 // An occasional extra small burst supplements the native family, never a
 // replacement for its class-specific main blast, sound or damage event.
 else if(!cls&&!fam&&size>=6&&size<=24&&(!palette||palette==='red'||palette==='orange')&&++CFX114.serial%4===0)cfx114Spawn('small',x,y,size*2);
 return out;
};
unitDeathFX=function(e,cls){const out=CFX114.base.death.apply(this,arguments);
 if(!e||CFX114.seen.has(e))return out;CFX114.seen.add(e);
 const bossy=cls==='boss'||cls==='mini'||e===boss||e===subBoss||e._boss||e._mini;
 // Named Stage8 destruction/corruption sequences retain their exact palette.
 if(run.stage===8&&bossy)return out;
 const size=Math.max(e.w||24,e.h||24),x=e.x,y=e._drawY??e.y;
 if(size>=58)cfx114Spawn('fire',x,y+size*.22,Math.min(96,size*.7),{owner:e,oy:size*.22});
 if(bossy)cfx114Spawn('column',x,y+size*.23,Math.min(256,size*.85),{owner:e,oy:size*.23});
 if(run.stage===4&&e.ground)cfx114Spawn('dust',x,y,size*.7);
 return out;
};
nukeAt=function(x,y){CFX114.suppressNuke++;let out;try{out=CFX114.base.nuke.apply(this,arguments);}finally{CFX114.suppressNuke--;}
 // Damage, crate interactions, launch stock and the nuclear sound stay native.
 const f=cfx114Spawn('cole_nuke',x,y,256);for(const q of nukeImpacts)if(q.x===x&&q.y===y&&q.t===0)q._cf114=true;
 return out;
};
drawNukeImpacts=function(){const all=nukeImpacts;nukeImpacts=all.filter(n=>!n._cf114);try{return CFX114.base.nukeDraw.apply(this,arguments);}finally{nukeImpacts=all;}};
atomBlast=function(){const first=atomBooms.length,out=CFX114.base.atom.apply(this,arguments);for(let i=first;i<atomBooms.length;i++)atomBooms[i]._cf114LZ='atomic_512';return out;};
drawAtomBooms=function(){const all=atomBooms,white=atomFlash;
 if(!all.some(b=>b._cf114LZ))return CFX114.base.atomDraw.apply(this,arguments);
 atomBooms=all.filter(b=>!b._cf114LZ);atomFlash=0;try{CFX114.base.atomDraw.apply(this,arguments);}finally{atomBooms=all;atomFlash=white;}
 ctx.save();ctx.globalAlpha=1;ctx.globalCompositeOperation='source-over';ctx.shadowBlur=0;ctx.imageSmoothingEnabled=false;
 for(const b of all)if(b._cf114LZ){const B=CF114_ART.banks[b._cf114LZ];cf114Blit(ctx,b._cf114LZ,cf114Frame(B,b.t,b.dur),b.x,b.y);}ctx.restore();
 // Retain the existing blinding hold and its last/top draw position.
 atomBooms=[];try{CFX114.base.atomDraw.apply(this,arguments);}finally{atomBooms=all;}
};
drawEffects=function(){const all=explosions;explosions=all.filter(e=>!e._cf114Nuke);try{CFX114.base.draw.apply(this,arguments);}finally{explosions=all;}
 ctx.save();ctx.globalAlpha=1;ctx.globalCompositeOperation='source-over';ctx.shadowBlur=0;ctx.imageSmoothingEnabled=false;
 for(const f of CFX114.fx){const B=CF114_ART.banks[f.id];cf114Blit(ctx,f.id,cf114Frame(B,f.t,f.life),f.x,f.y);}ctx.restore();
};
drawSmokeTrails=function(){const all=smokeTrails;smokeTrails=all.filter(s=>s.kind==='missile'||!XART.rdy(CF114_ART.banks[cfx114Id('smoke',(s.sz0||s.sz||12)+(s.grow||0))].key));try{CFX114.base.smoke.apply(this,arguments);}finally{smokeTrails=all;}
 ctx.save();ctx.globalAlpha=1;ctx.globalCompositeOperation='source-over';ctx.shadowBlur=0;ctx.imageSmoothingEnabled=false;
 for(const s of all){if(s.kind==='missile')continue;const id=cfx114Id('smoke',(s.sz0||s.sz||12)+(s.grow||0)),B=CF114_ART.banks[id];cf114Blit(ctx,id,cf114Frame(B,s.t,s.life),s.x,s.y);}ctx.restore();
};
drawSmokeRings=function(front){const all=_smokeRings;_smokeRings=all.filter(r=>r.angle!=null||!XART.rdy(CF114_ART.banks[cfx114Id('ring',r.size*3.5)].key));try{CFX114.base.ring.apply(this,arguments);}finally{_smokeRings=all;}
 ctx.save();ctx.globalAlpha=1;ctx.globalCompositeOperation='source-over';ctx.shadowBlur=0;ctx.imageSmoothingEnabled=false;
 for(const r of all){if(r.angle!=null||!!r.front!==!!front)continue;const id=cfx114Id('ring',r.size*3.5),B=CF114_ART.banks[id];cf114Blit(ctx,id,cf114Frame(B,r.t,r.life),r.x,r.y);}ctx.restore();
};
drawShockRings=function(){const all=shockRings;shockRings=all.filter(s=>s.fam!=='nsr_fire'||!XART.rdy(CF114_ART.banks[cfx114Id('ring',s.r1*2.4)].key));try{CFX114.base.shock.apply(this,arguments);}finally{shockRings=all;}
 ctx.save();ctx.globalAlpha=1;ctx.globalCompositeOperation='source-over';ctx.shadowBlur=0;ctx.imageSmoothingEnabled=false;
 for(const s of all){if(s.fam!=='nsr_fire')continue;const id=cfx114Id('ring',s.r1*2.4),B=CF114_ART.banks[id];cf114Blit(ctx,id,cf114Frame(B,s.t,s.life),s.x,s.y);}ctx.restore();
};
function cfx114Shield(kind,size,phase,t,hit,x,y){const n=cf114Size([64,96,128,192,256,384],size),id=kind+'_'+n;
 if(![id,kind+'_hold_'+n,kind+'_hit_'+n].map(k=>XART.rdy(CF114_ART.banks[k].key)).every(Boolean))return false;
 let key=id,frame=clamp(Math.floor(t/.067),0,4);
 if(phase==='broken'){if(t>=.30)return true;frame=4-clamp(Math.floor(t/.06),0,4);}
 else if(phase!=='deploy'||t>=.335){key=kind+'_hold_'+n;frame=Math.floor(t*12)%6;}
 if(hit>0){key=kind+'_hit_'+n;frame=0;}
 ctx.save();ctx.globalAlpha=1;ctx.globalCompositeOperation='source-over';ctx.shadowBlur=0;ctx.imageSmoothingEnabled=false;cf114Blit(ctx,key,frame,x,y);ctx.restore();return true;
}
drawEnemyShieldLayer=function(e,front){const s=e?._esh,kind=s?.family==='bubble_toxic'?'shield_green':['bubble_hex','bubble_volt'].includes(s?.family)?'shield_blue':null;
 // New articulated late rosters already own registered per-piece shells.
 if(!kind||e._s711||e._s811||e._s911||e._dyingT!=null)return CFX114.base.enemyShield.apply(this,arguments);
 if(!front)return;
 if(!cfx114Shield(kind,Math.max(e._drawW||e.w||32,e._drawH||e.h||32)*2.5,s.phase,s.animT||0,s.hitT||0,e.x,e.y))return CFX114.base.enemyShield.apply(this,arguments);
};
axelMegaShieldDraw=function(){if(!axelMegaShieldActive())return;const age=CFX114.axel.get(player)?.age||0;
 if(!cfx114Shield('shield_blue',axelMegaShieldRadius()*3.2,age<.335?'deploy':'active',age,player._megaFlash||0,player.x,player.y))return CFX114.base.mega.apply(this,arguments);
};
ca111FX=function(kind){const f=CFX114.base.atomic.apply(this,arguments);if(f&&kind==='nuclear_blast'){f._cf114Atomic=cfx114Id('atomic',f.size);XART.rdy(CF114_ART.banks[f._cf114Atomic].key);}return f;};
// The inherited hazard remains the upper bound. An explicit hot cap/stem
// trims invisible hits as the new blast grows; grey aftermath is decorative.
function cfx114AtomicHot(f,p){const B=CF114_ART.banks[f._cf114Atomic],frame=cf114Frame(B,f.t,f.life);if(frame>21)return false;
 const s=B.cw/128,x=(p.x-f.x)/s+64,y=(p.y-f.y)/s+64;
 const capY=[99,95,89,82,76,67,58,48,42,35,30,25,23,22,22,22,22,23,24,25,27,29][frame],rx=[8,17,24,29,29,29,30,33,38,42,44,46,47,47,47,47,46,46,45,44,43,41][frame],ry=Math.max(3,Math.min(18,frame*1.6));
 return((x-64)/rx)**2+((y-capY)/ry)**2<=1||frame>=5&&Math.abs(x-64)<10&&y>capY+ry*.5&&y<102;
}
ca111HazardTouches=function(f,p){return f?._cf114Atomic?CFX114.base.atomicHit.apply(this,arguments)&&cfx114AtomicHot(f,p):CFX114.base.atomicHit.apply(this,arguments);};
drawNavalFlashes=function(){const all=CA111.fx;CA111.fx=all.filter(f=>!f._cf114Atomic);try{CFX114.base.flashes.apply(this,arguments);}finally{CA111.fx=all;}
 ctx.save();ctx.globalAlpha=1;ctx.globalCompositeOperation='source-over';ctx.shadowBlur=0;ctx.imageSmoothingEnabled=false;
 for(const f of all)if(f._cf114Atomic){const B=CF114_ART.banks[f._cf114Atomic];cf114Blit(ctx,f._cf114Atomic,cf114Frame(B,f.t,f.life),f.x,f.y,[B.cw/2,B.ch/2]);}ctx.restore();
};
function cfx114NewPickup(p){return spaceWeaponsActive()&&['crate','weapon'].includes(p.kind)&&[3,4].includes(p.spaceType);}
drawPowerups=function(){const all=powerups;powerups=all.filter(p=>!cfx114NewPickup(p));try{CFX114.base.powerups.apply(this,arguments);}finally{powerups=all;}
 ctx.save();ctx.globalAlpha=1;ctx.globalCompositeOperation='source-over';ctx.shadowBlur=0;ctx.imageSmoothingEnabled=false;
 for(const p of all){if(p.dead||!cfx114NewPickup(p))continue;const family=sa114Family(p.spaceType),lv=spacePickupLevel(p.spaceType),size=p.kind==='crate'?40:36;
  const id=family+'_icon_'+lv+'_'+(p.kind==='crate'&&p.flash>0?'hit':size),yy=p.y+Math.sin((p.t||0)*2.4)*2;cf114Blit(ctx,id,0,p.x,yy);}
 ctx.restore();
};
function cfx114Warm(stage){const list=['ring_128','ring_256','smoke_24','smoke_40','smoke_64','small_40','fire_48','fire_64','column_160','dust_64'];
 if(_pilotKey()==='cole')list.push('cole_nuke_256');if(_pilotKey()==='lizzie')list.push('atomic_512');if(stage===6)list.push('atomic_128','atomic_256','atomic_512');
 for(const kind of['shield_blue','shield_green'])for(const n of[96,128,192,256])list.push(kind+'_'+n,kind+'_hold_'+n,kind+'_hit_'+n);
 for(const id of list)XART.rdy(CF114_ART.banks[id].key);
}
beginStage=function(){CFX114.fx=[];CFX114.seen=new WeakSet();CFX114.axel=new WeakMap();const out=CFX114.base.begin.apply(this,arguments);cfx114Warm(run.stage);return out;};
globalThis.BOF_COLEFORGE_FX_1104={state:CFX114,spawn:cfx114Spawn,warm:cfx114Warm};
