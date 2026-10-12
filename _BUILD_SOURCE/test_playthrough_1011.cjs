module.exports=function(vm,c,ok){
 const fs=require('fs'),path=require('path'),crypto=require('crypto'),root=path.resolve(__dirname,'..');
 console.log('=== October 11 recording: Armored Command, physical carrier and encounter corrections ===');
 for(const [file,key] of [['armored_command_art_1011.js','AC11_ART'],['armored_command_1011.js','AC11'],['playthrough_art_1011.js','PT11_ART'],['playthrough_1011.js','PT11'],['playthrough_finale_1011.js','PT11F']])
  if(vm.runInContext('typeof '+key,c)==='undefined')vm.runInContext(fs.readFileSync(path.join(root,'assets',file),'utf8'),c,{filename:file});
 const banks=JSON.parse(vm.runInContext('JSON.stringify(PT11_ART)',c));
 for(const [name,bank] of Object.entries(banks)){
  ok(bank.every(a=>{const bytes=fs.readFileSync(path.join(root,a.path));return a.w%2===0&&a.h%2===0&&a.w===bytes.readUInt32BE(16)&&a.h===bytes.readUInt32BE(20)&&crypto.createHash('sha256').update(bytes).digest('hex')===a.sha256;}),name+': registered even-sized shipping PNGs match hashes');
  if(name!=='ice_parts')ok(bank.length===16&&bank.every(a=>a.w===bank[0].w&&a.h===bank[0].h&&String(a.pivot)===String(bank[0].pivot)&&a.scale===bank[0].scale),name+': sixteen authored poses share their canvas, physical pivot and uniform scale');
 }
 const out=JSON.parse(vm.runInContext(`JSON.stringify((()=>{
  const out={};out['Armored Command has no radar well and larger live bands']=PH8.row===120&&PH8.height===212&&!AC11_ART.wells.radar;
  function stage(n){ht27Stop();coopOn=false;diffKey='furious';DIFF=difficultyForRun('arcade','furious');run.mode='arcade';run.pilot='maverick';beginStage(n);setState(GS.PLAY);BOFCinematicDirector.cancel();story=special=fb2Talk=null;s6Opening=null;player.invuln=999;boss=subBoss=null;bossActive=subBossActive=false;enemies=[];pBullets=[];eBullets=[];powerups=[];}
  stage(3);spawnSubBoss__inner('frostcruiser');const frost=subBoss;frost.enter=false;frost._noHit=false;frost.x=340;frost.y=frost._drawY=190;
  const gun=mr27Part(frost,'gunL'),p=mr27Shape(frost,'gunL'),right=mr27Part(frost,'gunR'),hp=right.hp;
  out['Carrier missile and cannon sockets are independent of its core']=Math.abs(p.pivotX-frost.x)>80&&mr27Shape(frost,'rocketL').pivotX!==p.pivotX;
  mr27Damage(frost,gun.hp+5,p.x,p.y);out['Destroying the left cannon leaves the right cannon operational']=gun.dead&&!mr27CanFire(frost,'L')&&mr27CanFire(frost,'R')&&right.hp===hp;
  stage(4);spawnBoss('stormsovereign');const storm=boss;storm.enter=false;storm.x=340;storm.y=180;storm._er26.engaged=true;
  stage4ShieldSyncNodes(storm);const before=JSON.stringify(storm._s4war.shield.nodes.map(n=>[n.x,n.y]));storm.x+=60;storm.y+=20;stage4ShieldSyncNodes(storm);
  out['Moving the Storm hull does not move generator targets']=JSON.stringify(storm._s4war.shield.nodes.map(n=>[n.x,n.y]))===before;
  out['Storm attack book uses lightning rather than the ice-laser dispatcher']=er26Book(storm).includes('ap10-stormburst')&&!er26Book(storm).includes('p2-core-laser');
  storm._s4war.shield.active=false;storm._s4war.shield.rearming=false;storm.hp=storm.maxhp*.25;
  stage4ShieldBeginRearm(storm,.25);for(let i=0;i<620;i++)er26Tick(storm,1/60);
  out['Final quarter pursuit ends without a shield refill or locked damage']=storm._s4war._pt11Chase.done&&storm._s4war._pt11Chase.wave>0&&!storm._s4war.shield.active&&!storm._s4war.shield.rearming&&!storm._noHit;
  stage(5);spawnBoss(curStage.boss);const b=boss,h=b._hammer;b.enter=b._noHit=false;b.hp=b.maxhp=6000;b.x=340;b.y=180;h.balance0922=h.intro1002=h.gp4FailsafeSeen=true;
  h.frArmor={hp:1000,max:1000,active:true,activated:true,half:true,barrier:0,t:0,checkpoints:[.75,.5,.35,.15]};h.state='storm_stun';h.t=.2;
  out['Electrified recovery cannot be cheesed by shooting from above']=hammerBossDamage(b,75)===0&&b.hp===6000;
  const old=h.chainMax;hammerBossModuleBreak(b,'chaingun');hammerBossModuleBreak(b,'chaingun');
  out['Chaingun salvage drops exactly once during the fight']=old>=Math.ceil(95*DIFF.eHp*1.85)&&powerups.filter(p=>p.kind==='pt11chain').length===1;
  out['Salvage has a finite position and guaranteed collection route']=powerups.filter(p=>p.kind==='pt11chain').every(p=>Number.isFinite(p.bob)&&p._fcHold!=null);
  return out;
 })())`,c));
 for(const [name,pass] of Object.entries(out))ok(pass,name);
};
