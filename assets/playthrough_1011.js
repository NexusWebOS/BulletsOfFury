"use strict";
/* October 11 recording. Physical parts own drawing, damage and muzzles together. */
const PT11={events:[],draws:{},base:{load:stageLoadBegin,init:er26Init,cell:mr27Cell,shape:mr27Shape,mount:mr27Mount,hullAt:mr27HullAt,
 blit:mr27Blit,roster:mr27Draw,head:fztHeadDraw,rearm:stage4ShieldBeginRearm,nodes:stage4ShieldSyncNodes,
 target:stage4CoreTurretTarget,war:er26WarTick,over:mr27Over,escort:er26EscortTick,
 hammerInit:hammerBossInit,hammerTick:hammerBossTick,hammerDamage:hammerBossDamage,hammerDraw:hammerBossDraw,
 arch:archBlit,activation:repair30ChromiumActivationDraw,break:hammerBossModuleBreak,pickup:applyPowerup,
 powerDraw:drawPowerups,play:updatePlay,begin:beginStage,world:drawWorld,enemyPlate:sm10EnemyPlate},radio:null};
for(const bank of Object.values(PT11_ART))for(const a of bank)XART._src[a.key]=a.path;
function pt11Log(event,data={}){PT11.events.push({event,...data});if(PT11.events.length>180)PT11.events.shift();}
function pt11Ready(name){return PT11_ART[name].map(a=>XART.rdy(a.key)).every(Boolean);}
function pt11Plate(name,f,x,y,k=1,rot=0,flash=0,form=null){
 const a=PT11_ART[name]?.[f];if(!a||!XART.rdy(a.key))return false;
 const im=form==='fire'?xartPalette(a.key,'#df5529'):XART.get(a.key);if(!im)return false;
 ctx.save();ctx.translate(x,y);ctx.rotate(rot);ctx.imageSmoothingEnabled=false;
 ctx.drawImage(im,-a.pivot[0]*k,-a.pivot[1]*k,a.w*k,a.h*k);
 if(flash>0){const white=xartTint(a.key,'#ffffff',1);ctx.globalAlpha*=Math.min(.32,flash*2);ctx.drawImage(white,-a.pivot[0]*k,-a.pivot[1]*k,a.w*k,a.h*k);}
 ctx.restore();PT11.draws[name]=(PT11.draws[name]||0)+1;return true;
}
stageLoadBegin=function(n,keys){const names=n===2?['furnace_head','fire_wave']:n===3?['ice_parts','ice_jet_a','ice_jet_b']:n===5?['hammer_core','harrier_cannon']:n===8?['ice_parts','hammer_core','furnace_head','black_heart','fire_wave','drone_raise']:[];
 names.push('fire_spray','sonic_pulse');
 return PT11.base.load.call(this,n,[...(keys||[]),...names.flatMap(k=>PT11_ART[k].map(a=>a.key))]);};
/* Recorded Forge feedback: sound reads as pressure, and a forged flame owns a
   distinct plume. The authored mask drives its contact bands at the same scale. */
PT11.base.round=ea11RoundDraw;PT11.base.flame=flameDraw;
PT11.base.flameHit=flameHit;PT11.base.flameTop=flameSpanTop;
ea11RoundDraw=function(b){
 const role=ea11Role(b);
 if(ea11Element(b)!=='kinetic'||!['round','heavy'].includes(role)||!pt11Ready('sonic_pulse'))return PT11.base.round.apply(this,arguments);
 if(b.dead||b._launchDelay>0)return false;
 const f=Math.floor(projectileVisualAge(b)*24)%16,a=PT11_ART.sonic_pulse[f],size=(role==='heavy'?24:16)+clamp(b.lv||1,1,5)*2;
 ctx.save();ctx.translate(b.x,b.y);ctx.rotate(Math.atan2(b.vy??-1,b.vx||0)+Math.PI/2);
 pt11Plate('sonic_pulse',f,0,size*.5,size/a.length);ctx.restore();return true;
};
function pt11FireGeometry(b){
 if(b?._inf!=='fire'||b.kind!=='flame'||!(b.bot>b.top))return null;
 const f=Math.floor(Math.max(0,b.anim||0)*24)%16,a=PT11_ART.fire_spray[f];
 if(!XART.rdy(a.key))return null;
 const k=(b.bot-b.top)*PLAYER_FLAME_SCALE*1.22/a.length;
 return{f,a,k,x:b.x,y:b.bot,top:b.bot-a.length*k};
}
flameDraw=function(b){const g=pt11FireGeometry(b);if(!g)return PT11.base.flame.apply(this,arguments);
 pt11Plate('fire_spray',g.f,g.x,g.y,g.k);
};
flameSpanTop=function(b){return pt11FireGeometry(b)?.top??PT11.base.flameTop.apply(this,arguments);};
flameHit=function(b,x,y,w,h){const g=pt11FireGeometry(b);if(!g)return PT11.base.flameHit.apply(this,arguments);
 const hw=(w||0)/2,hh=(h||w||0)/2,{a,k}=g;
 return a.hitBands.some(([t,bot,l,r])=>y+hh>g.y+(t-a.pivot[1])*k&&y-hh<g.y+(bot-a.pivot[1])*k&&
  x+hw>g.x+(l-a.pivot[0])*k&&x-hw<g.x+(r-a.pivot[0])*k);
};
sm10EnemyPlate=function(e,a){
 if(run.stage!==3||!['s3mine','s3interceptor'].includes(e.type))return PT11.base.enemyPlate.apply(this,arguments);
 const bank=e.type==='s3mine'?'ice_jet_b':'ice_jet_a',frame=Math.floor((e.t||0)*16)%16;
 if(!pt11Ready(bank))return PT11.base.enemyPlate.apply(this,arguments);
 const k=e.type==='s3mine'?.49:.53;
 pt11Plate(bank,frame,e.x,e.y+15,k,e.spin||0,e.flash);
 e._drawW=174*k;e._drawH=190*k;e._pt11Frame=frame;e._pt11Bank=bank;return true;
};

