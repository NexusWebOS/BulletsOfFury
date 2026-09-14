// ===== 304. RETINA COMPONENT TARGETS, 0914 =====
console.log('=== 304. Retina component targets ===');
{
 var rt304=JSON.parse(vm.runInContext(`(function(){
  var old={boss,subBoss,bossActive,subBossActive,enemies,retina,runBombs:run.bombs},o={};
  enemies=[];subBoss=null;subBossActive=false;bossActive=true;
  boss={_ship:'doomsdaycarriermk2',x:240,y:160,w:300,h:200,hp:1000,maxhp:1000,dead:false,enter:false,_bay:{L:10,R:10},_bayShield:{up:true},_mega:{phase:2,nodes:[{id:'L1',ox:-.3,oy:.1,hp:60,maxhp:60,dead:false}]}};
  var n=boss._mega.nodes[0],t=_lockTargets()[0];o.shieldedHullExcluded=_lockTargets().indexOf(boss)<0;o.nodePresent=t&&t.part===n;
  var same=t;boss.x+=30;o.follows=t.x===boss.x+boss.w*n.ox&&_lockTargets()[0]===same;
  retinaMissileDamage(t,7,{x:t.x,y:t.y});o.nodeDamage=n.hp===53&&boss.hp===1000;
  boss._bayShield.up=false;var bays=_lockTargets().filter(t=>t.kind==='missile bay');o.bays=bays.length===2&&_lockTargets().indexOf(boss)<0;
  retinaMissileDamage(bays[0],3,{x:bays[0].x,y:bays[0].y});o.bayDamage=boss._bay.L===7&&boss._bay.R===10;
  boss._bay.L=0;boss._bay.R=0;o.exposed=_lockTargets().indexOf(boss)>=0;
  retina={target:boss,phase:'locked',lockT:5};boss._bayShield.up=true;updateRetina(.01);o.reformClears=!retina.target&&!retina.phase;
  n.dead=true;o.deadNodeRemoved=_lockTargets().indexOf(t)<0;
  boss={x:240,y:160,w:200,h:200,hp:100,maxhp:100,dead:false,enter:false,_s4war:{coreUnlocked:true,coreTurrets:[{x:60,y:90,hp:100,dead:false,materialize:1}],shield:{active:true,rearming:false,nodes:[{id:'L',x:70,y:160,hp:30,dead:false}]}}};
  var list=_lockTargets();o.stage4=list.length===2&&list.some(t=>t.kind==='electrical node')&&list.some(t=>t.kind==='helper')&&list.indexOf(boss)<0;
  o.space=spaceTargets().length===2&&spaceTargets().indexOf(boss)<0;
  boss=old.boss;subBoss=old.subBoss;bossActive=old.bossActive;subBossActive=old.subBossActive;enemies=old.enemies;retina=old.retina;run.bombs=old.runBombs;return JSON.stringify(o);
 })()`,ctxv));
 for(var k of Object.keys(rt304))ok(rt304[k],'Retina component eligibility and damage: '+k);
}
