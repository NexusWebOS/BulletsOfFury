const fs=require('fs');
const path=require('path');
module.exports=function(vm,ctxv,ok){
  console.log('=== 322. authored Hard/Furious elite aces ===');
  const q=JSON.parse(vm.runInContext(`(function(){
    var save={runStage:run.stage,curStage:curStage,diffKey:diffKey,DIFF:DIFF,plan:stagePlan,en:enemies,pb:pBullets,eb:eBullets,px:player.x,py:player.y};
    var o={counts:true,sorted:true,flags:true,shields:true,variants:true,bounded:true,normalClean:true,hardOne:true,furiousTwo:true,unique:true};
    var expected={1:null,2:'emberwing',3:'glacierlance',4:'furytalon',5:'voidreaver',6:'tempest',7:'ironserpent',8:'nighthammer',9:'solarwarden'},seen=[];
    try{
      for(var s=1;s<=9;s++){
        run.stage=s;curStage=STAGES[s-1];
        for(const k of ['easy','normal','hard','furious']){
          diffKey=k;DIFF=DIFFS[k];enemies=[];pBullets=[];eBullets=[];stagePlan=buildStagePlan(s);
          var waves=stagePlan.filter(w=>w.fn&&w.fn._difficultyElite),want=s===1?0:(k==='furious'?2:(k==='hard'?1:0));   // Mike 0918: none on stage 1
          o.counts=o.counts&&waves.length===want;o.normalClean=o.normalClean&&((k==='easy'||k==='normal')?waves.length===0:true);
          o.hardOne=o.hardOne&&(k!=='hard'||waves.length===(s===1?0:1));o.furiousTwo=o.furiousTwo&&(k!=='furious'||waves.length===(s===1?0:2));o.stage1Clean=(o.stage1Clean!==false)&&(s!==1||waves.length===0);
          o.sorted=o.sorted&&stagePlan.every((w,i)=>i===0||stagePlan[i-1].t<=w.t);
          if(waves.length){
            var last=Math.max.apply(Math,stagePlan.filter(w=>!w.fn._difficultyElite).map(w=>w.t));
            o.bounded=o.bounded&&waves.every(w=>w.t>=12&&w.t<=Math.max(12,last));
            enemies=[];waves.forEach(w=>w.fn());var elite=enemies.filter(e=>e._difficultyElite);
            o.flags=o.flags&&elite.length===want&&elite.every(e=>e._continueEligible&&e.pattern==='elitex'&&e.art==='xelite_'+e._eliteAuthoredVariant);
            o.shields=o.shields&&elite.every(e=>e._esh&&e._esh.energy>0&&e._esh.max===e._esh.energy);
            if(k==='hard'){o.variants=o.variants&&elite[0]&&elite[0]._eliteAuthoredVariant===expected[s];seen.push(elite[0]._eliteAuthoredVariant);}
          }
        }
      }
      o.unique=new Set(seen).size===8;
      diffKey='furious';DIFF=DIFFS.furious;run.stage=6;curStage=STAGES[5];enemies=[];pBullets=[];eBullets=[];player.x=420;player.y=620;
      var ace=spawnDifficultyElite(6,0);ace.y=VH*ELITEX.tempest.band;ace.x=150;ace._fcd=0;pBullets=[{x:ace.x-8,y:ace.y+50,vy:-8,dead:false}];
      var x0=ace.x;elitexTick(ace,1/30);o.roll=ace._rollT!=null;o.hunts=ace.x!==x0;o.fires=eBullets.length===ELITEX.tempest.vol;
      o.authored=Object.keys(DIFFICULTY_ELITE_STAGE).length===8&&!DIFFICULTY_ELITE_STAGE[1]&&Object.values(DIFFICULTY_ELITE_STAGE).flat().every(k=>ELITEX[k]);
      o.noTint=spawnDifficultyElite.toString().indexOf('xartTint')<0&&difficultyElitePlan.toString().indexOf('palette')<0;
      return JSON.stringify(o);
    }finally{run.stage=save.runStage;curStage=save.curStage;diffKey=save.diffKey;DIFF=save.DIFF;stagePlan=save.plan;enemies=save.en;pBullets=save.pb;eBullets=save.eb;player.x=save.px;player.y=save.py;}
  })()`,ctxv));
  const labels={counts:'each stage injects zero/one/two aces on Normal/Hard/Furious',sorted:'elite waves preserve stable chronological stage scheduling',flags:'spawned aces carry authored identity and reward eligibility',shields:'every injected ace owns a live authored shield',variants:'each Hard stage receives its designated authored biome palette',bounded:'elite waves stay inside the authored combat timeline',normalClean:'Easy and Normal plans remain byte-for-byte free of difficulty elites',hardOne:'Hard adds one demanding ace per stage (none on stage 1)',furiousTwo:'Furious adds a second distinct ace wave per stage (none on stage 1)',stage1Clean:'Mike 0918: stage 1 fields no shielded difficulty ace on any difficulty',unique:'the eight ace stages each use a distinct primary authored ace',roll:'the ace rolls away from incoming player fire',hunts:'the ace strafes toward the player column',fires:'the ace releases its complete authored volley',authored:'all configured variants resolve through the existing ELITEX roster',noTint:'difficulty injection never applies a runtime palette overlay'};
  for(const k of Object.keys(labels))ok(q[k],labels[k]);
  const artRoot=path.join(__dirname,'..','assets','game','expansion_v1','ships_south');
  for(const name of ['razorback','emberwing','glacierlance','furytalon','voidreaver','tempest','ironserpent','nighthammer','solarwarden']){
    ok(fs.existsSync(path.join(artRoot,'xelite_'+name+'.png')),'authored elite plate exists: '+name);
  }
};
