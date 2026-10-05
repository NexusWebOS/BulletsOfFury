'use strict';
/* October 4 follow-up: five-ship routes, direct rift handoff, articulated final combat. */
const CF4={mapT:0,focus:false,mouse:false,previous:7,flight:0,portal:false,events:[]};
const CF4_BASE={leave:scLeaveStage,begin:beginStage,update:updatePlay,pose:r30Pose,parts:r30Parts,
 tick:r30Tick,draw:r30DrawBoss,rig:fmcRig,angles:fmcKnightAngles,charge:fmcCharge,exit:fr27Exit,
 donor:gd4Tick,head:hammerHeadPoint,grip:hammerGripPoint,throwHit:hammerBoomerangHit,
 save:Rival24.save,load:Rival24.load,map:Rival24.mapDraw,input:Rival24.mapInput,back:Rival24.mapBack};

function cf4PortalHandoff(result){
 if(CF4.portal)return;CF4.portal=true;
 // Keep earned score, rank, achievements and Furious currency without opening a results screen.
 if(!result){computeStageResults();result=drawStageClear._res;}
 run.score+=(result.bonus||0);run.lives=clamp(run.lives,0,9);
 if(result.seats){run2.score+=result.seats[1].bonus||0;run2.lives=clamp(run2.lives,0,9);}
 if(run.mode==='campaign'){campaign.unlockedMax=Math.max(campaign.unlockedMax||1,8);campaign._l78Pending=1;campAutoAfterClear(7,8,result.rank);}
 drawStageClear._init=false;drawStageClear._res=null;
 run._l78Entry=1;storySkip();BOFCinematicDirector.cancel();Audio.stopMusic();
 beginStage(8);run._l78Entry=1;l78EntryStart();setState(GS.WARPENTRY);CF4.portal=false;
}
function cf4Pending(){return run.mode==='campaign'&&campaign.stageX1004?.route&&!campaign.stageX1004.done;}
// The October 1 portal owns the live exit; earlier Stage-7 wrappers are fallback paths.
fr27Exit=function(b,dt){const result=CF4_BASE.exit.apply(this,arguments);
 if(run.stage===7&&b._s7warden?.final?.finished&&state===GS.STAGECLEAR)cf4PortalHandoff();return result;};
