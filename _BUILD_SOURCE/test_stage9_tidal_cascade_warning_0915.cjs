module.exports=function testStage9TidalCascadeWarning(vm,ctxv,ok){
  console.log('=== 340. Stage-9 Tidal Cascade shared row warnings ===');
  const result=JSON.parse(vm.runInContext(`(function(){
    const save={boss,player,run:{...run},camX,curStage,eBullets};const o={};
    try{
      camX=0;curStage=STAGES[8];run.stage=9;eBullets=[];player={x:360,y:400,dead:false,invuln:999,_hx:9,_hy:10};
      boss={x:240,y:126,_drawY:126,w:250,h:180,hp:500,maxhp:500,dead:false,flash:0,fireCd:0,_combatWarnings:{},_ship:'tidalsovereign'};
      tidalCascadeStart(boss,1);const T=boss._s9Cascade,gap=T.gap;o.start=!!T&&T.rowTell===.62&&T.next===.62&&eBullets.length===0;
      tidalCascadeTick(boss,.10);let B=boss._combatWarnings['stage9-tidal-cascade-0'];o.green=l23FovPhase(B.t/B.warm)==='green';
      tidalCascadeTick(boss,.22);B=boss._combatWarnings['stage9-tidal-cascade-0'];o.yellow=l23FovPhase(B.t/B.warm)==='yellow';
      player.x=40;tidalCascadeTick(boss,.24);B=boss._combatWarnings['stage9-tidal-cascade-0'];o.red=l23FovPhase(B.t/B.warm)==='red'&&T.gap===gap;
      tidalCascadeTick(boss,.07);const first=eBullets.filter(q=>q.kind==='s9pair');o.release=B.released&&first.length===6&&first.every(q=>Math.abs(q.vx)<.0001&&q.vy>0);
      const nextGap=T.gap;o.nextRow=T.wave===1&&nextGap===gap+1&&T.next===T.warnAt+T.rowTell&&!!boss._combatWarnings['stage9-tidal-cascade-1'];
      const before=eBullets.length;tidalCascadeTick(boss,.61);o.noEarlySecond=eBullets.length===before&&T.gap===nextGap;
      tidalCascadeTick(boss,.02);o.secondRelease=T.wave===2&&eBullets.filter(q=>q.kind==='s9pair').length===12;
      const draw=tidalCascadeDraw.toString();o.shared=draw.includes('fieldOnly:true')&&draw.includes('alertOnly:true')&&!draw.includes('#39caff')&&!draw.includes('#d4ffff');
      return JSON.stringify(o);
    }finally{boss=save.boss;player=save.player;Object.assign(run,save.run);camX=save.camX;curStage=save.curStage;eBullets=save.eBullets;}
  })()`,ctxv));
  for(const k of Object.keys(result))ok(result[k],'Tidal Cascade warning: '+k);
};
