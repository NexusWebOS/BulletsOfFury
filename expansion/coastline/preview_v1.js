'use strict';
const canvas=document.getElementById('map'),ctx=canvas.getContext('2d');
const view={x:0,y:0,z:1,ready:false,selected:0};
const clean=new Image(),route=new Image();
let cw=0,ch=0,drag=null,images=0;
function imageLoaded(){if(++images===2){view.ready=true;resize();fit();}}
clean.onload=route.onload=imageLoaded;
clean.src='assets/connecting_map_clean.png';route.src='assets/connecting_map_route.png';
function resize(){const r=canvas.getBoundingClientRect();cw=r.width;ch=r.height;const dpr=Math.min(devicePixelRatio||1,2);canvas.width=Math.round(cw*dpr);canvas.height=Math.round(ch*dpr);ctx.setTransform(dpr,0,0,dpr,0,0);draw();}
function clamp(){view.z=Math.max(Math.min(cw/2560,ch/1280)*.8,Math.min(2,view.z));const w=2560*view.z,h=1280*view.z;view.x=w<cw?(cw-w)/2:Math.min(0,Math.max(cw-w,view.x));view.y=h<ch?(ch-h)/2:Math.min(0,Math.max(ch-h,view.y));}
function draw(){ctx.fillStyle='#031a35';ctx.fillRect(0,0,cw,ch);if(!view.ready)return;clamp();ctx.imageSmoothingEnabled=false;ctx.drawImage(document.getElementById('route').checked?route:clean,view.x,view.y,2560*view.z,1280*view.z);const pt=COAST_MANIFEST.mapLayout.nodes[view.selected===0?'od01':'od02'];ctx.beginPath();ctx.arc(view.x+pt[0]*view.z,view.y+pt[1]*view.z,32*view.z,0,Math.PI*2);ctx.strokeStyle='#fff2bc';ctx.lineWidth=2;ctx.stroke();}
function fit(){view.z=Math.min(cw/2560,ch/1280);view.x=(cw-2560*view.z)/2;view.y=(ch-1280*view.z)/2;document.getElementById('full').classList.add('active');document.getElementById('coast').classList.remove('active');draw();}
function coast(){view.z=Math.min(cw/1100,ch/760);view.x=cw/2-480*view.z;view.y=ch/2-650*view.z;document.getElementById('coast').classList.add('active');document.getElementById('full').classList.remove('active');draw();}
function zoom(f,x=cw/2,y=ch/2){const old=view.z;view.z*=f;view.z=Math.min(2,Math.max(Math.min(cw/2560,ch/1280)*.8,view.z));view.x=x-(x-view.x)*view.z/old;view.y=y-(y-view.y)*view.z/old;draw();}
document.getElementById('full').onclick=fit;document.getElementById('coast').onclick=coast;document.getElementById('zoomIn').onclick=()=>zoom(1.25);document.getElementById('zoomOut').onclick=()=>zoom(.8);document.getElementById('route').onchange=draw;
canvas.addEventListener('wheel',e=>{e.preventDefault();const r=canvas.getBoundingClientRect();zoom(e.deltaY<0?1.12:.89,e.clientX-r.left,e.clientY-r.top);},{passive:false});
canvas.addEventListener('pointerdown',e=>{drag={x:e.clientX,y:e.clientY,ox:view.x,oy:view.y,moved:false};canvas.setPointerCapture(e.pointerId);canvas.classList.add('dragging');});
canvas.addEventListener('pointermove',e=>{if(!drag)return;const dx=e.clientX-drag.x,dy=e.clientY-drag.y;if(Math.abs(dx)+Math.abs(dy)>5)drag.moved=true;view.x=drag.ox+dx;view.y=drag.oy+dy;draw();});
canvas.addEventListener('pointerup',e=>{if(drag&&!drag.moved){const r=canvas.getBoundingClientRect(),x=(e.clientX-r.left-view.x)/view.z,y=(e.clientY-r.top-view.y)/view.z;Object.values(COAST_MANIFEST.mapLayout.nodes).forEach((p,i)=>{if(Math.hypot(x-p[0],y-p[1])<50/view.z)select(i);});}drag=null;canvas.classList.remove('dragging');});
canvas.addEventListener('pointercancel',()=>{drag=null;canvas.classList.remove('dragging');});
function select(index){view.selected=index;const m=COAST_STORY.missions[index];document.querySelectorAll('.mission').forEach((b,i)=>{b.classList.toggle('active',i===index);b.setAttribute('aria-pressed',String(i===index));});document.getElementById('mode').textContent='LEVEL 0'+m.number+' / '+m.mode.toUpperCase();document.getElementById('missionTitle').textContent=index===0?'Make it to the compound.':'Take the north gate.';document.getElementById('objective').textContent=m.objective;document.getElementById('beats').replaceChildren(...m.beats.map(t=>{const li=document.createElement('li');li.textContent=t;return li;}));document.getElementById('dialogue').replaceChildren(...m.dialogueDraft.map(d=>{const p=document.createElement('p');if(d.event){p.className='event';p.textContent=d.event;}else{const b=document.createElement('strong');b.textContent=d.speaker+': ';p.append(b,document.createTextNode(d.line));}return p;}));draw();}
document.querySelectorAll('.mission').forEach(b=>b.onclick=()=>select(Number(b.dataset.mission)));
window.addEventListener('resize',()=>{resize();fit();});select(0);
