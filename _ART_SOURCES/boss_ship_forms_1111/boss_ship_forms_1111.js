'use strict';
/* SF1111: whole authored ships/actors. Native encounters own HP, bullets,
   phase gates, rewards, music and the already approved hammer attacks. */
const SF1111={base:{blue:ha21Blue,image:b20Image,arch:archBlit,clip:v18Clip,pose:hb20Pose,start:hb20Start,tick:v19NativeTick,rig:v19HammerRig,blit:rd74Blit,draw:v19DonorDraw,bossDraw:r30DrawBoss,hit:modularHit,load:stageLoadBegin,keys:v18Keys,warm:v18Warm,clear:v18Clear,state:hammerState,enter:v18Enter,finish:rd74Finish},events:[],draws:{},folder:'assets/game/shared/combat/boss_ship_forms_1111/'};
function sf1111Log(event,data={}){SF1111.events.push({event,clock:efxClock,...data});if(SF1111.events.length>500)SF1111.events.shift();}
for(const [name,a]of Object.entries(SF1111_ART))for(const mat of ['regular','chrome','red','hit']){const key='sf1111_'+name+'_'+mat;XART._src[key]=SF1111.folder+name+'_'+mat+'.webp';if(a.gun&&mat!=='hit')XART._src[key+'_gunhit']=SF1111.folder+name+'_'+mat+'_gunhit.webp';}
function sf1111Keys(n){return Object.keys(XART._src).filter(k=>k.startsWith('sf1111_')&&(n===5?k.startsWith('sf1111_chronus-'):n===8?!k.startsWith('sf1111_chronus-'):true));}
function sf1111Warm(n){let ready=true;for(const k of sf1111Keys(n))if(!XART.rdy(k))ready=false;return ready;}
stageLoadBegin=function(n,keys){return SF1111.base.load.call(this,n,[...(keys||[]),...([5,8].includes(n)?sf1111Keys(n):[])]);};
v18Keys=function(){const prior=SF1111.base.keys();return run.stage===8?[...prior,...sf1111Keys(8)]:prior;};
v18Warm=function(){const prior=SF1111.base.warm();return prior&&(run.stage!==8||sf1111Warm(8));};
function sf1111Sample(bank,f=0,mat='regular'){const a=SF1111_ART[bank];f=clamp(Math.floor(f),0,a.count-1);return{a:{...a.meta[f],key:'sf1111_'+bank+'_'+mat,white:'sf1111_'+bank+'_hit',w:a.cell[0],h:a.cell[1],pivot:a.pivot,bank,frame:f,material:mat,_sf1111:true,_rd74:true},k:1,rot:0,kind:bank};}
function sf1111Blit(q,x,y,hit=false,gunhit=false){const a=SF1111_ART[q.a.bank],key=hit?q.a.white:gunhit&&a.gun?q.a.key+'_gunhit':q.a.key;if(!XART.rdy(key))return false;ctx.drawImage(XART.get(key),q.a.frame%a.cols*a.cell[0],Math.floor(q.a.frame/a.cols)*a.cell[1],...a.cell,Math.round(x-a.pivot[0]),Math.round(y-a.pivot[1]),...a.cell);SF1111.draws[q.a.bank]=(SF1111.draws[q.a.bank]||0)+1;return true;}
b20Image=function(a,x,y,k,rot,flash){if(a?._sf1111)return sf1111Blit({a},x,y,flash>0);return SF1111.base.image.apply(this,arguments);};
rd74Blit=function(q,x,y,hit=false){if(q?.a._sf1111){const Q=rd74Own(boss)&&hb20State(boss);return sf1111Blit(q,x,y,hit,(Q?.parts[2]?.flash||0)>0);}return SF1111.base.blit.apply(this,arguments);};
function sf1111Ship(bank,u,mat='regular'){return sf1111Sample(bank,clamp(u,0,1)*(SF1111_ART[bank].count-1),mat);}
ha21Blue=function(b){if(ba119Blue(b)){const h=b._hammer,m=b._hammerTime||b._hama;if(m&&m.mode!=='attack'){if(m.mode==='intro'&&m.musicStarted&&m.shipFrame!=null)return sf1111Ship('chronus-transform',(15-m.shipFrame)/9,c27Material(b));return SF1111.base.blue.apply(this,arguments);}if(['flyby','return','unfold'].includes(h.state))return sf1111Ship('chronus-transform',h.state==='unfold'?h.t/2:0,c27Material(b));}return SF1111.base.blue.apply(this,arguments);};
archBlit=function(key,f,x,y){if(key==='ship_transform'){if(HA21.painting===boss&&ha21Blue(boss)?.a._sf1111)return true;const m=boss?._hammerTime||boss?._hama,u=(15-f)/(m?.mode==='intro'?9:15);return sf1111Blit(sf1111Ship('chronus-transform',u,boss?c27Material(boss):'regular'),x,y);}return SF1111.base.arch.apply(this,arguments);};
hammerState=function(b,s){if(ba119Blue(b)&&['flyby','return','unfold'].includes(s)){b._hammer._td1111Dir=b._hammer._td1111From='center';}return SF1111.base.state.apply(this,arguments);};
v18Clip=function(name,t,d,x,y,size,reverse){if(name==='morph_hammer'){const Q=boss?._r30&&j3State(boss).hb20;return sf1111Blit(sf1111Ship('draconus-transform',reverse?1-clamp(t/d,0,1):clamp(t/d,0,1),Q?rd74Mat(Q):'regular'),x,y);}return SF1111.base.clip.apply(this,arguments);};
r30DrawBoss=function(b){if(v18Owned(b)){const S=b._r30,N=S.v18;let u=null;
 if(S.mode==='v18formOut'&&N.from===8)u=1-(N.to===0?S.t*.5:S.t)/1.45;
 else if(S.mode==='v18formOut'&&N.from===0&&N.to===8)u=S.t*.5/1.45;
 else if(S.mode==='v18formIn'&&N.form===8)u=(N.from===0?.8+S.t*.5:S.t)/1.6;
 else if(S.mode==='v18formIn'&&N.form===0&&N.from===8)u=1-(.8+S.t*.5)/1.6;
 if(u!==null){const Q=j3State(b).hb20;return sf1111Blit(sf1111Ship('draconus-transform',u,Q?rd74Mat(Q):'regular'),b.x,b.y);}
 }return SF1111.base.bossDraw.apply(this,arguments);};
