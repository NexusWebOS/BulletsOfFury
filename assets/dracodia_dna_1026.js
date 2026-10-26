'use strict';
/* Mike Oct26: living synthetic code rises and spirals into the fading skeleton. */
const RD28={base:{bank:er23DrawBank,scene:rb23SceneDraw,under:rd25UnderEffects,over:rd25OverEffects,load:stageLoadBegin},last:null,
 sources:{code:AA5_ART.code,fluid:SV10_ART.crawl,crop:[149,96,64,256]},skin:null,palette:new Map()};
for(const a of Object.values(RD28_PALETTE))XART._src[a.key]=a.path;
function rd28Keys(){return Object.values(RD28_PALETTE).map(a=>a.key);}
function rd28Ready(){return rd28Keys().map(k=>XART.rdy(k)).every(Boolean);}
function rd28Image(a){let c=RD28.palette.get(a.key);if(c)return c;
 const kind=a.key.startsWith('aa5_code_')?'code':'fluid',bank=RD28_PALETTE[kind],f=RD28.sources[kind].findIndex(q=>q.key===a.key);
 if(f<0||!XART.rdy(bank.key))return null;c=document.createElement('canvas');c.width=bank.w;c.height=bank.h;
 c.getContext('2d').drawImage(XART.get(bank.key),f%bank.cols*bank.w,Math.floor(f/bank.cols)*bank.h,bank.w,bank.h,0,0,bank.w,bank.h);
 RD28.palette.set(a.key,c);return c;
}
stageLoadBegin=function(n,keys){return RD28.base.load.call(this,n,[...(keys||[]),...(n===8?rd28Keys():[])]);};
function rd28State(b,x,y,time=b._r30.t){const t=time,absorb=clamp((t-13.8)/2,0,1),warm=clamp((t-6.2)/.8,0,1),fade=1-absorb,
 cx=x==null?rd25Pose(b).x:x,cy=y==null?rd25Pose(b).y:y;
 return{t,x:cx,y:Math.min(cy,viewTopY()+viewH()-105),height:320*(1-absorb*.50),absorb,alpha:warm*fade,
  phase:(t-6.2)*1.65,flow:(t-6.2)*.23,codeFrame:Math.floor((t-6.2)*12)%12,fluidFrame:Math.floor((t-6.2)*14)%32};
}
function rd28Point(S,u,side){const theta=u*TAU*1.65-S.phase+side*Math.PI,
 radius=(68+20*Math.sin(u*Math.PI)**2+13*Math.sin(u*7-S.t*1.7))*(1-S.absorb*.72),
 sway=Math.sin(u*5-S.t*1.2)*11*(1-S.absorb),z=Math.cos(theta);
 return{x:S.x+sway+Math.sin(theta)*radius,y:S.y+(0.5-u)*S.height+Math.sin(u*4+S.t*1.3)*7,z,u,side};
}
function rd28Stamp(S,p,angle,size,alpha){const bank=RD28.sources.code,a=bank[(S.codeFrame+Math.floor(p.u*9))%bank.length],im=rd28Image(a),
 v=((p.u*256-(S.t-6.2)*64)%192+192)%192;
 ctx.save();ctx.translate(p.x,p.y);ctx.rotate(angle);ctx.globalAlpha*=S.alpha*alpha;ctx.globalCompositeOperation='screen';ctx.imageSmoothingEnabled=false;
 // Fixed square fragments retain the authored glyph proportions as the strand bends.
 ctx.drawImage(im,149,96+v,64,64,-size/2,-size/2,size,size);ctx.restore();
}
function rd28Strands(S,front){if(!S.alpha||!rd28Ready())return;
 const count=36;
 for(let side=0;side<2;side++)for(let i=0;i<count;i++){
  const p=rd28Point(S,i/count,side),q=rd28Point(S,(i+1)/count,side);
  if((p.z>=0)!==front)continue;
  rd28Stamp(S,p,Math.atan2(q.y-p.y,q.x-p.x)-Math.PI/2,25*(1-S.absorb*.35),front?.80:.42);
  RD28.last[front?'front':'back']++;
 }
 // Code cross-links make the paired strands read as synthetic DNA.
 if(!front)for(let i=3;i<36;i+=4){const a=rd28Point(S,i/36,0),b=rd28Point(S,i/36,1),n=Math.max(2,Math.ceil(Math.abs(b.x-a.x)/19));
  for(let j=0;j<=n;j++)rd28Stamp(S,{x:lerp(a.x,b.x,j/n),y:a.y,u:i/36},Math.PI/2,17,.24);
  RD28.last.rungs++;
 }
 for(let i=0;i<14;i++){
  const u=((i/14+S.flow)%1+1)%1,p=rd28Point(S,u,i%2);if((p.z>=0)!==front)continue;
  const next=rd28Point(S,Math.min(1,u+.025),i%2),a=RD28.sources.fluid[(S.fluidFrame+i*3)%32],
   size=(48+18*Math.sin(u*Math.PI)+9*Math.sin(S.t*2+i))*(1-S.absorb*.55),angle=Math.atan2(next.y-p.y,next.x-p.x)+Math.PI/2,life=Math.sin(u*Math.PI)**.65;
  ctx.save();ctx.translate(p.x,p.y);ctx.rotate(angle);ctx.globalAlpha*=S.alpha*life*(front?.82:.53);ctx.imageSmoothingEnabled=false;
  ctx.drawImage(rd28Image(a),-size/2,-size/2,size,size);
  ctx.globalCompositeOperation='screen';ctx.globalAlpha*=.35;ctx.drawImage(rd28Image(a),-size*.60,-size*.60,size*1.2,size*1.2);ctx.restore();
  RD28.last.blobs.push({u,x:p.x,y:p.y,z:p.z,size,life,front});
 }
}
function rd28CodeSkin(b,x,y){const t=b._r30.t,alpha=clamp((t-7)/.7,0,1)*clamp((14-t)/1.2,0,1)*(.68-.45*rd27Visibility(t).alpha);
 if(alpha<=0||!rd28Ready())return;
 const c=RD28.skin||(RD28.skin=document.createElement('canvas'));if(c.width!==256)c.width=c.height=256;
 const g=c.getContext('2d'),a=RD28.sources.code[Math.floor(t*12)%12],scroll=((t-7)*64)%256;
 g.clearRect(0,0,256,256);g.globalCompositeOperation='source-over';g.imageSmoothingEnabled=false;
 for(let col=0;col<4;col++)for(const yy of [-256,0,256])g.drawImage(rd28Image(a),149,96,64,256,col*64,yy-scroll,64,256);
 g.globalCompositeOperation='destination-in';g.drawImage(rd27Blend('carrier',t*20/24),0,0);g.globalCompositeOperation='source-over';
 ctx.save();ctx.globalAlpha*=alpha;ctx.globalCompositeOperation='screen';ctx.drawImage(c,x-128,y-128,256,256);ctx.restore();RD28.last.skin=alpha;
}
function rd28Begin(S){RD28.last={...S,front:0,back:0,rungs:0,blobs:[],skin:0};}
er23DrawBank=function(name,frame,x,y,flash=false){
 if(name==='symbiote'&&rd25Own(boss)&&boss._r30.t>=7&&boss._r30.t<14&&!flash){
  const S=rd28State(boss,x+RD25.carrierHeart[0]-128,y+RD25.carrierHeart[1]-128);rd28Begin(S);rd28Strands(S,false);
  const out=RD28.base.bank.apply(this,arguments);rd28CodeSkin(boss,x,y);rd28Strands(S,true);return out;
 }return RD28.base.bank.apply(this,arguments);
};
rb23SceneDraw=function(b){const out=RD28.base.scene.apply(this,arguments),t=b?._r30?.t;
 if(rd25Own(b)&&t>=6.2&&t<7){const S=rd28State(b,camLeftX()+viewW()/2,viewTopY()+viewH()-105);rd28Begin(S);rd28Strands(S,false);rd28Strands(S,true);}
 if(!rd25Own(b)||t<6.2||t>=15.8)RD28.last=null;
 return out;
};
rd25UnderEffects=function(b,Q,R){RD28.base.under.apply(this,arguments);
 if(Q.t>=14&&Q.t<15.8){const S=rd28State(b,Q.x,Q.y);rd28Begin(S);rd28Strands(S,false);}
};
rd25OverEffects=function(b,Q,R){RD28.base.over.apply(this,arguments);
 if(Q.t>=14&&Q.t<15.8)rd28Strands(rd28State(b,Q.x,Q.y),true);
};
globalThis.BOF_DRACODIA_DNA_1026=RD28;
