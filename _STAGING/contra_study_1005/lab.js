'use strict';
const {Encounter,recipes,hit}=BOFPatterns;
const arena=document.querySelector('#arena'),g=arena.getContext('2d'),fxCanvas=document.querySelector('#fx'),fg=fxCanvas.getContext('2d');
const recipe=document.querySelector('#recipe'),difficulty=document.querySelector('#difficulty');
for(const [id,r] of Object.entries(recipes)){const o=document.createElement('option');o.value=id;o.textContent=r.name;recipe.append(o);}
const keys=new Set();let player={x:.5,y:.8},encounter,cycle=0,t=0,paused=false,hits=0,cooldown=0,accumulator=0,last=0,sim=0,pointer=null;
const art=new Image();let artReady=false;art.onload=()=>{artReady=true;document.querySelector('#asset-status').textContent='12 frames · native 1448 × 1086 RGBA · 20 fps · source pixels preserved';};art.onerror=()=>{document.querySelector('#asset-status').textContent='Asset failed to load';};art.src='art/reactor_pressure_discharge.png';
function restart(){cycle=0;t=0;sim=0;hits=0;cooldown=0;accumulator=0;player={x:.5,y:.8};encounter=new Encounter(recipe.value,difficulty.value,cycle);encounter.advance(0,()=>player);const r=recipes[recipe.value];document.querySelector('#name').textContent=r.name;document.querySelector('#lesson').textContent=r.lesson;document.querySelector('#fit').textContent='BOF fit: '+r.fit;document.querySelector('#source').textContent='Reference: '+r.source;}
recipe.addEventListener('change',restart);difficulty.addEventListener('change',restart);document.querySelector('#restart').onclick=restart;
document.querySelector('#pause').onclick=()=>{paused=!paused;document.querySelector('#pause').textContent=paused?'Resume':'Pause';};document.querySelector('#destroy').onclick=()=>encounter.cancel();
window.addEventListener('keydown',e=>{if(['ArrowUp','ArrowDown','ArrowLeft','ArrowRight','w','a','s','d'].includes(e.key)){if(e.target.tagName==='SELECT')return;e.preventDefault();keys.add(e.key);}});window.addEventListener('keyup',e=>keys.delete(e.key));window.addEventListener('blur',()=>{keys.clear();pointer=null;});
function aim(e){const r=arena.getBoundingClientRect();pointer={x:(e.clientX-r.left)/r.width,y:(e.clientY-r.top)/r.height};}
arena.addEventListener('pointerdown',e=>{arena.focus();arena.setPointerCapture(e.pointerId);aim(e);});arena.addEventListener('pointermove',e=>{if(arena.hasPointerCapture(e.pointerId))aim(e);});arena.addEventListener('pointerup',()=>pointer=null);arena.addEventListener('pointercancel',()=>pointer=null);
function tick(dt){
  if(encounter.cancelled)return;
  const old={...player};let dx=(keys.has('d')||keys.has('ArrowRight')?1:0)-(keys.has('a')||keys.has('ArrowLeft')?1:0),dy=(keys.has('s')||keys.has('ArrowDown')?1:0)-(keys.has('w')||keys.has('ArrowUp')?1:0);
  if(pointer){dx=pointer.x-player.x;dy=pointer.y-player.y;const dist=Math.hypot(dx,dy);if(dist<.48*dt){player={...pointer};dx=dy=0;}}
  const len=Math.hypot(dx,dy);if(len){player.x+=dx/len*.48*dt;player.y+=dy/len*.48*dt;}
  player.x=Math.max(.025,Math.min(.975,player.x));player.y=Math.max(.29,Math.min(.975,player.y));
  const before=t;t+=dt;sim+=dt;
  // Interpolate the target at crossed lock times, instead of sampling the render frame.
  encounter.advance(t,at=>{const p=Math.max(0,Math.min(1,(at-before)/dt));return{x:old.x+(player.x-old.x)*p,y:old.y+(player.y-old.y)*p};});
  const s=encounter.sample(t,player);cooldown=Math.max(0,cooldown-dt);
  if(cooldown===0&&hit(s,player,.012,old,dt)){hits++;cooldown=.8;}
  if(t>=encounter.duration){t=0;encounter=new Encounter(recipe.value,difficulty.value,++cycle);encounter.advance(0,()=>player);}
}
function line(a,b,color,width,dash=[]){g.strokeStyle=color;g.lineWidth=width*600;g.setLineDash(dash);g.beginPath();g.moveTo(a.x*600,a.y*800);g.lineTo(b.x*600,b.y*800);g.stroke();g.setLineDash([]);}
function circle(p,r,color,fill=false){g.beginPath();g.ellipse(p.x*600,p.y*800,r*600,r*800,0,0,Math.PI*2);g.strokeStyle=color;g.fillStyle=color;g.lineWidth=2;fill?g.fill():g.stroke();}
function reel(context,frame,x,y,size){if(!artReady)return;context.imageSmoothingEnabled=false;context.drawImage(art,frame%4*362,Math.floor(frame/4)*362,362,362,x-size/2,y-size/2,size,size);}
function draw(){
  const s=encounter.sample(t,player);g.clearRect(0,0,600,800);g.fillStyle='#0a1421';g.fillRect(0,0,600,800);
  g.strokeStyle='#172c42';g.lineWidth=1;for(let x=0;x<=600;x+=60){g.beginPath();g.moveTo(x,0);g.lineTo(x,800);g.stroke();}for(let y=0;y<=800;y+=80){g.beginPath();g.moveTo(0,y);g.lineTo(600,y);g.stroke();}
  g.fillStyle='#91a9c6';g.font='14px system-ui';g.fillText('COLLISION SCHEMATIC / NORMALIZED ARENA',18,26);
  for(const w of s.warnings){const amber=w.committed?'#ffe4a3':'#ffb85e';
    if(w.kind==='lane'||w.kind==='fan'){const a=Math.atan2(w.target.y-w.emitter.y,w.target.x-w.emitter.x);line(w.emitter,{x:w.emitter.x+Math.cos(a)*1.5,y:w.emitter.y+Math.sin(a)*1.5},amber,.006,[9,8]);circle(w.target,.025,amber);g.fillStyle=amber;g.fillText(w.committed?'LOCK':'TRACK',w.emitter.x*600+15,w.emitter.y*800);}
    else if(w.kind==='gate'){g.fillStyle='#ffb85e22';g.fillRect(0,128,(w.gapX-w.gap/2)*600,672);g.fillRect((w.gapX+w.gap/2)*600,128,600,672);line({x:w.gapX-w.gap/2,y:.16},{x:w.gapX-w.gap/2,y:1},amber,.003,[8,10]);line({x:w.gapX+w.gap/2,y:.16},{x:w.gapX+w.gap/2,y:1},amber,.003,[8,10]);}
    else if(w.kind==='sweep'){line({x:w.x0,y:.16},{x:w.x0,y:1},amber,w.width,[12,8]);line({x:w.x0,y:.22},{x:w.x1,y:.22},amber,.004,[6,8]);g.fillStyle=amber;g.fillText(w.x1>w.x0?'RAKE →':'← RAKE',210,160);}
    else if(w.kind==='circle'){circle(w.target,w.radius,amber);circle(w.target,w.radius*(1-w.progress),amber);}
    else if(w.kind==='radial'){const a=Math.atan2(w.target.y-w.emitter.y,w.target.x-w.emitter.x);circle(w.emitter,.15,amber);for(const d of [-w.gapAngle,w.gapAngle])line(w.emitter,{x:w.emitter.x+Math.cos(a+d),y:w.emitter.y+Math.sin(a+d)},'#77e2d6',.003,[8,9]);}
  }
  for(const b of s.bullets)circle(b,b.radius,'#ff7975',true);
  for(const b of s.beams){line(b.a,b.b,'#f75863',b.width);line(b.a,b.b,'#ffd3bb',b.width*.25);}
  for(const h of s.hazards)circle(h.center,h.radius,'#ed5656',true);
  for(const f of s.fx)reel(g,f.frame,f.center.x*600,f.center.y*800,110);
  if(!encounter.cancelled){circle({x:.5,y:.16},.023,'#92a4bd');}
  circle(player,.018,cooldown>0?'#fff':'#63e5e7');circle(player,.012,'#63e5e7',true);
  if(s.phase==='recovery'){g.fillStyle='#77e2d6';g.font='bold 25px system-ui';g.fillText('PUNISH WINDOW',190,75);}
  if(encounter.cancelled){g.fillStyle='#77e2d6';g.font='bold 22px system-ui';g.fillText('EMITTER DESTROYED — ATTACKS CLEARED',65,280);}
  document.querySelector('#status').textContent=`${paused?'PAUSED':s.phase.toUpperCase()} · ${t.toFixed(2)}s · cycle ${cycle+1} · hits ${hits} · x ${player.x.toFixed(2)} / y ${player.y.toFixed(2)}`;
  fg.clearRect(0,0,480,180);const frame=Math.floor((performance.now()/1000%1.2)*20)%12;reel(fg,frame,240,90,160);fg.fillStyle='#91a9c6';fg.font='12px system-ui';fg.fillText('Frame '+(frame+1)+' / 12',12,164);
}
function frame(now){const elapsed=last?Math.min(.1,(now-last)/1000):0;last=now;if(!paused){accumulator+=elapsed;while(accumulator>=1/120){tick(1/120);accumulator-=1/120;}}draw();requestAnimationFrame(frame);}
restart();requestAnimationFrame(frame);
