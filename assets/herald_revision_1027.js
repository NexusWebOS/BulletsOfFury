"use strict";
/* Native modular Herald HP, breakup, defeat and rewards remain the authority.
   New charge/attack poses and effects use fixed authored atlas cells. */
const HR28={base:{tell:hd1003Tell,tick:hd1003Tick,pose:hd1003Pose,blit:hd1003Blit,draw:heraldDeathDraw,
 bg:drawBG,projectile:drawCombatFinalProjectile,intercept:enemyOrdnanceCanIntercept,rules:s3kOrdnanceRules,element:enemyOrdnanceElement,update:updatePlay},events:[]};
function hr28Log(b,event,data={}){HR28.events.push({event,time:efxClock,attack:b._hd1003?.er28?.kind,...data});if(HR28.events.length>1200)HR28.events.shift();}
function hr28Start(b,kind){const H=b._hd1003;H.seq++;H.mode='er28-herald';H.age=H.attackAge=0;H.lanes=[];H.flashes=[];
 delete H._hb25;delete H._hp22;delete H._hd19;if(b._hc1007)b._hc1007.cross=null;
 S81003.beams=S81003.beams.filter(q=>q.owner!==b);groundTargetingCancel(b);
 const warm={storm:2.05,nuke:2.6,rage:1.9,pentagram:2.4}[kind],origin={x:camLeftX()+viewW()/2,y:viewTopY()+155};
 H.er28={kind,t:0,warm,phase:'charge',origin,from:{x:b.x,y:b.y},center:{x:camLeftX()+viewW()/2,y:viewTopY()+viewH()*.58},shot:0,beat:-1,hit:new Set(),dark:0,serial:H.seq};
 H.history.push('er28-'+kind);if(H.history.length>30)H.history.shift();b._s4MiniSafe=true;
 combatAudio0927(b,'bossWeaponCharge',.1);hr28Log(b,'charge',{warm});
}
hd1003Tell=function(b){if(!b?._hd1003||b!==subBoss)return HR28.base.tell.apply(this,arguments);const H=b._hd1003;
 // The repeated side pass is his identity. Corner swoops interrupt its rhythm;
 // a special attack always returns to a clear recovery before another pass.
 const book=['bomber','storm','bomber','nuke','swoop','rage','bomber','pentagram','bomber','swoop'];
 let kind=book[(H.er28Turn||0)%book.length];H.er28Turn=(H.er28Turn||0)+1;
 if(['bomber','swoop'].includes(kind)){delete H.er28;return hb25Flight(b,kind);}
 if(kind==='pentagram'&&!hb25Claws(b).length)kind='rage';return hr28Start(b,kind);
};
function hr28Round(b,x,y,a,speed,kind='code'){if(eBullets.filter(q=>q._heraldOwner1003===b&&!q.dead).length>=128)return null;
 const q=eShootT(x,y,a,speed,'s8pair',{owner:b,noMuzzle:true,silent:true,w:kind==='death'?70:12,h:kind==='death'?70:12});
 Object.assign(q,{_er28Herald:kind,_er28Born:efxClock,_heraldOwner1003:b,_heraldPart1003:'head',_weaponProof:true,_shootable:false,_noArsenal:true,_boss:true});delete q.hp;return q;}
function hr28Ring(b,p,n,phase=0,speed=2.7){for(let i=0;i<n;i++)hr28Round(b,p.x,p.y,i*TAU/n+phase,speed);}
function hr28CastPoint(b){const points=hb25Claws(b).map(id=>hd1003Muzzle(b,id));return points.length?{x:points.reduce((s,p)=>s+p.x,0)/points.length,y:points.reduce((s,p)=>s+p.y,0)/points.length}:hd1003Muzzle(b,'head');}
function hr28Contact(A,key,check,cause){for(const seat of seatList())withSeat(seat,()=>{const id=key+':'+seat;if(!A.hit.has(id)&&!player.dead&&check(player)){A.hit.add(id);playerHit(cause);}});}
function hr28Tornadoes(A){const l=camLeftX(),w=viewW(),top=viewTopY(),h=viewH(),t=Math.max(0,A.t-A.warm);
 return[0,1].map(i=>{const a=t*.8+i*Math.PI;return{x:l+w/2+Math.cos(a)*w*.31,y:top+h*.54+Math.sin(a)*h*.19};});}
