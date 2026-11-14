'use strict';
/* SJ120: coordinated jumping serpents, mouth-only charge and one 50/50 gauge. */
const SJ120={base:{init:sj98Init,ready:sj98Ready,load:stageLoadBegin,damage:sj98Damage,foreground:sj98Foreground,draw:sj98Draw,tick:sj98Tick,begin:beginStage},keys:Object.keys(SJ120_ART.pages),images:{},ready:false,events:[],draws:{},owner:null};
for(const[k,p]of Object.entries(SJ120_ART.pages))XART._src[k]=p.path;
function sj120Own(b){return sj98Own(b)&&!!b._sj120;}
function sj120Log(b,event,data={}){const C=b._sj120;SJ120.events.push({event,t:b.t,mode:C?.mode,...data});if(SJ120.events.length>1800)SJ120.events.shift();sj98Log('tandem-'+event,data);}
sj98Ready=function(){if(SJ120.ready)return true;if(!SJ120.base.ready()||!SJ120.keys.every(k=>XART.rdy(k)))return false;for(const k of SJ120.keys)SJ120.images[k]=XART.get(k);return SJ120.ready=true;};
stageLoadBegin=function(n,keys){SJ120.ready=false;return SJ120.base.load.call(this,n,n===7&&sj98Rank()?[...(keys||[]),...SJ120.keys]:keys);};
function sj120Blit(n,f,x,y,width){const B=SJ120_ART.banks[n];if(!B)return false;const c=B.cells[clamp(f|0,0,B.frames-1)],im=SJ120.images[c[0]];if(!im)return false;const w=width==null?c[3]:Math.min(c[3],Math.max(0,(width|0)-c[5]));if(w<=0)return true;ctx.drawImage(im,c[1],c[2],w,c[4],Math.round(x)-B.pivot[0]+c[5],Math.round(y)-B.pivot[1]+c[6],w,c[4]);SJ120.draws[n]=(SJ120.draws[n]||0)+1;return true;}
sj98Foreground=function(a){return a._sj120?!a.dead&&a.phase!=='entry'&&a.x>camLeftX()+35&&a.x<camRightX()-35&&a.y>viewTopY()+38&&a.y<VH-28:SJ120.base.foreground.apply(this,arguments);};
function sj120Neck(a){const h=Math.round(a.heading/TAU*32)*TAU/32,co=Math.cos(h),si=Math.sin(h);return{x:a.x-8*co+49*si,y:a.gy-8*si-49*co,h:a.height,heading:h};}
function sj120ResetTrail(a){const p=sj120Neck(a);a.trail=Array.from({length:70},(_,i)=>({x:p.x,y:p.y-i*5,h:p.h,heading:a.heading}));}
function sj120Trail(a){const p=sj120Neck(a),q=a.trail[0];if(Math.hypot(p.x-q.x,p.y-q.y)>2||Math.abs(p.h-q.h)>2)a.trail.unshift(p);if(a.trail.length>160)a.trail.length=160;}
function sj120Set(b,mode,dur){const C=b._sj120;C.mode=mode;C.t=0;C.dur=dur;for(const a of b._sj98.actors)if(!a.dead){a.from={x:a.x,y:a.gy};a.hits=new Map();a.nextShot=0;}sj120Log(b,'state',{mode,duration:dur,alive:b._sj98.actors.filter(a=>!a.dead).length});}
sj98Init=function(b){const out=SJ120.base.init.apply(this,arguments),G=b._sj98;SJ120.owner=b;SJ120.events=[];SJ120.draws={};b._sj120={mode:'entry',t:0,dur:1.45,hop:0,cycle:0,bar:[1,1]};
 for(const a of G.actors){const hp=Math.round(a.maxhp*14000/2896),gill=Math.floor(hp*.25);a.maxhp=a.hp=hp;a.pools[0].hp=a.pools[0].maxhp=gill;a.pools[1].hp=a.pools[1].maxhp=gill;a.pools[2].hp=a.pools[2].maxhp=hp-2*gill;a._sj120=true;a.heading=0;a.x=worldWidth()/2+(a.i?1:-1)*120;a.gy=-165-a.i*75;a.y=a.gy;a.height=0;a.stun=0;a.jaw=0;a.flashFx=0;a.from={x:a.x,y:a.gy};sj120ResetTrail(a);}
 G.flights=[];G.owner=null;G.rest=999;sj98Sync(b);stageLoadBegin(7,SJ120.keys);Snd.prepare(['combatToxic0927','enemyMachineGunHeavy','bossWeaponCharge','jetDash','hammerImpact','combatModule0927','expBig']);sj120Log(b,'budget',{total:b.maxhp,actors:G.actors.map(a=>a.maxhp)});return out;};
