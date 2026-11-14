'use strict';
/* New whole Draconus drawings; original Stage5 effect pixels are baked offline.
   Native copied-boss HP, phase clocks, shots, damage, sounds and return persist. */
const DCR13={base:{pose:hb20Pose,cast:rf1110CastPose,blit:rf1110Blit,hands:rf1110DracHands,
 charge:rf1110ChargeDraw,chargeTick:rf1110ChargeTick,fx:rf1110Fx,rdFx:rd74Fx,
 lightning:rf1110BeamLightning,draw:v19DonorDraw,bg:drawBG,load:stageLoadBegin,keys:v18Keys,
 warm:v18Warm,ready:stageLoadReady},events:[],draws:[]};
function dcr13Log(type,data={}){DCR13.events.push({type,time:efxClock,...data});if(DCR13.events.length>600)DCR13.events.shift();}
for(const n of Object.keys(DCR13_ART))XART._src['dcr13_'+n]='assets/game/shared/combat/draconus_cinematic_rage_1113/'+n+'.webp';
// Replace the complete center bank in every material, not a display-only overlay.
{const a=DCR13_ART.center_chrome,old=BA119_ART['corrupt-overhead'];
 Object.assign(old,{cell:[512,512],pivot:[256,256],count:32,cols:4,folder:'draconus_cinematic_rage_1113',meta:a.meta});
 for(const mat of ['regular','chrome','red','hit','red_hit']){
  const bank='ba119_corrupt-overhead_'+mat,key='nca_'+bank;
  XART._src[key]='assets/game/shared/combat/draconus_cinematic_rage_1113/center_'+mat+'.webp';
  for(let f=0;f<32;f++)BOFX.cells[bank+'_'+f]=[bank,f%4*512,Math.floor(f/4)*512,512,512];
  if(RD74_ART.banks[bank])Object.assign(RD74_ART.banks[bank],{key,cw:512,ch:512,cols:4,frames:32,pivot:[256,256],meta:a.meta});
 }
}
for(const depth of ['fore','back']){const bank='drac_palms_'+depth;
 RF1110_ART.banks[bank].meta=DCR13_ART['palms_'+depth+'_power'].meta;
 for(const mat of ['power','hit'])XART._src['rf1110_'+bank+'_'+mat]='assets/game/shared/combat/draconus_cinematic_rage_1113/palms_'+depth+'_'+mat+'.webp';
}
const DCR13_KEYS=Object.keys(DCR13_ART).filter(n=>!n.startsWith('center_')&&!n.startsWith('rage_')&&!n.startsWith('palms_')).map(n=>'dcr13_'+n);
function dcr13Warm(){return DCR13_KEYS.map(k=>XART.rdy(k)).every(Boolean);}
stageLoadBegin=function(n,keys){return DCR13.base.load.call(this,n,[...(keys||[]),...(n===8?DCR13_KEYS:[])]);};
v18Keys=function(){return[...DCR13.base.keys.apply(this,arguments),...(run.stage===8?DCR13_KEYS:[])];};
v18Warm=function(){return DCR13.base.warm.apply(this,arguments)&&(run.stage!==8||dcr13Warm());};
stageLoadReady=function(n=run.stage){return DCR13.base.ready.apply(this,arguments)&&(n!==8||dcr13Warm());};
function dcr13Frame(name,f){const a=DCR13_ART[name];f=clamp(f|0,0,a.count-1);const m=a.meta[f],hand=m.ball||[a.pivot[0],a.pivot[1]+65];return{...m,tip:hand,headCenter:hand,muzzle:hand,key:'dcr13_'+name,
 white:'dcr13_'+name+'_hit',w:a.cw,h:a.ch,pivot:a.pivot,bank:name,frame:f,_rf1110:true,_dcr13:true};}
function dcr13Draw(name,f,x,y,hit=false){const a=DCR13_ART[name];if(!a)return false;f=clamp(f|0,0,a.count-1);
 const key='dcr13_'+name+(hit?'_hit':'');if(!XART.rdy(key))return false;
 ctx.drawImage(XART.get(key),f%4*a.cw,Math.floor(f/4)*a.ch,a.cw,a.ch,Math.round(x-a.pivot[0]),Math.round(y-a.pivot[1]),a.cw,a.ch);
 return true;}
