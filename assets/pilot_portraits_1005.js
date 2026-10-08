'use strict';
/* All Fury pilots: retain each approved complete idle bezel and head; speech
   replaces only authored lip pixels. Cole retains his fixed speech/shouting reels. */
const PP5={cache:new Map(),poses:['idle','happy','laugh','anger','sad','crash','victory',
 'talk-closed','talk-small','talk-medium','talk-wide','talk-o'],
 mouths:{axel:[91,133,48,43],decker:[98,146,42,38],falva:[106,132,45,34],
 freezer:[84,146,47,43],juggernaut:[91,127,47,46],lizzie:[110,109,38,37],maverick:[89,133,46,38],yuri:[95,145,53,45]}};
for(const p of Object.keys(PP5.mouths).filter(p=>p!=='lizzie'))for(const em of PP5.poses)
 XART._src['pp5_raw_'+p+'_'+em]='assets/game/pilots_0922/portraits/'+p+'-'+em+'.png';
function pp5Cell(p,em,comm){
 const id=p+':'+em+':'+comm;if(PP5.cache.has(id))return PP5.cache.get(id);
 const idle='pp5_raw_'+p+'_idle',raw='pp5_raw_'+p+'_'+em;
 let base,source;
 if(p==='lizzie'){base=mapgLizzieCell('idle',false);source=mapgLizzieCell(em,false);if(!base||!source)return null;}
 else{if(!XART.rdy(idle)||!XART.rdy(raw))return null;base=XART.get(idle);source=XART.get(raw);}
 const w=base.naturalWidth||base.width,h=base.naturalHeight||base.height;
 const c=document.createElement('canvas');c.width=w;c.height=h;const g=c.getContext('2d');g.imageSmoothingEnabled=false;
 if(comm){g.translate(w,0);g.scale(-1,1);}g.drawImage(base,0,0,w,h);
 if(/^talk-/.test(em)){
  if(em!=='talk-closed'){const r=PP5.mouths[p];g.drawImage(source,...r,...r);}
 }else if(em!=='idle'){
  // Pose/emotion art lives inside the original full enclosure; rails never change.
  g.save();g.beginPath();g.moveTo(41,24);g.lineTo(w-41,24);g.lineTo(w-23,42);
  g.lineTo(w-23,h-42);g.lineTo(w-41,h-23);g.lineTo(41,h-23);g.lineTo(23,h-42);g.lineTo(23,42);g.closePath();g.clip();
  g.drawImage(source,0,0,w,h);g.restore();
 }
 c.complete=true;c.naturalWidth=w;c.naturalHeight=h;PP5.cache.set(id,c);return c;
}
const PP5_TOUCH=XART._touch;
XART._touch=function(k){
 const m=/^(comm_|port_cf_|port_)(axel|decker|falva|freezer|juggernaut|lizzie|maverick|yuri)_(.+)$/.exec(k||'');
 const face=/^face_(axel|decker|falva|freezer|juggernaut|lizzie|maverick|yuri)$/.exec(k||'');
 const yuri=/^yuri_v2_(.+)$/.exec(k||'');
 if(m||face||yuri||k==='yuri_avatar'){
  const p=m?m[2]:face?face[1]:'yuri';let em=m?m[3]:yuri?yuri[1]:'idle';
  if(em==='smile')em='happy';if(em==='alert')em='crash';if(em==='talk')em='talk-closed';
  if(PP5.poses.includes(em))return pp5Cell(p,em,!!m&&m[1]==='comm_');
 }
 return PP5_TOUCH.apply(this,arguments);
};
for(const p of Object.keys(PP5.mouths).filter(p=>p!=='lizzie'))for(const em of ['idle'])XART.rdy('pp5_raw_'+p+'_'+em);
