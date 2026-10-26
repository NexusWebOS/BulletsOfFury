'use strict';
/* Red rage adds alternating palm barrages at both depths; every third attack
   retains the existing two-handed red/white wave. No hammer returns. */
const C32={base:{tick:hammerBossTick,draw:hammerBossDraw,pose:ha21Blue,retreat:c30Retreat,laser:hammerLaserDraw,update:updatePlay,load:stageLoadBegin},events:[],cache:new Map()};
for(const s of Object.values(C32_ART.sheets))XART._src[s.key]=s.path;
for(const rows of Object.values(C32_ART.banks))for(const a of rows)BOFX.cells[a.key]=[a.sheet,...a.cell];
function c32Warm(){return [...Object.values(C32_ART.sheets).map(s=>s.key),'eglaser_0'].map(k=>XART.rdy(k)).every(Boolean);}
stageLoadBegin=function(n,keys){if(n===5)Snd.prepare(['enemyPulseLaserAlien','shadowCharge']);return C32.base.load.call(this,n,[...(keys||[]),...(n===5?[...Object.values(C32_ART.sheets).map(s=>s.key),'eglaser_0']:[])]);};
function c32Own(b){return c30Own(b)&&b._hammer.c30?.phase.startsWith('volley_');}
function c32Log(type,data={}){C32.events.push({type,time:efxClock,...data});if(C32.events.length>400)C32.events.shift();}
function c32Pose(b){const R=b._hammer.c30,V=R.volley,rows=C32_ART.banks.palms;let f=C32_ART.guardFrame||0;
 if(R.phase==='volley_fire'){f=V.pose||0;if(C32_ART.interpolated&&!V.dual){const u=clamp((R.t-(V.shotAt||0))/(hammerFurious()?.13:.16),0,1);f=Math.round(V.lastSide===0?u*8:(1-u)*8);}}
 const a=rows[f%rows.length];return{a,k:R.scale,rot:0,kind:'c32_palms'};}
ha21Blue=function(b){return c32Own(b)?c32Pose(b):C32.base.pose.apply(this,arguments);};
function c32Hands(b){const q=c32Pose(b);return q.a.palms.map(p=>hb20World(q.a,p,b,q.k,0));}
c30Retreat=function(b){const R=b._hammer.c30||(b._hammer.c30={scale:1,cycle:0}),kind=R.cycle%3;
 if(kind===2){R.volley=null;return C32.base.retreat.apply(this,arguments);}
 R.volley={depth:kind===0?'foreground':'background',group:0,beat:0,pose:0,flash:[0,0],angles:[Math.PI/2,Math.PI/2]};
 R.from={x:b.x,y:b.y,scale:R.scale};R.to={x:lerp(camLeftX(),camRightX(),kind===0?.5:(R.cycle%2?.73:.27)),y:viewTopY()+(kind===0?190:135),scale:kind===0?1.08:.42};
 c30Phase(b,'volley_move');c32Log('move',{depth:R.volley.depth,from:R.from,to:R.to});
};
function c32Warn(b){const R=b._hammer.c30,V=R.volley,p=targetShip(b.x,b.y);V.target={x:p.x,y:Math.max(p.y,b.y+200)};V.beat=0;V.pose=0;V.flash=[0,0];c30Phase(b,'volley_warn');b20Cue('shadowCharge');c32Log('warning',{depth:V.depth,group:V.group,target:V.target});}
function c32Shot(b){const R=b._hammer.c30,V=R.volley,beat=V.beat,dual=beat===2||beat===5,side=beat%2;
 V.pose=dual?C32_ART.dualFrame:(side===0?C32_ART.leftFrame:C32_ART.rightFrame);V.shotAt=R.t;V.lastSide=side;V.dual=dual;const hands=c32Hands(b),slots=dual?[0,1]:[side],offset=[-36,0,36,36,0,-36][beat];
 for(let i=0;i<slots.length;i++){const hand=slots[i],p=hands[hand],a=Math.atan2(V.target.y-p.y,V.target.x+offset-p.x),before=eBullets.length;
  hammerLaser(p.x,p.y,a,hammerFurious()?7.4:hammerHard()?6.7:6.0,i>0);
  for(const q of eBullets.slice(before)){q._c32Palm=true;q._c32Depth=V.depth;q._c32Start={x:p.x,y:p.y};q._c32Scale=R.scale;q._c32Owner=b;q.w=10;q.h=54;q._ph=beat;q._weaponProof=true;}
  V.flash[hand]=.10;V.angles[hand]=a;c32Log('palm-shot',{depth:V.depth,group:V.group,beat,hand,pose:V.pose,x:p.x,y:p.y,angle:a});
 }V.beat++;}