rf1110Blit=function(a,x,y,hit=false){if(a?._dcr13){DCR13.draws.push({bank:a.bank,frame:a.frame,time:efxClock,hit});if(DCR13.draws.length>300)DCR13.draws.shift();return dcr13Draw(a.bank,a.frame,x,y,hit);}return DCR13.base.blit.apply(this,arguments);};
function dcr13Formation(u){return clamp(Math.floor((u-.30)/.70*32),0,31);}
rf1110CastPose=function(unit,R){if(unit!=='drac')return DCR13.base.cast.apply(this,arguments);
 const phase=R.phase.replace('kame_',''),depth=R.scale<.7?'back':'fore';let f=0;
 if(phase==='charge'||phase==='gather'){const dur=R.phase==='gather'?1.7:C46_T.charge;f=Math.min(6,Math.floor(R.t/(dur*.65)*7));}
 else if(phase==='thrust')f=7+Math.min(5,Math.floor(R.t/.36*6));
 else if(phase==='fire'||phase==='beam')f=Math.floor(R.t*8)%4===3?13:12;
 else if(phase==='recover')f=13+Math.min(2,Math.floor(R.t/.16));
 return{a:dcr13Frame('cast_'+depth,f),k:1,rot:0,kind:'dcr13_two_hand_cast'};
};
hb20Pose=function(b){if(rd74Own(b)){const Q=hb20State(b),A=Q.action;
 if(A?.type==='rage'&&A.t>=.95){const recoup=A.t<2.16,bank=recoup?'recoup':'formation',age=A.t-.95,f=recoup?(age<.18?Math.floor(age/.18*3):age<.55?3+Math.min(1,Math.floor((age-.18)/.37*2)):5+Math.min(10,Math.floor((age-.55)/.66*11))):dcr13Formation(A.t/7.2);
  return{a:dcr13Frame(bank,f),k:1,rot:0,kind:recoup?'dcr13_stop_recoup':'dcr13_rage_formation'};}
 }return DCR13.base.pose.apply(this,arguments);};
rf1110DracHands=function(b,R,release=false){const q=release?{a:dcr13Frame('cast_'+(R.scale<.7?'back':'fore'),12)}:rf1110CastPose('drac',R),a=q.a,p=a.ball;
 return{x:b.x+p[0]-a.pivot[0],y:b.y+p[1]-a.pivot[1]};};
