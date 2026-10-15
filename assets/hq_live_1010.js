"use strict";
/* Live command-room instruments. Authored sprites supply every ship and FX;
   the cinematic clock owns movement, acquisition, sound and interaction. */
const HQ10={base:{cover:cinCover,load:stageLoadBegin,tick:BOFCinematicDirector.tick,hints:controlHintRow,viewport:_setCinematicViewport,block:msgDrawBlock},
 events:[],draws:{},rect:null,mapBounds:null,ready:false};
for(const bank of Object.values(HQ10_ART))for(const a of bank)XART._src[a.key]=a.path;
function hq10Record(event,data={}){HQ10.events.push({event,...data});if(HQ10.events.length>128)HQ10.events.shift();}
function hq10Sound(event){
 const names={boot:'retinaCharge',contact:'retinaLockBeep',focus:'blip',scan:'retinaCharge',confirmed:'select',signal:'av3_target_acquire',launch:'thruster'};
 const name=names[event],fn=Audio.SFX?.[name];if(fn)fn();hq10Record('sound',{cue:event,name,available:!!fn});
}
function hq10Shot(scene=BOFCinematicDirector.current){
 const beat=scene?.beats?.[scene.i],index=HQ10_ART.background.findIndex(a=>a.key===beat?.bg);
 return index<0?null:{scene,beat,index};
}
function hq10MapActive(){return hq10Shot()?.index===2;}
msgDrawBlock=function(o){
 if(hq10Shot()&&cutsceneViewWidth()<400)o={...o,maxH:Math.min(o.maxH||14,10),minH:Math.min(o.minH||8,6)};
 return HQ10.base.block.call(this,o);
};
_setCinematicViewport=function(on){
 const r=HQ10.base.viewport.apply(this,arguments);
 if(on&&hq10Shot()&&!BOFCinematicDirector.live){
  // HQ instruments and pilot portraits must have the same physical pixel
  // scale on both axes, even below the legacy 640px cinematic minimum.
  CINEMA_VW=Math.max(1,Math.round(VH*window.innerWidth/Math.max(1,window.innerHeight)));
  if(cv.width!==CINEMA_VW*SS||cv.height!==VH*SS){cv.width=CINEMA_VW*SS;cv.height=VH*SS;}
  ctx.imageSmoothingEnabled=false;if(window.__bofFit)window.__bofFit();
 }
 return r;
};
function hq10Warm(){
 let ready=true;for(const a of Object.values(HQ10_ART).flat())if(!XART.rdy(a.key))ready=false;
 for(const k of ['ship_'+(run.pilot||'cole'),'fb2_stealth_red','fb2_stealth_green','fb2_stealth_orange','mission29_radar','retm_0','retm_1','retm_2','retm_3'])if(!XART.rdy(k))ready=false;
 HQ10.ready=ready;return ready;
}
stageLoadBegin=function(n,keys){return HQ10.base.load.call(this,n,[...(keys||[]),...(n===5||n===6?Object.values(HQ10_ART).flat().map(a=>a.key):[])]);};
function hq10Formation(){
 const lead=run.pilot||'cole',pool=['axel','yuri','maverick','lizzie','falva','freezer','juggernaut'];
 return [lead,...pool.filter(k=>k!==lead)].slice(0,5);
}
function hq10Model(shot){
 const s=shot.scene;if(s._hq10?.i===s.i)return s._hq10;
 const tracks=Array.from({length:14},(_,i)=>({id:'hostile-'+i,kind:'hostile',role:i%3===1?'green':'red',
  startX:i%2?.88:.08,startY:.08+(i%7)*.105,endX:.50+(i%3-1)*.06,endY:.43,
  phase:i*.083,spawn:.45+Math.floor(i/4)*.75,seen:false,confirmed:false}));
 for(const [i,key]of hq10Formation().entries())tracks.push({id:key,kind:'friendly',key,phase:i/5,spawn:0,seen:false,confirmed:false});
 tracks.push({id:'unknown-signal',kind:'signal',spawn:5.8,seen:false,confirmed:false});
 s._hq10={i:s.i,t:0,tracks,selected:0,scan:null,controls:true,pingAt:-10,entered:false,signal:false};return s._hq10;
}
function hq10TrackPosition(q,t){
 if(q.kind==='signal')return {x:.50,y:.75};
 if(q.kind==='friendly'){const a=q.phase*Math.PI*2+t*.22;return{x:.51+Math.cos(a)*.16,y:.44+Math.sin(a)*.14};}
 const u=((t*.085+q.phase)%1+1)%1,k=u<.72?u/.72:1-(u-.72)/.28;
 return{x:q.startX+(q.endX-q.startX)*k,y:q.startY+(q.endY-q.startY)*k};
}
function hq10Tick(dt){
 const shot=hq10Shot();if(!shot)return;
 const M=hq10Model(shot);if(!HQ10.ready&&!hq10Warm())return;
 M.t+=Math.min(.1,Math.max(0,dt));
 if(!M.entered){M.entered=true;hq10Record('shot',{index:shot.index,pilot:run.pilot});if(shot.index===2)hq10Sound('boot');if(shot.index===3)hq10Sound('launch');}
 if(shot.index!==2)return;
 const angle=((M.t-2)*Math.PI*2/3+Math.PI*2)%(Math.PI*2),fill=clamp(M.t/2,0,1);
 for(const q of M.tracks){
  if(q.seen||M.t<q.spawn)continue;
  const p=hq10TrackPosition(q,M.t),a=(Math.atan2(p.x-.5,-(p.y-.5))+Math.PI*2)%(Math.PI*2);
  const delta=(angle-a+Math.PI*2)%(Math.PI*2);
  if((M.t<2&&a<fill*Math.PI*2)||(M.t>=2&&delta<.30)||M.t>q.spawn+3){
   q.seen=true;hq10Record('contact',{id:q.id,kind:q.kind,t:M.t});
   if(M.t-M.pingAt>.32){hq10Sound(q.kind==='signal'?'signal':'contact');M.pingAt=M.t;}
  }
 }
 if(M.scan){M.scan.t+=dt;if(M.scan.t>=1.5){const q=M.tracks[M.scan.index];q.confirmed=true;
  hq10Record('scan-complete',{id:q.id});hq10Sound('confirmed');M.scan=null;}}
}
BOFCinematicDirector.tick=function(dt){hq10Tick(dt);return HQ10.base.tick.call(this,dt);};
function hq10Focus(M,index){
 if(index<0||index===M.selected)return;M.selected=index;hq10Record('focus',{id:M.tracks[index].id});hq10Sound('focus');
}
function hq10SelectDirection(M,dx,dy){
 const current=hq10TrackPosition(M.tracks[M.selected],M.t);let best=-1,score=Infinity;
 for(let i=0;i<M.tracks.length;i++){
  if(i===M.selected||!M.tracks[i].seen)continue;const p=hq10TrackPosition(M.tracks[i],M.t),x=p.x-current.x,y=p.y-current.y,along=x*dx+y*dy;
  if(along<=.002)continue;const cost=Math.hypot(x,y)+Math.abs(x*dy-y*dx)*1.4;if(cost<score){score=cost;best=i;}
 }hq10Focus(M,best);
}
function hq10BeginScan(M){
 const q=M.tracks[M.selected];if(!q?.seen||M.scan)return;
 M.scan={index:M.selected,t:0};hq10Record('scan-start',{id:q.id});hq10Sound('scan');
}
// The director asks the active surface before interpreting A/click as NEXT.
// Start remains scene skip. B returns from radar inspection to ordinary
// dialogue; A then follows the director's original REVEAL/NEXT action.
function cinematicSurfaceInput(beat,scene,dt){
 if(beat.interactive!=='hq-radar')return false;
 const M=hq10Model({scene,beat,index:2});let handled=false;
 for(const [read,dx,dy]of [['menuLeft',-1,0],['menuRight',1,0],['menuUp',0,-1],['menuDown',0,1]]){
  if(Input[read]()){M.controls=true;hq10SelectDirection(M,dx,dy);handled=true;}
 }
 if(Input.menuBack()){M.controls=false;M.scan=null;hq10Record('radar-back');hq10Sound('focus');return true;}
 if(M.controls&&Input.menuConfirm()){hq10BeginScan(M);handled=true;}
 const bounds=HQ10.mapBounds;
 // The engine's cutscene mouse storage uses VW; the cinematic canvas uses W.
 const mouse={x:Input.mouse.x*cutsceneViewWidth()/VW,y:Input.mouse.y};
 if(bounds&&mouse.x>=bounds.x&&mouse.x<=bounds.x+bounds.w&&mouse.y>=bounds.y&&mouse.y<=bounds.y+bounds.h){
  let index=-1,best=24;
  for(let i=0;i<M.tracks.length;i++){if(!M.tracks[i].seen)continue;
   const q=hq10TrackPosition(M.tracks[i],M.t),d=Math.hypot(bounds.x+q.x*bounds.w-mouse.x,bounds.y+q.y*bounds.h-mouse.y);
   if(d<best){best=d;index=i;}}
  if(Input.mouse.moved&&index>=0)hq10Focus(M,index);
  if(Input.mouse.down&&!scene.md){M.controls=true;if(index>=0)hq10Focus(M,index);hq10BeginScan(M);scene.md=true;handled=true;}
 }
 return handled;
}
function hq10Cell(a,x,y,w,rotation=0,opacity=1){
 if(!a||!XART.rdy(a.key))return false;const k=w/a.w;
 ctx.save();ctx.translate(x,y);ctx.rotate(rotation);ctx.globalAlpha*=opacity;
 ctx.drawImage(XART.get(a.key),-a.pivot[0]*k,-a.pivot[1]*k,a.w*k,a.h*k);ctx.restore();return true;
}
function hq10Plane(key,x,y,h,heading,role){
 const art=role?'fb2_stealth_'+role:'ship_'+key;if(!XART.rdy(art))return;
 const im=XART.get(art);ctx.save();ctx.translate(x,y);ctx.rotate(heading);ctx.imageSmoothingEnabled=false;
 if(role)ctx.drawImage(im,384,0,128,128,-h/2,-h/2,h,h);
 else {const w=h*im.width/im.height;ctx.drawImage(im,-w/2,-h/2,w,h);}
 ctx.restore();HQ10.draws[art]=(HQ10.draws[art]||0)+1;
}
function hq10Radar(M,x,y,size,offset=0,opacity=.8){
 const f=M.t<2?Math.min(7,Math.floor(M.t*4)):8+(Math.floor((M.t-2)*8)+offset)%24;
 ctx.save();
 if(M.t<2){ctx.beginPath();ctx.moveTo(x,y);ctx.arc(x,y,size/2,-Math.PI/2,-Math.PI/2+Math.PI*2*clamp(M.t/2,0,1));ctx.closePath();ctx.clip();}
 hq10Cell(HQ10_ART.radar[f],x,y,size,0,opacity);ctx.restore();HQ10.draws.radar=(HQ10.draws.radar||0)+1;
}
function hq10Cross(x,y,size,t,alpha=1){
 const key='retm_'+(Math.floor(t*10)%4);if(!XART.rdy(key))return;
 const im=XART.get(key);ctx.save();ctx.globalAlpha*=alpha;ctx.drawImage(im,x-size/2,y-size/2,size,size);ctx.restore();
}
function hq10MapDraw(M,R){
 const x=R.x+R.w*.194,y=R.y+R.h*.112,w=R.w*.590,h=R.h*.502;
 HQ10.mapBounds={x,y,w,h};
 ctx.save();ctx.beginPath();ctx.rect(x,y,w,h);ctx.clip();
 hq10Radar(M,x+w*.51,y+h*.48,Math.min(w,h)*1.40,0,.34);
 for(let i=0;i<M.tracks.length;i++){
  const q=M.tracks[i];if(!q.seen)continue;const p=hq10TrackPosition(q,M.t),px=x+p.x*w,py=y+p.y*h;
  if(q.kind==='signal'){const a=AP10_CIN_ART.void[8+Math.floor(M.t*20)%16];hq10Cell(a,px,py,32,0,.9);}
  else{
   const target=q.kind==='hostile'?{x:q.endX,y:q.endY}:{x:.51,y:.44},angle=Math.atan2(target.y-p.y,target.x-p.x)+Math.PI/2;
   hq10Plane(q.key,px,py,q.kind==='hostile'?16:15,angle,q.kind==='hostile'?q.role:null);
  }
  if(i===M.selected&&M.controls){hq10Cross(px,py,28,M.t);if(M.scan?.index===i)hq10Radar({t:M.scan.t*2},px,py,42,0,.8);}
 }
 ctx.restore();
 hq10Radar(M,R.x+R.w*.090,R.y+R.h*.25,R.w*.170,0,.82);
 hq10Radar(M,R.x+R.w*.900,R.y+R.h*.25,R.w*.170,12,.76);
 // The two lower instruments use the already authored four-frame signal reel.
 const waveform=MISSION29_ART.radar;
 if(XART.rdy(waveform.key))for(const [i,left]of [.015,.810].entries()){
  const source=waveform.frames[(Math.floor(M.t*waveform.fps)+i*2)%waveform.frames.length],width=R.w*.17,height=width*source[3]/source[2];
  ctx.drawImage(XART.get(waveform.key),...source,R.x+R.w*left,R.y+R.h*.443-height/2,width,height);
  HQ10.draws.signal=(HQ10.draws.signal||0)+1;
 }
 const count=M.tracks.filter(q=>q.seen&&q.kind==='hostile').length,q=M.tracks[M.selected];
 const progress=M.scan?Math.round(clamp(M.scan.t/1.5,0,1)*100):Math.round(clamp(M.t/2,0,1)*100);
 const mode=M.scan?'ANALYZING':q.confirmed?'IDENTIFIED':M.t<2?'ACQUIRING':'LIVE TRACKING';
 const label=!M.controls?'FURY HQ / LIVE AIRSPACE':!q.seen?'WAITING FOR CONTACT':q.kind==='signal'?'UNKNOWN CODE SOURCE':q.kind==='friendly'?q.key.toUpperCase()+' / FURY':q.role.toUpperCase()+' STEALTH FIGHTER';
 ctx.save();ctx.fillStyle='rgba(1,11,20,.87)';ctx.fillRect(R.x+R.w*.195,R.y+R.h*.615,R.w*.59,R.h*.09);
 msgFaceUse('dialogue');
 const status='HOSTILES '+String(count).padStart(2,'0')+' / '+mode+' '+progress+'%';
 msgTextLeft(status,R.x+R.w*.205,R.y+R.h*.631,msgFitH(status,R.w*.57,8,5),'#63fbc5',0,1,.08,0);
 msgTextLeft(label,R.x+R.w*.205,R.y+R.h*.671,msgFitH(label,R.w*.57,8,5),q.kind==='hostile'?'#ff8877':'#a7edff',0,1,.08,0);
 msgFaceUse(null);ctx.restore();HQ10.draws.map=(HQ10.draws.map||0)+1;
}
function hq10FlightDraw(index,M,R){
 const t=M.t,lead=run.pilot||'cole';
 if(index===0){
  const u=clamp(t/5.6,0,1),k=u*u*(3-2*u),start={x:.24,y:.10},end={x:.71,y:.70};
  hq10Plane(lead,R.x+(start.x+(end.x-start.x)*k)*R.w,R.y+(start.y+(end.y-start.y)*k)*R.h,
   R.h*(.32-.18*k),Math.atan2(end.y-start.y,end.x-start.x)+Math.PI/2);
 }else if(index===1){
  ctx.save();ctx.beginPath();ctx.rect(R.x,R.y,R.w,R.h);ctx.clip();
  for(let i=0;i<7;i++){const u=(t*.16+i*.143)%1,fromRight=i%2===1,px=fromRight?1.12-u*1.35:-.12+u*1.35;
   hq10Plane(null,R.x+px*R.w,R.y+(.12+i*.073+Math.sin(t*1.3+i)*.018)*R.h,R.h*.10,fromRight?-Math.PI/2:Math.PI/2,i%3===1?'green':'red');}
  const f=Math.floor(t*24)%16;for(const [i,p]of [[.40,.50],[.79,.42],[.57,.69]].entries()){
   const bank=AF10_ART.plasma_blast;if(bank)hq10Cell(bank[(f+i*4)%bank.length],R.x+p[0]*R.w,R.y+p[1]*R.h,R.h*.13);}
  ctx.restore();
 }else if(index===3){
  const keys=hq10Formation();ctx.save();ctx.beginPath();ctx.rect(R.x,R.y,R.w,R.h);ctx.clip();
  for(let i=0;i<keys.length;i++){
   const u=clamp((t-i*.35)/5.8,0,1),k=u*u*(3-2*u),col=(i-2),start={x:.56+col*.050,y:.45},end={x:.50+col*.16,y:1.08-Math.abs(col)*.09};
   hq10Plane(keys[i],R.x+(start.x+(end.x-start.x)*k)*R.w,R.y+(start.y+(end.y-start.y)*k)*R.h,
    R.h*(.08+.22*k),Math.atan2(end.y-start.y,end.x-start.x)+Math.PI/2);
  }ctx.restore();
 }
}
cinCover=function(key,W,H,pan,flightY){
 const index=HQ10_ART.background.findIndex(a=>a.key===key);if(index<0)return HQ10.base.cover.apply(this,arguments);
 const a=HQ10_ART.background[index];if(!XART.rdy(a.key))return false;
 // Keep the complete cockpit/radar panel visible above the dialogue in every
 // viewport; a cover crop would remove the side radars or portrait edges.
 const k=Math.min(W/a.w,H*.70/a.h),R={x:(W-a.w*k)/2,y:(H*.70-a.h*k)/2,w:a.w*k,h:a.h*k};HQ10.rect=R;
 ctx.save();ctx.imageSmoothingEnabled=false;ctx.drawImage(XART.get(a.key),R.x,R.y,R.w,R.h);
 const shot=hq10Shot(),M=shot?hq10Model(shot):{t:0};
 if(index===2&&shot)hq10MapDraw(M,R);else hq10FlightDraw(index,M,R);
 ctx.restore();HQ10.draws.background=(HQ10.draws.background||0)+1;return true;
};
controlHintRow=function(items,y,cx,maxW,h){
 if(hq10MapActive()&&items.some(q=>q[0]==='pad_a'&&['REVEAL','NEXT'].includes(q[1])))
  items=BOFCinematicDirector.current._hq10?.controls?
   [['pad_dpad','CONTACT'],['pad_a','SCAN'],['pad_b','BACK'],['pad_start','SKIP SCENE']]:[['pad_dpad','CONTACT'],...items];
 return HQ10.base.hints.call(this,items,y,cx,maxW,h);
};
