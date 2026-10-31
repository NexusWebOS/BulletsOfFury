'use strict';
/* HD54: native 20% gate, authored depth turntable and Falva-derived rollers. */
const HD54={base:{tick:hd1003Tick,hit:hd1003Hit,clamp:er26DamageClamp,tell:hd1003Tell,at:hd1003At,targets:retinaBossTargets,
 draw:heraldDeathDraw,projectile:drawCombatFinalProjectile,update:updatePlay,effects:drawEffects,load:stageLoadBegin,
 intercept:enemyOrdnanceCanIntercept,element:enemyOrdnanceElement,rules:s3kOrdnanceRules,damageOverlay:encounterDamageOverlay},events:[],flights:[],serial:0};
for(const a of Object.values(HD54_ART))XART._src[a.key]=a.path;
function hd54Log(event,data={}){HD54.events.push({event,time:efxClock,...data});if(HD54.events.length>1000)HD54.events.shift();}
function hd54Boss(b){return run.stage===8&&b===subBoss&&!!b?._hd1003&&!b.dead;}
function hd54Own(b){return hd54Boss(b)&&b._hd1003.er28?._hd54?b._hd1003.er28:null;}
function hd54Protected(b){const A=hd54Own(b);return !!A&&A.phase!=='foreground'&&!b._hg70Counter;}
// Full-sized hull smoke cannot follow a small protected background skull.
encounterDamageOverlay=function(b){if(hd54Protected(b))return;return HD54.base.damageOverlay.apply(this,arguments);};
function hd54Blit(name,f,x,y,hit=false){const a=HD54_ART[name+(hit?'_hit':'')]||HD54_ART[name];if(!a||!XART.rdy(a.key))return false;f=clamp(f|0,0,a.frames-1);
 ctx.drawImage(XART.get(a.key),f%a.cols*a.cw,Math.floor(f/a.cols)*a.ch,a.cw,a.ch,Math.round(x-a.pivot[0]),Math.round(y-a.pivot[1]),a.cw,a.ch);return true;}
stageLoadBegin=function(n,keys){if(n===8)Snd.prepare(['bossWeaponCharge','wardenScream','combatOrb0927','combatAlien0927','expBig']);return HD54.base.load.call(this,n,n===8?[...(keys||[]),...Object.values(HD54_ART).map(a=>a.key)]:keys);};
function hd54Start(b){if(!hd54Boss(b))return;const H=b._hd1003,first=!H.hd54;
 H.hd54=true;hr28Start(b,'desperation');const A=H.er28;
 Object.assign(A,{_hd54:true,phase:'rumble',next:0,shots:0,spin:0,pulse:0,frame:0,bank:'front',dark:0,origin:{x:camLeftX()+viewW()/2,y:viewTopY()+170}});
 // The desperation metamorphosis physically sheds any surviving outer modules.
 for(const id of ['wingL','wingR','gunL','gunR']){const p=hd1003Part(b,id);if(hd1003Live(b,p))hd1003Break(b,p);}
 H.hs53Caster=true;H.lanes=[];H.flashes=[];
 for(const q of eBullets)if(q._heraldOwner1003===b)q.dead=true;
 for(const q of HS53.orbs)if(q._heraldOwner1003===b)q.dead=true;
 HS53.orbs.clear();HH52.skulls.clear();HD54.flights=HD54.flights.filter(q=>q.b!==b);groundTargetingCancel(b);
 combatAudio0927(b,'bossWeaponCharge',.1);hd54Log(first?'desperation-enter':'desperation-repeat',{hp:b.hp,maxhp:b.maxhp,ratio:b.hp/b.maxhp});
}
er26DamageClamp=function(b,dmg){dmg=HD54.base.clamp.apply(this,arguments);if(!hd54Boss(b))return dmg;
 if(hd54Protected(b))return 0;
 if(!b._hd1003.hd54){const floor=b.maxhp*.20;return Math.min(dmg,Math.max(0,b.hp-floor));}return dmg;};
hd1003Hit=function(b){if(hd54Protected(b))return;const r=HD54.base.hit.apply(this,arguments);
 if(hd54Boss(b)&&!b._hd1003.hd54&&b.hp<=b.maxhp*.20+.001)hd54Start(b);return r;};
