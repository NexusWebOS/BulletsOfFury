'use strict';
/* H125: authored weapon effects for the copied helicopter only. Native HC79
   pods, committed aim, projectile movement, damage and interception remain. */
const H125={base:{keys:v18Keys,warm:v18Warm,load:stageLoadBegin,round:hc79Round,missile:hc79Missile,projectile:hc79Projectile,draw:r30DrawBoss,bullets:drawBullets,update:updatePlay,impact:s1CombatImpact,trail:addTrail,rupture:hc79Rupture,explode,clear:v18Clear,enter:v18Enter},fx:[],watch:new Set(),draws:{},events:[],reduced:typeof matchMedia==='function'&&matchMedia('(prefers-reduced-motion: reduce)').matches};
for(const[k,a]of Object.entries(H125_ART.pages))XART._src[k]=a.path;
function h125Keys(){return Object.keys(H125_ART.pages);}
v18Keys=function(){return[...H125.base.keys(),...h125Keys()];};
v18Warm=function(){const prior=H125.base.warm();return h125Keys().map(k=>XART.rdy(k)).every(Boolean)&&prior;};
stageLoadBegin=function(n,keys){h125Reset();if(n===8)Snd.prepare(['overlordGun','overlordRocket','expSmall','expBig']);return H125.base.load.call(this,n,n===8?[...(keys||[]),...h125Keys()]:keys);};
function h125Log(event,data={}){H125.events.push({event,t:efxClock,...data});if(H125.events.length>600)H125.events.shift();}
function h125Blit(name,f,x,y){const rows=H125_ART.banks[name];if(!rows)return false;const a=rows[clamp(f|0,0,rows.length-1)],im=XART.get(a.key);if(!im)return false;ctx.drawImage(im,...a.rect,Math.round(x+a.offset[0]),Math.round(y+a.offset[1]),a.w,a.h);H125.draws[name]=(H125.draws[name]||0)+1;return true;}
function h125Reset(){H125.fx.length=0;H125.watch.clear();}
function h125Flash(b,id,kind){const Q=hc79State(b);(Q._h125Flashes??={})[id]={t:efxClock,kind};}
hc79Round=function(b,id,P){const n=eBullets.length,out=H125.base.round.apply(this,arguments);if(eBullets.length>n){for(const q of eBullets.slice(n))if(q._hc79Type==='gun')q._h125Born=efxClock;h125Flash(b,id,'muzzle');h125Log('gun-fire',{part:id,socket:hc79Socket(b,id)});}return out;};
hc79Missile=function(b,id,P){const n=eBullets.length,out=H125.base.missile.apply(this,arguments);for(const q of eBullets.slice(n))if(q._hc79Type==='missile'){q._h125Born=efxClock;H125.watch.add(q);h125Flash(b,id,'launch');h125Log('rocket-fire',{part:id,socket:hc79Socket(b,id,'missile')});}return out;};
hc79Projectile=function(q){if(q?._hc79Type==='gun'||q?._hc79Type==='missile'){const name=q._hc79Type==='gun'?'tracer':'missile',rate=name==='tracer'?30:24,f=H125.reduced?4:Math.floor((efxClock-(q._h125Born??q._hc79Born??efxClock))*rate)%8,d=hc79Dir(Math.atan2(q.vy,q.vx));return h125Blit(name,f*64+d,q.x,q.y);}return H125.base.projectile.apply(this,arguments);};
r30DrawBoss=function(b){if(!hc79Live(b))return H125.base.draw.apply(this,arguments);hc79Body(b);hc79Warnings(b);const Q=hc79State(b);for(const id of ['left','right']){const a=Q._h125Flashes?.[id];if(!a||!hc79Alive(b,id))continue;const age=efxClock-a.t,life=H125_ART.timing[a.kind];if(age<0||age>=life)continue;const at=hc79Socket(b,id,a.kind==='launch'?'missile':'gun'),d=hc79Dir(Q.turn[id]+Math.PI/2),f=H125.reduced?4:Math.min(7,Math.floor(age/life*8));h125Blit(a.kind,f*64+d,at.x,at.y);}};
function h125Burst(x,y,size=72,delay=0,reason='rocket'){if(H125.fx.length>=24)H125.fx.shift();H125.fx.push({x,y,bank:'burst'+size,born:efxClock+delay});h125Log('burst',{x,y,size,delay,reason});}
function h125MissileBurst(q){if(q._h125Burst)return;q._h125Burst=true;h125Burst(q.x,q.y,72,0,'missile-impact');combatAudio0927(q._hc79Owner,'expSmall',.10);}
s1CombatImpact=function(x,y,green,size){if(!green){const q=eBullets.find(q=>q._hc79Type==='missile'&&Math.abs(q.x-x)<.1&&Math.abs(q.y-y)<.1);if(q){h125MissileBurst(q);return;}}return H125.base.impact.apply(this,arguments);};
// Exhaust smoke is already authored into the flight poses. Suppress only the
// matching HC79 missile's legacy trail at its exact native trail origin.
addTrail=function(x,y,color,kind){if(kind==='missile'&&[...H125.watch].some(q=>!q.dead&&Math.abs(x-(q.x-Math.cos(q.ang||Math.PI/2)*q.h*.4))<.5&&Math.abs(y-(q.y-Math.sin(q.ang||Math.PI/2)*q.h*.4))<.5))return;return H125.base.trail.apply(this,arguments);};
updatePlay=function(dt){const out=H125.base.update.apply(this,arguments);H125.fx=H125.fx.filter(q=>efxClock-q.born<.8);for(const q of H125.watch){if(!hc79Live(q._hc79Owner)){H125.watch.delete(q);continue;}if(q.dead||!eBullets.includes(q)){if(q.dead&&!q._h125Burst&&q.x>=camLeftX()-24&&q.x<=camRightX()+24&&q.y>=viewTopY()-24&&q.y<=VH+24)h125MissileBurst(q);H125.watch.delete(q);}}return out;};
drawBullets=function(){const out=H125.base.bullets.apply(this,arguments);for(const q of H125.fx){const age=efxClock-q.born;if(age<0||age>=.8)continue;const f=Math.min(15,Math.floor(age*20));h125Blit(q.bank,H125.reduced?Math.max(7,f):f,q.x,q.y);}return out;};
explode=function(){if(H125.rupturing)return;return H125.base.explode.apply(this,arguments);};
hc79Rupture=function(b,p,base,args){if(!hc79Own(b))return H125.base.rupture.apply(this,arguments);const v=hc79Geometry(b).find(v=>v.p===p),already=p._hc79Broken;H125.rupturing=true;let out;try{out=H125.base.rupture.apply(this,arguments);}finally{H125.rupturing=false;}if(v&&!already&&p._hc79Broken){h125Burst(v.x,v.y,160,0,'pod-break');h125Burst(v.x-18,v.y+9,112,.10,'pod-secondary');h125Burst(v.x+20,v.y-12,112,.22,'pod-secondary');combatAudio0927(b,'expBig',.12);}return out;};
v18Clear=function(b){if(hc79Own(b))h125Reset();return H125.base.clear.apply(this,arguments);};
v18Enter=function(b,n,form){if(hc79Own(b)||n===2&&form===1)h125Reset();return H125.base.enter.apply(this,arguments);};
globalThis.BOF_HELICOPTER_EFFECTS_1111=H125;