/* The retired Stage 3 plate now serves as a Stage 8 heavy. It stays in the
   ordinary enemy list, with no miniboss music, route hold or extra boss bar. */
PT11.base.spawn=spawnEnemy;PT11.base.enemyDraw=drawEnemy;PT11.base.enemyHit=hitEnemy;
PT11.base.enemyBegin=ai27Begin;PT11.base.enemyEnd=ai27End;
spawnEnemy=function(type,x,y,opt={}){
 if(run.stage===6&&type==='s6buoy')return null;
 if(type!=='pt11frostcarrier')return PT11.base.spawn.apply(this,arguments);
 const e=PT11.base.spawn('s8interceptor',x,y,opt);if(!e)return e;
 for(const key of ['_s8mega','_alien1003','_orbit1003','_frRealmAI','_dr','_cn','_droid','_furyMove','_esh','_enemyShield','_frFlight','_entrySweep','_eb11'])delete e[key];
 Object.assign(e,{type,pattern:'pt11frostcarrier',_pt11LegacyFrost:true,_ship:'frostcruiser',_noSep:true,_noHit:false,
  _jc:{blasts:[],poseRot:0,mode:'idle'},w:260,h:240,ty:viewTopY()+160,ground:false,shoots:false,fk:null,_atk:'none',vx:0,vy:0,spin:0,score:5200,enter:true});
 er26Init(e);const hp=Math.ceil(350*DIFF.eHp*(coopActive()?1.5:1));e.hp=e.maxhp=e._maxhp=hp;e.name='FROST SIEGE VETERAN';
 for(const p of e._mr27.parts)p.hp=p.maxhp=Math.ceil(hp*(p.id.startsWith('gun')?.15:.10));
 e._er26.home=e.ty;e._pt11Age=0;
 for(const name of FB1002_FROST_NAMES)XART.rdy(FB1002_ART[name].key);
 pt11Log('stage8-frost-heavy-spawn',{hp});return e;
};
function pt11LegacyFrostTick(e,dt){
 e._pt11Age+=dt;e.flash=Math.max(0,(e.flash||0)-dt);
 if(e.enter){e.y=Math.min(e.ty,e.y+95*dt);e._drawY=e.y;if(e.y>=e.ty){e.enter=false;er26Set(e,'recover');}return;}
 // A survivor withdraws after a full attack sequence; it cannot stall the route.
 if(e._pt11Age>35){e._l23Beam=null;groundTargetingCancel(e);e.y+=100*dt;e._drawY=e.y;if(e.y>VH+e.h)e.dead=true;return;}
 er26Tick(e,dt);l23BossBeamTick(e,dt);shipBossMuzzleTick(e,dt);
}
ai27Begin=function(e,dt){return e._pt11LegacyFrost?null:PT11.base.enemyBegin.apply(this,arguments);};
ai27End=function(e,previous){if(!e._pt11LegacyFrost)return PT11.base.enemyEnd.apply(this,arguments);};
drawEnemy=function(e){if(e._pt11LegacyFrost){if(!e.dead&&e._dyingT==null)PT11.base.roster(e);return;}return PT11.base.enemyDraw.apply(this,arguments);};
hitEnemy=function(e,dmg){if(!e._pt11LegacyFrost)return PT11.base.enemyHit.apply(this,arguments);
 if(e.dead||e.enter||e._dyingT!=null)return;
 const q=e._pt11Contact||_dmgBullet||e;delete e._pt11Contact;
 dmg=mr27Damage(e,dmg,q.x,q.y);
 return PT11.base.enemyHit.call(this,e,dmg);
};

