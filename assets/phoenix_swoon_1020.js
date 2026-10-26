"use strict";
/* Whole wings / claws / body own their pixels. Detachable added cannon pods
   give way to four-corner Eagle Swoon, never the Furnace's fire rotor. */
const PH21={base:{enter:v18Enter,tick:v19NativeTick,rig:v19VolcanoRig,draw:v19DonorDraw,hit:modularHit,targets:retinaBossTargets,contact:target17BossContact,keys:v18Keys,warm:v18Warm,clear:v18Clear,load:stageLoadBegin},serial:0};
b20Register(PH21_ART);
function ph21Own(b){return v19Native(b)&&b._r30.v18.form===2;}
function ph21State(b){return j3State(b).ph21;}
function ph21Part(b,id){return ph21State(b)?.parts.find(p=>p.id===id);}
function ph21Alive(b,id){return !!ph21Part(b,id)&&!ph21Part(b,id).destroyed;}
function ph21Init(b){const J=j3State(b);let Q=J.ph21;if(!Q){const max=J.max[2],pods=Math.round(max*.18);Q=J.ph21={parts:[b20Part(b,'core',J.hp[2],'Furnace heart / body'),b20Part(b,'head',Math.round(max*.12),'Phoenix skull'),...['L','R'].flatMap(s=>[b20Part(b,'wing'+s,Math.round(max*.12),'Complete fire wing '+s),b20Part(b,'claw'+s,Math.round(max*.08),'Complete leg and talon '+s),b20Part(b,'cannon'+s,pods,'Detachable heavy cannon '+s)])],stage:'cannons',age:0,cycle:0,scale:1,angle:0,wing:0,claws:0,action:null,serial:0};}
 b.parts=Q.parts;b.hp=J.hp[2];b.maxhp=J.max[2];ph21Part(b,'core').hp=b.hp;J.modules[2]=b.parts;Q.stage=ph21Alive(b,'cannonL')||ph21Alive(b,'cannonR')?'cannons':'swoon';Q.action=null;Q.scale=1;Q.angle=0;Q.age=0;Q.cool=.9;b.name='CORRUPTED FIRE PHOENIX';b._r30.v18.swipe=null;b._r30.v18.nextClawAt=Infinity;return Q;}
v18Enter=function(b){const result=PH21.base.enter.apply(this,arguments);if(ph21Own(b))ph21Init(b);return result;};
v18Keys=function(){return [...PH21.base.keys(),...b20Keys(PH21_ART)];};
v18Warm=function(){const before=PH21.base.warm();return b20Ready(PH21_ART)&&before;};
stageLoadBegin=function(n,keys){return PH21.base.load.call(this,n,[...(keys||[]),...(n===8?b20Keys(PH21_ART):[])]);};
v18Clear=function(b){if(ph21Own(b)&&ph21State(b)){ph21State(b).action=null;for(const q of eBullets)if(q._ph21Owner===b)q.dead=true;}return PH21.base.clear.apply(this,arguments);};
function ph21Root(b,at){const Q=ph21State(b),k=v18Size(b)/320*Q.scale,c=Math.cos(Q.angle),s=Math.sin(Q.angle),x=(at[0]-160)*k,y=(at[1]-160)*k;return{x:b.x+x*c-y*s,y:b.y+x*s+y*c};}
v19VolcanoRig=function(b){if(!ph21Own(b)||!ph21State(b))return PH21.base.rig.apply(this,arguments);const Q=ph21State(b),k=v18Size(b)/320*Q.scale,out=[],wing={};
 const add=(id,a,at,rot=Q.angle,K=k,z=1)=>{const p=ph21Part(b,id);if(!p||p.destroyed)return null;const v=b20Piece(p,a,at,rot,K,id,z);out.push(v);return v;};
 add('core',PH21_ART.parts.core,ph21Root(b,PH21_ART.parts.core.anchor),Q.angle,k,2);
 add('core',PH21_ART.parts.tail,ph21Root(b,PH21_ART.parts.tail.anchor),Q.angle+Math.sin(Q.age*5)*.045,k,0);
 for(const side of ['L','R']){const sign=side==='L'?-1:1,id='wing'+side,a=PH21_ART.parts[id];wing[side]=add(id,a,ph21Root(b,a.anchor),Q.angle+sign*(Q.wing+Math.sin(Q.age*3.2)*.045),k,1);
  const claw='claw'+side,ca=PH21_ART.parts[claw];add(claw,ca,ph21Root(b,ca.anchor),Q.angle-sign*Q.claws*.48,k*(1+Q.claws*.08),3);
  const pod=PH21_ART.cannon,idp='cannon'+side;if(pod&&ph21Alive(b,idp)){const source=[(side==='L'?77:179)+32,107+32],at=wing[side]?v19WorldPoint(wing[side],source):ph21Root(b,source),rot=Q.podRot?.[idp]||0;add(idp,pod,at,rot,k*.64,5);}
 }
 add('head',PH21_ART.parts.head,ph21Root(b,PH21_ART.parts.head.anchor),Q.angle,k,4);return out;};
