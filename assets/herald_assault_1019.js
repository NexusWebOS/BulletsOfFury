"use strict";
/* Herald keeps its taught opening and eclipse cross. Living modules then rake
   committed lanes; losing the weapons exposes a mobile head/core last stand. */
const HD19={events:[],base:{tell:hd1003Tell,tick:hd1003Tick},cfg:[
 {warm:1.42,recover:1.20,rake:2,lance:1,gap:.94,head:2,speed:70},
 {warm:1.22,recover:.90,rake:3,lance:2,gap:.90,head:2,speed:95},
 {warm:1.06,recover:.72,rake:4,lance:2,gap:.82,head:3,speed:120},
 {warm:.94,recover:.58,rake:5,lance:3,gap:.76,head:4,speed:145},
 {warm:.90,recover:.54,rake:5,lance:3,gap:.72,head:4,speed:150}]};
function hd19Cfg(){return HD19.cfg[target17Rank()];}
function hd19Disarmed(b){return !!b?._hd1003&&b._hd1003.parts.filter(p=>!['head','core'].includes(p.id)).every(p=>p.dead||p.hp<=0);}
function hd19Log(event,b,data={}){HD19.events.push({event,time:b._hd1003.clock,...data});if(HD19.events.length>160)HD19.events.shift();}
function hd19Start(b,kind){const H=b._hd1003,C=hd19Cfg(),T=targetShip(b.x,b.y),rank=Math.min(2,Math.max(0,target17Rank()-1));
 H.seq++;H.mode='tell';H.age=0;H.attackAge=0;H.shots=0;H.rank=rank;H.warm=C.warm;H.target={x:T.x,y:T.y};H.lanes=[];H.flashes=[];
 const core=kind==='core-fury'||kind==='core-lance';
 H._hd19={kind,from:{x:b.x,y:b.y},released:0};H.attack=kind==='wing-rake'||kind==='core-lance'?'lances':'skulls';
 const ids=core?['head','core']:kind==='wing-rake'?['wingL','wingR']:['gunL','gunR'];
 const live=ids.filter(id=>hd1003Live(b,hd1003Part(b,id))),waves=kind==='core-fury'?C.head:kind==='core-lance'?(rank>1?2:1):kind==='wing-rake'?C.lance:C.rake;
 if(!live.length){H._hd19=null;return hd19Start(b,'core-fury');}
 for(let wave=0;wave<waves;wave++)for(let n=0;n<(core?1:live.length);n++){
  const id=live[(n+(core?wave:0)+(H.seq%2))%live.length],P=hd1003Muzzle(b,id),offset=kind==='wing-rake'?(wave-(waves-1)/2)*.22:kind==='core-fury'?0:core?(wave-(waves-1)/2)*.12:(wave-(waves-1)/2)*.095;
  const a=Math.atan2(T.y-P.y,T.x-P.x)+offset,len=VH*1.3,gap=kind==='wing-rake'?C.gap:kind==='core-fury'?.48:.40;
  H.lanes.push({x:P.x,y:P.y,ex:P.x+Math.cos(a)*len,ey:P.y+Math.sin(a)*len,width:H.attack==='lances'?15:44,id,aim:a,
   tx:T.x,ty:T.y,delay:wave*gap+n*(kind==='wing-rake'?.18:.20),issued:false});
 }
 H.history.push(kind);if(H.history.length>30)H.history.shift();r30Sound('bossWeaponCharge');hd19Log('attack-tell',b,{kind,warm:H.warm,lanes:H.lanes.length});
}
hd1003Tell=function(b){const H=b._hd1003;
 if(hd19Disarmed(b))return hd19Start(b,H.seq%3===1?'core-lance':'core-fury');
 if(H.seq<3){H._hd19=null;return HD19.base.tell.apply(this,arguments);}
 const book=['cannon-rake','wing-rake','eclipse-cross','cannon-rake','head-salvo','wing-rake'],kind=book[(H.seq-3)%book.length];
 if(kind==='eclipse-cross'&&H.parts.some(p=>p.id.startsWith('wing')&&!p.dead)){
  const seq=H.seq;H.seq=3;H._hd19=null;const r=HD19.base.tell.call(this,b);H.seq=seq+1;return r;
 }
 if(kind==='head-salvo'){H._hd19=null;const seq=H.seq;H.seq=2;const r=HD19.base.tell.call(this,b);H.seq=seq+1;return r;}
 if(kind==='wing-rake'&&H.parts.some(p=>p.id.startsWith('wing')&&!p.dead))return hd19Start(b,kind);
 if(H.parts.some(p=>p.id.startsWith('gun')&&!p.dead))return hd19Start(b,'cannon-rake');
 return hd19Start(b,'core-fury');
};
hd1003Tick=function(b,dt){const H=b._hd1003,C=hd19Cfg();
 if(!b.dead&&hd19Disarmed(b)&&!H._hd19&&H.mode!=='rest'){
  S81003.beams=S81003.beams.filter(q=>q.owner!==b);if(b._hc1007)b._hc1007.cross=null;H.mode='rest';H.age=0;H.lanes=[];
 }
 if(!H._hd19){const was=H.mode,r=HD19.base.tick.apply(this,arguments);
  if(H.mode==='rest'){
   const span=hd19Disarmed(b)?Math.min(115,viewW()*.24):Math.min(105,viewW()*.22),tx=clamp(camLeftX()+viewW()/2+Math.sin(H.clock*.92)*span,camLeftX()+b.w*.40,camRightX()-b.w*.40);
   b.x+=clamp(tx-b.x,-C.speed*dt,C.speed*dt);b._drawY=b.y;
   if(was!=='rest')H.age=Math.max(H.age,1.05-C.recover);
  }return r;
 }
 const P=H._hd19;H.clock+=dt;H.age+=dt;H.attackAge+=dt;b.fireCd=999;b._sba=null;b._drawY=b.y;
 const live=H.lanes.filter(L=>hd1003Live(b,hd1003Part(b,L.id)));H.lanes=live;
 if(!live.length){H._hd19=null;H.mode='rest';H.age=0;return true;}
 for(let i=0;i<live.length;i++){const L=live[i];if(!L.issued&&H.attackAge>=L.delay)combatWarningTick(b,'hd19-'+H.seq+'-'+i,Math.min(H.warm,H.attackAge-L.delay),H.warm);
  if(!L.issued&&H.attackAge+1e-8>=H.warm+L.delay){hd1003Release(b,L);P.released++;hd19Log('module-release',b,{kind:P.kind,part:L.id,angle:L.aim});}}
 if(H.attackAge>=H.warm)H.mode='fire';
 const last=Math.max(...live.map(L=>L.delay));if(H.attackAge>H.warm+last+(H.attack==='lances'?.70:.36)){
  H._hd19=null;H.mode='rest';H.age=1.05-C.recover;H.lanes=[];hd19Log('recovery',b,{kind:P.kind,seconds:C.recover});}
 return true;
};
window.BOF_HERALD_ASSAULT={state:HD19,disarmed:hd19Disarmed,cfg:hd19Cfg};
