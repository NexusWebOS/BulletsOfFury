module.exports=function testStage2ReaverSharedWarning(vm,ctxv,ok){
  console.log('=== 359. Stage-2 Inferno Reaver role and shared shotgun warning ===');
  const out=JSON.parse(vm.runInContext(`(function(){
    const save={boss:boss,subBoss:subBoss,player:player,run:{...run},DIFF:DIFF,diff:diffKey,camX:camX,curStage:curStage,eBullets:eBullets,warnDraw:combatWarningDraw};
    const o={},draws=[];
    try{
      run.stage=2;curStage=STAGES[1];camX=0;diffKey='normal';DIFF=DIFFS.normal;eBullets=[];
      player={x:330,y:480,dead:false,alive:true,invuln:999,_hx:9,_hy:10};
      const b={x:240,y:120,_drawY:120,ty:120,maxhp:400,dead:false,enter:false,flash:0,fireCd:0};
      shipBossInit(b,'magmaward');b.enter=false;b.x=240;b.y=120;b.ty=120;boss=b;subBoss=b;
      o.identity=b.name==='INFERNO REAVER'&&!b._mwBarrier&&!b._furnace;

      b.hp=b.maxhp;b._sbStep=0;shipBossAttack(b);
      o.passStarts=!!b._irPass&&!b._mwAttack&&eBullets.length===0;
      infernoReaverPassTick(b,.73);infernoReaverPassTick(b,.01);infernoReaverPassTick(b,.01);
      o.passAdvances=!!b._l23Beam&&b._l23Beam.slots.length===1&&b._l23Beam.slots[0]==='L'&&b._l23Beam.warm>=L23_WARN_T;

      b._irPass=null;b._l23Beam=null;b._orb=null;b._sbStep=0;b.hp=b.maxhp*.10;shipBossAttack(b);
      o.rollStarts=!!b._irRoll&&!b._mwAttack;
      const x0=b.x;infernoReaverRollTick(b,.75);infernoReaverRollTick(b,.01);infernoReaverRollTick(b,.25);
      o.rollAdvances=!!b._irRoll&&b._irRoll.phase==='roll'&&(Math.abs(b.x-x0)>1||Math.abs(b._irRoll.poseRot)>0);

      b._irRoll=null;b._l23Beam=null;b._orb=null;b._sba=null;b._sbStep=0;b.hp=b.maxhp*.45;b.x=240;b.y=120;b._sbaPhase=2;eBullets=[];
      shipBossQueueAttack(b);const A=b._sba,W=A&&A.warning,B=b._combatWarnings&&b._combatWarnings['stage2-reaver-shotgun-fan'];
      o.warningStarts=!!A&&A.pat==='infernoburst'&&!!W&&W.paths.length===9&&!!B&&!B.released&&A.tell>.65;
      combatWarningDraw=function(owner,q){draws.push({...q});};b.x+=17;shipBossActionWarningDraw(b,false);shipBossActionWarningDraw(b,true);
      const C=shipBossMount(b,'C');o.draws=draws.length===10&&draws.filter(q=>q.fieldOnly).length===9&&draws.filter(q=>q.alertOnly).length===1&&Math.abs(draws[0].x-C.x)<1e-9;
      shipBossActionTick(b,A.tell*.20);o.green=l23FovPhase(B.t/B.warm)==='green'&&eBullets.length===0;
      shipBossActionTick(b,A.tell*.30);o.yellow=l23FovPhase(B.t/B.warm)==='yellow'&&eBullets.length===0;
      shipBossActionTick(b,A.tell*.30);o.red=l23FovPhase(B.t/B.warm)==='red'&&eBullets.length===0;
      shipBossActionTick(b,A.tell*.21);
      const groups={};for(const q of eBullets){const k=q.x.toFixed(4)+','+q.y.toFixed(4);groups[k]=(groups[k]||0)+1;}
      o.releaseState=B.released&&A.fired;
      o.releaseCount=eBullets.length===9;
      o.releaseSkin=eBullets.every(q=>q.kind==='magma');
      o.releaseMounts=Object.values(groups).sort((a,b)=>a-b).join(',')==='1,1,7';
      const move=shipBossManoeuvre.toString(),draw=shipBossDraw.toString(),init=shipBossInit.toString();
      o.roleRoutes=move.includes("b._ship==='magmaward'&&b._irPass")&&move.includes("b._ship==='magmaward'&&b._irRoll")&&draw.includes("b._ship==='magmaward'&&b._irRoll");
      o.shieldContract=init.includes("if(kind==='infernoreaver' && typeof magmaWardBarrierInit")&&!init.includes("kind==='magmaward'||kind==='infernoreaver'");
      return JSON.stringify(o);
    }finally{boss=save.boss;subBoss=save.subBoss;player=save.player;Object.assign(run,save.run);DIFF=save.DIFF;diffKey=save.diff;camX=save.camX;curStage=save.curStage;eBullets=save.eBullets;combatWarningDraw=save.warnDraw;}
  })()`,ctxv));
  for(const k of Object.keys(out))ok(out[k],'Stage-2 Reaver shared warning: '+k);
};
