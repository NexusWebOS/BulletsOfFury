'use strict';
/* Alien rigs share their campaign donor's live controller. No second boss is
   spawned: proxies own only attack state, never rewards, exits or health bars. */
const GD4_BASE={tick:r30Tick,pose:r30Pose,draw:r30DrawBoss,clear:j3Clear,mount:shipBossMount,
 erOwns:er26Owns,canFire:mr27CanFire,furnaceMuzzle:furnaceMuzzle,ovMount:ovMount,
 ovFacing:ovFacingMount,ovMG:ovTwinMG,ovRocket:ovRocketSide,ovSonicMissiles:ovSonicMissileVolley,ovRotor:ovRotorTempest,
 attack:r30Attack,attackTick:r30AttackTick,knightAngles:fmcKnightAngles,rig:fmcRig,
 s7Owns:s7mOwns,s7Muzzle:s7mMuzzle,carrierMuzzle:s67WhvMuzzle,aceGuns:whvAceGuns,aceMissiles:whvAceFireMissiles};
const GD4_KIND={1:'damkeeper',2:'infernoreaver',3:'cryospear',4:'stormsovereign',5:'hammer',6:'warhive',7:'sludgeemperor'};
er26Owns=function(b){return b?._gp4Host?['cryospear','stormsovereign'].includes(b._ship):GD4_BASE.erOwns(b);};
s7mOwns=function(b){return b?._gp4Host?b._ship==='sludgeemperor':GD4_BASE.s7Owns(b);};
function gd4Parts(p){return fmcRig(p._gp4Host).filter(v=>v.spec.tags?.length||v.spec.role==='claw');}
function gd4Port(p,side,id){const exact=id&&fmcRig(p._gp4Host).find(v=>v.p.id===id);if(exact)return fmcPoint(exact,...(exact.spec.emit||[.5,.85]));
 const list=gd4Parts(p),a=list.filter(v=>Math.sign(v.spec.x)===(side<0?-1:1));
 const v=a[0]||list[0];if(!v)return{x:p.x,y:p.y+65};return fmcPoint(v,...(v.spec.emit||[.5,.85]));}
shipBossMount=function(b,slot){if(!b?._gp4Host)return GD4_BASE.mount.apply(this,arguments);
 const text=String(slot),side=text.includes('L')?-1:1,suffix=side<0?'L':'R';
 const id=text==='LIGHTNING'?'lightning':text.startsWith('ROCKET')?'rack'+suffix:b._ship==='cryospear'?'gun'+suffix+(text.endsWith('1')?'2':'1'):null;
 return gd4Port(b,side,id);};
mr27CanFire=function(b,slot){if(!b?._gp4Host)return GD4_BASE.canFire.apply(this,arguments);
 if(slot==='LIGHTNING')return fmcAlive(b._gp4Host,'lightning');
 if(typeof slot!=='string'||['C','CORE','CL','CR'].includes(slot))return true;
 const side=slot.includes('L')?-1:1,suffix=side<0?'L':'R';
 const id=slot.startsWith('ROCKET')?'rack'+suffix:b._ship==='cryospear'?'gun'+suffix+(slot.endsWith('1')?'2':'1'):null;
 if(id)return fmcAlive(b._gp4Host,id);return gd4Parts(b).some(v=>Math.sign(v.spec.x)===side);};
furnaceMuzzle=function(b,side){if(!b?._gp4Host)return GD4_BASE.furnaceMuzzle.apply(this,arguments);
 const p=gd4Port(b,side==='left'?-1:1);return{...p,a:b._fz.a+b._fz.arm[side].a};};
ovMount=function(b,x,y){if(!b?._gp4Host)return GD4_BASE.ovMount.apply(this,arguments);const p=gd4Port(b,x<0?-1:1);return[p.x,p.y];};
ovFacingMount=function(b,x,y){if(!b?._gp4Host)return GD4_BASE.ovFacing.apply(this,arguments);
 return x===0?{x:b.x,y:b.y+60}:gd4Port(b,x<0?-1:1,Math.abs(x)>20?'rack'+(x<0?'L':'R'):x<0?'left':'right');};
