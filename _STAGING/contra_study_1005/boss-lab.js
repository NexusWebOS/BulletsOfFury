'use strict';
const {Boss,definitions}=BOFBosses,canvas=document.querySelector('#boss-arena'),ctx=canvas.getContext('2d'),select=document.querySelector('#boss-select'),difficulty=document.querySelector('#boss-difficulty');
for(const [id,d]of Object.entries(definitions)){const o=document.createElement('option');o.value=id;o.textContent=d.name;select.append(o);}select.value='regent';
const keys=new Set();let boss,player,hits=0,cooldown=0,paused=false,last=0,acc=0,sim=0,shotTimer=0,meleeTimer=0,shots=[],pointer=null;
const signatureArt=new Image();let signatureReady=false;signatureArt.onload=()=>signatureReady=true;signatureArt.src='art/boss_signature_fx.png';
function restart(){boss=new Boss(select.value,difficulty.value);player={x:250,y:480};hits=0;cooldown=0;sim=0;acc=0;shots=[];shotTimer=0;meleeTimer=0;document.querySelector('#boss-lesson').textContent=boss.def.lesson;document.querySelector('#boss-source').textContent='Study: '+boss.def.source;}
select.onchange=restart;difficulty.onchange=restart;document.querySelector('#boss-restart').onclick=restart;document.querySelector('#boss-pause').onclick=()=>{paused=!paused;document.querySelector('#boss-pause').textContent=paused?'Resume':'Pause';};document.querySelector('#boss-phase').onclick=()=>boss.nextPhase();
document.querySelector('#boss-step').onclick=()=>{paused=true;document.querySelector('#boss-pause').textContent='Resume';for(let i=0;i<30;i++)tick(1/120);};
window.addEventListener('keydown',e=>{if(e.target.tagName==='SELECT'||e.target.tagName==='BUTTON')return;if(['ArrowUp','ArrowDown','ArrowLeft','ArrowRight',' ','w','a','s','d','f'].includes(e.key)){e.preventDefault();keys.add(e.key);}});window.addEventListener('keyup',e=>keys.delete(e.key));window.addEventListener('blur',()=>{keys.clear();pointer=null;});
function locate(e){const r=canvas.getBoundingClientRect();return{x:(e.clientX-r.left)/r.width*960,y:(e.clientY-r.top)/r.height*600};}
canvas.onpointerdown=e=>{canvas.focus();canvas.setPointerCapture(e.pointerId);pointer=locate(e);};canvas.onpointermove=e=>{if(canvas.hasPointerCapture(e.pointerId))pointer=locate(e);};canvas.onpointerup=canvas.onpointercancel=()=>pointer=null;
function tick(dt){
  let dx=(keys.has('d')||keys.has('ArrowRight')?1:0)-(keys.has('a')||keys.has('ArrowLeft')?1:0),dy=(keys.has('s')||keys.has('ArrowDown')?1:0)-(keys.has('w')||keys.has('ArrowUp')?1:0);
  if(pointer){dx=pointer.x-player.x;dy=pointer.y-player.y;if(Math.hypot(dx,dy)<240*dt){player={...pointer};dx=dy=0;}}
  const n=Math.hypot(dx,dy);if(n){player.x+=dx/n*240*dt;player.y+=dy/n*240*dt;}player.x=Math.max(22,Math.min(938,player.x));player.y=Math.max(180,Math.min(578,player.y));
  const old=boss.phase;sim+=dt;boss.advance(sim,()=>player);if(old!==boss.phase||boss.dead)shots=[];
  cooldown=Math.max(0,cooldown-dt);if(!cooldown&&boss.hit(player,12)){hits++;cooldown=.7;}
  shotTimer-=dt;meleeTimer-=dt;
  if((keys.has(' ')||document.querySelector('#boss-auto').checked)&&shotTimer<=0){const p=boss.pose(player).parts.filter(p=>p.vulnerable).sort((a,b)=>Math.hypot(a.x-player.x,a.y-player.y)-Math.hypot(b.x-player.x,b.y-player.y))[0];if(p){const a=Math.atan2(p.y-player.y,p.x-player.x);shots.push({x:player.x,y:player.y,vx:Math.cos(a)*650,vy:Math.sin(a)*650,life:1.6});}shotTimer=.18;}
  if(keys.has('f')&&meleeTimer<=0){meleeTimer=.4;const parts=boss.pose(player).parts.filter(p=>p.vulnerable&&Math.hypot(p.x-player.x,p.y-player.y)<70+p.r);for(const p of parts)boss.damage(p.id,10);boss.effect('contact',player.x,player.y,'player');}
  for(const s of shots){s.x+=s.vx*dt;s.y+=s.vy*dt;s.life-=dt;const p=boss.hitPart(s,5);if(p){boss.damage(p.id,5);s.life=0;}}
  shots=shots.filter(s=>s.life>0); // Phase changes during damage also clear player shots.
  if(old!==boss.phase||boss.dead)shots=[];
}
function line(p,q,color,width,dash=[]){ctx.strokeStyle=color;ctx.lineWidth=width;ctx.setLineDash(dash);ctx.beginPath();ctx.moveTo(p.x,p.y);ctx.lineTo(q.x,q.y);ctx.stroke();ctx.setLineDash([]);}
function circle(p,r,color,fill=true){ctx.beginPath();ctx.arc(p.x,p.y,r,0,Math.PI*2);ctx.fillStyle=color;ctx.strokeStyle=color;ctx.lineWidth=2;fill?ctx.fill():ctx.stroke();}
function effect(f){const z=(boss.time-f.start)/f.life;if(z<0||z>=1)return;ctx.globalAlpha=1-z;
  if(signatureReady){const rows={joint:0,contact:1,breach:2},row=rows[f.name];if(row!==undefined){const frame=Math.min(3,Math.floor(z*4)),size=f.name==='breach'?140:f.name==='contact'?140:115,pivotY=f.name==='joint'?.58:f.name==='contact'?.72:.5;ctx.imageSmoothingEnabled=false;ctx.drawImage(signatureArt,frame*362,row*362,362,362,f.x-size*.5,f.y-size*pivotY,size,size);ctx.globalAlpha=1;return;}}
  if(f.name==='joint'){for(let i=0;i<3;i++){const x=f.x-30+i*20;line({x,y:f.y},{x:x+10,y:f.y-12+Math.sin(z*30+i)*12},'#8be9ff',3);line({x:x+10,y:f.y-12+Math.sin(z*30+i)*12},{x:x+20,y:f.y},'#fff4cc',2);}}
  else{for(let i=0;i<8;i++){const a=i*Math.PI/4;circle({x:f.x+Math.cos(a)*z*55,y:f.y+Math.sin(a)*z*(f.name==='contact'?15:55)},(1-z)*8,f.name==='contact'?'#e0b980':'#ff9c62');}}
  ctx.globalAlpha=1;
}
function draw(){
  const p=boss.pose(player);ctx.clearRect(0,0,960,600);ctx.fillStyle='#0c1726';ctx.fillRect(0,0,960,600);ctx.fillStyle='#182337';ctx.fillRect(0,180,960,420);
  for(let y=210;y<600;y+=90)line({x:0,y},{x:960,y},'#294058',1);for(let x=0;x<960;x+=120)line({x,y:180},{x,y:600},'#20374b',1);
  ctx.font='14px system-ui';ctx.fillStyle='#8db0c7';ctx.fillText(boss.def.name+' / '+(boss.phase+1)+' '+p.kind.toUpperCase(),22,28);
  if(boss.id==='payload'){ctx.fillStyle='#293f50';ctx.fillRect(340,85,280,90);ctx.strokeStyle='#72909b';ctx.strokeRect(340,85,280,90);}
  for(const w of p.warnings){if(w.kind==='segment'){line(w.a,w.b,w.locked?'#ffe4a0':'#e5b363',w.r*2,[8,10]);circle(w.b,20,'#fcca84',false);}else circle(w,w.r,'#e8b467',false);}
  for(const s of p.segments){line(s.a,s.b,'#516278',s.r*2+5);line(s.a,s.b,'#b0c8d0',s.r*1.2);circle(s.a,7,'#e4af69');}
  for(const h of p.hazards){if(h.kind==='segment')line(h.a,h.b,'#ff746a88',h.r*2);else circle(h,h.r,'#ff746a88');}
  for(const part of p.parts){const color=part.id==='core'?(part.vulnerable?'#67dcc8':'#9c788d'):'#d5a868';circle(part,part.r+5,'#060e16');circle(part,part.r,color);circle(part,part.r*.58,'#223447');circle({x:part.x+4,y:part.y-5},part.r*.25,'#e3f7ed');ctx.fillStyle='#eff7ff';ctx.font='11px ui-monospace';ctx.fillText(part.id+' '+part.hp,part.x-24,part.y+part.r+18);}
  for(const b of p.bullets){circle(b,b.r+3,'#692b46');circle(b,b.r,'#ff866c');circle(b,b.r*.45,'#ffe8bd');}
  for(const s of shots)circle(s,4,'#7fdef1');for(const f of p.fx)effect(f);
  circle(player,17,cooldown?'#fff':'#5ce7ec',false);circle(player,12,'#5ce7ec');
  ctx.font='bold 20px system-ui';ctx.fillStyle=p.state==='recovery'?'#81efcf':'#f5c789';ctx.fillText(p.state==='recovery'?'CORE LOW — MELEE / SHOOT':p.state.toUpperCase(),22,61);
  document.querySelector('#status').textContent=`${paused?'PAUSED':p.state} · phase ${boss.phase+1}/${boss.def.phases.length} · core ${boss.hp}/100 · hits ${hits} · ${boss.time.toFixed(1)}s`;
  document.querySelector('#events').textContent=boss.events.slice(-6).map(e=>`${e.at.toFixed(2)} ${e.type} ${e.owner||e.kind||''}`).join('\n');document.querySelector('#events').style.whiteSpace='pre-wrap';
}
function frame(now){const dt=last?Math.min(.1,(now-last)/1000):0;last=now;if(!paused){acc+=dt;while(acc>=1/120){tick(1/120);acc-=1/120;}}draw();requestAnimationFrame(frame);}
restart();requestAnimationFrame(frame);
