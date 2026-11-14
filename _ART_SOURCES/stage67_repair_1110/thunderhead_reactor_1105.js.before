'use strict';
/* TC119: socketed beams, coordinated batteries, moving reactor and depth launch.
   Native FB112 pools, damage, rewards and defeat remain authoritative. */
const TC119={base:{keys:fb112Keys,ready:fb112Ready,load:stageLoadBegin,create:fb112Create,
 tick:fb112Tick,start:fb112Start,draw:fb112Draw,point:fb112Point,bore:fb112Bore,
 at:fb112At,visible:fb112Visible,damage:fb112Damage,cancel:fb112Cancel,
 round:th114Round,roundDraw:th114RoundDraw,strike:th114StrikeTick,weather:th114Weather,begin:beginStage},
 far:TC119_ART.depths.length-1,keys:Object.keys(TC119_ART.pages),images:{},bits:null,load:null,ready:false,owner:null,events:[],draws:{}};
for(const[k,p]of Object.entries(TC119_ART.pages))XART._src[k]=p.path;
function tc119Own(b){return tm115Own(b)&&!!b._tc119;}
function tc119Log(b,event,data={}){const row={event,t:b.t,phase:b._tc119?.flow?.state,attack:b._fb112.attack,...data};TC119.events.push(row);if(TC119.events.length>1600)TC119.events.shift();fb112Log(b,'reactor-'+event,data);}
function tc119Warm(){if(!TC119.load)TC119.load=fetch(TC119_ART.maskPath).then(r=>{if(!r.ok)throw Error('Thunderhead reactor masks '+r.status);return r.arrayBuffer();}).then(a=>{if(a.byteLength!==TC119_ART.maskBytes)throw Error('Thunderhead reactor mask size');TC119.bits=new Uint8Array(a);}).catch(console.error);}
fb112Keys=function(){tc119Warm();return [...TC119.base.keys(),...TC119.keys];};
fb112Ready=function(){if(TC119.ready)return true;if(!TC119.bits||!TC119.base.ready()||!TC119.keys.every(k=>XART.rdy(k)))return false;for(const k of TC119.keys)TC119.images[k]=XART.get(k);return TC119.ready=true;};
stageLoadBegin=function(n,keys){TC119.ready=false;if(n===6&&fb112Rank())keys=[...(keys||[]),...fb112Keys()];return TC119.base.load.call(this,n,keys);};
fb112Create=function(model,sub){const b=TC119.base.create.apply(this,arguments);if(model==='thunder'){
 b._tc119={clock:0,di:0,flow:null,volley:0,gunT:0,gunPhase:'idle',debris:[],bursts:[],cyclones:[],shade:0};TC119.owner=b;
 Snd.prepare(['chronosLightning1026','bossWeaponCharge','overlordWind','jetDash','enemyMachineGunHeavy','combatModule0927','expBig','expSmall']);
 tc119Log(b,'assembly',{hp:b.hp,modules:b._fb112.parts.length});}return b;};
function tc119Blit(n,f,x,y){const B=TC119_ART.banks[n];if(!B)return false;const c=B.cells[clamp(f|0,0,B.frames-1)],im=TC119.images[c[0]];if(!im)return false;
 ctx.drawImage(im,c[1],c[2],c[3],c[4],Math.round(x)-B.pivot[0]+c[5],Math.round(y)-B.pivot[1]+c[6],c[3],c[4]);TC119.draws[n]=(TC119.draws[n]||0)+1;return true;}
