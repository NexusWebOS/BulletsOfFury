"use strict";
// Native squad scheduling: do not let a repeating formation starve personal books.
const RD42={attack:rg4Attack,events:[]};
rg4Attack=function(q,R,G,forced){
 if(forced||!rr33Group(boss)||G.scene)return RD42.attack.apply(this,arguments);
 if(G.rd21?.fleet||R.ships.some(s=>rd21Live(s)&&(rbal19Heavy(s)||s.rg4?.act&&s.rg4.act.phase!=='recover'))){q.rg4.cd=Math.max(.15,q.rg4.cd);return;}
 const ready=R.ships.filter(s=>rd21Live(s)&&s.rg4&&!s.rg4.act&&s.stun<=0&&s.rg4.cd<=0);
 ready.sort((a,b)=>(a.rg4._rd42Turn||0)-(b.rg4._rd42Turn||0)||a.rg4.cd-b.rg4.cd||a.i-b.i);
 const pilot=ready[0]||q,before=pilot.rg4.act,result=RD42.attack.call(this,pilot,R,G);
 if(pilot.rg4.act&&pilot.rg4.act!==before){
  pilot.rg4._rd42Turn=G._rd42Turn=(G._rd42Turn||0)+1;
  RD42.events.push({pilot:pilot.key,kind:pilot.rg4.act.kind,time:G.age,turn:G._rd42Turn});
  if(RD42.events.length>150)RD42.events.shift();
 }
 return result;
};
