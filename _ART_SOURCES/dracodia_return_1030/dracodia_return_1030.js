'use strict';
/* RD76: defeated copies return to the main arena; only non-final returns repair limbs.
   Copy pools/main HP never refill. Fixed authored blits and scan clipping only. */
const RD76={base:{morph:j3Morph,tick:r30Tick,draw:r30DrawBoss,world:drawWorld,keys:v18Keys,warm:v18Warm,load:stageLoadBegin},events:[],draws:0};
for(const a of Object.values(RD76_ART.banks))XART._src[a.key]=a.path;
function rd76Keys(){return Object.values(RD76_ART.banks).map(a=>a.key);}
v18Keys=function(){return [...RD76.base.keys(),...rd76Keys()];};
v18Warm=function(){const prior=RD76.base.warm();return rd76Keys().map(k=>XART.rdy(k)).every(Boolean)&&prior;};
stageLoadBegin=function(n,keys){return RD76.base.load.call(this,n,n===8?[...(keys||[]),...rd76Keys()]:keys);};
function rd76Log(b,event,data={}){RD76.events.push({event,clock:b._r30.clock,...data});if(RD76.events.length>200)RD76.events.shift();}
function rd76State(b){return b?._r30?.v18?.rd76Return;}
function rd76Start(b){const N=b._r30.v18,J=j3State(b);if(N.rd76Return)return;
 const from=N.form,remaining=rd30Copies(b),last=remaining.length===0;
 // The native main-life guard reserves this pool until every copy is defeated.
 // Repair only anatomy. Never replace/refill J.hp or resurrect a defeated pool.
 v18Clear(b);rd30State(b).transition=null;
 const T=N.rd76Return={from,last,remaining:remaining.slice(),switched:false,t:0,
  hp:J.hp.slice(),seats:seatList().map(seat=>withSeat(seat,()=>({seat,x:player.x,y:player.y}))),
  home:{x:worldWidth()/2,y:viewTopY()+viewH()*.40}};
 dr5Ships(b);dr5State(b).radio=null;groundTargetingReset();
 v18SetMode(b,'v18returnDownload');r30Sound('teleportIn');
 rd76Log(b,'return-start',{from,last,remaining,mainHP:J.hp[0]});return T;
}
j3Morph=function(b,to){if(v18Owned(b)&&j3State(b).encounter===2&&to==='home'&&b._r30.v18.form!==0&&j3State(b).hp[b._r30.v18.form]<=0&&j3State(b).hp[0]>0)return rd76Start(b);
 return RD76.base.morph.apply(this,arguments);};
function rd76Build(b,T){const J=j3State(b),N=b._r30.v18;let old=J.modules[0];
 if(!T.last){
  // Native IDs, fresh transient state; restore severed arms without healing life HP.
  if(!old?.length||!['core','left','right'].every(id=>old.some(p=>p.id===id))){const saved=b.parts;v18PartsBuild(b,J.hp[0]);old=b.parts;b.parts=saved;}
  J.modules[0]=old.map(p=>({...p,hp:p.id==='core'?J.hp[0]:p.maxhp,destroyed:false,flash:0,kick:0,_rd30Shattered:false,_rd77Broken:false}));
 }
 v18Enter(b,2,0);N.rd76Return=T;N.arenaPhase=2;N.arenaCurrent='void';N.arenaDownload=null;
 b.x=T.home.x;b.y=b.ty=T.home.y;N.home={...T.home};b._lastPart=null;b.enter=b._noHit=true;
 // v18Enter owns identity/health but resets the state timer; retain this transfer clock.
 b._r30.mode='v18returnDownload';b._r30.t=T.t;T.switched=true;
 rd76Log(b,'arena-restored',{from:T.from,last:T.last,hp:b.hp,parts:b.parts.map(p=>({id:p.id,hp:p.hp,destroyed:p.destroyed})),pools:J.hp.slice()});
}
r30Tick=function(b,dt){const T=rd76State(b);if(!T||b._r30.mode!=='v18returnDownload')return RD76.base.tick.apply(this,arguments);
 dt=clamp(dt||0,0,.05);dr5Protect(b,dt);T.t+=dt;b._r30.t=T.t;b.enter=b._noHit=true;
 for(const q of T.seats)withSeat(q.seat,()=>{if(!player.dead){player.x=q.x;player.y=q.y;}});
 if(T.t>=.85&&!T.switched)rd76Build(b,T);
 if(T.t>=1.6&&!T.buildCue){T.buildCue=true;Snd.play('combatEnergy0927',.8);}
 if(T.t>=4.2){const N=b._r30.v18;N.rd76Return=null;dr5State(b).ships=[];v18Fight(b);N.home={x:b.x,y:b.y};rd76Log(b,'return-complete',{last:T.last,hp:b.hp,pools:j3State(b).hp.slice()});}
};
function rd76Blit(name,f,x,y){const a=RD76_ART.banks[name];if(!a||!XART.rdy(a.key))return;ctx.drawImage(XART.get(a.key),f%a.cols*a.w,Math.floor(f/a.cols)*a.h,a.w,a.h,Math.round(x-a.pivot[0]),Math.round(y-a.pivot[1]),a.w,a.h);RD76.draws++;}
r30DrawBoss=function(b){const T=rd76State(b);if(!T||b._r30.mode!=='v18returnDownload')return RD76.base.draw.apply(this,arguments);
 if(!T.switched||T.t<1.6)return;const u=clamp((T.t-1.6)/2.4,0,1),f=Math.floor(b._r30.clock*V18_ART.models.colossus.fps)%16,cut=Math.round(b.y-205+410*u);
 for(const id of ['left','core','right']){const p=b.parts.find(p=>p.id===id);if(!p||p.destroyed)continue;
  ctx.save();ctx.beginPath();ctx.rect(b.x-205,b.y-205,410,Math.max(0,cut-(b.y-205)));ctx.clip();rd76Blit(id+'_body',f,b.x,b.y);ctx.restore();
  if(u<1){ctx.save();ctx.beginPath();ctx.rect(b.x-205,cut,410,Math.max(0,b.y+205-cut));ctx.clip();rd76Blit(id+'_wire',f,b.x,b.y);ctx.restore();}
 }
};
function rd76Scan(t,y){const a=AD20_ART.curtain;if(!XART.rdy(a.key))return;const f=Math.floor(t*a.fps)%a.frames,c=a.cells[f];ctx.save();ctx.beginPath();ctx.rect(camLeftX(),y-18,viewW(),36);ctx.clip();for(let x=camLeftX();x<camRightX();x+=256)ctx.drawImage(XART.get(a.key),...c,Math.round(x),Math.round(y-128),256,256);ctx.restore();}
drawWorld=function(){const out=RD76.base.world.apply(this,arguments),b=boss,T=rd76State(b);if(!T||b._r30.mode!=='v18returnDownload')return out;
 // Follow the same camera adapter used by the native full-view curtain owner.
 ctx.save();ctx.setTransform(SS,0,0,SS,0,0);const z=viewZoom();ctx.scale(z,z);ctx.translate(-camLeftX(),VH*(1-z)/z);
 if(T.t<1.6){const u=T.t<.85?T.t/.65:1-(T.t-.95)/.65;er23Curtain('blackout',Math.round(clamp(u,0,1)*16));rd76Scan(T.t,viewTopY()+viewH()*clamp(T.t/1.6,0,1));}
 else if(T.t<4)rd76Scan(T.t,b.y-205+410*clamp((T.t-1.6)/2.4,0,1));
 ctx.restore();return out;
};
globalThis.BOF_DRACODIA_RETURN_1030=RD76;
