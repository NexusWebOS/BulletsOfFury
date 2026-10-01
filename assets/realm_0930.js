"use strict";
/* Stage 8: three encounter lives, destructible code constructs and a returning
   portal. One pose owns drawing, hits and Retina. No shell pays stage rewards. */
for(const [k,a] of Object.entries(REALM30_ART))XART._src['r30_'+k]=a.path;
const R30_BASE={build:vile24BuildForm,spawn:spawnBoss,update:updateBoss,draw:drawBossSprite,
 part:modularPartAt,hit:modularHit,die:bossDie,health:bossHealthVisible,frac:bossHealthFraction,
 targets:retinaBossTargets,projectile:drawCombatFinalProjectile,enemy:drawEnemy,hitEnemy:hitEnemy,
 bg:drawBG,player:drawPlayer,begin:beginStage,fill:bmbarFill,bar:drawHealthBarV2,drawBoss:drawBoss,hitTest:bossHitTest,shieldFrac:bossShieldFrac};
function r30Difficulty(){return {easy:0,normal:0,hard:1,furious:2,insanity:3}[diffKey]||0;}
function r30Sound(k){try{(Audio.SFX[k]||Audio.SFX.combatAlien0927||Audio.SFX.expBig||function(){})();}catch(_e){}}
function r30Warm(){for(const k of Object.keys(REALM30_ART))XART.rdy('r30_'+k);for(const k of ['vile24_robot_gray','vile24_alien_final','vile25_void_knight','enc30_entry',...PILOTS.map(p=>'ship_'+p.key)])XART.rdy(k);_liquidFrames('nlq_sludgeF');}
function r30Blit(k,x,y,w,h,a,alpha){return rot5Draw(REALM30_ART[k]?'r30_'+k:k,x,y,w,h,a||0,alpha==null?1:alpha);}
function r30FX(b,x,y,size,kind){const S=b._r30;S.fx.push({x,y,size,kind:kind||'death',t:0});if(S.fx.length>48)S.fx.shift();}
function r30Form(b,n){
 const S=b._r30,base=S.base,total=Math.ceil(base*[1,1.4,4][n]);
 S.form=n;S.seq=0;S.attack=null;S.cd=1.3;S.pose=n===0?'possessed':n===1?'ghost':'colossus';S.shape=S.pose;S.shield=0;S.shieldMax=1;
 b._vForm=n;b._vPhaseHp=total;b.hp=b.maxhp=total;b.w=n===2?470:260;b.h=n===2?260:230;b.ty=n===2?160:166;b.x=worldWidth()/2;b.y=b.ty;
 b.parts=[{id:'core',rc:'central_core',share:.6},{id:'left',rc:'left_systems',share:.2},{id:'right',rc:'right_systems',share:.2}].map(p=>({...p,dmg:true,hp:total*p.share,maxhp:total*p.share,destroyed:false,flash:0}));
 b.modular=true;b._v24={shield:0,shieldMax:1,pattern:null,foes:[],shards:[],muzzles:[],seq:0};
 b.name=['THE POSSESSED HOST','THE GHOST IN THE CODE','THE VILE COLOSSUS'][n];b._morphT=null;b._symEntry=null;b.dead=false;
 S.history.push({event:'form',form:n,hp:total});
}
vile24BuildForm=function(b,n){if(!b._r30){b._r30={base:b._vBase||b.maxhp||1800,form:0,mode:'takeover',t:0,clock:0,fx:[],history:[],walls:[],attack:null,pose:'possessed',seq:0,shield:0};r30Warm();}r30Form(b,Math.min(2,n));};
spawnBoss=function(){const r=R30_BASE.spawn.apply(this,arguments);if(boss?._r30){const b=boss,S=b._r30;S.base=b.maxhp;S.mode='takeover';S.t=0;b.enter=true;b._symEntry=null;b._morphT=null;S.history.push({event:'takeover'});}return r;};
beginStage=function(n){const r=R30_BASE.begin.apply(this,arguments);if(n===8){r30Warm();run._realmReturned=false;}return r;};
function r30Live(b){return !!(b?._r30&&b._r30.mode==='fight'&&!b.dead&&!b.enter);}
function r30Pose(b){
 const S=b._r30,P=S.attack,t=P?P.t:0,active=t-(P?P.tell:0);let x=b.x,y=b.y,angle=0,alpha=1,shape=S.shape;
 if(P&&['ghost','knight'].includes(P.type)){
  const cycle=P.cycle||0,u=clamp((active-cycle*1.5)/1.5,0,1);
  if(active>=0){if(u<.22){alpha=1-u/.22;S.ghostHidden=alpha<.25;}else if(u<.42){alpha=0;S.ghostHidden=true;}else{alpha=clamp((u-.42)/.14,0,1);x=P.tx;y=P.ty-28;S.ghostHidden=false;}}
 }else S.ghostHidden=false;
 if(P?.type==='ball'&&active>=0){const u=clamp(active/P.active,0,1);x=lerp(P.fromX,P.tx,Math.sin(u*Math.PI));y=lerp(P.fromY,P.ty,Math.sin(u*Math.PI));angle=active*4;}
 if(P&&['chopper','furnace','ghost','knight','ball'].includes(P.type)){
  if(P.t<.3)alpha*=1-P.t/.3;
  else{shape=P.type;alpha*=clamp((P.t-.3)/.3,0,1);}
 }
 if(S.returning){const u=S.returning.t;if(u<.3){shape=S.returning.from;alpha*=1-u/.3;}else alpha*=clamp((u-.3)/.3,0,1);}
 return {x,y,angle,alpha,shape};
}
function r30Parts(b){
 const S=b._r30,Q=r30Pose(b),wide=Q.shape==='colossus',armH=wide?250:134,spread=wide?118:72;
 const P=S.attack,u=P?P.t-P.tell:0,sweep=P&&P.type==='arms'&&u>0?Math.sin(clamp(u/P.active,0,1)*Math.PI):0;
 const a=(wide?.08:.03)*Math.sin(S.clock*1.4),out=[];
 for(const p of b.parts){
  let x=Q.x,y=Q.y,w=wide?280:164,h=wide?260:180,rot=0,key=wide?'colossus_body':'possessed_body';
  if(p.id!=='core'){const side=p.id==='left'?-1:1;rot=side*(a+sweep*.82);const rootX=Q.x+side*spread,rootY=Q.y-(wide?50:35);
   x=rootX-Math.sin(rot)*armH*.40;y=rootY+Math.cos(rot)*armH*.40;w=wide?130:58;h=armH;key=(wide?'colossus_arm':'possessed_arm')+(side<0?'L':'R');}
  if(!['possessed','colossus'].includes(Q.shape)){
   if(p.id!=='core')continue;x=Q.x;y=Q.y;w=Q.shape==='chopper'?225:Q.shape==='furnace'?270:180;h=Q.shape==='chopper'?270:Q.shape==='furnace'?290:210;
   key=Q.shape==='chopper'?'chopper_body':Q.shape==='furnace'?'furnace':Q.shape==='knight'?'vile25_void_knight':Q.shape==='ball'?'fx_6':'vile24_alien_final';rot=Q.angle;
  }
  if(p.destroyed&&p.id!=='core'&&!['fall','finalFall'].includes(S.mode))continue;
  out.push({p,x,y,w,h,rot,key,alpha:Q.alpha});
 }
 return out;
}
function r30At(b,x,y){
 if(!r30Live(b))return null;
 const Q=r30Pose(b),S=b._r30;
 if(S.ghostHidden)return null;
 if(S.shield>0){const q=r30ShieldBounds(b);if(((x-q.x)/(q.w*.5))**2+((y-q.y)/(q.h*.5))**2<1)return {id:'shield',hp:S.shield,dmg:true};}
 for(const v of r30Parts(b).reverse()){const dx=x-v.x,dy=y-v.y,c=Math.cos(v.rot),s=Math.sin(v.rot),xx=dx*c+dy*s,yy=-dx*s+dy*c;
  if(v.alpha>.25&&Math.abs(xx)<v.w*.43&&Math.abs(yy)<v.h*.44)return v.p;}
 return null;
}
function r30ShieldBounds(b){const parts=r30Parts(b),bounds=parts.map(v=>{const w=Math.abs(v.w*Math.cos(v.rot))+Math.abs(v.h*Math.sin(v.rot)),h=Math.abs(v.h*Math.cos(v.rot))+Math.abs(v.w*Math.sin(v.rot));return [v.x-w/2,v.y-h/2,v.x+w/2,v.y+h/2];});
 const l=Math.min(...bounds.map(v=>v[0])),t=Math.min(...bounds.map(v=>v[1])),r=Math.max(...bounds.map(v=>v[2])),bt=Math.max(...bounds.map(v=>v[3]));return{x:(l+r)/2,y:(t+bt)/2,w:r-l+14,h:bt-t+14};}
