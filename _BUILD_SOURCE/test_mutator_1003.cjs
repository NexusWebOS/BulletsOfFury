module.exports=function(vm,ctxv,ok){
 const fs=require('fs'),path=require('path');
 for(const f of ['build_integration_1003.js','mutator_art_1003.js','mutator_1003.js'])vm.runInContext(fs.readFileSync(path.join(__dirname,'../assets',f),'utf8'),ctxv,{filename:f});
 console.log('=== October 3 integrated build and selected Monster Mutator roster ===');
 const checks=JSON.parse(vm.runInContext(`JSON.stringify((()=>{
 const o={};ht27Stop();debugFight=null;coopOn=false;run.mode='campaign';run.pilot='yuri';
 function reset(stage,d='normal'){diffKey=d;DIFF=DIFFS[d];beginStage(stage);setState(GS.PLAY);player.reset();BOFCinematicDirector.cancel();story=null;stagePlan=[];enemies=[];eBullets=[];pBullets=[];boss=null;subBoss=null;bossActive=subBossActive=false;player.x=worldWidth()/2;player.y=VH-70;player.invuln=1e9;camX=player.x-VW/2;groundTargetingReset();ai27Context=null;}
 o['exactly seven selected designs and three component kits']=Object.keys(MM1003_DEF).length===7&&Object.keys(MM1003_ART).length===10;
 for(const diff of ['easy','normal','hard','furious']){
  for(const stage of [7,8]){
   reset(stage,diff);const plan=buildStagePlan(stage);for(const wave of plan)wave.fn();
   o[diff+' stage '+stage+' campaign callbacks dispatch selected replacements']=Object.values(MM1003_SLOTS[stage]).every(k=>enemies.some(e=>e._mutator1003===k));
   if(stage===8)o[diff+' keeps all three new alien FOV units']=Object.values(S81003_ROLES).every(k=>enemies.some(e=>e._alien1003===k));
  }
  for(const kind of Object.keys(MM1003_DEF)){
   reset(8,diff);const e=spawnEnemy('mm1003_'+kind,player.x,130,{}),A=e._mm1003;A.phase='rest';A.cd=0;A.homeX=e.x;A.homeY=e.y;const hp=e.hp;
   let fired=0,cast=0,locked=null,stable=true,phase=new Set();
   for(let i=0;i<680&&!e.dead;i++){
    mm1003Tick(e,1/60);phase.add(A.phase);fired=Math.max(fired,eBullets.filter(q=>q._mutatorShot1003).length);cast=Math.max(cast,groundTargetingFx.filter(q=>q.owner===e).length);
    if(A.phase==='tell'){const t=JSON.stringify(A.target);if(locked&&locked!==t)stable=false;locked=t;}else locked=null;
   }
   o[diff+' '+kind+' has finite upright pose and committed tell']=Number.isFinite(e.x+e.y)&&e.spin===0&&stable&&phase.has('tell');
   o[diff+' '+kind+' releases its distinct attack']=kind==='hellhugger'?phase.has('dash'):kind==='hexpyre'?cast>=2&&cast%2===0:fired>0;
   o[diff+' '+kind+' preserves a recovery window']=phase.has('recover')&&e.hp===hp;
  }
 }
 reset(7);const e=spawnEnemy('mm1003_riflelocust',player.x,140,{});e._mm1003.phase='rest';const guns=e._mm1003.parts.filter(p=>p.kind==='gun');
 const t=mm1003Target(e,guns[0]);o['module has a stable real Retina and space target']=_lockTargets().includes(t)&&spaceTargets().includes(t)&&mm1003Target(e,guns[0])===t;
 const hp=e.hp;retinaMissileDamage(t,999,{kind:'gmiss'});retinaMissileDamage(t,999,{kind:'gmiss'});
 o['targeted missile removes only its rifle and retires the lock']=guns[0].dead&&e.hp===hp&&!_lockTargets().includes(t)&&MM1003.debris.length===1;
 for(const p of guns)if(!p.dead){mm1003PartHit(e,p,999);mm1003PartHit(e,p,999);}
 eBullets=[];e._mm1003.phase='fire';e._mm1003.age=0;for(let i=0;i<120;i++)mm1003Tick(e,1/60);
 o['destroying both rifles cancels the attack']=!eBullets.some(q=>q._mutatorShot1003)&&mm1003Disarmed(e);
 reset(8);const h=spawnEnemy('mm1003_hexpyre',player.x,140,{});mm1003Warning(h);o['caster ground warnings are committed local circles']=groundTargetingFx.length===2&&groundTargetingFx.every(q=>!q.track&&!q.lane);
 for(let i=0;i<3&&mm1003Alive(h);i++)hitEnemy(h,9999);o['caster death cancels its floor hazards']=groundTargetingFx.every(q=>q.dead);
 reset(7);const claw=spawnEnemy('mm1003_hellhugger',player.x,120,{});o['Hellhugger is a fragile threat']=claw.hp<spawnEnemy('mm1003_hellram',player.x+130,120,{}).hp*.4;
 mm1003Warning(claw);for(const p of claw._mm1003.parts.filter(p=>p.front)){mm1003PartHit(claw,p,99);mm1003PartHit(claw,p,99);}mm1003Tick(claw,.01);o['breaking both foreclaws interrupts its warned rush']=claw._mm1003.phase==='recover';
 beginStage(1);o['stage transition clears detached modules']=MM1003.debris.length===0;
 reset(5);spawnBoss(curStage.boss);const b=boss;b._hammer.state='unfold';b._hammer.t=1.95;fb2IntroStart(b);
 o['one live Hammer dialogue owns the intro']=fb2IntroActive()&&b._hammer.intro1002&&!BOFCinematicDirector.live;
 o['campaign live dialogue preserves the trap taunt']=fb2Intro.lines.some(l=>l.text.includes('Legion has already'));
 fb2IntroEnd();o['dialogue ends with the opening jump warning']=b._hammer.state==='warn'&&!b._noHit;
 const opening=[];for(let i=0;i<540;i++){hammerBossTick(b,1/60);if(opening.at(-1)!==b._hammer.state)opening.push(b._hammer.state);}
 o['opening jump lands and returns before chromium activation']=['warn','leap','recover','back','fr_activation','hammer'].every((s,i,a)=>opening.includes(s)&&(i===0||opening.indexOf(s)>opening.indexOf(a[i-1])));
 o['opening jump releases its armor deferral']=!b._hammer.openingJump1003&&!!fr27Armor(b)?.activated;
 return o;})())`,ctxv));
 for(const [name,pass]of Object.entries(checks))ok(pass,name);
};
