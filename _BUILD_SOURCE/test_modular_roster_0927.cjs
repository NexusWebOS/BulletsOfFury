module.exports=function(vm,ctxv,ok){
 const fs=require('fs'),path=require('path');
 for(const file of ['modular_roster_art_0927.js','modular_roster_0927.js'])vm.runInContext(fs.readFileSync(path.join(__dirname,'../assets',file),'utf8'),ctxv,{filename:file});
 console.log('=== Corrected modular roster and difficulty routes, September 27 ===');
 const out=JSON.parse(vm.runInContext(`JSON.stringify((()=>{
  const o={};
  const fixture=(stage,kind,mini,diff)=>{run.mode='arcade';run.stage=stage;run.pilot='cole';curStage=STAGES[stage-1];diffKey=diff;DIFF=DIFFS[diff];boss=null;subBoss=null;enemies=[];eBullets=[];pBullets=[];player.dead=false;player.x=240;player.y=420;camX=0;groundTargetingReset();polishReset();if(mini)spawnSubBoss__inner(kind);else spawnBoss(kind);const b=mini?subBoss:boss;b.enter=false;b._be=null;b._noHit=false;b.x=worldWidth()/2;b.y=b.ty||170;b._drawY=b.y;return b;};
  for(const diff of ['easy','normal','hard','furious']){diffKey=diff;DIFF=DIFFS[diff];
   o[diff+' intended true-route eligibility']=mr27TrueRoute()===['furious','insanity'].includes(diffKey);
   for(const [stage,kind,mini]of [[3,'cryospear',false],[4,'olivewarden',true],[4,'stormsovereign',false]]){
    const b=fixture(stage,kind,mini,diff);if(b._s4war?.shield){b._s4war.shield.active=false;b._s4war.shield.rearming=false;}
    b._er26.neutralOpening=false;const p=b._mr27.parts[0],q=mr27Shape(b,p.id),old=b.hp;
    _lastHitX=q.x;_lastHitY=q.y;_dmgBullet=null;const loss=mr27Damage(b,p.hp+100,q.x,q.y);
    o[diff+' '+kind+' mounted cannon is destructible']=p.dead&&loss===p.maxhp&&!mr27CanFire(b,'L');
    o[diff+' '+kind+' break cancels attack and gives recovery']=b._mr27.stun>0&&b._er26.mode==='recover'&&!b._l23Beam;
    const n=eBullets.length;if(stage===3)er26Shot(b,'L',Math.PI/2,3);else er26WarShot(b,'L',Math.PI/2,3,'mg');
    o[diff+' '+kind+' broken cannon cannot fire']=eBullets.length===n&&b.hp===old;
    const rocket=mr27Part(b,'rocketR'),r=mr27Shape(b,'rocketR');mr27Damage(b,rocket.hp+1,r.x,r.y);
    o[diff+' '+kind+' rocket rack uses independent pool']=rocket.dead&&!mr27Part(b,'gunR').dead;
   }
   for(const stage of [5,6]){
    const b=fixture(stage,SUBBOSS[stage].kind,true,diff),B=b._bomber;
    o[diff+' stage '+stage+' correct bomber and full private HP']=!!B&&B.space===(stage===5)&&b.hp===b.maxhp&&b.hp===B.core+B.parts.reduce((a,p)=>a+p.hp,0);
    const q=siegeBomberParts(b).find(p=>p.id==='laserL');siegeBomberSet(b,'charge');siegeBomberHit(b,B.parts.find(p=>p.id==='laserL').hp+1,q.x,q.y,'laserL');
    o[diff+' stage '+stage+' shooting laser cancels charge']=B.mode==='recover'&&B.parts.find(p=>p.id==='laserL').hp===0;
   }
   const b=fixture(8,'vileexistence',false,diff);vileBuildForm(b,2);b.enter=false;b._v24.shield=0;
   for(const p of b.parts){if(p.dmg){p.hp=1;b._lastPart=p;modularHit(9999);if(!p.destroyed){b._lastPart=p;modularHit(9999);}}}
   o[diff+' final boss stops or reveals true form correctly']=diff==='furious'?b._vForm===3&&!b.dead:b.dead&&b._vForm===2;
  }
  const hb=fixture(4,'stormsovereign',false,'hard');stage4CoreTurretSpawnMissing(hb,.5);const hd=hb._s4war.coreTurrets[0];hd.materialize=1;
  const hg=mr27HelperState(hd),hq=mr27HelperGun(hb,hd),he=stage4HelperExtent(hd);_lastHitX=hq.x;_lastHitY=hq.y;
  o['Modular helper collision matches compact 96px art']=he.x===48&&he.y===48&&hq.h===96*.62;
  hd.shield=100;const before=hg.hp;mr27HelperDamage(hb,hd,1000);
  o['Helper shield protects its mounted gun']=hg.hp===before&&!hg.dead;
  hd.shield=0;mr27HelperDamage(hb,hd,hg.hp+1);
  o['Helper cannon can break while hull survives']=hg.dead&&hg.hp===0&&!hd.dead;
  o['Easy encounter HP floor respects handicap']=(()=>{diffKey='easy';DIFF=DIFFS.easy;return encounterFloorDifficultyMul(6)===.48;})();
  return o;
 })())`,ctxv));
 for(const [name,result]of Object.entries(out))ok(result,name);
 const art=JSON.parse(vm.runInContext('JSON.stringify(MR27_ART)',ctxv));
 for(const [name,d]of Object.entries(art))ok(fs.existsSync(path.join(__dirname,'..',d.path))&&d.cells.length===(name==='corefx'?8:6),name+' generated sheet and measured cells exist');
};
