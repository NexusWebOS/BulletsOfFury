'use strict';
/* Fixed authored Cole bezel and head. Talk reels replace only the mouth, so
   unequal generated portrait crops never move the frame, hair or shoulders. */
const CP5={cache:new Map(),poses:['idle','happy','laugh','anger','sad','crash','victory',
 'talk-closed','talk-small','talk-medium','talk-wide','talk-o','neutral','smirking',
 'brooding','sunglasses','shout','smile-shades','salute','thinking']};
for(const em of CP5.poses)XART._src['cp5_raw_'+em]='assets/game/pilots_0922/portraits/cole-'+em+'.png';
for(let i=0;i<3;i++)XART._src['cp5_rage_'+i]='assets/game/dispatch_1002/cole_rage_'+i+'.png';
function cp5Cell(em,comm,rage){
 const id=em+':'+comm+':'+rage;if(CP5.cache.has(id))return CP5.cache.get(id);
 const baseKey=rage?'cp5_rage_2':'cp5_raw_idle';
 const talk=/^talk-/.test(em),sourceKey=rage?'cp5_rage_'+em:'cp5_raw_'+em;
 // Await the requested pose; never alternate between a cropped frame and its fallback.
 if(!XART.rdy('cp5_raw_idle')||!XART.rdy(baseKey)||!XART.rdy(sourceKey))return null;
 const c=document.createElement('canvas');c.width=c.height=256;
 const g=c.getContext('2d');g.imageSmoothingEnabled=false;
 if(comm){g.translate(256,0);g.scale(-1,1);}
 g.drawImage(XART.get('cp5_raw_idle'),0,0,256,256);
 if(rage||(!talk&&em!=='idle')){
  // All four complete rails come from the approved neutral plate.
  g.save();g.beginPath();g.moveTo(40,24);g.lineTo(216,24);g.lineTo(233,41);
  g.lineTo(233,215);g.lineTo(215,233);g.lineTo(41,233);g.lineTo(23,215);g.lineTo(23,41);g.closePath();g.clip();
  g.drawImage(XART.get(rage?baseKey:sourceKey),0,0,256,256);g.restore();
 }
 if(talk&&em!=='talk-closed'){
  // Align the generated lips to the supplied neutral face; keep the eyes/nose fixed.
  g.drawImage(XART.get(sourceKey),99,143,45,34,92,140,45,34);
 }else if(rage){
  // The shouting sequence likewise keeps one head, costume and frame anchor.
  g.drawImage(XART.get(sourceKey),55,65,22,21,110,130,44,42);
 }
 c.complete=true;c.naturalWidth=c.naturalHeight=256;CP5.cache.set(id,c);return c;
}
const CP5_TOUCH=XART._touch;
XART._touch=function(k){
 const m=/^(comm_cole_|port_cf_cole_|port_cole_)(.+)$/.exec(k||'');
 if(m||k==='face_cole'){
  let em=m?m[2]:'idle';if(em==='smile')em='happy';if(em==='alert')em='crash';
  if(CP5.poses.includes(em))return cp5Cell(em,!!m&&m[1]==='comm_cole_',false);
 }
 const rage=/^fb2_cole_rage_([0-2])$/.exec(k||'');if(rage)return cp5Cell(rage[1],false,true);
 return CP5_TOUCH.apply(this,arguments);
};
for(const em of ['idle','talk-closed','talk-small','talk-medium','talk-wide','talk-o'])XART.rdy('cp5_raw_'+em);