// The exact Stage5 strike schedule and scatter/closing-in targets, once per tick.
rf1110ChargeTick=function(b,C,u,dt,color){if(color!=='purple'||!rd74Own(b))return DCR13.base.chargeTick.apply(this,arguments);
 const P=C.rf1110??={n:0,bolts:[],done:false};for(const q of P.bolts)q.age+=dt;P.bolts=P.bolts.filter(q=>q.age<.18);
 const q=hb20Pose(b),n=c45StrikeCount(u);
 while(P.n<n){const i=++P.n,T=c45StrikeTarget(b,q,i),at=T.ground?T.pt:c45Point(b,q,T.body[0],T.body[1]),offset=(((i*37)%11)-5)*7;
  P.bolts.push({x:at.x,y:at.y,age:0,index:i,offset});shake=Math.max(shake,4+Math.min(7,i*.3));
  if(T.ground)explode(at.x,at.y,30+30*c45Prog(u),'red');else P.flash=2/60;
  Snd.play(CF48.key,.63);rf1110Log('charge-strike',{color,index:i});dcr13Log('formation-strike',{index:i,ground:T.ground,at});
 }
 P.flash=Math.max(0,(P.flash||0)-dt);
 if(u>=.8&&!P.done){P.done=true;P.bolts.push({x:b.x,y:b.y+40,age:0,index:27,offset:0});flashScreen=Math.max(flashScreen||0,.18);shake=Math.max(shake,18);
  hb20State(b).rf1110Rings={x:b.x,y:b.y,start:efxClock};Snd.play(CF48.key,.63);rf1110Log('charge-release',{color});dcr13Log('formation-release');}
};
function dcr13Bolt(q){dcr13Draw('bolt_'+((q.offset||0)+35),Math.floor(q.age/.18*8),q.x,q.y);}
rf1110ChargeDraw=function(b,C,u,unit){if(unit!=='drac')return DCR13.base.charge.apply(this,arguments);
 const f=dcr13Formation(u),swirl=clamp(Math.floor((u-.38)/.62*32),0,31);
 if(u>=.38)dcr13Draw('swirl_back',swirl,b.x,b.y);
 dcr13Draw('aura_formation',f,b.x,b.y);
 dcr13Draw('formation',f,b.x,b.y,Math.max(b.flash||0,hb20State(b).parts[0].flash||0,C.rf1110?.flash||0)>0);
 for(const q of C.rf1110?.bolts||[])dcr13Bolt(q);
 if(u>=.38)dcr13Draw('swirl_front',swirl,b.x,b.y);
 RF1110.last={unit,phase:'dcr13-rage-formation',frame:f,charge:u};
};
function dcr13Casting(R){return['kame_charge','gather','kame_thrust','thrust','kame_fire','beam'].includes(R?.phase);}
// Remove only the superseded one-palm ball and copied purple wave during the
// new two-handed cast. Ordinary palm volley flashes keep their native owner.
rf1110Fx=function(color,kind){if(color==='purple'&&kind==='gather'&&rf1110Drac(boss)&&dcr13Casting(hb20State(boss).rf1110))return;return DCR13.base.fx.apply(this,arguments);};
rd74Fx=function(name){if(name==='wave_purple'&&rf1110Drac(boss))return;return DCR13.base.rdFx.apply(this,arguments);};
rf1110BeamLightning=function(b,R,color){if(color==='purple'&&rd74Own(b)&&dcr13Casting(R)){
 const phase=R.phase.replace('kame_',''),off={charge:0,gather:0,thrust:2.6,fire:2.96,beam:2.96}[phase],elapsed=off+R.t,age=elapsed%.38;
 if(age<.18){const beat=Math.floor(elapsed/.38),x=lerp(camLeftX(),camRightX(),[.18,.76,.39,.89,.58,.09,.68,.30][beat%8]);dcr13Bolt({x,y:VH-15,age,offset:0});}return;
 }return DCR13.base.lightning.apply(this,arguments);};
v19DonorDraw=function(b){const Q=rd74Own(b)&&hb20State(b),R=Q?.rf1110;
 if(R&&dcr13Casting(R)){const q=rf1110CastPose('drac',R);dcr13Draw('aura_cast_'+(R.scale<.7?'back':'fore'),q.a.frame,b.x,b.y);}
 const out=DCR13.base.draw.apply(this,arguments);
 if(R&&dcr13Casting(R)){
  const fire=R.phase==='kame_fire'||R.phase==='beam',thrust=R.phase==='kame_thrust'||R.phase==='thrust',dur=R.phase==='gather'?1.7:C46_T.charge;
  const p=rf1110DracHands(b,R),u=fire||thrust?1:clamp(R.t/dur,0,1);
  if(fire){const L=rf1110DracLine(b,R);dcr13Draw('wave',c41Frame(R.t,R.phase==='beam'?1.35:C46_T.fire),L.from.x,L.from.y);}
  dcr13Draw(R.scale<.7?'ball_back':'ball',Math.floor(u*15),p.x,p.y);
  DCR13.lastCast={phase:R.phase,frame:rf1110CastPose('drac',R).a.frame,ball:{...p},release:rf1110DracHands(b,R,true)};
 }
 return out;
};
drawBG=function(){const out=DCR13.base.bg.apply(this,arguments);if(rd74Own(boss)){
 const Q=hb20State(boss),A=Q.action;if(A?.type==='rage'&&A.t>=2.16)cf50DimDraw(Math.round(clamp(c45Prog(A.t/7.2),0,1)*15));
 else if(Q.rf1110&&!dcr13Casting(Q.rf1110))cf50DimDraw(9);
 }return out;};
globalThis.BOF_DRACONUS_CINEMATIC_RAGE_1113=DCR13;
