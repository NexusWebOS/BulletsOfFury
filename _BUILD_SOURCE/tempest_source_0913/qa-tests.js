// ===== 294. APPROVED STAGE-6 TEMPEST BROTHERS, NATIVE CAMPAIGN ADAPTER (0913) =====
console.log('=== 294. Tempest brothers ===');
{
  var _pre294="ASSETS.ready=true;run.stage=6;curStage=STAGES[5];player.dead=false;player.roll=null;player.somer=null;player.x=240;player.y=400;subBoss=null;subBossActive=false;subBossDone=false;eBullets.length=0;playerLocks=[];spawnSubBoss('tempestbrothers');var b=subBoss,D=b._tempestDuo;";
  vm.runInContext(_pre294,ctxv);
  ok(vm.runInContext("SUBBOSS[6].kind==='tempestbrothers'&&ALTBOSS[6].kind==='blacksteel'",ctxv),'Stage 6 fields the approved brothers and retains Blacksteel');
  ok(vm.runInContext("D.ships.length===2&&D.ai.black!==D.ai.gray&&D.ai.black.rig!==D.ai.gray.rig",ctxv),'two independent ships and aperture pools');
  ok(vm.runInContext("b.hp===b.maxhp&&D.ai.black.hp===8000&&D.ai.gray.hp===8000",ctxv),'combined bar starts full after the native encounter HP floor');
  ok(vm.runInContext("BOFX.img.tlvb_hull&&BOFX.img.tlvb_hull_damaged",ctxv)&&fs.existsSync(path.join(ROOT,'assets/game/bosses/tempest/tlvb_hull.png'))&&fs.existsSync(path.join(ROOT,'assets/game/bosses/tempest/tlvb_hull_damaged.png')),'both authored gray hull states are registered and on disk');
  ok(vm.runInContext("bossmodeArtKeys('tempestbrothers').some(k=>k==='tlvb_hull')&&debugFightFor(6,'mini').name==='TEMPEST LEVIATHAN BROTHERS'",ctxv),'Boss Mode names and browses both brothers');
  vm.runInContext("D.ai.black.enter('chase');D.ai.gray.enter('chase');D.ai.black.boss.x=200;D.ai.gray.boss.x=700;D.ai.black.boss.y=D.ai.gray.boss.y=230;D.ai.black.vulnerable=D.ai.gray.vulnerable=true;tempestBrothersSync(b);",ctxv);
  ok(vm.runInContext("tempestBrothersPartAt(b,D.ships[0].x,D.ships[0].y)==='Bhull'&&tempestBrothersPartAt(b,D.ships[1].x,D.ships[1].y)==='Ghull'",ctxv),'hull hits identify the correct brother');
  ok(vm.runInContext("subBossSolidAt(tlvX(450),tlvY(230))===false&&!tempestBrothersContact(b,tlvX(450),tlvY(230))",ctxv),'empty air between brothers blocks neither pellets nor the player');
  vm.runInContext("var p=D.ships[0],port=tempestPortXY(p,1),gHP=D.ai.gray.hp;hitSubBoss(b.maxhp*0.01,port.x,port.y);",ctxv);
  ok(vm.runInContext("D.ai.black.rig[1].hp<300&&D.ai.black.hp===8000&&D.ai.gray.hp===gHP&&D.ai.gray.rig.every(r=>r.hp===300)",ctxv),'a port hit consumes only its own aperture pool');
  ok(vm.runInContext("D.ships[0].flash>0&&D.ships[1].flash===0",ctxv),'only the struck brother flashes');
  vm.runInContext("hitSubBoss(b.maxhp,port.x,port.y);",ctxv);
  ok(vm.runInContext("D.ai.black.rig[1].hp===0&&D.ai.black.hp===7910&&D.ai.gray.hp===8000",ctxv),'a silenced aperture costs only its own hull the reviewed 90 HP');
  vm.runInContext("hitSubBoss(b.maxhp*10,D.ships[0].x,D.ships[0].y);",ctxv);
  ok(vm.runInContext("D.ai.black.hp===6000&&D.ai.black.phase==='overtake'&&D.ai.gray.hp===8000&&b.hp/b.maxhp===0.875",ctxv),'independent black 75% gate preserves gray HP and sums the combined bar');
  ok(vm.runInContext("tempestBrothersPartAt(b,D.ships[0].x,D.ships[0].y)===null",ctxv),'the crossing brother is unhittable');
  vm.runInContext("D.ai.gray.boss.x=-190;D.ai.gray.boss.y=300;D.ai.gray.change('regroup');var px=player.x,py=player.y;for(var i=0;i<10;i++)tempestBrothersUpdate(b,1/60);",ctxv);
  ok(vm.runInContext("D.ai.holds>0&&D.ai.gray.entryWarn===null&&!D.ships[1]._tlv.vuln",ctxv),'gray holds offscreen without a warning or hitbox during black crossing');
  ok(vm.runInContext("player.x===px&&player.y===py",ctxv),'native duo movement never moves the player');
  vm.runInContext("D.ai.black.enter('pursuit');D.ai.gray.change('warn');D.ai.black.change('ram-warn');",ctxv);
  ok(vm.runInContext("D.ai.black.state==='row'&&D.ai.black.deferred>0",ctxv),'a warned inbound gray crossing defers the black side ram');
  vm.runInContext("D.ai.black.enter('chase');D.ai.black.boss.y=230;D.ai.black.change('laser-track');D.ai.gray.planRun();",ctxv);
  ok(vm.runInContext("D.ai.pincers>0&&D.ai.gray.entryWarn.run==='pincer'&&D.ai.gray.start.y>D.ai.black.boss.y&&D.ai.gray.start.y<D.ai.player.y",ctxv),'gray pincer crosses between black rear lasers and the player');
  vm.runInContext("D.ai.black.hp=0;D.ai.black.enter('death');for(var i=0;i<205;i++)tempestBrothersUpdate(b,1/60);",ctxv);
  ok(vm.runInContext("D.ai.black.gone&&D.ai.alone&&!b.dead&&D.ai.gray.hp>0",ctxv),'one falling reactor leaves the survivor fighting without completing the encounter');
  ok(vm.runInContext("D.ai.gray.speedFor('cross')>1050*1.14",ctxv),'the surviving gray brother receives its reviewed 15% speed increase');
  vm.runInContext("D.ai.gray.hp=0;D.ai.gray.enter('death');for(var i=0;i<205;i++)updateSubBoss(1/60);",ctxv);
  ok(vm.runInContext("b.dead&&b.hp===0&&!subBossDone",ctxv),'both reactors trigger the ordinary miniboss completion once');
  vm.runInContext("for(var i=0;i<130;i++)updateSubBoss(1/60);",ctxv);
  ok(vm.runInContext("subBoss===null&&!subBossActive&&subBossDone&&player.x===px&&player.y===py",ctxv),'ordinary slot release completes without moving the player into a standalone escape');
  vm.runInContext("subBoss=null;subBossActive=false;subBossDone=false;eBullets.length=0;playerLocks=[];",ctxv);
}