// The campaign controller still owns attack selection, timing and warning lanes.
// Its hull guns now terminate at the alien's actual, independently breakable mounts.
ovTwinMG=function(b,sweep){if(!b?._gp4Host)return GD4_BASE.ovMG.apply(this,arguments);
 for(const side of [-1,1]){if(!fmcAlive(b._gp4Host,side<0?'left':'right'))continue;
  const p=ovFacingMount(b,side*10,54),aim=sweep?Math.PI/2+(b._pivot||0):aimPlayer(p.x,p.y);
  const a=sweep?ovSweepGunAim(b,p.x,p.y,aim+side*.05):eAimDown(aim+side*.05);
  eBullets.push({x:p.x,y:p.y,vx:Math.cos(a)*4.2*DIFF.ebSpeed,vy:Math.sin(a)*4.2*DIFF.ebSpeed,w:5,h:12,kind:'mg',_ph:(Math.random()*4)|0});
  navalFlash(null,p,.74,S1_MUZZLE_ROTARY,{n:6,hpx:35,life:.12,follow:()=>ovFacingMount(b,side*10,54)});
 }stageRevisionCue(b,'overlordGun',.085);};
ovRocketSide=function(b,side,fan){if(b?._gp4Host&&(b.dead||!fmcAlive(b._gp4Host,'rack'+(side<0?'L':'R'))))return;
 return GD4_BASE.ovRocket.apply(this,arguments);};
ovSonicMissileVolley=function(b,index){if(!b?._gp4Host)return GD4_BASE.ovSonicMissiles.apply(this,arguments);
 if(b.dead||diffKey!=='furious')return;for(const side of [-1,1])if(fmcAlive(b._gp4Host,'rack'+(side<0?'L':'R')))for(const spread of [-.12,.12]){
  const m=ovFacingMount(b,side<0?-48:46,41),a=Math.PI/2+(b._pivot||0)+side*.18+spread;
  eBullets.push({kind:'s1jungleMissile',_ovSonicMissile:true,_shootable:true,_volley:index,x:m.x,y:m.y,vx:Math.cos(a)*2.3,vy:Math.sin(a)*2.3,ang:a,w:14,h:26,t:0,hp:1,homing:true,turn:.028,spd:2.3,_accel:.045,_maxspd:4.8});
  navalFlash(null,m,.9,S1_MUZZLE_MILITARY,{n:6,hpx:42,life:.2,follow:()=>ovFacingMount(b,side<0?-48:46,41)});
 }stageRevisionCue(b,'overlordRocket',.1);weaponFeedbackSound('colePressureRelease',.45);};
ovRotorTempest=function(b){if(b?._gp4Host&&!fmcAlive(b._gp4Host,'rotor'))return;return GD4_BASE.ovRotor.apply(this,arguments);};
s7mMuzzle=function(b,id){if(!b?._gp4Host)return GD4_BASE.s7Muzzle.apply(this,arguments);return{...(id==='emitter'?{x:b.x,y:b.y+55}:gd4Port(b,id.endsWith('L')?-1:1,id)),a:b._s7mod.aim||Math.PI/2};};
s67WhvMuzzle=function(b,side){if(!b?._gp4Host)return GD4_BASE.carrierMuzzle.apply(this,arguments);
 const beam=fmcRig(b._gp4Host).find(v=>v.p.id==='beam');return beam&&(b._whv.beam||b._whv.beam2)?fmcPoint(beam,.5,.87):gd4Port(b,side==='L'?-1:1);};
whvAceGuns=function(b,A,spread){if(!b?._gp4Host)return GD4_BASE.aceGuns.apply(this,arguments);
 for(const side of [-1,1])if(mr27CanFire(b,side<0?'L':'R')){const p=gd4Port(b,side);eShoot(p.x,p.y,Math.PI/2+(spread||0)*side,6.2,'mg');}whvSfx('enemyShoot',.6);};
