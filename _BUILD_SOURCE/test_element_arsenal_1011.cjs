'use strict';
module.exports=function(vm,c,ok){
 const fs=require('fs'),path=require('path');
 for(const [file,symbol]of [['element_arsenal_art_1011.js','EA11_ART'],['element_arsenal_1011.js','PA11']])
  if(vm.runInContext('typeof '+symbol,c)==='undefined')vm.runInContext(fs.readFileSync(path.join(__dirname,'../assets',file),'utf8'),c,{filename:file});
 console.log('=== Nine elemental player arsenals 1011 ===');
 const out=JSON.parse(vm.runInContext(`JSON.stringify((()=>{
  const out={};ht27Stop();coopOn=false;run.mode='arcade';run.pilot='cole';beginStage(1);state=GS.PLAY;
  BOFCinematicDirector.cancel();story=fb2Talk=special=null;player.reset();player.dead=player.out=false;player.invuln=999;
  boss=subBoss=null;bossActive=subBossActive=false;enemies=[];pBullets=[];eBullets=[];stagePlan=[];
  const elements=Object.keys(EA11_FAMILIES);
  out['Nine families map once each to the nine boss rewards']=elements.length===9&&new Set(elements.map(e=>EA11_FAMILIES[e].stage)).size===9&&elements.every(e=>BOSS_ELEMENT_BY_STAGE[EA11_FAMILIES[e].stage]===e);
  for(const e of elements){
   out[e+' has nine named recipes and registered menu badges']=FORGE_WEAPONS.every(w=>!!FORGE_NAMES[e][w]&&!!XART._src[forgeBadgeKey(e,w,1)]);
  }
  out['Sixteen new banks contain sixteen real even-sized poses each']=Object.values(EA11_ART.banks).length===16&&Object.values(EA11_ART.banks).every(a=>a.frames.length===16&&a.frames.every(r=>r.every(n=>n%2===0))&&a.size.every(n=>n===128));
  for(const e of elements.filter(e=>e!=='wind')){
   const b={kind:'missile',x:100,y:180,vx:0,vy:-4,lv:3};ea11Stamp(b,{elem:e,lv:4},2);
   run.infusion={elem:'wind',lv:1};run.weapon=0;ea11Stamp(b,run.infusion,1);
   out[e+' round retains its launch element, tier and seat after switching']=b._inf===e&&b._el===e&&b._infLv===4&&b.seat===2&&ea11Bank(b)===EA11_ART.banks[e+'_missile'];
  }
  const source={kind:'lasermist',x:140,y:200,lv:3,dmg:4,seat:2,_inf:'water',_infLv:4,_el:'water',_mistLedger:{hits:[]}};
  pBullets=[];run.infusion={elem:'fire',lv:1};laserMistChild(source,1,0,-9,0);const child=pBullets[0];laserMistChild(child,2,1,-9,1);
  out['Both mist splits inherit source element, level, ledger and seat']=pBullets.length===2&&pBullets.every(b=>b._inf==='water'&&b._infLv===4&&b._el==='water'&&b.seat===2&&b._mistLedger===source._mistLedger);
  pBullets=[];yuriLightningOrbRelease({...source,kind:'yuriLightningOrb'});
  out['Sphere discharges retain their owner and element']=pBullets.length>0&&pBullets.every(b=>b.seat===2&&b._el==='water'&&b._inf==='water');
  const lance={kind:'mavlaser',lv:1,dmg:2};ea11Stamp(lance,{elem:'dark',lv:5},2);
  out['Maverick homing lances remain outside all infusion and art upgrades']=lance.lv===1&&lance.dmg===2&&lance._inf===undefined&&ea11Role(lance)===null;
  const neutral={kind:'mg',_inf:null};run.infusion={elem:'toxic',lv:5};out['Bare rounds never borrow the currently equipped element']=ea11Element(neutral)===null;
  const held={kind:'beam',_inf:'fire',_infLv:3};ea11Stamp(held,{elem:'ice',lv:2},1,true);
  out['Held beams refresh on their own trigger']=held._inf==='ice'&&held._infLv===2;
  const bare={kind:'beam'};ea11Stamp(bare,{elem:'water',lv:1},1);ea11Stamp(bare,null,1,true);
  out['Unforging a held beam removes the previous damage element']=bare._inf===null&&bare._el===undefined&&damageProjectileElement(bare)!=='water';
  _dmgBullet={kind:'flame',_inf:'water',_el:'fire'};out['A forged water spray has water damage, never hidden fire damage']=attackElement('flame')==='water'&&damageProjectileElement(_dmgBullet)==='water';_dmgBullet=null;
  function target(x=220){return {x,y:170,w:24,h:24,hp:1000,maxhp:1000,vx:2,vy:2,t:0,kind:'scout',type:'scout',dead:false,_entry:0};}
  function hit(el){let e=target();enemies=[e];pBullets=[];eBullets=[];run.infusion={elem:'fire',lv:1};efxClock+=1;
   const b={kind:'mg',x:200,y:190,vx:0,vy:-9,lv:3,_inf:el,_infLv:3,seat:2};_dmgBullet=b;infusionOnHit(e,b,2);_dmgBullet=null;return e;}
  out['Fire applies a burning duration from the fired round']=hit('fire')._burn>0;
  out['Ice freezes at the fired tier despite a different current element']=hit('ice')._frozen>0;
  out['Sonic pressure moves ordinary enemies']=hit('kinetic').y<170;
  out['Water soaks targets']=hit('water')._soaked>0;
  out['Toxic applies its fired poison tier']=hit('toxic')._poisonLv===3;
  out['Wind applies a bounded push']=!!hit('wind')._ap10Gust;
  let e=target(),other=target(260);enemies=[e,other];efxClock+=1;_dmgBullet={kind:'mg',lv:2,_inf:'lightning',_infLv:1};infusionOnHit(e,_dmgBullet,2);_dmgBullet=null;
  out['Lightning actually damages a second target']=other.hp<1000;
  e=target();other=target(260);enemies=[e,other];infusionOnHit(e,{kind:'mg',_inf:'dark',_infLv:1},2);
  out['Dark matter pulls neighboring ordinary targets inward']=other.x<260;
  eBullets=[{kind:'emg',x:220,y:170,vx:0,vy:3,w:6,h:8}];pBullets=[];_dmgBullet={kind:'mg',_inf:'chrome',_infLv:2,seat:2};infusionOnHit(target(),_dmgBullet,2);_dmgBullet=null;
  out['Chromium reflections remain attributed to their firing pilot']=eBullets[0].dead&&pBullets.some(b=>b._mirror&&b.seat===2&&b._inf==='chrome'&&b._infLv===2);
  boss=target();const y=boss.y;infusionOnHit(boss,{kind:'mg',_inf:'kinetic',_infLv:3,x:200},2);
  out['Sonic cannot dislodge a mounted boss']=boss.y===y;boss=null;
  function sonicDamage(current){const e=target();enemies=[e];run.infusion=current;_dmgBullet={kind:'mg',_inf:'kinetic',_infLv:2,lv:1,x:220,y:200,seat:1};hitEnemy(e,10);_dmgBullet=null;return 1000-e.hp;}
  out['A Sonic hit keeps identical damage after changing or removing the equipped infusion']=sonicDamage({elem:'fire',lv:5})===sonicDamage(null);
  pBullets=[];iceBurst(220,170,6,3,{el:'ice',forge:true,forgeLv:2,seat:2});
  out['Orb shrapnel preserves its original pilot and element']=pBullets.length===6&&pBullets.every(b=>b.seat===2&&b._inf==='ice'&&b._infLv===2);
  const locked=target();locked._mercuryLock=.7;locked._mercurySource={seat:2,_infLv:2};locked.hp=0;enemies=[locked];pBullets=[];run.infusion={elem:'fire',lv:5};killEnemy(locked);
  out['Chromium destruction splinters keep the pilot who applied the lock']=pBullets.some(b=>b._mirror)&&pBullets.filter(b=>b._mirror).every(b=>b.seat===2&&b._infLv===2&&b._inf==='chrome');
  return out;
 })())`,c));
 for(const [name,passed]of Object.entries(out))ok(passed,'Arsenal1011: '+name);
};
