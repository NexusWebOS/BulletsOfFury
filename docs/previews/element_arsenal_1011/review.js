'use strict';
const $=s=>document.querySelector(s),order=['fire','kinetic','lightning','water','ice','chrome','toxic','dark','wind'];
const labels=['FIRE','SONIC','LIGHTNING','WATER','ICE','CHROMIUM','TOXIC','DARK MATTER','WIND'];
const colors=['#ff884d','#ffce78','#81b5ff','#56ceff','#a1eaff','#d8e5f6','#b1eb63','#c09cff','#79e1b3'];
const carriers=['MACHINE GUN','SPREAD','MISSILES','LASER','SPRAY','ORB','MIST','CHAINGUN','YURI SPHERE'];
let selected='fire',slot=0,paused=false,frame=0,elapsed=0,last=0,ready=false,engine,manifest,images={},familyData;
for(const [i,el]of order.entries()){
 const b=document.createElement('button');b.type='button';b.dataset.element=el;b.innerHTML=`<canvas width="48" height="48" aria-hidden="true"></canvas>${labels[i]}`;b.addEventListener('click',()=>choose(el));$('#families').append(b);
}
for(let w=0;w<9;w++){
 const b=document.createElement('button');b.className='weapon';b.type='button';b.dataset.weapon=w;b.innerHTML=`<canvas width="88" height="72" aria-hidden="true"></canvas><strong></strong><span>${carriers[w]}</span>`;b.addEventListener('click',()=>{slot=w;refreshWeapon();});$('#weapons').append(b);
}
function call(code){return engine.eval(code);}
function pixels(canvas,key){
 const d=call(`(()=>{const k=${JSON.stringify(key)};if(!XART.rdy(k))return null;const im=XART.get(k);ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,88,72);const s=Math.min(84/im.width,68/im.height);ctx.drawImage(im,(88-im.width*s)/2,(72-im.height*s)/2,im.width*s,im.height*s);const out=ctx.getImageData(0,0,88,72);ctx.restore();return out;})()`);
 if(d){const c=document.createElement('canvas');c.width=88;c.height=72;c.getContext('2d').putImageData(d,0,0);const g=canvas.getContext('2d');g.clearRect(0,0,canvas.width,canvas.height);g.imageSmoothingEnabled=false;g.drawImage(c,0,0,canvas.width,canvas.height);return true;}return false;
}
function refreshWeapon(){
 if(!ready)return;
 const names=call(`FORGE_NAMES[${JSON.stringify(selected)}]`);
 $('#weaponName').textContent=names[slot];
 for(const b of document.querySelectorAll('.weapon')){b.setAttribute('aria-pressed',String(+b.dataset.weapon===slot));b.querySelector('strong').textContent=names[+b.dataset.weapon];}
 call(`window.ARSENAL_PREVIEW=forgePreviewNew(${slot},${JSON.stringify(selected)},${+$('#tier').value});`);
 paintIcons();
}
function paintIcons(){
 if(!ready)return;let done=true;
 for(const b of document.querySelectorAll('nav button'))done=pixels(b.querySelector('canvas'),'inf_'+b.dataset.element)&&done;
 for(const b of document.querySelectorAll('.weapon'))done=pixels(b.querySelector('canvas'),call(`forgeBadgeKey(${JSON.stringify(selected)},${+b.dataset.weapon},1)`))&&done;
 if(!done)setTimeout(paintIcons,150);
}
function choose(el){
 selected=el;document.documentElement.style.setProperty('--accent',colors[order.indexOf(el)]);
 for(const b of document.querySelectorAll('nav button'))b.setAttribute('aria-pressed',String(b.dataset.element===el));
 $('#familyName').textContent=labels[order.indexOf(el)];
 if(ready){$('#effect').textContent=familyData[el].effect;$('#unlock').textContent='STAGE '+familyData[el].stage+' REWARD';refreshWeapon();}
 $('.windlink').style.display=el==='wind'?'block':'none';
 $('#proof').innerHTML=[0,4,5].map(w=>`<figure style="margin:0"><img src="proof/${el}-${w}.webp" alt="${labels[order.indexOf(el)]} ${carriers[w]} hitting native enemies" loading="lazy"><figcaption><small>${carriers[w]}</small></figcaption></figure>`).join('');
}
$('#tier').addEventListener('change',refreshWeapon);
$('#pause').addEventListener('click',()=>{paused=!paused;$('#pause').textContent=paused?'Play':'Pause';});
$('#frame').addEventListener('input',()=>{paused=true;$('#pause').textContent='Play';frame=+$('#frame').value;elapsed=frame/24;});
function ammo(kind){
 const c=$('#'+kind),g=c.getContext('2d');g.clearRect(0,0,256,256);g.imageSmoothingEnabled=false;
 if(!manifest)return;
 if(selected==='wind'){
  if(ready){const data=call(`(()=>{ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,256,256);const b={kind:${JSON.stringify(kind==='round'?'mg':'missile')},x:128,y:100,vx:0,vy:-6,w:16,h:24,lv:3,t:${frame/24},_visualAge:${frame/24},_inf:'wind'};wp11Draw(b);const out=ctx.getImageData(0,0,256,256);ctx.restore();return out;})()`);g.putImageData(data,0,0);}return;
 }
 const key=selected+'_'+kind,a=manifest.banks[key],im=images[key];if(!im?.complete||!im.naturalWidth)return;
 const draw=(f,alpha)=>{g.globalAlpha=alpha;g.drawImage(im,...a.frames[(f+16)%16],0,0,256,256);};
 if($('#onion').checked){draw(frame-1,.25);draw(frame+1,.25);draw(frame,.65);}else draw(frame,1);g.globalAlpha=1;
}
function animate(t){
 const dt=Math.min(.05,(t-last)/1000||0);last=t;
 try{
  if(!paused){elapsed+=dt;frame=Math.floor(elapsed*24)%16;$('#frame').value=frame;}
  $('#frameLabel').textContent='FRAME '+String(frame+1).padStart(2,'0')+' / 16';ammo('round');ammo('missile');
  if(ready){const d=call(`(()=>{const P=ARSENAL_PREVIEW;if(!${paused})forgePreviewTick(P,360,470,${dt});ctx.save();ctx.setTransform(1,0,0,1,0,0);forgePreviewDraw(P,0,0,360,470);const out=ctx.getImageData(0,0,360,470);ctx.restore();if(P.err)throw Error(P.err);return out;})()`);$('#live').getContext('2d').putImageData(d,0,0);}
 }catch(e){$('#status').textContent='Preview error: '+e.message;console.error(e);ready=false;}
 requestAnimationFrame(animate);
}
async function boot(){
 manifest=await(await fetch('../../../assets/game/shared/player_weapons/element_arsenal_1011/manifest.json')).json();
 for(const [key,a]of Object.entries(manifest.banks)){const im=new Image();im.src='../../../'+a.path;images[key]=im;}
 engine=$('#engine').contentWindow;
 await new Promise((resolve,reject)=>{let n=0;const poll=()=>{try{if(call('window.__bofFrames>4 && typeof PA11!=="undefined"'))return resolve();}catch(_){}if(++n>600)return reject(Error('Game did not load'));setTimeout(poll,100);};poll();});
 call(`window.requestAnimationFrame=()=>0;run.pilot='cole';run.stage=1;beginStage(1);setState(GS.PLAY);player.reset();BOFCinematicDirector.cancel();story=fb2Talk=null;for(const k of Object.keys(Audio.SFX))Audio.SFX[k]=()=>{};Snd.loopOn=Snd.loopOff=()=>{};`);
 familyData=call('EA11_FAMILIES');ready=true;choose(selected);$('#status').textContent='Live renderer ready · choose an element and weapon';
}
choose(selected);requestAnimationFrame(animate);boot().catch(e=>{$('#status').textContent=e.message;console.error(e);});