/* Cryogenic crossbar carrier: separate socketed cannons and missile magazines.
   A part's local mount, rotated image center, hitbox and muzzle share one transform. */
function pt11Frost(b){return b?._ship==='frostcruiser'&&!b._pt11LegacyFrost;}
er26Init=function(b){const r=PT11.base.init.apply(this,arguments);if(pt11Frost(b)){b.w=300;b.h=280;b.name='CRYOGENIC SIEGE CARRIER';}return r;};
function pt11Part(b,id){
 const side=id.endsWith('L')?-1:1,gun=id.startsWith('gun'),core=id==='core';
 const cell=core?3:gun?(side<0?1:2):(side<0?4:5),a=PT11_ART.ice_parts[cell],part=mr27Part(b,id);
 const k=core?.145:gun?.32:.23,rot=part?.rot||0;
 const x=b.x+(core?0:gun?side*99:side*48),y=(b._drawY??b.y)+(core?0:gun?-6:-54)-(part?.recoil||0)*4;
 const c=Math.cos(rot),s=Math.sin(rot),dx=(a.w/2-a.pivot[0])*k,dy=(a.h/2-a.pivot[1])*k;
 const muzzle=core?[a.pivot[0],a.pivot[1]+20]:gun?(side<0?[166,554]:[102,554]):[a.pivot[0],a.h-12];
 const mx=(muzzle[0]-a.pivot[0])*k,my=(muzzle[1]-a.pivot[1])*k;
 return {id,cell,x:x+dx*c-dy*s,y:y+dx*s+dy*c,w:a.w*k,h:a.h*k,rot,
  pivotX:x,pivotY:y,scale:k,muzzle:{x:x+mx*c-my*s,y:y+mx*s+my*c}};
}
mr27Shape=function(b,id){return pt11Frost(b)?pt11Part(b,id):PT11.base.shape.apply(this,arguments);};
/* The new carrier has no MR27_ART entry. Ordinary rounds must use its actual
   drawn hull/core pixels, not the retired skin lookup that always missed it.
   The offline mask includes the seated reactor; guns retain mr27At priority. */
mr27HullAt=function(b,x,y){
 if(!pt11Frost(b))return PT11.base.hullAt.apply(this,arguments);
 const G=typeof MR27_HULL_MASK!=='undefined'?MR27_HULL_MASK:null,a=PT11_ART.ice_parts[0];
 if(!G?.rows.pt11_frost||!a)return false;
 const k=300/806,u=((x-b.x)/k+a.pivot[0])/a.w,v=((y-(b._drawY??b.y))/k+a.pivot[1])/a.h;
 if(!(u>=0&&u<1&&v>=0&&v<1))return false;
 G.num??={};const rows=G.num.pt11_frost??=(G.rows.pt11_frost.map(h=>parseInt(h,16))),n=G.n;
 return Math.floor(rows[Math.floor(v*n)]/Math.pow(2,n-1-Math.floor(u*n)))%2===1;
};
mr27Mount=function(b,slot){if(!pt11Frost(b))return PT11.base.mount.apply(this,arguments);
 const id=/ROCKET/.test(slot)?(slot.endsWith('L')?'rocketL':'rocketR'):['L','L0','L1','LW','CL','gunL'].includes(slot)?'gunL':['R','R0','R1','RW','CR','gunR'].includes(slot)?'gunR':'core';
 return pt11Part(b,id).muzzle;
};
mr27Cell=function(skin,cell,form){if(skin!=='pt11_frost')return PT11.base.cell.apply(this,arguments);
 const a=PT11_ART.ice_parts[cell];return a&&XART.rdy(a.key)?form==='fire'?xartPalette(a.key,'#df5529'):XART.get(a.key):null;};