whvAceFireMissiles=function(b,n){if(!b?._gp4Host)return GD4_BASE.aceMissiles.apply(this,arguments);
 for(let i=0;i<n;i++){const side=i%2?1:-1;enemyLockOn(b,1+i*.24,{fire:()=>{if(b.dead||!fmcAlive(b._gp4Host,side<0?'rackL':'rackR'))return;
  const p=gd4Port(b,side),a=Math.PI/2+side*.35;eShootT(p.x,p.y,a,3.1,'emissile',{w:11,h:18,hp:1,_shootable:true,spd:3.1,ang:a,_accel:.03,_maxspd:5.2,_bright:true});whvSfx('missile',.8);}});}
};
function gd4Create(b,i){const J=j3State(b);J.gp4Donors??=[];if(J.gp4Donors[i])return J.gp4Donors[i];
 const p={_gp4Host:b,kind:GD4_KIND[i],x:b.x,y:b.y,ty:b.y,w:b.w,h:b.h,hp:b.hp,maxhp:b.maxhp,t:0,flash:0,enter:false,dead:false,fireCd:.5,_noHit:false};
 const D={p,i,age:0,cycle:0,alien:4.8,history:[],last:null};J.gp4Donors[i]=D;
 if(i===2){shipBossInit(p,'infernoreaver');furnaceSync(p);furnaceEnter(p,'arms');p._fz.trans=0;p._fz.pt=10;}
 if(i===3||i===4){shipBossInit(p,GD4_KIND[i]);delete p._scene;er26Init(p);p._er26.engaged=true;p._er26.home=220;p._er26.to.y=220;
  if(p._s4war){p._s4war.shield.active=false;p._s4war.shield.rearming=false;for(const n of p._s4war.shield.nodes)n.dead=true;p._s4war.drones=[];p._s4war.coreTurrets=[];}delete p._mr27;}
 if(i===5){hammerBossInit(p);p.kind='alienKnight';p._hammer.balance0922=true;p._hammer.ballSeen=true;p._hammer.whirlSeen=true;
  p._hammer.gp4FailsafeSeen=true;p._hammer.mode='hammer';p._hammer.comboPending=true;p._hammer.rage=999;hammerTarget(p);hammerState(p,'warn');}
 if(i===6){warhiveInit(p);Object.assign(p._whv,{cx:b.x,cy:b.y,dy:0,st:'hold',doorOpen:true});
  p._whv.ace={x:b.x,y:b.y,vx:0,vy:0,t:0,st:'fight',roll:null,somer:null,dash:null,rollCd:1.2,somerCd:3,gunCd:.7,mslCd:3,dashCd:5,rng:{ox:0,oy:0,t:0},orb:null,desp:null,inverted:false,invSomerCd:4,pvx:0,ppx:player.x,trail:[]};}
 if(i===7){shipBossInit(p,'sludgeemperor');s7mInit(p);p._s7mod.shield=0;s7mSet(p,'recover');}
 p.x=b.x;p.y=b.y;p.enter=false;p._noHit=false;p.hp=b.hp;p.maxhp=b.maxhp;
 return D;
}
function gd4State(D){const p=D.p;return p._er26?.mode||p._fz?.attack||p._hammer?.state||(p._whv&&(p._whv.can.last||p._whv.ace.st))||p._s7mod?.mode||p._ovState;}
function gd4Tick(b,dt){const J=j3State(b),S=b._r30,D=gd4Create(b,J.mimic),p=D.p;D.age+=dt;p.t+=dt;p.hp=b.hp;p.maxhp=b.maxhp;p.dead=false;p.flash=0;
 // Source damage stages escalate without importing the source's ending/cutscene.
 if(D.i===1)updateOverlordX(p,dt);
 else if(D.i===2){const F=p._fz;F.t+=dt;F.pt+=dt;F.at+=dt;F.beams=[];F.tells=[];F.eyeMuzzles=[];F.fx=F.fx.filter(q=>(q.life-=dt)>0);
  for(const side of ['left','right'])if(!fmcAlive(b,side))F.pools[side]=0;
  const phase=b.hp/b.maxhp<.30?'head':b.hp/b.maxhp<.64?'core':'arms';if(F.phase!==phase){furnaceEnter(p,phase);F.trans=0;}
  furnaceCombat(p,dt);for(const q of F.beams)for(const seat of seatList())withSeat(seat,()=>{const dx=q.ex-q.x,dy=q.ey-q.y,u=clamp(((player.x-q.x)*dx+(player.y-q.y)*dy)/(dx*dx+dy*dy||1),0,1);if(Math.hypot(player.x-q.x-dx*u,player.y-q.y-dy*u)<q.width/2+5)playerHit('alien furnace beam');});
 }else if(D.i===3||D.i===4)er26Tick(p,dt);
 else if(D.i===5){FR27_BASE.hammerTick(p,dt);p._hammer.phasePending=false;}
 else if(D.i===6){const W=p._whv;for(const side of ['L','R'])W.parts[side].dead=!fmcAlive(b,'fan'+side);
  if(W.beam||W.beam2){W.ace.vx=W.ace.vy=0;W.ace.t+=dt;}else whvAceTick(p,dt);
  W.cx=p.x;W.cy=p.y;whvCannonTick(p,dt);if(!fmcAlive(b,'beam'))W.beam=W.beam2=null;whvBeamTick(p,dt);whvShotsTick(p,dt);
 }else if(D.i===7){const M=p._s7mod,map={frontL:'left',frontR:'right',rearL:'legL',rearR:'legR',gunL:'gunL',gunR:'gunR'};
  for(const part of M.parts)part.hp=fmcAlive(b,map[part.id])?part.max:0;M.shield=0;s7mTick(p,dt);
 }
 b.x=p.x;b.y=p.y;b._drawY=b.y;
 if(D.i===5){const live=['leap','recover'].includes(p._hammer.state),L=fmcBlade(b);
  if(live&&L){const prev=D.blade||L;for(const seat of seatList())withSeat(seat,()=>{
   for(let k=0;k<=5;k++){const u=k/5,line={x:lerp(prev.x,L.x,u),y:lerp(prev.y,L.y,u),ex:lerp(prev.ex,L.ex,u),ey:lerp(prev.ey,L.ey,u)};
    if(s81003Distance(player.x,player.y,line)<L.width*.5+3){playerHit('alien powered sword');break;}}
  });D.blade=L;}else D.blade=null;
 }
 // Campaign movement limits were tuned to different silhouettes. Use the alien
 // rig's actual extents, except deliberate offscreen helicopter charge passes.
 if(D.i!==1){const rig=fmcRig(b).filter(v=>!(D.i===5&&p._hammer.throw&&v.p.id==='sword')),left=Math.min(...rig.map(v=>v.x-v.w*.5)),right=Math.max(...rig.map(v=>v.x+v.w*.5));
  const dx=left<camLeftX()+8?camLeftX()+8-left:right>camRightX()-8?camRightX()-8-right:0;
  b.x+=dx;p.x=b.x;if(p._whv?.ace)p._whv.ace.x=b.x;}
 const mode=gd4State(D);if(mode!==D.last){D.last=mode;D.history.push(mode);if(D.history.length>60)D.history.shift();}
 // One alien flank cast sits between source bursts, with the original warning.
 D.alien-=dt;if(D.alien<1.0&&D.alien>0)combatWarningTick(b,'alien-donor-flank',1-D.alien,1);
 if(D.alien<=0){D.alien=6.5;const gap=Math.atan2(player.y-b.y,player.x-b.x);
  for(let i=0;i<12;i++){const a=TAU*i/12;if(Math.abs(Math.atan2(Math.sin(a-gap),Math.cos(a-gap)))>.42)f1003bShot(b,b.x,b.y+60,a,2.5,'code');}r30Sound('combatAlien0927');}
 if(D.age>=32){D.age=0;j3Morph(b,'home');}
}
r30Tick=function(b,dt){const J=j3State(b),S=b?._r30;
 if(J?.encounter===2&&J.mimic>0&&S.mode==='fight'){
  dt=Math.min(.05,dt);j3Timers(b,dt);b.enter=false;gd4Tick(b,dt);j3Save(b);return;
 }return GD4_BASE.tick.apply(this,arguments);
};
j3Clear=function(b){const J=j3State(b),D=J?.gp4Donors?.[J.mimic];if(D){D.p.dead=true;D.blade=null;groundTargetingCancel(D.p);playerLocks=playerLocks.filter(q=>q.src!==D.p);D.p._l23Beam=null;if(D.p._fz){D.p._fz.beams=[];D.p._fz.tells=[];}}return GD4_BASE.clear.apply(this,arguments);};
r30Pose=function(b){const J=j3State(b),D=J?.gp4Donors?.[J.mimic];if(J?.mimic>0&&D&&b._r30.mode==='fight')return{x:b.x,y:b.y-(D.p._s7mod?.height||0),angle:0,alpha:1,scale:1,shape:f1003bDef(b).id};return GD4_BASE.pose.apply(this,arguments);};
fmcRig=function(b){const rig=GD4_BASE.rig(b),J=j3State(b),M=J?.mimic===7&&J.gp4Donors?.[7]?.p._s7mod,F=J?.mimic===2&&J.gp4Donors?.[2]?.p._fz;
 if(F)for(const v of rig){const dx=v.ax-b.x,dy=v.ay-b.y,c=Math.cos(F.a),s=Math.sin(F.a);v.ax=b.x+dx*c-dy*s;v.ay=b.y+dx*s+dy*c;v.rot+=F.a+(F.arm[v.p.id]?.a||0);const mid=fmcPoint(v,.5,.5);v.x=mid.x;v.y=mid.y;}
 if(M?.mode?.startsWith('swipe'))for(const v of rig)if(v.spec.role==='claw'){
  const side=v.p.id==='left'?-1:1;if(M.mode==='swipeX'||M.mode===(side<0?'swipeL':'swipeR'))v.rot+=side*Math.sin(clamp((M.t-M.warn)/.38,0,1)*Math.PI)*1.2;
  const mid=fmcPoint(v,.5,.5);v.x=mid.x;v.y=mid.y;
 }return rig;};
