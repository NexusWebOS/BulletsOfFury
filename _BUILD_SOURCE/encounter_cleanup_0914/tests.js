// ===== 300. READABLE ATTACKS AND SHARED WARNINGS, 0914 =====
console.log('=== 300. readable attacks and shared warnings ===');
{
  var jet300=JSON.parse(vm.runInContext(`(function(){
    run.stage=1;curStage=STAGES[0];beginStage(1);state=GS.PLAY;player.reset();player.dead=false;player.x=worldWidth()/2;player.y=420;eBullets=[];
    var e=spawnEnemy('s1jetdelta',player.x,120,{route:'straight'});e.ghost=false;e.enter=false;e._s1DelayFrames=0;e._stagger=0;
    var generic=enemyVolley(e,true);enemyVolleyTick(e,3);var extras=eBullets.length;
    e._jet=1;e._jspd=96;e._lane=e.x;e._burst=1;e._shotCd=0;e._dodge=0;e._fmul=1;jetTick(e,1/60);
    return JSON.stringify({generic:generic,extras:extras,shots:eBullets.map(q=>({kind:q.kind,vx:q.vx,vy:q.vy}))});
  })()`,ctxv));
  ok(!jet300.generic&&jet300.extras===0,'armed stage-1 jet cannot fire a second generic fan/rake/salvo channel');
  ok(jet300.shots.length===2&&jet300.shots.every(q=>q.kind==='s1bullet'&&Math.abs(q.vx)<1e-8&&q.vy>0),'the same jet retains its real straight twin nose guns');
  var head300=JSON.parse(vm.runInContext(`(function(){
    var F={at:1.0,t:2,a:0,eye:{'-1':.15,'1':-.10},attack:'eyeStab',dir:1,shotBeat:-1,tells:[],beams:[]},b={x:240,y:100,_fz:F};
    player.x=60;player.y=430;furnaceHeadCombat(b,.016);var warm=F.beams.length,eyes=[F.eye[-1],F.eye[1]],pose=[b.x,b.y];
    player.x=440;F.at=1.7;furnaceHeadCombat(b,.016);
    return JSON.stringify({warm:warm,eyes:eyes,after:[F.eye[-1],F.eye[1]],pose:pose,afterPose:[b.x,b.y],beams:F.beams.length});
  })()`,ctxv));
  ok(head300.warm===0&&head300.beams===2,'Furnace head charge is harmless and releases only after its longer warning');
  ok(head300.eyes.join()===head300.after.join()&&head300.pose.join()===head300.afterPose.join(),'moving across the arena after commitment cannot drag a firing head laser or its origin after the player');
  var impacts300=JSON.parse(vm.runInContext(`(function(){
    pBullets=[];var old=explosions.length;
    for(var i=0;i<100;i++){var b={x:60+i%10*32,y:200+Math.floor(i/10)*32};pBullets.push(b);spaceImpact(b,'volley',5,80);}
    return JSON.stringify({visible:pBullets.filter(q=>!q._quietVisual).length,quiet:pBullets.filter(q=>q._quietVisual).length,explosions:explosions.length-old,max:Math.max.apply(null,pBullets.map(q=>q.w))});
  })()`,ctxv));
  ok(impacts300.visible===6&&impacts300.quiet===94,'one hundred simultaneous space impacts retain at most six independent decorations');
  ok(impacts300.explosions===0&&impacts300.max===40,'high-tier Volley hits cannot stack generic explosions or inflate into opaque screen-sized blasts');
  var flame300=JSON.parse(vm.runInContext(`(function(){
    var old=flameIsIce;flameIsIce=function(){return false;};var base=flameHalfW(3,1),f={top:100,bot:300},out={width:flameHalfWDrawn(3),base:base,tip:flameSpanTop(f)};
    flameIsIce=function(){return true;};out.iceWidth=flameHalfWDrawn(3);out.iceTip=flameSpanTop(f);flameIsIce=old;return JSON.stringify(out);
  })()`,ctxv));
  ok(flame300.width===flame300.base*.75&&flame300.tip===150,'player flame shrinks 25 percent in both dimensions while keeping its nozzle at the plane');
  ok(flame300.iceWidth===flame300.base*.85&&flame300.iceTip===120,'the separate Ice Breath retains its own authored scale');
  var pause300=vm.runInContext(`(function(){var tap=Input.tap,p=pauseTapped;Input.tap=function(k){return k==='backspace';};pauseTapped=function(){return false;};state='paused';drawPaused();var out=state;Input.tap=tap;pauseTapped=p;state=GS.PLAY;return out;})()`,ctxv);
  ok(pause300==='paused','Backspace while paused cannot abandon the level or return to the title');
  vm.runInContext('enemies=[];eBullets=[];pBullets=[];boss=null;subBoss=null;bossActive=false;subBossActive=false;Snd.loopStopAll();',ctxv);
}
