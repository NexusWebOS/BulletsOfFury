module.exports=function(vm,ctxv,ok){
 console.log('=== 312. Maverick, collection, warnings and Eclipse bomber ===');
 const result=JSON.parse(vm.runInContext(`(()=>{
  const out={};run.stage=2;run.pilot='maverick';run.weapon=3;run.wlevel=5;run.spaceMode=false;run.sonicT=run.dkT=0;special=null;run.forge={};run.infusion=null;run.wvars=[];pBullets=[];
  pShoot();out['bare lances remain three tier-I shots']=pBullets.length===3&&pBullets.every(q=>q.kind==='mavlaser'&&q.lv===1&&!infusionCarrier(q));
  const cadence=_weaponCadence();run.wlevel=1;out['lance cadence also stays fixed']=_weaponCadence()===cadence;
  run.wlevels=WEAPONS.map(()=>1);applyPowerup({kind:'weapon',wtype:3,wvar:'mavhoming',x:240,y:300});pBullets=[];pShoot();out['laser pickups equip and upgrade beams instead of lances']=run._mavBeamUnlocked&&heldVariant(3)==='laserbeam'&&run.wlevel===2&&pBullets.some(q=>q.kind==='beam');run.wlevel=5;
  run.forge={3:{elem:'fire',lv:1}};run.wvars[3]='mavhoming';pBullets=[];pShoot();
  out['stale Lance pickup cannot override equipped Fire Whip']=heldVariant(3)==='firewhip'&&pBullets.length===1&&pBullets[0].kind==='firewhip';
  run.forge={3:{elem:'lightning',lv:1}};pBullets=[];pShoot();out['other laser infusions use the beam']=heldVariant(3)==='laserbeam'&&pBullets.some(q=>q.kind==='beam')&&!pBullets.some(q=>q.kind==='mavlaser');
  const owned=achievementState.owned;achievementState.owned={};run.forgeForms={};run.wlevels=WEAPONS.map(()=>0);run.forgeElems={fire:1};
  polishRememberWeapon(2);polishRememberItem('variant_mavhoming');polishRememberForm(3,'fire');polishRememberItem('space_2');
  const normalized=achievementNormalize(achievementState);out['acquired collection survives profile normalization']=!!normalized.owned.arsenal_base_2&&!!normalized.owned.arsenal_variant_mavhoming&&!!normalized.owned.arsenal_space_2&&!!normalized.owned[forgeComboId('fire',3)];
  const cells=polishCollection();out['element access alone does not reveal unacquired combinations']=cells.find(c=>c.w===3&&c.elem==='fire').owned&&!cells.find(c=>c.w===2&&c.elem==='fire').owned;
  out['collection includes 90 combinations and 10 distinct variants/space weapons']=cells.length===100&&cells.filter(c=>c.space!=null).length===3;
  achievementState.owned=owned;
  run.stage=5;run.spaceMode=true;run.spaceWeapon=1;run.forge={};flashScreen=.13;const oldPlayer=player,oldBullets=pBullets,oldRun=JSON.stringify(run),fx=Audio.SFX;let sounds=0;
  const playSample=Snd.play;Snd.play=()=>{sounds++;};Audio.SFX=Object.fromEntries(Object.keys(fx).map(k=>[k,()=>sounds++]));
  for(const [space,kind] of [[0,'spaceLaser'],[1,'shadowOrb'],[2,'spaceVolley']]){
   const P=forgePreviewNew(0,null,1);P.space=space;P.cd=0;forgePreviewTick(P,180,180,1/60);
   out['Armory previews real '+kind+' with sound']=!P.err&&P.bullets.some(q=>q.kind===kind)&&sounds>0;sounds=0;
  }
  Audio.SFX=fx;Snd.play=playSample;out['preview restores live state and screen flash']=JSON.stringify(run)===oldRun&&oldPlayer===player&&oldBullets===pBullets&&flashScreen===.13;
  diffKey='hard';DIFF=DIFFS.hard;curStage=STAGES[4];subBoss=null;subBossActive=false;boss=null;bossActive=false;groundTargetingReset();polishReset();enemies=[];powerups=[];eBullets=[];pBullets=[];player.x=240;player.y=420;player.dead=false;player.invuln=999;
  spawnSubBoss__inner('siegebomber');const b=subBoss,B=b._bomber;
  out['difficulty health bar matches all private pools']=b.hp===B.core+B.parts.reduce((n,p)=>n+p.hp,0)&&b.maxhp===B.coreMax+B.parts.reduce((n,p)=>n+p.max,0);
  out['bomber spans half the visible playfield']=b.w===VW*.5;
  for(let i=0;i<140;i++)siegeBomberTick(b,1/60);out['bomber enters once into bomb pursuit']=!b.enter&&B.mode==='bombs';
  const first=siegeBomberParts(b).find(p=>p.id==='engineL'),part=B.parts.find(p=>p.id==='engineL'),before=part.hp;
  hitSubBoss(17,first.x,first.y);out['ordinary projectiles hit the visible engine pool']=part.hp===before-17;
  const targets=siegeBomberTargets(b);out['all five physical parts expose Retina targets']=targets.length===5;
  const cannon=siegeBomberParts(b).find(p=>p.id==='laserR');out['held beam reaches cannon']=!!siegeBomberBeam(b,{x:cannon.x,w:5,top:0,bot:VH});
  siegeBomberSet(b,'charge');siegeBomberHit(b,1e6,cannon.x,cannon.y,'laserR');out['breaking a cannon interrupts charge']=B.mode==='recover'&&B.parts.find(p=>p.id==='laserR').hp===0;
  siegeBomberSet(b,'bombs');siegeBomberTick(b,.02);const marker=B.bombs.at(-1),tx=marker.x;player.x+=100;out['bomb landing warning is committed']=!marker.track&&marker.x===tx&&marker.warn>1;
  polishReset();eBullets=[];const lane=polishLane(b,200,120,Math.PI/2,{warn:1,speed:4.9});polishCombatTick(.9);out['missile stays absent during warning']=eBullets.length===0;
  b.x+=50;b.y+=20;polishLaneOrigin(lane);out['moving launcher carries its warning without retargeting']=lane.x===250&&lane.y===140&&lane.angle===Math.PI/2;
  polishCombatTick(.11);out['missile follows announced lane at authored speed']=eBullets.length===1&&eBullets[0]._committed&&!eBullets[0].homing&&eBullets[0].spd===4.9&&Math.abs(eBullets[0].vx)<.001;
  out['moving launcher fires from its current warning origin']=eBullets[0].x===250&&eBullets[0].y===140;
  siegeBomberHit(b,1e6,b.x,b.y,'core');polishCombatTick(.1);out['bomber defeat cancels its hazards and starts engine cookoffs']=b.dead&&polishLanes.length===0&&polishDeaths.length===1;
  for(let i=0;i<180;i++)siegeBomberTick(b,1/60);out['bomber death releases the campaign miniboss gate']=subBoss===null&&!subBossActive&&subBossDone;
  return JSON.stringify(out);
 })()`,ctxv));
 for(const [name,value] of Object.entries(result))ok(value,'September 27 polish: '+name);
};
