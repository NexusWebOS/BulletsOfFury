"use strict";
/* Reviewed generated assets retain one scale/pivot across every animation. */
for(const a of Object.values(ENC30_ART))XART._src[a.key]=a.path;
function enc30Warm(stage){
 const names=stage===4?['tank_hull','tank_turret','tank_pod_l','tank_pod_r','jet','jet_laser','jet_missile','jet_rotary']:
 stage===6?['ace','ace_body','ace_wing_l','ace_wing_r','ace_body_damage','ace_wing_l_damage','ace_wing_r_damage','bomber']:
 stage===7?['vent_body','vent_fluid','entry']:[];
 for(const name of names)XART.rdy(ENC30_ART[name].key);
 if(stage===6)for(let i=0;i<8;i++)XART.rdy('nthr_blue_'+i);
}
function enc30Cell(name,f,x,y,w,h,tint){
 const a=ENC30_ART[name];if(!a||!XART.rdy(a.key))return false;
 const r=a.frames[((f|0)%a.frames.length+a.frames.length)%a.frames.length];
 const im=tint?xartPalette(a.key,tint):XART.get(a.key);if(!im)return false;
 ctx.save();ctx.imageSmoothingEnabled=false;ctx.drawImage(im,...r,Math.round(x-w/2),Math.round(y-h/2),w,h);ctx.restore();return true;
}
const ENC30_BASE={stage:beginStage,spawn:spawnEnemy,tankDraw:drawModularTank,jetDraw:drawModularJet,tankTick:modularTankTick,
 jetPoint:modularJetPoint,hit:hitEnemy,connector:connectorSurface,ace:whvDrawAce,aceSpawn:whvAceSpawn,
 aceHit:warhiveHitTest,fleet:furyFleetDraw,storm:drawS6Storm,bomb:missionBomb};