mr27Blit=function(skin,cell,p,flash,form,owner){if(skin!=='pt11_frost')return PT11.base.blit.apply(this,arguments);
 const a=PT11_ART.ice_parts[cell];if(!a)return false;
 if(p.pivotX!=null)return pt11Plate('ice_parts',cell,p.pivotX,p.pivotY,p.scale,p.rot,flash,form);
 const k=Math.min(p.w/a.w,p.h/a.h),c=Math.cos(p.rot||0),s=Math.sin(p.rot||0),dx=(a.pivot[0]-a.w/2)*k,dy=(a.pivot[1]-a.h/2)*k;
 return pt11Plate('ice_parts',cell,p.x+dx*c-dy*s,p.y+dx*s+dy*c,k,p.rot,flash,form);
};
mr27Draw=function(b){if(!pt11Frost(b)||!pt11Ready('ice_parts'))return PT11.base.roster.apply(this,arguments);
 mr27Init(b);const M=b._mr27,R=b._er26,form=b._s3Nuclear?R.form:null;M.skin='pt11_frost';
 if(b._l23Beam)l23BossBeamDraw(b);
 pt11Plate('ice_parts',0,b.x,b._drawY??b.y,300/806,0,b.flash,form);
 for(const p of M.parts)if(!p.dead)mr27Blit(M.skin,pt11Part(b,p.id).cell,pt11Part(b,p.id),Math.max(p.flash,b.flash||0),form,b);
 mr27Blit(M.skin,3,pt11Part(b,'core'),b.flash,form,b);er26Draw(b);shipBossMuzzleDraw(b);M.draws++;return true;
};

/* A complete animated skull on the same forehead-eye anchor. The two eye-laser
   collision owners remain untouched; this replaces only the approved head plate. */
fztHeadDraw=function(x,y,charged,a,hpRatio,s){if(!pt11Ready('furnace_head'))return PT11.base.head.apply(this,arguments);
 const t=boss?._fz?.t??AV3.clock,frame=charged>.03?Math.min(15,Math.floor(charged*15)):Math.floor(t*5)%4;
 // Original forehead socket is 3.5 px right / 15.5 px above its image center.
 const k=(s||1)*FZT_S,c=Math.cos(a||0),sn=Math.sin(a||0);
 pt11Plate('furnace_head',frame,x+(3.5*c+15.5*sn)*k,y+(3.5*sn-15.5*c)*k,k*.66,a||0);
};

/* Flame arms release travelling crescents. Core and eye lasers retain their
   continuous beam owners. A crescent's leading edge, not an invisible column,
   owns damage, and every wave keeps its release heading. */
PT11.base.furnaceCombat=furnaceCombat;PT11.base.furnaceBeam=fztBeam;PT11.base.furnaceProjectile=furnaceProjectileDraw;
furnaceCombat=function(b,dt){b._fz._pt11Emitter=0;return PT11.base.furnaceCombat.apply(this,arguments);};
fztBeam=function(F,x,y,a,len,width,kind){
 if(kind!=='flame')return PT11.base.furnaceBeam.apply(this,arguments);
 if(width<=.5)return;const port=F._pt11Emitter++,key=F.serial+':'+port;
 F._pt11Waves??={};if((F._pt11Waves[key]||0)>F.t)return;
 F._pt11Waves[key]=F.t+(diffKey==='furious'?.54:diffKey==='hard'?.66:diffKey==='easy'?.96:.78);
 // Keep at most the current attack's schedule. No wall-clock or draw-rate firing.
 for(const k of Object.keys(F._pt11Waves))if(!k.startsWith(F.serial+':'))delete F._pt11Waves[k];
 const speed=diffKey==='furious'?3.65:diffKey==='hard'?3.3:2.85,k=.64;
 eBullets.push({x,y,vx:-Math.sin(a)*speed,vy:Math.cos(a)*speed,w:112,h:34,ang:a,t:0,
  kind:'pt11FireWave',_fzt:true,_pt11Wave:true,_pt11Scale:k,_weaponProof:true,_shootable:false});
 pt11Log('furnace-wave',{port,serial:F.serial,x,y,angle:a});fztSfx('furnaceFlameRelease');
};
function pt11FireWaveHit(q,p,hx,hy,oldX=q.x,oldY=q.y){
 const c=Math.cos(q.ang),s=Math.sin(q.ang),k=q._pt11Scale;
 const pts=[[-84,-21],[-56,-11],[-28,-3],[0,0],[28,-3],[56,-11],[84,-21]].map(([x,y])=>({x:q.x+(x*c-y*s)*k,y:q.y+(x*s+y*c)*k}));
 const radius=Math.max(hx,hy)*.68+5;
 for(let i=1;i<pts.length;i++){const a=pts[i-1],b=pts[i];if(ec7SegmentBox(a.x,a.y,b.x,b.y,p.x,p.y,radius,radius))return true;}
 for(const a of pts)if(ec7SegmentBox(a.x+oldX-q.x,a.y+oldY-q.y,a.x,a.y,p.x,p.y,radius,radius))return true;
 return false;
}
furnaceProjectileDraw=function(q){if(!q._pt11Wave)return PT11.base.furnaceProjectile.apply(this,arguments);
 return pt11Plate('fire_wave',Math.floor((q.t||0)*20)%16,q.x,q.y,q._pt11Scale,q.ang);};