function tc119Scale(b){return TC119_ART.depths[b._tc119.di];}
function tc119Angle(b){return Math.PI/2+fb112Dir(b._fb112.heading,16)*TAU/16;}
fb112Point=function(b,p){if(!tc119Own(b))return TC119.base.point.apply(this,arguments);const k=tc119Scale(b),a=tc119Angle(b)-Math.PI/2,x=(p[0]-288)*k,y=(p[1]-288)*k;return{x:b.x+x*Math.cos(a)-y*Math.sin(a),y:b.y+x*Math.sin(a)+y*Math.cos(a)};};
fb112Bore=function(b,p){if(!tc119Own(b))return TC119.base.bore.apply(this,arguments);const m=fb112PartPoint(b,p),k=tc119Scale(b),a=p.type==='gun'?fb112Angle(p.angle):tc119Angle(b),r=(p.type==='gun'?56-(p.recoil>.035?2.24:0):p.bore[1])*k;return{x:m.x+Math.cos(a)*r,y:m.y+Math.sin(a)*r};};
fb112Visible=function(b){return tc119Own(b)&&b._tc119.flow?false:TC119.base.visible.apply(this,arguments);};
function tc119Mask(f,x,y,cx,cy){const B=TC119_ART.banks.gun_mask,m=TC119_ART.masks.gun_mask[f],px=Math.floor(x-cx+B.pivot[0])-m[0],py=Math.floor(y-cy+B.pivot[1])-m[1];if(px<0||py<0||px>=m[2]||py>=m[3])return false;const bit=py*m[2]+px;return !!(TC119.bits[m[4]+(bit>>3)]&(1<<(bit&7)));}
fb112At=function(b,x,y,pad=0){if(!tc119Own(b))return TC119.base.at.apply(this,arguments);if(!fb112Visible(b))return null;const q=b._fb112;let best=null,score=Infinity;
 for(const p of fb112LiveParts(b)){const m=fb112PartPoint(b,p),box=p===q.core?q.M.coreBox:p.hitBox,ca=p.type==='gun'?Math.abs(Math.cos(p.angle-Math.PI/2)):1,sa=p.type==='gun'?Math.abs(Math.sin(p.angle-Math.PI/2)):0,v=((x-m.x)/((ca*box[0]+sa*box[1])/2+pad))**2+((y-m.y)/((sa*box[0]+ca*box[1])/2+pad))**2,f=(p.recoil>.035?32:0)+fb112Dir(p.angle);
  if(v<=1&&v<score&&(p.type==='gun'?tc119Mask(f,x,y,m.x,m.y):tm115Mask(p===q.core?'core':'pod'+p.index,0,m.x,m.y,x,y))){best=p;score=v;}}
 return best;};
function tc119AliveAllies(){const list=(s6Wing?.ships||[]).filter(q=>q.phase==='fight'&&q.hp>0&&!q.dead&&Number.isFinite(q.x)&&Number.isFinite(q.y)).map(q=>({kind:'ally',key:q.key,ship:q}));
 if(ally&&!ally.dead&&Number.isFinite(ally.x)&&Number.isFinite(ally.y)&&!list.some(q=>q.key===ally.key))list.push({kind:'ally',key:ally.key,ship:ally});return list;}
function tc119Assign(b){const C=b._tc119,q=b._fb112,guns=q.parts.filter(p=>p.type==='gun'&&p.hp>0),friends=tc119AliveAllies(),playerTurn=C.volley%4!==3,lead=guns.length?guns[Math.floor(C.volley/4)%guns.length]:null;let ai=C.volley%Math.max(1,friends.length);
 for(const p of guns){const target=p===lead&&playerTurn?{kind:'player',key:run.pilot,ship:targetShip(b.x,b.y)}:friends.length?friends[ai++%friends.length]:null;p._tc119Target=target;p._tc119Lock=target?{x:target.ship.x,y:target.ship.y}:null;p._tc119Next=0;}
 tc119Log(b,'target-assignment',{serial:C.volley,playerTurn,targets:guns.map(p=>({part:p.id,kind:p._tc119Target?.kind,key:p._tc119Target?.key}))});C.volley++;C.gunPhase='aim';C.gunT=0;}