function cf4Hub(){return fr27CoreMapPosition();}
function cf4LaunchX(){const X=campaign.stageX1004;if(!X||X.done)return false;
 const returnStage=clamp(campaign.unlockedMax||7,7,8);GP4.route=X.route;GP4.stage6Only=false;CF4.focus=false;CF4.mouse=false;
 beginStage(6);run._cf4Return=returnStage;setState(GS.PLAY);BOFCinematicDirector.cancel();storySkip();gp4QuickEncounter();Input.clearTaps?.();return true;
}
scLeaveStage=function(R){
 if(run.stage===7)return cf4PortalHandoff(R);
 if(run.stage!==6)return CF4_BASE.leave.apply(this,arguments);
 if(run._gp4StageX){const dest=run._cf4Return||7;
  if(campaign.stageX1004?.route===run._gp4StageX)campaign.stageX1004.done=true;
  run.score+=(R.bonus||0);run.mode='campaign';delete run._gp4StageX;delete run._cf4Return;
  drawStageClear._init=false;drawStageClear._res=null;Audio.stopMusic();campSuspend();openStageSelect(dest,{});return;
 }
 const route=s6Wing?.route;
 if(route){campaign.stageX1004={route:route==='left'?'right':'left',done:false};campaign.rivalScattered=false;CF4.flight=0;}
 const result=CF4_BASE.leave.apply(this,arguments);
 // Retire the old five isolated duels for this new pending full encounter.
 if(route){campaign.rivalScattered=false;campAutoAfterClear(6,7,R.rank);campSuspend();}return result;
};
Rival24.save=function(){return{...CF4_BASE.save(),stageX1004:campaign.stageX1004?{...campaign.stageX1004}:null};};
Rival24.load=function(s){CF4_BASE.load(s);campaign.stageX1004=s?.stageX1004&&['left','right'].includes(s.stageX1004.route)?{...s.stageX1004}:null;CF4.focus=false;CF4.flight=3.3;};
const cf4Available=Object.getOwnPropertyDescriptor(Rival24,'mapAvailable').get;
const cf4Focused=Object.getOwnPropertyDescriptor(Rival24,'mapFocused').get;
const cf4Flying=Object.getOwnPropertyDescriptor(Rival24,'flying').get;
Object.defineProperties(Rival24,{
 mapAvailable:{get(){return !!cf4Pending()||cf4Available.call(Rival24);}},
 mapFocused:{get(){return CF4.focus||cf4Focused.call(Rival24);}},
 flying:{get(){return !!cf4Pending()&&CF4.flight<3.2||cf4Flying.call(Rival24);}}
});
Rival24.mapDraw=function(dt){if(!cf4Pending())return CF4_BASE.map(dt);if(sselBoot>0)return;
 CF4.mapT+=dt||0;CF4.flight+=dt||0;const h=cf4Hub(),o=sselFlagScreenXY(6);if(!h)return;
 const harrier=campaign.stageX1004.route==='left',keys=harrier?['gp4_ace_top']:REBEL_SHIPS.map(k=>'rr_ship_'+k);
 keys.forEach((key,i)=>{if(!XART.rdy(key))return;const im=XART.get(key),a=CF4.mapT*.65+i*TAU/keys.length,
  u=clamp((CF4.flight-i*.14)/2.7,0,1),e=u*u*(3-2*u),tx=h.x+Math.cos(a)*85,ty=h.y+Math.sin(a)*38,
  x=lerp(o?.x||h.x,tx,e),y=lerp(o?.y||h.y,ty,e)-Math.sin(u*Math.PI)*65,z=harrier?50:30;
  ctx.save();ctx.translate(x,y);ctx.rotate(u<.98?Math.atan2(ty-(o?.y||h.y),tx-(o?.x||h.x))-Math.PI/2:a);ctx.imageSmoothingEnabled=false;ctx.drawImage(im,-z*im.width/im.height/2,-z/2,z*im.width/im.height,z);ctx.restore();});
 if(typeof map4eStageXMarker!=='function'&&XART.rdy('fr27_stagex_card')){const im=XART.get('fr27_stagex_card'),w=CF4.focus?115:100;ctx.drawImage(im,h.x-w/2,h.y-w*im.height/im.width/2,w,w*im.height/im.width);}
 if(CF4.focus)mapgBriefingDraw({key:'cf4-x-'+harrier,title:'STAGE X - '+(harrier?'HARRIER PURSUIT':'REBEL FURY'),body:harrier?'THE ESCAPED HARRIER IS HOLDING OVER THE CENTRAL CITY. FINISH THE PURSUIT.':'FIVE REBEL PILOTS. YOUR FULL FIVE-SHIP WING. FINISH THE FIGHT.'});
 if(CF4.flight<3.2)campText((harrier?'HARRIER':'REBEL FURY')+' MOVING TO STAGE X',VW/2,VH-212,10,'#ffb4a3');
 else controlHintRow(CF4.focus?[['pad_a','FIGHT'],['pad_b','MAP']]:[['pad_dpad','STAGE X']],VH-212,VW/2,VW-24,20);
};
Rival24.mapInput=function(){if(!cf4Pending())return CF4_BASE.input();if(CF4.flight<3.2)return true;
 const h=cf4Hub(),m=Input.mouse||{},hit=typeof map4eStageXAt==='function'?map4eStageXAt(m.x,m.y):h&&Math.abs(m.x-h.x)<105&&Math.abs(m.y-h.y)<60;
 if(m.down&&!CF4.mouse&&hit){CF4.mouse=true;if(CF4.focus)cf4LaunchX();else{CF4.previous=sselCursor;CF4.focus=true;}return true;}CF4.mouse=!!m.down;
 if(!CF4.focus){if(Input.menuDown()){CF4.previous=sselCursor;CF4.focus=true;Audio.SFX.blip();return true;}return false;}
 if(Input.menuUp()||Input.menuBack()){CF4.focus=false;sselCursor=CF4.previous;Audio.SFX.blip();return true;}
 if(Input.menuConfirm())cf4LaunchX();return true;
};
Rival24.mapBack=function(){if(CF4.focus&&Input.menuBack()){CF4.focus=false;sselCursor=CF4.previous;return true;}return CF4_BASE.back();};