beginStage=function(n){const r=ENC30_BASE.stage.apply(this,arguments);enc30Warm(n);return r;};
spawnEnemy=function(){
 const args=Array.from(arguments);
 if(run.stage===4&&['tank','htank','minitank','s4minitank','s4airfield','roadtank'].includes(args[0]))args[0]='sandtank';
 const start=enemies.length,r=ENC30_BASE.spawn.apply(this,args);
 for(const e of enemies.slice(start)){
  if(run.stage===4&&(e._modTank===4||e._modJet)){
   const tank=e._modTank===4,k=tank?1.35:1.12;e.hp*=k;e.maxhp*=k;if(e._maxhp)e._maxhp*=k;
   e._r30={left:{hp:e.maxhp*.28},right:{hp:e.maxhp*.28},turret:{hp:e.maxhp*.40},rocketCd:3.2,warning:null};
   enc30Warm(4);
  }
  if(e._s6storm==='s6bomber'){e.w=116;e.h=124;enc30Warm(6);}
 }return r;
};
function enc30PartFlash(e,name,f,x,y,w,h,pal){
 const r=enc30Cell(name,f,x,y,w,h,pal);
 if(r&&e.flash>0){ctx.save();ctx.globalAlpha=Math.min(.85,e.flash*7);enc30Cell(name,f,x,y,w,h,hitFlashColor(e));ctx.restore();}return r;
}
drawModularTank=function(e){
 if(e._modTank!==4||e.dead||e._dyingT!=null)return ENC30_BASE.tankDraw(e);
 const w=e.w*1.26,h=w*144/128;
 if(!XART.rdy('enc30_tank_hull')||!XART.rdy('enc30_tank_turret'))return ENC30_BASE.tankDraw(e);
 const frame=Math.abs(e._spd||0)>1?Math.floor((e._wheelT||e.t||0)*3)%2:0;
 e._drawW=w*.90;e._drawH=h*.88;
 enc30PartFlash(e,'tank_hull',frame,e.x,e.y,w,h);
 for(const side of [-1,1]){
  const part=e._r30&&e._r30[side<0?'left':'right'];if(part&&part.hp<=0)continue;
  enc30PartFlash(e,side<0?'tank_pod_l':'tank_pod_r',0,e.x+side*w*.40,e.y+h*.08,w*.23,h*.44);
 }
 if(!e._r30||e._r30.turret.hp>0){
  ctx.save();ctx.translate(e.x,e.y+h*(76/144-.5));ctx.rotate((e._modAngle||Math.PI/2)-Math.PI/2);
  enc30PartFlash(e,'tank_turret',(e._recoil||e._muz||0)>0?1:0,0,h*(.5-65/144),w,h);ctx.restore();
 }
 const q=e._r30?.warning;
 if(q)combatWarningDraw(e,{x:e.x,y:e.y,ex:q.x,ey:q.y,progress:q.t/q.dur,width:36});
 return true;
};
drawModularJet=function(e){
 if(!e._modJet||e.dead||e._dyingT!=null||!XART.rdy('enc30_jet'))return ENC30_BASE.jetDraw(e);
 const w=Math.max(e.w,e.h)*1.28,h=w*144/120,pal=e._modJet==='snow'?'#b8d5df':e._modJet==='black'?'#515b65':null;
 // Authored banks foreshorten wings; no skewing or squashing the hull.
 const f=e.spin<-.10?1:e.spin>.10?2:0;
 e._drawW=w*.9;e._drawH=h*.90;enc30PartFlash(e,'jet',f,e.x,e.y,w,h,pal);
 for(const side of [-1,1]){
  if(e._r30&&e._r30[side<0?'left':'right'].hp<=0)continue;
  const p=modularJetMount(e,side),a=e._modJetAngles[side<0?'left':'right'];
  const gun='jet_'+(e._modJet==='desert'?'rotary':e._modJet==='black'?'missile':'laser');
  ctx.save();ctx.translate(p.x,p.y);ctx.rotate(a-Math.PI/2);
  enc30PartFlash(e,gun,0,0,0,w*.20,h*.32,pal);ctx.restore();
 }return true;
};
modularJetPoint=function(e,side){const p=ENC30_BASE.jetPoint(e,side);if(e._r30)p._disabled=e._r30[side<0?'left':'right'].hp<=0;return p;};
hitEnemy=function(e,dmg){
 const before=e.hp,r=ENC30_BASE.hit.apply(this,arguments),parts=e._r30,loss=Math.max(0,before-e.hp);
 if(parts&&loss>0&&!e.dead){
  const bx=_dmgBullet?.x,dx=Number.isFinite(bx)?bx-e.x:0;
  const name=Math.abs(dx)>e.w*.20?(dx<0?'left':'right'):'turret',p=parts[name];
  if(p&&p.hp>0){p.hp=Math.max(0,p.hp-loss);if(p.hp===0){
   const x=e.x+(name==='turret'?0:(name==='left'?-1:1)*e.w*.4);
   explode(x,e.y,e.w*.38,'red','fireball');if(Audio.SFX.expSmall)Audio.SFX.expSmall();
   if(e._modJet&&parts.left.hp<=0&&parts.right.hp<=0){e._s4Act=null;e._fcd=999;}
  }}
 }return r;
};
modularTankTick=function(e,dt){
 ENC30_BASE.tankTick(e,dt);const p=e._r30;if(e._modTank!==4||!p||e.dead)return;
 if(p.warning){
  const q=p.warning;q.t+=dt;combatWarningTick(e,'siege-pods',q.t,q.dur);
  if(q.t>=q.dur){for(const side of [-1,1]){
   if(p[side<0?'left':'right'].hp<=0)continue;
   const x=e.x+side*e.w*.48,y=e.y+e.h*.28,a=clamp(Math.atan2(q.y-y,q.x-x),Math.PI*.18,Math.PI*.82);
   const v=[3.5,4.6,5.7][fr27Difficulty()],b=eShootT(x,y,a,v,'s4missile',{w:10,h:22});
   b._s4Accel=.75;b._s4Max=v+1.2;
   navalFlash(null,{x,y,aim:a},.65,BPFX_MUZZLE_MISSILE,{n:8,hpx:24,life:.15});
  }p.warning=null;p.rocketCd=[5.4,4.5,3.8][fr27Difficulty()];}return;
 }
 p.rocketCd-=dt;
 if(p.rocketCd<=0&&(p.left.hp>0||p.right.hp>0)&&e.y>viewTopY()+35&&e.y<player.y-90&&e.x>camLeftX()+30&&e.x<camRightX()-30){
  p.warning={x:player.x,y:player.y,t:0,dur:[1.2,1.05,.92][fr27Difficulty()]};
 }
};
// Bomber doors show the actual bomb release rather than looping unrelated views.
function enc30BomberDraw(e,direction){
 if(!XART.rdy('enc30_bomber'))return false;
 const age=e._r30BombAt==null?99:efxClock-e._r30BombAt;
 const prep=e._s6Act&&!e._s6Act.fired;
 const f=age<.16?3:age<.4?2:age<.62?1:prep?2:0,w=152,h=158;
 ctx.save();ctx.translate(e.x,e.y);ctx.rotate(direction==='east'?-Math.PI/2:direction==='west'?Math.PI/2:0);
 enc30PartFlash(e,'bomber',f,0,0,w,h);ctx.restore();
 e._drawW=direction==='south'?w:h;e._drawH=direction==='south'?h:w;return true;
}
const MISSION1001_PALETTE=new Map();
function missionPaletteJetDraw1001(e){
 const A=e._mission29;if(e.dead||e._dyingT!=null)return true;
 const art=MISSION29_ART.bluejets;if(!XART.rdy(art.key))return true;
 const color=A.direction==='west'?'red':A.direction==='east'?'green':'blue';let im=XART.get(art.key);
 if(color!=='blue'){
  if(!MISSION1001_PALETTE.has(color)){
   const c=document.createElement('canvas');c.width=im.width;c.height=im.height;const g=c.getContext('2d');g.drawImage(im,0,0);
   const data=g.getImageData(0,0,c.width,c.height),d=data.data;
   for(let i=0;i<d.length;i+=4){const r=d[i],v=d[i+1],b=d[i+2];
    // Change blue paint only; keep the white metal, outlines and orange ordnance.
    if(d[i+3]&&b>r*1.35&&b>v*1.12){d[i]=color==='red'?b:r;d[i+1]=color==='green'?b:v*.62;d[i+2]=color==='red'?r:v*.48;}}
   g.putImageData(data,0,0);MISSION1001_PALETTE.set(color,c);
  }im=MISSION1001_PALETTE.get(color);
 }
 const f={east:0,west:1,south:2}[A.direction],s=e._s67Draw||100,r=art.frames[f];
 ctx.save();ctx.imageSmoothingEnabled=false;ctx.drawImage(im,...r,e.x-s/2,e.y-s/2,s,s);ctx.restore();
 if(e.flash>0)s67CellFlash('bluejets',f,e.x-s/2,e.y-s/2,s,s,e);e._drawW=e._drawH=s;return true;
}
furyFleetDraw=function(e){if(e._mission29)return missionPaletteJetDraw1001(e);return ENC30_BASE.fleet(e);};
drawS6Storm=function(e){if(e._s6storm==='s6bomber'&&!e.dead&&e._dyingT==null&&enc30BomberDraw(e,e._dir<0?'west':'east'))return true;return ENC30_BASE.storm(e);};
missionBomb=function(e){e._r30BombAt=efxClock;return ENC30_BASE.bomb(e);};