modularPartAt=function(x,y){return boss?._r30?r30At(boss,x,y):R30_BASE.part(x,y);};
bossHitTest=function(x,y){if(!boss?._r30)return R30_BASE.hitTest(x,y);boss._lastPart=r30At(boss,x,y);return !!boss._lastPart;};
modularHit=function(dmg){
 const b=boss,S=b?._r30;if(!S)return R30_BASE.hit.apply(this,arguments);if(!r30Live(b)||!Number.isFinite(dmg)||dmg<=0)return;
 const p=b._lastPart||b.parts.find(p=>p.id==='core');markHit(b,.12);
 if(S.shield>0){S.shield=Math.max(0,S.shield-dmg);S.shieldFlash=.12;if(!S.shield){r30FX(b,b.x,b.y,b.w,'shield');r30Sound('shieldBreakCombat');}return;}
 // Transformations retain the same shared life pool; no free HP from changing shapes.
 let left=dmg,first=p.destroyed?b.parts.find(q=>!q.destroyed):p;
 for(const q of [first,...b.parts.filter(q=>q!==first)]){if(!q||q.destroyed||left<=0)continue;const take=Math.min(q.hp,left);q.hp-=take;left-=take;q.flash=.12;
  if(q.hp<=0){q.destroyed=true;const v=r30Parts(b).find(v=>v.p===q);r30FX(b,v?.x||b.x,v?.y||b.y,q.id==='core'?150:90);r30Sound('expBig');}}
 b.hp=b.parts.reduce((v,p)=>v+Math.max(0,p.hp),0);stageStats.dmgDealt+=dmg-left;if(b.hp<=.001)r30Break(b);
};
function r30Clear(b){eBullets.length=0;pBullets.length=0;playerLocks.length=0;for(const e of enemies)if(e._r30Wall)e.dead=true;b._r30.walls=[];}
function r30Break(b){const S=b._r30;if(S.mode!=='fight')return;S.mode=S.form<2?'fall':'finalFall';S.t=0;S.origin={x:b.x,y:b.y};S.attack=null;S.shield=0;b.enter=true;b.hp=0;S.history.push({event:'shellBroken',form:S.form});r30Clear(b);Audio.stopMusic();r30Sound('expBoss');}
bossDie=function(){if(boss?._r30&&!boss._r30.rewarded){r30Break(boss);return;}return R30_BASE.die.apply(this,arguments);};
function r30Wall(b,type){
 const S=b._r30,n=r30Difficulty(),count=5,gap=(S.seq*2+1)%count,span=camRightX()-camLeftX()-24,left=camLeftX()+12,step=span/count;
 for(let i=0;i<count;i++){if(i===gap)continue;const e={type:'realm-data-wall',_r30Wall:true,_r30Binary:type==='binarywall',x:left+step*(i+.5),y:clamp(b.y+b.h*.5+18,220,VH-145),w:step-10,h:58,hp:12+n*7,maxhp:12+n*7,t:0,vx:0,vy:0,pattern:'ground',speed:0,shoots:false,fireCd:99999,score:0,flash:0,ground:true,_born:stageTimer,_r30Owner:b,_r30Life:10};enemies.push(e);S.walls.push(e);}
 S.history.push({event:type,gap});
}
function r30Shot(b,kind,x,y,a,speed){
 const n=r30Difficulty(),k=kind==='bomb'?9:kind==='matter'?10:8,q=eShootT(x,y,a,speed*(1+n*.10),'s8pair',{w:kind==='bolt'?12:25,h:kind==='bolt'?24:25,silent:true});
 q._r30Shot=k;q._boss=true;q._noArsenal=true;q._noAutoface=false;q._r30Age=0;q._r30Owner=b;
 if(kind==='bomb'){q.hp=3+n;q._shootable=true;q._r30Fuse=1.7;}return q;
}
function r30Attack(b){
 const S=b._r30,n=r30Difficulty(),lists=[['binary','bombs','datawall','cannons','shield','tentacles'],['ghost','knight','ball','binarywall','codeRain','bombs'],['arms','tentacles','binarywall','chopper','arms','furnace','codeRain','shield','ghost','knight','ball']];
 const type=lists[S.form][S.seq++%lists[S.form].length];
 S.attack={type,t:0,tell:[1.2,1.0,.82,.74][n],active:['ghost','knight'].includes(type)?(2+n)*1.5:['chopper','furnace'].includes(type)?5:3.1,next:0,cycle:0,tx:clamp(player.x,camLeftX()+42,camRightX()-42),ty:clamp(player.y,170,VH-68),fromX:b.x,fromY:b.y};
 S.history.push({event:'attack',type,form:S.form});combatWarningTick(b,'r30-'+S.seq,0,S.attack.tell,true);r30Sound('bossWeaponCharge');
 if(['chopper','furnace','ghost','knight','ball'].includes(type)){r30FX(b,b.x,b.y,270,'morph');r30Sound('teleportIn');}
}
function r30AttackTick(b,dt){
 const S=b._r30,n=r30Difficulty(),P=S.attack;if(!P)return;P.t+=dt;const u=P.t-P.tell;
 combatWarningTick(b,'r30-'+S.seq,Math.min(P.t,P.tell),P.tell);
 if(u<0)return;
 if(!P.started){P.started=true;if(['datawall','binarywall'].includes(P.type))r30Wall(b,P.type);
  if(P.type==='shield'){S.shieldMax=Math.ceil(S.base*.06);S.shield=S.shieldMax;r30Sound('combatEnergy0927');}
 }
 if(['ghost','knight'].includes(P.type)){
  const cycle=Math.floor(u/1.5),local=u-cycle*1.5;if(cycle!==P.cycle){P.cycle=cycle;P.tx=clamp(player.x,camLeftX()+40,camRightX()-40);P.ty=clamp(player.y,175,VH-70);P.struck=false;}
  if(local>1.0&&!P.struck){P.struck=true;r30FX(b,P.tx,P.ty,100);r30Sound('hammerImpact');for(const seat of seatList())withSeat(seat,()=>{if(Math.hypot(player.x-P.tx,player.y-P.ty)<42)playerHit('alien claw');});}
 }else if(P.type==='ball'){
  const Q=r30Pose(b);for(const seat of seatList())withSeat(seat,()=>{if(Math.hypot(player.x-Q.x,player.y-Q.y)<49)playerHit('symbiote mass');});
 }
 if(P.type==='arms'){
  for(const v of r30Parts(b).filter(v=>v.p.id!=='core')){const tip={x:v.x-Math.sin(v.rot)*v.h*.37,y:v.y+Math.cos(v.rot)*v.h*.37};
   for(const seat of seatList())withSeat(seat,()=>{if(Math.hypot(player.x-tip.x,player.y-tip.y)<34)playerHit('symbiote talon');});}
 }
 if(P.type==='tentacles'&&u>.28&&u<.60&&!P.struck){P.struck=true;r30FX(b,P.tx,P.ty,98,'morph');r30Sound('combatModule0927');for(const seat of seatList())withSeat(seat,()=>{if(Math.hypot(player.x-P.tx,player.y-P.ty)<34)playerHit('tentacle');});}
 if(u>=P.next&&['binary','bombs','cannons','codeRain','chopper','furnace'].includes(P.type)){
  P.next=u+([.72,.60,.48,.42][n])*(P.type==='bombs'?1.8:1);
  const kind=P.type==='bombs'?'bomb':P.type==='furnace'?'matter':'bolt',spread=P.type==='cannons'?1:3+n;
  if(P.type==='codeRain'){
   const gap=(Math.floor(u*2)+S.seq)%6;for(let i=0;i<6;i++)if(i!==gap&&i!==((gap+1)%6))r30Shot(b,'bolt',camLeftX()+(camRightX()-camLeftX())*(i+.5)/6,55,Math.PI/2,2.6);
  }else for(const side of [-1,1]){
   if(S.form===0&&b.parts.find(p=>p.id===(side<0?'left':'right')).destroyed)continue;
   const x=b.x+side*(P.type==='furnace'?76:65),y=b.y+50,angle=Math.atan2(P.ty-y,P.tx-x);
   for(let i=0;i<spread;i++)r30Shot(b,kind,x,y,angle+(i-(spread-1)/2)*.15,kind==='bomb'?2.2:3.4);
  }r30Sound(P.type==='chopper'?'overlordGun':'enemyBossCannon');
 }
 if(u>P.active){S.attack=null;S.ghostHidden=false;S.cd=[1.15,.85,.78,.72][n];S.history.push({event:'recover'});if(['chopper','furnace','ghost','knight','ball'].includes(P.type)){S.returning={t:0,from:P.type};r30FX(b,b.x,b.y,280,'morph');}}
}
function r30Tick(b,dt){
 const S=b._r30;dt=Math.min(.05,dt);S.t+=dt;S.clock+=dt;b.t+=dt;b.flash=Math.max(0,(b.flash||0)-dt);S.shieldFlash=Math.max(0,(S.shieldFlash||0)-dt);
 if(S.returning){S.returning.t+=dt;if(S.returning.t>=.6)S.returning=null;}
 for(const p of b.parts)p.flash=Math.max(0,p.flash-dt);for(const f of S.fx)f.t+=dt;S.fx=S.fx.filter(f=>f.t<.7);
 for(const q of eBullets.slice()){if(!q._r30Shot)continue;q._r30Age+=dt;if(q._r30Fuse&&q._r30Age>q._r30Fuse&&!q.dead){q.dead=true;r30FX(b,q.x,q.y,70);r30Sound('expSmall');const a=Math.atan2(player.y-q.y,player.x-q.x);for(const offset of [-.55,-.28,.28,.55])r30Shot(b,'bolt',q.x,q.y,a+offset,2.5);}}
 for(const e of S.walls){if(e.dead)continue;e.t+=dt;e.flash=Math.max(0,e.flash-dt);e._r30Life-=dt;e.y+=dt*(e._r30Binary?12+r30Difficulty()*6:5);if(e._r30Life<=0||e.y>VH+e.h){e.dead=true;r30FX(b,e.x,e.y,e.w,'wall');}}
 if(S.mode==='fight'){
  b.enter=false;b.x=worldWidth()/2+Math.sin(S.clock*.48)*(S.form===2?12:38);b.y=b.ty+Math.sin(S.clock*.7)*6;
  if(S.attack)r30AttackTick(b,dt);else {S.cd-=dt;if(S.cd<=0)r30Attack(b);}return;
 }
 b.enter=true;eBullets.length=0;for(const seat of seatList())withSeat(seat,()=>{player.invuln=Math.max(player.invuln||0,.3);});
 if(S.mode==='takeover'){
  if(S.t>5.8){S.mode='fight';S.t=0;b.enter=false;bossPhaseMusic(8,1);}return;
 }
 if(S.mode==='fall'||S.mode==='finalFall'){
  b.y=S.origin.y+S.t*S.t*30;if(S.t>(S.nextBurst||0)){S.nextBurst=S.t+.19;r30FX(b,b.x+Math.sin(S.t*17)*75,b.y+Math.cos(S.t*11)*65,125);r30Sound('expBig');shake=Math.max(shake,7);}
  if(S.t>2.8){S.mode=S.form<2?'silence':'escape';S.t=0;S.nextBurst=0;S.shipX=player.x;S.shipY=player.y;r30Clear(b);S.history.push({event:S.mode});}return;
 }
 if(S.mode==='silence'){
  if(S.t>1.8){S.mode='reform';S.t=0;S.history.push({event:'fragmentsRise'});r30Sound('combatAlien0927');}return;
 }
 if(S.mode==='reform'){
  b.x=worldWidth()/2;b.y=165;if(S.t>3.4){r30Form(b,S.form+1);S.mode='reveal';S.t=0;bossPhaseMusic(8,S.form+1);r30Sound('bossPhase');}return;
 }
 if(S.mode==='reveal'){if(S.t>1.4){S.mode='fight';S.t=0;b.enter=false;}return;}
 if(S.mode==='escape'){
  const u=clamp((S.t-1.5)/3,0,1);for(const seat of seatList())withSeat(seat,()=>{player.x=lerp(S.shipX,worldWidth()/2,u);player.y=lerp(S.shipY,118,u);});
  if(S.t>5.8){S.mode='reunion';S.t=0;S.history.push({event:'sewerReunion'});run._realmReturned=true;r30Sound('teleportIn');Audio.startMusic('realm8');}return;
 }
 if(S.mode==='reunion'){
  player.x=worldWidth()/2;player.y=lerp(112,300,clamp(S.t/2,0,1));
  if(S.t>6.5&&!S.rewarded){S.rewarded=true;run._trueFinaleCleared=true;R30_BASE.die();for(const p of powerups)if(p.kind==='forgecombo'&&!p.dead){applyPowerup(p);p.dead=true;}
   whiteBlast=0;S.mode='done';S.history.push({event:'complete'});drawStageClear._init=false;drawStageClear._res=null;setState(GS.STAGECLEAR);}return;
 }
}
updateBoss=function(dt){if(boss?._r30)return r30Tick(boss,dt);return R30_BASE.update.apply(this,arguments);};
function r30DrawBoss(b){
 const S=b._r30,T=S.t;ctx.save();
 if(S.mode==='takeover'){
  const p=clamp(T/5.8,0,1);r30Blit('vile24_robot_gray',b.x,b.y,220,220,0,1-clamp((p-.52)/.25,0,1));
  if(p>.16)for(let i=0;i<8;i++){const u=clamp((p-.16)/.58,0,1),a=i*2.4;r30Blit('fx_4',b.x+Math.sin(a)*(1-u)*170,b.y+Math.cos(a)*(1-u)*160,45,55,a,.9);}
  if(p>.62){ctx.globalAlpha=clamp((p-.62)/.23,0,1);for(const v of r30Parts(b))r30Blit(v.key,v.x,v.y,v.w,v.h,v.rot);}
 }else if(['silence','escape','reunion','done'].includes(S.mode)){
  if(S.mode==='escape'&&T>0.7&&T<5.8){const f=T<1.2?12:T<1.8?13:T<4.5?14:15;r30Blit('fx_'+f,worldWidth()/2,120,260,330,0,1);}
 }else if(S.mode==='reform'){
  const u=clamp(T/3.4,0,1);for(let i=0;i<18;i++){const p=clamp((u-i*.018)*1.5,0,1),sx=worldWidth()*(i+.5)/18,sy=VH+70+(i%3)*70;r30Blit('fx_4',lerp(sx,b.x,p),lerp(sy,b.y,p),38,48,(i+u*4),1);}
  if(u>.60)r30Blit('fx_'+(u>.84?7:6),b.x,b.y,210,240,0,1);
 }else{
 const fall=S.mode==='fall'||S.mode==='finalFall',alpha=S.mode==='reveal'?clamp(T/.8,0,1):1;
  for(const v of r30Parts(b)){r30Blit(v.key,v.x,v.y,v.w,v.h,v.rot,alpha*v.alpha);
   if(v.p.flash>0||b.flash>0){const k=v.key.startsWith('vile')?v.key:'r30_'+v.key,im=xartTint(k,'#ffffff',1);if(im){ctx.save();ctx.globalAlpha=.7;ctx.translate(v.x,v.y);ctx.rotate(v.rot);ROT5.depth++;try{ctx.drawImage(im,-v.w/2,-v.h/2,v.w,v.h);}finally{ROT5.depth--;ctx.restore();}}}}
  const Q=r30Pose(b);if(Q.shape==='chopper')r30Blit('chopper_rotor',Q.x,Q.y,248,248,S.clock*14,alpha);
  if(S.shield>0){const q=r30ShieldBounds(b);r30Blit('walls_'+(S.shield/S.shieldMax>.5?3:4),q.x,q.y,q.w,q.h,0,S.shieldFlash>0?1:.80);}
 }
 const P=S.attack;if(S.mode==='fight'&&P){
  const warn=P.t<P.tell,progress=clamp(P.t/P.tell,0,1),u=P.t-P.tell;
  if(warn){if(P.type==='arms'){
    for(const side of [-1,1])for(let j=0;j<5;j++){
     const angle=side*j*.82/4,rootX=b.x+side*118,rootY=b.y-50;
     combatWarningDraw(b,{x:rootX-Math.sin(angle)*250*.40,y:rootY+Math.cos(angle)*250*.40,ex:rootX-Math.sin(angle)*250*.79,ey:rootY+Math.cos(angle)*250*.79,progress,width:68,fieldOnly:true});}
   }else if(['tentacles','ghost','knight','ball'].includes(P.type))groundTargetReticleDraw(P.tx,P.ty,72,progress,.9);
   else if(['datawall','binarywall','codeRain'].includes(P.type)){const cols=P.type==='codeRain'?6:5,gap=P.type==='codeRain'?S.seq%6:(S.seq*2+1)%5;for(let i=0;i<cols;i++)if(i!==gap)combatWarningDraw(b,{x:camLeftX()+(camRightX()-camLeftX())*(i+.5)/cols,y:85,ex:camLeftX()+(camRightX()-camLeftX())*(i+.5)/cols,ey:VH,progress,width:38,fieldOnly:true});}
   else for(const side of [-1,1])combatWarningDraw(b,{x:b.x+side*65,y:b.y+50,ex:P.tx,ey:P.ty,progress,width:35});}
  if(['ghost','knight'].includes(P.type)&&u>=0){const local=u%1.5;if(local<1.0)groundTargetReticleDraw(P.tx,P.ty,78,local,.85);}
  if(P.type==='tentacles'&&u>0&&u<1.1)r30Blit('fx_11',P.tx,P.ty-65,66,190,0,Math.min(1,u*5));
 }
 for(const f of S.fx){const frame=f.kind==='morph'?4+Math.min(3,Math.floor(f.t/.7*4)):Math.min(3,Math.floor(f.t/.7*4));
  if(f.kind==='wall'||f.kind==='shield')r30Blit('walls_'+(f.kind==='wall'?2:5),f.x,f.y,f.size,f.kind==='wall'?65:b.h,0,1-f.t/.7);
  else r30Blit('fx_'+frame,f.x,f.y,f.size,f.size,0,1-f.t/.7);}
 ctx.restore();
}
drawBossSprite=function(b){if(b?._r30)return r30DrawBoss(b);return R30_BASE.draw.apply(this,arguments);};
drawBoss=function(){if(boss?._r30)return r30DrawBoss(boss);return R30_BASE.drawBoss.apply(this,arguments);};
bossHealthVisible=function(b){return b?._r30?['fight','reveal'].includes(b._r30.mode)&&!b.dead:R30_BASE.health(b);};
bossShieldFrac=function(b){return b?._r30?b._r30.shield>0?b._r30.shield/b._r30.shieldMax:null:R30_BASE.shieldFrac(b);};
bossHealthFraction=function(b){if(!b?._r30)return R30_BASE.frac(b);const S=b._r30,layer=S.form===2?S.base:b.maxhp,bar=((Math.max(.000001,b.hp)-.000001)%layer)/layer;return S.mode==='reveal'?clamp(S.t/1.4,0,1):clamp(bar,0,1);};
bmbarFill=function(kind,stage){if(kind==='boss'&&boss?._r30?.form===2){const layer=clamp(Math.ceil(boss.hp/boss._r30.base),1,4),key=['bmbar_fill_red','bmbar_fill_cyan','bmbar_fill_grey','bmbar_fill_green'][layer-1];if(XART.rdy(key))return XART.get(key);}return R30_BASE.fill.apply(this,arguments);};
drawHealthBarV2=function(kind,frac,cx,cy,w,inWorld,lagKey){const r=R30_BASE.bar.apply(this,arguments);if(kind==='boss'&&boss?._r30?.form===2&&bossHealthVisible(boss)){
 ctx.save();if(inWorld)ctx.translate(camX,0);msgText('X'+clamp(Math.ceil(boss.hp/boss._r30.base),1,4),cx+w*.42,cy,9,'#ffffff',1,1,.08);ctx.restore();}return r;};