// Generated poses are separate torso and leg plates. Head, arms and weapons stay articulated.
for(const part of ['core','legL','legR'])for(let f=0;f<4;f++){
 const name=part+'_'+f,key='cf4_'+name;XART._src[key]='assets/game/campaign_focus_1004b/'+name+'.png';
 FMC_ART[key]={key,path:XART._src[key],rects:{}};XART.rdy(key);
}
function cf4Knight(b){const J=j3State(b);return J?.mimic===5?J.gp4Donors?.[5]?.p._hammer:null;}
r30Pose=function(b){const Q=CF4_BASE.pose(b),h=cf4Knight(b);if(!h)return Q;
 const s=h.state;Q.scale=s==='giant_rise'?lerp(1,.30,clamp(h.t,0,1)):s==='giant_warn'?.30:
  s==='giant_dive'?lerp(.30,1.35,clamp(h.t/.52,0,1)):s==='giant_sweep'?1.35:
  s==='giant_recover'?lerp(1.35,1,clamp(h.t/.8,0,1)):s==='curl'?lerp(1,.45,clamp(h.t/HAMMER_BALL_WARN,0,1)):
  s==='ball'?.45:s==='uncurl'?lerp(.45,1,clamp(h.t/1.25,0,1)):1;return Q;
};
function cf4KnightFrame(h){return ['warn','storm_warn','giant_windup','giant_warn','curl'].includes(h.state)?0:
 ['leap','back','storm_slam','giant_rise','giant_dive','ball','whirlwind'].includes(h.state)?1:
 ['recover','storm_split','giant_sweep'].includes(h.state)&&h.t<.18?2:3;}
