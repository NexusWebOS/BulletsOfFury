'use strict';
const C31={cache:new Map(),get:XART.get,ready:XART.rdy,cell:ch23Cell,round:ch23BulletDraw,draw:hammerBossDraw,tick:hammerBossTick,mount:ch23Mount,muzzle:wm26Draw};
function c31Warm(){if(!C31.ready.call(XART,'c30_rotor_0'))return false;if(C31.cache.has('c31_rotor_0'))return true;const source=C31.get.call(XART,'c30_rotor_0');
 for(let i=0;i<36;i++){const c=C31Texture.rotor(source,i*Math.PI/18);C31.cache.set('c31_rotor_'+i,c);const hit=document.createElement('canvas');hit.width=104;hit.height=208;const g=hit.getContext('2d');g.drawImage(c,0,0);g.globalCompositeOperation='source-in';g.fillStyle='white';g.fillRect(0,0,104,208);C31.cache.set('c31_rotor_hit_'+i,hit);}return true;}
XART.rdy=function(key){if(typeof key==='string'&&key.startsWith('c31_rotor'))return c31Warm();return C31.ready.apply(this,arguments);};
XART.get=function(key){if(typeof key==='string'&&key.startsWith('c31_rotor')){c31Warm();return C31.cache.get(key);}const im=C31.get.apply(this,arguments);if(!im)return im;
 if(/^c30_wave_\d+$/.test(key)){const k='red_'+key;if(!C31.cache.has(k))C31.cache.set(k,C31Texture.palette(im,'red'));return C31.cache.get(k);}return im;};
ch23GunFrame=function(b){return Math.floor(((b._hammer.c31Angle||0)%(Math.PI*2)+Math.PI*2)%(Math.PI*2)/(Math.PI/18))%36;};
ch23Cell=function(bank,b,f=0){if(bank!=='barrel')return C31.cell.apply(this,arguments);const a=C30_ART.banks.rotor[0];return{...a,key:'c31_rotor_'+f,white:'c31_rotor_hit_'+f,frame:f};};
hammerBossTick=function(b,dt){const r=C31.tick.apply(this,arguments);if(ch23Own(b)&&!b.dead){const h=b._hammer,speed=h.state==='chaingun'?lerp(1.35,4.7,clamp((h.c29GunTime||0)/4,0,1)):1.35*(h.ch23Rev||0);h.c31Angle=(h.c31Angle||0)+dt*Math.PI*2*speed;}return r;};
ch23BulletDraw=function(q){if(!q?._ch23Round)return C31.round.apply(this,arguments);const key='arch_blaster_fx_'+(4+(((q._ph||0)+Math.floor(efxClock*18))&1));if(!XART.rdy(key))return false;
 const k='gold_'+key;if(!C31.cache.has(k))C31.cache.set(k,C31Texture.trim(C31Texture.palette(XART.get(key),'gold')));ctx.save();ctx.translate(q.x,q.y);ctx.rotate(Math.atan2(q.vy,q.vx)+Math.PI/2+Math.PI);ctx.imageSmoothingEnabled=false;ctx.drawImage(C31.cache.get(k),-5,-12,10,24);ctx.restore();return true;};
// Use the existing native flash owner at the rotating disk's bore plane.
ch23Mount=function(b){const m=C31.mount(b);m.muzzleY=m.top+180;return m;};
wm26Draw=function(g,family,x,y,angle,u,size,color){if(C31.firing&&family==='chaingun'){C31.lastMuzzle={x,y,phase:u};return C31.muzzle(g,'fire',x,y,angle,u,62,'#ffce52');}return C31.muzzle.apply(this,arguments);};
hammerBossDraw=function(b){C31.firing=ch23Armed(b)&&b._hammer.state==='chaingun';try{return C31.draw.apply(this,arguments);}finally{C31.firing=false;}};
window.BOF_CHRONOS_ROTOR=C31;c31Warm();