v18Enter=function(b){const r=SF1111.base.enter.apply(this,arguments);if(rd74Own(b)){const Q=hb20State(b);Q._td1111Dir=Q._td1111From='center';Q.sf1111={acquired:false,held:false,broken:false};}return r;};
function sf1111State(Q){return Q.sf1111??=( {acquired:false,held:false,broken:false} );}
function sf1111Held(Q){return sf1111State(Q).held&&!sf1111State(Q).broken&&Q.gunHP>0;}
function sf1111Empty(Q,f=7){return sf1111Sample('draconus-catch-pre',f,rd74Mat(Q));}
function sf1111Hammer(Q,f=0){const count=BA119_ART[td1111Name('corrupt',Q._td1111Dir)]?.count||32;return ba119Corrupt(Q,f*16/count);}
function sf1111ArsenalPose(Q,A){const t=A.t;if(t<.8)return sf1111Hammer(Q,0);if(t<1.5)return sf1111Hammer(Q,(t-.8)/.7*16);if(t<1.78)return sf1111Hammer(Q,16+(t-1.5)/.28*6);if(t<1.98)return sf1111Hammer(Q,22);if(t<2.28)return sf1111Hammer(Q,24+(t-1.98)/.3*7);if(t<2.46)return sf1111Hammer(Q,(t-2.28)/.18*16);if(t<3.54)return sf1111Empty(Q,(t-2.46)/1.08*7);return sf1111Sample('draconus-catch-take',(t-3.54)/1.18*8,rd74Mat(Q));}
hb20Pose=function(b){if(rd74Own(b)){const Q=hb20State(b),A=Q.action,S=sf1111State(Q),mat=rd74Mat(Q);if(A&&!Q.rf1110&&!Q.rage){const t=A.t;
 if(A.type==='sf1111_arsenal')return sf1111ArsenalPose(Q,A);
 if(A.type==='sf1111_break')return sf1111Sample('draconus-gun-break',t/.84*7,mat);
 if(A.type==='recall'&&A.sf1111)return t<.60?sf1111Empty(Q):sf1111Hammer(Q,0);
 if(A.type==='armor'&&sf1111Held(Q))return sf1111Sample('draconus-gun-armor',t/A.duration*8,'regular');
 if(A.type==='gun'){
  if(A.sf1111Equip&&t<.38)return sf1111Hammer(Q,t/.38*16);
  if(A.sf1111Equip&&t<.60)return sf1111Empty(Q,(t-.38)/.22*7);
  if(A.sf1111Equip&&t<A.tell)return sf1111Sample('draconus-catch-take',(t-.60)/(A.tell-.60)*8,mat);
  if(t>=5.40)return sf1111Sample('draconus-gun-stow',(t-5.40)/.80*8,mat);
  if(t>=5)return sf1111Sample('draconus-gun-spin',7-(t-5)/.4*7,mat);
  const firing=t>=A.tell,bank=firing?'draconus-gun-fire':'draconus-gun-spin',count=SF1111_ART[bank].count;
  return sf1111Sample(bank,Math.floor((firing?t-A.tell:t)* (firing?24:8))%count,mat);
 }
 }if(!A&&S.held&&!Q.rf1110&&!Q.rage)return sf1111Sample('draconus-gun-spin',0,mat);}return SF1111.base.pose.apply(this,arguments);};
