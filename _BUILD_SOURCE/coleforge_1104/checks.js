()=>{
 const results=[];const ck=(ok,name,data)=>results.push({ok:!!ok,name,data});
 const save=campSnapshot();run.spaceLevels=[1,1,1];sa114Ensure();ck(JSON.stringify(run.spaceLevels)==='[1,1,1,0,0]','legacy space array migrates with unowned new guns');
 for(const w of[3,4]){
  run.spaceLevels[w]=0;applyPowerup({kind:'weapon',spaceType:w,wtype:w});ck(run.spaceLevels[w]===1&&run.spaceWeapon===w,'first pickup starts tier1 '+w);
  for(let i=0;i<8;i++)applyPowerup({kind:'weapon',spaceType:w,wtype:w});ck(run.spaceLevels[w]===5,'upgrade caps at5 '+w);
 }
 run.spaceWeapon=4;applyPowerup({kind:'weapon',spaceType:2,wtype:2});ck(run.spaceWeapon===4,'Volley Missile pickup never replaces primary');
 ck([3,4,7].every(raw=>spaceWeaponPickupIndex({wtype:raw})===((raw%3)+3)%3),'legacy boss rewards retain original pickup mapping');
 ck(JSON.stringify(crateWeaponPool())==='[0,1,2,3,4]','five space pickup choices');
 for(const w of[3,4]){run._wbag=[w];powerups=[];spawnContainer('crate',player.x,player.y-100);const q=powerups.find(p=>p.kind==='crate');ck(q?.spaceType===w,'native crate carries explicit new weapon tag '+w,q&&{wtype:q.wtype,spaceType:q.spaceType});if(q){breakContainer(q);ck(powerups.some(p=>p.kind==='weapon'&&p.spaceType===w),'broken crate preserves new weapon identity '+w);}}
 let prevSpread=0,prevPlasma=0;
 for(const w of[3,4])for(let lv=1;lv<=5;lv++){
  enemies=[];powerups=[];pBullets=[];run.spaceWeapon=w;run.spaceLevels[w]=lv;run.spaceAkimbo=0;
  const points=spaceShipHardpoints(player.x,player.y,SPACE_SHIP_SIZE).laser;spaceWeaponFire();const A=pBullets.filter(q=>q._cf114),n=w===3?6:2;
  ck(A.length===n,'native fire emits correct round count '+w+'/'+lv);
  ck(points.every(h=>A.some(q=>Math.abs(q.x-h.x)<.01&&Math.abs(q.y-(h.y-6))<.01)),'both measured cannon ports '+w+'/'+lv);
  ck(A.every(q=>q.kind==='spaceLaser'&&q.vy<0&&Number.isFinite(q.dmg+q.vx+q.vy)),'native collision kind and forward velocity '+w+'/'+lv);
  ck(w===3?A.some(q=>q.vx<-1)&&A.some(q=>q.vx>1)&&A.some(q=>Math.abs(q.vx)<.01):A.every(q=>Math.abs(q.vx)<.01),'spread fan / straight plasma '+w+'/'+lv);
  const D=A[0].dmg;ck(D>(w===3?prevSpread:prevPlasma),'increasing damage '+w+'/'+lv);if(w===3)prevSpread=D;else prevPlasma=D;
  const q=A[0],oldY=q.y;spaceBulletTick(q,1/60);ck(q.y<oldY&&!q.dead,'native projectile tick '+w+'/'+lv);
  spaceImpact(q,'laser',lv,32);ck(q.kind==='spaceImpact'&&q._cf114,'native impact retains supplied family '+w+'/'+lv);spaceBulletTick(q,.21);ck(q.dead,'native impact cleanup '+w+'/'+lv);
 }
 run.spaceWeapon=4;run.spaceLevels[4]=5;run.spaceAkimbo=1;pBullets=[];spaceWeaponFire();ck(pBullets.filter(q=>q._cf114).length===4,'Akimbo uses four forward plasma ports');run.spaceAkimbo=0;
 const A=campSnapshot();run.spaceLevels=[1,1,1,0,0];run.spaceWeapon=0;campApply(A);ck(run.spaceWeapon===4&&run.spaceLevels[3]===5&&run.spaceLevels[4]===5,'new tiers and equipped weapon survive save load');
 const legacy={...A};delete legacy.spaceArsenal;campApply(legacy);ck(JSON.stringify(run.spaceLevels)==='[1,1,1,0,0]'&&run.spaceWeapon===0,'old saves load safely without new arsenal field');campApply(A);
 const ground=JSON.stringify(run._groundLoadout);spaceModeStage(6);ck(!run.spaceMode,'return to ground retains normal loadout owner');spaceModeStage(9);ck(run.spaceLevels[4]===5&&run.spaceWeapon===4,'Stage9 retains upgraded arsenal');
 const pool=crateWeaponPool();ck(pool.includes(3)&&pool.includes(4),'Stage9 can drop both additions');
 for(const w of[3,4]){const P=forgePreviewNew(0,null,5);P.space=w;for(let i=0;i<5;i++)forgePreviewTick(P,260,300,.05);ck(!P.err&&P.bullets.some(q=>q._cf114===sa114Family(w)),'native Armory preview fires new weapon '+w,{error:P.err,rounds:P.bullets.length});}
 ck(polishCollection().filter(q=>q.space===3||q.space===4).length===2,'Armory collection includes both additions');
 // Native target damage. No fake collision renderer or alternate damage path.
 run.stage=5;run.spaceMode=true;run.spaceWeapon=4;run.spaceLevels[4]=1;enemies=[];powerups=[];pBullets=[];
 const h=spaceShipHardpoints(player.x,player.y,SPACE_SHIP_SIZE).laser[0];const E=spawnEnemy('s5skimmer',h.x,h.y-110,{});const hp=E.hp;spaceWeaponFire();for(let i=0;i<20;i++)for(const q of pBullets)if(!q.dead)spaceBulletTick(q,1/60);
 ck(E.hp<hp||E.dead,'Plasma damages a real native Stage5 enemy',{before:hp,after:E.hp,dead:E.dead});
 // New ordinary bullets do not acquire interception flags; native physical missiles keep theirs.
 const ordinary={kind:'s1bullet',hp:2,shootable:true};ck(!enemyOrdnanceCanIntercept(ordinary),'ordinary boat fire remains unshootable');
 const missile={kind:'missile',hp:2,shootable:true};ck(enemyOrdnanceCanIntercept(missile),'physical missiles remain interceptable');
 // Shared damage/visual owners retain lifecycle and safe queue caps.
 enemies=[];eBullets=[];powerups=[];pBullets=[];CFX114.fx=[];nukeImpacts=[];explosions=[];nukeAt(player.x,player.y-150);
 ck(CFX114.fx.some(f=>f.kind==='cole_nuke')&&explosions.length>=2&&explosions.every(q=>q._cf114Nuke),'Cole nuke uses new animation with native explosion owner');
 ck(nukeImpacts.some(q=>q._cf114),'native nuke impact suppression is scoped');
 const F=CFX114.fx[0],before=F.t;updateEffects(.1);ck(F.t>before,'new FX use native game-time update');
 for(let i=0;i<40;i++)cfx114Spawn('small',100,100,40);ck(CFX114.fx.length<=24,'supplementary FX cap24');
 updateEffects(4);ck(CFX114.fx.length===0,'expired FX fully clean up');
 const owner={x:100,y:200,w:80,h:80};const f=cfx114Spawn('fire',100,200,48,{owner,ox:4,oy:8});owner.x+=30;owner.y+=10;updateEffects(.01);ck(f.x===134&&f.y===218,'new fire stays anchored to current owner');
 // Decorative atomic smoke cannot create hits outside the native hazard upper bound.
 const N=ca111FX('nuclear_blast',240,200,460,true);ck(N._cf114Atomic==='atomic_512','strategic warhead selects large32-frame atomic bank');N.t=1.5;ck(!ca111HazardTouches(N,{x:240,y:200}),'atomic aftermath smoke is harmless');
 return results;
}