fmcKnightAngles=function(K){const b=boss,J=j3State(b),h=J?.gp4Donors?.[5]?.p?._hammer;
 if(J?.mimic!==5||!h)return GD4_BASE.knightAngles(K);const live=['leap','recover'].includes(h.state),u=clamp(h.t/.4,0,1);
 return{arm:live?lerp(-1.2,1.25,u):-.45,wrist:live?lerp(-.5,.6,u):-.2,shield:live?.25:-.25};};
r30DrawBoss=function(b){GD4_BASE.draw.apply(this,arguments);const J=j3State(b),D=J?.gp4Donors?.[J.mimic];if(!D||b._r30.mode!=='fight')return;const p=D.p;
 if(p._er26){er26Draw(p);shipBossMuzzleDraw(p);}
 if(p._fz){for(const q of p._fz.tells)fztTellDraw(q,p);for(const q of p._fz.beams)fztBeamDraw(q);}
 if(D.i===1){ovSweepSafeDraw(p);ovRushWarningDraw(p,false);ovSonicWarningDraw(p);}
 if(D.i===6)whvDrawShots(p);
 if(D.i===7&&p._s7mod.t<p._s7mod.warn){const M=p._s7mod;combatWarningDraw(p,{x:b.x,y:b.y+55,ex:M.target.x,ey:M.target.y,width:M.mode.startsWith('swipe')?180:65,progress:M.t/M.warn});}
 if(D.i===5){const h=p._hammer;if(['warn','chain_warn'].includes(h.state))combatWarningDraw(p,{x:p.x,y:p.y,ex:h.tx||p.x,ey:h.ty||p.y,width:70,progress:clamp(h.t/.58,0,1)});
  if(h.leapFx)efxFrame('efx_burst_fire',Math.min(7,Math.floor(h.leapFx/.56*8)),h.leapFxX-55,h.leapFxY-55,110,110,.8);
  const blade=fmcRig(b).find(v=>v.p.id==='sword');if(blade){const tip=fmcPoint(blade,.5,.9);av3Muzzle(ctx,tip.x,tip.y,42,3,b.t);}}
};