hb20Start=function(b,type){if(!rd74Own(b))return SF1111.base.start.apply(this,arguments);const Q=hb20State(b),S=sf1111State(Q);if(Q.rage||Q.rf1110)return SF1111.base.start.apply(this,arguments);
 if(!type&&S.held&&Q.chrome&&Q.pendingArsenal)type='gun';
 if((type==='arsenal'||type==='gun')&&S.broken)return SF1111.base.start.call(this,b,'side');
 let A=SF1111.base.start.call(this,b,type);if(!A||Q.rf1110||Q.rage)return A;
 if(A.type==='arsenal'&&S.acquired)A=SF1111.base.start.call(this,b,'gun');
 if(A.type==='arsenal'||A.type==='gun'&&!S.acquired){A.type='sf1111_arsenal';A.tell=0;A.duration=4.72;Q._td1111Dir=Q._td1111From='center';Q.parts[2].destroyed=true;A.sf1111=true;sf1111Log('icon-box-approach',{hp:b.hp,gunHP:Q.gunHP});}
 else if(A.type==='gun'){A.sf1111=true;A.sf1111Equip=!S.held;A.duration=6.20;sf1111Log('gun-rev',{equipping:A.sf1111Equip,gunHP:Q.gunHP});}
 else if(A.type==='recall'&&Q.pendingRecall!=='rage'&&(S.acquired||S.broken)){A.sf1111=true;S.held=false;}
 return A;
};
function sf1111At(b,point){return{x:b.x+point[0]-256,y:b.y+point[1]-256};}
function sf1111Box(b){const Q=hb20State(b),a=sf1111Hammer(Q,22).a,box=SF1111_ART['icon-box'];return sf1111At(b,[a.tip[0],a.tip[1]+box.pivot[1]-box.meta[0].bounds[1]]);}
function sf1111Release(b,A){const Q=hb20State(b);A.sf1111Launch=rf1110HammerCentre(b,sf1111Hammer(Q,16).a);rd74Sound(A,'hammerThrow');sf1111Log('hammer-release',{...A.sf1111Launch});}
v19NativeTick=function(b,dt){if(!rd74Own(b))return SF1111.base.tick.apply(this,arguments);const Q=hb20State(b),S=sf1111State(Q),A=Q.action;if(Q.rf1110||Q.rage)return SF1111.base.tick.apply(this,arguments);
 if(A?.type==='gun'&&A.t+dt>=5)A.next=1e9;
 const r=SF1111.base.tick.apply(this,arguments);
 if(A&&A===Q.action){
  if(A.type==='sf1111_arsenal'){
   b.x=A.origin.x;b.y=A.origin.y;b._noHit=true;
   if(A.t>=1.78&&!A.sf1111Hit){A.sf1111Hit=true;rd74Sound(A,'hammerImpact');shake=Math.max(shake,5);sf1111Log('icon-box-hit',sf1111Box(b));}
   if(A.t>=2.46&&!A.sf1111Launch)sf1111Release(b,A);
   if(A.t>=3.06&&!A.sf1111Eject){A.sf1111Eject=true;sf1111Log('gun-eject',sf1111Box(b));}
   if(A.t>=3.54&&!S.acquired){S.acquired=S.held=true;rd74Sound(A,'weapon');sf1111Log('gun-catch',{hp:b.hp,gunHP:Q.gunHP});}
  }else if(A.type==='gun'){
   if(A.sf1111Equip&&A.t>=.38&&!A.sf1111Launch)sf1111Release(b,A);
   if(A.sf1111Equip&&A.t>=.60&&!S.held){S.held=true;rd74Sound(A,'weapon');sf1111Log('gun-re-equip',{gunHP:Q.gunHP});}
   if(A.t>=6.05)S.held=false;
  }
 }else if(A&&Q.action!==A){
  if(A.type==='sf1111_arsenal'){S.acquired=S.held=true;Q.cool=0;hb20Start(b,'gun');}
  else if(A.type==='sf1111_break'){S.held=false;Q.pendingRecall='gun';Q.cool=0;hb20Start(b,'recall');}
 }
 const live=Q.action,q=hb20Pose(b);Q.parts[2].destroyed=!(sf1111Held(Q)&&q?.a._sf1111&&q.a.gunSpans&&['gun','armor','sf1111_arsenal'].includes(live?.type));Q.parts[2].hp=Q.gunHP;Q.parts[1].destroyed=['gun','sf1111_arsenal','sf1111_break','recall'].includes(live?.type);return r;
};
v19HammerRig=function(b){if(!rd74Own(b))return SF1111.base.rig.apply(this,arguments);const Q=hb20State(b),A=Q.action,q=hb20Pose(b);if(!A||Q.rf1110||Q.rage||!['sf1111_arsenal','sf1111_break','gun','recall'].includes(A.type)&&!q?.a._sf1111)return SF1111.base.rig.apply(this,arguments);
 const core=b20Piece(Q.parts[0],q.a,b,0,1,'core',1);core._rd74=true;const out=[core];if(q.a.gunSpans&&sf1111Held(Q)&&!Q.parts[2].destroyed){const ga={...q.a,bounds:q.a.gunBounds,spans:q.a.gunSpans};const gun=b20Piece(Q.parts[2],ga,b,0,1,'chaingun',5);gun._rd74=true;gun._sf1111Gun=true;out.push(gun);}return out;
};
modularHit=function(dmg){const b=boss;if(!rd74Own(b))return SF1111.base.hit.apply(this,arguments);const Q=hb20State(b),S=sf1111State(Q),p=b._lastPart,before=Q.gunHP,r=SF1111.base.hit.apply(this,arguments);if(p===Q.parts[2]&&before>0&&Q.gunHP<=0&&!S.broken&&!Q.rage&&!Q.rf1110){S.broken=true;S.held=false;const A=Q.action;Q.action={type:'sf1111_break',t:0,tell:0,duration:.84,origin:{x:b.x,y:b.y},serial:++RD74.serial,next:0,hit:new Set(),hits:new Map(),bolts:[],n:0,sf1111:true};Q.pendingGun=Q.pendingArsenal=false;Q.parts[2].destroyed=true;sf1111Log('gun-broken',{hp:b.hp,previous:A?.type});}return r;};
function sf1111Tool(b,A,recall=false){const Q=hb20State(b),mat=rd74Mat(Q),to=rf1110HammerCentre(b,sf1111Hammer(Q,0).a);let at;if(recall){if(A.t>=.60)return;at={x:to.x,y:lerp(viewTopY()-180,to.y,v19Ease(A.t/.60))};}else{if(!A.sf1111Launch)return;const start=A.type==='gun'?.38:2.46,u=clamp((A.t-start)/.70,0,1);if(u>=1)return;at={x:A.sf1111Launch.x,y:lerp(A.sf1111Launch.y,viewTopY()-180,u)};}const q=rd74Sample('tool_'+mat,0),off=rd74Point({x:0,y:0},q);rd74Blit(q,at.x-off.x,at.y-off.y);}
v19DonorDraw=function(b){if(!rd74Own(b))return SF1111.base.draw.apply(this,arguments);const Q=hb20State(b),A=Q.action;if(!A||Q.rage||Q.rf1110)return SF1111.base.draw.apply(this,arguments);
 if(A.type==='recall'&&A.sf1111){const q=hb20Pose(b);q.a._sf1111?rd74Blit(q,b.x,b.y,b.flash>0):SF1111.base.blit(q,b.x,b.y,b.flash>0);sf1111Tool(b,A,true);return;}
 if(A.type==='sf1111_arsenal'){
  const q=hb20Pose(b);rd74Blit(q,b.x,b.y,b.flash>0);const box=sf1111Box(b),t=A.t,f=t<1.78?0:1+clamp((t-1.78)/.75,0,1)*7,drop=Math.max(0,t-3.06);sf1111Blit(sf1111Sample('icon-box',f),box.x,box.y+drop*drop*280);
  sf1111Tool(b,A);
  if(t>=3.06&&t<3.54){const u=v19Ease((t-3.06)/.48);sf1111Blit(sf1111Sample('gun-prop',0,rd74Mat(Q)),lerp(box.x,b.x,u),lerp(box.y,b.y+76,u));}return;
 }
 const r=SF1111.base.draw.apply(this,arguments);
 if(A.type==='gun'){
  if(A.sf1111Equip){sf1111Tool(b,A);if(A.t>=.38&&A.t<.60){const u=v19Ease((A.t-.38)/.22);sf1111Blit(sf1111Sample('gun-prop',0,rd74Mat(Q)),lerp(b.x-85,b.x,u),lerp(b.y+70,b.y+76,u));}}
  if(A.t<A.tell){const q=sf1111Sample('draconus-gun-spin',0,rd74Mat(Q)),m=rd74Point(b,q,'muzzle');b20Field(b,m,{x:m.x,y:VH+30},84,clamp(A.t/A.tell,0,1));bossShootGraphic(m.x,m.y+85);}
 }return r;
};
v18Clear=function(b){if(rd74Own(b)){const Q=hb20State(b);delete Q.sf1111;sf1111Log('cleanup');}return SF1111.base.clear.apply(this,arguments);};
globalThis.BOF_BOSS_SHIP_FORMS_1111=SF1111;
