module.exports=function testStage8VileSharedAnnihilationWarning(vm,ctxv,ok){
  console.log('=== 338. Stage-8 Vile shared annihilation warning ===');
  const result=JSON.parse(vm.runInContext(`(function(){
    const save={boss,player,run:{...run},camX,curStage,eBullets,phase:Audio.SFX.bossPhase};const o={};
    try{
      Audio.SFX.bossPhase=()=>{};camX=0;curStage=STAGES[7];run.stage=8;eBullets=[];
      player={x:360,y:400,dead:false,invuln:999,_hx:9,_hy:10};
      boss={x:240,y:140,w:236,h:236,hp:5000,maxhp:5000,dead:false,flash:0,fireCd:0,t:0,_vile:true,_vForm:3,_annihilationUsed:false};
      vileAnnihilationStart(boss);const A=boss._annihilation,tx=A.tx,ty=A.ty,src=vileAnnihilationSources(A);
      o.commits=tx===360&&ty===400&&src.length===4&&boss._combatWarnings['stage8-vile-annihilation'].t===0;
      A.t=.13;vileAnnihilationTick(boss,0);let B=boss._combatWarnings['stage8-vile-annihilation'];o.green=l23FovPhase(B.t/B.warm)==='green';
      player.x=40;player.y=260;A.t=.39;vileAnnihilationTick(boss,0);B=boss._combatWarnings['stage8-vile-annihilation'];o.yellow=l23FovPhase(B.t/B.warm)==='yellow'&&A.tx===tx&&A.ty===ty;
      player.x=230;player.y=450;A.t=.702;vileAnnihilationTick(boss,0);B=boss._combatWarnings['stage8-vile-annihilation'];o.red=l23FovPhase(B.t/B.warm)==='red'&&A.tx===tx&&A.ty===ty;
      A.t=.79;vileAnnihilationTick(boss,0);B=boss._combatWarnings['stage8-vile-annihilation'];const shots=eBullets.filter(q=>q._bfam==='vile');
      o.release=B.released&&A.wave===1&&shots.length===8;
      o.targets=shots.every((q,i)=>{const p=src[(i/2)|0],a=Math.atan2(ty-p[1],tx-p[0]);return Math.abs(Math.atan2(q.vy,q.vx)-a)<.0001;});
      const draw=vileAnnihilationDraw.toString(),body=drawModularBoss.toString();o.shared=draw.includes('fieldOnly:true')&&draw.includes('alertOnly:true')&&body.includes('vileAnnihilationDraw(b,false)')&&body.includes('vileAnnihilationDraw(b,true)');
      return JSON.stringify(o);
    }finally{boss=save.boss;player=save.player;Object.assign(run,save.run);camX=save.camX;curStage=save.curStage;eBullets=save.eBullets;Audio.SFX.bossPhase=save.phase;}
  })()`,ctxv));
  for(const k of Object.keys(result))ok(result[k],'Vile annihilation warning: '+k);
};
