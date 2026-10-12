"use strict";
/* Shared authored-pixel painter for live combat and the review's onion viewer. */
const WP11_FAMILIES=['bullets','spread','missile','laser','gust','tornado','mist','heavy','electric'];
function wp11Family(b){
 if(!b||b._inf!=='wind'&&b._el!=='wind')return null;
 if(b._cal50)return 'heavy';
 return ({mg:'bullets',spread:'spread',missile:'missile',beam:'laser',flame:'gust',orb:'tornado',
  lasermist:'mist',shard:'mist',iceLance:'mist',yuriLightningOrb:'electric',yuriLightningBolt:'electric',
  prismRay:'spread',chromeRay:'spread',forgeFireBlast:'spread'})[b.kind]||null;
}
function wp11Frame(bank,resolve,t){
 if(!bank?.length)return null;
 const phase=Math.floor(Math.max(0,Number.isFinite(t)?t:0)*(bank[0].fps||24))%bank.length;
 // Every key is touched before selecting a ready image. A cold decode never blanks a shot.
 const loaded=bank.map(a=>resolve(a.key));
 for(let d=0;d<bank.length;d++){const i=(phase-d+bank.length)%bank.length;if(loaded[i])return {a:bank[i],im:resolve(bank[i].key)};}
 return null;
}
function wp11Paint(g,bank,resolve,b,clock=0){
 if(!b||b.dead||b._launchDelay>0||!Number.isFinite(b.x))return 0;
 const family=WP11_FAMILIES[bank?.[0]?.slot];if(!family)return 0;
 const held=family==='laser'||family==='gust',t=held?clock:(b.t??b._bt??clock);
 if(!held&&!Number.isFinite(b.y))return 0;
 const q=wp11Frame(bank,resolve,t);if(!q)return 0;
 const {a,im}=q,lv=Math.max(1,Math.min(5,b._infLv||b.lv||1));let draws=0;
 const rect=(r,k,x,y)=>{g.drawImage(im,...r,x+(r[0]-a.pivot[0])*k,y+(r[1]-a.pivot[1])*k,r[2]*k,r[3]*k);draws++;};
 g.save();g.imageSmoothingEnabled=false;g.shadowBlur=0;
 if(held){
  const top=b.top??b.y-(b.h||0),bot=b.bot??b.y,width=b.w||18,length=bot-top;
  if(![top,bot,width,length].every(Number.isFinite)||length<=0||width<.5){g.restore();return 0;}
  if(family==='laser'){
   const r=a.body_rect,k=width*2/r[2],root=a.root_rect,tip=a.tip_rect;
   const start=top+Math.min(length,60*k),end=bot-Math.min(length,34*k),step=Math.max(1,r[3]*k-2);
   g.beginPath();g.rect(b.x-width*4,top,width*8,length+30*k);g.clip();
   g.save();g.beginPath();g.rect(b.x-width*4,Math.floor(start),width*8,Math.max(0,Math.ceil(end)-Math.floor(start)));g.clip();
   for(let y=start,n=0;y<end&&n<128;y+=step,n++){
    // Overlap adjacent source tiles by two pixels; one shared end clip prevents seams.
    g.drawImage(im,...r,b.x+(r[0]-a.pivot[0])*k,y,r[2]*k,r[3]*k);draws++;
   }
   g.restore();
   g.drawImage(im,...tip,b.x+(tip[0]-a.pivot[0])*k,top,tip[2]*k,tip[3]*k);draws++;
   rect(root,k,b.x,bot);
  }else{
   const k=Math.max(34,width)/128,r=[0,16,256,a.pivot[1]-16],step=140*k;
   g.beginPath();g.rect(b.x-width*1.3,top,width*2.6,length);g.clip();
   for(let y=bot,n=0;y>top&&n<128;y-=step,n++){
    rect(r,k,b.x,y);
   }
  }
 }else{
  let k;
  if(['bullets','spread','missile','heavy'].includes(family)){
   const physical=bank[0].body_height||70;
   const desired=({bullets:16+lv*2,spread:15+lv*2,missile:30+lv*3,heavy:27+lv*3})[family];k=desired/physical;
  }else{k=(family==='mist'?38+lv*4:Math.max(b.w||24,b.h||24)*2)/a.h;}
  const angle=family==='tornado'||family==='electric'?0:Math.atan2(b.vy||-1,b.vx||0)+Math.PI/2;
  g.translate(b.x,b.y);g.rotate(angle);rect([0,0,a.w,a.h],k,0,0);
 }
 g.restore();return draws;
}
