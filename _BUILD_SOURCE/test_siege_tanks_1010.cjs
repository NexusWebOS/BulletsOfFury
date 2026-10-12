module.exports=function(vm,c,ok){
 const fs=require('fs'),path=require('path'),crypto=require('crypto'),root=path.resolve(__dirname,'..');
 console.log('=== Level 1 siege tank passwords 1010 ===');
 for(const [name,symbol]of [['asset_memory_1007.js','BOF_MEMORY'],['siege_tanks_art_1010.js','SG10_ART'],['siege_tanks_1010.js','SG10']])
  if(vm.runInContext('typeof '+symbol,c)==='undefined')vm.runInContext(fs.readFileSync(path.join(root,'assets',name),'utf8'),c,{filename:name});
 const banks=JSON.parse(vm.runInContext('JSON.stringify(SG10_ART)',c));let files=true,geometry=true,hashes=true;
 for(const bank of Object.values(banks)){const a=bank[0];
  for(const q of bank){const p=path.join(root,q.path);if(!fs.existsSync(p)){files=false;continue;}const bytes=fs.readFileSync(p);
   geometry&&=q.w%2===0&&q.h%2===0&&q.w===bytes.readUInt32BE(16)&&q.h===bytes.readUInt32BE(20)&&q.w===a.w&&q.h===a.h&&String(q.pivot)===String(a.pivot);
   hashes&&=crypto.createHash('sha256').update(bytes).digest('hex')===q.sha256;
  }
 }
 ok(files,'All shipped siege frame paths exist');ok(geometry,'Shipped PNGs have registered even bank dimensions and fixed pivots');ok(hashes,'Shipped art matches the approved normalized pixels');
 const result=JSON.parse(vm.runInContext(`JSON.stringify((()=>{
  const out={},old={hit:playerHit,drop:dropPowerup,src:_dmgSrc,bullet:_dmgBullet};
  try{
   playerHit=()=>{};dropPowerup=()=>{};_dmgBullet=null;_dmgSrc='bullet';
   out['Default Level 1 miniboss remains Razorback']=SUBBOSS[1].kind==='razorback';
   const pages=pc5Pages().flatMap(p=>p.rows),seen=new Set();
   out['Pinned catalog contains each new named encounter once']=Object.keys(SG10.routes).every(code=>pages.filter(r=>r[0]===code).length===1&&pages.find(r=>r[0]===code)[1]===SG10.specs[SG10.kinds[SG10.routes[code]]].name);
   for(const diff of ['easy','normal','hard','furious'])for(const [code,kind]of Object.entries(SG10.routes)){
    run.mode='arcade';diffKey=diff;DIFF=difficultyForRun('arcade',diff);pilotIndex=PILOTS.findIndex(p=>p.key==='yuri');
    setState(GS.PASSWORD);pwInput=code.toLowerCase();submitPassword();
    out[code+' '+diff+' enters the ordinary difficulty flow']=state===GS.DIFF&&PENDING_STAGE===1&&ON5.pending?.kind===kind;
    startRun(1);const b=subBoss,S=b._sg10;b.enter=false;b.y=b.ty;sg10Sync(b);player.invuln=999;player.dead=false;
    out[code+' '+diff+' launches a real Level 1 miniboss']=run.stage===1&&state===GS.PLAY&&subBossActive&&b.kind===kind&&b.maxhp>0&&b.hp===b.maxhp&&Object.keys(S.parts).length===8;
    const before=b.hp,p=S.parts.weapon;sg10Damage(b,12,null,null,'weapon');
    out[code+' '+diff+' weapon hits reduce both module and encounter health']=p.hp<p.maxhp&&b.hp<before&&b.flash>0;
    const box=sg10Box(b,SG10_RIG.at(-1)),beam={kind:'beam',x:(box.l+box.r)/2,w:12,top:PLAY.y,bot:VH};
    const hit=sg10Beam(b,beam),saved=b.hp;_dmgBullet=beam;hitSubBoss(10,hit?.x,hit?.y);_dmgBullet=null;
    out[code+' '+diff+' finite beams damage mounted geometry']=!!hit&&b.hp<saved&&!sg10Beam(b,{...beam,top:VH-12,bot:VH});
    const locks=retinaBossTargets(b),target=locks.find(t=>t._retinaId==='podL'),podBefore=S.parts.podL.hp;
    target._retinaHit(10);out[code+' '+diff+' missile locks damage the chosen live module']=S.parts.podL.hp<podBefore&&locks.length===8;
    const hp=b.hp;sg10Damage(b,20);out[code+' '+diff+' area attacks spend encounter damage once']=Math.abs((hp-b.hp)-20)<.01;
    sg10Break(b,'weapon');S.rest=0;sg10StartAttack(b);out[code+' '+diff+' destroyed main weapon disables cannon attacks']=S.attack.kind==='pods'&&!retinaBossTargets(b).some(t=>t._retinaId==='weapon');
    sg10Reset();sg10Death(b);out[code+' '+diff+' defeat begins physical module breakup']=b.dead&&b.hp===0&&SG10.debris.length===7&&SG10.debris.every(d=>!('alpha' in d));
    sg10FXTick(.5);out[code+' '+diff+' detached modules visibly spin']=SG10.debris.some(d=>Math.abs(d.spin)>0);
    sg10FXTick(1.5);sg10Tick(b,2.6);out[code+' '+diff+' defeat releases the miniboss slot']=subBoss===null&&!subBossActive&&subBossDone;
   }
   const unit='sonic',bank='sonic_explosion';run.stage=1;diffKey='normal';DIFF=difficultyForRun('arcade','normal');spawnSubBoss__inner('siegesonic');subBoss.enter=false;subBoss.y=subBoss.ty;sg10Sync(subBoss);
   const q={x:player.x,y:VH-80,_sg10Unit:unit,_sg10Owner:subBoss,_sg10Charged:true};sg10Detonate(q,true);const burst=SG10.fx.find(q=>q.charged);
   out['Charged sonic bloom retains the approved one-third footprint']=!!burst&&Math.abs(SG10_METRICS[bank].peakInk*burst.k**2/(viewW()*PLAY.h)-.33)<1e-8;
   const harmless={x:player.x,y:VH-100,_sg10Unit:'deviator',_sg10Owner:subBoss,_sg10Charged:false};ordnanceBreak1002(harmless);
   out['Intercepted missiles explode without creating a damage field']=harmless._intercepted&&harmless._sg10Done&&!SG10.fx.at(-2).hazard;
  }finally{playerHit=old.hit;dropPowerup=old.drop;_dmgSrc=old.src;_dmgBullet=old.bullet;}
  return out;
 })())`,c));
 for(const [name,pass]of Object.entries(result))ok(pass,name);
};