function sj120PlanHop(b){const C=b._sj120,mid=worldWidth()/2;for(const a of b._sj98.actors)if(!a.dead){const side=a.x>=mid?-1:1,high=(C.hop+a.i+C.cycle)%2===0,gy=high?Math.min(VH-78,player.y+15):220+(C.hop%2)*30;a.to={x:mid+side*Math.min(135,viewW()/2-92),y:clamp(gy,155,VH-78)};a.hopArc=high?96:78;a.pathBend=(high?clamp(player.y,380,VH-40):250)-(a.gy+a.to.y)/2;a.impact={x:a.to.x+2,y:a.to.y+32};}sj120Set(b,'hop-warn',b._sj98.actors.filter(a=>!a.dead).length===2?.62:.53);}
function sj120Row(b){const alive=b._sj98.actors.filter(a=>!a.dead),C=b._sj120;C.rowSlots=new Map();alive.sort((a,z)=>a.x-z.x).forEach((a,i)=>C.rowSlots.set(a.i,alive.length===2?(i?77:-77):0));sj120Set(b,'row-form',1.1);}
function sj120Shoot(b,a){if(a.dead||a.stun>0)return;const m=sj98Socket(a,'heart');if(m.x<camLeftX()+15||m.x>camRightX()-15||m.y<viewTopY()+48||m.y>VH-34)return;
 let close=false;for(const seat of seatList())withSeat(seat,()=>{if(!player.dead&&Math.abs(player.x-m.x)<52&&player.y>=m.y-15&&player.y<m.y+86)close=true;});if(close)return;
 if(eBullets.filter(q=>q._sj120&&!q.dead).length>=44)return;const q=eShootT(m.x,m.y,Math.PI/2,5.2,'s7acid',{owner:b,noMuzzle:true,silent:true,w:160,h:160});if(!q)return;
 Object.assign(q,{_sj120:true,_ss116:'orb',_sj98Actor:a,_sj98Owner:b,_sj98Age:0,_weaponProof:true,_shootable:false,_noArsenal:true,_boss:true});a.flashFx=.10;combatAudio0927(a,'combatToxic0927',.08);combatAudio0927(a,'enemyMachineGunHeavy',.30);sj120Log(b,'large-orb',{actor:a.i,x:m.x,y:m.y,angle:Math.PI/2,speed:5.2});}
