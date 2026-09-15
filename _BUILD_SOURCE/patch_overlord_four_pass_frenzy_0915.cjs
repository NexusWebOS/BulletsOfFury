const fs=require('fs'),path=require('path');const root=path.resolve(__dirname,'..'),gamePath=path.join(root,'assets','game.js'),suitePath=path.join(root,'_BUILD_SOURCE','test_fl.js');
const recovery=path.join(root,'_shots','overlord_four_pass_frenzy_0915','recovery');fs.mkdirSync(recovery,{recursive:true});
const before=fs.readFileSync(gamePath,'utf8'),suite=fs.readFileSync(suitePath,'utf8');if(before.includes('\r\n'))throw new Error('game must remain LF');if(/(^|[^\r])\n/.test(suite))throw new Error('suite must remain CRLF');
fs.writeFileSync(path.join(recovery,'game.js.before'),before);fs.writeFileSync(path.join(recovery,'test_fl.js.before'),suite);let s=before;
function once(a,b,label){const n=s.split(a).length-1;if(n!==1)throw new Error(label+' expected once, got '+n);s=s.replace(a,b);}

once("const OV_CHARGE_BEATS=8, OV_CHARGE_TELL=1.60, OV_CHARGE_FLASH=.105;\n",
`const OV_CHARGE_BEATS=8, OV_CHARGE_TELL=1.60, OV_CHARGE_FLASH=.105;
const OV_PASS_LANES=[86,188,292,394];
function ovPassLane(Q){
  const open=OV_PASS_LANES.filter(x=>Q.used.indexOf(x)<0),px=clamp(player.x,86,VW-86);
  open.sort((a,b)=>Math.abs(a-px)-Math.abs(b-px));
  const lane=open[0]==null?px:open[0];Q.used.push(lane);Q.lastLane=lane;return lane;
}
function ovChargeOrigin(b,T){
  const dir=T&&T.dir<0?-1:1,y=(b._drawY!=null?b._drawY:b.y)+dir*(b._drawH||b.h)*.38;
  return {x:b.x+(b._ovJitterX||0),y:y+(b._ovJitterY||0)};
}
function ovPassRain(b,Q){
  const y=(b._drawY!=null?b._drawY:b.y)+b.h*.26,spread=Q.pass===3?[-34,-11,11,34]:[-28,0,28];
  for(let i=0;i<spread.length;i++){
    const x=b.x+spread[i],a=Math.PI/2+(i-(spread.length-1)/2)*.045;
    eShootT(x,y,a,b._crit?5.5:5.0,'mg',{w:5,h:12,silent:i>0,impact:'yellow'});
    navalFlash(null,{x:x,y:y},.68,S1_MUZZLE_ROTARY,{n:6,hpx:30,life:.10});
  }
  stageRevisionCue(b,'overlordGun',.075);
}
`,'four-pass helpers');

once("function ovStartChargeTell(b){\n  b._ovState='chargeTell';\n  b._chargeTell={t:0,dur:OV_CHARGE_TELL,lane:clamp(player.x,72,VW-72),locked:false,pulse:0,beat:-1,flash:0};\n",
`function ovStartChargeTell(b){
  if(b._enraged&&!b._ovPassUsed&&!b._ovPassSeq){b._ovPassUsed=true;b._ovPassSeq={pass:0,used:[],lastLane:null};}
  const Q=b._ovPassSeq,pass=Q?Q.pass:-1,dir=Q&&pass%2===1?-1:1,base=Q?ovPassLane(Q):clamp(player.x,72,VW-72);
  b._ovState='chargeTell';
  b._chargeTell={t:0,dur:OV_CHARGE_TELL,lane:base,baseLane:base,locked:false,pulse:0,beat:-1,flash:0,pass:pass,dir:dir,holdY:dir>0?VH*.22:VH*.78};
`,'sequence-aware tell');

once("      const T=b._chargeTell, p=ovChargeWarningProgress(T), hub=ovMount(b,0,4);\n      combatWarningDraw(b,{x:hub[0],y:hub[1],ex:T.lane,ey:VH,progress:p,width:42,fieldOnly:true});\n",
"      const T=b._chargeTell, p=ovChargeWarningProgress(T), hub=ovChargeOrigin(b,T);\n"+
"      combatWarningDraw(b,{x:hub.x,y:hub.y,ex:T.lane,ey:T.dir<0?0:VH,progress:p,width:42,fieldOnly:true});\n",
'bidirectional field');

once("      const T=b._chargeTell,p=ovChargeWarningProgress(T),hub=ovMount(b,0,4);\n      combatWarningDraw(b,{x:hub[0],y:hub[1],ex:T.lane,ey:VH,progress:p,width:42,alertOnly:true});\n",
"      const T=b._chargeTell,p=ovChargeWarningProgress(T),hub=ovChargeOrigin(b,T);\n"+
"      combatWarningDraw(b,{x:hub.x,y:hub.y,ex:T.lane,ey:T.dir<0?0:VH,progress:p,width:42,alertOnly:true});\n",
'bidirectional alert');

