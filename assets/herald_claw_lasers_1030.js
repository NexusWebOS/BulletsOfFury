'use strict';
/* Herald's shared claw-targeting attack: source-authored red dual laser rounds. */
const HL67={base:{emit:target17Emit,tell:hd1003Tell,projectile:drawCombatFinalProjectile,draw:heraldDeathDraw,load:stageLoadBegin},events:[],flashes:[],draws:0};
const HL67_ART={projectile:{key:'hl67_laser',cw:64,ch:64,cols:32,frames:512,fps:16},muzzle:{key:'hl67_muzzle',cw:64,ch:64,cols:32,frames:512,fps:40}};
for(const[k,a]of Object.entries(HL67_ART))XART._src[a.key]='assets/game/levels/stage_08/miniboss/herald_claw_lasers_1030/'+k+'.png';
function hl67Own(b){return run.stage===8&&b===subBoss&&!!b?._hd1003&&!b.dead;}
hd1003Tell=function(b){const T=b?._target17;
 // Complete an already-committed claw volley before the next flight/spell.
 // No extra attack, shortened tell or simultaneous special is introduced.
 if(hl67Own(b)&&b._hd1003.mode==='rest'&&hb25Claws(b).length&&T&&['track','fire'].includes(T.phase))return;
 return HL67.base.tell.apply(this,arguments);};
stageLoadBegin=function(n,keys){return HL67.base.load.call(this,n,n===8?[...(keys||[]),...Object.values(HL67_ART).map(a=>a.key)]:keys);};
function hl67Blit(name,phase,angle,x,y){const a=HL67_ART[name];if(!XART.rdy(a.key))return false;
 const dir=((Math.round((angle-Math.PI/2)*64/TAU)%64)+64)%64,f=((phase|0)%8)*64+dir;
 ctx.drawImage(XART.get(a.key),f%32*64,Math.floor(f/32)*64,64,64,Math.round(x)-32,Math.round(y)-32,64,64);HL67.draws++;return true;}
target17Emit=function(b,T,port,rocket){if(!hl67Own(b)||!['gunL','gunR'].includes(port.id))return HL67.base.emit.apply(this,arguments);
 const part=hd1003Part(b,port.id),p=port.pos();if(!p||!hd1003Live(b,part))return;
 const angle=Math.atan2(T.aim.y-p.y,T.aim.x-p.x),q=eShootT(p.x,p.y,angle,3.1+target17Rank()*.15,'s9needle',{owner:b,w:10,h:28,silent:true,noMuzzle:true});
 if(!q||q.dead)return;
 Object.assign(q,{_hl67:true,_hl67Born:efxClock,_target17Owner:b,_target17Port:port.id,_target17Element:T.kind,_target17Age:0,
  _heraldOwner1003:b,_heraldPart1003:port.id,_noArsenal:true,homing:false,_committed:true,_shootable:false,_weaponProof:true});
 delete q.hp;part.kick=3;
 HL67.flashes.push({b,id:port.id,angle,at:efxClock});if(HL67.flashes.length>12)HL67.flashes.shift();
 // One native launcher cue per synchronized pair, including a lone surviving claw.
 if(port.id===target17Ports(b,T.kind)[0]?.id)(Audio.SFX.enemyHeavyLaser||Audio.SFX.enemyMachineGunHeavy)?.();
 T.shots++;target17Log('weapon-shot',{kind:T.kind,port:port.id,x:p.x,y:p.y,rocket:false,serial:T.serial});
 HL67.events.push({event:'claw-laser',time:efxClock,port:port.id,serial:T.serial,wave:T.waves,x:p.x,y:p.y,angle});if(HL67.events.length>240)HL67.events.shift();
};
drawCombatFinalProjectile=function(q){if(q?._hl67)return hl67Blit('projectile',Math.floor(Math.max(0,efxClock-q._hl67Born)*16),Math.atan2(q.vy,q.vx),q.x,q.y);return HL67.base.projectile.apply(this,arguments);};
heraldDeathDraw=function(b){const r=HL67.base.draw.apply(this,arguments);
 HL67.flashes=HL67.flashes.filter(f=>hl67Own(f.b)&&hd1003Live(f.b,hd1003Part(f.b,f.id))&&efxClock-f.at<.20);
 for(const f of HL67.flashes)if(f.b===b){const p=hd1003Muzzle(b,f.id),x=p.x-Math.cos(f.angle)*7,y=p.y-Math.sin(f.angle)*7;
  hl67Blit('muzzle',Math.min(7,Math.floor((efxClock-f.at)*40)),f.angle,x,y);}
 return r;
};
globalThis.BOF_HERALD_CLAW_LASERS_1030=HL67;
