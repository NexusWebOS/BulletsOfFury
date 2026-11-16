"use strict";
/* Internal relay restoration, native top-down departure and cockpit-reference Cole. */
const SL14={base:{rows:c16Rows,keys:d1110Keys,visual:d1110Visual,step:d1110Step,start:BOFCinematicDirector.start,map:drawStageSelect},last:null,mapFade:0,events:[]};
for(const [family,name,a]of SL14_ART.bindings){({FP5:FP5_ART,CM3:CM3_ART,C16:C16_ART,CX4:CX4_ART})[family].banks[name]=a;XART._src[a.key]=a.path;}
const SL14_SOURCE=[
 ['SL2-01','PILOT','$techName, what am I looking at?','radio'],
 ['SL2-02','TECH',"A service data-link. It's restoring power to our internal relay systems.",'radio'],
 ['SL2-03','TECH',"Think of it like a LAN, but wireless for all of us. Our squad channels are coming back.",'radio'],
 ['SL2-04','PILOT',"You're a genius, $techName.",'radio'],
 ['SL2-05','TECH',"Hey, I'm just telling you what I know from what we have left.",'radio'],
 ['SL2-06','TECH',"I'm raising your systems' heat levels. You should be able to toggle up to maximum efficiency.",'heat'],
 ['SL2-07','TECH',"You'll find an extra surprise for those icy units if they give you any trouble.",'heat'],
 ['SL2-08','TECH','Get out of there. The ground is moving.','alert'],
 ['SL2-09','SYSTEM','','takeoff',4.6],
 ['SL2-10','SYSTEM','','fade',1.2]
];
C16_STORY.scenes['post-2']=SL14_SOURCE.map(([id,who,text,mode,duration])=>({id,who,text,service14:mode,kind:'dialogue',people:['$pilot','$tech'],style:0,duration:duration||Math.max(4.2,text.length/30+2.2),...(id==='SL2-06'?{cue:'bossWeaponCharge',cueAt:.55}:{}),...(id==='SL2-07'?{upgrade:2}:{}),...(mode==='takeoff'?{cue:'jetDash',cueAt:.18}:{})}));
c16Rows=function(id,p=run.pilot,route=s113Route()){
 const rows=SL14.base.rows.apply(this,arguments);if(id!=='post-2')return rows;
 for(const b of rows){
  if(b.id==='SL2-01'&&p==='decker')b.text='Cole, what am I looking at?';
  if(b.id==='SL2-07'&&p==='maverick')b.text="Your homing lasers stay as they are. I've raised the squad's heat limits for those icy units.";
  b.duration=b.service14==='fade'?1.2:b.service14==='takeoff'?4.6:Math.max(b.duration,b.text.length/30+2.3+(b.cm3?.readAt||0));
  b.speechEnd=b.text.length/30+.12;b.cm3.baseDuration=b.duration;
 }return rows;
};
C16.rows=CM3.rows=FP5.rows=c16Rows;
d1110Keys=function(rows,p=run.pilot){const keys=SL14.base.keys.apply(this,arguments);if(rows.some(b=>b.service14)){
 for(const pk of d1110Active(p))for(const key of [S113_ART.banks['cockpit-'+pk]?.key,'ship_'+pk,'ship_'+pk+'_g1','ship_'+pk+'_g2'])if(key)keys.push(key);
 keys.push(CM3_ART.banks['caption-0'].key,...ls112Keys(2));for(let i=0;i<4;i++)keys.push('fchg_'+i);
 }return [...new Set(keys)];};
