module.exports=function(vm,ctxv,ok){
  const fs=require('fs'),path=require('path');
  console.log('=== 305. Stage 2–4 authored encounter directors and nuclear ordering ===');
  for(const file of ['stage3_thermo.js','encounters_0926.js'])
    vm.runInContext(fs.readFileSync(path.join(__dirname,'../assets',file),'utf8'),ctxv,{filename:file});
  const results=JSON.parse(vm.runInContext(`(function(){
    const o={};
    function fixture(kind,stage,diff){
      run.stage=stage;run.pilot='cole';curStage=STAGES[stage-1];diffKey=diff;DIFF=DIFFS[diff];
      boss=null;subBoss=null;bossActive=false;subBossActive=false;enemies=[];eBullets=[];pBullets=[];
      powerups=[];explosions=[];particles=[];camX=0;player.x=240;player.y=410;player.dead=false;player.invuln=10000;
      const mini=kind==='magmaward'||kind==='frostcruiser'||kind==='olivewarden';
      if(mini)spawnSubBoss__inner(kind);else spawnBoss(kind);
      const b=mini?subBoss:boss;b.enter=false;b._be=null;b._noHit=false;b.x=worldWidth()/2;b.y=b._er26.home;
      b._er26.from={x:b.x,y:b.y};b._er26.to={x:b.x,y:b.y};b._drawY=b.y;return b;
    }
    const books={};
    for(const [kind,stage] of [['magmaward',2],['frostcruiser',3],['cryospear',3],['olivewarden',4],['stormsovereign',4]]){
      for(const diff of ['normal','hard','furious']){
        const b=fixture(kind,stage,diff),R=b._er26,seen=new Set();let bounded=true,old={x:b.x,y:b.y};
        for(let i=0;i<2700;i++){
          b.t=(b.t||0)+1/60;er26Tick(b,1/60);seen.add(R.mode);
          bounded=bounded&&Number.isFinite(b.x)&&Number.isFinite(b.y)&&Math.hypot(b.x-old.x,b.y-old.y)<15;old={x:b.x,y:b.y};
          if(i%120===0)eBullets=[];
        }
        o[kind+' '+diff+' progresses with continuous movement']=seen.size>=5&&bounded;
        const shots=eBullets.length;shipBossAttack(b);shipBossQueueAttack(b);
        o[kind+' '+diff+' has one attack owner']=eBullets.length===shots&&b.fireCd===999;
        if(kind==='magmaward'){
          books[diff]=er26Book(b);
          o['Reaver '+diff+' uses authored round fire instead of yellow darts']=eBullets.every(q=>q._er26Art==='fire'&&!q._l23fx&&!q._bfam);
        }
      }
    }
    o['Furious Reaver has an entirely separate attack book']=books.furious.every(k=>!books.normal.includes(k));
    for(const kind of ['frostcruiser','cryospear']){
      const b=fixture(kind,3,'furious'),role=kind==='frostcruiser'?'mini':'boss',max=b.maxhp;
      o[kind+' begins neutral with one health-bar settle before the bomb']=b._er26.neutralOpening&&s3ThermoStrikeTick(role,b,1/60)&&!S3_THERMO_STRIKE[role];
      const fire=elementalDamageResult(b,role,{_el:'fire'},10,b.x,b.y),ice=elementalDamageResult(b,role,{_el:'ice'},10,b.x,b.y);
      o[kind+' neutral is normal damage and white impact']=fire.dmg===10&&ice.dmg===10&&hitFlashColor(b,'#ffffff')==='#ffffff';
      o[kind+' burst cannot skip the nuclear transformation']=er26DamageClamp(b,max*2)===max*.25;
      b._s3Arrival=.65;b._er26.mode='recover';b.hp=max*.75;
      s3ThermoStrikeTick(role,b,1/60);o[kind+' missile starts after the single arrival']=S3_THERMO_STRIKE[role].old===b&&b._noHit;
      const before=b.hp;_dmgBullet={_el:'fire'};if(role==='mini')hitSubBoss(10,b.x,b.y);else hitBoss(10);
      o[kind+' nuclear cinematic is damage-safe']=before===b.hp;
      for(let i=0;i<365;i++)s3ThermoStrikeTick(role,b,1/60);
      o[kind+' same actor transforms directly into fire']=b.kind===kind&&(role==='mini'?subBoss:boss)===b&&b._s3Nuclear.mode==='fire'&&b.hp===max*.75&&!b._noHit&&!b._er26.neutralOpening;
      o[kind+' blast uses sustained engine explosions once']=b._s3Nuclear.blasts>=20&&!s3ThermoStrikeTick(role,b,1)&&S3_THERMO_STRIKE[role]===null;
      for(const form of ['fire','ice']){
        b._s3Nuclear.mode=form;
        const weak=elementalDamageResult(b,role,{_el:form==='fire'?'ice':'fire'},10),same=elementalDamageResult(b,role,{_el:form},10);
        o[kind+' '+form+' weakness 1.5x and same-element 1x']=weak.dmg===15&&same.dmg===10&&hitFlashColor(b,'#ffffff')==='#ffffff';
      }
      run.pilot='freezer';b._s3Nuclear.mode='fire';
      o[kind+' Freezer pre-scaling does not multiply twice']=elementalDamageResult(b,role,{_ts:true,_el:'fireice'},15).dmg===15;
      run.pilot='cole';b._er26.form='fire';b._s3Nuclear.mode='fire';b._er26.formBeats=2;er26Next(b);
      for(let i=0;i<96;i++)er26Tick(b,1/60);
      o[kind+' alternates into ice without another bomb']=b._er26.form==='ice'&&b._s3Nuclear.mode==='ice'&&!b._noHit;
    }
    const b=fixture('stormsovereign',4,'furious'),S=b._s4war,R=b._er26;
    for(const n of S.shield.nodes)stage4ShieldDestroyNode(b,n);stage4ShieldBeginRearm(b,.25);
    for(let i=0;i<80;i++)er26Tick(b,1/60);er26Set(b,'escort-crossfire');
    let alternating=true,noBody=true,hotWindow=false,left=0,right=0;R.bodyShots=0;
    for(let i=0;i<375;i++){
      const start=eBullets.length,body=R.bodyShots;er26Tick(b,1/60);
      const fresh=eBullets.slice(start).filter(q=>q._er26Source==='core');
      alternating=alternating&&new Set(fresh.map(q=>q._s4CoreSide)).size<=1;
      if(R.mode==='escort-crossfire')noBody=noBody&&body===R.bodyShots;
      left+=fresh.filter(q=>q._s4CoreSide<0).length;right+=fresh.filter(q=>q._s4CoreSide>0).length;
      hotWindow=hotWindow||S.coreTurrets.some(t=>t.state==='overheat'&&t.vulnerable);
    }
    o['Sovereign helpers take separate committed firing turns']=alternating&&left>0&&right>0;
    o['Sovereign hull does not stack fire on the helper turn']=noBody;
    o['Sovereign helpers offer a visible overheat punish window']=hotWindow;
    _dmgBullet=null;return JSON.stringify(o);
  })()`,ctxv));
  for(const [name,pass] of Object.entries(results))ok(pass,'Encounter revamp: '+name);
};