// Normalized joint centers measured on the imported pixels (not the sheet cells).
const CF4_JOINTS=[
 {neck:[.544,.112],shoulders:[[.081,.286],[.927,.355]],hips:[[.097,.833],[.762,.833]],legs:[[.69,.13],[.281,.131]]},
 {neck:[.5,.06],shoulders:[[.085,.233],[.919,.233]],hips:[[.188,.855],[.816,.855]],legs:[[.44,.10],[.514,.065]]},
 {neck:[.498,.104],shoulders:[[.059,.296],[.934,.30]],hips:[[.188,.827],[.823,.827]],legs:[[.35,.104],[.641,.106]]},
 {neck:[.498,.066],shoulders:[[.068,.25],[.928,.25]],hips:[[.115,.83],[.894,.83]],legs:[[.36,.096],[.667,.073]]}
];
fmcRig=function(b){const rig=CF4_BASE.rig(b),h=cf4Knight(b);if(!h)return rig;const frame=cf4KnightFrame(h);
 for(const v of rig){if(!['core','legL','legR'].includes(v.p.id))continue;const sheet='cf4_'+v.p.id+'_'+frame,im=XART.get(sheet);if(!im)continue;
  FMC_ART[sheet].rects.pose=[0,0,im.width,im.height];v.spec={...v.spec,sheet,art:'pose'};v.key=sheet;
  // Knees fold without moving their hip sockets; one pose drives art and hit geometry.
  const scale=r30Pose(b).scale||1;
  if(v.p.id!=='core'){v.h=(frame===0?78:frame===1?76:frame===2?88:101)*scale;v.rot=frame===1?Math.sign(v.spec.x)*.16:0;}
  else if(frame===0||frame===2)v.h=124*scale;
  const mid=fmcPoint(v,.5,.5);v.x=mid.x;v.y=mid.y;
 }
 const joints=CF4_JOINTS[frame],core=rig.find(v=>v.p.id==='core'),scale=r30Pose(b).scale||1;
 if(core&&core.spec.sheet?.startsWith('cf4_')){
  core.spec={...core.spec,px:joints.neck[0],py:joints.neck[1]};core.ax=b.x;core.ay=b.y-55*scale;Object.assign(core,fmcPoint(core,.5,.5));
  for(const [i,id]of ['legL','legR'].entries()){const v=rig.find(v=>v.p.id===id);if(!v)continue;
   const im=XART.get(v.key);v.spec={...v.spec,px:joints.legs[i][0],py:joints.legs[i][1]};if(im)v.w=v.h*im.width/im.height;
   const q=fmcPoint(core,...joints.hips[i]);v.ax=q.x;v.ay=q.y;Object.assign(v,fmcPoint(v,.5,.5));}
  for(const [i,id]of ['swordArm','shieldArm'].entries()){const v=rig.find(v=>v.p.id===id);if(!v)continue;
   v.spec={...v.spec,px:i?.84:.20,py:.24};const q=fmcPoint(core,...joints.shoulders[i]);v.ax=q.x;v.ay=q.y;Object.assign(v,fmcPoint(v,.5,.5));
   const tool=rig.find(v=>v.p.id===(i?'shield':'sword'));if(tool){const hand=fmcPoint(v,i?.469:.493,i?.954:.936);tool.ax=hand.x;tool.ay=hand.y;Object.assign(tool,fmcPoint(tool,.5,.5));}}
 }
 const sword=rig.find(v=>v.p.id==='sword');
 if(sword&&h.throw){sword.spec={...sword.spec,px:.5,py:.5};sword.ax=h.throw.x;sword.ay=h.throw.y;sword.w=34;sword.h=100;sword.rot=h.throw.angle;sword.x=h.throw.x;sword.y=h.throw.y;}
 if(h.state==='ball')for(const v of rig){const x=v.ax-b.x,y=v.ay-b.y,c=Math.cos(h.angle),s=Math.sin(h.angle);v.ax=b.x+x*c-y*s;v.ay=b.y+x*s+y*c;v.rot+=h.angle;Object.assign(v,fmcPoint(v,.5,.5));}
 return rig;
};
fmcKnightAngles=function(K){const h=cf4Knight(boss);if(!h)return CF4_BASE.angles(K);
 const u=clamp(h.t/(hammerFurious()?.27:.52),0,1);
 if(['warn','storm_warn','giant_windup','giant_warn'].includes(h.state))return{arm:lerp(.25,2.5,clamp(h.t/.58,0,1)),wrist:-.55,shield:-.5};
 if(['leap','storm_slam','giant_dive'].includes(h.state))return{arm:lerp(2.5,-.45,u*u),wrist:lerp(-.55,-.8,u),shield:.15};
 if(['recover','storm_split','giant_sweep'].includes(h.state))return{arm:-.45,wrist:-.8,shield:.15};
 if(['spin','revenge_charge','whirlwind','whirl_warn','whirl_turn'].includes(h.state))return{arm:h.spinAngle||h.whirl?.reel||h.t*12,wrist:-.3,shield:-.7};
 if(h.state==='spell'||h.state.startsWith('storm'))return{arm:2.4,wrist:-.5,shield:-1.4};
 if(h.state.includes('chain'))return{arm:-.65,wrist:.5,shield:-.3};
 return{arm:.3,wrist:0,shield:-.25};
};
fmcCharge=function(b){const h=cf4Knight(b);if(!h)return CF4_BASE.charge(b);
 if(['warn','storm_warn','giant_warn','spell','mega_charge','spin','revenge_charge'].includes(h.state))return{frame:Math.min(5,Math.floor(h.t*9)),alpha:1};
 if(['leap','recover','storm_slam','storm_split','giant_dive','giant_sweep','spell_blast','chaingun','mega_beam','throw','whirlwind'].includes(h.state))return{frame:6,alpha:.85};return null;
};
hammerHeadPoint=function(p){if(p?._gp4Host&&p._hammer){if(p._hammer.throw)return{x:p._hammer.throw.x,y:p._hammer.throw.y};const v=fmcRig(p._gp4Host).find(v=>v.p.id==='sword');if(v)return fmcPoint(v,.5,.86);}return CF4_BASE.head(p);};
hammerGripPoint=function(p){if(p?._gp4Host&&p._hammer){const v=fmcRig(p._gp4Host).find(v=>v.p.id==='swordArm');if(v)return fmcPoint(v,.5,.89);}return CF4_BASE.grip(p);};
hammerBoomerangHit=function(T,dt){if(!T._cf4Host)return CF4_BASE.throwHit(T,dt);T.hitCd=Math.max(0,T.hitCd-dt);if(T.reflected||T.hitCd>0)return false;
 const L=fmcBlade(T._cf4Host);let hit=false;if(L)for(const seat of seatList())withSeat(seat,()=>{if(!player.dead&&player.invuln<=0&&s81003Distance(player.x,player.y,L)<L.width*.5+6){playerHit('alien returning sword');hit=true;}});
 if(hit){T.hitCd=.82;shake=Math.max(shake,7);}return hit;
};
gd4Tick=function(b,dt){const J=j3State(b),D=J?.mimic===5?gd4Create(b,5):null;
 if(D){const h=D.p._hammer;if(h.throw)h.throw._cf4Host=b;
  if(!fmcAlive(b,'sword')||!fmcAlive(b,'swordArm')){h.throw=null;if(h.mode==='hammer'||h.mode==='storm')hammerPhaseTwoStart(D.p);}}
 return CF4_BASE.donor.apply(this,arguments);
};

