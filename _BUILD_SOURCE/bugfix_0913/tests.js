// ===== 297. EXPOSED PELLETS, FINITE HELD LASERS AND THREE NUCLEAR IMPACTS =====
console.log('=== 297. Razorback and Tempest weapon geometry; Cole impact sound ===');
{
  var _pre297="ASSETS.ready=true;run.stage=1;curStage=STAGES[0];beginStage(1);setState(GS.PLAY);player.reset();player.invuln=999;stagePlan=[];waveIdx=0;boss=null;bossActive=false;bossTriggered=true;subBoss=null;subBossActive=false;subBossTriggered=true;aminiTriggered=true;enemies=[];eBullets=[];pBullets=[];powerups=[];special=null;playerLocks=[];spawnSubBoss('razorback');var b=subBoss,R=b._rzb;razorbackUpdate(b,0);b.x=worldWidth()/2;b.y=210;b.enter=false;R.state='guns';R.trans=0;R.a=Math.PI/2;R.tgt={x:b.x,y:b.y};R.speed=0;R.attack='sonic';R.at=0;subBossActive=true;";
  vm.runInContext(_pre297,ctxv);
  vm.runInContext("var hp=b.hp,shot={kind:'bullet',x:b.x,y:b.y,vx:0,vy:0,w:3,h:3,dmg:7,t:0};pBullets=[shot];updatePlay(1/60);",ctxv);
  ok(vm.runInContext("!shot.dead&&b.hp===hp&&subBossSolidAt(b.x,b.y)===false",ctxv),'a native pellet crossing sealed Razorback armor survives without changing HP');
  vm.runInContext(_pre297+"var q=rzbWorld(b,-57,96),before=R.pools.left,shot={kind:'bullet',x:q.x,y:q.y,vx:0,vy:0,w:3,h:3,dmg:7,t:0};pBullets=[shot];updatePlay(1/60);",ctxv);
  ok(vm.runInContext("shot.dead&&R.pools.left<before",ctxv),'a native pellet still damages and stops at the rotated exposed gun');
  vm.runInContext(_pre297+"R.pools.left=0;var q=rzbWorld(b,-57,96),hp=b.hp,shot={kind:'bullet',x:q.x,y:q.y,vx:0,vy:0,w:3,h:3,dmg:7,t:0};pBullets=[shot];updatePlay(1/60);",ctxv);
  ok(vm.runInContext("!shot.dead&&b.hp===hp&&subBossSolidAt(q.x,q.y)===false",ctxv),'a destroyed gun leaves no invisible pellet obstacle');
  vm.runInContext(_pre297+"R.state='turret';R.trans=1;var hp=b.hp,shot={kind:'bullet',x:b.x,y:b.y,vx:0,vy:0,w:3,h:3,dmg:7,t:0};pBullets=[shot];updatePlay(1/60);",ctxv);
  ok(vm.runInContext("!shot.dead&&b.hp===hp",ctxv),'invulnerable part transitions pass pellets instead of eating them');
  vm.runInContext("R.trans=0;R.state='turret';",ctxv);
  ok(vm.runInContext("subBossSolidAt(b.x,b.y)===true",ctxv),'the exposed turret remains targetable');
  vm.runInContext("R.state='hull';",ctxv);
  ok(vm.runInContext("subBossSolidAt(b.x,b.y)===true",ctxv),'the final exposed hull remains targetable');
  vm.runInContext(_pre297+"R.a=0;var q=rzbWorld(b,-57,96);player.x=q.x;player.y=430;var before=R.pools.left,old=updateSubBoss;updateSubBoss=function(){};pBullets=[{kind:'beam',x:player.x,w:2,dmg:7,life:.5,_hit:[],top:-20,bot:416}];try{updatePlay(1/60);}finally{updateSubBoss=old;}",ctxv);
  ok(vm.runInContext("R.pools.left<before",ctxv),'the actual held-beam update damages a gun away from the hull center');
  ok(vm.runInContext("razorbackBeamHit(b,{x:q.x+20,w:10,top:-20,bot:416}).key==='left'&&razorbackBeamHit(b,{x:q.x,w:2,top:-20,bot:q.y-20})===null",ctxv),'laser width reaches a gun edge while its finite endpoint excludes a gun beyond reach');
  vm.runInContext(_pre295+"s.boss.y=340;J.angle=Math.PI/2;D.ships[1]._ai.vulnerable=false;tempestBrothersSync(b);var q=tempestPortXY(p,2),beam={kind:'beam',x:q.x+8,w:2,top:-20,bot:416};",ctxv);
  ok(vm.runInContext("tempestBrothersBeamHit(b,beam).key==='B2'",ctxv),'a quarter-turn laser column reaches the physically rotated front aperture');
  vm.runInContext("var before=s.rig[2].hp,hp=s.hp,gray=D.ai.gray.hp;_dmgBullet=beam;hitSubBoss(7,b.x,b.y);_dmgBullet=null;",ctxv);
  ok(vm.runInContext("s.rig[2].hp<before&&s.hp===hp&&D.ai.gray.hp===gray",ctxv),'the real damage route consumes only the aperture intersected by the held laser');
  vm.runInContext("s.rig[2].hp=0;tempestBrothersSync(b);",ctxv);
  ok(vm.runInContext("tempestBrothersBeamHit(b,Object.assign({},beam,{top:p.y}))===null&&tempestBrothersBeamHit(b,Object.assign({},beam,{bot:p.y-100}))===null",ctxv),'silenced and out-of-range apertures cannot take phantom laser damage');
  vm.runInContext("s.boss.x=450;s.boss.y=340;s.vulnerable=true;J.angle=0;var g=D.ships[1];g._ai.boss.x=450;g._ai.boss.y=700;g._ai.vulnerable=true;g._jet.angle=0;tempestBrothersSync(b);var hit=tempestBrothersBeamHit(b,{x:p.x,w:2,top:-20,bot:296});",ctxv);
  ok(vm.runInContext("b.y>296&&hit&&hit.key==='Bhull'",ctxv),'the combined gauge center never hides a reachable brother or makes the farther hull hittable');
  vm.runInContext("var oldNow=window.performance.now,oldLast=Snd._last.nuclearDetonate,oldIndex=Snd.pools.nuclearDetonate.i,clock297=0;window.performance.now=function(){return clock297;};Snd._last.nuclearDetonate=null;var accepted297=[];for(var t of [0,1100,2200]){clock297=t;accepted297.push(Snd.play('nuclearDetonate'));}clock297=2250;var duplicate297=Snd.play('nuclearDetonate');window.performance.now=oldNow;Snd._last.nuclearDetonate=oldLast;Snd.pools.nuclearDetonate.i=oldIndex;",ctxv);
  ok(vm.runInContext("accepted297.every(Boolean)",ctxv),'three separate nuclear impact events each receive a sound voice');
  ok(vm.runInContext("duplicate297===false",ctxv),'the nuclear impact route still throttles a same-frame duplicate');
  vm.runInContext("subBoss=null;subBossActive=false;subBossDone=false;eBullets=[];pBullets=[];playerLocks=[];_dmgBullet=null;",ctxv);
}