// New ace has its own complete poses; the intro stealth squad keeps its identity.
whvAceSpawn=function(b){ENC30_BASE.aceSpawn(b);enc30Warm(6);b.w=148;b.h=152;b._whv.ace._enc30=true;};
function enc30AceFrame(b,A){
 if(A.somer)return 12+clamp(Math.floor(A.somer.t/.62*8),0,7);
 if(A.roll){const f=clamp(Math.floor(A.roll.t/.46*8),0,7);return 4+(A.roll.dir>0?f:(8-f)%8);}
 if(A.inverted)return 2;
 if(Math.abs(A.vx)>170)return A.vx>0?5:11;
 return b.hp/b.maxhp<.5?1:0;
}
warhiveHitTest=function(b,x,y){
 const W=b._whv,A=W?.ace;if(W?.mode!=='ace'||!A?._enc30)return ENC30_BASE.aceHit(b,x,y);
 if(b.dead||whvAceInvuln(A))return false;
 const dx=x-A.x,dy=y-A.y,hit=Math.abs(dx)<(Math.abs(dy)<30?74:40)&&Math.abs(dy)<74;
 if(hit)A._hitMod=Math.abs(dx)<36?'body':dx<0?'wingL':'wingR';return hit;
};
whvDrawAce=function(b){
 const W=b._whv,A=W?.ace;if(!A||!XART.rdy('enc30_ace'))return ENC30_BASE.ace(b);
 const w=184,h=192;
 if(A.dash?.st==='warn')combatWarningDraw(b,{x:A.x,y:A.y,ex:A.dash.ex,ey:A.dash.ey,progress:A.dash.t/.95,width:w*.65});
 const P=A.desp;
 if(P?.st==='warn')combatWarningDraw(b,{x:A.x,y:A.y,ex:A.x,ey:VH+60,progress:P.t/.8,width:w*.65});
 if(P?.st==='cross'&&P.t<P.lead){combatWarningDraw(b,{x:P.x0,y:P.y0,ex:P.x1,ey:P.y1,progress:P.t/P.lead,width:95,fieldOnly:true});return;}
 const f=enc30AceFrame(b,A),whole=b.dead||f>1;
 if(whole){ctx.save();ctx.translate(A.x,A.y);if(b.dead)ctx.rotate(A.spin||0);enc30PartFlash(b,'ace',f,0,0,w,h);ctx.restore();}
 else{
  for(const [part,fl] of [['wing_l','wingL'],['body','body'],['wing_r','wingR']]){
   const name='ace_'+part+(f===1?'_damage':'');enc30Cell(name,0,A.x,A.y,w,h);
   if((A.fl?.[fl]||0)>0){ctx.save();ctx.globalAlpha=Math.min(.9,A.fl[fl]*7);enc30Cell(name,0,A.x,A.y,w,h,'#fff');ctx.restore();A.fl[fl]=Math.max(0,A.fl[fl]-(_lastDt||1/60));}
  }
 }
 if(!b.dead&&!A.somer&&!A.inverted){
  const f=Math.floor(efxClock*14)%8;
  const key='nthr_blue_'+f;
  if(XART.rdy(key))for(const s of [-1,1]){ctx.save();ctx.translate(A.x+s*22,A.y-h*.30);ctx.rotate(Math.PI);ctx.imageSmoothingEnabled=false;ctx.globalAlpha=.85;ctx.drawImage(XART.get(key),-6,-1,12,48);ctx.restore();}
 }
 if(!b.dead){const r=b.hp/b.maxhp;whvPartFx(b,{x:A.x-58,y:A.y},r,false,.8,5);whvPartFx(b,{x:A.x+58,y:A.y},r,false,.8,6.3);}
};
whvAceGuns=function(b,A,spread){
 for(const s of [-1,1])eShoot(A.x+s*61,A.y+48,Math.PI/2+(spread||0)*s,6.2,'mg');
 whvSfx('enemyShoot',.6);
};

