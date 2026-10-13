/* Four new authored armor families, with different weapons and movement roles. */
(function(root){
  'use strict';const TD=root.TD,M=TD.M,FX=TD.FX,art=TD.AssaultArt,A=TD.Audio;
  const defs={jackal:{hp:10,speed:1.9,r:25,gun:'burst',cd:1.4,prefer:[110,210],score:650,ds:.34},lancer:{hp:17,speed:1.1,r:29,gun:'snipe',cd:2.8,warn:.55,prefer:[220,310],score:1100,ds:.37},manticore:{hp:23,speed:.95,r:30,gun:'rocket',cd:3.6,prefer:[190,270],score:1250,ds:.38},bastion:{hp:38,speed:.62,r:39,gun:'twin',cd:2.6,prefer:[130,230],score:1800,ds:.45}};
  for(const [name,def]of Object.entries(defs))TD.ET[name]=Object.assign({odTank:name,art:'od_'+name+'_0',wreck:'od_'+name+'_3',vis:{range:330,half:.7}},def);
  const draw=TD.drawUnit,hit=TD.hitUnit,tick=TD.unitTick;
  TD.drawUnit=function(ctx,u){const d=TD.ET[u.type];if(!d.odTank)return draw(ctx,u);if(u.dead)return;const k='od_'+d.odTank+'_'+(u.burst>0||u.fireCd>d.cd-.13?2:Math.floor((u.armorTravel||0)/8)%2);art.draw(ctx,k,u.x+4,u.y+5,{s:d.ds,a:u.a+Math.PI,tint:'#000000',alpha:.35});art.draw(ctx,k,u.x,u.y,{s:d.ds,a:u.a+Math.PI,flash:u.flash>0?1:0});};
  TD.unitTick=function(u,G,dt){const x=u.x,y=u.y;tick(u,G,dt);if(TD.ET[u.type].odTank)u.armorTravel=(u.armorTravel||0)+Math.hypot(u.x-x,u.y-y);};
  TD.hitUnit=function(G,u,dmg,x,y,silent){const was=u.dead;hit(G,u,dmg,x,y,silent);const t=TD.ET[u.type];if(!was&&u.dead&&t.odTank){const w=G.wrecks.at(-1);if(w&&w.x===u.x&&w.y===u.y){w.art=t.wreck;w.still=true;w.s=t.ds;}FX.concrete(u.x,u.y,80);A.play('expBoss',.35);}};
  // The existing tank missions retain their encounter order and now mix the new armor.
  for(const m of TD.MISSIONS.filter(m=>m.mode==='tank')){
    const replacements=m.id===2?['jackal','lancer','manticore','bastion']:['manticore','jackal','lancer','bastion'];let i=0;
    for(const u of m.data.units)if(!['camera','turret'].includes(u.type)&&i<4)u.type=replacements[i++];
  }
})(window);
