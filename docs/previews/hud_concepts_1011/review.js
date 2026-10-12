'use strict';
// Review-only bitmap composition. This file never imports or changes game state.
const $=s=>document.querySelector(s), W=576, TOP=112, FIELD=512, BOTTOM=160;
let data,font,selected=0,scenario='normal',background='stage6';
const images={},cards=[],checks={draws:0,placements:[],counterSizes:[]};
const examples={normal:{lives:5,missiles:12,roll:1,somer:1,special:.65,speed:3,shield:2,lock:false},
 low:{lives:1,missiles:1,roll:.35,somer:.15,special:.12,speed:3,shield:1,lock:true},
 empty:{lives:0,missiles:0,roll:.05,somer:.3,special:0,speed:3,shield:0,lock:false}};
function loadImage(key,path){return new Promise((resolve,reject)=>{const im=new Image();im.onload=()=>{images[key]=im;resolve(im)};im.onerror=()=>reject(new Error('Image failed: '+path));im.src=path;});}
function measure(text,h){const s=h/font.line_height,space=font.glyphs[' '];return [...String(text).toUpperCase()].reduce((w,ch)=>w+(font.glyphs[ch]||space).x_advance*s,0);}
function text(g,value,x,y,size,maxWidth,align='left'){
 const string=String(value).toUpperCase(),h=Math.min(size,size*maxWidth/Math.max(1,measure(string,size))),sc=h*2/font.line_height,space=font.glyphs[' '];
 let pen=(x-(align==='center'?measure(string,h)/2:align==='right'?measure(string,h):0))*2;
 // Same dense-grid rounding as ph8Text / bmfDrawOn in the native HUD.
 g.save();g.scale(.5,.5);g.imageSmoothingEnabled=false;
 for(const ch of string){const v=font.glyphs[ch];if(v&&v.sprite_rect&&v.sprite_rect[2]){const q=v.sprite_rect,b=v.bounds_in_cell;
  g.drawImage(images.font,...q,Math.round(pen+b[0]*sc),Math.round(y*2-h+b[1]*sc),Math.max(1,Math.round(q[2]*sc)),Math.max(1,Math.round(q[3]*sc)));}
  pen+=(v||space).x_advance*sc;}
 g.restore();return h;
}
function icon(g,key,x,y,size){const im=images[key];g.drawImage(im,x-size/2,y-size/2,size,size);}
function banner(g,v,index,destY,destHeight){
 const b=v.bands[index],bw=b[2]-b[0],bh=b[3]-b[1],scale=Math.min(W/bw,destHeight/bh),ox=(W-bw*scale)/2,oy=destY+(destHeight-bh*scale)/2;
 g.drawImage(images[v.key],b[0],b[1],bw,bh,ox,oy,bw*scale,bh*scale);
 const box=key=>{const r=v.wells[key];return [ox+(r[0]-b[0])*scale,oy+(r[1]-b[1])*scale,r[2]*scale,r[3]*scale];};
 return box;
}
function counter(g,r,key,count,v){
 const [x,y,w,h]=r,cy=y+h/2,n=String(count).padStart(2,'0'),digitSize=Math.min(30,h-4),numberWidth=measure(n,digitSize);
 const label=key==='lives'?'LIVES':'MISSILES',iconSize=Math.min(40,h+4),numX=x+w-8,icx=numX-numberWidth-36;
 const labelMax=Math.max(40,icx-iconSize/2-x-10);
 text(g,label,x+8,cy,14,labelMax);icon(g,key,icx,cy,iconSize);
 text(g,'X',numX-numberWidth-12,cy,12,12,'center');
 const drawn=text(g,n,numX,cy,digitSize,numberWidth+1,'right');
 if(count<=1){g.fillStyle=count===0?'#ff4149':'#ffb345';g.fillRect(x+6,y+h-3,w-12,2);}
 checks.counterSizes.push({concept:v.key,key,size:drawn,count});
}
function meter(g,r,kind,fraction){
 const [x,y,w,h]=r,label=kind==='somer'?'SOMERSAULT':kind.toUpperCase();
 const title=Math.min(14,Math.max(10,h*.36)),bh=Math.min(13,Math.max(7,h*.28)),by=y+h-bh-5;
 text(g,label,x+w/2,y+title/2+4,title,w-10,'center');
 g.fillStyle='#02060c';g.fillRect(x+7,by,w-14,bh);g.strokeStyle='#556475';g.lineWidth=.8;g.strokeRect(x+7,by,w-14,bh);
 if(fraction>0)g.drawImage(images.meters,170,105,4,26,x+8,by+1,(w-16)*fraction,bh-2);
}
function special(g,r,state){
 const [x,y,w,h]=r,thin=h<38,ic=Math.min(24,h*.65),titleY=y+(thin?9:10);
 icon(g,'special',x+ic/2+6,titleY,ic);
 text(g,'NUKE STRIKE MK II',x+ic+10,titleY,12,w-ic-17);
 const bh=thin?8:Math.min(12,h*.24),by=y+h-bh-4;
 g.fillStyle='#02060c';g.fillRect(x+6,by,w-12,bh);g.strokeStyle='#556475';g.lineWidth=.8;g.strokeRect(x+6,by,w-12,bh);
 if(state.special>0)g.drawImage(images.meters,740,130,4,31,x+7,by+1,(w-14)*state.special,bh-2);
 text(g,state.special>0?Math.ceil(state.special*20)+'S · NUKES '+(state.special<.2?1:4):'NO SPECIAL',x+w/2,thin?by+bh/2:y+23,thin?8:10,w-14,'center');
}
function pips(g,r,kind,n){
 const [x,y,w,h]=r,compact=h<24,col=kind==='speed'?'#ffbd47':'#70e5ff';
 const labelH=compact?11:12,start=x+(compact?w*.52:7),by=compact?y+(h-7)/2:y+h-13,bw=compact?w*.43:w-14;
 text(g,kind.toUpperCase(),compact?x+4:x+w/2,compact?y+h/2:y+11,labelH,compact?w*.48:w-8,compact?'left':'center');
 const pw=bw/5;
 for(let i=0;i<5;i++){g.fillStyle=i<n?col:'#233341';g.fillRect(start+i*pw,by,pw-3,8);g.fillStyle=i<n?'#ffffee':'#344452';g.fillRect(start+i*pw,by,pw-3,1);}
}
function weapon(g,r){
 const [x,y,w,h]=r,size=Math.min(60,w-6,h-27),labelH=12;
 icon(g,'weapon',x+w/2,y+(h-labelH)/2,size);
 text(g,'L1 · MG',x+w/2,y+h-10,labelH,w-6,'center');
}
function lock(g,r,active){
 const [x,y,w,h]=r;
 if(h<43){const isize=Math.min(26,h+6);icon(g,'lock',x+isize/2+4,y+h/2,isize);text(g,active?'LOCKED':'NO LOCK',x+w-5,y+h/2,13,w-isize-11,'right');}
 else{icon(g,'lock',x+w/2,y+h*.39,Math.min(40,w-14,h*.48));text(g,active?'LOCKED':'NO LOCK',x+w/2,y+h*.75,14,w-9,'center');}
 if(active){g.strokeStyle='#ff5b49';g.lineWidth=1.5;g.strokeRect(x+2,y+2,w-4,h-4);}
}
function drawStrips(g,v,bottomY,state){
 const t=banner(g,v,0,0,TOP),bottom=banner(g,v,1,bottomY,BOTTOM);
 for(const [key,label,score] of [['score','COLE SCORE','187,450'],['high','HIGH SCORE','750,000']]){
  const [x,y,w,h]=t(key);text(g,label,x+5,y+h/2,10,w*.49);text(g,score,x+w-5,y+h/2,18,w*.49,'right');}
 counter(g,t('lives'),'lives',state.lives,v);counter(g,t('missiles'),'missiles',state.missiles,v);
 meter(g,bottom('roll'),'roll',state.roll);meter(g,bottom('somer'),'somer',state.somer);
 weapon(g,bottom('weapon'));special(g,bottom('special'),state);
 pips(g,bottom('speed'),'speed',state.speed);pips(g,bottom('shield'),'shield',state.shield);
 lock(g,bottom('lock'),state.lock);
 for(const [key,r] of Object.entries(v.wells))checks.placements.push({concept:v.key,key,inBanner:key==='score'||key==='high'||key==='lives'||key==='missiles'?r[1]+r[3]<=v.bands[0][3]:r[1]>=v.bands[1][1]});
}
function paint(canvas,v,hudOnly=false){
 const height=hudOnly?TOP+BOTTOM:TOP+FIELD+BOTTOM;
 canvas.width=W*2;canvas.height=height*2;
 const g=canvas.getContext('2d');g.scale(2,2);g.imageSmoothingEnabled=false;g.fillStyle='#000';g.fillRect(0,0,W,height);
 if(!hudOnly){g.drawImage(images[background],212,59,676,724,(W-480)/2,TOP,480,FIELD);}
 drawStrips(g,v,hudOnly?TOP:TOP+FIELD,examples[scenario]);checks.draws++;
}
function render(){
 if(!data)return;checks.counterSizes=[];checks.placements=[];
 const v=data.layouts[selected];document.documentElement.style.setProperty('--accent',v.accent);
 paint($('#screen'),v);$('#screen').setAttribute('aria-label',`${v.name}. ${examples[scenario].lives} lives, ${examples[scenario].missiles} missiles. No radar.`);
 $('#conceptNumber').textContent=String(v.number).padStart(2,'0');$('#conceptName').textContent=v.name;$('#conceptNote').textContent=v.note;
 $('#livesReadout').textContent=String(examples[scenario].lives).padStart(2,'0');$('#missilesReadout').textContent=String(examples[scenario].missiles).padStart(2,'0');$('#raw').href=v.image;
 document.querySelectorAll('#conceptTabs button').forEach((b,i)=>b.setAttribute('aria-selected',String(i===selected)));
 for(let i=0;i<cards.length;i++){paint(cards[i].canvas,data.layouts[i],true);cards[i].article.classList.toggle('selected',i===selected);}
 window.__hudConceptChecks=checks;
}
function choose(i){selected=i;render();const u=new URL(location.href);u.searchParams.set('concept',data.layouts[i].key);history.replaceState(null,'',u);}
async function init(){
 [data,font]=await Promise.all([fetch('concepts.json').then(r=>r.json()),fetch('command-alloy.json').then(r=>r.json())]);
 const names=['font','lives','missiles','weapon','special','lock','meters','stage1','stage6'],paths=['command-alloy.png','lives.png','missiles.png','weapon.png','special.png','lock.png','authored-meter-source.png','gameplay-stage1.png','gameplay-stage6.png'];
 await Promise.all([...names.map((n,i)=>loadImage(n,paths[i])),...data.layouts.map(v=>loadImage(v.key,v.image))]);
 const requested=new URL(location.href).searchParams.get('concept');selected=Math.max(0,data.layouts.findIndex(v=>v.key===requested));
 data.layouts.forEach((v,i)=>{
  const button=document.createElement('button');button.type='button';button.innerHTML=`<span>CONCEPT ${String(v.number).padStart(2,'0')}</span>${v.name}`;button.onclick=()=>choose(i);$('#conceptTabs').append(button);
  const article=document.createElement('article');article.className='card';const h=document.createElement('h3');h.textContent=String(v.number).padStart(2,'0')+' · '+v.name;article.append(h);
  const canvas=document.createElement('canvas');canvas.setAttribute('aria-label',v.name+' HUD strips without the playfield');article.append(canvas);
  const note=document.createElement('p');note.textContent=v.note;article.append(note);const view=document.createElement('button');view.textContent='View over gameplay';view.onclick=()=>{choose(i);$('#conceptTabs').scrollIntoView({block:'start',behavior:matchMedia('(prefers-reduced-motion:reduce)').matches?'auto':'smooth'});};article.append(view);$('#gallery').append(article);cards.push({article,canvas});
 });
 $('#background').onchange=e=>{background=e.target.value;render()};$('#scenario').onchange=e=>{scenario=e.target.value;render()};
 $('#enlarge').onclick=()=>{const active=document.body.classList.toggle('enlarged');$('#enlarge').setAttribute('aria-pressed',String(active));$('#enlarge').textContent=active?'Standard size':'Enlarge HUD';};
 $('#save').onclick=()=>{const a=document.createElement('a');a.download=data.layouts[selected].key+'-'+scenario+'-mockup.png';a.href=$('#screen').toDataURL('image/png');a.click();};
 render();window.hudConceptReady=true;
}
init().catch(error=>{console.error(error);$('.screen-column').textContent='Preview could not load: '+error.message;});