function tc119Slug(b,p){const C=b._tc119,m=fb112Bore(b,p),a=fb112Angle(p.angle),side=p._tc119Side===1?-1:1;p._tc119Side=side;
 const x=m.x-Math.sin(a)*side*3,y=m.y+Math.cos(a)*side*3,r=eShootT(x,y,a,4.6,'l6bolt',{owner:b,silent:true,noMuzzle:true,w:24,h:46});
 Object.assign(r,{_tc119Slug:true,_th114Owner:b,_th114Part:p,_th114Born:b.t,_th114Life:3.3,_th114Family:'orb',_fb112Owner:b,_fb112Part:p,_fb112Born:b.t,_rw117Angle:a,_weaponProof:true,_shootable:false,_noArsenal:true,_boss:true});
 p.recoil=.07;p._tc119Muzzle=.07;tc119Log(b,'slug',{part:p.id,target:p._tc119Target?.key,kind:p._tc119Target?.kind,x,y,angle:a});}
function tc119Guns(b,dt){const C=b._tc119,q=b._fb112;if(b.enter||C.flow||b.dead){C.gunPhase='idle';C.gunT=0;return;}C.gunT+=dt;
 if(C.gunPhase==='idle'){if(C.gunT>.65)tc119Assign(b);return;}
 for(const p of q.parts.filter(p=>p.type==='gun'&&p.hp>0&&p._tc119Target)){
  const target=p._tc119Target.ship;if(target.dead||target.hp===0||p._tc119Target.kind==='ally'&&target.phase!=='fight'){p._tc119Target=p._tc119Lock=null;continue;}
  if(C.gunPhase==='aim'&&C.gunT<.62)p._tc119Lock={x:target.x,y:target.y};
  if(C.gunPhase==='aim'){const at=fb112PartPoint(b,p),T=p._tc119Lock;p.angle=Math.atan2(T.y-at.y,T.x-at.x);combatWarningTick(p,'tc119-gun-'+C.volley,C.gunT,.92);}
  else if(C.gunPhase==='fire'&&C.gunT>=p._tc119Next&&eBullets.filter(r=>r._tc119Slug&&!r.dead).length<56){tc119Slug(b,p);p._tc119Next=C.gunT+turretInterval15(.12);combatAudio0927(p,'enemyMachineGunHeavy',.10);}
 }
 if(C.gunPhase==='aim'&&C.gunT>=.92){C.gunPhase='fire';C.gunT=0;}
 else if(C.gunPhase==='fire'&&C.gunT>=.95){C.gunPhase='idle';C.gunT=0;}
}
th114Round=function(b,at,angle,speed,family,part){if(tc119Own(b)&&part?.type==='gun'&&family==='orb')return null;return TC119.base.round.apply(this,arguments);};
th114RoundDraw=function(r){if(!r?._tc119Slug)return TC119.base.roundDraw.apply(this,arguments);if(r.dead)return true;return rw117Blit('slug',(1+Math.floor((r._th114Owner.t-r._th114Born)*22)%3)*32+fb112Dir(r._rw117Angle),r.x,r.y);};
th114StrikeTick=function(b,dt){const out=TC119.base.strike.apply(this,arguments);if(tc119Own(b))for(const P of th114State(b).impacts)if(!P._tc119Audio){P._tc119Audio=true;Snd.play('chronosLightning1026',.76);tc119Log(b,'audible-lightning',{id:P.id});}return out;};
function tc119Set(b,state,dur){const C=b._tc119;C.flow={state,t:0,dur,from:{x:b.x,y:b.y},heading:b._fb112.heading};b._fb112.phase='depth';b._fb112.t=0;tc119Log(b,'depth-state',{state,duration:dur,depth:C.di});}
fb112Start=function(b){const out=TC119.base.start.apply(this,arguments);if(!tc119Own(b))return out;const q=b._fb112,C=b._tc119;
 if(q.attack==='storm-tempest'){tm115State(b).beams=[];C.gunPhase='idle';for(const p of q.parts)p._tc119Target=null;tc119Set(b,'turn-north',.65);combatAudio0927(b,'jetDash',.3);}
 return out;};
