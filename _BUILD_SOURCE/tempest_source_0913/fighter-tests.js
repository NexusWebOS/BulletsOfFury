// ===== 295. MIKE'S SOUTH-FACING TEMPEST FIGHTER PASSES (0913) =====
console.log('=== 295. Tempest fighter turns, slides and red/green thrust ===');
{
  var _pre295="ASSETS.ready=true;run.stage=6;curStage=STAGES[5];player.dead=false;player.x=240;player.y=430;subBoss=null;subBossActive=false;subBossDone=false;eBullets.length=0;playerLocks=[];spawnSubBoss('tempestbrothers');var b=subBoss,D=b._tempestDuo,p=D.ships[0],s=p._ai,J=p._jet;s.enter('chase');s.boss.x=400;s.boss.y=230;s.vulnerable=true;D.ai.player.x=450;D.ai.player.y=870;tempestBrothersSync(b);";
  vm.runInContext(_pre295,ctxv);
  ok(vm.runInContext("D.ships.every(p=>p._jet.angle===Math.PI)&&s.ports(1).every(q=>q.id===0||q.id===2)",ctxv),'both jets begin nose south; the physical front apertures fire toward the pilot');
  ok(vm.runInContext("tempestJetStart(b,p)&&D.striker===p&&!tempestJetStart(b,D.ships[1])",ctxv),'only one brother owns a committed fighter pass at a time');
  vm.runInContext("var x=s.boss.x,y=s.boss.y;for(var i=0;i<12;i++)tempestJetTick(b,p,1/60);",ctxv);
  ok(vm.runInContext("s.boss.x!==x&&s.boss.y!==y&&J.angle!==Math.PI",ctxv),'the fighter banks and slides on two axes as Mike requested');
  vm.runInContext("for(var i=0;i<100&&J.state!=='charge';i++)tempestJetTick(b,p,1/60);",ctxv);
  ok(vm.runInContext("J.state==='charge'&&J.cue==='red'",ctxv),'aiming flashes red before the committed thrust');
  vm.runInContext("for(var i=0;i<60&&J.cue!=='green';i++)tempestJetTick(b,p,1/60);var lockX=J.lock.x,lockY=J.lock.y;D.ai.player.x=200;D.ai.player.y=300;tempestJetTick(b,p,1/60);",ctxv);
  ok(vm.runInContext("J.cue==='green'&&J.state==='charge'&&J.lock.x===lockX&&J.lock.y===lockY",ctxv),'green visibly holds the locked target before launch instead of tracking a late dodge');
  vm.runInContext("for(var i=0;i<30&&J.state!=='thrust';i++)tempestJetTick(b,p,1/60);var vx=J.vx,vy=J.vy,a=J.angle;D.ai.player.x=850;D.ai.player.y=100;for(var i=0;i<6;i++)tempestJetTick(b,p,1/60);",ctxv);
  ok(vm.runInContext("J.state==='thrust'&&J.thrusts===1&&J.vx===vx&&J.vy===vy&&J.angle===a&&Math.hypot(vx,vy)>839.99",ctxv),'afterburner thrust commits to its fast velocity and nose direction without homing');
  vm.runInContext("s.rig[0].hp=0;p._pending=[];J.shot=0;tempestJetTick(b,p,1/60);",ctxv);
  ok(vm.runInContext("p._pending.length===1&&p._pending[0].id===2&&Math.abs(p._pending[0].a-(J.angle-Math.PI/2))<1e-9",ctxv),'a silenced front aperture stays silent while its surviving partner follows the turning nose');
  vm.runInContext("s.rig[0].hp=300;J.angle=Math.PI/2;tempestBrothersSync(b);var port=tempestPortXY(p,0);",ctxv);
  ok(vm.runInContext("tempestJetPartAt(p,port.x,port.y)==='ap0'&&tempestBrothersPartAt(b,port.x,port.y)==='B0'",ctxv),'aperture collision rotates with the authored hull during a rapid turn');
  vm.runInContext("eBullets.length=0;tempestBrothersRound(p,{id:0,a:Math.PI/2,s:540,kind:'bolt'});var q=eBullets[0];",ctxv);
  ok(vm.runInContext("q&&Math.abs(q.ang-(J.angle-Math.PI/2))<1e-9&&Math.abs(q.y-port.y)<1e-9&&Math.abs(q.x-port.x)<1e-9",ctxv),'front gun rounds leave the rotating physical muzzle along the actual nose');
  vm.runInContext("s.beams=[{id:0,dir:-1,active:true,charge:1}];tempestBrothersSync(b);",ctxv);
  ok(vm.runInContext("Math.abs(p._tlv.beams[0].ang-(J.angle-Math.PI/2))<1e-9",ctxv),'banked lasers also follow their physical aperture rather than a stale vertical direction');
  vm.runInContext("s.vulnerable=true;tempestBrothersSync(b);hitSubBoss(b.maxhp*4,p.x,p.y);",ctxv);
  ok(vm.runInContext("s.phase==='overtake'&&!J.active&&J.cue===null&&D.striker===null",ctxv),'a real phase-gate hit cancels the pass and its charge immediately');
  ok(vm.runInContext("['tlvJetCharge','tlvJetReady','tlvJetTurn','tlvJetThrust','tlvJetEngine','tlvJetBrake'].every(k=>typeof Audio.SFX[k]==='function'&&!!BOFA.sfx[k]&&!!Snd.TAME[k])",ctxv),'turn, charge, launch, engine and brake cues have real samples and gated mixer rows');
  vm.runInContext("subBoss=null;subBossActive=false;subBossDone=false;eBullets.length=0;playerLocks=[];",ctxv);
}