function ph21TalonPoint(v){return v19WorldPoint(v,[v.layer==='clawL'?135:185,218]);}
function ph21Muzzle(b,id,barrel=0){const v=v19VolcanoRig(b).find(v=>v.layer===id);return v?v19WorldPoint(v,[(barrel%2?81:47),108]):null;}
function ph21Set(b,mode,extra={}){const Q=ph21State(b);Q.action={mode,t:0,serial:++Q.serial,hit:new Set(),...extra};if(['volley','fan','lance'].includes(mode))b20Cue(mode==='lance'?'furnaceLaserCharge':'bossWeaponCharge');b20Log('phoenix-'+mode,{serial:Q.serial,...extra});return Q.action;}
function ph21Corner(b){const Q=ph21State(b),choices=[0,1,2,3].filter(i=>i!==Q.lastCorner),corner=choices[Math.floor(Math.random()*choices.length)];Q.lastCorner=corner;const l=camLeftX(),r=camRightX(),top=viewTopY(),bottom=top+viewH(),m=100,z=viewZoom(),points=[{x:l-m,y:top-m},{x:r+m,y:top-m},{x:l-m,y:bottom+m},{x:r+m,y:bottom+m}],from=points[corner],to=points[3-corner],sign={x:to.x>from.x?1:-1,y:to.y>from.y?1:-1};return{corner,from,to,marker:{x:corner%2?r-34/z:l+34/z,y:corner<2?top+104/z:bottom-110/z},a:Math.atan2(sign.y,sign.x)};}
function ph21Shot(b,id,a,speed,barrel){const at=ph21Muzzle(b,id,barrel);if(!at)return;const q=eShootT(at.x,at.y,a,speed,'mg',{w:10,h:14});if(q){q._fzt=true;q._ph20Feather=true;q._ph21Owner=b;q._ph21Module=id;}b20Cue('enemyBossCannon');}
v19NativeTick=function(b,dt){if(!ph21Own(b)||!ph21State(b))return PH21.base.tick.apply(this,arguments);const Q=ph21State(b),rank=b20Rank(),N=b._r30.v18;Q.age+=dt;N.donorAge=(N.donorAge||0)+dt;b._noHit=false;Q.cool=Math.max(0,(Q.cool||0)-dt);
 if(Q.stage==='cannons'&&!ph21Alive(b,'cannonL')&&!ph21Alive(b,'cannonR')){Q.stage='swoon';Q.action=null;Q.cool=.4;b20Log('phoenix-cannons-destroyed');}
 if(!Q.action&&Q.cool<=0){if(Q.stage==='cannons')ph21Set(b,['volley','fan','lance'][Q.cycle++%3],{target:b20Target(b),tell:[1.4,1.2,1.05,.9][rank],next:0,round:0});else ph21Set(b,'recede',{from:{x:b.x,y:b.y}});}
 const A=Q.action;if(A){A.t+=dt;
  if(['volley','fan','lance'].includes(A.mode)){const u=A.t-A.tell;Q.scale=1;Q.angle=0;Q.wing=-.06*Math.min(1,A.t/A.tell);Q.claws=0;combatWarningTick(b,'ph21-'+A.serial,Math.min(A.t,A.tell),A.tell);
   if(u>=0&&u>=A.next&&u<1.45&&A.mode!=='lance'){A.next=u+[.36,.30,.25,.22][rank];for(const id of ['cannonL','cannonR'])if(ph21Alive(b,id)){const at=ph21Muzzle(b,id,A.round),aim=Math.atan2(A.target.y-at.y,A.target.x-at.x),offsets=A.mode==='fan'?[-.15,0,.15]:[0];for(const off of offsets)ph21Shot(b,id,aim+off,2.7+rank*.3,A.round);}A.round++;}
   if(A.mode==='lance'&&u>=0&&u<1.1){if(!A.released){A.released=true;b20Cue('furnaceLaserBurst');}for(const id of ['cannonL','cannonR'])if(ph21Alive(b,id)){const at=ph21Muzzle(b,id),angle=Math.atan2(A.target.y-at.y,A.target.x-at.x),to={x:at.x+Math.cos(angle)*1000,y:at.y+Math.sin(angle)*1000};b20HitSegment(b,at,to,16,'phoenix cannon laser',A.hit);}}
   if(u>1.65){Q.action=null;Q.cool=[.9,.7,.55,.4][rank];j3Save(b);}
  }else if(A.mode==='recede'){const u=clamp(A.t/.85,0,1);Q.scale=lerp(1,.24,u);Q.wing=.5*u;Q.angle=0;b._noHit=u>.45;b.y=lerp(A.from.y,viewTopY()-140,u);if(u>=1){Q.remaining=Math.max(1,[2,3,3,4][rank]-(!ph21Alive(b,'wingL')||!ph21Alive(b,'wingR')?1:0));ph21Set(b,'corner',{...ph21Corner(b),tell:[1.30,1.10,.95,.82][rank]});}}
  else if(A.mode==='corner'){b.x=A.from.x;b.y=A.from.y;b._noHit=true;Q.scale=.28;Q.angle=A.a+Math.PI/2;combatWarningTick(b,'ph21-corner-'+A.serial,Math.min(A.t,A.tell),A.tell);if(A.t>=A.tell){b20Cue('hammerLeap');ph21Set(b,'dive',{from:A.from,to:A.to,a:A.a,corner:A.corner,duration:[.65,.56,.49,.43][rank]+(!ph21Alive(b,'wingL')||!ph21Alive(b,'wingR')?.09:0)});}}
  else if(A.mode==='dive'){const before={x:b.x,y:b.y},u=clamp(A.t/A.duration,0,1);b.x=lerp(A.from.x,A.to.x,u);b.y=lerp(A.from.y,A.to.y,u);Q.scale=.58+Math.sin(u*Math.PI)*.62;Q.angle=A.a+Math.PI/2;Q.wing=-.6*Math.sin(u*Math.PI);Q.claws=Math.sin(u*Math.PI);b._noHit=u<.10||u>.90;const feet=v19VolcanoRig(b).filter(v=>v.layer==='clawL'||v.layer==='clawR');A.feet??={};for(const v of feet){const at=ph21TalonPoint(v),last=A.feet[v.layer]||at;if(!b._noHit)b20HitSegment(b,last,at,27,'phoenix diagonal talon swoon',A.hit);A.feet[v.layer]=at;}if(!feet.length&&!b._noHit)b20HitSegment(b,before,b,31,'phoenix diagonal body swoon',A.hit);
   if(u>=1){Q.remaining--;if(Q.remaining>0)ph21Set(b,'corner',{...ph21Corner(b),tell:[1.15,.98,.85,.74][rank]});else ph21Set(b,'return',{from:{x:b.x,y:b.y}});}}
  else if(A.mode==='return'){const u=v19Ease(A.t/.9);b.x=lerp(A.from.x,worldWidth()/2,u);b.y=lerp(A.from.y,viewTopY()+viewH()*.36,u);Q.scale=lerp(.38,1,u);Q.angle*=Math.exp(-dt*10);Q.wing=-.15;Q.claws=0;b._noHit=u<.65;if(u>=1){Q.action=null;Q.cool=[1.15,.95,.8,.65][rank];}}
 }
 if(!A){Q.scale=1;Q.angle=0;Q.wing=0;Q.claws=0;}
 Q.podRot??={cannonL:0,cannonR:0};for(const v of v19VolcanoRig(b))if(v.layer.startsWith('cannon')){const target=Q.action?.target||{x:b.x,y:b.y+600},wish=Math.atan2(target.y-v.ay,target.x-v.ax)-Math.PI/2;Q.podRot[v.layer]+=fztWrap(wish-Q.podRot[v.layer])*Math.min(1,dt*9);}
 b._drawY=b.y;ph21Part(b,'core').hp=b.hp;j3Save(b);if(N.donorAge>46&&!Q.action&&j3State(b).hp[0]>0)j3Morph(b,'home');
};
function ph21Vulnerable(b,p){const Q=ph21State(b);return !p.destroyed&&!b._noHit&&(Q.stage==='swoon'||p.id.startsWith('cannon'));}
modularHit=function(dmg){const b=boss;if(!ph21Own(b)||!ph21State(b))return PH21.base.hit.apply(this,arguments);if(!r30Live(b)||b._noHit||!(dmg>0))return;const p=b.parts.includes(b._lastPart)?b._lastPart:ph21Part(b,'core');markHit(b,.12);markHit(p,.12);if(!ph21Vulnerable(b,p))return;
 const damage=Math.min(b.hp,dmg,p.id==='core'?b.hp:p.hp);b.hp-=damage;p.hp=p.id==='core'?b.hp:Math.max(0,p.hp-damage);stageStats.dmgDealt+=damage;ph21Part(b,'core').hp=b.hp;
 if(p.id!=='core'&&p.hp<=0&&!p.destroyed){v19Rupture(b,p);p.destroyed=true;b20Cue('shieldBreakCombat');b20Log('phoenix-module-break',{id:p.id});}
 if(!ph21Alive(b,'cannonL')&&!ph21Alive(b,'cannonR')&&ph21State(b).stage==='cannons'){const Q=ph21State(b);Q.stage='swoon';Q.action=null;Q.cool=.3;b20Log('phoenix-cannons-destroyed');}
 j3Save(b);if(b.hp<=0)r30Break(b);
};
retinaBossTargets=function(b){if(!ph21Own(b)||!ph21State(b))return PH21.base.targets.apply(this,arguments);if(!r30Live(b)||b._noHit)return[];return b.parts.filter(p=>ph21Vulnerable(b,p)).map(p=>retinaDynamicPiece(b,'ph21-'+p.id,p.spec.label,()=>{const v=v19VolcanoRig(b).find(v=>v.p===p);return{x:v?.x||b.x,y:v?.y||b.y,hp:p.hp,dead:!ph21Own(b)||p.destroyed||!v||!ph21Vulnerable(b,p)};},d=>{b._lastPart=p;hitBoss(d);},42,48));};
target17BossContact=function(b){if(ph21Own(b))return false;return PH21.base.contact.apply(this,arguments);};
v19DonorDraw=function(b){if(!ph21Own(b)||!ph21State(b))return PH21.base.draw.apply(this,arguments);const Q=ph21State(b),A=Q.action;for(const v of v19VolcanoRig(b).sort((a,b)=>a.z-b.z))v19Paint(v,b);if(!A)return;
 if(['volley','fan','lance'].includes(A.mode))for(const id of ['cannonL','cannonR'])if(ph21Alive(b,id)){const at=ph21Muzzle(b,id,A.round),angle=Math.atan2(A.target.y-at.y,A.target.x-at.x);if(A.t<A.tell){b20Field(b,at,A.target,A.mode==='fan'?110:28,A.t/A.tell);if(A.mode==='lance')b20SizedEffect(DR21_ART.banks.ball,Q.age,at.x,at.y,12+20*A.t/A.tell,Q.age*TAU);}else{const u=A.t-A.tell;if(A.mode==='lance'&&u<1.1)fztBeamDraw({_ph20:true,_ph20Time:Q.age,x:at.x,y:at.y,a:angle-Math.PI/2,len:1000,width:16});if(u<1.4)b20Effect(PH20_ART.plume.frames,Q.age,at.x,at.y,48,angle-Math.PI/2);}}
 if(A.mode==='corner'){b20Field(b,A.from,A.to,160,A.t/A.tell);const a=PH21_ART.warning;if(a){const phase=Math.floor(A.t*9)%2;ctx.save();ctx.globalAlpha=phase?.95:.65;b20Image(a,A.marker.x,A.marker.y,.9,A.a-Math.PI/4);ctx.restore();}}
};
globalThis.BOF_PHOENIX_SWOON={state:PH21,rig:v19VolcanoRig};