function tc119Launch(b){const C=b._tc119,at=th114Core(b),T=targetShip(at.x,at.y),end=C.aim||{x:clamp(T.x,camLeftX()+95,camRightX()-95),y:Math.max(VH*.77,T.y)};
 C.cyclones.push({t:0,from:{...at},to:end,x:at.x,y:at.y,size:0,hits:new Set()});tc119Log(b,'perspective-launch',{from:at,to:end});combatAudio0927(b,'overlordWind',.3);Snd.play('chronosLightning1026',.7);}
function tc119Flow(b,dt){const C=b._tc119,F=C.flow,q=b._fb112,S=th114State(b),M=tm115State(b);if(!F)return;F.t+=dt;q.t+=dt;b.t+=dt;S.clock+=dt;M.clock+=dt;
 b.flash=Math.max(0,b.flash-dt);for(const p of [...q.parts,q.core]){p.flash=Math.max(0,p.flash-dt);p.recoil=Math.max(0,p.recoil-dt);}
 for(const f of q.fx)f.t+=dt;q.fx=q.fx.filter(f=>f.t<.6);for(const f of S.muzzle)f.age+=dt;S.muzzle=S.muzzle.filter(f=>f.age<.16);
 th114StrikeTick(b,dt);th114FieldsTick(b,dt);S.weather+=clamp(.96-S.weather,-dt*.28,dt*.35);
 const u=clamp(F.t/F.dur,0,1),smooth=u*u*(3-2*u),done=u>=1,home={x:worldWidth()/2,y:175};
 if(F.state==='turn-north'){q.heading=lerp(Math.PI/2,-Math.PI/2,smooth);if(done)tc119Set(b,'leave-north',1.1);}
 else if(F.state==='leave-north'){q.heading=-Math.PI/2;b.y=lerp(F.from.y,-420,smooth);if(done){C.di=TC119.far;tc119Set(b,'far-enter',1.25);b.y=-200;C.flow.from.y=-200;}}
 else if(F.state==='far-enter'){q.heading=Math.PI/2;b.x=home.x;b.y=lerp(-200,125,smooth);if(done){tc119Set(b,'far-charge',4.4);C.chargeMarks=0;C.aim=null;combatAudio0927(b,'bossWeaponCharge',.3);}}
 else if(F.state==='far-charge'){if(!C.aim||F.t<F.dur-.85){const A=targetShip(b.x,b.y);C.aim={x:clamp(A.x,camLeftX()+95,camRightX()-95),y:Math.max(VH*.77,A.y)};}q.heading=Math.PI/2;b.x=home.x+Math.sin(C.clock*2)*3;b.y=125+Math.sin(C.clock*(7+u*25))*(1+u*2);combatWarningTick(b,'tc119-depth-'+q.seq,F.t,F.dur);
  if(F.t>=1.1+C.chargeMarks*.9&&C.chargeMarks<3){const T=targetShip(b.x,b.y);th114Mark(b,T.x+[-80,80,0][C.chargeMarks],T.y);C.chargeMarks++;}
  combatAudio0927(b,'bossWeaponCharge',1.5);combatAudio0927(b,'overlordWind',1.8);if(done){tc119Launch(b);tc119Set(b,'recoil',.38);}}
 else if(F.state==='recoil'){q.heading=Math.PI/2;b.y=lerp(F.from.y,F.from.y-36,1-(1-u)**3);if(done)tc119Set(b,'recoil-recover',.55);}
 else if(F.state==='recoil-recover'){b.y=lerp(F.from.y,125,smooth);if(done)tc119Set(b,'far-turn-north',.5);}
 else if(F.state==='far-turn-north'){q.heading=lerp(Math.PI/2,-Math.PI/2,smooth);if(done)tc119Set(b,'far-rise',.95);}
 else if(F.state==='far-rise'){q.heading=-Math.PI/2;b.y=lerp(F.from.y,-240,smooth);if(done){tc119Set(b,'foreground-return',1.5);b.y=-400;C.flow.from.y=-400;}}
 else if(F.state==='foreground-return'){q.heading=Math.PI/2;C.di=clamp(TC119.far-Math.floor(u*TC119_ART.depths.length),0,TC119.far);b.x=home.x;b.y=lerp(-400,home.y,smooth);if(done){C.flow=null;C.di=0;q.heading=Math.PI/2;fb112Set(b,'recover');q.wait=1.5;tc119Log(b,'foreground-restored');}}
 if(C.flow)for(const p of q.parts)p.angle=q.heading;
}
function tc119Effects(b,dt){const C=b._tc119,q=b._fb112;C.clock+=dt;const hot=!b.dead&&(C.flow?.state==='far-charge'||q.phase==='warn'||q.phase==='attack');C.shade+=clamp((hot?1:0)-C.shade,-dt*.45,dt*.32);
 for(const p of q.parts)p._tc119Muzzle=Math.max(0,(p._tc119Muzzle||0)-dt);
 for(const f of C.debris){f.t+=dt;f.x+=f.vx*dt;f.y+=f.vy*dt;f.vy+=180*dt;f.angle+=dt*3.1;if(f.t>.65&&!f.burst){f.burst=true;explode(f.x,f.y,f.type==='gun'?24:42,'orange');cfx114Spawn('ring',f.x,f.y,f.type==='gun'?96:160);combatAudio0927(f,'expSmall',.2);for(let i=0;i<4;i++)C.bursts.push({type:f.type,t:0,x:f.x,y:f.y,vx:(i-1.5)*80,vy:-75-i*17,angle:i});}}
 C.debris=C.debris.filter(f=>f.t<.65);for(const f of C.bursts){f.t+=dt;f.x+=f.vx*dt;f.y+=f.vy*dt;f.vy+=200*dt;f.angle+=dt*4;}C.bursts=C.bursts.filter(f=>f.t<1.1&&f.y<VH+50);
 for(const f of C.cyclones){f.t+=dt;const u=clamp(f.t/2.7,0,1);f.x=lerp(f.from.x,f.to.x,u);f.y=lerp(f.from.y,f.to.y,u);f.size=Math.min(TC119_ART.cycloneSizes.length-1,Math.floor(u*TC119_ART.cycloneSizes.length));if(f.t>2.7)f.y+=(f.t-2.7)*520;
  const r=TC119_ART.cycloneSizes[f.size]*.39;if(f.t>.7)for(const seat of seatList())withSeat(seat,()=>{if(!player.dead&&player.invuln<=0&&!f.hits.has(seat)&&Math.hypot(player.x-f.x,player.y-f.y)<r){f.hits.add(seat);playerHit('Thunderhead depth cyclone');tc119Log(b,'depth-cyclone-hit',{seat});}});}
 C.cyclones=C.cyclones.filter(f=>f.t<3.8&&f.y-TC119_ART.cycloneSizes[f.size]/2<VH+30);
 for(const r of eBullets)if(r._tc119Slug&&(r._th114Part.hp<=0||b.t-r._th114Born>r._th114Life))r.dead=true;
}
fb112Tick=function(b,dt){if(!tc119Own(b))return TC119.base.tick.apply(this,arguments);if(!fb112Ready()){stageLoadTick();return;}const C=b._tc119;TC119.owner=b;
 if(b.dead){C.flow=null;C.cyclones=[];const out=TC119.base.tick.apply(this,arguments);tc119Effects(b,dt);return out;}
 if(C.flow)tc119Flow(b,dt);else TC119.base.tick.apply(this,arguments);
 tc119Effects(b,dt);if(!b.dead)tc119Guns(b,dt);
};
fb112Damage=function(b){const own=tc119Own(b),before=own?b._fb112.parts.map(p=>p.hp):null,out=TC119.base.damage.apply(this,arguments);if(own){const C=b._tc119;
 b._fb112.parts.forEach((p,i)=>{if(before[i]>0&&p.hp<=0){const m=fb112PartPoint(b,p);const fragment={type:p.type==='gun'?'gun':'pod'+p.index,t:0,x:m.x,y:m.y,w:p.type==='gun'?70:150,h:p.type==='gun'?100:224,vx:i%2?140:-140,vy:-80,angle:p.angle-Math.PI/2};C.debris.push(fragment);unitDeathFX(fragment,'turret','blue');p._tc119Target=null;tc119Log(b,'module-breakaway',{part:p.id,x:m.x,y:m.y});}});}
 return out;};