hd1003At=function(b){if(hd54Protected(b))return null;return HD54.base.at.apply(this,arguments);};
retinaBossTargets=function(b){return hd54Protected(b)?[]:HD54.base.targets.apply(this,arguments);};
hd1003Tell=function(b){if(hd54Boss(b)&&b._hd1003.hd54)return hd54Start(b);return HD54.base.tell.apply(this,arguments);};
function hd54Phase(A,phase){if(A.phase!==phase){A.phase=phase;hd54Log('phase',{phase,t:A.t});}}
function hd54Emit(b,A){if(HD54.flights.filter(F=>!F.done).length>=48)return;
 const meta=(HD54_ART[A.bank]?.sockets||HD54_ART.spin.sockets)[A.frame],p={x:b.x+meta[0],y:b.y+meta[1]},n=A.shots++,spread=[-72,0,72,-36,36][n%5];
 const target={x:clamp(player.x+spread,camLeftX()+45,camRightX()-45),y:clamp(player.y+20,viewTopY()+viewH()*.65,VH-35)},flight=1.9-Math.min(.40,(A.t-7.4)*.035);
 const q={id:++HD54.serial,b,born:efxClock,life:flight,from:p,target,x:p.x,y:p.y,level:0,spin:n%32};HD54.flights.push(q);
 combatAudio0927(b,'combatOrb0927',.085);hd54Log('roller-release',{id:q.id,index:n,x:p.x,y:p.y,frame:A.frame,flight,target});
}
hd1003Tick=function(b,dt){if(hd54Boss(b)&&!b._hd1003.hd54&&b.hp<=b.maxhp*.20+.001)hd54Start(b);
 const A=hd54Own(b);if(!A)return HD54.base.tick.apply(this,arguments);const H=b._hd1003;H.clock+=dt;H.age+=dt;H.attackAge+=dt;A.t+=dt;
 b.fireCd=999;b._sba=null;b._s4MiniSafe=true;const t=A.t,top=viewTopY(),cx=camLeftX()+viewW()/2;
 A.dark=15;A.pulse+=(2+Math.min(20,Math.max(0,t-2.4)*4))*dt;A.frame=Math.floor(A.pulse*8)%32;
 if(t<.8){hd54Phase(A,'rumble');A.bank='front';b.x=A.from.x+Math.sin(t*75)*3;b.y=A.from.y+Math.sin(t*93)*2;A.dark=Math.floor(t/.8*15);shake=Math.max(shake,2);}
 else if(t<1.5){hd54Phase(A,'retreat');const u=(t-.8)/.7;A.bank='depart';A.frame=Math.min(23,Math.floor(u*24));b.x=lerp(A.from.x,cx,u);b.y=lerp(A.from.y,top-150,u);}
 else if(t<2.4){hd54Phase(A,'background-entry');const u=(t-1.5)/.9;A.bank='charge';b.x=cx;b.y=lerp(top-110,top+105,u);}
 else if(t<7.4){hd54Phase(A,'charge');const u=(t-2.4)/5;A.bank='charge';b.x=cx+Math.sin(t*93)*(1+u*4);b.y=top+105+Math.sin(t*103)*(1+u*3);
  if(Math.floor((t-dt-2.4)*3)<Math.floor((t-2.4)*3)){combatAudio0927(b,'bossWeaponCharge',.1);shake=Math.max(shake,1+u*2);}}
 else if(t<18.4){hd54Phase(A,'spin');A.spin+=(.45+Math.min(3.2,(t-7.4)*.29))*dt;A.frame=Math.floor(A.spin*32)%32;A.bank='spin';
  b.x=cx+Math.sin((t-7.4)*.72)*viewW()*.24;b.y=top+102+Math.sin(t*2)*10;
  if(t>=A.next){hd54Emit(b,A);A.next=t+Math.max(.13,.55*Math.pow(.88,A.shots))/(run.ngplus?1.15:1);}}
 else if(t<19.2){hd54Phase(A,'return-north');A.bank='spin';A.frame=Math.floor(A.spin*32)%32;b.y=lerp(top+105,top-120,(t-18.4)/.8);}
 else if(t<20.6){hd54Phase(A,'return');const u=(t-19.2)/1.4;A.bank='return';A.frame=Math.min(23,Math.floor(u*24));b.x=cx;b.y=lerp(top-120,A.origin.y,u);}
 else{hg70Foreground(b,A,dt);}
 if(A.phase==='charge'||A.phase==='rumble'){const warm=A.phase==='rumble'?.8:5,elapsed=A.phase==='rumble'?t:t-2.4;combatWarningTick(b,'hd54-'+A.serial+'-'+A.phase,elapsed,warm);}
 b._drawY=b.y;return true;
};
heraldDeathDraw=function(b){const A=hd54Own(b);if(!A)return HD54.base.draw.apply(this,arguments);
 hd54Blit(A.bank,A.frame,b.x,b.y,Math.max(b.flash||0,...b._hd1003.parts.map(p=>p.flash||0))>0);
 if(A.phase==='rumble'||A.phase==='charge')hh52Blit('star',0,b.x,b.y-(A.phase==='charge'?70:124));return true;};