retinaBossTargets=function(b){if(!b?._r30)return R30_BASE.targets(b);if(!r30Live(b)||b._r30.ghostHidden)return [];
 if(b._r30.shield>0){const q=r30ShieldBounds(b);return [retinaDynamicPiece(b,'r30-shield','binary shield',()=>({...r30ShieldBounds(b),hp:b._r30.shield,dead:!r30Live(b)||b._r30.shield<=0}),dmg=>{b._lastPart={id:'shield'};hitBoss(dmg);},q.w*.8,q.h*.8)];}
 return r30Parts(b).map(v=>retinaDynamicPiece(b,'r30-'+v.p.id,'module',()=>{const live=r30Parts(b).find(q=>q.p.id===v.p.id);return {x:live?.x||v.x,y:live?.y||v.y,hp:live&&!v.p.destroyed?v.p.hp:0,dead:!r30Live(b)||!live||v.p.destroyed};},dmg=>{b._lastPart=b._r30.shield>0?{id:'shield'}:v.p;hitBoss(dmg);},v.w*.8,v.h*.8));};
drawCombatFinalProjectile=function(q,role){if(q._r30Shot){r30Blit('fx_'+q._r30Shot,q.x,q.y,q._r30Shot===8?20:34,q._r30Shot===8?34:34,q._r30Shot===8?Math.atan2(q.vy,q.vx)-Math.PI/2:q._r30Age*2);return true;}return R30_BASE.projectile.apply(this,arguments);};
drawEnemy=function(e){if(e._r30Wall){if(!e.dead){r30Blit('walls_'+(e.hp/e.maxhp>.5?0:1),e.x,e.y,e.w,e.h,0,1);if(e.flash>0){const im=xartTint('r30_walls_0','#fff',1);if(im){ctx.save();ctx.globalAlpha=.7;ctx.drawImage(im,e.x-e.w/2,e.y-e.h/2,e.w,e.h);ctx.restore();}}}return;}return R30_BASE.enemy.apply(this,arguments);};
hitEnemy=function(e,dmg){if(!e?._r30Wall)return R30_BASE.hitEnemy.apply(this,arguments);if(e.dead)return;e.hp-=Math.max(0,dmg);e.flash=.12;if(e.hp<=0){e.dead=true;r30FX(e._r30Owner,e.x,e.y,e.w,'wall');r30Sound('expSmall');}return true;};
drawBG=function(dt){const S=boss?._r30;if(run.stage===8&&S?.mode==='reunion'){
 ENC30_BASE.connector(7,0,worldWidth());const im=XART.get('enc30_entry');if(im){ctx.drawImage(im,0,Math.max(0,im.height-VH),im.width,VH,0,viewFillY(),worldWidth(),viewFillH());}return;}
 return R30_BASE.bg.apply(this,arguments);};
