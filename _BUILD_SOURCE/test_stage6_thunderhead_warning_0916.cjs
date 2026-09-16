module.exports=function testStage6ThunderheadWarning(vm,ctxv,ok){
  console.log('=== 341. Stage-6 Thunderhead shared row warnings ===');
  const result=JSON.parse(vm.runInContext(`(function(){
    const save={boss,player,run:{...run},camX,curStage,eBullets};const o={};
    try{
      camX=0;curStage=STAGES[5];run.stage=6;eBullets=[];player={x:180,y:400,dead:false,invuln:999,_hx:9,_hy:10};
      boss=null;spawnBoss('doomsdaycarriermk2');boss.enter=false;carrierMegaInit(boss);boss._mega.phase=1;boss._combatWarnings={};
      carrierThunderheadStart(boss);const T=boss._mega.thunderhead,gap=T.gap;o.start=!!T&&T.rowTell===.66&&T.next===.66&&T.warnAt===0&&eBullets.length===0;
      carrierThunderheadTick(boss,.10);let B=boss._combatWarnings['stage6-thunderhead-0'];o.green=l23FovPhase(B.t/B.warm)==='green';
      carrierThunderheadTick(boss,.24);B=boss._combatWarnings['stage6-thunderhead-0'];o.yellow=l23FovPhase(B.t/B.warm)==='yellow';
      player.x=440;carrierThunderheadTick(boss,.23);B=boss._combatWarnings['stage6-thunderhead-0'];o.red=l23FovPhase(B.t/B.warm)==='red'&&T.gap===gap;
      carrierThunderheadTick(boss,.10);const first=eBullets.filter(q=>q.kind==='s6prism'||q.kind==='s6cyclone');
      o.release=B.released&&first.length===12&&first.every(q=>Math.abs(q.vx)<.0001&&q.vy>0);
      const nextGap=T.gap;o.nextRow=T.wave===1&&nextGap===gap+1&&T.next===T.warnAt+T.rowTell&&!!boss._combatWarnings['stage6-thunderhead-1'];
      const before=eBullets.length;carrierThunderheadTick(boss,.65);o.noEarlySecond=eBullets.length===before&&T.gap===nextGap;
      carrierThunderheadTick(boss,.02);o.secondRelease=T.wave===2&&eBullets.filter(q=>q.kind==='s6prism'||q.kind==='s6cyclone').length===24;
      carrierThunderheadTick(boss,.67);carrierThunderheadTick(boss,.67);o.complete=T.wave===4&&eBullets.filter(q=>q.kind==='s6prism'||q.kind==='s6cyclone').length===48;
      const draw=carrierThunderheadDraw.toString();o.shared=draw.includes('combatWarningDraw')&&draw.includes('fieldOnly:true')&&draw.includes('alertOnly:true')&&!draw.includes("fillStyle='#67dcff'");
      o.layered=carrierMegaDrawUnder.toString().includes('carrierThunderheadDraw(b,false)')&&carrierMegaDrawOver.toString().includes('carrierThunderheadDraw(b,true)');
      o.live=carrierMegaTick.toString().includes('carrierThunderheadTick')&&carrierMegaTick.toString().includes('carrierThunderheadStart');
      return JSON.stringify(o);
    }finally{boss=save.boss;player=save.player;Object.assign(run,save.run);camX=save.camX;curStage=save.curStage;eBullets=save.eBullets;}
  })()`,ctxv));
  for(const k of Object.keys(result))ok(result[k],'Thunderhead warning: '+k);
};