/* At the final quarter the Sovereign abandons its shield and commits to a
   south exit, northbound pursuit and a finite last barrage. */
stage4ShieldBeginRearm=function(b,threshold){if(b?._ship!=='stormsovereign'||threshold>.251)return PT11.base.rearm.apply(this,arguments);
 const S=b._s4war,H=S.shield;if(S._pt11Chase)return false;
 H.active=H.rearming=false;H.breakT=0;for(const n of H.nodes){n.dead=true;n.hp=0;}
 b._ap10Storm=null;b._l23Beam=null;S.giantStrike=null;S.finalGuns='off';
 S._pt11Chase={t:0,from:{x:b.x,y:b.y},exit:{x:clamp(b.x,camLeftX()+105,camRightX()-105),y:viewTopY()+viewH()+b.h},shot:0,wave:0,done:false};
 b._er26.mode='pt11-chase';b._er26.warnings=[];b._er26.od=true;S.mode='chase';stage4WarfareSound('bossPhase','enemyElectricBolt');
 pt11Log('storm-final-pursuit');return true;
};
stage4ShieldSyncNodes=function(b){const H=b?._s4war?.shield;if(!H)return PT11.base.nodes.apply(this,arguments);
 if(!H._pt11Station&&b._er26?.engaged&&!b.enter)H._pt11Station={x:b.x,y:b._er26.home};
 if(!H._pt11Station)return PT11.base.nodes.apply(this,arguments);
 H.anchorX??=Math.min(VW*.5-36,b.w*.67+36);H.anchorY??=46;H.rowOffset??=78;
 for(const n of H.nodes){n.x=H._pt11Station.x+n.side*H.anchorX;n.y=H._pt11Station.y+H.anchorY+n.row*H.rowOffset;}
};
stage4CoreTurretTarget=function(b,side){const H=b?._s4war?.shield;if(!H?._pt11Station)return PT11.base.target.apply(this,arguments);
 const pair=H.nodes.filter(n=>n.side===side);return {x:clamp(pair.reduce((v,n)=>v+n.x,0)/pair.length,56,worldWidth()-56),y:pair.reduce((v,n)=>v+n.y,0)/pair.length};
};
function pt11ChaseTick(b,dt){const S=b._s4war,Q=S._pt11Chase,R=b._er26;Q.t+=dt;R.warnings=[];
 const ease=p=>{p=clamp(p,0,1);return p*p*(3-2*p);},top=PLAY.y+105,home=camLeftX()+viewW()/2;
 if(Q.t<1.0){const p=Q.t;R.warnings.push({x:b.x,y:b.y+b.h*.35,angle:Math.PI/2,width:b.w*.72,progress:p});combatWarningTick(b,'storm-south-exit',Q.t,1);b._noHit=false;}
 else if(Q.t<2.6){const u=ease((Q.t-1)/1.6);b.x=lerp(Q.from.x,Q.exit.x,u);b.y=lerp(Q.from.y,Q.exit.y,u);b._noHit=b.y>viewTopY()+viewH()+b.h*.35;}
 else if(Q.t<4.5){const u=ease((Q.t-2.6)/1.9);b.x=lerp(Q.exit.x,home,u);b.y=lerp(Q.exit.y,top,u);b._noHit=b.y>viewTopY()+viewH()+b.h*.35;}
 else{b._noHit=false;b.y+=(top-b.y)*Math.min(1,dt*3);b.x+=(home+Math.sin((Q.t-4.5)*.65)*viewW()*.22-b.x)*Math.min(1,dt*2);}
 b._drawY=b.y;
 // Scattered balls come off the visible hull; ordinary pellets remain immune.
 Q.shot-=dt;if(Q.t>3.05&&Q.shot<=0&&b.y<viewTopY()+viewH()+20){const rank=diffKey==='furious'?3:diffKey==='hard'?2:diffKey==='easy'?0:1;
  const count=3+rank*2,offset=Q.wave++*.31;for(let i=0;i<count;i++){const a=Math.PI/2+(i-(count-1)/2)*.22+Math.sin(offset)*.12;
   const p={x:b.x+Math.sin(i*2.4)*b.w*.26,y:b.y+b.h*.23},q=stage4WarfareShot(b,p,a,2.9+rank*.45,'orb',{shootable:true,hp:2,szMul:.65,lift:0});
   q._ap10Lightning=true;q._er26Art='lightning';q._weaponProof=false;q._pt11Chase=true;}
  Q.shot=rank===0?.90:rank===1?.72:rank===2?.59:.48;Audio.SFX.enemyElectricBolt?.();}
 if(!Q.done&&Q.t>=10){Q.done=true;Q.shot=1.2;er26Set(b,'recover');pt11Log('storm-pursuit-complete');}
 return true;
}
er26WarTick=function(b,dt){if(b._s4war?._pt11Chase&&!b._s4war._pt11Chase.done)return pt11ChaseTick(b,dt);return PT11.base.war.apply(this,arguments);};
mr27Over=function(b){const H=b?._s4war?.shield;
 if(H&&(H.active||H.rearming))for(const n of H.nodes)if(!n.dead){const dx=b.x-n.x,dy=b.y-n.y,len=Math.hypot(dx,dy);
  av3Beam(ctx,n.x,n.y,Math.atan2(dy,dx),len,7,'lightning',b._mr27.clock,.65,false);}
 const r=PT11.base.over.apply(this,arguments);
 return r;
};
er26EscortTick=function(b,dt){const r=PT11.base.escort.apply(this,arguments);if(b._ship!=='olivewarden'||diffKey==='easy'||b.dead)return r;
 const R=b._er26;R._pt11EscortCd=(R._pt11EscortCd??7)-dt;if(R._pt11EscortCd>0)return r;
 const limit=diffKey==='furious'?4:diffKey==='hard'?3:2,alive=enemies.filter(e=>e._pt11Escort===b&&!e.dead&&e._dyingT==null).length;
 if(alive<limit){const side=(R._pt11EscortWave||0)%2?1:-1;R._pt11EscortWave=(R._pt11EscortWave||0)+1;
  const e=spawnEnemy('s4interceptor',camLeftX()+viewW()*(side<0?.18:.82),viewTopY()-90,{});if(e)e._pt11Escort=b;}
 R._pt11EscortCd=diffKey==='furious'?4.2:diffKey==='hard'?5.5:8;return r;
};

