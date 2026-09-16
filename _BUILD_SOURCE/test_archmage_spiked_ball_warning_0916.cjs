module.exports=function testArchmageSpikedBallWarning(vm,ctxv,ok){
  console.log('=== 357. Archmage committed spiked-ball launch warning ===');
  const out=JSON.parse(vm.runInContext(`(function(){
    const save={boss,player,run:{...run},powerups,camX,curStage,diff:diffKey,DIFF:DIFF,charge:Audio.SFX.bossWeaponCharge};const o={};
    try{Audio.SFX.bossWeaponCharge=()=>{};camX=0;curStage=STAGES[4];run.stage=5;powerups=[];diffKey='normal';DIFF=DIFFS.normal;player={x:326,y:392,dead:false,invuln:999,_hx:9,_hy:10};
      boss={x:240,y:168,w:158,h:176,hp:1000,maxhp:1000,dead:false,flash:0};hammerBossInit(boss);boss.x=240;boss.y=168;boss.enter=false;boss._noHit=false;boss._combatWarnings={};const h=boss._hammer;h.state='shield';h.t=.995;
      hammerBossTick(boss,.01);const B=boss._combatWarnings['archmage-spiked-ball'],dir=h.ballDir,path=hammerBallLaunchPath(boss);o.arm=h.state==='curl'&&h.ballWarn&&Math.abs(dir)===1&&B&&B.t===0&&!B.released;
      player.x=72;player.y=260;hammerBossTick(boss,.20);o.green=l23FovPhase(B.t/B.warm)==='green'&&h.ballDir===dir&&JSON.stringify(hammerBallLaunchPath(boss))===JSON.stringify(path);
      player.x=430;player.y=470;hammerBossTick(boss,.40);o.yellow=l23FovPhase(B.t/B.warm)==='yellow'&&h.ballDir===dir;
      hammerBossTick(boss,.45);o.red=l23FovPhase(B.t/B.warm)==='red'&&h.state==='curl';hammerBossTick(boss,.21);o.release=h.state==='ball'&&B.released&&!h.ballWarn&&h.ballFirst&&h.vx===150*dir&&h.vy===165;
      const l=camLeftX()+54,r=camRightX()-54,bt=PLAY.y+PLAY.h-54;o.path=path.dir===dir&&(Math.abs(path.ex-(dir<0?l:r))<.001||Math.abs(path.ey-bt)<.001)&&path.ey>path.y;
      const vx=h.vx;hammerBossTick(boss,.25);o.ball=h.state==='ball'&&h.angle>0&&Math.abs(h.vx)>=Math.abs(vx);
      h.state='shield';h.t=1.01;hammerBossTick(boss,.01);const C=boss._combatWarnings['archmage-spiked-ball'];hammerState(boss,'chaingun_draw');o.cancel=C.released&&!h.ballWarn&&h.state==='chaingun_draw';
      const draw=hammerBossDraw.toString(),tick=hammerBossTick.toString();o.shared=draw.includes("h.state==='curl'&&h.ballWarn")&&draw.includes('hammerBallLaunchPath')&&tick.includes("combatWarningTick(b,'archmage-spiked-ball'");o.timing=HAMMER_BALL_WARN===1.25;
      return JSON.stringify(o);
    }finally{boss=save.boss;player=save.player;Object.assign(run,save.run);powerups=save.powerups;camX=save.camX;curStage=save.curStage;diffKey=save.diff;DIFF=save.DIFF;Audio.SFX.bossWeaponCharge=save.charge;}
  })()`,ctxv));for(const k of Object.keys(out))ok(out[k],'Archmage spiked-ball warning: '+k);
};
