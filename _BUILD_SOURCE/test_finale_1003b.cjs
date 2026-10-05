module.exports=function(vm,ctxv,ok){
 const fs=require('fs'),path=require('path');
 for(const f of ['primary_1003b.js','finale_art_1003b.js','finale_1003b.js'])vm.runInContext(fs.readFileSync(path.join(__dirname,'../assets',f),'utf8'),ctxv,{filename:f});
 console.log('=== All-pilot late-stage chainguns and eight-life alien finale ===');
 const result=JSON.parse(vm.runInContext(`JSON.stringify((()=>{
 const out={};ht27Stop();debugFight=null;coopOn=false;diffKey='furious';DIFF=DIFFS.furious;
 for(const p of PILOTS){
  pilotIndex=PILOTS.indexOf(p);chaingunUnlocked=false;startRun(7);BOFCinematicDirector.cancel();story=null;setState(GS.PLAY);
  out[p.key+' password defaults to the mounted chaingun']=run.weapon===7&&run.wlevel>=1&&run.loadout.includes(7)&&!run.loadout.includes(0)&&chaingunReplacesMG();
  const old=campSnapshot();delete old.primary1003b;old.earnedUnlocks={};old.weapon=0;old.loadout=[0,1,2,3,4];campApply(old);
  out[p.key+' old Stage 7 save migrates its primary']=run.weapon===7&&run._earnedUnlocks.chaingun;
  const switchMG=weaponBaseForms(7).find(o=>o.id==='mg');weaponFormSelect(7,switchMG);const saved=campSnapshot();
  run._primary1003b='chain';campApply(saved);beginStage(8);
  out[p.key+' deliberate MG choice survives save and next stage']=run._primary1003b==='mg'&&!chaingunReplacesMG()&&run.loadout.includes(0)&&!run.loadout.includes(7);
  weaponFormSelect(0,weaponBaseForms(0).find(o=>o.id==='chain'));run.weapon=0;chaingunMGSync();
  out[p.key+' switching back restores chaingun respawn primary']=run.weapon===7&&chaingunReplacesMG();
 }
 function reset(diff){diffKey=diff;DIFF=DIFFS[diff];run.mode='campaign';run.pilot='yuri';beginStage(8);setState(GS.PLAY);player.reset();BOFCinematicDirector.cancel();story=null;special=null;stagePlan=[];enemies=[];eBullets=[];pBullets=[];groundTargetingReset();boss=null;bossActive=false;spawnBoss('vileexistence');bossActive=true;player.x=worldWidth()/2;player.y=VH-90;player.invuln=1e9;return boss;}
 for(const diff of ['easy','normal','hard','furious']){
  const b=reset(diff),S=b._r30;S.t=4.8;
  out[diff+' introduction fills eight distinct life rows']=f1003bBarFractions(b).length===8&&f1003bBarFractions(b).every(f=>f===1)&&new Set(F1003B_FORMS.map(d=>d.color)).size===8;
  const initialScore=run.score;
  for(let form=0;form<8;form++){
   r30Form(b,form);S.mode='fight';b.enter=false;
   const id=f1003bDef(b).id,book=f1003bDef(b).book;
   out[diff+' '+id+' starts whole with its own finite HP']=b.parts.every(p=>p.hp>0&&!p.destroyed)&&b.hp===S.pools[form]&&Number.isFinite(b.hp);
   for(let atk=0;atk<book.length;atk++){
    eBullets=[];groundTargetingReset();S.orbitals=[];S.attack=null;r30Attack(b);
    const P=S.attack,tx=P.tx,ty=P.ty;let frames=0;
    while(S.attack&&frames++<2000)r30Tick(b,1/60);
    out[diff+' '+id+' '+book[atk]+' completes with recovery']=!S.attack&&S.cd>0&&frames<2000&&P.tx===tx&&P.ty===ty&&Number.isFinite(b.x+b.y);
   }
   b._lastPart=b.parts[0];modularHit(b.hp+100);
   out[diff+' '+id+' exhaustion clears hazards without early reward']=b.hp===0&&S.mode===(form===7?'finalFall':'morph1003b')&&run.score===initialScore&&groundTargetingFx.every(q=>q.owner!==b||q.dead);
   if(form<7){for(let i=0;i<175;i++)r30Tick(b,1/60);out[diff+' advances exactly one form after '+id]=S.form===form+1&&S.mode==='fight'&&b.hp===b.maxhp;}
  }
 }
 for(const stage of [6,8]){pilotIndex=PILOTS.findIndex(p=>p.key==='yuri');startRun(stage);out['password stage '+stage+' defaults to chaingun']=run.weapon===7&&run.loadout.includes(7);}
 run.pilot='yuri';run.stage=7;run.spaceMode=false;gravityMode=null;run.forge={};run.forgeForms={};special=null;
 for(let lv=1;lv<=5;lv++){
  run.weapon=0;run.wlevel=lv;run.wlevels[0]=lv;pBullets=[];pShoot();const mg=pBullets.reduce((a,b)=>a+b.dmg,0)/_weaponCadence();
  run.weapon=7;run.wlevels[7]=lv;pBullets=[];pShoot();const chain=pBullets.reduce((a,b)=>a+b.dmg,0)/_weaponCadence();
  out['chaingun tier '+lv+' exceeds equal-tier bare MG damage rate']=chain>mg;
 }
 const b=reset('furious'),S=b._r30;S.mode='fight';b.enter=false;S.seq=2;r30Attack(b);const arm=b.parts[1];b._lastPart=arm;modularHit(arm.hp);
 out['host arm has an independent break and live core']=arm.destroyed&&b.hp>0&&r30Parts(b).length===2;
 out['breaking a host cannon cancels its committed laser warning']=S.attack.lanes.length===1&&f1003bMuzzles(b).length===1;
 r30Form(b,2);S.mode='fight';b.enter=false;out['furnace uses its whole authored arm plate after host damage']=r30Parts(b).length===1&&r30Parts(b)[0].key==='furnace'&&!b.parts[0].destroyed;
 r30Form(b,5);S.mode='fight';b.enter=false;r30Attack(b);const hp=b.hp;modularHit(9999);
 out['knight wall breaks before hull damage with radial shatter']=S.shield===0&&b.hp===hp&&S81003.effects.some(f=>f.kind==='shatter');
 run.stage=7;enemies=[];for(const wave of buildStagePlan(7))wave.fn();
 out['actual sewer waves replace both remaining toxic pods']=enemies.some(e=>e._mutatorSlot1003==='s7canister')&&enemies.some(e=>e._mutatorSlot1003==='s7mine')&&!enemies.some(e=>e.type==='s7canister'||e.type==='s7mine');
 return out;})())`,ctxv));
 for(const [name,pass]of Object.entries(result))ok(pass,name);
};