/* Hammer recovery is brief, visible, on-screen and invulnerable only while
   the electrified get-up is being shown. It never restores any health. */
function pt11HammerGhost(b){return ['fr_stun','hammer_stun','storm_stun','storm_rebuild'].includes(b?._hammer?.state)&&!b.dead;}
hammerBossInit=function(b){const r=PT11.base.hammerInit.apply(this,arguments),h=b._hammer;h.chainHP=h.chainMax=Math.ceil(h.chainMax*1.85);return r;};
hammerBossTick=function(b,dt){const h=b._hammer,ghost=pt11HammerGhost(b);
 if(ghost){const limit=h.state==='hammer_stun'?5:h.state==='fr_stun'||h.state==='storm_stun'?4:2.4,target=h.state==='storm_rebuild'?1.1:1.6;
  h.t+=dt*(limit/target-1);const x=clamp(b.x,camLeftX()+100,camRightX()-100),y=clamp(b.y,PLAY.y+125,PLAY.y+viewH()*.56);
  b.x+=clamp(x-b.x,-280*dt,280*dt);b.y+=clamp(y-b.y,-280*dt,280*dt);}
 const r=PT11.base.hammerTick.apply(this,arguments);
 if(pt11HammerGhost(b)){b._noHit=true;h._pt11Ghost=true;}else if(h._pt11Ghost){h._pt11Ghost=false;b._noHit=false;}
 return r;
};
hammerBossDamage=function(b,dmg){if(pt11HammerGhost(b)){b._hammerModuleHit=null;return 0;}return PT11.base.hammerDamage.apply(this,arguments);};
hammerBossDraw=function(b){const ghost=pt11HammerGhost(b),h=b._hammer;
 if(!b.dead&&!h.hc11Counter&&['hammer','shield','storm_idle'].includes(h.state)&&(!b._hammerTime||b._hammerTime.mode==='attack')&&(!b._hama||b._hama.mode==='attack')&&pt11Ready('hammer_core')){
  pt11Plate('hammer_core',Math.floor(hm10Data(b).age*10)%8,b.x,b.y,HM10.bodyScale,0,b.flash);hm10WallDraw(b);return;}
 ctx.save();if(ghost)ctx.globalAlpha*=.30+.07*Math.sin(b._hammer.t*14);
 try{return PT11.base.hammerDraw.apply(this,arguments);}finally{ctx.restore();}};
