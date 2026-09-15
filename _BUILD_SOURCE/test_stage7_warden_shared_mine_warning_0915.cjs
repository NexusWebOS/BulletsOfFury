module.exports=function testStage7WardenSharedMineWarning(vm,ctxv,ok){
  console.log('=== 336. Toxic Portal Warden shared minefield warning ===');
  const result=JSON.parse(vm.runInContext(`(function(){
    const save={boss,player,run:{...run},camX,curStage,eBullets,shoot:Audio.SFX.enemyBossCannon};const o={};
    try{
      Audio.SFX.enemyBossCannon=()=>{};camX=0;curStage=STAGES[6];run.stage=7;eBullets=[];
      player={x:360,y:400,dead:false,invuln:999,_hx:9,_hy:10};
      boss={x:240,y:178,w:300,h:230,hp:5000,maxhp:5000,dead:false,flash:0,fireCd:999};s7WardenInit(boss);
      boss._s7warden.final.phase='fight';boss._s7warden.noHit=false;s7WardenMode(boss,'minefield');const S=boss._s7warden,gap=S.mineGap,targets=s7WardenMineTargets(S);
      const expectedGap=clamp(Math.floor(player.x/(worldWidth()/7)),1,5);
      o.commits=gap===expectedGap&&targets.length===6&&!targets.some(q=>q.index===gap);
      S.mt=.12;s7WardenTick(boss,0);let B=boss._combatWarnings['stage7-warden-minefield'];o.green=l23FovPhase(B.t/B.warm)==='green';
      player.x=40;S.mt=.36;s7WardenTick(boss,0);B=boss._combatWarnings['stage7-warden-minefield'];o.yellow=l23FovPhase(B.t/B.warm)==='yellow'&&S.mineGap===gap;
      player.x=230;S.mt=.648;s7WardenTick(boss,0);B=boss._combatWarnings['stage7-warden-minefield'];o.red=l23FovPhase(B.t/B.warm)==='red'&&S.mineGap===gap;
      S.mt=.73;s7WardenTick(boss,0);B=boss._combatWarnings['stage7-warden-minefield'];const mines=eBullets.filter(q=>q._s7warden==='mine'),W=worldWidth();
      o.release=B.released&&S.event===1&&mines.length===6;
      const xs=mines.map(q=>q._wardenAnchor.x),expected=targets.map(q=>q.x);o.targets=expected.every((x,i)=>Math.abs(xs[i]-x)<.001)&&!xs.some(x=>Math.abs(x-(gap+.5)*W/7)<.001);
      const draw=s7WardenMineWarningDraw.toString(),body=s7WardenDraw.toString();o.shared=draw.includes('fieldOnly:true')&&draw.includes('alertOnly:true')&&body.includes('s7WardenMineWarningDraw(b,false)')&&body.includes('s7WardenMineWarningDraw(b,true)');
      return JSON.stringify(o);
    }finally{boss=save.boss;player=save.player;Object.assign(run,save.run);camX=save.camX;curStage=save.curStage;eBullets=save.eBullets;Audio.SFX.enemyBossCannon=save.shoot;}
  })()`,ctxv));
  for(const k of Object.keys(result))ok(result[k],'Toxic Warden mine warning: '+k);
};