fb112Cancel=function(b){const out=TC119.base.cancel.apply(this,arguments);if(tc119Own(b)){const C=b._tc119;C.flow=null;C.cyclones=[];C.gunPhase='idle';for(const p of b._fb112.parts)p._tc119Target=null;tc119Log(b,'cancel');}return out;};
function tc119Charge(b){const q=b._fb112,F=b._tc119.flow;return F?F.state==='far-charge'?clamp(F.t/F.dur,0,1):F.state==='recoil'?1:0:q.phase==='warn'?clamp(q.t/q.dur,0,1):q.phase==='attack'?.6:0;}
function tc119Sign(b){const C=b._tc119,F=C.flow,q=b._fb112;if(!(F?.state==='far-charge'||!F&&q.phase==='warn'))return;const u=tc119Charge(b);if(u>=2/3&&Math.floor(C.clock*12)%2)return;rd72Blit('asterisk',u>=2/3?1:0,b.x,clamp(b.y-140*tc119Scale(b),viewTopY()+65,VH-45));TC119.draws.warning=(TC119.draws.warning||0)+1;}
function tc119GunWarnings(b){const C=b._tc119;if(C.flow||C.gunPhase!=='aim')return;for(const p of b._fb112.parts)if(p.hp>0&&p._tc119Lock){fb112Warn(b,p,p.angle,C.gunT,.92,22);th114Retina({x:p._tc119Lock.x,y:p._tc119Lock.y,age:C.gunT,warm:.92});}}
function tc119Beams(b){for(const B of tm115State(b).beams){const f=B.recovery?22+Math.min(5,Math.floor(B.tail*24)):B.age<TM115.beamGrow?Math.min(5,Math.floor(B.age*24)):6+Math.floor((B.age-TM115.beamGrow)*24)%16;
 tm115Bank('wind_beam',f,B.x,B.y+14);tc119Blit(B.recovery?'beam_coupling_tail':'beam_coupling',B.recovery?Math.min(5,Math.floor(B.tail*24)):Math.floor(B.age*24)%16,B.x,B.y);const at=fb112PartPoint(b,B.part);if(B.part.hp>0)tc119Blit('pod'+B.part.index+'_lip',0,at.x,at.y);}}
