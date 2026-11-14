'use strict';
/* Guided comic reading: authored raster zoom/fade frames, integer camera motion.
   Caption readability and all native callbacks, rewards and save owners persist. */
const CM3={version:1,last:null,base:{rows:c16Rows,keys:d1110Keys,visual:d1110Visual,step:d1110Step,mouth:c16Mouth},events:[]};
for(const a of Object.values(CM3_ART.banks))XART._src[a.key]=a.path+'?v='+a.sha256.slice(0,12);
function cm3Ease(v){v=clamp(v,0,1);return 1-(1-v)*(1-v)*(1-v);}
function cm3Blit(name,frame,x,y){const a=CM3_ART.banks[name];if(!a||!XART.rdy(a.key))return false;frame=clamp(Math.floor(frame),0,a.frames-1);ctx.drawImage(XART.get(a.key),frame%a.cols*a.w,Math.floor(frame/a.cols)*a.h,a.w,a.h,Math.round(x),Math.round(y),a.w,a.h);return true;}
function cm3Cover(box,frame){if(frame>=8)return;const[x,y,w,h]=box;c16Clip(box,()=>{for(let yy=y;yy<y+h;yy+=350)for(let xx=x;xx<x+w;xx+=512)cm3Blit('ink-fade',frame,xx,yy);});}
function cm3Fade(t,start,end,from=0,to=8){return Math.round(from+(to-from)*clamp((t-start)/Math.max(.01,end-start),0,1));}
c16Rows=function(id,p=run.pilot,route=s113Route()){
 const rows=CM3.base.rows(id,p,route);let group=-1,lastKey='',ordered=null,page=0;
 rows.forEach((b,i)=>{
  const key=b.kind==='dialogue'?'talk:'+b.people.slice().sort().join('|'):'picture:'+i;
  const fresh=key!==lastKey;if(fresh){group++;lastKey=key;page=b.page;const speaker=b.who.toLowerCase();ordered=b.people.slice();if(b.kind==='dialogue'&&ordered.includes(speaker))ordered=[speaker,...ordered.filter(pk=>pk!==speaker)];}
  if(b.kind==='dialogue'){b.page=page;b.people=ordered.slice();}
  const readAt=fresh?.42:.26;b.cm3={group:id+':'+group,readAt,newStrip:fresh,baseDuration:b.duration};b.duration+=readAt+.14;
 });return rows;
};
d1110Keys=function(rows,p=run.pilot){const keys=CM3.base.keys(rows,p);for(const b of rows){if(!b.cm3)continue;keys.push(CM3_ART.banks['strip-'+b.page].key,CM3_ART.banks['caption-'+b.page].key,CM3_ART.banks['ink-fade'].key);for(const pk of b.people||[])keys.push(CM3_ART.banks['talk-zoom-'+pk].key,CM3_ART.banks['backdrop-zoom-'+pk].key);}return[...new Set(keys)];};
function cm3Active(b){if(b.kind==='dialogue')return Math.max(0,b.people.indexOf(b.who.toLowerCase()));return 0;}
function cm3View(b,s,index,time,snapshot=false){
 const previous=s.beats[index-1],same=previous?.cm3?.group===b.cm3.group;
 const known=new Set();for(let i=index-1;i>=0&&s.beats[i]?.cm3?.group===b.cm3.group;i--)known.add(cm3Active(s.beats[i]));
 let active=cm3Active(b),old=same?cm3Active(previous):active,zoom=0;
 if(b.kind==='dialogue')zoom=D1110.static||snapshot?6:same?Math.round(6-2*Math.sin(Math.PI*clamp(time/.7,0,1))):Math.round(6*cm3Ease((time-.36)/.68));
 const factor=CM3_ART.zooms[zoom],panels=C16_ART.pages[b.page].panels;
 let reaction=b.kind!=='dialogue'&&panels.length>1&&C16_ART.pilots.includes(b.who.toLowerCase())&&!!b.text;
 if(reaction){active=time<.62&&!snapshot&&!D1110.static?0:1;old=0;}
 const progress=D1110.static||snapshot?1:cm3Ease(reaction?(time-.62)/.63:time/.55);
 function camera(which){const q=panels[Math.min(which,panels.length-1)],anchor=panels.length===1?456:which===0?300:600;return(q[0]+q[2]/2)*factor-anchor;}
 const cameraX=Math.round(camera(old)+(camera(active)-camera(old))*progress),cameraY=Math.round(-21+57*zoom/6);
 return{known,active,old,zoom,factor,cameraX,cameraY,same,reaction,snapshot};
}
function cm3DrawFace(pk,box,b,time,view){const a=CM3_ART.banks['talk-zoom-'+pk],bg=CM3_ART.banks['backdrop-zoom-'+pk],z=view.zoom,pose=time<b.cm3.readAt?0:CM3.base.mouth(b,{t:time-b.cm3.readAt},pk),[x,y,w,h]=box;const xx=x+Math.round((w-a.sizes[z])/2),yy=y+h-a.baselines[z]+a.bleeds[z];cm3Blit('backdrop-zoom-'+pk,z,x+Math.round((w-bg.sizes[z][0])/2),y+Math.round((h-bg.sizes[z][1])/2));cm3Blit('talk-zoom-'+pk,z*7+pose,xx,yy);return{pilot:pk,frame:pose,zoom:z,origin:[xx,yy],baseline:a.baselines[z],bottom:y+h,bleed:a.bleeds[z]};}
function cm3Strip(b,s,index,time,offset,snapshot=false){
 const v=cm3View(b,s,index,time,snapshot),page=C16_ART.pages[b.page],boxes=page.panels.map(q=>[Math.round(q[0]*v.factor)-v.cameraX,Math.round(q[1]*v.factor)-v.cameraY+offset,Math.round(q[2]*v.factor),Math.round(q[3]*v.factor)]),faces=[],visible=[];
 boxes.forEach((box,i)=>{
  let show=false,fade=8;
  if(b.kind==='dialogue'){
   show=i===v.active||v.known.has(i);
   if(show&&!snapshot&&!D1110.static){if(i===v.active)fade=v.old===v.active&&v.same?8:cm3Fade(time,.10,.46,v.known.has(i)?4:0,8);else fade=cm3Fade(time,0,.3,8,4);}
   else if(show&&i!==v.active)fade=4;
  }else if(i===0){show=true;fade=snapshot||D1110.static?8:cm3Fade(time,.10,.46);}
  else if(v.reaction){show=time>=.62||snapshot||D1110.static;fade=snapshot||D1110.static?8:cm3Fade(time,.62,1.04);}
  if(!show||fade===0)return;visible.push(i);
  c16Clip(box,()=>{
   if(b.kind==='dialogue'){const pk=b.people[i%b.people.length];faces.push(cm3DrawFace(pk,box,b,time,v));}
   else if(i===0)c16Illustration({...b,duration:b.cm3.baseDuration},{...s,t:Math.max(0,time-b.cm3.readAt)},box);
   else{const pk=b.who.toLowerCase();faces.push(cm3DrawFace(pk,box,b,time,v));}
   cm3Cover(box,fade);
  });
 });
 cm3Blit('strip-'+b.page,v.zoom,-v.cameraX,-v.cameraY+offset);
 return{...v,visiblePanels:visible,faces,boxes};
}
d1110Visual=function(b,s){
 if(!b.cm3){const r=CM3.base.visual.apply(this,arguments),previous=s.beats[s.i-1],continuous=b.cbFinisher&&s.i>0||b.battle&&previous?.battle===b.battle;if(b.d1110&&!continuous&&s.t<.25){ctx.save();ctx.setTransform(SS,0,0,SS,0,0);cm3Cover([0,0,912,512],cm3Fade(s.t,.02,.25));ctx.restore();}return r;}
 const previous=s.beats[s.i-1],fresh=!previous||previous.cm3?.group!==b.cm3.group,staticView=D1110.static,scroll=fresh&&!staticView?Math.round(350*(1-cm3Ease(s.t/.58))):0;
 ctx.save();ctx.setTransform(SS,0,0,SS,0,0);ctx.imageSmoothingEnabled=false;ctx.fillStyle='#000';ctx.fillRect(0,0,912,512);
 let result;
 c16Clip([0,0,912,350],()=>{
  if(fresh&&previous?.cm3&&scroll>0){cm3Strip(previous,s,s.i-1,previous.duration-.2,scroll-350,true);cm3Cover([0,0,912,scroll],cm3Fade(s.t,0,.34,8,0));}
  c16Clip([0,scroll,912,350-scroll],()=>{result=cm3Strip(b,s,s.i,s.t,scroll);if(fresh&&!staticView)cm3Cover([0,scroll,912,350-scroll],cm3Fade(s.t,.06,.45));});
 });
 cm3Blit('caption-'+b.page,0,37,350);const page=C16_ART.pages[b.page],speaker=b.who.toLowerCase(),title=b.who==='CAPTION'?'BULLETS OF FURY':b.who==='SYSTEM'?'':b.who;
 c16Blit('name-'+b.page+'-'+speaker,0,37+page.name[0],350+page.name[1]-322);
 msgFaceUse('dialogue');if(title)msgText(title,37+page.name[0]+page.name[2]/2,350+page.name[1]-322+page.name[3]/2,15,'#090b13',1,1,.04);
 if(b.text)msgDrawBlock({text:b.text,x:37+page.body[0]+9,y:350+page.body[1]-322+2,w:page.body[2]-18,h:page.body[3]-4,maxH:23,minH:18,lineMul:1.23,spacing:.04,color:'#fff0cf',budget:s.shown,valign:'middle'});
 if(!staticView)cm3Cover([37,350,838,148],cm3Fade(s.t,.10,b.cm3.readAt+.15));
 if(s.t>b.cm3.readAt+.2||staticView)controlHintRow([['pad_a',s.shown<b.text.length?'READ':'NEXT'],['pad_start','SKIP']],505,456,840,10);msgFaceUse(null);
 if(!s.beats[s.i+1]&&!staticView&&s.t>b.duration-.18)cm3Cover([0,0,912,512],cm3Fade(s.t,b.duration-.18,b.duration,8,0));
 ctx.restore();CM3.last={id:s.id,shot:b.id,who:b.who,text:b.text,pilot:run.pilot,coOp:d1110Active(),page:b.page,kind:b.kind,bank:b.bank,frame:c16Frame(b,{t:Math.max(0,s.t-b.cm3.readAt)}),time:s.t,motion3:true,readAt:b.cm3.readAt,scroll,...result};C16.last=D1110.last=CM3.last;
};
d1110Step=function(s,dt,onAdvance,onFinish){const b=s.beats[s.i];if(!b?.cm3)return CM3.base.step.apply(this,arguments);if(D1110.paused)return;
 s.age+=dt;s.d1110Wait=(s.d1110Wait||0)+dt;if(s.age>.15&&Input.menuStart()){onFinish();return;}
 const click=Input.mouse.down&&!s.md;s.md=!!Input.mouse.down;
 if(s.age>.15&&(Input.menuConfirm()||click)){if(s.shown<b.text.length){s.shown=b.text.length;s.t=Math.max(s.t,.75,b.cm3.readAt+b.text.length/30);}else onAdvance();return;}
 if(!d1110Ready(s.d1110Keys||[])&&s.d1110Wait<15)return;
 const before=s.shown,previous=s.t;s.t+=Math.max(0,dt);s.shown=Math.max(s.shown,Math.min(b.text.length,Math.floor(Math.max(0,s.t-b.cm3.readAt)*30)));dialogueLetterTicks(b.text,before,s.shown);
 if(b.cue)d1110Cue(s,b,b.cue,(b.cueAt??.08)+b.cm3.readAt,previous);for(const q of b.c16Cues||[])d1110Cue(s,b,q.name,q.at+b.cm3.readAt,previous);
 if(s.t>=b.duration){s.shown=b.text.length;onAdvance();}
};
C16.rows=c16Rows;CM3.rows=c16Rows;C16.motion3=CM3;window.BOF_COMIC_MOTION_1111=CM3;