hammerBossTick=function(b,dt){if(!c32Own(b))return C32.base.tick.apply(this,arguments);const h=b._hammer,R=h.c30,V=R.volley;c30BudgetTick(b,dt);R.t+=dt;h.t=R.t;b._noHit=false;
 V.flash=V.flash.map(t=>Math.max(0,t-dt));
 if(R.phase==='volley_move'){const done=c35DepthFlight(b,R,R.to.scale);if(done){R.scale=R.to.scale;c32Warn(b);}}
 else if(R.phase==='volley_warn'){if(R.t>=(V.group?.58:.85)){c30Phase(b,'volley_fire');V.beat=0;c32Shot(b);}}
 else if(R.phase==='volley_fire'){const interval=hammerFurious()?.13:.16;if(V.beat<6&&R.t>=V.beat*interval)c32Shot(b);if(R.t>=6*interval+.18){V.group++;if(V.group<3)c32Warn(b);else c30Phase(b,'volley_recover');}}
 else if(R.phase==='volley_recover'&&R.t>=.55){R.cycle++;c30Retreat(b);}
 b._drawY=b.y;
};
function c32Lane(b,hand){const V=b._hammer.c30.volley,p=c32Hands(b)[hand],dy=Math.max(80,V.target.y-p.y),ratio=(PLAY.y+PLAY.h+40-p.y)/dy;return{from:p,to:{x:p.x+(V.target.x-p.x)*ratio,y:PLAY.y+PLAY.h+40},width:Math.max(112,90*ratio)};}
hammerBossDraw=function(b){if(!c32Own(b))return C32.base.draw.apply(this,arguments);const R=b._hammer.c30,V=R.volley;hammerBossAtmosphereDraw(b);ha21Body(b,c32Pose(b));
 if(R.phase==='volley_warn')for(let i=0;i<2;i++){const L=c32Lane(b,i);C25.base.warning(b,{x:L.from.x,y:L.from.y,ex:L.to.x,ey:L.to.y,width:L.width,progress:clamp(R.t/(V.group?.58:.85),0,1),fieldOnly:true});}
 const hands=c32Hands(b);for(let i=0;i<2;i++)if(V.flash[i]>0)wm26Draw(ctx,'laser',hands[i].x,hands[i].y,V.angles[i],1-V.flash[i]/.10,36*R.scale,'#ff475e');
 C32.lastDraw={depth:V.depth,scale:R.scale,pose:c32Pose(b).a.key,hands,phase:R.phase};
};
hammerLaserDraw=function(q){if(!q._c32Palm)return C32.base.laser.apply(this,arguments);if(!XART.rdy('eglaser_0'))return;
 if(!C32.cache.has('red-laser'))C32.cache.set('red-laser',C31Texture.trim(C31Texture.palette(XART.get('eglaser_0'),'red')));
 const im=C32.cache.get('red-laser');ctx.save();ctx.translate(q.x,q.y);ctx.rotate(Math.atan2(q.vy,q.vx)-Math.PI/2);ctx.imageSmoothingEnabled=false;ctx.drawImage(im,-q.w/2,-q.h/2,q.w,q.h);ctx.restore();};
updatePlay=function(dt){for(const q of eBullets)if(q._c32Palm){const progress=clamp(Math.hypot(q.x-q._c32Start.x,q.y-q._c32Start.y)/280,0,1),k=q._c32Depth==='background'?lerp(.6,1,progress):1;q.w=10*k;q.h=54*k;}return C32.base.update.apply(this,arguments);};
window.BOF_CHRONOS_VOLLEY=C32;c32Warm();