function hd54OrbDraw(q){hd54Blit('orb_'+q.level,(Math.floor((efxClock-q.born)*30)+q.spin)%32,q.x,q.y);}
drawCombatFinalProjectile=function(q){if(q?._hd54){const u=clamp((efxClock-q._hd54Flight.born)/q._hd54Flight.life,0,1);if(!q._hd54Flight.surface)q._hd54Flight.level=Math.min(9,Math.floor(u*10));
  hd54OrbDraw({...q._hd54Flight,x:q.x,y:q.y});return true;}return HD54.base.projectile.apply(this,arguments);};
enemyOrdnanceCanIntercept=function(q){return q?._hd54?false:HD54.base.intercept.apply(this,arguments);};
enemyOrdnanceElement=function(q){return q?._hd54?null:HD54.base.element.apply(this,arguments);};
s3kOrdnanceRules=function(q){if(q?._hd54){q._weaponProof=true;q._shootable=false;delete q.hp;return;}return HD54.base.rules.apply(this,arguments);};
updatePlay=function(dt){for(const F of HD54.flights){if(F.b!==subBoss||F.b.dead||run.stage!==8){if(F.q)F.q.dead=true;F.done=true;continue;}
 if(F.done)continue;if(F.returning){hg70Return(F);continue;}
 const u=clamp((efxClock-F.born)/F.life,0,1);if(!F.surface)F.level=Math.min(9,Math.floor(u*10));F.x=lerp(F.from.x,F.target.x,u);F.y=lerp(F.from.y,F.target.y,u);
 if(!F.q&&u>=.65){const q=eShootT(F.x,F.y,Math.atan2(F.target.y-F.y,F.target.x-F.x),1,'s8pair',{owner:F.b,noMuzzle:true,silent:true,w:10,h:10});
  if(q){const remain=Math.max(.1,F.life*(1-u));q.vx=(F.target.x-F.x)/(remain*60);q.vy=(F.target.y-F.y)/(remain*60);
   Object.assign(q,{_hd54:true,_hd54Flight:F,_hd54Born:efxClock,_heraldOwner1003:F.b,_heraldPart1003:'head',_noArsenal:true,_boss:true,_weaponProof:true,_shootable:false,_s3kOriginalProof:false,homing:false});delete q.hp;F.q=q;
   hd54Log('roller-foreground',{id:F.id,x:q.x,y:q.y,level:F.level});}}
 if(F.q){const d=HD54_ART['orb_'+F.level].diameter;F.q.w=F.q.h=Math.max(8,d*.68);if(F.q.dead||efxClock-F.born>F.life+2){F.q.dead=true;F.done=true;}}
 }
 hg70Intercept(dt);const out=HD54.base.update.apply(this,arguments);HD54.flights=HD54.flights.filter(F=>!F.done&&(!F.q||!F.q.dead));return out;};
drawEffects=function(){const out=HD54.base.effects.apply(this,arguments);for(const F of HD54.flights)if(!F.q&&!F.done)hd54OrbDraw(F);return out;};
globalThis.BOF_HERALD_DESPERATION_1029={state:HD54,start:hd54Start};