drawPlayer=function(){const S=boss?._r30;if(S?.mode==='escape'&&S.t>4.4)return;R30_BASE.player.apply(this,arguments);
 if(S?.mode==='reunion'){const others=PILOTS.filter(p=>p.key!==run.pilot).slice(0,4);for(let i=0;i<others.length;i++){const k='ship_'+others[i].key;XART.rdy(k);r30Blit(k,worldWidth()/2+[-130,-66,66,130][i],330+(i%2)*36,36,58,0,1);}
  if(S.t<2)r30Blit('fx_'+(S.t<1?14:15),worldWidth()/2,112,200,245,0,1);}
};
// Keep the radio on the same screen-space panel as the existing flight dialogue.
const R30_WORLD=drawWorld;
drawWorld=function(dt){const r=R30_WORLD.apply(this,arguments),S=boss?._r30;if(!S)return r;
 let who=null,line=null;
 if(S.mode==='silence'){who=run.pilot;line='That is one shell down. Wait... those fragments are moving.';}
 if(S.mode==='escape'){who=run.pilot;line='The code is collapsing! That portal is my way home.';}
 if(S.mode==='reunion'){who=run.pilot==='decker'?'cole':'decker';line='We have your signal! Fury flight is right here. Welcome back.';}
 if(line)dlgBox({who:who.toUpperCase(),portrait:who,full:line,shown:line.slice(0,Math.floor(S.t*48)),forceShown:true,fade:clamp(S.t*3,0,1),pw:VW*.92,ph:100,x:VW*.04,y:VH*.13,screenSpace:true});
 return r;
};
