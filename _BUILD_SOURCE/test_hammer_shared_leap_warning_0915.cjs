module.exports=function testHammerSharedLeapWarning(vm,ctxv,ok){
  console.log('=== 334. Chrome Hammer shared leap warning ===');
  const result=JSON.parse(vm.runInContext(`(function(){
    const save={boss,player,run:{...run},powerups,camX,curStage,shoot:Audio.SFX.enemyShoot};const o={};
    try{
      Audio.SFX.enemyShoot=()=>{};camX=0;curStage=STAGES[4];run.stage=5;powerups=[];
      player={x:326,y:392,dead:false,invuln:999,_hx:9,_hy:10};
      boss={x:240,y:168,w:154,h:168,hp:1000,maxhp:1000,dead:false,flash:0};hammerBossInit(boss);
      boss.x=240;boss.y=168;boss.enter=false;boss._noHit=false;
      hammerTarget(boss);hammerState(boss,'warn');const h=boss._hammer,tx=h.tx,ty=h.ty;
      h.t=.19;hammerBossTick(boss,.01);let B=boss._combatWarnings['chrome-hammer-leap'];
      o.green=B.t===.2&&l23FovPhase(B.t/B.warm)==='green'&&h.state==='warn';
      player.x=80;player.y=260;h.t=.59;hammerBossTick(boss,.01);B=boss._combatWarnings['chrome-hammer-leap'];
      o.yellow=B.t===.6&&l23FovPhase(B.t/B.warm)==='yellow'&&h.tx===tx&&h.ty===ty;
      player.x=430;player.y=300;h.t=.99;hammerBossTick(boss,.01);B=boss._combatWarnings['chrome-hammer-leap'];
      o.red=B.t===1&&l23FovPhase(B.t/B.warm)==='red'&&h.tx===tx&&h.ty===ty;
      h.t=1.19;hammerBossTick(boss,.01);B=boss._combatWarnings['chrome-hammer-leap'];
      o.release=B.released&&B.t===1.2&&h.state==='leap'&&h.tx===tx&&h.ty===ty;
      const srcTick=hammerBossTick.toString(),srcDraw=hammerBossDraw.toString();
      o.shared=srcTick.includes("combatWarningTick(b,'chrome-hammer-leap'")&&srcDraw.includes('combatWarningDraw(b,{x:b.x,y:b.y,ex:h.tx,ey:h.ty');
      o.reticle=srcDraw.includes("hammerFrame('reticle',0,h.t<.4?null:h.t<.8?'yellow':'red')");
      o.boomerang=srcTick.includes("combatWarningTick(b,'chrome-hammer-boomerang'")&&HAMMER_SPIN_TIME===1.55&&HAMMER_OUT_TIME===.70&&HAMMER_RETURN_SPEED===315;
      return JSON.stringify(o);
    }finally{boss=save.boss;player=save.player;Object.assign(run,save.run);powerups=save.powerups;camX=save.camX;curStage=save.curStage;Audio.SFX.enemyShoot=save.shoot;}
  })()`,ctxv));
  for(const k of Object.keys(result))ok(result[k],'Chrome Hammer leap warning: '+k);
};