archBlit=function(key,f,x,y,h,tint,rot,alpha){const b=HM10.drawing;
 if(b&&!b.dead&&['hammer','shield','leap_reset','storm_idle'].includes(b._hammer.state)&&!b._hammer.hc11Counter&&key==='leap_strike_0922'&&pt11Ready('hammer_core')){
  const frame=Math.floor(hm10Data(b).age*10)%8;return pt11Plate('hammer_core',frame,x,y,HM10.bodyScale,rot||0,b.flash);}
 return PT11.base.arch.apply(this,arguments);
};
repair30ChromiumActivationDraw=function(b){if(!pt11Ready('hammer_core'))return PT11.base.activation.apply(this,arguments);
 const f=8+Math.min(7,Math.floor(clamp(b._hammer.t/FR27_ACT.end,0,.999)*8));
 return pt11Plate('hammer_core',f,b.x,b.y,HM10.bodyScale,0,b.flash);
};
hammerBossModuleBreak=function(b,which){const was=b._hammer.chainDestroyed,r=PT11.base.break.apply(this,arguments);
 if(which==='chaingun'&&!was&&b._hammer.chainDestroyed&&!b._hammer._pt11PartDropped){b._hammer._pt11PartDropped=true;
  powerups.push({kind:'pt11chain',x:clamp(b.x,camLeftX()+36,camRightX()-36),y:clamp(b.y+60,PLAY.y+60,VH-100),t:0,w:38,h:38,vy:.8,bob:0,_fcHold:1});
  PT11.radio={t:0,text:'Bring that back in one piece when you get home. Good luck.'};pt11Log('chaingun-salvage-dropped');}
 return r;
};
applyPowerup=function(p){if(p.kind!=='pt11chain')return PT11.base.pickup.apply(this,arguments);
 const held={weapon:run.weapon,wlevel:run.wlevel};chaingunUnlock();if(spaceWeaponsActive())Object.assign(run,held);
 run.score=(run.score||0)+PICKUP_SCORE;stageStats.pickups++;pickupAnnounce('CHAINGUN SALVAGE ACQUIRED','#d9efff');pt11Log('chaingun-salvage-collected');
};
drawPowerups=function(){const all=powerups,parts=all.filter(p=>p.kind==='pt11chain');powerups=all.filter(p=>p.kind!=='pt11chain');
 try{PT11.base.powerDraw.apply(this,arguments);}finally{powerups=all;}
 for(const p of parts)iconDraw('micon_chaingun_1',p.x,p.y,38,true);
};
updatePlay=function(dt){const r=PT11.base.play.apply(this,arguments);if(PT11.radio&&!BOFCinematicDirector.live){PT11.radio.t+=dt;if(PT11.radio.t>5.5)PT11.radio=null;}return r;};
beginStage=function(){PT11.radio=null;return PT11.base.begin.apply(this,arguments);};
drawWorld=function(dt){const r=PT11.base.world.apply(this,arguments),q=PT11.radio;
 if(q&&run.stage===5&&state===GS.PLAY&&!BOFCinematicDirector.live)dlgBox({who:'DECKER',portrait:'decker',full:q.text,shown:q.text.slice(0,Math.floor(q.t*34)),forceShown:true,
  tint:'#d9e8ff',fade:Math.min(1,q.t*4,(5.5-q.t)*3),pw:VW*.94,ph:VH*.20,x:VW*.03,y:VH*.68,screenSpace:true});return r;
};

/* Harrier: physical cannon pools, sixteen hinge-registered recoil frames and
   room to fly around the airframe. Warp immunity still follows the old clock. */
Object.assign(PT11.base,{harrierTick:chaosHarrierUpdate,harrierPart:chaosHarrierPart,harrierShot:chaosHarrierShot,
 harrierPoint:chaosHarrierPoint,miniHit:hitSubBoss,miniSolid:subBossSolidAt,retina:retinaBossTargets});
function pt11HarrierGuns(b){return b._pt11Guns??=(['left_cannon','right_cannon'].map((id,i)=>({id,side:i?1:-1,hp:Math.ceil(b.maxhp*.16),maxhp:Math.ceil(b.maxhp*.16),dead:false})));}
function pt11HarrierFrame(b,slot){const W=b._chTell,t=b._chT||0;
 if(!W||W.slot&&W.slot!==slot)return Math.floor((b.t||0)*6)%4;
 if(t<W.warm)return 4+Math.min(3,Math.floor(t/W.warm*4));
 if(b._chActiveLaser?.slot===slot||b._chState==='plasma')return 8+Math.floor((t-W.warm)*18)%4;
 return 12+Math.min(3,Math.floor((t-W.warm)*12));
}
function pt11HarrierGunPose(b,p){const m=chaosHarrierGunMount(b,p.side),f=pt11HarrierFrame(b,p.id),rot=m.a,s=m.s;
 const dx=p.side*23*s,dy=85*s;return{x:m.x+dx*Math.cos(rot)-dy*Math.sin(rot),y:m.y+dx*Math.sin(rot)+dy*Math.cos(rot),w:72*s,h:176*s,rot};}
