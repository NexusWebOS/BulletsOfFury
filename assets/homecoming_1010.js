"use strict";
/* Mike rejected the generated aircraft likenesses. Use the original pilot
   sheets' straight front/rear images; movement and scale animate the flight. */
const HC10={pilots:['cole','axel','freezer','yuri','maverick','falva','lizzie','decker','juggernaut'],
 draws:{},last:null,portal:null};
for(const bank of Object.values(HC10_ART))for(const a of bank)XART._src[a.key]=a.path;
function hc10ShipKey(pk,view){
 pk=HC10.pilots.includes(pk)?pk:'axel';
 return 'ship_'+pk+'_so'+(view==='front'?6:2);
}
function hc10ShipAssets(pk){return ['front','rear'].map(view=>({key:hc10ShipKey(pk,view)}));}
function hc10ShipGeometry(pk,view){
 const key=hc10ShipKey(pk,view),a=window.BOFX?.ships?.[key];if(!a)return null;
 // The owning ship manifest supplies the real alpha trim within XART's
 // original canvas. Crop the empty padding, preserving every authored pixel.
 return {key,rect:[a[4],a[5],a[2],a[3]],w:a[2],h:a[3]};
}
function hc10StaticShip(pk,view,x,y,width){
 const a=hc10ShipGeometry(pk,view);if(!a||!XART.rdy(a.key))return false;
 const height=width*a.h/a.w;ctx.save();ctx.imageSmoothingEnabled=false;
 ctx.drawImage(XART.get(a.key),...a.rect,x-width/2,y-height/2,width,height);ctx.restore();
 HC10.draws[a.key]=(HC10.draws[a.key]||0)+1;return true;
}
function hc10FlightAssets(pk){
 pk=HC10.pilots.includes(pk)?pk:'axel';
 return [...HC10_ART.space,...HC10_ART.earth,...hc10ShipAssets(pk),...AP10_CIN_ART.void];
}
function hc10Cell(bank,f,x,y,width,alpha=1){
 const list=HC10_ART[bank],a=list?.[clamp(f|0,0,list.length-1)];if(!a||!XART.rdy(a.key))return false;
 const k=width/a.w;ctx.save();ctx.globalAlpha*=alpha;ctx.imageSmoothingEnabled=false;
 ctx.drawImage(XART.get(a.key),x-a.pivot[0]*k,y-a.pivot[1]*k,a.w*k,a.h*k);ctx.restore();
 HC10.draws[a.key]=(HC10.draws[a.key]||0)+1;return true;
}
function hc10Rect(bank,W,H){
 const a=HC10_ART[bank][0],c=a.content_rect,k=Math.min(W/c[2],H*.72/c[3]);
 return {x:(W-c[2]*k)/2,y:8,w:c[2]*k,h:c[3]*k};
}
function hc10Plate(bank,R,alpha=1){
 const a=HC10_ART[bank][0];if(!XART.rdy(a.key))return false;
 ctx.save();ctx.globalAlpha*=alpha;ctx.imageSmoothingEnabled=false;
 ctx.drawImage(XART.get(a.key),...a.content_rect,R.x,R.y,R.w,R.h);ctx.restore();
 HC10.draws[a.key]=(HC10.draws[a.key]||0)+1;return true;
}
function hc10FlightSample(t,pk){
 pk=HC10.pilots.includes(pk)?pk:'axel';
 const earth=t>=3,approach=t>=6,q=clamp(earth?(approach?(t-6)/3.4:(t-3)/3):t/3,0,1),d=q*q*(3-2*q),
  view=earth?'rear':'front',bank=hc10ShipKey(pk,view);
 return {pilot:pk,t,phase:approach?'approach':earth?'earth':'escape',bank,view,frame:0,x:.5,
  y:approach?lerp(.22,.58,d):earth?lerp(.23,.66,d):lerp(.37,.57,d),
  width:approach?lerp(.065,.20,d):earth?lerp(.31,.018,d):lerp(.045,.32,d),rotation:0};
}
function hc10Flight(t,pk,R){
 const s=hc10FlightSample(t,pk),width=R.w*s.width,nativeWidth=width;
 if(t<3){
  const opening=t<.67,closing=t>=2.05,
   frame=opening?ap10VoidFrame('open',t):closing?ap10VoidFrame('close',(t-2.05)*.85):ap10VoidFrame('loop',t);
  const size=R.h*(closing?lerp(.68,.08,clamp((t-2.05)/.60,0,1)):.76),x=R.x+R.w*.5,y=R.y+R.h*.37;
  if(t<2.66)ap10VoidCell(frame,x,y,size,size,0,1);
  HC10.portal={frame,size,x,y,visible:t<2.66,source:AP10_CIN_ART.void[frame].key};
 }else HC10.portal=null;
 hc10StaticShip(s.pilot,s.view,R.x+R.w*s.x,R.y+R.h*s.y,width);
 HC10.last={...s,rect:R,jet:{x:R.x+R.w*s.x,y:R.y+R.h*s.y,width,nativeWidth},portal:HC10.portal};
 return HC10.last;
}
