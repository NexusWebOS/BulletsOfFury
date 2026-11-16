"use strict";
/* Shared talking cockpit portraits. Native dialogue clocks and letter audio own speech. */
const CP15={base:{keys:d1110Keys,face:cm3DrawFace,visual:d1110Visual,cover:sl14Cover,strip:fixc14Image,plate:d1110Plate,load:stageLoadBegin},active:null,last:null,draws:{},history:[]};
for(const a of [...Object.values(CP15_ART.banks),...Object.values(CP15_ART.minis)])XART._src[a.key]=a.path;
for(const p of CP15_ART.pilots)for(const room of ['cockpit-sky','cockpit-space','cockpit-tunnel'])for(const n of [48,64,84,96])FP5_ART.banks['mini-'+room+'-'+p+'-'+n]={...CP15_ART.minis[p+'-'+n],room};
function cp15Context(){if(CP15.active)return CP15.active;const s=state===GS.CAMPAIGNINTRO?campaignIntro?.d1110:state===GS.VICTORY?D1110.ending?.scene:BOFCinematicDirector.current;return s?{s,b:s.beats[s.i]}:null;}
function cp15Pose(p,b,s,time=0){
 const text=String(b?.text||''),budget=s?Math.min(text.length,s.shown||0):Math.min(text.length,Math.floor(Math.max(0,time-(b?.cm3?.readAt||0))*30));
 if(!D1110.static&&b?.who===p.toUpperCase()&&budget>0&&budget<text.length){
  const c=text[budget-1].toLowerCase();if(/[mbp\s.,!?;:'-]/.test(c))return 0;if(c==='a')return 1;if(/[eiy]/.test(c))return 2;if(/[owq]/.test(c))return 3;if(c==='u')return 4;if(/[fv]/.test(c))return 5;return 6;
 }
 const a=CP15_ART.banks[p],clock=s?.age??time,offset=CP15_ART.pilots.indexOf(p)*.37;
 return a.blink&&!D1110.static&&((clock+offset)%4.7)>4.53?7:0;
}
function cp15Draw(p,box,b=cp15Context()?.b,s=cp15Context()?.s,time=s?.t||0){
 const a=CP15_ART.banks[p];if(!a||!XART.rdy(a.key))return false;
 const f=cp15Pose(p,b,s,time),im=XART.get(a.key),[x,y,w,h]=box,k=Math.max(w/a.w,h/a.h),dw=a.w*k,dh=a.h*k;
 // Pin the cabin's top to the visible panel so comic zooms cannot crop hair.
 const dx=Math.round(x+(w-dw)/2),dy=Math.round(Math.max(0,y));
 ctx.save();ctx.beginPath();ctx.rect(x,y,w,h);ctx.clip();ctx.imageSmoothingEnabled=false;
 ctx.drawImage(im,f%a.cols*a.w,Math.floor(f/a.cols)*a.h,a.w,a.h,dx,dy,Math.round(dw),Math.round(dh));ctx.restore();
 const q={pilot:p,frame:f,key:a.key,box:[...box],image:[dx,dy,Math.round(dw),Math.round(dh)],speaking:b?.who===p.toUpperCase()&&(s?.shown||0)<String(b?.text||'').length,family:'talking-cockpit',artFamily:a.family||'legacy-1114',assetPath:a.path,assetSha256:a.sha256,fixedCamera:true};
 CP15.last=q;CP15.draws[p]=(CP15.draws[p]||0)+1;if(CP15.history.at(-1)?.pilot!==p||CP15.history.at(-1)?.frame!==f){CP15.history.push(q);if(CP15.history.length>600)CP15.history.shift();}return q;
}
d1110Visual=function(b,s){const before=CP15.active;CP15.active={b,s};try{return CP15.base.visual.apply(this,arguments);}finally{CP15.active=before;}};
cm3DrawFace=function(p,box,b,time,view){const room=b.fpLocations?.[p];if(room?.startsWith('cockpit-')){const q=cp15Draw(p,box,b,cp15Context()?.s,time);return q?{...q,room,channel:'radio',zoom:view.zoom}:{pilot:p,key:CP15_ART.banks[p]?.key,room,channel:'radio',family:'talking-cockpit',loading:true};}return CP15.base.face.apply(this,arguments);};
function cp15PilotKey(key){return /^s113_cockpit-(.+)$/.exec(key)?.[1];}
sl14Cover=function(key,box){const p=cp15PilotKey(key);if(p&&cp15Draw(p,box))return;return CP15.base.cover.apply(this,arguments);};
fixc14Image=function(key,box){const p=cp15PilotKey(key);if(p&&cp15Draw(p,box))return;return CP15.base.strip.apply(this,arguments);};
d1110Plate=function(b,time){if(b.art==='cockpit'&&cp15Draw(run.pilot,[0,0,912,D1110.visualH||392],b,cp15Context()?.s,time))return;return CP15.base.plate.apply(this,arguments);};
d1110Keys=function(rows,p=run.pilot){const keys=CP15.base.keys.apply(this,arguments),needed=new Set();
 for(const b of rows){for(const pk of b.people||[])if(b.fpLocations?.[pk]?.startsWith('cockpit-'))needed.add(pk);if(b.service14||b.fury14||b.art==='cockpit')for(const pk of d1110Active(p))needed.add(pk);}
 for(const pk of needed)if(CP15_ART.banks[pk])keys.push(CP15_ART.banks[pk].key);return [...new Set(keys)];};
stageLoadBegin=function(n,keys){const more=Object.values(CP15_ART.minis).map(a=>a.key);for(const p of d1110Active())if(CP15_ART.banks[p])more.push(CP15_ART.banks[p].key);return CP15.base.load.call(this,n,[...(keys||[]),...more]);};
CP15.pose=cp15Pose;CP15.draw=cp15Draw;CP15.preview=(p='cole')=>D1110.preview('post-2',p);window.BOF_COCKPIT_TALK_1114=CP15;
