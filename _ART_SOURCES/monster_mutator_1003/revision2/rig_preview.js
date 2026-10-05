/* Art-only component previews. No game globals, imports or campaign changes. */
const rigState={time:0,paused:false,explode:false,hp:3,death:-1,ready:false,frames:0};
window.mmr2=rigState;
const images={};
function sprite(ctx,img,part,x,y,scale,angle=0,alpha=1){
 const [sx,sy,sw,sh]=part.rect;ctx.save();ctx.translate(x,y);ctx.rotate(angle);ctx.globalAlpha=alpha;
 ctx.drawImage(img,sx,sy,sw,sh,-part.pivot[0]*scale,-part.pivot[1]*scale,sw*scale,sh*scale);ctx.restore();
}
function renderRig(name,t){
 const cv=document.getElementById('rig-'+name),ctx=cv.getContext('2d'),rig=RIGS[name],im=images[name];
 ctx.clearRect(0,0,cv.width,cv.height);ctx.imageSmoothingEnabled=false;
 const split=rigState.explode?1:0,s=rig.scale;
 if(name==='hexpyre'){
  const x=360,y=278+Math.sin(t*2)*3;
  for(let i=0;i<rig.limbs.length;i++){
   const limb=rig.limbs[i],a=limb.side*Math.sin(t*1.8)*.14,lx=x+limb.attach[0]*s+limb.side*split*70,ly=y+limb.attach[1]*s;
   sprite(ctx,im,limb,lx,ly,s,a);
   const px=limb.palm[0]*s,py=limb.palm[1]*s,fx=lx+px*Math.cos(a)-py*Math.sin(a),fy=ly+px*Math.sin(a)+py*Math.cos(a)-split*35;
   sprite(ctx,im,rig.flames[Math.floor(t*10+i)%2],fx,fy,.24+Math.sin(t*14+i)*.012,0,.88+.12*Math.sin(t*9+i));
  }
  sprite(ctx,im,rig.body,x,y,s);
  document.getElementById('hex-phase').textContent=split?'Separated hull · arms · flames':'Independent shoulder rotation · layered flames';
 }else if(name==='riflelocust'){
  const x=360,y=215,cycle=t%4.4;
  for(const pod of rig.pods){
   sprite(ctx,im,pod,x+pod.attach[0]*s+pod.side*split*70,y+pod.attach[1]*s-split*25,s*.88,pod.side*Math.sin(t*1.6)*.045);
  }
  for(const gun of rig.guns){
   const phase=(t+(gun.side>0?.28:0))%4.4;
   const burst=phase>1.6&&phase<3.2;
   const recoil=burst?Math.max(0,1-((phase-1.6)%.32)/.12)*7:0;
   const angle=Math.sin(t*.85+gun.side*.6)*.12;
   sprite(ctx,im,gun,x+gun.attach[0]*s+gun.side*split*75,y+gun.attach[1]*s-recoil+split*25,s,angle);
  }
  sprite(ctx,im,rig.body,x,y,s);
  if(split)sprite(ctx,im,rig.cap,x,455,.22);
  document.getElementById('locust-phase').textContent=split?'Hull · two rifles · two engine pods · spare socket cap':cycle<1.6?'Independent rifles track · hull remains upright':cycle<3.2?'Alternating rifle recoil':'Weapon recovery';
 }else{
  const age=rigState.death<0?-1:Math.min(2,t-rigState.death),cycle=t%3.8;
  let attack=cycle<1.4?0:cycle<2?(cycle-1.4)/.6:cycle<2.22?1-(cycle-2)/.22:0;
  const dash=cycle<2?0:cycle<2.22?(cycle-2)/.22:cycle<3?1-(cycle-2.22)/.78:0;
  const x=360+Math.sin(t*.9)*12,y=236+dash*65,sweep=cycle>=2&&cycle<2.45?Math.sin((cycle-2)/.45*Math.PI):0;
  let index=0;
  const draw=(part,px,py,sc,a=0)=>{
   const n=index++,dead=age>=0,rad=n*Math.PI*2/6;
   sprite(ctx,im,part,px+(dead?Math.cos(rad)*age*170:0),py+(dead?Math.sin(rad)*age*155:0),sc,a+(dead?age*(n%2?2:-2):0),dead?Math.max(0,1-age/1.25):1);
  };
  draw(rig.thruster,x,y+rig.thruster.attach[1]*s-split*40,rig.thruster.scale*(1+dash*.15));
  for(const limb of rig.limbs){
   const a=limb.side*(limb.front?(-attack*.55+sweep*.66):Math.sin(t*4)*.10+attack*.18);
   draw(limb,x+limb.attach[0]*s+limb.side*split*65,y+limb.attach[1]*s+(limb.front?1:-1)*split*35,s*.90,a);
  }
  draw(rig.body,x,y,s);
  document.getElementById('hell-phase').textContent=age>=0?'Core broken · modules scatter':split?'Core · four claws · separate thruster':cycle<1.4?'Stalking':cycle<2?'Claws draw back':cycle<2.22?'Kamikaze lunge':cycle<3?'Recovery':'Reset';
 }
}
function paint(){if(!rigState.ready)return;for(const name of Object.keys(RIGS))renderRig(name,rigState.time);rigState.frames++;}
window.renderMutatorRigs=t=>{rigState.time=t;paint();};
Promise.all(Object.entries(RIGS).map(([name,rig])=>new Promise((resolve,reject)=>{const im=new Image();images[name]=im;im.onload=resolve;im.onerror=()=>reject(new Error('Cannot load '+rig.sheet));im.src=rig.sheet;}))).then(()=>{rigState.ready=true;paint();}).catch(e=>{console.error(e);document.getElementById('hell-phase').textContent='Image load failed';});
let last=performance.now();function frame(now){const dt=Math.min(.05,(now-last)/1000);last=now;if(!rigState.paused)rigState.time+=dt;paint();requestAnimationFrame(frame);}requestAnimationFrame(frame);
document.getElementById('separate').onchange=e=>{rigState.explode=e.target.checked;paint();};
document.getElementById('pause').onclick=e=>{rigState.paused=!rigState.paused;e.target.textContent=rigState.paused?'Resume motion':'Pause motion';};
document.getElementById('hit').onclick=()=>{if(rigState.hp>0){rigState.hp--;if(!rigState.hp)rigState.death=rigState.time;}document.getElementById('hit').textContent=rigState.hp?'Hit core · '+rigState.hp+' hits left':'Core broken';};
document.getElementById('reset').onclick=()=>{rigState.hp=3;rigState.death=-1;document.getElementById('hit').textContent='Hit core · 3 hits left';paint();};
