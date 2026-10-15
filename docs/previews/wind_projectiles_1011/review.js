"use strict";
const images=new Map(),cards=new Map(),hero=document.querySelector('#hero'),g=hero.getContext('2d');
const select=document.querySelector('#family'),frame=document.querySelector('#frame'),pause=document.querySelector('#pause');
let review,running=true,last=0,elapsed=0;
async function load(a){if(images.has(a.key))return;const im=new Image();im.src='../../../'+a.path+'?v='+a.sha256.slice(0,12);await im.decode();images.set(a.key,im);}
function pose(q,bank,index,cx,cy,k=1,alpha=1){const a=bank[index],im=images.get(a.key);q.save();q.globalAlpha*=alpha;q.imageSmoothingEnabled=false;
 const r=a.draw_rect||[0,0,256,256];q.drawImage(im,...r,cx+(r[0]-a.pivot[0])*k,cy+(r[1]-a.pivot[1])*k,r[2]*k,r[3]*k);q.restore();}
function sample(f,i){return {kind:['mg','spread','missile','beam','flame','orb','lasermist','mg','yuriLightningOrb'][i],_cal50:f==='heavy',_inf:'wind',_infLv:5,lv:5,x:320,y:290,top:60,bot:450,w:f==='gust'?70:24,h:32,t:elapsed,vy:-4};}
function paint(){if(!review)return;const index=Number(frame.value),f=select.value,bank=review.banks[f],i=WP11_FAMILIES.indexOf(f);
 g.clearRect(0,0,640,560);g.fillStyle='#0a1520';g.fillRect(0,0,640,560);
 // Registration crosshairs are review guides, never in-game sprites.
 g.strokeStyle='#24413f';g.lineWidth=1;g.beginPath();g.moveTo(320,24);g.lineTo(320,536);g.moveTo(24,300);g.lineTo(616,300);g.stroke();
 if(document.querySelector('#view').value==='combat'){
  const b=sample(f,i);b.t=(index+.2)/24;wp11Paint(g,bank,k=>images.get(k),b,b.t);
 }else{
  const y=['laser','gust'].includes(f)?440:300;
  if(document.querySelector('#onion').checked)pose(g,bank,(index+15)%16,320,y,1.6,.25);
  pose(g,bank,index,320,y,1.6);
 }
 document.querySelector('#caption').textContent=bank[0].name+' · pose '+String(index+1).padStart(2,'0')+'/16 · 24 fps · 256 × 256 · fixed pivot '+bank[0].pivot.join(', ');
 for(const [name,c] of cards){const q=c.getContext('2d');q.clearRect(0,0,256,256);pose(q,review.banks[name],index,128,['laser','gust'].includes(name)?214:128,.9);}
}
function tick(now){if(last&&running){elapsed+=Math.min(.1,(now-last)/1000);frame.value=String(Math.floor(elapsed*24)%16);}last=now;paint();requestAnimationFrame(tick);}
pause.onclick=()=>{running=!running;pause.textContent=running?'Pause':'Play';};
frame.oninput=()=>{running=false;pause.textContent='Play';elapsed=(Number(frame.value)+.2)/24;paint();};select.onchange=paint;
fetch('review.json',{cache:'no-store'}).then(r=>r.json()).then(async d=>{
 review=d;await Promise.all([...Object.values(d.banks).flat(),...d.icons,d.symbol].map(load));
 const symbol=new Image();symbol.src=images.get(d.symbol.key).src;symbol.alt='Wind elemental reward';const text=document.createElement('p');text.textContent='Stage 6 boss reward: the Wind gust symbol. The upgrade icons use matching green borders and white Roman level tags.';document.querySelector('#reward').append(symbol,text);
 for(const f of WP11_FAMILIES){const bank=d.banks[f],slot=bank[0].slot,opt=document.createElement('option');opt.value=f;opt.textContent=bank[0].name;select.append(opt);
  const card=document.createElement('article'),title=document.createElement('h3'),c=document.createElement('canvas'),p=document.createElement('p'),badges=document.createElement('div');card.className='reel-card';title.textContent=bank[0].name;c.width=c.height=256;p.textContent='16 poses · 24 fps · levels I–V';badges.className='badges';
  for(const a of d.icons.filter(a=>a.slot===slot)){const im=new Image();im.className='badge';im.src=images.get(a.key).src;im.alt=a.name+' level '+a.level;badges.append(im);}
  card.append(title,c,p,badges);card.onclick=()=>{select.value=f;paint();document.querySelector('.viewer').scrollIntoView({behavior:'smooth',block:'start'});};document.querySelector('#reels').append(card);cards.set(f,c);
 }
 for(const a of d.captures){const fig=document.createElement('figure'),im=new Image(),cap=document.createElement('figcaption');im.src=a.path;im.alt=a.family+' native weapon preview';cap.textContent=d.banks[a.family]?.[0].name||'Stage 6 combat';fig.append(im,cap);document.querySelector('#captures').append(fig);}
 window.windReviewReady=true;requestAnimationFrame(tick);
}).catch(e=>{document.querySelector('#caption').textContent=String(e);console.error(e);});
