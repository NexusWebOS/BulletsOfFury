module.exports=function testHammerBoomerang(vm,ctxv,ok){
  console.log('=== 304e. Chrome Hammer counter, catch and spiral retaliation ===');
  const result=JSON.parse(vm.runInContext(`(function(){
    const save={boss,player,hit:playerHit,run:{...run},powerups,camX,curStage,diffKey,DIFF,random:Math.random,bullet:_dmgBullet};const o={};
    try{
      camX=0;curStage=STAGES[4];run.stage=5;run.lives=9;powerups=[];diffKey='normal';DIFF=DIFFS.normal;
      player={x:326,y:392,dead:false,invuln:999,_hx:9,_hy:10};
      boss={x:240,y:168,w:154,h:168,hp:1000,maxhp:1000,dead:false,flash:0};hammerBossInit(boss);
      boss.x=240;boss.y=168;boss.enter=false;boss._noHit=false;const h=boss._hammer;h.balance0922=true;hammerState(boss,'hammer');
      hammerBoomerangStart(boss);o['committed opening']=h.state==='spin'&&h.throwX===326;
      player.x=95;hammerBossTick(boss,.2);o['no late retarget']=h.throwX===326;
      const a0=h.spinAngle;hammerBossTick(boss,.35);const a1=h.spinAngle;hammerBossTick(boss,.35);const a2=h.spinAngle;o['spin accelerates']=a2-a1>a1-a0;
      hammerBossTick(boss,.66);o['releases']=h.state==='throw'&&h.throw.phase==='out';
      hammerBossTick(boss,.3);const T=h.throw;const hp=h.hammerHP;
      o['detached weapon hittable']=bossHitTest(T.x,T.y)&&boss._hammerModuleHit==='hammer';
      o['counter no hull damage']=hammerBossDamage(boss,1)===0&&T.reflected&&T.phase==='return'&&h.hammerHP===hp;
      let hits=0;playerHit=()=>hits++;player.invuln=0;player.x=T.x;player.y=T.y;hammerBoomerangHit(T,.01);o['counter return safe']=hits===0;
      player.invuln=999;for(let i=0;i<180&&h.state==='throw';i++)hammerBossTick(boss,1/60);
      o['magnetic catch']=h.state==='hammer_catch'&&!h.throw&&h.catchRetaliate;
      Math.random=()=>.1;hammerBossTick(boss,.7);o['angry windup']=h.state==='revenge_charge'&&h.spiralPlan.side===-1;
      const plan={...h.spiralPlan};hammerBossTick(boss,1);o['faster windup']=h.spinAngle>45;
      hammerBossTick(boss,1.01);o['retaliation release']=h.state==='throw'&&h.throw.phase==='swirl'&&h.throw.revenge;
      const locked={cx:h.throw.cx,cy:h.throw.cy,side:h.throw.side};player.x=450;hammerBossTick(boss,.6);
      o['spiral stays committed']=h.throw.cx===locked.cx&&h.throw.cy===locked.cy&&h.throw.side===locked.side;
      const p0=hammerSpiralPoint(plan,0),p1=hammerSpiralPoint(plan,1);o['spiral contracts']=Math.hypot(p1.x-plan.cx,p1.y-plan.cy)<Math.hypot(p0.x-plan.cx,p0.y-plan.cy)*.2;
      const right={...plan,side:1},L=hammerSpiralPoint(plan,.2),R=hammerSpiralPoint(right,.2);o['both spiral directions']=Math.abs(L.x+R.x-2*plan.cx)<.001&&Math.abs(L.y-R.y)<.001;
      o['retaliation counterable']=hammerThrowReflect(boss);for(let i=0;i<180&&h.state==='throw';i++)hammerBossTick(boss,1/60);
      o['no endless retaliation']=h.state==='hammer_catch'&&!h.catchRetaliate;hammerBossTick(boss,.7);o['returns to hammer']=h.state==='hammer';
      Math.random=()=>.9;hammerSpiralArm(boss);o['rng right start']=h.spiralPlan.side===1;
      return JSON.stringify(o);
    }finally{boss=save.boss;player=save.player;playerHit=save.hit;Object.assign(run,save.run);powerups=save.powerups;camX=save.camX;curStage=save.curStage;diffKey=save.diffKey;DIFF=save.DIFF;Math.random=save.random;_dmgBullet=save.bullet;}
  })()`,ctxv));
  for(const [k,v] of Object.entries(result))ok(v,'Chrome Hammer boomerang: '+k);
};