// Fixed outlet + animated liquid. Both drawing and damage use these same bounds.
function enc30VentAge(e){return e.live&&!e.done?e.t-stage7SluiceWarn():-99;}
function enc30VentFrame(age){return age<0?0:age<.13?2:age<.25?3:age<.78?4+(Math.floor(age*12)%2):age<.94?6:7;}
function enc30VentRange(e){const age=enc30VentAge(e);return age<0||age>=.78?0:age<.13?76:age<.25?145:178;}
stage7SluiceTick=function(dt){
 if(run.stage!==7||!Number.isFinite(_masterSrcY))return;enc30Warm(7);
 const rank=fr27Difficulty(),warn=stage7SluiceWarn();
 for(const e of stage7SluiceEvents()){
  if(e.tier>rank||e.done)continue;const y=e.row-_masterSrcY;
  if(!e.live){if(bossActive||subBossActive||y<VH*.60||y>VH*.82)continue;e.live=true;e.t=0;(Audio.SFX.bossWeaponCharge||function(){})();}
  e.t+=dt;
  if(!e.fired&&e.t>=warn){e.fired=true;(Audio.SFX.enemyToxicSpit||function(){})();}
  if(e.t>=warn+1.10){e.done=true;continue;}
  const reach=enc30VentRange(e),W=worldWidth(),mouth=168;
  if(!reach||y<-45||y>VH+45)continue;
  const lo=e.side<0?mouth:W-mouth-reach,hi=e.side<0?mouth+reach:W-mouth;
  for(const seat of seatList())withSeat(seat,()=>{if(!player.dead&&!player.out&&player.invuln<=0&&
   player.x+(player._hx||9)>lo&&player.x-(player._hx||9)<hi&&Math.abs(player.y-y)<24+(player._hy||10))playerHit('stage7Sluice');});
 }
};
stage7SluiceDraw=function(){
 if(run.stage!==7||!XART.rdy('enc30_vent_body')||!XART.rdy('enc30_vent_fluid'))return;
 for(const e of stage7SluiceEvents()){
  if(e.tier>fr27Difficulty())continue;const y=e.row-_masterSrcY;if(y<-100||y>VH+100)continue;
  const age=enc30VentAge(e),warning=e.live&&!e.done&&age<0,warn=stage7SluiceWarn();
  ctx.save();if(e.side>0){ctx.translate(worldWidth(),0);ctx.scale(-1,1);}
  if(warning)s67LaneBand(168,y,346,y,48,clamp(e.t/warn,0,1),1.2);
  enc30Cell('vent_body',0,122,y-10,116,180);
  if(warning){ctx.save();ctx.globalCompositeOperation='lighter';ctx.globalAlpha=.12+.15*(1+Math.sin(e.t*18));enc30Cell('vent_body',0,122,y-10,116,180);ctx.restore();}
  if(age>=0&&age<1.10)enc30Cell('vent_fluid',enc30VentFrame(age),168+90,y,180,100);
  ctx.restore();
 }
};
connectorSurface=function(st,joinY,ww){
 const r=ENC30_BASE.connector.apply(this,arguments);
 if(st!==7||!XART.rdy('enc30_entry')||joinY+1120<0)return r;
 // Same coordinate system and velocity as entryConnectorDraw. Animated sludge
 // remains below the alpha holes; the pilot crosses an overhead beam top-down.
 const w=Math.max(680,ww),x=(w-680)/2;
 ctx.save();ctx.imageSmoothingEnabled=false;ctx.drawImage(XART.get('enc30_entry'),x,joinY,680,1120);ctx.restore();
 return true;
};

