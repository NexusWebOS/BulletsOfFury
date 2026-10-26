"use strict";
// Authored, registered plates: stationary metalwork never morphs between frames.
// Only the faceless liquid bank moves; infection reveals the matching hull plate.
const OT24={base:ip21Visual,keys:campaignIntroKeys,last:null};
Snd.prepare(['crackle','bossWeaponCharge']);
XART._src.ot24_corrupt_laser='assets/game/levels/stage_08/boss/neural_archon_1023/beam_2.webp';
for(const a of Object.values(OT24_ART))XART._src[a.key]=a.path;
campaignIntroKeys=function(){return [...OT24.keys(),...Object.values(OT24_ART).map(a=>a.key),...PL11.keys('black_void'),'ot24_corrupt_laser'];};
{
 const rows=IP21.beats.map(b=>({...b})),i=rows.findIndex(b=>b.replay==='takeover');
 for(const b of rows)if(b.replay)b.duration=8;
 rows.splice(i+1,0,{replay:'downlink',who:'',text:'',duration:5},
  {bg:'cin_war_civilian_collapse',who:'NARRATOR',text:'Our infrastructure was hijacked. Machines turned on man.',duration:6},
  {bg:'cin_war_suburban_tanks',who:'CIVIL DISPATCH',text:'They are firing on homes! Get everyone away from the road!',duration:6},
  {bg:'cin_war_city_air_attack',who:'AIR DISPATCH',text:'Aircraft are attacking the city. We cannot regain control!',duration:6},
  {bg:'cin_war_naval_exchange',who:'NARRATOR',text:'Chaos spread across the globe.',duration:5});
 // Establish the event without showing its consequences before transmission.
 for(const b of rows)if(['cin_war_civilian_collapse','cin_war_city_air_attack'].includes(b.bg)&&b.at!==undefined){delete b.bg;b.hq=true;b.text=b.text.startsWith('One day')?'One day, it finally happened.':'Something unknown had reached our world.';}

 let t=0;for(const b of rows){b.at=t;b.to=t+=b.duration;}
 IP21.beats=rows;IP21.finaleAt=t;IP21.end=t+OB24.finaleDuration;
}
function ot24Image(name,x,y,size,alpha=1){
 const a=OT24_ART[name];if(!a||!XART.rdy(a.key))return false;
 const k=size/a.w;ctx.save();ctx.globalAlpha*=alpha;ctx.imageSmoothingEnabled=false;
 ctx.drawImage(XART.get(a.key),x-a.pivot[0]*k,y-a.pivot[1]*k,a.w*k,a.h*k);ctx.restore();return true;
}
function ot24Fluid(t,x,y,size,alpha=1){
 const a=OT24_ART.fluid;if(!XART.rdy(a.key))return;
 // Ping-pong keeps both ends continuous; never jump from last to first pose.
 const cycle=(a.frames-1)*2,n=Math.floor(Math.max(0,t)*10)%cycle,f=n<a.frames?n:cycle-n,k=size/a.w;
 ctx.save();ctx.globalAlpha*=alpha;ctx.imageSmoothingEnabled=false;
 ctx.drawImage(XART.get(a.key),(f%a.columns)*a.w,Math.floor(f/a.columns)*a.h,a.w,a.h,x-a.pivot[0]*k,y-a.pivot[1]*k,a.w*k,a.h*k);ctx.restore();
 return f;
}
function ot24Smooth(v){v=clamp(v,0,1);return v*v*(3-2*v);}
// Lock the clean structure. Only authored living-fluid pixels move over it.
function ot24Crawl(t,x,y,size){
 const root=[x-size*.10,y],duration=5.4,u=ot24Smooth(t/duration);
 const lanes=[[-.10,0,-.43,-.02,0],[-.10,0,-.10,-.38,.4],[-.10,0,.40,-.10,.7],[-.10,0,.02,.37,1.0],[.02,.10,.40,.17,1.3]];
 // Feed mass is clipped by the receiving hull, never faded or cut to clean.
 const feed=ot24Smooth(t/2.8);
 ctx.save();ctx.beginPath();ctx.rect(root[0]-size*.19,root[1]-size*.2,size*.38*(1-feed),size*.4);ctx.clip();ot24Fluid(t+8,root[0],root[1],size*.37);ctx.restore();
 for(let i=0;i<lanes.length;i++){
  const [ax,ay,bx,by,delay]=lanes[i],v=ot24Smooth((t-delay)/3.8);
  if(v<=0)continue;
  // Reuse actual animated tendril art at several fixed hull routes. Growing
  // coverage is a moving physical tip; no full satellite frame is replaced.
  const start=[x+ax*size,y+ay*size],end=[x+bx*size,y+by*size];
  const dx=end[0]-start[0],dy=end[1]-start[1],angle=Math.atan2(dy,dx);
  ctx.save();ctx.translate(start[0],start[1]);ctx.rotate(angle);
  ctx.beginPath();ctx.rect(-size*.09,-size*.055,(Math.hypot(dx,dy)+size*.18)*v,size*.11);ctx.clip();
  for(let j=0;j<3;j++)ot24Fluid(t+i*.6+j*.3,j*size*.10,0,size*.19);
  ctx.restore();
 }
 return {progress:u,feed,lanes:lanes.length};
}
ip21Visual=function(b,c,t,W,H){
 if(!b.replay)return OT24.base.apply(this,arguments);
 const down=b.replay==='downlink';
 if(down){
  ip21Cue(c,'ot24-downlink',b.at+.05,'crackle',c.t-.03);
  cinCover(OT24_ART.earth.key,W,H,.5);
  const sx=W*.31,sy=H*.26,size=H*.32,target=[W*.51,H*.57];
  const angle=-Math.atan2(target[0]-sx,target[1]-sy),socket=size*.45;
  const from=[sx-Math.sin(angle)*socket,sy+Math.cos(angle)*socket],length=Math.hypot(target[0]-from[0],target[1]-from[1]);
  ctx.save();ctx.translate(sx,sy);ctx.rotate(angle);
  ot24Image('satellite',0,0,size);ot24Crawl(t+8,0,0,size);ctx.restore();
  const charge=ot24Smooth(t/1.15),growth=ot24Smooth((t-1.15)/.65);
  ctx.save();ctx.translate(from[0],from[1]);ctx.rotate(angle);
  c22Bank('code_fragments',t,0,0,H*.10*charge,false,charge);
  if(growth>0&&XART.rdy('ot24_corrupt_laser')){
   const im=XART.get('ot24_corrupt_laser'),cw=im.width/4,ch=im.height/4,f=Math.floor(t*18)%16;
   // Registered authored beam cell, one proportional scale, socket at top.
   const scale=length/ch,w=cw*scale;
   ctx.save();ctx.beginPath();ctx.rect(-w/2,0,w,length*growth);ctx.clip();
   ctx.drawImage(im,f%4*cw,Math.floor(f/4)*ch,cw,ch,-w/2,0,w,length);ctx.restore();
  }
  ctx.restore();
  ip21Cue(c,'ot24-laser-charge',b.at+.05,'bossWeaponCharge',c.t-.03);
  OT24.last={shot:'downlink',from,to:target,angle,charge,growth,absorbed:true,laser:true};
 }else{
  cinCover('cinend_deep_space',W,H,.5);
  const x=W*.61,y=H*.43,size=Math.min(H*.81,W*.64),arrival=b.replay==='arrival';
  ot24Image('satellite',x,y,size);
  if(arrival){
   const u=ot24Smooth((t-.25)/1.2),travel=ot24Smooth((t-1.1)/5.6),px=W*.19,py=y;
   const pose=PL11.sequence('black_void',t,{form:1.1,loop:5.4,close:1.5});

   // Fluid comes through the portal's plane, then reaches the left hull edge.
   const fx=lerp(px,x-size*.10,travel),fy=lerp(py,y,travel),s=size*.37;
   ctx.save();ctx.beginPath();ctx.rect(px-size*.18,py-size*.20,size*.36+W*ot24Smooth((t-1.1)/.65),size*.40);ctx.clip();
   const frame=ot24Fluid(t,fx,fy,s);ctx.restore();
   // Portal is the foreground occluder: throat and rim hide the entire
   // symbiote until its leading edge physically passes the exit plane.
   PL11.draw(ctx,pose,px,py,H*.57,k=>XART.get(k));
   ip21Cue(c,'ot24-portal',b.at+.1,'warpGate',c.t-.03);
   OT24.last={shot:'arrival',frame,travel,face:false,portal:'black_void',fluidAlpha:1};
  }else{
   const motion=ot24Crawl(t,x,y,size);
   OT24.last={shot:'takeover',...motion,lockedHull:true,alpha:1,face:false};
  }
 }
 msgFaceUse('dialogue');msgText(down?'HIJACKED RELAY / EARTH DOWNLINK':'FURY SATELLITE / ORBITAL WATCH',W/2,H*.045,Math.max(9,H*.021),'#a8e7ef',1,.9,.02);msgFaceUse(null);
};
// Silent visual shots have no empty speaker frame. User text overrides still show.
const ot24Caption=ip21Caption;
ip21Caption=function(b,c){if(b.replay&&!ip21Line(b,c).trim())return;return ot24Caption.apply(this,arguments);};