fb112Draw=function(b){if(!tc119Own(b))return TC119.base.draw.apply(this,arguments);if(!fb112Ready())return;const q=b._fb112,C=b._tc119,S=th114State(b),di=C.di,k=tc119Scale(b),d=fb112Dir(q.heading,16),face=d===8?1:0,turn=d!==0&&d!==8,charge=tc119Charge(b),level=Math.min(3,Math.floor(charge*4)),pulse=THS114.reduced?0:Math.floor(C.clock*(8+charge*30))%4,phase=THS114.reduced?0:Math.floor(C.clock*(16+charge*38))%24;
 if(q.death<3){if(!b.dead&&di===0&&charge>0&&!turn)tm115Aura(b);
 tc119Blit(turn?'hull_turn_d'+di:'hull_d'+di+'_'+face,turn?d:level*4+pulse,b.x,b.y);
 const core=fb112PartPoint(b,q.core);tc119Blit(turn?'core_turn_d'+di:'core_d'+di+'_'+face,turn?d:level*24+phase,core.x,core.y);if(q.open&&q.core.flash>0&&di===0)tm115Bank('core_hit',0,core.x,core.y);
 for(const p of q.parts){const at=fb112PartPoint(b,p),dir=fb112Dir(p.angle),r=p.recoil>.035?1:0;
  if(p.hp<=0){if(di===0){const B=CF114_ART.banks.smoke_40;cf114Blit(ctx,'smoke_40',cf114Frame(B,C.clock%.9,.9),at.x,at.y-12);}continue;}
  if(p.type==='gun'){if(di===0)tc119Blit(p.flash>0?'gun_hit':'gun',p.flash>0?r*32+dir:(level*4+pulse)*64+r*32+dir,at.x,at.y);else tc119Blit('gun_d'+di,dir,at.x,at.y);
   if(p._tc119Muzzle>0&&di===0){const m=fb112Bore(b,p);rw117Blit('muzzle',(1+Math.floor(C.clock*48)%3)*32+dir,m.x,m.y);}}
  else{tc119Blit(turn?'pod'+p.index+'_turn_d'+di:'pod'+p.index+'_d'+di+'_'+face,turn?d:level*8+Math.floor(C.clock*24)%8,at.x,at.y);if(p.flash>0&&di===0)tm115Bank('pod'+p.index+'_hit',0,at.x,at.y);}
 }
 if(!b.dead)for(const e of q.M.engines){const at=fb112Point(b,e),boost=C.flow&&C.flow.state!=='far-charge';tc119Blit('thrust_'+(boost?'throttle':'cruise')+'_d'+di,(Math.floor(C.clock*18)%4)*(di===0||di===TC119.far?16:1)+d,at.x,at.y);}
 }
 for(const f of C.debris)tc119Blit(f.type+'_detach',fb112Dir(Math.PI/2+f.angle),f.x,f.y);
 for(const f of C.bursts)tc119Blit(f.type+'_shard',Math.floor(f.angle/TAU*16)&15,f.x,f.y);
 for(const f of q.fx){const B=CF114_ART.banks.small_64;cf114Blit(ctx,'small_64',cf114Frame(B,f.t,.6),f.x,f.y);}
 if(!b.dead){for(const f of S.fields)th114RoundDraw(f);for(const P of S.marks)th114Retina(P);for(const P of S.impacts){if(P.age<(THS114.reduced?.09:.24))th114Blit('bolt',Math.floor(P.age*24)%8,P.x,P.y-256);th114Blit('impact',Math.min(13,Math.floor(P.age*24)),P.x,P.y);}if(!C.flow){tc119Beams(b);tm115Warnings(b);tc119GunWarnings(b);}tc119Sign(b);if(C.flow?.state==='far-charge'&&C.aim&&C.flow.t>C.flow.dur-.85)th114Retina({x:C.aim.x,y:C.aim.y,age:C.flow.t-(C.flow.dur-.85),warm:.85});}
 for(const f of C.cyclones)tc119Blit('cyclone_'+f.size,Math.floor(f.t*30)%12,f.x,f.y);
};
th114Weather=function(){const out=TC119.base.weather.apply(this,arguments),b=boss;if(out&&tc119Own(b)){const f=Math.round(b._tc119.shade*15);for(let y=128;y<650;y+=256)for(let x=170;x<worldWidth()+340;x+=340)tc119Blit('shade',f,x,y);}return out;};
beginStage=function(){if(TC119.owner)fb112Cancel(TC119.owner);TC119.owner=null;return TC119.base.begin.apply(this,arguments);};
globalThis.BOF_THUNDERHEAD_REACTOR_1105={state:TC119,owns:tc119Own};