function sj120Fire(b,a,interval){if(a.t>=a.nextShot){sj120Shoot(b,a);a.nextShot=a.t+interval;}}
function sj120Contact(b,a){if(a.dead||a.height>22||!['hop','split','row-fire'].includes(a.phase))return;const m=sj98Socket(a,'heart');for(const seat of seatList())withSeat(seat,()=>{if(player.dead||player.invuln>0||a.clock-(a.hits.get(seat)??-99)<.8)return;if(((player.x-m.x)/32)**2+((player.y-m.y)/18)**2<1){a.hits.set(seat,a.clock);playerHit('Sumpjaw tandem landing');sj120Log(b,'contact',{actor:a.i,seat});}});}
function sj120StartCross(b){sj120Set(b,'cross',1.65);for(const a of b._sj98.actors)if(!a.dead){const fromLeft=(a.i+b._sj120.cycle)%2===0;a.x=fromLeft?camLeftX()-240:camRightX()+240;a.gy=240;a.height=a.i?30:128;a.y=a.gy-a.height;a.from={x:a.x,y:240};a.to={x:fromLeft?camRightX()+240:camLeftX()-240,y:240};a.heading=fromLeft?-Math.PI/2:Math.PI/2;sj120ResetTrail(a);}}
function sj120Return(b){sj120Set(b,'return',1.2);for(const a of b._sj98.actors)if(!a.dead){const side=a.x>worldWidth()/2?1:-1;a.x=worldWidth()/2+side*120;a.gy=-260;a.height=0;a.y=a.gy;a.from={x:a.x,y:-260};a.heading=0;sj120ResetTrail(a);}}
function sj120Motion(b,a,dt){const C=b._sj120,u=clamp(C.t/C.dur,0,1),k=u*u*(3-2*u),mid=worldWidth()/2,live=b._sj98.actors.filter(a=>!a.dead).length;a.jaw=0;a.mouthLevel=0;a.phase=C.mode;a.t=C.t;
 if(C.mode==='entry'){a.phase='entry';a.heading=0;a.x=mid+(a.i?120:-120);a.gy=lerp(a.from.y,165+a.i*40,k);a.height=0;}
 else if(C.mode==='hop-warn'){a.heading+=clamp(ss116Wrap(-a.heading),-dt*8,dt*8);a.height=Math.max(0,a.height-dt*260);a.jaw=1;a.mouthLevel=Math.min(3,1+Math.floor(u*3));sj98Tell(a,C.t,C.dur);}
 else if(C.mode==='hop'){const bend=a.pathBend*Math.sin(u*Math.PI);a.x=lerp(a.from.x,a.to.x,u);a.gy=lerp(a.from.y,a.to.y,u)+bend;a.height=Math.sin(u*Math.PI)*a.hopArc;a.heading=0;a.jaw=1;a.mouthLevel=3;if(u>.20&&u<.82)sj120Fire(b,a,live===2?.24:.18);}
 else if(C.mode==='row-form'){a.x=lerp(a.from.x,mid+C.rowSlots.get(a.i),k);a.gy=lerp(a.from.y,158,k);a.height=Math.sin(u*Math.PI)*48;a.heading+=clamp(ss116Wrap(-a.heading),-dt*8,dt*8);}
 else if(C.mode==='row-charge'){a.x=mid+C.rowSlots.get(a.i);a.gy=158;a.height=0;a.heading=0;a.jaw=1;a.mouthLevel=Math.min(3,1+Math.floor(u*3));sj98Tell(a,C.t,C.dur);}
 else if(C.mode==='row-fire'){const offset=Math.sin(C.t*1.45)*65*(C.cycle%2?-1:1);a.x=mid+C.rowSlots.get(a.i)+offset;a.gy=158+Math.sin(C.t*2.2)*9;a.height=0;a.heading=0;a.jaw=1;const burst=C.t%1.2<.86;a.mouthLevel=burst?3:1;if(burst)sj120Fire(b,a,live===2?.14:.105);}
 else if(C.mode==='split'){const side=a.x>=mid?1:-1;a.x=lerp(a.from.x,mid+side*Math.min(145,viewW()/2-88),u);a.gy=lerp(a.from.y,260,u);a.height=Math.sin(u*Math.PI)*90;a.heading=0;a.jaw=1;a.mouthLevel=2;if(u>.3&&u<.7)sj120Fire(b,a,.26);}
 else if(C.mode==='north'){a.gy=lerp(a.from.y,-300,k);a.x=a.from.x;a.height=Math.sin(u*Math.PI)*80;ss116Heading(a,0,-1,dt);}
 else if(C.mode==='cross'){const x=lerp(a.from.x,a.to.x,u);ss116Heading(a,x-a.x,0,dt);a.x=x;a.gy=240;a.height=(a.i?30:128)+Math.sin(u*Math.PI)*(a.i?18:30);}
 else if(C.mode==='return'){a.gy=lerp(-260,175,k);a.height=Math.sin(u*Math.PI)*66;a.heading=0;}
 if(a.stun>0){a.mouthLevel=0;a.jaw=0;}a.y=a.gy-a.height;sj120Trail(a);sj120Contact(b,a);
}
function sj120Next(b){const C=b._sj120,live=b._sj98.actors.filter(a=>!a.dead).length;if(!live)return;
 if(C.mode==='entry'){C.hop=0;sj120PlanHop(b);}
 else if(C.mode==='hop-warn'){sj120Set(b,'hop',live===2?1.02:.88);combatAudio0927(b,'jetDash',.2);}
 else if(C.mode==='hop'){for(const a of b._sj98.actors)if(!a.dead){a.height=0;a.y=a.gy;combatAudio0927(a,'hammerImpact',.2);}C.hop++;if(C.hop<6)sj120PlanHop(b);else sj120Row(b);}
 else if(C.mode==='row-form'){sj120Set(b,'row-charge',live===2?1.0:.85);combatAudio0927(b,'bossWeaponCharge',.2);}
 else if(C.mode==='row-charge')sj120Set(b,'row-fire',live===2?5.5:4.6);
 else if(C.mode==='row-fire'){sj120Set(b,'split',.85);combatAudio0927(b,'jetDash',.2);}
 else if(C.mode==='split')sj120Set(b,'north',.9);
 else if(C.mode==='north'){if(live===2)sj120StartCross(b);else sj120Return(b);}
 else if(C.mode==='cross')sj120Return(b);
 else if(C.mode==='return'){C.cycle++;C.hop=0;sj120PlanHop(b);}
}
function sj120Death(b,a,dt){const G=b._sj98;a.dying+=dt;for(let j=0;j<7;j++)if(a.dying>=.13+j*.13&&!(a.deathBits&(1<<j))){a.deathBits=(a.deathBits||0)|(1<<j);const p=ss116Point(a,15+j*21);explode(p.x,p.y-p.h,32,'green');}
 if(a.dying>=1.1&&!a.shattered){a.shattered=true;for(let j=0;j<9;j++)G.fragments.push({f:j,x:a.x+(j%3-1)*50,y:a.y+(Math.floor(j/3)-1)*50,vx:(j%3-1)*105,vy:-65+Math.floor(j/3)*50,t:0});}}