once("    if(p<0.48){ T.lane=lerp(T.lane,clamp(player.x,72,VW-72),0.18); }\n",
"    if(p<0.48){\n"+
"      const aim=T.pass>=0?clamp(player.x,T.baseLane-42,T.baseLane+42):clamp(player.x,72,VW-72);\n"+
"      T.lane=lerp(T.lane,aim,0.18);\n"+
"    }\n",
'lane-band tracking');

once("    b.y=lerp(b.y,bobTargetY,0.08);\n    b._pivot=clamp(b._pivot*0.55-(b.x-oldX)*0.12,-0.65,0.65);\n",
"    b.y=lerp(b.y,T.holdY,0.08);\n"+
"    const face=T.dir<0?Math.PI:0;b._pivot=lerp(b._pivot,face,.12);\n"+
"    if(T.dir>0)b._pivot=clamp(b._pivot-(b.x-oldX)*0.12,-0.65,0.65);\n",
'bidirectional hold and facing');

once("      b._ovState='chargeOff'; b._chg={t:0,lane:T.lane,v:b._enraged?225:190};\n",
"      b._ovState='chargeOff'; b._chg={t:0,lane:T.lane,v:b._enraged?225:190,dir:T.dir,pass:T.pass};\n",
'charge direction commit');

const oldCharge=`  if(S==='chargeOff'){
    // Committed attack run: it may align for 0.16s, then it never tracks the player's new position.
    // That fixed lane is what makes the violent rush fair and consistently evadable.
    b._chg.t+=dt;
    const tx=b._chg.lane;
    if(b._chg.t<0.16) b.x=lerp(b.x,tx,0.24); else b.x=tx;
    b._chg.v=(b._chg.v||190)+640*dt; b.y+=b._chg.v*dt;
    b._pivot=lerp(b._pivot,0,0.18);
    if(b.y<VH*0.68){ b._chgFire-=dt; if(b._chgFire<=0){ b._chgFire=b._enraged?0.07:0.095; ovTwinMG(b); } }
    if(b.y>VH+110){
      const from=tx<VW/2?-1:1;
      b._ovState='reentry';
      b._re={t:0,from:from,startX:from<0?-115:VW+115,startY:VH*0.70,fire:0.12,rocket:0.72,rkN:0};
      b.x=b._re.startX; b.y=b._re.startY;
    }
    return;
  }
`;
const newCharge=`  if(S==='chargeOff'){
    // Every leg commits to the warned lane. The half-health set alternates south/north four times;
    // only legs two and four rain rounds downfield while the helicopter crosses the arena.
    b._chg.t+=dt;
    const tx=b._chg.lane,dir=b._chg.dir<0?-1:1,Q=b._ovPassSeq;
    if(b._chg.t<0.16)b.x=lerp(b.x,tx,0.24);else b.x=tx;
    b._chg.v=(b._chg.v||190)+640*dt;b.y+=dir*b._chg.v*dt;
    b._pivot=lerp(b._pivot,dir<0?Math.PI:0,0.18);
    if(Q&&(Q.pass===1||Q.pass===3)&&b.y>-40&&b.y<VH+40){
      b._chgFire-=dt;if(b._chgFire<=0){b._chgFire=Q.pass===3?.075:.095;ovPassRain(b,Q);}
    }else if(!Q&&b.y<VH*.68){b._chgFire-=dt;if(b._chgFire<=0){b._chgFire=b._enraged?.07:.095;ovTwinMG(b);}}
    const escaped=dir>0?b.y>VH+110:b.y<-110;
    if(escaped){
      if(Q&&Q.pass<3){Q.pass++;b._chgFire=0;ovStartChargeTell(b);return;}
      if(Q)b._ovPassSeq=null;
      const from=tx<VW/2?-1:1;b._ovState='reentry';
      b._re={t:0,from:from,startX:from<0?-115:VW+115,startY:VH*.70,fire:.12,rocket:.72,rkN:0};
      b.x=b._re.startX;b.y=b._re.startY;
    }
    return;
  }
`;
once(oldCharge,newCharge,'four-pass charge state');

fs.writeFileSync(gamePath,s,'utf8');if(s.includes('\r\n'))throw new Error('game endings changed');
const include="require('./test_overlord_four_pass_frenzy_0915.cjs')(vm,ctxv,ok);\r\n",marker="require('./test_overlord_eight_beat_warning_0915.cjs')(vm,ctxv,ok);\r\n";
if(!suite.includes(include)){const n=suite.split(marker).length-1;if(n!==1)throw new Error('suite marker count '+n);fs.writeFileSync(suitePath,suite.replace(marker,marker+include),'utf8');}
if(/(^|[^\r])\n/.test(fs.readFileSync(suitePath,'utf8')))throw new Error('suite endings changed');console.log('patched Overlord four-pass half-health frenzy');

