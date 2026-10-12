"use strict";
/* Mike 1011 recording, 38:02: bottom-half Chromium columns and an anchored SIDE SLIDE.
   Reuses the authored Chromium beam and intact sixteen-pose Hammer banks. */
const HC11={version:1,events:[],draws:{beam:0,counter:0},base:{impact:hammerStormImpact,tick:hammerStormTick,
 wave:hammerStormWaveTick,shape:hammerStormSpikeShape,hits:hammerStormSpikeHits,spikeDraw:hammerStormSpikeDraw,
 draw:hammerStormDraw,head:hammerHeadPoint,depth:hammerDepthScale,plane:hammerOnPlayerPlane,
 committed:hammerStrikeCommitted,load:stageLoadBegin}};
function hc11Log(event,data={}){HC11.events.push({event,...data});if(HC11.events.length>120)HC11.events.shift();}
function hc11Fight(b){return !!b?._hammer&&!b.dead&&(!b._hammerTime||b._hammerTime.mode==='attack')&&(!b._hama||b._hama.mode==='attack');}
function hc11MidY(){return viewTopY()+viewH()*.5;}
function hc11Ready(){return XART.rdy('arch_chromium_beam_0926')&&['swing_left','swing_right'].every(n=>HM10_ART[n].every(a=>XART.rdy(a.key)));}
stageLoadBegin=function(n,keys){return HC11.base.load.call(this,n,[...(keys||[]),...([5,8].includes(n)?['arch_chromium_beam_0926']:[])]);};
hammerStormImpact=function(b){const r=HC11.base.impact.apply(this,arguments);if(!hc11Fight(b))return r;
 const h=b._hammer,top=hc11MidY(),bottom=hammerStormFloorY();
 h.hc11Counter=null;h.hc11CounterDone=false;h.bm9Counter=null;h.bm9CounterDone=true;
 h.stormBounds.top=top;h.stormBounds.bottom=bottom;
 for(const q of h.stormWaves||[]){Object.assign(q,{hc11Beam:true,y:bottom,top,height:bottom-top,radius:17,retinaWidth:64,
  warm:Math.max(1.2,q.warm),active:1.18,hitSeats:{}});}
 hc11Log('chromium-bottom-half',{top,bottom,lanes:h.stormWaves.length});return r;
};
function hc11BeamShape(q){
 const start=q.split+(q.delay||0)+q.warm,dur=q.active,age=q.t-start;
 if(q.t<start||q.t>=start+dur)return null;
 const rise=.16,fade=.22,p=clamp(age/rise,0,1),out=clamp((dur-age)/fade,0,1);
 return {hc11Beam:true,age,dur,f:hammerChromiumFrame(age,dur),height:q.height,
  width:q.radius*2*Math.min(p,out),alpha:Math.min(1,p*2,out*2),live:age>=.10&&age<dur-.12};
}
hammerStormSpikeShape=function(q){return q.hc11Beam?hc11BeamShape(q):HC11.base.shape.apply(this,arguments);};
hammerStormSpikeHits=function(q,x,y){if(!q.hc11Beam)return HC11.base.hits.apply(this,arguments);
 const a=hc11BeamShape(q);return !!a&&a.live&&y>=q.top&&y<=q.y&&Math.abs(x-q.x)<a.width/2;
};
hammerStormSpikeDraw=function(q){if(!q.hc11Beam)return HC11.base.spikeDraw.apply(this,arguments);
 const a=hc11BeamShape(q),key='arch_chromium_beam_0926';if(!a||a.width<.5||!XART.rdy(key))return;
 const im=XART.get(key),cw=im.width/4,ch=im.height/2,k=q.height/ch;
 ctx.save();ctx.beginPath();ctx.rect(q.x-60,q.top,120,q.height);ctx.clip();ctx.globalAlpha*=a.alpha;
 // Bypass the old global Chromium-to-ice substitution. Keep both authored caps
 // and the whole cell's proportions; column height controls one uniform scale.
 ctx.imageSmoothingEnabled=false;
 ctx.drawImage(im,(a.f%4)*cw,Math.floor(a.f/4)*ch,cw,ch,q.x-cw*k/2,q.top,cw*k,ch*k);
 HC11.draws.beam++;
 ctx.restore();
};
hammerStormWaveTick=function(b,dt){const h=b._hammer;
 if(!(h.stormWaves||[]).some(q=>q.hc11Beam))return HC11.base.wave.apply(this,arguments);
 for(const q of h.stormWaves){q.t+=dt;const age=q.t-q.split-(q.delay||0);
  if(age>=0&&age<q.warm)combatWarningTick(q,'chromium-spike',age,q.warm);
  if(age>=q.warm&&!q.started){q.started=true;combatWarningTick(q,'chromium-spike',q.warm,q.warm);
   Audio.SFX.hammerEradBlast?.();hc11Log('chromium-column',{x:q.x,top:q.top,bottom:q.y});}
  for(const seat of seatList())withSeat(seat,()=>{
   if(!player.dead&&!player.out&&player.invuln<=0&&(q.hitSeats[seat]||0)<=q.t&&hammerStormSpikeHits(q,player.x,player.y)){
    q.hitSeats[seat]=q.t+.85;playerHit('Chromium beam');}
  });
 }
};
function hc11UpperTarget(){let target=null;
 for(const seat of seatList())withSeat(seat,()=>{if(!player.dead&&!player.out&&player.y<hc11MidY()&&(!target||player.y<target.y))target={x:player.x,y:player.y,seat};});
 return target;
}
function hc11Frame(C,t=C.t){
 if(t<C.riseAt)return Math.min(3,Math.floor(t/C.riseAt*4));
 if(t<C.lockAt)return 4+Math.min(3,Math.floor((t-C.riseAt)/(C.lockAt-C.riseAt)*4));
 if(t<C.tell)return 7;
 if(t<C.strikeEnd)return 8+Math.min(3,Math.floor((t-C.tell)/(C.strikeEnd-C.tell)*4));
 return 12+Math.min(3,Math.floor((t-C.strikeEnd)/(C.end-C.strikeEnd)*4));
}
function hc11Rotate(x,y,angle){return{x:x*Math.cos(angle)-y*Math.sin(angle),y:x*Math.sin(angle)+y*Math.cos(angle)};}
function hc11Tip(C,f=hc11Frame(C),x=C.x,y=C.y,scale=C.scale,angle=C.angle){
 const a=HM10_ART[C.bank][f],p=hc11Rotate((a.tip[0]-a.pivot[0])*HM10.bodyScale*scale,(a.tip[1]-a.pivot[1])*HM10.bodyScale*scale,angle);
 return{x:x+p.x,y:y+p.y};
}
function hc11Landing(anchor,side){
 const bank=side>0?'swing_right':'swing_left',a=HM10_ART[bank][11],scale=1.1;
 const dx=(a.tip[0]-a.pivot[0])*HM10.bodyScale*scale,dy=(a.tip[1]-a.pivot[1])*HM10.bodyScale*scale,r=Math.hypot(dx,dy);
 // Orbit the intact plate around its chest; the measured hammer head meets the
 // locked point even at the upper edge, without cropping or moving that target.
 const ty=Math.min(dy,-Math.max(0,PLAY.y+100-anchor.y)),vy=Math.max(-r*.90,ty);
 const vx=side*Math.sqrt(Math.max(0,r*r-vy*vy));let angle=Math.atan2(vy,vx)-Math.atan2(dy,dx);
 while(angle>Math.PI)angle-=TAU;while(angle<-Math.PI)angle+=TAU;
 const x=anchor.x-vx,y=anchor.y-vy;
 const penalty=Math.max(0,camLeftX()+95-x)+Math.max(0,x-(camRightX()-95));
 return{bank,side,x,y,scale,angle,penalty};
}
function hc11BeginCounter(b,anchor){const h=b._hammer,preferred=anchor.x>=b.x?1:-1;
 const a=hc11Landing(anchor,preferred),z=hc11Landing(anchor,-preferred),land=z.penalty<a.penalty?z:a;
 const lock=hammerFurious()?.62:hammerHard()?.72:diffKey==='easy'?.96:.84;
 const C=h.hc11Counter={anchor:{...anchor},bank:land.bank,side:land.side,land,t:0,riseAt:.32,lockAt:.80,
  diveAt:.80+lock,tell:1.22+lock,strikeEnd:1.58+lock,end:2.30+lock,
  ox:b.x,oy:b.y,x:b.x,y:b.y,scale:1,angle:0,hitSeats:{}};
 C.sky={x:clamp(anchor.x-land.side*65,camLeftX()+55,camRightX()-55),y:Math.max(viewTopY()+72,anchor.y-115)};
 h.bm9Counter=null;h.bm9CounterDone=true;h.stormRecovery=null;
 Audio.SFX.bossWeaponCharge?.();hc11Log('upper-half-lock',{...anchor,side:C.side});return C;
}
function hc11Pose(C,t=C.t){const ease=p=>p*p*(3-2*p);let x=C.ox,y=C.oy,scale=1,angle=0;
 // Stay on the player's plane, sliding into the measured side-strike pose.
 // Only the separate orbital jump attack travels into the background.
 if(t<C.tell){const u=ease(clamp(t/C.diveAt,0,1));
  x=lerp(C.ox,C.land.x,u);y=lerp(C.oy,C.land.y,u);scale=lerp(1,C.land.scale,u);angle=C.land.angle*u;}
 else if(t>=C.tell){x=C.land.x;y=C.land.y;scale=C.land.scale;angle=C.land.angle;
  if(t>=C.strikeEnd){const u=ease(clamp((t-C.strikeEnd)/(C.end-C.strikeEnd),0,1));scale=lerp(scale,1,u);angle*=1-u;}}
 return{x,y,scale,angle};
}
function hc11StrikeLane(C){const p=C.land,a=hc11Tip(C,7,p.x,p.y,p.scale,p.angle),z=hc11Tip(C,11,p.x,p.y,p.scale,p.angle),L={x:a.x,y:a.y,ex:z.x,ey:z.y};
 const bend=Math.max(...[8,9,10].map(f=>{const q=hc11Tip(C,f,p.x,p.y,p.scale,p.angle);return s81003Distance(q.x,q.y,L);}));
 return{...L,width:38+bend*2,progress:clamp(C.t/C.tell,0,1),laneShape:'line'};
}
function hc11WarningDraw(C){const p=C.land,points=[7,8,9,10,11].map(f=>hc11Tip(C,f,p.x,p.y,p.scale,p.angle)),progress=clamp(C.t/C.tell,0,1);
 for(let i=1;i<points.length;i++){const a=points[i-1],z=points[i];
  combatWarningDraw(C,{x:a.x,y:a.y,ex:z.x,ey:z.y,width:44,progress,laneShape:'line',fieldOnly:true,alpha:.65});}
 combatWarningDraw(C,{x:C.anchor.x,y:C.anchor.y,ex:C.anchor.x,ey:C.anchor.y,progress,alertOnly:true,alertX:C.anchor.x,alertY:C.anchor.y-55});
}
function hc11StrikeTick(C,before){
 if(C.t<C.tell||before>=C.strikeEnd)return;
 const at=Math.max(C.tell,before),end=Math.min(C.t,C.strikeEnd-.000001),samples=[at];
 for(let i=1;i<4;i++){const t=C.tell+(C.strikeEnd-C.tell)*i/4;if(t>at&&t<=end)samples.push(t);}
 samples.push(end);let previous=C.previous||hc11Tip(C,7,C.land.x,C.land.y,C.land.scale,C.land.angle);
 for(const t of samples){const f=hc11Frame(C,t),q=hc11Tip(C,f,C.land.x,C.land.y,C.land.scale,C.land.angle),L={x:previous.x,y:previous.y,ex:q.x,ey:q.y};
  for(const seat of seatList())withSeat(seat,()=>{if(!C.hitSeats[seat]&&!player.dead&&!player.out&&player.invuln<=0&&s81003Distance(player.x,player.y,L)<22){
   C.hitSeats[seat]=true;playerHit('Hammer anchored side strike');}});previous=q;
 }
 C.previous=previous;
}
function hc11CounterTick(b,C,dt){const h=b._hammer,before=C.t;C.t+=dt;
 Object.assign(C,hc11Pose(C));b.x=C.x;b.y=C.y;
 if(C.t<C.tell)combatWarningTick(C,'hammer-side-counter',C.t,C.tell);
 if(before<C.diveAt&&C.t>=C.diveAt){Audio.SFX.hammerThrow?.();hc11Log('upper-half-slide',{...C.anchor});}
 if(before<C.tell&&C.t>=C.tell){combatWarningTick(C,'hammer-side-counter',C.tell,C.tell);Audio.SFX.hammerImpact?.();shake=Math.max(shake,6);}
 hc11StrikeTick(C,before);
 if(!C.impact&&C.t>=C.tell+(C.strikeEnd-C.tell)*.75){C.impact=true;h.leapFx=.01;h.leapFxX=C.anchor.x;h.leapFxY=C.anchor.y;
  hc11Log('anchored-hammer-impact',{...C.anchor,tip:hc11Tip(C,11,C.land.x,C.land.y,C.land.scale,C.land.angle)});}
 if(C.t>=C.end){h.hc11Counter=null;h.hc11CounterDone=true;const home=h.stormHome||{x:worldWidth()/2,y:VH*.34};
  h.stormRecovery={ox:b.x,oy:b.y,x:home.x,y:home.y,depart:h.t,duration:.75,done:false};hc11Log('counter-recovery');}
}
hammerStormTick=function(b,dt){const h=b._hammer;
 if(h.state!=='storm_split'){if(h.hc11Counter){h.hc11Counter=null;h.stormWaves=[];}return HC11.base.tick.apply(this,arguments);}
 if(!hc11Fight(b)||!(h.stormWaves||[]).some(q=>q.hc11Beam))return HC11.base.tick.apply(this,arguments);
 hammerStormWaveTick(b,dt);
 if(!h.hc11Counter&&!h.hc11CounterDone&&h.t>=.45){const target=hc11UpperTarget();if(target)hc11BeginCounter(b,target);}
 if(h.hc11Counter)hc11CounterTick(b,h.hc11Counter,dt);else hammerStormReturnTick(b);
 if(!h.hc11Counter&&(!h.stormRecovery||h.stormRecovery.done)&&h.stormWaves.every(q=>q.t>q.split+(q.delay||0)+q.warm+q.active)){
  h.stormWaves=[];hammerState(b,'storm_idle');}
 return true;
};
hammerStrikeCommitted=function(b){const C=b?._hammer?.hc11Counter;return !!C&&C.t<C.strikeEnd||HC11.base.committed.apply(this,arguments);};
hammerDepthScale=function(b){return b?._hammer?.hc11Counter?.scale??HC11.base.depth.apply(this,arguments);};
hammerOnPlayerPlane=function(b){const C=b?._hammer?.hc11Counter;
 // This move's collision is the measured hammer sweep. The sliding body cannot
 // create a second untelegraphed contact hit.
 return C?false:HC11.base.plane.apply(this,arguments);
};
hammerHeadPoint=function(b){const C=b?._hammer?.hc11Counter;return C?hc11Tip(C):HC11.base.head.apply(this,arguments);};
hammerStormDraw=function(b){const C=b?._hammer?.hc11Counter;if(!C)return HC11.base.draw.apply(this,arguments);
 const h=b._hammer;if(ctx.getTransform)h.stormDrawMatrix=ctx.getTransform();
 for(const q of h.stormWaves||[]){hammerStormRedZoneDraw(q);hammerStormRowRetinaDraw(q);hammerStormSpikeDraw(q);hammerStormRowAlertDraw(q);}
 if(C.t<C.tell){const p=C.t/C.tell,col=p<.40?null:p<.72?'yellow':'red';
  hammerGroundReticleDraw(hammerFrame('reticle',0,col),C.anchor.x,C.anchor.y,100,.95);
  hc11WarningDraw(C);}
 ctx.save();ctx.translate(b.x,b.y);ctx.rotate(C.angle);
 if(hm10Blit(C.bank,hc11Frame(C),0,0,HM10.bodyScale*C.scale,b.flash||0))HC11.draws.counter++;
 ctx.restore();return true;
};
