(function(){
'use strict';
const atlas=new Image();atlas.src='assets/game/ui/widescreen_0918/operations_panels.png';
const room=document.getElementById('room');if(!room)return;
const left=document.createElement('canvas'),right=document.createElement('canvas'),clock=document.createElement('canvas');
const mapTop=document.createElement('div');mapTop.id='wide-map-top';room.appendChild(mapTop);
left.id='wide-left';right.id='wide-right';clock.id='wide-clock';
for(const c of [left,right,clock]){c.className='wide-overlay';c.setAttribute('aria-hidden','true');room.appendChild(c);}
const L=left.getContext('2d'),R=right.getContext('2d'),T=clock.getContext('2d');
const bgRect={cell:[27,190,126,211],panel:[1184,90,320,810],clock:[182,680,826,130]};
const stageElements=['kinetic','fire','ice','lightning','chrome','dark','toxic','prism','water'];
const portraits={},ranks={};
function img(cache,key,path){if(!cache[key]){const im=new Image();im.src=path;cache[key]=im;}return cache[key];}
function pilotPortraitPath(key){return 'assets/game/pilots_0922/portraits/'+key+'-idle.png';}
function plate(g,source,x,y,w,h){if(atlas.complete&&atlas.naturalWidth)g.drawImage(atlas,...source,x,y,w,h);}
/* Engine UI rule: permanent HUD, leaderboard and side-panel copy uses the authored
   wide Command Alloy face. Dialogue copy keeps Command Signal inside conversations. */
function uiFace(){return window.BOF_UI_FACE||'game';}
function txt(g,str,x,y,size,color,align){if(typeof bmfDrawOn==='function')bmfDrawOn(g,uiFace(),str,x,y,size,align||'left');}
function symbol(g,key,x,y,size){try{
  if(typeof iconBlit==='function'){const v=iconBlit(g,key,x,y,size,true);if(v)return true;}
  if(typeof XART!=='undefined'&&XART.rdy(key)){const im=XART.get(key);g.drawImage(im,x-size/2,y-size/2,size,size);return true;}
}catch(_){}return false;}
function pilot(){try{return (run&&run.pilot)||'cole';}catch(_){return 'cole';}}
function current(){try{return state;}catch(_){return '';}}
function values(){try{
 const key=pilot(),p=typeof PILOTS!=='undefined'?PILOTS.find(v=>v.key===key):null;
 const stage=current()==='stagesel'?sselCursor:(run.stage||1);
 const total=typeof achievementPoints==='function'?achievementPoints():0;
 const points=typeof furiousBalance==='function'?furiousBalance():0;
 const cap=typeof DIFF!=='undefined'&&DIFF?DIFF.continues:0;
 return {key,name:(p&&p.name)||key.toUpperCase(),stage,score:run.score||0,lives:run.lives||0,
  continues:cap<0?'âˆž':Math.max(0,cap-(run.contUsed||0)),diff:(diffKey||'normal').toUpperCase(),points,total,
  objective:(typeof STAGES!=='undefined'&&STAGES[stage-1]?STAGES[stage-1].sub:'RETURN TO FURY HQ')};
}catch(_){return {key:'cole',name:'COLE',stage:1,score:0,lives:0,continues:0,diff:'NORMAL',points:0,total:0,objective:'STANDBY'};}}
function stageGrid(g,w,h,v){
 const cols=9,gap=2,cellW=Math.min(50,Math.floor((w-12-gap*8)/9)),cellH=Math.round(cellW*1.12);
 const x0=8,y0=h-cellH-14;
 const shade=g.createLinearGradient(0,y0-46,0,h);shade.addColorStop(0,'rgba(2,8,20,0)');shade.addColorStop(.55,'rgba(2,8,20,.72)');shade.addColorStop(1,'rgba(2,8,20,.82)');g.fillStyle=shade;g.fillRect(0,y0-46,w,h-y0+46);
 for(let i=0;i<9;i++){
  const st=i+1,x=x0+(i%cols)*(cellW+gap),y=y0+Math.floor(i/cols)*(cellH+gap),unlocked=st<=(campaign.unlockedMax||1)||(st===9&&campaign.bonusUnlocked);
  g.save();g.globalAlpha=unlocked?1:.48;
  plate(g,[bgRect.cell[0]+i*125,bgRect.cell[1],bgRect.cell[2],bgRect.cell[3]],x,y,cellW,cellH);
  if(symbol(g,'inf_'+stageElements[i],x+cellW/2,y+cellH*.57,cellH*.44)===false)txt(g,String(st),x+cellW/2,y+cellH*.6,20,'#adbdcc','center');
  const rank=campaign.rank&&campaign.rank[st];
  if(rank){const file=String(rank).toLowerCase(),im=img(ranks,file,'assets/game/ui/debrief_0916/rankplate_'+file+'.png');
    if(im.complete&&im.naturalWidth)g.drawImage(im,x+cellW*.36,y+2,cellW*.28,cellH*.34);}
  if(st===v.stage){g.strokeStyle='#ffd76e';g.lineWidth=2;g.strokeRect(x+3,y+cellH*.26,cellW-6,cellH*.67);}
  txt(g,'0'+st,x+cellW*.10,y+cellH*.82,Math.max(7,Math.min(10,cellW*.2)),unlocked?'#dce8f2':'#70808b');
  g.restore();
 }
 txt(g,'THEATER PROGRESSION',w/2,Math.max(24,y0-24),17,'#e8d7a1','center');
}
function leaderboard(g,w,h,v){
 const panelW=Math.min(w-12,Math.floor(h*.45)),panelH=Math.min(h-20,Math.floor(panelW*810/320));
 const x=(w-panelW)/2,y=h-panelH-12;
 plate(g,bgRect.panel,x,y,panelW,panelH);
 txt(g,'LOCAL LEADERBOARD',w/2,y+panelH*.20,Math.max(12,Math.min(18,panelW*.048)),'#ffe1a0','center');
 let scores=[{name:v.name,score:v.score}];
 try{for(let i=0;i<CAMP_SLOTS;i++){const save=campReadSlot(i);if(save&&save.v===CAMP_SAVE_VER)scores.push({name:String(save.pilot||'PILOT').toUpperCase(),score:save.score||0});}}catch(_){}
 scores.sort((a,b)=>b.score-a.score);scores=scores.slice(0,4);
 scores.forEach((e,i)=>{const yy=y+panelH*(.397+i*.095);
  txt(g,(i+1)+'. '+e.name,x+panelW*.18,yy,Math.max(10,Math.min(14,panelW*.037)),'#c4d3e2');
  txt(g,String(e.score).padStart(8,'0'),x+panelW*.82,yy,Math.max(10,Math.min(14,panelW*.037)),'#f3cf86','right');});
 txt(g,'ON THIS DEVICE',w/2,y+panelH*.89,Math.max(10,Math.min(13,panelW*.036)),'#94a9b7','center');
}
function rightPanel(g,w,h,v,isMap){
 const panelW=Math.min(w-12,Math.floor(h*.45)),panelH=Math.min(h-20,Math.floor(panelW*810/320));
 const x=(w-panelW)/2,y=h-panelH-12;
 plate(g,bgRect.panel,x,y,panelW,panelH);
 const port=img(portraits,v.key,pilotPortraitPath(v.key));
 if(port.complete&&port.naturalWidth){const bx=x+panelW*.16,by=y+panelH*.075,bw=panelW*.68,bh=panelH*.24;
  const scale=Math.min(bw*.94/port.naturalWidth,bh*.94/port.naturalHeight),pw=port.naturalWidth*scale,ph=port.naturalHeight*scale;
  g.drawImage(port,bx+(bw-pw)/2,by+(bh-ph)/2,pw,ph);}
 const rows=[['SCORE',v.score.toLocaleString()],['FURY PTS',v.points],['ACHIEVEMENT PTS',v.total],['LIVES / CONT',v.lives+' / '+v.continues],['DIFFICULTY',v.diff],['OBJECTIVE',v.objective]];
 rows.forEach((row,i)=>{const yy=y+panelH*(.396+i*.095),fs=Math.max(10,Math.min(15,panelW*.047));
  txt(g,row[0],x+panelW/2,yy-panelH*.013,fs*.8,'#8bbbcf','center');
  const val=String(row[1]),f=val.length>20?Math.max(8,fs*.68):fs;
  txt(g,val,x+panelW/2,yy+panelH*.016,f,'#f2f6fb','center');});
}
function menuPanel(g,w,h,st){
 const panelW=Math.min(w-12,Math.floor(h*.45)),panelH=Math.min(h-20,Math.floor(panelW*810/320));
 const x=(w-panelW)/2,y=h-panelH-12;
 plate(g,bgRect.panel,x,y,panelW,panelH);
 let key='hub',name='',lines=['OPERATIONS','NEW GAME / LOAD','24 MANUAL SLOTS','ONE AUTO CHECKPOINT','SELECT A PILOT','STAND BY'];
 if(st==='diff'){lines=['DIFFICULTY','EASY TO FURIOUS','INSANITY LOCKED','FURIOUS ARMORY','SELECT A PILOT','STAND BY'];}
 if(st==='pilot'){
  try{const p=PILOTS[pilotIndex]||PILOTS[0];key=p.key;name=p.name||p.key.toUpperCase();lines=['PILOT ROSTER','CALLSIGN  '+name.toUpperCase(),'FURY DIVISION','SHIP READY','CONFIRM PILOT','GOOD LUCK'];}catch(_){}
 }
 const port=img(portraits,key,key==='hub'?'assets/game/ui/logo_0916/bof_logo.png':pilotPortraitPath(key));
 if(port.complete&&port.naturalWidth){const bx=x+panelW*.16,by=y+panelH*.075,bw=panelW*.68,bh=panelH*.24;
  const scale=Math.min(bw*.94/port.naturalWidth,bh*.94/port.naturalHeight),pw=port.naturalWidth*scale,ph=port.naturalHeight*scale;
  g.drawImage(port,bx+(bw-pw)/2,by+(bh-ph)/2,pw,ph);}
 if(name)txt(g,name.toUpperCase(),x+panelW/2,y+panelH*.35,Math.max(12,panelW*.058),'#ffe3a3','center');
 lines.forEach((line,i)=>{const size=Math.max(9,Math.min(15,panelW*.045));
  const measure=typeof bmfMeasure==='function'?bmfMeasure(uiFace(),line,size):line.length*size*.65;
  const fit=Math.min(size,size*panelW*.64/Math.max(1,measure));
  txt(g,line,x+panelW/2,y+panelH*(.41+i*.095),fit,'#e1f0ff','center');});
}
function clockPanel(g,w,h){plate(g,bgRect.clock,0,0,w,h);const now=new Date();
 const stamp=[now.getHours(),now.getMinutes(),now.getSeconds()].map(v=>String(v).padStart(2,'0')).join(':');
 txt(g,'LOCAL '+stamp,w/2,h*.52,Math.max(12,h*.32),'#d9f1ff','center');}
let last=0,prev='';
function tick(now){requestAnimationFrame(tick);if(now-last<180)return;last=now;
 const st=current(),map=st==='stagesel',playing=['play','paused','continue','stageclear','gameover'].includes(st);
 const wide=innerWidth>=1150&&document.body.classList.contains('fs')&&!document.body.classList.contains('cinematic-full');
 document.body.classList.toggle('wide-map',wide&&map);
 document.body.classList.toggle('wide-playing',wide&&playing);
 const frame=document.getElementById('game-frame').getBoundingClientRect(),half=Math.max(0,(innerWidth-frame.width)/2),side=Math.min(460,Math.floor(half-18));
 const visible=wide&&side>=184;
 left.style.display=right.style.display=visible?'block':'none';clock.style.display=visible&&map?'block':'none';mapTop.style.display='none';
 if(!visible)return;
 const h=Math.min(innerHeight-16,Math.max(420,Math.floor(frame.height))),top=Math.max(8,Math.round((innerHeight-h)/2));
 for(const [c,sideName] of [[left,'left'],[right,'right']]){
  const x=sideName==='left'?Math.max(8,Math.floor(frame.left-side-8)):Math.min(innerWidth-side-8,Math.ceil(frame.right+8));
  c.style.left=x+'px';c.style.top=top+'px';c.style.width=side+'px';c.style.height=h+'px';
  if(c.width!==side||c.height!==h){c.width=side;c.height=h;}
 }
 if(map){mapTop.style.left=Math.round(frame.left)+'px';mapTop.style.top=Math.round(frame.top)+'px';mapTop.style.width=Math.round(frame.width)+'px';mapTop.style.height=Math.round(frame.width*68/480)+'px';
  const cw=Math.min(400,Math.floor(frame.width*.58)),ch=Math.floor(cw*130/826);clock.width=cw;clock.height=ch;
  clock.style.width=cw+'px';clock.style.height=ch+'px';clock.style.left=Math.round(frame.left+(frame.width-cw)/2)+'px';
  clock.style.top=Math.round(frame.top+frame.width*52/480)+'px';}
 L.clearRect(0,0,left.width,left.height);R.clearRect(0,0,right.width,right.height);
 const v=values();
 if(map){stageGrid(L,left.width,left.height,v);rightPanel(R,right.width,right.height,v,true);T.clearRect(0,0,clock.width,clock.height);clockPanel(T,clock.width,clock.height);}
 else if(playing){leaderboard(L,left.width,left.height,v);rightPanel(R,right.width,right.height,v,false);}
 else{leaderboard(L,left.width,left.height,v);menuPanel(R,right.width,right.height,st);}
}
requestAnimationFrame(tick);
})();
