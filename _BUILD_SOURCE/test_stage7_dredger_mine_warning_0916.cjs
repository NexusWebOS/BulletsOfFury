module.exports=function testStage7DredgerMineWarning(vm,ctxv,ok){
  console.log('=== 343. Stage-7 Dredger shared mine warning ===');
  const result=JSON.parse(vm.runInContext(`(function(){
    const save={boss,subBoss,player,run:{...run},camX,curStage,eBullets,shake};const o={};
    try{
      camX=0;curStage=STAGES[6];run.stage=7;eBullets=[];shake=0;player={x:360,y:420,dead:false,invuln:999,_hx:9,_hy:10};
      const b={x:240,y:126,_drawY:126,w:240,h:220,hp:72,maxhp:360,dead:false,flash:0,fireCd:0,_combatWarnings:{},_ship:'dualscoopdredger'};boss=b;subBoss=b;
      s7DredgerAttack(b,4);const M=b._s7DredgerMine,gap=M.gap,targets=s7DredgerMineTargets(M),W=worldWidth();
      o.start=!!M&&M.warn===.86&&M.cols===6&&gap===clamp(Math.floor(360/(W/6)),0,5)&&targets.length===5&&eBullets.length===0;
      s7DredgerMineTick(b,.10);let B=b._combatWarnings['stage7-dredger-minefield'];o.green=l23FovPhase(B.t/B.warm)==='green'&&eBullets.length===0;
      player.x=40;s7DredgerMineTick(b,.34);B=b._combatWarnings['stage7-dredger-minefield'];o.yellow=l23FovPhase(B.t/B.warm)==='yellow'&&M.gap===gap&&eBullets.length===0;
      player.x=230;s7DredgerMineTick(b,.32);B=b._combatWarnings['stage7-dredger-minefield'];o.red=l23FovPhase(B.t/B.warm)==='red'&&M.gap===gap&&eBullets.length===0;
      s7DredgerMineTick(b,.09);o.noEarly=eBullets.length===0&&!M.released;
      const C=shipBossMount(b,'C');s7DredgerMineTick(b,.02);B=b._combatWarnings['stage7-dredger-minefield'];const mines=eBullets.filter(q=>q._s7warden==='mine');
      o.release=B.released&&M.released&&mines.length===5&&shake===6;
      o.paths=mines.every((q,i)=>Math.abs(Math.atan2(q.vy,q.vx)-Math.atan2(targets[i].y-C.y,targets[i].x-C.x))<1e-8)&&!targets.some(q=>q.index===gap);
      const draw=s7DredgerMineDraw.toString(),body=shipBossDraw.toString(),queue=shipBossQueueAttack.toString();
      o.shared=draw.includes('fieldOnly:true')&&draw.includes('alertOnly:true')&&body.includes('s7DredgerMineDraw(b,false)')&&body.includes('s7DredgerMineDraw(b,true)');
      o.ownsChannel=queue.includes('b._s7DredgerMine')&&s7DredgerAttack.toString().includes('s7DredgerMineStart(b)');
      s7DredgerMineTick(b,.46);o.cleanup=!b._s7DredgerMine&&b.fireCd===.56;
      return JSON.stringify(o);
    }finally{boss=save.boss;subBoss=save.subBoss;player=save.player;Object.assign(run,save.run);camX=save.camX;curStage=save.curStage;eBullets=save.eBullets;shake=save.shake;}
  })()`,ctxv));
  for(const k of Object.keys(result))ok(result[k],'Dredger mine warning: '+k);
};