function hr28End(b){const H=b._hd1003;H.mode='rest';H.age=0;H.attackAge=0;H.lanes=[];delete H.er28;b._s4MiniSafe=false;hr28Log(b,'recovery-complete');}
hd1003Tick=function(b,dt){const H=b?._hd1003,A=H?.er28;if(!A||H.mode!=='er28-herald')return HR28.base.tick.apply(this,arguments);if(b.dead)return true;
 H.clock+=dt;H.age+=dt;H.attackAge+=dt;A.t+=dt;b.fireCd=999;b._sba=null;b._s4MiniSafe=true;
 const approach=clamp(A.t/.8,0,1);b.x=lerp(A.from.x,A.origin.x,approach);b.y=lerp(A.from.y,A.origin.y,approach)+Math.sin(H.clock*2)*3;b._drawY=b.y;
 if(A.t<A.warm){A.phase='charge';A.dark=Math.min(15,Math.floor(A.t/A.warm*15));combatWarningTick(b,'hr28-'+A.serial,A.t,A.warm);return true;}
 const u=A.t-A.warm,rate=run.ngplus?1.15:1;
 if(A.phase==='charge'){A.phase='active';combatAudio0927(b,'wardenScream',.1);hr28Log(b,'release');}
 A.dark=15;
 if(A.kind==='storm'){
  const points=hr28Tornadoes(A);for(let i=0;i<points.length;i++){const p=points[i];hr28Contact(A,'tornado-'+i+'-'+Math.floor(u/.4),q=>((q.x-p.x)/37)**2+((q.y-p.y)/126)**2<1,'Herald chaos tornado');}
  A.shot-=dt*rate;if(A.shot<=0&&u<4.6){A.shot=.43;const p=points[A.beat++%2===0?0:1];hr28Ring(b,p,6+bh25Rank()*2,u*.75,2.05);combatAudio0927(b,'combatOrb0927',.3);}
  if(u>=4.8)A.phase='recover';if(u>=6)hr28End(b);
 }else if(A.kind==='nuke'){
  if(!A.ball){const p=hr28CastPoint(b);A.ball=hr28Round(b,p.x,p.y,Math.PI/2,0,'death');A.ballFrom=p;A.ballAt=efxClock;}
  if(u<1&&A.ball){A.ball.x=lerp(A.ballFrom.x,A.center.x,u);A.ball.y=lerp(A.ballFrom.y,A.center.y,u);A.ball.vx=A.ball.vy=0;}
  else if(u<2.05){if(A.ball)A.ball.dead=true;A.explosion=u-1;const radius=viewW()*.425*Math.min(1,(u-1)/.32);
   hr28Contact(A,'nuke',q=>Math.hypot(q.x-A.center.x,q.y-A.center.y)<radius,'Herald skull death nuke');
   if(!A.blastCue){A.blastCue=true;combatAudio0927(b,'timedBombBlast',.1);shake=Math.max(shake,8);hr28Log(b,'nuke-impact',{width:viewW()*.85,edgeSafeWidth:viewW()*.075});}
  }else{A.explosion=null;A.phase='recover';if(u>3.15)hr28End(b);}
 }else if(A.kind==='rage'){
  const beat=Math.floor(u/(.60/rate));A.flashAge=(u%( .60/rate));
  if(beat<6&&beat>A.beat){A.beat=beat;A.bolts=[];const l=camLeftX()+40,r=camRightX()-40,gap=72,escape=beat%2?l+gap:r-gap;
   for(let i=0;i<5+bh25Rank();i++){const x=lerp(l,r,i/(4+bh25Rank()));if(Math.abs(x-escape)<52)continue;A.bolts.push({x,y:viewTopY()+256});hr28Round(b,x,viewTopY()+25,Math.PI/2,4.3);}
   combatAudio0927(b,'combatBeam0927',.1);combatAudio0927(b,'wardenScream',.45);hr28Log(b,'red-lightning-volley',{beat,count:A.bolts.length,escape});
  }
  if(beat<6&&A.flashAge<.15)for(let i=0;i<(A.bolts||[]).length;i++){const p=A.bolts[i];hr28Contact(A,'bolt-'+beat+'-'+i,q=>Math.abs(q.x-p.x)<13,'Herald red lightning');}
  if(beat>=6){A.bolts=[];A.phase='recover';if(u>6*(.60/rate)+1.1)hr28End(b);}
 }else if(A.kind==='pentagram'){
  if(!A.sigil){const p=hr28CastPoint(b);A.sigil=hr28Round(b,p.x,p.y,Math.PI*.27,3.0,'pentagram');if(A.sigil){A.sigil.w=A.sigil.h=80;A.sigil._er28Bounces=0;}}
  if(u>8.5||A.sigil?._er28Bounces>=6){if(A.sigil)A.sigil.dead=true;A.phase='recover';if(u>9.4)hr28End(b);}
 }
 if(A.phase==='recover')A.dark=Math.max(0,15-Math.floor((A.recoverAge=(A.recoverAge||0)+dt)*18));
 return true;
};
hd1003Pose=function(b,p){const A=b?._hd1003?.er28;if(!A||b._hd1003.mode!=='er28-herald')return HR28.base.pose.apply(this,arguments);
 const H=b._hd1003,s=p.spec,side=p.id.endsWith('L')?-1:1,u=clamp(A.t/A.warm,0,1);let a=0,x=b.x+s.attach[0],y=b.y+s.attach[1];
 if(p.id.startsWith('wing')){const rate=A.kind==='rage'?4+u*11:4;a=side*(-.22-.33*u+Math.sin(H.clock*rate)*(.12+.12*u));}
 if(p.id.startsWith('gun')){a=side*(A.kind==='nuke'||A.kind==='pentagram'?.36:-.78)*u;y-=u*24;}
 if(p.id==='head'&&A.kind==='rage'&&A.t>A.warm){x+=Math.sin(H.clock*64)*2;y+=Math.cos(H.clock*51)*2;}
 if(p.id!=='head'&&p.id!=='core')a=-.9+Math.round((clamp(a,-.9,.9)+.9)/.06)*.06;
 return{x,y,a,s:s.scale};
};
hd1003Blit=function(p,P,flash=0,alpha=1){const b=subBoss,A=b?._hd1003?.er28;if(!A||b._hd1003.mode!=='er28-herald'||b.dead)return HR28.base.blit.apply(this,arguments);
 if(p.id==='head'){const name=A.kind==='pentagram'?'head_grin':'head_rage',f=A.kind==='rage'&&A.phase==='active'?Math.floor(b._hd1003.clock*24)%16:Math.min(15,Math.floor(A.t/Math.max(1,A.warm)*16));return er28Blit(name,f,P.x,P.y,flash>0);}
 const name='herald_'+p.id,a=ER28_ART[name],f=p.id==='core'?0:Math.round((P.a-a.angleMin)/a.angleStep);return er28Blit(name,f,P.x,P.y,flash>0);
};
drawBG=function(){const out=HR28.base.bg.apply(this,arguments),A=subBoss?._hd1003?.er28;if(run.stage===8&&A&&A.dark>0&&!subBoss.dead){for(let y=Math.floor(viewTopY()/64)*64;y<VH;y+=64)for(let x=Math.floor(camLeftX()/64)*64;x<camRightX();x+=64){er28Blit('dark',A.dark,x+32,y+32);if(A.kind==='rage'&&A.phase==='active'&&A.flashAge<.23)er28Blit('red_flash',Math.min(15,Math.floor(A.flashAge/.23*16)),x+32,y+32);}}return out;};
heraldDeathDraw=function(b){const A=b?._hd1003?.er28;if(A&&!b.dead&&b._hd1003.mode==='er28-herald'){
 const u=A.t-A.warm;
 if(A.kind==='storm'){
  if(u<0)for(let i=0;i<12;i++){const a=i*TAU/12,c=camLeftX()+viewW()/2,y=viewTopY()+viewH()*.54;combatWarningDraw(b,{x:c+Math.cos(a)*viewW()*.31,y:y+Math.sin(a)*viewH()*.19,ex:c+Math.cos(a+.3)*viewW()*.31,ey:y+Math.sin(a+.3)*viewH()*.19,width:75,progress:A.t/A.warm,fieldOnly:true});}
  else if(u<4.8)for(const p of hr28Tornadoes(A))er28Blit('tornado',Math.floor(u*24)%16,p.x,p.y);
 }
 if(A.kind==='nuke'){
  if(u<1)combatWarningDraw(b,{x:A.center.x,y:viewTopY(),ex:A.center.x,ey:VH,width:viewW()*.85,progress:clamp(A.t/(A.warm+1),0,1),fieldOnly:true});
  if(A.explosion!=null)er28Blit('nuke',Math.min(15,Math.floor(A.explosion/1.05*16)),A.center.x,A.center.y);
 }
 if(A.kind==='rage'){
  if(u<0)for(let i=0;i<5+bh25Rank();i++){const x=camLeftX()+40+i*(viewW()-80)/(4+bh25Rank());combatWarningDraw(b,{x,y:viewTopY(),ex:x,ey:VH,width:27,progress:A.t/A.warm,fieldOnly:true});}
  if(A.flashAge<.23&&A.phase==='active')for(const p of A.bolts||[])er28Blit('lightning',Math.floor(A.flashAge/.23*16),p.x,p.y);
 }
 if(u<0&&['nuke','pentagram'].includes(A.kind)){const p=hr28CastPoint(b);er28Blit(A.kind==='nuke'?'death_ball':'pentagram',Math.min(15,Math.floor(A.t/A.warm*16)),p.x,p.y);}
 }return HR28.base.draw.apply(this,arguments);};
