module.exports=function(vm,ctxv,ok){
 /* 1017 - Mike: "bullets and missiles both should be able to individually target modular pieces. Lasers should
    pierce and target all pieces or enemies that the laser will hit. orbs should hit each piece individually ...
    Stage 4 miniboss, he does nothing when all his modular pieces are destroyed."
    Real-Chromium proof: _BUILD_SOURCE/probe_modular_1017.py (every encounter x every weapon) and
    _BUILD_SOURCE/probe_warden_laststand_1017.py (33 checks with a busted arm). */
 const fs=require('fs'),path=require('path');
 console.log('=== 383. Modular pieces: every weapon finds the piece it is aimed at; the Warden fights on ===');
 if(!vm.runInContext('typeof MR27_HULL_MASK',ctxv).includes('object'))
  vm.runInContext(fs.readFileSync(path.join(__dirname,'../assets/mr27_hull_mask_1017.js'),'utf8'),ctxv,{filename:'mr27_hull_mask_1017.js'});
 const r=JSON.parse(vm.runInContext(`JSON.stringify((()=>{
  const o={};
  const fixture=(stage,kind,mini,diff)=>{run.mode='arcade';run.stage=stage;run.pilot='cole';curStage=STAGES[stage-1];diffKey=diff;DIFF=DIFFS[diff];boss=null;subBoss=null;enemies=[];eBullets=[];pBullets=[];player.dead=false;player.x=240;player.y=420;camX=0;groundTargetingReset();polishReset();if(mini)spawnSubBoss__inner(kind);else spawnBoss(kind);const b=mini?subBoss:boss;b.enter=false;b._be=null;b._noHit=false;b.x=worldWidth()/2;b.y=b.ty||170;b._drawY=b.y;return b;};
  o.mask=['iron','rime','storm'].every(k=>MR27_HULL_MASK.rows[k]&&MR27_HULL_MASK.rows[k].length===MR27_HULL_MASK.n);
  const b=fixture(4,'olivewarden',true,'normal');subBossActive=true;
  const g=mr27Shape(b,'gunL'),cy=b._drawY??b.y;
  // a point under the turret: inside the OLD core box (|dy|<h*.44) and below the turret, over bare road
  const ux=g.x,uy=Math.min(cy+b.h*.43,g.y+g.h*.5+12);
  o.oldBox=Math.abs(ux-b.x)<b.w*.37&&Math.abs(uy-cy)<b.h*.44;
  o.underTurret=mr27At(b,ux,uy);
  o.gunCentre=mr27At(b,g.x,g.y);
  o.hullCentre=mr27At(b,b.x,cy);
  o.solidAir=subBossSolidAt(ux,uy);
  o.solidGun=subBossSolidAt(g.x,g.y);
  // a held beam down the left column crosses the gun turret AND the rocket pod above it
  const hp=()=>Object.fromEntries(b._mr27.parts.map(p=>[p.id,p.hp]));const h0=hp();
  const beam={kind:'beam',x:g.x,bot:420,top:-20,w:24,dmg:5,lv:3,_hit:[]};
  o.pierced=beamPiercePieces(b,beam);const h1=hp();
  o.beamGun=h0.gunL-h1.gunL;o.beamRocket=h0.rocketL-h1.rocketL;o.beamRight=(h0.gunR-h1.gunR)+(h0.rocketR-h1.rocketR);
  // the piece list holds each part once
  const L=livePieces(b),keys=L.map(pieceKey);o.unique=new Set(keys).size===keys.length;o.pieces=L.length;
  const near=piecesInCircle(b,g.x,g.y,10);o.nearFirst=near.length>0&&near[0]._retinaId==='mr27-gunL';
  o.circleMiss=piecesInCircle(b,b.x,cy-b.h*2,20).length;
  {const gr=mr27Shape(b,'gunR');b.flash=0;for(const p of b._mr27.parts)p.flash=0;_lastHitX=gr.x;_lastHitY=gr.y;hitSubBoss(3,gr.x,gr.y);
   o.flashPieceHull=b.flash;o.flashPiece=b._mr27.parts.find(p=>p.id==='gunR').flash;
   b.flash=0;let cy2=null;for(let y=b.y-b.h*.3;y<b.y+b.h*.3&&cy2===null;y+=3)if(mr27At(b,b.x,y)==='core')cy2=y;_lastHitX=b.x;_lastHitY=cy2;hitSubBoss(3,b.x,cy2);o.flashHull=b.flash;}
  if(typeof fb10StrikePieces==='function'){
   const h2=hp(),orb={kind:'orb',x:g.x,y:g.y,w:34,h:34,dmg:6,lv:3,seat:1};
   o.orbAll=fb10StrikePieces(orb,b,g.x,g.y-40,60,6,true);const h3=hp();
   o.orbOne=fb10StrikePieces(orb,b,g.x,g.y-40,60,6,false);
   o.orbHitGun=h2.gunL-h3.gunL>0;o.orbHitRocket=h2.rocketL-h3.rocketL>0;
  }else o.orbAll=null;
  return o;})())`,ctxv));
 ok(r.mask,'the hull mask is loaded for all three modular skins');
 ok(r.oldBox&&r.underTurret===null,'a point under the turret was "core" in the old box and is bare road now (got '+r.underTurret+')');
 ok(r.gunCentre==='gunL'&&r.hullCentre==='core','the turret centre is the turret, the hull centre is the core');
 ok(r.solidAir===false&&r.solidGun===true,'the pellet box: a round over bare air flies on, a round on the turret stops (air '+r.solidAir+', gun '+r.solidGun+')');
 ok(r.pierced>=2&&r.beamGun>0&&r.beamRocket>0,'a held beam strikes every piece in its column (pieces '+r.pierced+', gun -'+r.beamGun+', rocket -'+r.beamRocket+')');
 ok(r.beamRight===0,'and nothing outside its column');
 ok(r.flashPiece>0&&r.flashPieceHull===0&&r.flashHull>0,'a module hit flashes the module alone (module '+r.flashPiece+', hull '+r.flashPieceHull+'); a hull hit flashes the hull ('+r.flashHull+')');
 ok(r.unique&&r.pieces>=4,'the live piece list holds each part once ('+r.pieces+' pieces)');
 ok(r.nearFirst&&r.circleMiss===0,'a circle finds the piece it overlaps, nearest first, and nothing it does not');
 if(r.orbAll!==null){
  ok(r.orbAll>=2&&r.orbHitGun&&r.orbHitRocket,'a piercing orb strikes every piece inside its body ('+r.orbAll+')');
  ok(r.orbOne===1,'a contact orb strikes the one piece it touched');
 }
 const strip=s=>s.replace(/\/\*[\s\S]*?\*\//g,'').replace(/(^|[^:'"])\/\/.*$/gm,'$1');
 const idx=fs.readFileSync(path.join(__dirname,'../index.html'),'utf8');
 const a=idx.indexOf('assets/stage34_assault_1014.js'),w=idx.indexOf('assets/warden_last_stand_1017.js'),m=idx.indexOf('assets/mr27_hull_mask_1017.js'),mr=idx.indexOf('assets/modular_roster_0927.js');
 ok(a>0&&w>a,'the last stand loads after the assault layer that owns the Warden');
 ok(m>0&&m<mr,'the hull mask loads before the modular roster');
 const ls=strip(fs.readFileSync(path.join(__dirname,'../assets/warden_last_stand_1017.js'),'utf8'));
 ok(/wls17Exposed\(b\)\)return \['sa14-corefan','sa14-ram'/.test(ls),'an exposed Warden swaps to the core-fan / hull-ram book');
 ok(/sa14Warning\(/.test(ls)&&/combatWarningTick\(b,'warden-core-'/.test(ls)&&/combatWarningTick\(b,'warden-ram-'/.test(ls),'both last-stand attacks warn through the shared warning path');
 ok(/hard:\['S','S','N','N'\]/.test(ls)&&/furious:\['S','S','N','N','E','W'\]/.test(ls)&&/insanity:\['S','S','N','N','E','W'\]/.test(ls),'the orbit wing: Hard 2 south + 2 north, Furious and Insanity add east and west');
 ok(/WING17_RESPAWN=5\.0/.test(ls),'a destroyed wing jet is replaced 5 seconds later');
 ok(!/A\.glow|lightning/i.test(ls.replace(/no lightning|but no lightning/gi,'')),'the Warden layer draws no lightning');
 ok(['wardenGun','wardenRocket','wardenRackCharge','bossWeaponCharge','razorbackCharge','razorbackRam'].every(k=>ls.includes("'"+k+"'")),'every Warden attack names its own sound');
 ok(!/Math\.random/.test(ls),'the last stand draws no random numbers (the wave-plan fixtures read the unseeded stream)');
 const g=strip(fs.readFileSync(path.join(__dirname,'../assets/game.js'),'utf8'));
 ok(/if\(b\._mr27&&typeof mr27At==='function'\)return mr27At\(b,x,y\)!==null;/.test(g),'subBossSolidAt asks the modular pieces');
 ok(/subBossSolidAt\(b\.x,b\.y\)!==false\)\{ reach=true;b\._impactTarget=subBoss;/.test(g),'an unguided missile flies past bare air to the piece it was aimed at');
 ok(/mr27At\(subBoss,player\.x,player\.y\)!==null/.test(g),'body contact with a modular miniboss is its silhouette');
};
