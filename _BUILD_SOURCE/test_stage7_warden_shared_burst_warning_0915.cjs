module.exports=function testStage7WardenSharedBurstWarning(vm,ctxv,ok){
  console.log('=== 337. Toxic Portal Warden shared cannon-burst warning ===');
  const result=JSON.parse(vm.runInContext(`(function(){
    const save={boss,player,run:{...run},camX,curStage,eBullets,shoot:Audio.SFX.enemyBossCannon};const o={};
    try{
      Audio.SFX.enemyBossCannon=()=>{};camX=0;curStage=STAGES[6];run.stage=7;eBullets=[];
      player={x:360,y:400,dead:false,invuln:999,_hx:9,_hy:10};
      boss={x:240,y:178,w:300,h:230,hp:5000,maxhp:5000,dead:false,flash:0,fireCd:999};s7WardenInit(boss);
      boss._s7warden.final.phase='fight';boss._s7warden.noHit=false;s7WardenMode(boss,'burst');const S=boss._s7warden,aim=S.aim,angles=s7WardenBurstAngles(S);
      o.commits=Number.isFinite(aim)&&angles.length===5&&boss._combatWarnings['stage7-warden-burst'].t===0;
      S.mt=.08;s7WardenTick(boss,0);let B=boss._combatWarnings['stage7-warden-burst'];o.green=l23FovPhase(B.t/B.warm)==='green';
      player.x=40;S.mt=.24;s7WardenTick(boss,0);B=boss._combatWarnings['stage7-warden-burst'];o.yellow=l23FovPhase(B.t/B.warm)==='yellow'&&S.aim===aim;
      player.x=230;S.mt=.432;s7WardenTick(boss,0);B=boss._combatWarnings['stage7-warden-burst'];o.red=l23FovPhase(B.t/B.warm)==='red'&&S.aim===aim;
      S.mt=.49;s7WardenTick(boss,0);B=boss._combatWarnings['stage7-warden-burst'];o.release=B.released&&S.shot===1&&eBullets.filter(q=>q._s7warden==='shell').length===1;
      S.mt=1.44;s7WardenTick(boss,0);const shells=eBullets.filter(q=>q._s7warden==='shell'),shotAngles=shells.map(q=>Math.atan2(q.vy,q.vx));o.pattern=shells.length===10&&shotAngles.every((a,i)=>Math.abs(a-angles[i%5])<.0001);
      const draw=s7WardenBurstWarningDraw.toString(),body=s7WardenDraw.toString(),final=s7WardenFinalTick.toString();o.shared=draw.includes('fieldOnly:true')&&draw.includes('alertOnly:true')&&body.includes('s7WardenBurstWarningDraw(b,false)')&&body.includes('s7WardenBurstWarningDraw(b,true)')&&final.split('s7WardenBurstArm(b)').length===3;
      return JSON.stringify(o);
    }finally{boss=save.boss;player=save.player;Object.assign(run,save.run);camX=save.camX;curStage=save.curStage;eBullets=save.eBullets;Audio.SFX.enemyBossCannon=save.shoot;}
  })()`,ctxv));
  for(const k of Object.keys(result))ok(result[k],'Toxic Warden burst warning: '+k);
};
