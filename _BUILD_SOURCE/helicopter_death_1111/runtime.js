'use strict';
/* H126: both Stage1 Overlord-X palettes and Dracodia's actual copied helicopter.
   Authored yaw plates and real-pixel debris; native defeat/progression owners. */
const H126={base:{load:stageLoadBegin,keys:v18Keys,warm:v18Warm,die:bossDie,break:r30Break,tick:r30Tick,update:updateBoss,draw:drawBoss,copyDraw:r30DrawBoss,clear:v18Clear,begin:beginStage,deathFX:unitDeathFX,targets:retinaBossTargets,contact:target17BossContact},events:[],draws:{},reduced:typeof matchMedia==='function'&&matchMedia('(prefers-reduced-motion: reduce)').matches};
for(const[k,a]of Object.entries(H126_ART.pages))XART._src[k]=a.path;
function h126Keys(stage){const names=Object.keys(H126_ART.banks).filter(n=>n.startsWith('burst')||(stage===8?n.includes('dracodia'):!n.includes('dracodia')));return [...new Set(names.flatMap(n=>H126_ART.banks[n].map(a=>a.key)))];}
v18Keys=function(){return [...H126.base.keys(),...h126Keys(8)];};
v18Warm=function(){const prior=H126.base.warm();return h126Keys(8).map(k=>XART.rdy(k)).every(Boolean)&&prior;};
stageLoadBegin=function(n,keys){if(n===1||n===8)Snd.prepare(['expSmall','expBig','expBoss','overlordWind']);return H126.base.load.call(this,n,n===1||n===8?[...(keys||[]),...h126Keys(n)]:keys);};
function h126Log(b,event,data={}){H126.events.push({event,kind:b._h126?.kind,t:b._h126?.t||0,...data});if(H126.events.length>700)H126.events.shift();}
function h126Blit(name,f,x,y){const rows=H126_ART.banks[name];if(!rows)return;const a=rows[clamp(f|0,0,rows.length-1)],im=XART.get(a.key);if(!im)return;ctx.drawImage(im,...a.rect,Math.round(x+a.offset[0]),Math.round(y+a.offset[1]),a.w,a.h);H126.draws[name]=(H126.draws[name]||0)+1;}
function h126Stage1(b){return run.stage===1&&b?.kind==='damkeeper';}
function h126Burst(b,x,y,size=88,delay=0){const D=b._h126;if(D.fx.length>=32)D.fx.shift();D.fx.push({x,y,size,t:-delay});h126Log(b,'explosion',{x,y,size,delay});}
function h126Start(b,kind,mask=0){const copy=kind==='dracodia',family=copy?'dracodia-'+mask:diffKey==='furious'?'furious':'normal';b._h126={kind,family,t:0,blast:copy?3.85:6.65,duration:copy?5.4:8.6,origin:{x:b.x,y:b.y},x:b.x,y:b.y,L:camLeftX(),R:camRightX(),top:viewTopY(),side:b.x<(camLeftX()+camRightX())/2?-1:1,next:.08,n:0,fx:[],debris:[],angle:0,finished:false};
 for(const L of playerLocks)if(L.src===b||L.src?._hc79Host===b){L.src.dead=true;for(const s of L.launches)s.done=true;}
 groundTargetingCancel(b);h126Log(b,'death-start',{family,mask,hp:b.hp,pools:copy?j3State(b).hp.slice():null});return b._h126;
}
unitDeathFX=function(e){if(e===H126.starting)return;return H126.base.deathFX.apply(this,arguments);};
bossDie=function(){const b=boss;if(!h126Stage1(b))return H126.base.die.apply(this,arguments);if(b.dead||b._h126)return;H126.starting=b;let out;try{out=H126.base.die.apply(this,arguments);}finally{H126.starting=null;}if(b.dead)h126Start(b,'stage1');return out;};
r30Break=function(b){const eligible=hc79Own(b)&&b._r30.mode==='fight',mask=eligible?(!hc79Alive(b,'left')?1:0)|(!hc79Alive(b,'right')?2:0):0;const out=H126.base.break.apply(this,arguments);if(eligible&&b._r30.mode==='v19copyDeath'&&!b._h126)h126Start(b,'dracodia',mask);return out;};
function h126Chunk(b,index,small=false){const D=b._h126,rows=H126_ART.chunks[D.family],a=rows[index%rows.length],angle=D.angle,cs=Math.cos(angle),sn=Math.sin(angle),ox=a.origin[0],oy=a.origin[1],theta=index*2.399963229728653+angle*.13,speed=small?90+(index%5)*16:150+(index%7)*24;D.debris.push({bank:a.bank,x:D.x+ox*cs-oy*sn,y:D.y+ox*sn+oy*cs,vx:Math.cos(theta)*speed+D.side*40,vy:Math.sin(theta)*speed+35,spin:index%2?-1:1,phase:index%8,t:0,life:small?1.4:1.8+(index%3)*.12});}
function h126Position(D,t,u,targetX,targetY){return{x:lerp(D.origin.x,targetX,u*u)+Math.sin(t*5)*18*Math.sin(Math.PI*u),y:lerp(D.origin.y,targetY,Math.pow(u,2.3))+Math.sin(t*4)*10*Math.sin(Math.PI*u)};}
function h126Tick(b,dt){const D=b._h126;D.t+=dt;const t=D.t,u=clamp(t/D.blast,0,1),progress=u*u,targetX=D.side>0?D.R+20:D.L-20,targetY=VH-20;
 D.angle=TAU*(.12*t+.28*t*t);const position=h126Position(D,t,u,targetX,targetY);D.x=position.x;D.y=position.y;
 for(const q of D.fx)q.t+=dt;D.fx=D.fx.filter(q=>q.t<.8);
 for(const q of D.debris){q.t+=dt;q.x+=q.vx*dt;q.y+=q.vy*dt;q.vy+=115*dt;if(!q.burst&&q.t>=q.life){q.burst=true;if(q.x>D.L-30&&q.x<D.R+30&&q.y>D.top-30&&q.y<VH+30)h126Burst(b,q.x,q.y,88);}}
 D.debris=D.debris.filter(q=>q.t<q.life+.08&&q.x>D.L-180&&q.x<D.R+180&&q.y<VH+220);
 if(t<D.blast&&t>=D.next){const interval=lerp(.46,.055,Math.pow(u,1.5)),a=D.angle+D.n*2.4,r=(D.kind==='dracodia'?60:34)*(1+u*.3);D.next=t+interval;h126Burst(b,D.x+Math.cos(a)*r,D.y+Math.sin(a)*r,D.n%4===0?144:88);if(u>.54&&D.n%2===0)h126Chunk(b,D.n,true);combatAudio0927(b,D.n%4===0?'expBig':'expSmall',.11);h126Log(b,'cookoff',{interval,spin:D.angle,position:{x:D.x,y:D.y}});D.n++;}
 if(t>=D.blast&&!D.shattered){D.shattered=true;D.final={x:D.x,y:D.y};h126Burst(b,D.x,D.y,384);h126Burst(b,D.x-D.side*65,D.y-35,256,.12);h126Burst(b,D.x-D.side*110,D.y-75,256,.26);for(let i=0;i<H126_ART.chunks[D.family].length;i++)h126Chunk(b,i);Snd.play('expBoss',.85);h126Log(b,'shatter',{chunks:D.debris.length,x:D.x,y:D.y});}
 if(t>=D.duration&&!D.finished){D.finished=true;h126Log(b,'death-complete');}
}
updateBoss=function(dt){const b=boss,D=b?._h126;if(!D||D.kind!=='stage1')return H126.base.update.apply(this,arguments);dt=clamp(dt||0,0,.05);b.t+=dt;b.dying+=dt;b.flash=Math.max(0,(b.flash||0)-dt);h126Tick(b,dt);whiteBlast=0;if(b.dying>=(D.damSwapAt??6.7)&&!damBroken)damBroken=true;};
r30Tick=function(b,dt){const D=b?._h126;if(!D||D.kind!=='dracodia'||b._r30.mode!=='v19copyDeath')return H126.base.tick.apply(this,arguments);dt=clamp(dt||0,0,.05);j3Timers(b,dt);dr5TalkTick(b,dt);b.enter=b._noHit=true;h126Tick(b,dt);if(D.finished){b._r30.v18.deathBurst=true;return H126.base.tick.call(this,b,0);}};
function h126Draw(b){const D=b._h126;if(!D)return;const effects=front=>{D.fx.forEach((q,i)=>{if(q.t<0||(!D.shattered&&i%2!==(front?1:0))||(D.shattered&&!front))return;const f=Math.min(15,Math.floor(q.t*20));h126Blit('burst'+q.size,H126.reduced?Math.max(7,f):f,q.x,q.y);});};effects(false);
 if(!D.shattered){const turns=H126.reduced?D.t*.12:D.angle/TAU,f=((Math.floor(turns*64)%64)+64)%64;h126Blit('spin-'+D.family,f,D.x,D.y);}
 effects(true);for(const q of D.debris){const f=((Math.floor(q.phase+q.t*(H126.reduced?2:14)*q.spin)%8)+8)%8;h126Blit(q.bank,f,q.x,q.y);}
}
drawBoss=function(){const b=boss;if(b?._h126?.kind==='stage1')return h126Draw(b);return H126.base.draw.apply(this,arguments);};
r30DrawBoss=function(b){if(b?._h126?.kind==='dracodia'&&b._r30.mode==='v19copyDeath')return h126Draw(b);return H126.base.copyDraw.apply(this,arguments);};
retinaBossTargets=function(b){return b?._h126&&!b._h126.finished?[]:H126.base.targets.apply(this,arguments);};
target17BossContact=function(b){return b?._h126?false:H126.base.contact.apply(this,arguments);};
v18Clear=function(b){if(b?._h126)delete b._h126;return H126.base.clear.apply(this,arguments);};
beginStage=function(){if(boss?._h126)delete boss._h126;return H126.base.begin.apply(this,arguments);};
globalThis.BOF_HELICOPTER_DEATH_1111=H126;
