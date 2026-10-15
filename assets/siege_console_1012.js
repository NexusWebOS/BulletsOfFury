"use strict";
/* Approved Siege Console: live seat state, proportional authored housings and
   one layout owner for stage cards, fly-ins, combat, pause and continue. */
const SC12 = (() => {
 const art=SC12_ART,room=document.getElementById('room');
 const flow=new Set(['intro','launch','play','paused','continue','gameover','outbound','warpentry','rival','flyover']);
 const base={state:setState,rec:debugRecFrame,load:stageLoadBegin};
 const api={art,base,mode:null,layout:null,last:[],draws:0,contacts:[],clock:0,previousState:null,previousT:0};
 const panels=[0,1].map(i=>{const c=document.createElement('canvas');c.id=i?'siege-right':'siege-left';c.className='siege-side';c.width=512;c.height=1536;room.append(c);return c;});
 const compact=document.createElement('canvas');compact.id='siege-compact';compact.className='siege-compact';compact.width=960;compact.height=352;room.append(compact);
 api.panels=panels;api.compact=compact;
 XART._src[art.key]=art.path;
 stageLoadBegin=function(n,keys){return base.load.call(this,n,[...new Set([...(keys||[]),art.key])]);};
 const isActive=()=>flow.has(state)&&!document.body.classList.contains('campaign-full');
 function css(el,values){for(const [key,value] of Object.entries(values))el.style[key]=typeof value==='number'?value+'px':value;}
 function fit(vw=innerWidth,vh=innerHeight){
  const active=isActive();document.body.classList.toggle('siege-console',active);window.__bofSideHudOwnsLayout=active;
  if(!active){api.mode=null;for(const c of [...panels,compact])c.style.display='none';return false;}
  const rows=seatList().length,fullW=vh*VW/VH,roomW=(vw-fullW)/2-16;
  let width,height,left,top;
  if(roomW>=128){
   api.mode='sides';height=vh;width=fullW;left=(vw-width)/2;top=0;
   const k=Math.min(vh/(1536*rows),roomW/512),pw=512*k,ph=1536*rows*k;
   for(const [i,c] of panels.entries())css(c,{display:'block',width:pw,height:ph,top:(vh-ph)/2,left:i?left+width+8:left-pw-8});
   compact.style.display='none';
  }else{
   api.mode='compact';const hudH=art.compactHeight*rows,k=Math.min(vw/VW,vh/(VH+hudH));
   width=VW*k;height=VH*k;left=(vw-width)/2;top=(vh-(VH+hudH)*k)/2;
   for(const c of panels)c.style.display='none';css(compact,{display:'block',width,height:hudH*k,left,top:top+height});
  }
  const frame=document.getElementById('game-frame'),area=document.getElementById('screen-area');
  css(frame,{position:'fixed',left,top,width,height,marginBottom:0});css(area,{width,height});css(cv,{width,height});
  api.layout={mode:api.mode,rows,field:{x:left,y:top,w:width,h:height},viewport:[vw,vh]};return true;
 }
 function text(g,value,x,y,size,max,align='center'){
  if(value==null)return;const face=window.BOF_UI_FACE||'game',s=String(value).toUpperCase();
  const h=Math.min(size,size*max/Math.max(1,bmfMeasure(face,s,size)));bmfDrawOn(g,face,s,x,y,h,align);
 }
 function inside(g,r,draw){g.save();g.beginPath();g.rect(r[0]+3,r[1]+3,r[2]-6,r[3]-6);g.clip();draw(...r);g.restore();}
 function meter(g,r,frac,color='green'){
  const a=PH8_ART[ph8Theme()]||PH8_ART.stage_01;if(!a||!XART.rdy(a.key))return;
  const n=clamp(Number(frac)||0,0,1);if(!n)return;
  const q=color==='red'?a.special:a.roll;
  g.save();g.beginPath();g.rect(r[0]+2,r[1]+2,(r[2]-4)*n,r[3]-4);g.clip();
  g.drawImage(XART.get(a.key),color==='red'?a.redX:a.greenX,q[1]-a.sourceY,4,q[3],r[0]+2,r[1]+2,r[2]-4,r[3]-4);g.restore();
 }
 function weaponIcon(g,key,x,y,size){
  if(!key)return;
  // Retain the native icon's measured alpha crop, while allowing this larger
  // well to use more than the older horizontal HUD's 38px width cap.
  if(!P2_HUD_ICONS.has(key)){g.save();g.beginPath();g.rect(0,0,0,0);g.clip();p2HudWeaponIcon(g,key,x,y,size);g.restore();}
  const icon=P2_HUD_ICONS.get(key);if(!icon){ph8Icon(g,key,x,y,size);return;}
  const k=size/Math.max(icon.rect[2],icon.rect[3]),w=icon.rect[2]*k,h=icon.rect[3]*k;
  g.drawImage(icon.canvas,...icon.rect,x-w/2,y-h/2,w,h);
 }
 function nameLines(name){
  const str=String(name||''),parts=str.split(/\s*\/\s*/);if(parts.length>1)return [parts[0],parts.slice(1).join(' / ')];
  const words=str.split(/\s+/);if(words.length<2)return [str];
  let best=[str],width=Infinity;
  for(let i=1;i<words.length;i++){const rows=[words.slice(0,i).join(' '),words.slice(i).join(' ')],w=Math.max(...rows.map(s=>bmfMeasure(window.BOF_UI_FACE||'game',s,34)));
   if(w<width){width=w;best=rows;}}
  return best;
 }
 function contacts(){
  const list=[],left=camLeftX(),right=camRightX(),top=viewTopY(),height=viewH();
  const add=(p,color,size,kind)=>{if(!p||p.dead||!Number.isFinite(p.x)||!Number.isFinite(p.y)||p.x<left||p.x>right||p.y<top||p.y>top+height)return;list.push({x:(p.x-left)/Math.max(1,right-left),y:(p.y-top)/height,color,size,kind});};
  for(const e of enemies)if(e&&!e.frCloak)add(e,'#ff7653',5,'enemy');
  if(subBossActive)add(subBoss,'#ffb369',7,'mini');
  if(bossActive&&boss&&!boss.dead){if(boss._rebels){for(const q of boss._rebels.ships)if(q.hp>0&&!q.frCloak)add(q,'#ff5c5c',7,'boss');}else add(boss,'#ff5c5c',8,'boss');}
  for(const seat of seatList())add(seatShip(seat),seat===1?'#bcff98':'#80dfff',7,'player');
  return list;
 }
 function radar(g,r,k){inside(g,r,(x,y,w,h)=>{
  text(g,'RADAR',x+w/2,y+h*.09,30*k,w-18*k);const cx=x+w/2,cy=y+h*.55,radius=Math.min(w*.39,h*.34);
  g.lineWidth=Math.max(.6,2*k);g.strokeStyle='#286557';
  for(const scale of [1,.67,.33]){g.beginPath();g.arc(cx,cy,radius*scale,0,Math.PI*2);g.stroke();}
  g.beginPath();g.moveTo(cx-radius,cy);g.lineTo(cx+radius,cy);g.moveTo(cx,cy-radius);g.lineTo(cx,cy+radius);g.stroke();
  const angle=api.clock*.8-Math.PI/2;g.strokeStyle='#8ae4b1';g.beginPath();g.moveTo(cx,cy);g.lineTo(cx+Math.cos(angle)*radius,cy+Math.sin(angle)*radius);g.stroke();
  for(const p of api.contacts){const dx=cx+(p.x*2-1)*radius*.7,dy=cy+(p.y*2-1)*radius*.7,s=p.size*k;g.fillStyle=p.color;g.fillRect(dx-s/2,dy-s/2,s,s);}
  const n=api.contacts.filter(p=>p.kind!=='player').length;text(g,n+' CONTACT'+(n===1?'':'S'),cx,y+h*.92,22*k,w-20*k);
 });}
 function widget(g,key,r,v,barRect){
  const k=r[2]/art.wells[key][2],pk={yuri:0,falva:1,cole:2,maverick:3,axel:4,juggernaut:5,lizzie:6,decker:7,freezer:8}[v.pilot]??0;
  if(key==='radar'){radar(g,r,k);return;}
  inside(g,r,(x,y,w,h)=>{
   const tx=(s,px,py,size,max=w-18*k,align='center')=>text(g,s,px,py,size*k,max,align);
   const ic=(key,px,py,size)=>ph8Icon(g,key,px,py,size*k);
   if(key==='scores'){
    tx((seatList().length>1?'P'+v.seat+' ':'')+v.pilot+' SCORE',x+w/2,y+h*.16,29);tx(ph8Score(v.score),x+w/2,y+h*.43,62);
    tx('HIGH SCORE',x+w*.27,y+h*.78,21,w*.45);tx(ph8Score(api.highScore),x+w*.75,y+h*.78,30,w*.47);
   }else if(key==='roll'||key==='somer'){
    const available=key==='roll'?v.rollAvailable:v.somerAvailable,fraction=available?v[key]:0;
    tx(key==='roll'?'ROLL':'SOMERSAULT',x+w/2,y+h*.22,29);tx(available?(fraction>=.999?'READY':Math.round(fraction*100)+'%'):'LOCKED',x+w/2,y+h*.62,42);
   }else if(key==='weapon'){
    tx('EQUIPPED WEAPON',x+w/2,y+h*.09,27);
    if(v.weapon.reel)cf1004Cell(v.weapon.reel,CF1004.clock,x+w/2,y+h*.43,80*k,128*k,0,g);
    else weaponIcon(g,v.weapon.key,x+w/2,y+h*.43,146*k);
    tx(v.weapon.label||v.weaponName,x+w/2,y+h*.72,34);tx(v.weaponFixed?'FIXED / LEVEL 01':'LEVEL '+String(v.weapon.lv).padStart(2,'0'),x+w/2,y+h*.86,29);
    for(let i=0;i<v.loans.length;i++){const q=v.loans[i],lx=x+18*k+i*52*k;ic(q.icon,lx,y+h-12*k,28);meter(g,[lx-14*k,y+h-3*k,28*k,5*k],q.frac,'red');}
   }else if(key==='special'){
    tx('SPECIAL ABILITY',x+w/2,y+h*.09,28);ic(specialArtKey('spicon_'+v.pilot),x+w/2,y+h*.4,126);
    const lines=nameLines(v.name);for(let i=0;i<lines.length;i++)tx(lines[i],x+w/2,y+h*(lines.length===1?.73:.68+i*.115),34);
    tx(v.dead?'SHIP LOST':v.detail,x+w/2,y+h*.93,24);
   }else if(key==='lives'||key==='missiles'){
    tx(key,x+w/2,y+h*.13,27);ic((key==='lives'?'nli_':'nmi_')+pk,x+w*.22,y+h*.55,44);
    tx(String(Math.max(0,v[key]|0)).padStart(2,'0'),x+w*.65,y+h*.57,76,w*.67);
    if(v[key]<=1){g.fillStyle=v[key]?'#ffbd54':'#ff535b';g.fillRect(x+10*k,y+h-11*k,w-20*k,4*k);}
   }else if(key==='lock'){
    tx('RETINA LOCK',x+w/2,y+h*.12,28);ic('retm_0',x+w/2,y+h*.46,88);tx(v.lock?'TARGET LOCKED':'NO LOCK',x+w/2,y+h*.81,34);
    if(v.lock){g.strokeStyle='#ff7053';g.lineWidth=4*k;g.strokeRect(x+6*k,y+6*k,w-12*k,h-12*k);}
   }else if(key==='speed'||key==='shield'){
    tx(key,x+10*k,y+h*.45,27,w*.34,'left');const start=x+w*.40,step=w*.105;
    for(let i=0;i<5;i++){g.fillStyle=i<v[key]?(key==='shield'?'#57dce8':'#ffbd60'):'#20313c';g.fillRect(start+i*step,y+h*.22,step-5*k,h*.47);}
   }else if(key==='pilot'){
    tx((seatList().length>1?'P'+v.seat+' / ':'')+v.pilot+' / FURY FLIGHT',x+w/2,y+h*.14,28);
    ic('nli_'+pk,x+w/2,y+h*.47,80);tx(v.dead?'SHIP LOST':'STAGE '+(run._gp4StageX?'X':String(run.stage).padStart(2,'0')),x+w/2,y+h*.78,30);
   }
  });
  if(barRect)meter(g,barRect,key==='special'?v.resource:(key==='roll'?v.rollAvailable:v.somerAvailable)?v[key]:0,key==='special'?'red':'green');
 }
 function readSeat(seat){return withSeat(seat,()=>{
  const v=ph8Values(),variant=heldVariant(run.weapon);
  v.weaponName=spaceWeaponsActive()?spaceWeaponName():(WVAR_NAME[variant]||WEAPONS[run.weapon]||'WEAPON');
  v.weaponFixed=!spaceWeaponsActive()&&v.pilot==='maverick'&&run.weapon===3&&variant==='mavhoming';
  if(v.weaponFixed)v.weapon={...v.weapon,lv:1};return v;
 });}
 // Keep the authored housing on its surface. Redraw only wells whose visible
 // values changed; the radar/animated weapon still advance on every frame.
 const columnState=[{},{}];
 function signature(key,v,bar){
  const iconReady=k=>{if(!k)return false;const t=BOFX.icons?.[specialArtKey(k)];return XART.rdy(t?(t[4]||'nia_icons'):specialArtKey(k));};
  const pixel=(frac,r)=>Math.round(clamp(Number(frac)||0,0,1)*Math.max(0,r?r[2]-4:0));
  let fields;
  if(key==='scores')fields=[v.pilot,v.seat,v.score,api.highScore,valuesRows];
  else if(key==='roll'||key==='somer')fields=[v[key+'Available'],Math.round(v[key]*100),v[key]>=.999,pixel(v[key],bar)];
  else if(key==='weapon')fields=[v.weapon,v.weaponName,v.weaponFixed,v.loans.map(q=>[q.icon,q.frac,iconReady(q.icon)]),iconReady(v.weapon.key),v.weapon.reel?CF1004.clock:0];
  else if(key==='special')fields=[v.name,v.detail,v.dead,pixel(v.resource,bar),iconReady(specialArtKey('spicon_'+v.pilot))];
  else if(key==='radar')fields=[api.clock,api.contacts];
  else if(key==='lives'||key==='missiles'){const pk={yuri:0,falva:1,cole:2,maverick:3,axel:4,juggernaut:5,lizzie:6,decker:7,freezer:8}[v.pilot]??0;fields=[v.pilot,v[key],iconReady((key==='lives'?'nli_':'nmi_')+pk)];}
  else if(key==='pilot')fields=[v.pilot,v.dead,run.stage,run._gp4StageX,valuesRows,iconReady('nli_'+({yuri:0,falva:1,cole:2,maverick:3,axel:4,juggernaut:5,lizzie:6,decker:7,freezer:8}[v.pilot]??0))];
  else fields=[v.pilot,v[key],key==='lock'?iconReady('retm_0'):true];
  return JSON.stringify([ph8Theme(),...fields]);
 }
 let valuesRows=1;
 function drawColumns(source,values){
  valuesRows=values.length;
  for(const [side,canvas] of panels.entries()){
   const targetH=1536*values.length,C=columnState[side];
   const reset=canvas.height!==targetH||C.source!==source||C.rows!==values.length;
   if(canvas.height!==targetH)canvas.height=targetH;
   const g=canvas.getContext('2d');g.imageSmoothingEnabled=false;
   if(reset){g.clearRect(0,0,512,targetH);C.source=source;C.rows=values.length;C.keys=new Map();
    for(let i=0;i<values.length;i++)g.drawImage(source,side*512,0,512,1536,0,i*1536,512,1536);}
   for(const v of values)withSeat(v.seat,()=>{g.save();g.translate(0,(v.seat-1)*1536);
    const rect=key=>{const r=art.wells[key];return [r[0]-side*512,r[1],r[2],r[3]];};
    for(const key of side?['radar','special','lives','missiles','lock']:['scores','roll','somer','weapon','speed','shield','pilot']){
     const r=rect(key),bar=['roll','somer','special'].includes(key)?rect(key+'Bar'):null,id=v.seat+':'+key,sig=signature(key,v,bar);
     if(C.keys.get(id)===sig){api.widgetsSkipped=(api.widgetsSkipped||0)+1;continue;}
     const x=Math.floor(Math.min(r[0],bar?bar[0]:r[0])-1),y=Math.floor(Math.min(r[1],bar?bar[1]:r[1])-1);
     const w=Math.ceil(Math.max(r[0]+r[2],bar?bar[0]+bar[2]:r[0]+r[2])+1)-x,h=Math.ceil(Math.max(r[1]+r[3],bar?bar[1]+bar[3]:r[1]+r[3])+1)-y;
     g.clearRect(x,y,w,h);g.drawImage(source,x+side*512,y,w,h,x,y,w,h);
     widget(g,key,r,v,bar);C.keys.set(id,sig);api.widgetsPainted=(api.widgetsPainted||0)+1;
    }
    g.restore();});
  }
 }
 function drawCompact(source,values){
  const wanted=art.compactHeight*values.length*2;if(compact.height!==wanted)compact.height=wanted;
  const g=compact.getContext('2d');g.clearRect(0,0,compact.width,compact.height);g.save();g.scale(2,2);g.imageSmoothingEnabled=false;
  const cells=[['scores',[0,0,200,80]],['lives',[200,0,84,80]],['missiles',[284,0,84,80]],['radar',[368,0,112,80]],
   ...['roll','somer','weapon','special','lock'].map((key,i)=>[key,[i*96,80,96,96]])];
  for(const v of values)withSeat(v.seat,()=>{g.save();g.translate(0,(v.seat-1)*art.compactHeight);
   for(const [key,cell] of cells){const src=art.modules[key],k=Math.min(cell[2]/src[2],cell[3]/src[3]),x=cell[0]+(cell[2]-src[2]*k)/2,y=cell[1]+(cell[3]-src[3]*k)/2;
    g.drawImage(source,...src,x,y,src[2]*k,src[3]*k);const rect=name=>{const r=art.wells[name];return [x+(r[0]-src[0])*k,y+(r[1]-src[1])*k,r[2]*k,r[3]*k];};
    widget(g,key,rect(key),v,['roll','somer','special'].includes(key)?rect(key+'Bar'):null);
   }g.restore();});g.restore();
 }
 function refresh(){
  if(!isActive())return;const rows=seatList().length;
  if(!api.layout||api.layout.rows!==rows||api.layout.viewport[0]!==innerWidth||api.layout.viewport[1]!==innerHeight)fit();
  if(state==='play'&&api.previousState===state&&stateT>=api.previousT)api.clock+=Math.min(.1,stateT-api.previousT);
  api.previousState=state;api.previousT=stateT;
  if(!XART.rdy(art.key)||!bmfReady(window.BOF_UI_FACE||'game'))return;
  api.contacts=contacts();const values=seatList().map(readSeat),source=XART.get(art.key);
  api.highScore=Math.max(highScore,...values.map(v=>v.score));
  if(api.mode==='sides')drawColumns(source,values);else drawCompact(source,values);
  api.last=values;api.draws++;
  const paused=state==='paused',filter=paused?'grayscale(.8) brightness(.88)':'';
  for(const c of [...panels,compact])if(c.style.filter!==filter)c.style.filter=filter;
 }
 setState=function(){const r=base.state.apply(this,arguments);if(window.__bofFit)window.__bofFit();refresh();return r;};
 debugRecFrame=function(){refresh();return base.rec.apply(this,arguments);};
 Object.assign(api,{fit,active:isActive,refresh,invalidate:()=>{for(const c of columnState)c.source=null;}});return api;
})();
window.BOFSideHUD=SC12;
window.__bofFit();