enemyOrdnanceCanIntercept=function(q){return !q?._er28Herald&&HR28.base.intercept.apply(this,arguments);};
enemyOrdnanceElement=function(q){return q?._er28Herald?null:HR28.base.element.apply(this,arguments);};
s3kOrdnanceRules=function(q){if(q?._er28Herald){q._weaponProof=true;q._shootable=false;delete q.hp;return;}return HR28.base.rules.apply(this,arguments);};
drawCombatFinalProjectile=function(q){if(q._er28Herald){const age=efxClock-q._er28Born,name=q._er28Herald==='death'?'death_ball':q._er28Herald==='pentagram'?'pentagram':'code_round';return er28Blit(name,Math.floor(age*24)%16,q.x,q.y);}return HR28.base.projectile.apply(this,arguments);};
updatePlay=function(dt){const out=HR28.base.update.apply(this,arguments);for(const q of [...eBullets])if(q._er28Herald){const b=q._heraldOwner1003;
 if(!b||b!==subBoss||b.dead||run.stage!==8||efxClock-q._er28Born>10){q.dead=true;continue;}
 if(q._er28Herald==='pentagram'&&!q.dead){const pad=48,l=camLeftX()+pad,r=camRightX()-pad,t=viewTopY()+pad,d=VH-pad;let bounce=false;
  if(q.x<l){q.x=l;q.vx=Math.abs(q.vx);bounce=true;}else if(q.x>r){q.x=r;q.vx=-Math.abs(q.vx);bounce=true;}
  if(q.y<t){q.y=t;q.vy=Math.abs(q.vy);bounce=true;}else if(q.y>d){q.y=d;q.vy=-Math.abs(q.vy);bounce=true;}
  if(bounce){q._er28Bounces++;hr28Ring(b,q,10+bh25Rank()*2,q._er28Bounces*.21,2.4);combatAudio0927(b,'combatOrb0927',.1);hr28Log(b,'pentagram-bounce',{count:q._er28Bounces,x:q.x,y:q.y});}
 }}return out;};
globalThis.BOF_HERALD_REVISION_1027={state:HR28,start:hr28Start};