// The sewer entrance needs liquid under both sides of the join: its terminal
// terrain edge is intentionally transparent. Clip-free underlay prevents voids.
const ENC30_ENTRY=entryConnectorDraw;
entryConnectorDraw=function(st,dy){
 if(st!==7||!XART.rdy('enc30_entry'))return ENC30_ENTRY(st,dy);
 const d=Math.max(0,Math.round(dy)),ww=worldWidth(),join=VH-d;
 ctx.save();if(ww>VW)ctx.translate(-camX,0);
 ENC30_BASE.connector(st,join,ww);
 // Tuck the new floor below the master's irregular terminal edge.
 ctx.drawImage(XART.get('enc30_entry'),(Math.max(680,ww)-680)/2,join-32,680,1120);
 ctx.restore();
 if(d>=VH)return false;
 const cfg=_levelCfg(),mk=stageMasterKey(cfg);if(!XART.rdy(mk))return false;
 ctx.save();ctx.beginPath();ctx.rect(0,0,VW,Math.max(0,join-32));ctx.clip();
 if(ww>VW)ctx.translate(-camX,0);ctx.translate(0,-d);drawBG(0);ctx.restore();
 // The authored overhead girder covers the structural join, like a tunnel lintel.
 ctx.save();if(ww>VW)ctx.translate(-camX,0);
 ctx.drawImage(XART.get('enc30_entry'),0,500,680,58,(Math.max(680,ww)-680)/2,join-44,680,58);ctx.restore();return true;
};