sj98Tick=function(b,dt){if(!sj120Own(b))return SJ120.base.tick.apply(this,arguments);const G=b._sj98,C=b._sj120;if(!sj98Ready())return;b.t+=dt;G.clock+=dt;C.t+=dt*(ng27On()?1.15:1);
 for(const a of G.actors){a.clock+=dt;a.flash=Math.max(0,a.flash-dt);a.flashFx=Math.max(0,a.flashFx-dt);a.stun=Math.max(0,a.stun-dt);if(a.dead)sj120Death(b,a,dt);else sj120Motion(b,a,dt);}
 if(!b.dead&&C.t>=C.dur)sj120Next(b);
 for(const q of eBullets)if(q._sj98Owner===b){q._sj98Age+=dt;if(q._sj98Age>3||q._sj98Actor.dead||b.dead)q.dead=true;}
 for(const f of G.fx)f.t+=dt;G.fx=G.fx.filter(f=>f.t<.55&&!f.a.dead);G.flights=[];
 for(const f of G.fragments){f.t+=dt;f.x+=f.vx*dt;f.y+=f.vy*dt;f.vy+=180*dt;}G.fragments=G.fragments.filter(f=>f.t<.85);
 if(b.dead){b.dying+=dt;if(b.dying>=2.4&&!G.rewarded){G.rewarded=true;continueRewardResolve(b,b.x,VH*.4,'miniboss');dropPowerup(b.x,VH*.4,'weapon');run.score+=5200;subBoss=null;subBossActive=false;subBossDone=true;sj120Log(b,'progression');}}
 sj98Sync(b);
};
sj98Damage=function(b){const own=sj120Own(b),old=own?b._sj98.actors.map(a=>({dead:a.dead,state:sj98State(a)})):null,out=SJ120.base.damage.apply(this,arguments);if(own){const C=b._sj120;for(const a of b._sj98.actors)if(!a.dead&&old[a.i].state!==3&&sj98State(a)===3){a.stun=.55;sj120Log(b,'heart-open',{actor:a.i});}
 const lost=b._sj98.actors.some(a=>!old[a.i].dead&&a.dead);if(lost){sj120Log(b,'snake-defeat',{alive:b._sj98.actors.filter(a=>!a.dead).length});if(!b.dead){C.hop=0;sj120PlanHop(b);}else C.mode='defeat';}}
 return out;};