function sl14Cover(key,box){if(!XART.rdy(key))return;const im=XART.get(key),[x,y,w,h]=box,k=Math.max(w/im.width,h/im.height);ctx.drawImage(im,Math.round(x+(w-im.width*k)/2),Math.round(y+(h-im.height*k)/2),Math.round(im.width*k),Math.round(im.height*k));}
function sl14Frame(box){const[x,y,w,h]=box;ctx.strokeStyle='#09090c';ctx.lineWidth=8;ctx.strokeRect(x,y,w,h);ctx.strokeStyle='#efddb4';ctx.lineWidth=3;ctx.strokeRect(x-4,y-4,w+8,h+8);}
function sl14Radio(b,s){
 const pilot=run.pilot,tech=d1110Tech(pilot),left=[12,12,552,354],right=[580,12,320,354];
 c16Clip(left,()=>sl14Cover(S113_ART.banks['cockpit-'+pilot].key,left));
 c16Clip(right,()=>cm3DrawFace(tech,right,b,s.t,{zoom:0}));
 sl14Frame(left);sl14Frame(right);
 SL14.last={mode:'radio',pilot,tech,identityKey:S113_ART.banks['cockpit-'+pilot].key,wholeCockpit:true};
}
function sl14HeatAge(s){let age=s.t;for(let i=s.i-1;i>=0&&s.beats[i].service14!=='radio';i--)age+=s.beats[i].duration;return age;}
function sl14TopDown(b,s){
 const box=[12,12,888,354],mode=b.service14,age=sl14HeatAge(s),heat=clamp(age/6,0,1),u=clamp((s.t-.2)/3.8,0,1),e=u*u*(3-2*u);
 const afterHeat=mode!=='heat',settle=mode==='alert'?clamp(s.t/1.3,0,1):afterHeat?1:0;
 const requestedZoom=afterHeat?lerp(1.9,1.18,settle):lerp(1.18,1.9,clamp(age/4,0,1));
 const world={x:Number.isFinite(player.x)?player.x:worldWidth()/2,y:Number.isFinite(player.y)?player.y:VH*.78},actors=d1110Active();
 // Keep the entire camera window inside the finite stage plate. A four-pixel
 // source inset also covers rounding at fractional cinematic zoom levels.
 const terrainW=Math.min(worldWidth(),LS112_ART.levels['2'].w),terrainH=VH,inset=4,anchor={x:456,y:184};
 const zoom=Math.max(requestedZoom,box[2]/(terrainW-inset*2),box[3]/(terrainH-inset*2));
 const left=(anchor.x-box[0])/zoom,right=(box[0]+box[2]-anchor.x)/zoom,top=(anchor.y-box[1])/zoom,bottom=(box[1]+box[3]-anchor.y)/zoom;
 const endShipY=box[1]+box[3]-64*zoom*.5-18-(actors.length-1)*12;
 const wantedY=lerp(world.y,world.y-(endShipY-anchor.y)/zoom,settle);
 const viewX=clamp(world.x,left+inset,terrainW-right-inset),viewY=clamp(wantedY,top+inset,terrainH-bottom-inset);
 const shipX=anchor.x+(world.x-viewX)*zoom,shipY=anchor.y+(world.y-viewY)*zoom;
 const framing={requestedZoom,zoom,viewX,viewY,terrainW,terrainH,inset,visible:{left:viewX-left,right:viewX+right,top:viewY-top,bottom:viewY+bottom},box};
 c16Clip(box,()=>{
  ctx.save();ctx.translate(anchor.x-viewX*zoom,anchor.y-viewY*zoom);ctx.scale(zoom,zoom);drawBG(0);ctx.restore();
  for(let i=0;i<actors.length;i++){
   const pk=actors[i],x=shipX+(i-(actors.length-1)/2)*94,y=(mode==='takeoff'?lerp(shipY,-160,e):mode==='fade'?-170:shipY)+i*12;
   const size=Math.round(64*zoom*(mode==='takeoff'?1+.12*Math.sin(Math.PI*u):1)),burn=mode==='takeoff'||mode==='fade'?1:mode==='alert'?.7:.28+.18*heat;
   if(mode==='heat'){
    const key='fchg_'+Math.min(3,1+Math.floor(heat*2)),im=xartPalette(key,'#ff9835')||XART.get(key),w=Math.round(size*1.6),h=Math.round(size*1.45);
    if(im){ctx.save();ctx.globalAlpha=.45+.3*heat;ctx.drawImage(im,x-w/2,y-h/2,w,h);ctx.restore();}
   }
   pt11OpeningShip(pk,age,x,y,size,burn);
   SL14.last={mode,pilot:run.pilot,actors,world,zoom,heat,ship:{x,y,size,burn},topDown:true,backgroundStage:run.stage,framing};
  }
 });sl14Frame(box);
}
function sl14Caption(b,s){
 if(!b.text)return;const a=CM3_ART.banks['caption-0'];if(XART.rdy(a.key))ctx.drawImage(XART.get(a.key),31,382,850,116);
 msgFaceUse('dialogue');msgText(b.who,155,397,14,'#16131a',1,1);
 msgDrawBlock({text:b.text,budget:s.shown,x:75,y:422,w:762,h:56,maxH:18,minH:16,lineMul:1.25,color:'#fff1d3',valign:'middle'});msgFaceUse(null);
}
d1110Visual=function(b,s){if(!b.service14)return SL14.base.visual.apply(this,arguments);
 ctx.save();ctx.setTransform(SS,0,0,SS,0,0);ctx.imageSmoothingEnabled=false;ctx.fillStyle='#080d14';ctx.fillRect(0,0,912,512);
 if(b.service14==='radio')sl14Radio(b,s);else sl14TopDown(b,s);sl14Caption(b,s);
 if(b.service14==='fade'){ctx.fillStyle='rgba(0,0,0,'+clamp(s.t/(b.duration-.1),0,1)+')';ctx.fillRect(0,0,912,512);}
 if(s.i===0&&s.t<.4){ctx.fillStyle='rgba(0,0,0,'+(1-s.t/.4)+')';ctx.fillRect(0,0,912,512);}
 msgFaceUse('dialogue');controlHintRow([['pad_a',s.shown<b.text.length?'READ':'NEXT'],['pad_start','SKIP']],505,723,887,9);msgFaceUse(null);
 SL14.last={...SL14.last,id:s.id,shot:b.id,text:b.text,time:s.t};D1110.last=SL14.last;ctx.restore();
};
d1110Step=function(s,dt,onAdvance,onFinish){if(s.beats[s.i]?.service14&&!D1110.paused)efxClock+=Math.max(0,Math.min(.1,dt||0));return SL14.base.step.apply(this,arguments);};
BOFCinematicDirector.start=function(n,done){if(n!==2||run.mode!=='campaign')return SL14.base.start.apply(this,arguments);
 return SL14.base.start.call(this,n,()=>{SL14.events.push({event:'departure-complete',pilot:run.pilot});done?.();SL14.mapFade=state===GS.STAGESEL?.9:0;});};
drawStageSelect=function(dt){const r=SL14.base.map.apply(this,arguments);if(SL14.mapFade>0&&state===GS.STAGESEL){SL14.mapFade=Math.max(0,SL14.mapFade-Math.max(0,dt||0));ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.fillStyle='rgba(0,0,0,'+(SL14.mapFade/.9)+')';ctx.fillRect(0,0,cv.width,cv.height);ctx.restore();}return r;};
Snd.prepare?.(['bossWeaponCharge','jetDash']);
window.BOF_SERVICE_DATALINK_1114=SL14;