// The Dracula body now gets three substantial beats between borrowed forms:
// independent swipes, tentacle pursuit, then a flanking orb volley.
r30Attack=function(b){const J=j3State(b),S=b?._r30;
 if(J?.encounter===2&&J.mimic==null&&J.attacks===2){J.attacks++;S.seq++;S.attack={type:'gp4Throne',t:0,tell:1.15,active:3.4,next:0,tx:player.x,ty:player.y};r30Sound('bossWeaponCharge');return;}
 return GD4_BASE.attack.apply(this,arguments);
};
r30AttackTick=function(b,dt){const P=b?._r30?.attack;if(P?.type!=='gp4Throne')return GD4_BASE.attackTick.apply(this,arguments);
 P.t+=dt;combatWarningTick(b,'dracula-orb-court',Math.min(P.t,P.tell),P.tell);const u=P.t-P.tell;if(u<0)return;
 if(u>=P.next){P.next=u+.55;for(const side of [-1,1]){const x=b.x+side*120,y=b.y+45;const a=Math.atan2(P.ty-y,P.tx-x);for(const off of [-.19,0,.19])f1003bShot(b,x,y,a+off,3.2,'code',true);}r30Sound('combatAlien0927');}
 if(u>=P.active){b._r30.attack=null;b._r30.cd=.65;}
};
