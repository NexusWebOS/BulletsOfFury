'use strict';
/* A second authored pilot family for face-to-face conversations. CM3 retains
   its reveal/pan/scroll/timing owner. Radio pilots retain their flight gear. */
const FP5={version:1,revision:2,last:null,base:{rows:c16Rows,keys:d1110Keys,face:cm3DrawFace,dlg:dlgBox},defaults:{cole:'conference',axel:'hangar',freezer:'hangar',yuri:'conference',maverick:'hangar',falva:'hangar',lizzie:'hangar',decker:'workshop',juggernaut:'lounge'}};
for(const a of Object.values(FP5_ART.banks))XART._src[a.key]=a.path+'?v='+a.sha256.slice(0,12);
function fp5Room(id,b,pk,p,index){
 const tech=d1110Tech(p),room=pk===tech?(pk==='decker'?'workshop':'conference'):null;
 const cockpit=/warp|arrival-9|post-9|sting/.test(id)?'cockpit-space':/arrival-7|post-7/.test(id)?'cockpit-tunnel':'cockpit-sky';
 // After the HQ evacuation, the technician is flying with the team too.
 // Keep every airborne speaker in the current shared cockpit art family.
 if(/^(post-[6789]|arrival-[79]|warp-5-9|sting)$/.test(id))return cockpit;
 if(id==='opening'){
  const n=Number(String(b.id).split('-').at(-1));
  if(n>=17)return room||cockpit;
  if(n>=10)return pk===tech&&pk==='decker'?'workshop':'hangar';
  return ['cole','decker'].includes(pk)?'workshop':'hangar';
 }
 if(id==='post-3')return index<13?'conference':'workshop';
 if(id==='post-4')return 'hangar';
 if(id==='post-5'){
  if(b.id==='B501'||b.id==='B507')return room||'cockpit-sky';
  if(['POST5-02','POST5-03'].includes(b.id))return 'hangar';
  if(b.id==='B505'||/^POST5-1[456]$/.test(b.id))return 'conference';
  return 'workshop';
 }
 if(id==='ending')return index<5?(room||'cockpit-sky'):index>=15?'lounge':'conference';
 return room||cockpit;
}
c16Rows=function(id,p=run.pilot,route=s113Route()){
 const rows=FP5.base.rows.apply(this,arguments);
 rows.forEach((b,index)=>{b.fpScene=id;b.fpPilot=p;b.fpLocations={};for(const pk of b.people||[])b.fpLocations[pk]=fp5Room(id,b,pk,p,index);});return rows;
};
d1110Keys=function(rows,p=run.pilot){
 const keys=FP5.base.keys.apply(this,arguments).filter(k=>!/^cm3_(talk-zoom-|backdrop-zoom-)/.test(k));
 for(const b of rows)for(const pk of b.people||[]){
  const room=b.fpLocations?.[pk];if(!room)continue;
  keys.push(FP5_ART.banks['backdrop-'+room].key);
   keys.push(FP5_ART.banks['talk-zoom-'+pk].key);
   for(const n of [48,64,84,96])keys.push(FP5_ART.banks['mini-'+room+'-'+pk+'-'+n].key);
 }
 return [...new Set(keys)];
};
function fp5Blit(name,frame,x,y){
 const a=FP5_ART.banks[name];if(!a||!XART.rdy(a.key))return false;
 frame=clamp(Math.floor(frame),0,a.frames-1);ctx.drawImage(XART.get(a.key),frame%a.cols*a.w,Math.floor(frame/a.cols)*a.h,a.w,a.h,Math.round(x),Math.round(y),a.w,a.h);return true;
}
cm3DrawFace=function(pk,box,b,time,view){
 const room=b.fpLocations?.[pk];if(!room)return FP5.base.face.apply(this,arguments);
 const radio=room.startsWith('cockpit-'),a=FP5_ART.banks['talk-zoom-'+pk],bg=FP5_ART.banks['backdrop-'+room];
 if(!XART.rdy(a.key)||!XART.rdy(bg.key))return FP5.base.face.apply(this,arguments);
 const z=view.zoom,pose=time<b.cm3.readAt?0:CM3.base.mouth(b,{t:time-b.cm3.readAt},pk),[x,y,w,h]=box;
 const xx=x+Math.round((w-a.sizes[z])/2),yy=y+h-a.baselines[z]+a.bleeds[z];
 fp5Blit('backdrop-'+room,z,x+Math.round((w-bg.sizes[z][0])/2),y+Math.round((h-bg.sizes[z][1])/2));
 fp5Blit('talk-zoom-'+pk,z*7+pose,xx,yy);
 const result={pilot:pk,frame:pose,zoom:z,origin:[xx,yy],baseline:a.baselines[z],bottom:y+h,bleed:a.bleeds[z],room,channel:radio?'radio':'in-person',family:'front-headset-free'};
 FP5.last=result;return result;
};
function fp5Current(){return state===GS.CAMPAIGNINTRO?campaignIntro?.d1110:state===GS.VICTORY?D1110.ending?.scene:BOFCinematicDirector.current;}
function fp5BoxRoom(o,pk){
 if(o.frontPortrait===false)return null;
 if(FP5_ART.rooms.includes(o.location))return o.location;
 const s=fp5Current(),b=s?.beats?.[s.i],place=b?.fpLocations?.[pk];
 if(place)return place;
 if(state===GS.PLAY||state===GS.LAUNCH||state===GS.COCKPIT)return pk===d1110Tech(run.pilot)?(pk==='decker'?'workshop':'conference'):run.stage===5||run.stage===9?'cockpit-space':run.stage===7||run.stage===8?'cockpit-tunnel':'cockpit-sky';
 return FP5.defaults[pk];
}
function fp5Dialogue(o){
 const pk=cx4Pilot(o||{});if(!pk||!cx4Eligible(o))return FP5.base.dlg.apply(this,arguments);
 const room=fp5BoxRoom(o,pk);if(!room)return FP5.base.dlg.apply(this,arguments);
 const replacements=[48,64,84,96].map(n=>['face-'+pk+'-'+n,FP5_ART.banks['mini-'+room+'-'+pk+'-'+n]]);
 if(!replacements.every(([,a])=>XART.rdy(a.key)))return FP5.base.dlg.apply(this,arguments);
 const saved=replacements.map(([key])=>[key,CX4_ART.banks[key]]);
 try{for(const[key,a]of replacements)CX4_ART.banks[key]=a;return FP5.base.dlg.apply(this,arguments);}
 finally{for(const[key,a]of saved)CX4_ART.banks[key]=a;}
}
Object.assign(fp5Dialogue,dlgBox);dlgBox=cx4Draw=fp5Dialogue;
window.BOF_CINEMATIC_DIALOGUE_1111.draw=fp5Dialogue;
C16.rows=c16Rows;CM3.rows=c16Rows;FP5.rows=c16Rows;FP5.resolve=fp5Room;
C16.frontPilots=CM3.frontPilots=BOFCinematicDirector.frontPilots=FP5;
window.BOF_FRONT_PILOTS_1111=FP5;
