"use strict";
(() => {
 const $=id=>document.getElementById(id),images={},W=2048,H=1152,K=.75;
 const state={selected:0,scene:'gameplay',stocks:'normal',motion:!matchMedia('(prefers-reduced-motion: reduce)').matches,ready:false,time:0};
 const examples={normal:{lives:3,missiles:12,roll:1,somer:1,special:.8,lock:false},low:{lives:1,missiles:1,roll:.42,somer:.16,special:.18,lock:true},empty:{lives:0,missiles:0,roll:0,somer:0,special:0,lock:false}};
 const canvas=$('preview'),g=canvas.getContext('2d');let data,font,last=0;
 const placements=[];
 function load(key,path){return new Promise((resolve,reject)=>{const im=new Image();im.onload=()=>{images[key]=im;resolve(im);};im.onerror=()=>reject(Error('Unable to load '+path));im.src=path;});}
 function measure(value,size){return [...String(value).toUpperCase()].reduce((s,ch)=>s+(font.glyphs[ch]||font.glyphs[' ']).x_advance,0)*size/font.line_height;}
 function text(ctx,value,x,y,size,maxWidth,align='center'){
  const str=String(value).toUpperCase(),actual=Math.min(size,size*maxWidth/Math.max(1,measure(str,size))),k=actual/font.line_height;
  let px=x-(align==='center'?measure(str,actual)/2:align==='right'?measure(str,actual):0);
  for(const ch of str){const q=font.glyphs[ch],sp=font.glyphs[' '];if(q?.sprite_rect?.[2]){const r=q.sprite_rect,b=q.bounds_in_cell;ctx.drawImage(images.font,...r,Math.round(px+b[0]*k),Math.round(y-actual/2+b[1]*k),Math.max(1,Math.round(r[2]*k)),Math.max(1,Math.round(r[3]*k)));}px+=(q||sp).x_advance*k;}
  return actual;
 }
 function icon(ctx,key,x,y,size){const im=images[key],k=size/Math.max(im.width,im.height);ctx.drawImage(im,x-im.width*k/2,y-im.height*k/2,im.width*k,im.height*k);}
 function well(v,key){const r=v.wells[key],right=r[0]>512;return [(right?1614:50)+(r[0]-(right?512:0))*K,r[1]*K,r[2]*K,r[3]*K];}
 function inside(ctx,rect,fn){ctx.save();ctx.beginPath();ctx.rect(rect[0]+6,rect[1]+5,rect[2]-12,rect[3]-10);ctx.clip();fn(...rect);ctx.restore();}
 function bar(ctx,r,frac,red=false){const [x,y,w,h]=r;ctx.save();ctx.beginPath();ctx.rect(x+4,y+3,(w-8)*Math.max(0,Math.min(1,frac)),h-6);ctx.clip();ctx.drawImage(images.meters,red?740:170,red?130:105,4,red?31:26,x+4,y+3,w-8,h-6);ctx.restore();}
 function render(ctx,index,scene,stocks,clock=0){
  const v=data.concepts[index],s=examples[stocks];ctx.clearRect(0,0,W,H);ctx.imageSmoothingEnabled=false;
  ctx.fillStyle='#070b10';ctx.fillRect(0,0,W,H);
  const field=data.playfield;ctx.drawImage(images[scene],...field);
  ctx.drawImage(images[v.id],0,0,512,1536,50,0,384,H);
  ctx.drawImage(images[v.id],512,0,512,1536,1614,0,384,H);
  placements.push({concept:v.id,scene,field:[...field],scale:field[2]/480});if(placements.length>120)placements.shift();
  inside(ctx,well(v,'scores'),(x,y,w,h)=>{text(ctx,'COLE SCORE',x+w/2,y+h*.16,20,w-18);text(ctx,'187,450',x+w/2,y+h*.43,36,w-22);text(ctx,'HIGH SCORE',x+w*.30,y+h*.75,14,w*.48);text(ctx,'750,000',x+w*.76,y+h*.75,20,w*.45);});
  for(const [key,label,frac] of [['roll','ROLL',s.roll],['somer','SOMERSAULT',s.somer]]){
   inside(ctx,well(v,key),(x,y,w,h)=>{text(ctx,label,x+w/2,y+h*.22,18,w-16);text(ctx,frac===1?'READY':Math.round(frac*100)+'%',x+w/2,y+h*.59,26,w-18);});
   bar(ctx,well(v,key+'Bar'),frac);
  }
  inside(ctx,well(v,'weapon'),(x,y,w,h)=>{text(ctx,'EQUIPPED WEAPON',x+w/2,y+22,18,w-26);icon(ctx,'weapon',x+w/2,y+h*.47,Math.min(122,w*.52));text(ctx,'MACHINE GUN',x+w/2,y+h*.77,22,w-26);text(ctx,'LEVEL 01',x+w/2,y+h*.9,18,w-30);});
  for(const [key,f] of [['speed',.6],['shield',.8]])inside(ctx,well(v,key),(x,y,w,h)=>{text(ctx,key,x+8,y+h/2,17,w*.36,'left');bar(ctx,[x+w*.4,y+6,w*.55,h-12],f,key==='shield');});
  inside(ctx,well(v,'pilot'),(x,y,w,h)=>{text(ctx,'COLE / FURY FLIGHT',x+w/2,y+h*.19,19,w-25);icon(ctx,'lives',x+w/2,y+h*.5,64);text(ctx,scene==='fly-in'?'APPROACH':scene==='continue'?'STANDBY':'STAGE 01',x+w/2,y+h*.8,20,w-28);});
  inside(ctx,well(v,'radar'),(x,y,w,h)=>{
   text(ctx,'RADAR',x+w/2,y+20,20,w-22);const cx=x+w/2,cy=y+h*.57,r=Math.min(w*.38,h*.34);
   ctx.lineWidth=1.5;ctx.strokeStyle='#285750';
   for(const a of [1,.67,.33]){ctx.beginPath();ctx.arc(cx,cy,r*a,0,Math.PI*2);ctx.stroke();}
   ctx.beginPath();ctx.moveTo(cx-r,cy);ctx.lineTo(cx+r,cy);ctx.moveTo(cx,cy-r);ctx.lineTo(cx,cy+r);ctx.stroke();
   const angle=clock*.75-.7;ctx.strokeStyle='#71e2a8';ctx.beginPath();ctx.moveTo(cx,cy);ctx.lineTo(cx+Math.cos(angle)*r,cy+Math.sin(angle)*r);ctx.stroke();
   for(const q of [[-.45,-.5],[.30,-.7],[.67,.0]]){ctx.fillStyle='#ff8754';ctx.fillRect(cx+q[0]*r-3,cy+q[1]*r-3,6,6);}ctx.fillStyle='#c0ffd8';ctx.fillRect(cx-4,cy+r*.65-4,8,8);
   text(ctx,'3 CONTACTS',cx,y+h-15,14,w-20);
  });
  inside(ctx,well(v,'special'),(x,y,w,h)=>{text(ctx,'SPECIAL ABILITY',x+w/2,y+21,18,w-22);icon(ctx,'special',x+w/2,y+h*.45,Math.min(98,w*.5));text(ctx,'NUKE STRIKE',x+w/2,y+h*.77,23,w-22);text(ctx,s.special?'READY / HOLD':'RECHARGING',x+w/2,y+h*.9,15,w-24);});
  bar(ctx,well(v,'specialBar'),s.special,true);
  for(const key of ['lives','missiles'])inside(ctx,well(v,key),(x,y,w,h)=>{text(ctx,key,x+w/2,y+h*.16,16,w-10);icon(ctx,key,x+w*.24,y+h*.58,38);const n=String(s[key]).padStart(2,'0');text(ctx,n,x+w*.67,y+h*.6,48,w*.57);if(s[key]<=1){ctx.fillStyle=s[key]?'#ffbd45':'#ff4b4b';ctx.fillRect(x+8,y+h-12,w-16,3);}});
  inside(ctx,well(v,'lock'),(x,y,w,h)=>{text(ctx,'RETINA LOCK',x+w/2,y+h*.15,19,w-26);icon(ctx,'lock',x+w/2,y+h*.48,Math.min(68,h*.46));text(ctx,s.lock?'TARGET LOCKED':'NO LOCK',x+w/2,y+h*.82,23,w-24);});
  if(s.lock){const [x,y,w,h]=well(v,'lock');ctx.strokeStyle='#ff794f';ctx.lineWidth=3;ctx.strokeRect(x+7,y+7,w-14,h-14);}
 }
 function draw(){if(!state.ready)return;render(g,state.selected,state.scene,state.stocks,state.time);}
 function select(index){state.selected=Math.max(0,Math.min(4,index));const v=data.concepts[state.selected];$('number').textContent='0'+v.number+' / 05';$('conceptTitle').textContent=v.name;$('note').textContent=v.note;
  for(const b of $('concepts').children)b.setAttribute('aria-pressed',String(Number(b.dataset.index)===state.selected));const url=new URL(location.href);url.searchParams.set('concept',v.id);history.replaceState(null,'',url);draw();}
 function scene(name){state.scene=name;for(const b of document.querySelectorAll('[data-scene]'))b.setAttribute('aria-pressed',String(b.dataset.scene===name));draw();}
 function snapshots(){return data.concepts.map((v,i)=>{const c=document.createElement('canvas');c.width=W;c.height=H;render(c.getContext('2d'),i,'gameplay','normal',1.2);return {id:v.id,url:c.toDataURL('image/png')};});}
 async function init(){
  data=await fetch('concepts.json').then(r=>r.json());font=await fetch('../hud_concepts_1011/command-alloy.json').then(r=>r.json());
  await Promise.all([...data.concepts.map(v=>load(v.id,v.path)),...['gameplay','fly-in','continue'].map(k=>load(k,k+'.png')),
   ...['weapon','special','lives','missiles','lock'].map(k=>load(k,'../hud_concepts_1011/'+k+'.png')),
   load('font','../hud_concepts_1011/command-alloy.png'),load('meters','../hud_concepts_1011/authored-meter-source.png')]);
  for(const [i,v] of data.concepts.entries()){const b=document.createElement('button');b.type='button';b.dataset.index=i;b.innerHTML='<small>0'+v.number+'</small><span>'+v.name+'</span>';b.onclick=()=>select(i);$('concepts').append(b);}
  state.ready=true;for(const [i,q] of snapshots().entries()){const v=data.concepts[i],b=document.createElement('button');b.type='button';b.className='card';b.dataset.index=i;const im=document.createElement('img');im.src=q.url;im.alt=v.name+' side HUD concept';const copy=document.createElement('div'),title=document.createElement('strong'),note=document.createElement('span');title.textContent='0'+v.number+' / '+v.name;note.textContent=v.note;copy.append(title,note);b.append(im,copy);b.onclick=()=>{select(i);$('conceptTitle').scrollIntoView({behavior:'smooth',block:'start'});};$('gallery').append(b);}
  const chosen=data.concepts.findIndex(v=>v.id===new URLSearchParams(location.search).get('concept'));select(Math.max(0,chosen));$('status').textContent='Five generated plates loaded · Native game icons and font · 2048 × 1152 preview · Review only';
 }
 for(const b of document.querySelectorAll('[data-scene]'))b.onclick=()=>scene(b.dataset.scene);
 $('stocks').onchange=e=>{state.stocks=e.target.value;draw();};$('motion').checked=state.motion;$('motion').onchange=e=>{state.motion=e.target.checked;};
 $('full').onclick=async()=>{if(document.fullscreenElement)await document.exitFullscreen();else await $('screen').requestFullscreen();};
 $('download').onclick=()=>{if(!state.ready)return;const a=document.createElement('a');a.download=data.concepts[state.selected].id+'-'+state.scene+'.png';a.href=canvas.toDataURL();a.click();};
 window.SIDE_HUD_REVIEW={state,select,scene,draw,placements,snapshots,field:()=>data.playfield};
 init().catch(e=>{$('status').textContent=e.message;$('status').className='error';console.error(e);});
 function tick(now){const dt=last?Math.min(.1,(now-last)/1000):0;last=now;if(state.ready&&state.motion&&!document.hidden){state.time+=dt;draw();}requestAnimationFrame(tick);}requestAnimationFrame(tick);
})();
