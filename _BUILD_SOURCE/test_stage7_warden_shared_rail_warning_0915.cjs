module.exports=function testStage7WardenSharedRailWarning(vm,ctxv,ok){
  console.log('=== 335. Toxic Portal Warden shared rail warning ===');
  const result=JSON.parse(vm.runInContext(`(function(){
    const save={boss,player,run:{...run},camX,curStage,eBullets,shoot:Audio.SFX.enemyHeavyLaser};const o={};
    try{
      Audio.SFX.enemyHeavyLaser=()=>{};camX=0;curStage=STAGES[6];run.stage=7;eBullets=[];
      player={x:360,y:400,dead:false,invuln:999,_hx:9,_hy:10};
      boss={x:240,y:178,w:300,h:230,hp:5000,maxhp:5000,dead:false,flash:0,fireCd:999};s7WardenInit(boss);
      boss._s7warden.final.phase='fight';boss._s7warden.noHit=false;s7WardenMode(boss,'rail');const S=boss._s7warden,aim=S.railAim,safe=S.railSafe;
      o.commits=Number.isFinite(aim)&&safe===1&&s7WardenRailAngles(S).length===5;
      S.mt=.15;s7WardenTick(boss,0);let B=boss._combatWarnings['stage7-warden-rail'];o.green=l23FovPhase(B.t/B.warm)==='green';
      player.x=60;S.mt=.43;s7WardenTick(boss,0);B=boss._combatWarnings['stage7-warden-rail'];o.yellow=l23FovPhase(B.t/B.warm)==='yellow'&&S.railAim===aim&&S.railSafe===safe;
      player.x=430;S.mt=.774;s7WardenTick(boss,0);B=boss._combatWarnings['stage7-warden-rail'];o.red=l23FovPhase(B.t/B.warm)==='red'&&S.railAim===aim&&S.railSafe===safe;
      S.mt=.87;s7WardenTick(boss,0);B=boss._combatWarnings['stage7-warden-rail'];const shots=eBullets.filter(q=>q._s7warden==='rail');
      o.release=B.released&&S.event===1&&shots.length===5;
      const expected=s7WardenRailAngles(S),actual=shots.map(q=>Math.atan2(q.vy,q.vx));o.angles=actual.every((a,i)=>Math.abs(Math.atan2(Math.sin(a-expected[i]),Math.cos(a-expected[i])))<.0001);
      const draw=s7WardenRailWarningDraw.toString(),body=s7WardenDraw.toString();o.shared=draw.includes('fieldOnly:true')&&draw.includes('alertOnly:true')&&body.includes('s7WardenRailWarningDraw(b,false)')&&body.includes('s7WardenRailWarningDraw(b,true)')&&s7WardenTick.toString().includes("combatWarningTick(b,'stage7-warden-rail'");
      return JSON.stringify(o);
    }finally{boss=save.boss;player=save.player;Object.assign(run,save.run);camX=save.camX;curStage=save.curStage;eBullets=save.eBullets;Audio.SFX.enemyHeavyLaser=save.shoot;}
  })()`,ctxv));
  for(const k of Object.keys(result))ok(result[k],'Toxic Warden rail warning: '+k);
};
