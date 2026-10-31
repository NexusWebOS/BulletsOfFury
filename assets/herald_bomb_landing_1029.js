'use strict';
/* Each physical Herald bomber drop owns a committed bottom impact and a short
   authored Retina arrival. Ordinary drops retain their existing direct danger;
   the original explosive subset retains its native radial pattern. */
const HL51={base:{drop:hb25BombDrop,burst:hb25Burst,load:stageLoadBegin},events:[],serial:0,draws:[],floorPad:36};
const HL51_ART={key:'hl51_arrival_retina',path:'assets/game/levels/stage_08/miniboss/herald_landing_retinas_1030/retina.png',cw:64,ch:32,cols:8,frames:24};
XART._src[HL51_ART.key]=HL51_ART.path;
stageLoadBegin=function(n,keys){return HL51.base.load.call(this,n,n===8?[...(keys||[]),HL51_ART.key]:keys);};
function hl51Own(b){return run.stage===8&&b===subBoss&&!!b?._hd1003&&!b.dead;}
function hl51Log(event,data){HL51.events.push({event,time:efxClock,...data});if(HL51.events.length>600)HL51.events.shift();}
hb25BombDrop=function(b,Q,P){if(!hl51Own(b))return HL51.base.drop.apply(this,arguments);
 const old=P.target,heavy=!!P.burst;P.target={x:old.x,y:VH-HL51.floorPad};
 const first=eBullets.length,r=HL51.base.drop.apply(this,arguments),q=eBullets.slice(first).find(q=>q._hb25Drop&&q._heraldOwner1003===b);
 if(q){const index=b._hd1003._hl51Band||0;let B=q._hb25Bomb;
  if(!B){const flight=Math.max(.24,(P.target.y-q.y)/(q.vy*60));
   B=q._hb25Bomb={at:efxClock+flight,target:{x:q.x+q.vx*60*flight,y:P.target.y},escapeX:Q.escapeX,rank:Q.rank,seed:P.seed};q._hl51Simple=true;
  }
  b._hd1003._hl51Band=index+1;q._hl51=++HL51.serial;B._hl51=q._hl51;
  // Cosmetic acquisition sweeps into the already committed world-space point.
  // It cannot drag the bomb target after release or shorten its flight.
  q._hl51From={x:clamp(B.target.x+(index%2?92:-92),camLeftX()+32,camRightX()-32),y:B.target.y-48-(index%3)*12};
  q._hl51Reveal=Math.min(.18,(B.at-q._hb25Born)*.25);
  hl51Log('drop',{id:q._hl51,simple:!heavy,part:P.id,x:q.x,y:q.y,vx:q.vx,vy:q.vy,target:{...B.target},at:B.at,from:{...q._hl51From},reveal:q._hl51Reveal});
 }else P.target=old;
 return r;
};
function hl51Mark(q){const B=q?._hb25Bomb;if(!q?._hl51||!B||q.dead||!hl51Own(q._heraldOwner1003)||!hd1003Live(q._heraldOwner1003,hd1003Part(q._heraldOwner1003,q._heraldPart1003)))return null;
 const age=Math.max(0,efxClock-q._hb25Born),u=clamp(age/q._hl51Reveal,0,1),ease=1-Math.pow(1-u,3),progress=clamp(age/(B.at-q._hb25Born),0,1),colour=progress<.5?0:progress<.78?1:2,
  fade=u<1?Math.min(7,Math.floor(u*8)):colour===2&&Math.floor(age*14)%2?6:7,frame=colour*8+fade;
 return{id:q._hl51,x:lerp(q._hl51From.x,B.target.x,ease),y:lerp(q._hl51From.y,B.target.y,ease),frame,progress,settled:u>=1,target:B.target};
}
function hl51Reticle(q){const p=hl51Mark(q),a=HL51_ART;if(!p||!XART.rdy(a.key))return false;
 ctx.drawImage(XART.get(a.key),p.frame%8*64,Math.floor(p.frame/8)*32,64,32,Math.round(p.x)-32,Math.round(p.y)-16,64,32);
 HL51.draws.push({id:p.id,x:p.x,y:p.y,frame:p.frame,settled:p.settled});if(HL51.draws.length>80)HL51.draws.shift();return true;
}
hb25Burst=function(q){const B=q?._hb25Bomb;if(!q?._hl51)return HL51.base.burst.apply(this,arguments);
 const b=q._heraldOwner1003,live=hl51Own(b)&&hd1003Live(b,hd1003Part(b,q._heraldPart1003));q.x=B.target.x;q.y=B.target.y;
 let r;if(q._hl51Simple){q.dead=true;if(live){explode(q.x,q.y,26,'red');combatAudio0927(b,'combatOrb0927',.12);}}
 else r=HL51.base.burst.apply(this,arguments);
 if(live)hl51Log('impact',{id:q._hl51,simple:!!q._hl51Simple,x:B.target.x,y:B.target.y});return r;
};
globalThis.BOF_HERALD_BOMB_LANDING_1029=HL51;
