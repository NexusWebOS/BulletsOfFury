'use strict';
const canvas=document.getElementById('map'),ctx=canvas.getContext('2d'),layout=COAST_MANIFEST.mapLayout;
const [MW,MH]=layout.canvas,imgs=new Map();
const view={x:0,y:0,z:1,selected:0,ready:false,time:0,focus:'full'},nodeHits=[];
let cw=0,ch=0,drag=null,last=0,drawAt=0;
const assetFiles=new Map(COAST_MANIFEST.assets.map(a=>[a.id,a.file]));
const spriteFile=id=>assetFiles.get(id);
const files=new Set([layout.baseImage,...layout.nodes.map(n=>n.file),...layout.ambient.map(a=>spriteFile(a.sprite)),...COAST_MANIFEST.assets.filter(a=>a.id.startsWith('nss_')).map(a=>a.file)]);
Promise.all([...files].map(file=>new Promise((resolve,reject)=>{const im=new Image();im.onload=()=>{imgs.set(file,im);resolve();};im.onerror=()=>reject(Error('Missing image: '+file));im.src=file;}))).then(()=>{view.ready=true;resize();focus('comet');requestAnimationFrame(tick);}).catch(e=>{document.getElementById('mapStatus').textContent=e.message;});
function resize(){const r=canvas.getBoundingClientRect();cw=r.width;ch=r.height;const dpr=Math.min(devicePixelRatio||1,2);canvas.width=Math.round(cw*dpr);canvas.height=Math.round(ch*dpr);ctx.setTransform(dpr,0,0,dpr,0,0);draw();}
function clamp(){view.z=Math.max(Math.min(cw/MW,ch/MH)*.8,Math.min(2.4,view.z));const w=MW*view.z,h=MH*view.z;view.x=w<cw?(cw-w)/2:Math.min(0,Math.max(cw-w,view.x));view.y=h<ch?(ch-h)/2:Math.min(0,Math.max(ch-h,view.y));}
function focus(which){view.focus=which;const [x,y,w,h]=layout.focusBoxes[which];view.z=Math.min(cw/w,ch/h);view.x=cw/2-(x+w/2)*view.z;view.y=ch/2-(y+h/2)*view.z;document.querySelectorAll('[data-focus]').forEach(b=>{b.classList.toggle('active',b.dataset.focus===which);b.setAttribute('aria-pressed',String(b.dataset.focus===which));});draw();}
function zoom(f,x=cw/2,y=ch/2){const old=view.z;view.z=Math.min(2.4,Math.max(Math.min(cw/MW,ch/MH)*.8,old*f));view.x=x-(x-view.x)*view.z/old;view.y=y-(y-view.y)*view.z/old;draw();}
function blit(file,x,y,w,h){const im=imgs.get(file);if(im)ctx.drawImage(im,x,y,w,h);}
function ambient(a){const {x,y,angle}=COAST_MOTION.pose(a,view.time);const [w,h]=a.size;ctx.save();ctx.translate(x,y);if(a.type==='drone'){ctx.fillStyle='#00101b77';ctx.beginPath();ctx.ellipse(14,18,w*.32,h*.2,0,0,Math.PI*2);ctx.fill();}ctx.rotate(angle);ctx.globalAlpha=a.type==='cloud'?.88:1;blit(spriteFile(a.sprite),-w/2,-h/2,w,h);ctx.restore();}
function flagKey(n,selected){const state=document.getElementById('flagState').value;if(state==='locked'&&n.number===2)return 'nss_flag2_lock';if(state==='cleared'&&n.number===1)return 'nss_flag1_done';return 'nss_flag'+n.number+(selected?'_hi'+(Math.floor(view.time*6)%2):'_av');}
function draw(){ctx.fillStyle='#031a35';ctx.fillRect(0,0,cw,ch);if(!view.ready)return;clamp();ctx.imageSmoothingEnabled=false;ctx.save();ctx.translate(view.x,view.y);ctx.scale(view.z,view.z);blit(layout.baseImage,0,0,MW,MH);
if(document.getElementById('route').checked){const p=new Path2D(layout.flightRoute);ctx.strokeStyle='#041a33';ctx.lineWidth=12;ctx.stroke(p);ctx.setLineDash([13,16]);ctx.lineDashOffset=-view.time*12;ctx.strokeStyle='#82e1e3';ctx.lineWidth=4;ctx.stroke(p);ctx.setLineDash([]);}
if(document.getElementById('objects').checked)layout.ambient.filter(a=>a.type==='boat').forEach(ambient);
for(const f of layout.originalFlags){const s=Math.max(1,.45/view.z);blit(spriteFile('nss_flag'+f.number+'_av'),f.at[0]-20*s,f.at[1]-48*s,40*s,48*s);}
nodeHits.length=0;
layout.nodes.forEach((n,i)=>{const bob=Math.sin(view.time*1.7+i*1.5)*7,selected=i===view.selected,extra=selected?5:0,x=n.center[0],y=n.center[1]+bob-extra;ctx.fillStyle='#00101677';ctx.beginPath();ctx.ellipse(n.ground[0],n.ground[1]-38,n.size*.38,22,0,0,Math.PI*2);ctx.fill();blit(n.file,x-n.size/2,y-n.size/2,n.size,n.size);const scale=Math.max(1.5,.78/view.z),fw=40*scale,fh=48*scale,fx=n.flag[0]-fw/2,fy=n.flag[1]-fh+bob-extra;blit(spriteFile(flagKey(n,selected)),fx,fy,fw,fh);nodeHits.push({x:x-n.size/2,y:y-n.size/2,w:n.size,h:n.size,i});if(selected){ctx.strokeStyle='#ff5e57';ctx.lineWidth=1.5/view.z;const cx=fx+fw*.55,cy=fy+fh*.45,r=8/view.z;ctx.beginPath();ctx.arc(cx,cy,r,0,Math.PI*2);ctx.moveTo(cx-r-4/view.z,cy);ctx.lineTo(cx+r+4/view.z,cy);ctx.moveTo(cx,cy-r-4/view.z);ctx.lineTo(cx,cy+r+4/view.z);ctx.stroke();}});
if(document.getElementById('objects').checked)layout.ambient.filter(a=>a.type==='drone').forEach(ambient);
if(document.getElementById('clouds').checked)layout.ambient.filter(a=>a.type==='cloud').forEach(ambient);
ctx.restore();}
function tick(now){if(last&&document.getElementById('motion').checked)view.time+=Math.min((now-last)/1000,.06);last=now;if(now-drawAt>32){draw();drawAt=now;}requestAnimationFrame(tick);}
document.querySelectorAll('[data-focus]').forEach(b=>b.onclick=()=>focus(b.dataset.focus));
document.getElementById('zoomIn').onclick=()=>zoom(1.25);document.getElementById('zoomOut').onclick=()=>zoom(.8);
for(const id of ['route','objects','clouds','motion','flagState'])document.getElementById(id).onchange=draw;
if(matchMedia('(prefers-reduced-motion: reduce)').matches)document.getElementById('motion').checked=false;
canvas.addEventListener('wheel',e=>{e.preventDefault();const r=canvas.getBoundingClientRect();zoom(e.deltaY<0?1.12:.89,e.clientX-r.left,e.clientY-r.top);},{passive:false});
canvas.addEventListener('pointerdown',e=>{drag={x:e.clientX,y:e.clientY,ox:view.x,oy:view.y,moved:false};canvas.setPointerCapture(e.pointerId);canvas.classList.add('dragging');});
canvas.addEventListener('pointermove',e=>{if(!drag)return;const dx=e.clientX-drag.x,dy=e.clientY-drag.y;if(Math.abs(dx)+Math.abs(dy)>5)drag.moved=true;view.x=drag.ox+dx;view.y=drag.oy+dy;draw();});
canvas.addEventListener('pointerup',e=>{if(drag&&!drag.moved){const r=canvas.getBoundingClientRect(),x=(e.clientX-r.left-view.x)/view.z,y=(e.clientY-r.top-view.y)/view.z;const h=nodeHits.find(p=>x>=p.x&&x<=p.x+p.w&&y>=p.y&&y<=p.y+p.h);if(h)select(h.i);}drag=null;canvas.classList.remove('dragging');});
canvas.addEventListener('pointercancel',()=>{drag=null;canvas.classList.remove('dragging');});
function select(index){view.selected=index;const m=COAST_STORY.missions[index];document.querySelectorAll('.mission').forEach((b,i)=>{b.classList.toggle('active',i===index);b.setAttribute('aria-pressed',String(i===index));});document.getElementById('mode').textContent='SECTION 0'+m.number+' / '+m.mode.toUpperCase();document.getElementById('missionTitle').textContent=index===0?'Make it to the compound.':'Take the north gate.';document.getElementById('objective').textContent=m.objective;document.getElementById('beats').replaceChildren(...m.beats.map(t=>{const li=document.createElement('li');li.textContent=t;return li;}));document.getElementById('dialogue').replaceChildren(...m.dialogueDraft.map(d=>{const p=document.createElement('p');if(d.event){p.className='event';p.textContent=d.event;}else{const b=document.createElement('strong');b.textContent=d.speaker+': ';p.append(b,document.createTextNode(d.line));}return p;}));draw();}
document.querySelectorAll('.mission').forEach(b=>b.onclick=()=>select(Number(b.dataset.mission)));
const gallery=document.getElementById('objectGallery');
for(const a of COAST_MANIFEST.assets.filter(a=>['Independent ambient map object','Separate southern island','Separate northwest causeway','Northwest city region','Comet-struck coastal region','Corrupted coastal surround'].includes(a.role))){const figure=document.createElement('figure'),link=document.createElement('a'),im=document.createElement('img'),cap=document.createElement('figcaption');link.href=a.file;link.target='_blank';im.src=a.file;im.alt=a.id.replaceAll('_',' ');cap.textContent=im.alt;link.append(im);figure.append(link,cap);gallery.append(figure);}
window.addEventListener('resize',()=>{resize();focus(view.focus);});select(0);
