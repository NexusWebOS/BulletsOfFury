const fs=require('fs'),path=require('path'),Module=require('module');
const ROOT=path.resolve(__dirname,'..');
const harness=fs.readFileSync(path.join(ROOT,'_BUILD_SOURCE/test_fl.js'),'utf8');
const boot=harness.slice(0,harness.indexOf('/* top-level const/let'));
const test=`
const result=vm.runInContext(\`(()=>{
 const checks=[];const check=(v,n)=>{checks.push({name:n,ok:!!v});if(!v)throw Error(n);};
 const art={
  hq_space_box_0915:'fury_hq_box.png',hq_space_helper_icon_0915:'helper_orb_icon.png',
  hq_space_akimbo_icon_0915:'akimbo_icon.png',hq_space_mine_icon_0915:'proximity_mine_icon.png',
  hq_space_helper_0915:'helper_orb.png',hq_space_mine_0915:'proximity_mine.png',
  hq_space_shrapnel_long_0915:'shrapnel_long.png',hq_space_shrapnel_forked_0915:'shrapnel_forked.png'};
 for(const k in art)check(XART._src[k]==='assets/game/ui/space_armory_0915/'+art[k],k+' registered');
 run.stage=5;run.spaceMode=true;run.spaceLevels=[3,3,3];run.spaceWeapon=0;run.spaceAkimbo=0;
 enemies.length=0;powerups.length=0;pBullets.length=0;spaceHelpers.length=0;spaceMines.length=0;boss=null;bossActive=false;
 run._spaceArmoryBag=[];const bag=[spaceArmoryRoll(),spaceArmoryRoll(),spaceArmoryRoll()];
 check(new Set(bag).size===3&&bag.every(k=>SPACE_ARMORY_REWARDS.indexOf(k)>=0),'RNG bag deals all three rewards once per cycle');
 const box=spaceArmorySpawnBox(210,90,'spacehelper');check(box&&box.kind==='hqspacebox'&&box._hqReward==='spacehelper'&&box.hp===9,'Fury HQ box bakes its reward and is shootable');
 box.dead=true;breakContainer(box);check(powerups.some(p=>p.kind==='spacehelper'),'broken HQ box releases its baked helper icon');
 pBullets.length=0;run.spaceAkimbo=0;spaceLaserFire();check(pBullets.filter(b=>b.kind==='spaceLaser').length===12,'standard laser remains dual across six authored pulses');
 pBullets.length=0;spaceArmoryGrant('spaceakimbo',player.x,player.y);spaceLaserFire();check(pBullets.filter(b=>b.kind==='spaceLaser').length===24,'Akimbo makes Laser Cannon quad across all six pulses');
 pBullets.length=0;run.spaceWeapon=1;spaceShadowRelease(SPACE_SHADOW_FULL_CHARGE);check(pBullets.filter(b=>b.kind==='shadowOrb').length===2,'Akimbo launches two independently travelling Shadow Orbs');
 pBullets.length=0;spaceVolleyLaunchRack(3);check(pBullets.filter(b=>b.kind==='spaceVolley').length===4,'Akimbo converts Volley Missiles to a four-missile rack');
 pBullets.length=0;run.spaceWeapon=0;spaceArmoryGrant('spacehelper',player.x,player.y);enemies.push({x:player.x,y:player.y-170,w:30,h:30,hp:80,maxhp:80,dead:false,score:10});
 spaceArmoryTick(.6);check(spaceHelpers.length===1&&pBullets.some(b=>b.kind==='spaceHelperBeam'),'helper orb orbits and independently fires at a forward target');
 spaceHelpers.length=0;pBullets.length=0;enemies.length=0;const victim={x:player.x,y:player.y-24,w:32,h:32,hp:100,maxhp:100,dead:false,score:10};enemies.push(victim);
 spaceArmoryGrant('spacemine',player.x,player.y);spaceMines[0].arm=0;spaceArmoryTick(.01);
 check(spaceMines.length===0&&victim.hp===80,'armed proximity mine triggers and applies splash damage in range');
 check(pBullets.filter(b=>b.kind==='spaceShrapnel').length===12,'mine detonation launches twelve damaging shrapnel projectiles');
 const oldR=XART.rdy,oldG=XART.get,oldD=ctx.drawImage,calls=[];XART.rdy=k=>/^hq_space_/.test(k);XART.get=k=>({naturalWidth:320,naturalHeight:300,_key:k});ctx.drawImage=(im)=>calls.push(im._key);
 for(const kind of ['hqspacebox','spacehelper','spaceakimbo','spacemine'])check(drawSpaceArmoryPickup({kind,x:100,t:1},130),kind+' uses dedicated generated art');
 check(new Set(calls).size===4,'crate and three reward icons render as independent art');XART.rdy=oldR;XART.get=oldG;ctx.drawImage=oldD;
 return {passed:checks.length,failed:0,checks};
})()\`,ctxv);console.log(JSON.stringify(result,null,2));`;
const m=new Module(__filename,module);m.filename=__filename;m.paths=module.paths;m._compile(boot+test,__filename);