function cf4Dracula(b){const J=j3State(b);return J?.encounter===2&&J.mimic==null;}
function cf4Claw(v){return{x:v.x-Math.sin(v.rot)*v.h*.37,y:v.y+Math.cos(v.rot)*v.h*.37};}
function cf4ClawTell(b,P,v){
 const start=cf4Claw(v);if(P.type==='cf4Court')return{x:start.x,y:start.y,ex:P.tx,ey:P.ty,width:55};
 const time=P.t;try{P.t=P.tell+(P.type==='cf4Sweep'?(v.p.id==='left'?0:1.25)+.775:1.125);
  const target=r30Parts(b).find(q=>q.p.id===v.p.id),end=target?cf4Claw(target):start;
  return{x:start.x,y:start.y,ex:end.x,ey:end.y,width:80};
 }finally{P.t=time;}
}
r30Parts=function(b){if(!cf4Dracula(b)||b._r30.mode!=='fight')return CF4_BASE.parts(b);
 const S=b._r30,P=S.attack,k=Math.min(1.12,viewW()/530),out=[],t=S.clock;
 for(const p of b.parts){if(p.destroyed&&p.id!=='core')continue;
  if(p.id==='core'){out.push({p,x:b.x,y:b.y,w:240*k,h:290*k,rot:Math.sin(t*.6)*.018,key:'colossus_body',alpha:1});continue;}
  const side=p.id==='left'?-1:1,local=P?(P.t-P.tell-(P.type==='cf4Sweep'?(side<0?0:1.25):0)):0;
  let rot=-side*(.2+Math.sin(t*1.3+side)*.08),reach=0;
  if(P?.type==='cf4Sweep'){const u=clamp(local/1.55,0,1);rot=side*lerp(-.75,.95,Math.sin(u*Math.PI));reach=Math.sin(u*Math.PI)*50;}
  if(P?.type==='cf4Crush'){const u=clamp(local/2.25,0,1),v=Math.sin(u*Math.PI);rot=side*lerp(-.48,.55,v);reach=v*115;}
  const root={x:b.x+side*102*k,y:b.y-48*k+reach*k},h=265*k;
  out.push({p,x:root.x-Math.sin(rot)*h*.40,y:root.y+Math.cos(rot)*h*.40,w:125*k,h,rot,key:'colossus_arm'+(side<0?'L':'R'),alpha:1});
 }return out;
};
r30Tick=function(b,dt){if(!cf4Dracula(b)||b._r30.mode!=='fight')return CF4_BASE.tick.apply(this,arguments);
 dt=Math.min(.05,dt);j3Timers(b,dt);const S=b._r30,J=j3State(b);b.enter=false;
 b.x=camLeftX()+viewW()/2+Math.sin(S.clock*.53)*26;b.y=PLAY.y+158+Math.sin(S.clock*.79)*16;
 if(!S.attack){S.cd-=dt;if(S.cd>0)return;if(J.attacks>=3){j3Morph(b,J.active);return;}
  const type=['cf4Sweep','cf4Crush','cf4Court'][J.attacks++];S.seq++;
  S.attack={type,t:0,tell:diffKey==='easy'?1.5:1.15,active:type==='cf4Sweep'?3.1:type==='cf4Crush'?2.6:4.0,next:0,tx:player.x,ty:player.y};
  j3Log(b,'draculaPattern',{type});r30Sound('bossWeaponCharge');
 }
 const P=S.attack;P.t+=dt;const u=P.t-P.tell;
 combatWarningTick(b,'cf4-'+S.seq,Math.min(P.t,P.tell),P.tell);
 if(u<0)return;
 if(P.type!=='cf4Court')for(const v of r30Parts(b).filter(v=>v.p.id!=='core')){const tip=cf4Claw(v);for(const seat of seatList())withSeat(seat,()=>{if(!player.dead&&Math.hypot(player.x-tip.x,player.y-tip.y)<31)playerHit('colossus sweeping talon');});}
 if(u>=P.next){P.next=u+(P.type==='cf4Court'?.62:1.1);
  const ports=P.type==='cf4Court'?r30Parts(b).filter(v=>v.p.id!=='core').map(cf4Claw):[{x:b.x,y:b.y+95}];
  if(!ports.length)ports.push({x:b.x,y:b.y+95});
  for(const m of ports){const a=Math.atan2(P.ty-m.y,P.tx-m.x);for(const off of(P.type==='cf4Court'?[-.3,-.15,.15,.3]:[-.23,0,.23]))f1003bShot(b,m.x,m.y,a+off,P.type==='cf4Court'?2.7:3.2,'code',true);}
  r30Sound('combatAlien0927');
 }
 // Gentle orbit pull, bounded and telegraphed; thrust always overcomes it.
 if(P.type==='cf4Court')for(const seat of seatList())withSeat(seat,()=>{if(!player.dead){const a=Math.atan2(b.y-player.y,b.x-player.x);player.x=clamp(player.x+Math.cos(a+.55)*dt*19,camLeftX()+20,camRightX()-20);player.y=clamp(player.y+Math.sin(a+.55)*dt*12,PLAY.y+20,VH-35);}});
 if(u>P.active){S.attack=null;S.cd=.65;}j3Save(b);
};
r30DrawBoss=function(b){const J=j3State(b),S=b?._r30;if(!J)return CF4_BASE.draw.apply(this,arguments);
 // Hit throttling in markHit keeps concentrated allied fire from holding the
 // silhouette white, while every accepted hit remains visible for its duration.
  if(cf4Dracula(b)&&S.mode==='fight'){
   j3Body(b);const P=S.attack;if(P&&P.t<P.tell){for(const v of r30Parts(b).filter(v=>v.p.id!=='core'))combatWarningDraw(b,{...cf4ClawTell(b,P,v),progress:P.t/P.tell});}
   return;
  }
  CF4_BASE.draw(b);
  const h=cf4Knight(b);if(h){
   const p=J.gp4Donors[5].p;
   if(['chaingun_draw','chain_warn','chaingun','chain_cool'].includes(h.state))hammerBlasterGunDraw(p,h.state==='chaingun_draw'?clamp(h.t/2,0,1):1);
   if(h.throw)for(let i=Math.min(4,h.throw.trail.length-1);i>=2;i-=2){const q=h.throw.trail[i];fmcCell('knight','sword',q.x,q.y,34,100,q.angle,.10);}
   if(['storm_warn','giant_warn','mega_charge','curl','whirl_warn','whirl_turn','nova_charge'].includes(h.state)){
    const target=h.stormTarget||h.whirl&&{x:h.whirl.endX,y:h.whirl.y}||{x:h.tx||b.x,y:h.ty||VH-75};
    const duration=h.state==='mega_charge'?1.65:h.state==='curl'?HAMMER_BALL_WARN:h.state==='nova_charge'?1.6:1.1;
    combatWarningDraw(p,{x:b.x,y:b.y,ex:target.x,ey:target.y,width:h.state==='mega_charge'?hammerEradWidth():96,progress:clamp(h.t/duration,0,1)});
   }
   if(h.state==='storm_split')for(const q of h.stormWaves||[]){hammerStormRedZoneDraw(q);hammerStormRowRetinaDraw(q);hammerStormSpikeDraw(q);hammerStormRowAlertDraw(q);}
   if(['spell','spell_blast'].includes(h.state))for(const q of h.state==='spell'?h.spellTargets:h.pillars){
    groundTargetReticleDraw(q.x,VH-65,72,clamp(h.t/2.35,0,1),.9);if(h.state==='spell_blast')hammerChromiumDraw(q.x,VH-12,PLAY.y,44,h.t,1.35);}
   if(h.state==='mega_beam')hammerChromiumDraw(b.x,b.y-20,VH,hammerEradWidth(),h.t,hammerEradDuration());
  }
};