function pt11HarrierGunAt(b,x,y){return pt11HarrierGuns(b).find(p=>{if(p.dead)return false;const q=pt11HarrierGunPose(b,p),dx=x-q.x,dy=y-q.y;
 return Math.abs(dx*Math.cos(q.rot)+dy*Math.sin(q.rot))<q.w/2+5&&Math.abs(-dx*Math.sin(q.rot)+dy*Math.cos(q.rot))<q.h/2+5;});}
function pt11HarrierContact(b,x,y){return b._chCollision&&(((x-b.x)/(b.w*.31))**2+((y-b.y)/(b.h*.43))**2<1||!!pt11HarrierGunAt(b,x,y));}
chaosHarrierPart=function(b,key,x,y,scale,anchor,angle,flip){if(key.startsWith('ch2_gun_')&&pt11Ready('harrier_cannon')){
 const side=flip||1,slot=side<0?'left_cannon':'right_cannon';if(pt11HarrierGuns(b).find(p=>p.id===slot).dead)return true;
 ctx.save();ctx.translate(x,y);ctx.rotate(angle||0);ctx.scale(side,1);
 try{return pt11Plate('harrier_cannon',pt11HarrierFrame(b,slot),0,0,scale,0,b.flash);}finally{ctx.restore();}
 }return PT11.base.harrierPart.apply(this,arguments);};
chaosHarrierPoint=function(b,slot){if(!['left_cannon','right_cannon'].includes(slot))return PT11.base.harrierPoint.apply(this,arguments);
 const m=chaosHarrierGunMount(b,slot==='left_cannon'?-1:1),f=pt11HarrierFrame(b,slot),recoil=f===9?35:f===10||f===11?22:0;
 const dx=23*m.side*m.s,dy=(184-recoil)*m.s;return{x:m.x+dx*Math.cos(m.a)-dy*Math.sin(m.a),y:m.y+dx*Math.sin(m.a)+dy*Math.cos(m.a)};
};
chaosHarrierShot=function(b,family,slot){if(pt11HarrierGuns(b).some(p=>p.id===slot&&p.dead))return;return PT11.base.harrierShot.apply(this,arguments);};
chaosHarrierUpdate=function(b,dt){pt11HarrierGuns(b);
 const deadSlot=pt11HarrierGuns(b).some(p=>p.id===b._chTell?.slot&&p.dead);
 if(deadSlot){b._chActiveLaser=null;chaosHarrierFinish(b);}
 return PT11.base.harrierTick.apply(this,arguments);
};
hitSubBoss=function(dmg,hx,hy){const b=subBoss;if(!b?._harrier)return PT11.base.miniHit.apply(this,arguments);
 if(!b._chCollision||b.dead)return;
 const gun=Number.isFinite(hx+hy)?pt11HarrierGunAt(b,hx,hy):null;
 if(gun){const actual=Math.min(gun.hp,dmg);gun.hp-=actual;
  if(gun.hp<=0){gun.dead=true;const q=pt11HarrierGunPose(b,gun);unitDeathFX({...q},'turret','purple');explode(q.x,q.y,54,'purple');pt11Log('harrier-cannon-destroyed',{id:gun.id});}
 }
 return PT11.base.miniHit.apply(this,arguments);
};
subBossSolidAt=function(x,y){return subBoss?._harrier?pt11HarrierContact(subBoss,x,y):PT11.base.miniSolid.apply(this,arguments);};
retinaBossTargets=function(b){if(!b?._harrier)return PT11.base.retina.apply(this,arguments);
 if(b.dead||!b._chCollision)return[];
 return [...pt11HarrierGuns(b).filter(p=>!p.dead).map(p=>retinaImpactTarget(b,'pt11-'+p.id,'Harrier cannon',()=>({...pt11HarrierGunPose(b,p),hp:p.hp,dead:p.dead||b.dead||!b._chCollision}),28,68)),
  retinaImpactTarget(b,'pt11-harrier-core','Harrier core',()=>({x:b.x,y:b.y,hp:b.hp,dead:b.dead||!b._chCollision}),92,140)];
};