function sj120Segments(a,shadow){for(let i=9;i>=0;i--){const p=ss116Point(a,i*19),n=((Math.round(p.heading/TAU*32)%32)+32)%32,mode=shadow?'shadow':a.flash>0?'hit':'body';ss116Blit('segment'+(i>7?2:i>4?1:0)+'_'+mode,n,p.x,p.y+(shadow?12:-p.h));}}
function sj120Warnings(b){const C=b._sj120;for(const a of b._sj98.actors)if(!a.dead){if(C.mode==='hop-warn')sj98Retina(a.impact.x,a.impact.y,C.t,C.dur);else if(C.mode==='hop')sj98Retina(a.impact.x,a.impact.y,C.dur,C.dur);
 if(C.mode==='row-charge'){const m=sj98Socket(a,'heart');combatWarningDraw(a,{x:m.x,y:m.y,ex:m.x,ey:VH+60,width:52,progress:C.t/C.dur,fieldOnly:true});}}
}
function sj120Bar(b){const C=b._sj120,A=b._sj98.actors;C.bar=A.map(a=>clamp(a.hp/a.maxhp,0,1));screenBar(()=>{const x=VW/2,y=24;sj120Blit('health_frame',0,x,y);sj120Blit('health_half',0,x-192,y+5,Math.ceil(190*C.bar[0]));sj120Blit('health_half',0,x+2,y+5,Math.ceil(190*C.bar[1]));pm27Draw(ctx,'SUMPJAW PAIR',x,y-5,8,{family:'command',palette:'toxic',width:260});pm27Draw(ctx,'01',x-172,y-5,8,{family:'command',palette:'toxic',width:22});pm27Draw(ctx,'02',x+172,y-5,8,{family:'command',palette:'toxic',width:22});});}
sj98Draw=function(b){if(!sj120Own(b))return SJ120.base.draw.apply(this,arguments);if(!sj98Ready())return;const G=b._sj98,C=b._sj120;sj120Warnings(b);
 for(const a of G.actors)if(!a.dead||a.dying<1.1){sj120Segments(a,true);ss116Blit('head_shadow',ss116Frame(a)%32,a.x,a.gy+12);}
 for(const a of [...G.actors].sort((a,z)=>a.height-z.height)){if(a.dead&&a.dying>=1.1)continue;sj120Segments(a,false);const white=a.flash>0||a.dead&&Math.floor(a.dying*20)%2;ss116Blit(white?'hit':'body'+sj98State(a),ss116Frame(a),a.x+(a.dead?Math.floor(Math.sin(a.dying*61)*2):0),a.y);
  if(!white&&!a.dead&&a.mouthLevel>0){const n=((Math.round(a.heading/TAU*32)%32)+32)%32,level=clamp(a.mouthLevel,0,3),phase=Math.floor(a.clock*(16+level*6))%8;sj120Blit('mouth',(level*8+phase)*64+(a.jaw?32:0)+n,a.x,a.y);}
  if(!a.dead&&a.flashFx>0){const m=sj98Socket(a,'heart');sj120Blit('mouth_flash',Math.min(15,Math.floor((.10-a.flashFx)*150)),m.x,m.y);}}
 for(const f of G.fragments)sj98Blit('fragment',f.f,f.x,f.y);for(const f of G.fx)if(!f.mouth)sj98Blit('splash',Math.min(15,Math.floor(f.t/.55*16)),f.x,f.y);if(!b.dead)sj120Bar(b);
};
beginStage=function(){if(SJ120.owner){for(const q of eBullets)if(q._sj98Owner===SJ120.owner)q.dead=true;}SJ120.owner=null;return SJ120.base.begin.apply(this,arguments);};
BOF_SUMPJAW_DUO_1031.init=sj98Init;BOF_SUMPJAW_SERPENTS_1104.init=sj98Init;
globalThis.BOF_SUMPJAW_TANDEM_1105={state:SJ120,owns:sj120Own};
