"""Revise superseded design expectations and add behavior checks, preserving test CRLF."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];p=ROOT/'_BUILD_SOURCE/test_fl.js'
baseline=ROOT/'_shots/stage_1_5_0914/test.before.js'
if not baseline.exists():baseline.write_bytes(p.read_bytes())
s=baseline.read_bytes().decode('utf-8').replace('\r\n','\n')
def replace(a,b):
 global s
 assert s.count(a)==1,(s.count(a),a[:90]);s=s.replace(a,b,1)
replace("e._nef='nef_s1_jungle_tank'","e._nef='nef_s2_lava_crawler'")
replace("_arm257.indexOf('return [right,center,left]')", "_arm257.indexOf('return [left,center,right]')")
replace('Volley Missiles cross onto distinct right/center/left locks and only reacquire when required','Volley Missiles keep distinct left/center/right locks and only reacquire when required')
replace("b.kind==='spaceVolleySeed';}).length;return JSON.stringify({active:","b.kind==='spaceVolley';}).length;return JSON.stringify({active:")
replace('_passive257.n===1,','_passive257.n===3,')
replace("_src259.indexOf('Audio.SFX.enemyMachineGunBurst')>=0",'_src259.indexOf("stageRevisionCue(b,\'overlordGun\'")>=0')
replace('Snd.TAME.spaceLaserCannon.g>=1&&Snd.TAME.spaceShadowRelease.g>=1&&Snd.TAME.spaceVolleyLaunch.g>=1','Snd.TAME.spaceLaserCannon.g>0&&Snd.TAME.spaceLaserCannon.g<=.5&&Snd.TAME.spaceShadowRelease.g>=1&&Snd.TAME.spaceVolleyLaunch.g>=1')
replace('all three space launch cues are foreground-mixed over Stage-5/9 music','space cannon is quieter while Shadow Orb and Volley reports retain their foreground mix')
replace('ok(/coleSonicBoom/.test(_mv), "with Cole\'s sonic release");','ok(/razorbackPressure/.test(_mv), "with its dedicated pressure release");')
tests=r'''
// ===== 299. MIKE'S STAGE 1–5 ENCOUNTER CORRECTIONS, 0914 =====
console.log('=== 299. stage 1–5 corrections ===');
{
  var burn299=JSON.parse(vm.runInContext(`(function(){
    var e={_nef:'nef_s1_jungle_tank',maxhp:100,hp:100,dead:false,_dyingT:null,t:.25,w:60,h:70};
    var out=[51,50,25,1,0].map(h=>{e.hp=h;return stage1Burning(e);});
    e.hp=25;var art=nefArtFor(e);e.dead=true;out.push(stage1Burning(e));e.dead=false;e._dyingT=0;out.push(stage1Burning(e));
    e._dyingT=null;e._nef='nef_s2_lava_crawler';out.push(stage1Burning(e));
    return JSON.stringify({out:out,art:art});
  })()`,ctxv));
  ok(burn299.out.join()==='false,true,true,true,false,false,false,false','living stage-1 fodder burns at half HP; healthy, dead, dying and other-stage hulls do not');
  ok(/_intact$/.test(burn299.art),'burning stage-1 hull keeps its clean authored plate without frozen damage plumes');
  var warden299=JSON.parse(vm.runInContext(`(function(){
    run.stage=4;curStage=STAGES[3];beginStage(4);state=GS.PLAY;player.reset();player.dead=false;
    spawnSubBoss('olivewarden');var b=subBoss;b.enter=false;b.x=worldWidth()/2;b.y=b.ty;var shots=[],sounds=[];
    var f=stage4MiniMachine,g=stage4MiniRocket,h=weaponFeedbackSound;
    stage4MiniMachine=function(){var q=f.apply(this,arguments);shots.push({kind:q.kind,slot:q._s4Slot,x:q.x,y:q.y});return q;};
    stage4MiniRocket=function(){var q=g.apply(this,arguments);shots.push({kind:q.kind,slot:q._s4Slot,x:q.x,y:q.y});return q;};
    weaponFeedbackSound=function(k){sounds.push(k);return true;};
    for(var i=0;i<480;i++){b.t+=1/60;stage4MiniDirector(b,1/60);}
    stage4MiniMachine=f;stage4MiniRocket=g;weaponFeedbackSound=h;
    return JSON.stringify({shots:shots,sounds:sounds,drones:b._s4war.drones.length});
  })()`,ctxv));
  ok(['L','R','CL','CR'].every(s=>warden299.shots.some(q=>q.slot===s&&q.kind==='mg')),'Warden fires mounted spread and center double lines as machine bullets');
  ok(['L','R'].every(s=>warden299.shots.some(q=>q.slot===s&&q.kind==='s4rocket'))&&warden299.drones===0,'Warden fires rockets from both mounts and fights without the removed helpers');
  ok(['wardenGun','wardenCenterGun','wardenRackCharge','wardenRocket'].every(k=>warden299.sounds.includes(k)),'all three Warden weapon acts and rack warning reach their own sound routes');
  var sovereign299=JSON.parse(vm.runInContext(`(function(){
    subBoss=null;subBossActive=false;run.stage=4;beginStage(4);state=GS.PLAY;spawnBoss('stormsovereign');
    var b=boss;b.enter=false;b.y=b.ty;b._phaseInvuln=0;stage4ShieldTick(b,1);
    var H=b._s4war.shield,ns=H.nodes.filter(n=>n.side<0),others=H.nodes.filter(n=>n.side>0);ns.forEach(n=>n.hp=10);
    var hp=b.hp;stage4PiercingBeam(b,{x:ns[0].x,w:26,top:-20,bot:430,dmg:12});
    var pair=ns.every(n=>n.dead),untouched=others.every(n=>!n.dead),carrier=b.hp===hp;
    var blocked=!stage4RamStart(b);others.forEach(n=>stage4ShieldDestroyNode(b,n));
    player.x=worldWidth()/2;var start=stage4RamStart(b),trace=[];
    for(var i=0;i<510;i++){b.t+=1/60;stage4RamTick(b,1/60);trace.push({mode:b._s4war.mode,y:b.y,air:!!b._s4Airborne,noHit:!!b._noHit});if(!b._s4war.ram)break;}
    return JSON.stringify({pair:pair,untouched:untouched,carrier:carrier,blocked:blocked,start:start,trace:trace,clean:!b._s4Airborne&&!b._noHit&&!b._s4war.ram,h:b.h});
  })()`,ctxv));
  ok(sovereign299.pair&&sovereign299.untouched&&sovereign299.carrier,'piercing laser destroys both intersected generators while the other column and shielded carrier remain unharmed');
  ok(sovereign299.blocked&&sovereign299.start,'Sovereign cannot dive while powered and can dive after the field breaks');
  ok(['ramTell','ramDive','ramOff','ramOver','ramReturn'].every(m=>sovereign299.trace.some(q=>q.mode===m)),'Sovereign completes a warning, dive, offscreen turn, overhead pass and opposite-edge return');
  ok(sovereign299.trace.some(q=>q.mode==='ramOff'&&q.y>512+sovereign299.h*.65+72),'Sovereign waits until the entire hull clears the screen before turning');
  ok(sovereign299.trace.filter(q=>q.air).every(q=>q.noHit)&&sovereign299.clean,'overhead pass disables hull collision and return restores all transient flight flags');
  var sound299=JSON.parse(vm.runInContext(`(function(){
    var oldB=Audio.SFX.expBig,oldS=Audio.SFX.expSmall,oldW=weaponFeedbackSound,n=0,heard=[];
    Audio.SFX.expBig=Audio.SFX.expSmall=function(){n++;};weaponFeedbackSound=function(k){heard.push(k);return true;};
    var before=explosions.length;explode(200,220,9,'blue',null,null,null,null,true);var visual=explosions.length-before;
    var b={t:0,dead:false};stage4ContactFeedback(b,100,120,8);stage4ContactFeedback(b,100,240,8);b.t=.11;stage4ContactFeedback(b,100,240,8);
    var contacts=heard.filter(k=>k==='sovereignContact').length;
    heard=[];boss=null;run.stage=4;beginStage(4);spawnBoss('stormsovereign');b=boss;b.t=0;b._s4war.shield.nodes.filter(n=>n.side<0).forEach(n=>stage4ShieldDestroyNode(b,n));
    var breaks=heard.filter(k=>k==='sovereignBreak').length;
    Audio.SFX.expBig=oldB;Audio.SFX.expSmall=oldS;weaponFeedbackSound=oldW;
    return JSON.stringify({visual:visual,contacts:contacts,breaks:breaks});
  })()`,ctxv));
  ok(sound299.visual===1,'quiet contact explosion still creates its complete authored visual entity');
  ok(sound299.contacts===2,'simultaneous piercing contacts share one report and a later contact gets a new report');
  ok(sound299.breaks===1,'simultaneous generator destruction receives one gated heavy explosion report');
  var volley299=JSON.parse(vm.runInContext(`(function(){
    boss=null;bossActive=false;subBoss=null;subBossActive=false;run.stage=5;curStage=STAGES[4];beginStage(5);state=GS.PLAY;
    player.reset();player.dead=false;player.x=worldWidth()/2;player.y=430;run.spaceLevels=[3,3,3];run.spaceWeapon=1;
    enemies=[];pBullets=[];var ts=[-70,0,70].map((dx,i)=>spawnEnemy('s5interceptor',player.x+dx,190+i*20,{}));ts.forEach(t=>t.ghost=false);
    spaceVolleyFire();var rack=pBullets.slice(),independent=rack.every((q,i)=>q._target===ts[i]);
    var origin=rack.map(q=>q.x);var oldHit=spaceBulletHit;spaceBulletHit=function(){return false;};
    rack[0]._target.dead=true;spaceBulletTick(rack[0],.15);var reacquired=rack[0]._target!==ts[0]&&!rack[0]._target.dead;
    for(var i=0;i<120;i++)rack.forEach(q=>spaceBulletTick(q,1/60));spaceBulletHit=oldHit;
    pBullets=[];spaceShadowRelease(SPACE_SHADOW_FULL_CHARGE);var orb=pBullets[0];
    return JSON.stringify({count:rack.length,origins:origin,independent:independent,reacquired:reacquired,forward:rack.every(q=>q.vy<0&&isFinite(q.x)&&isFinite(q.y)),primary:run.spaceWeapon,dmg:orb.dmg,expected:SPACE_SHADOW_TIER[2].base*1.5*1.35});
  })()`,ctxv));
  ok(volley299.count===3&&volley299.origins[0]<volley299.origins[1]&&volley299.origins[1]<volley299.origins[2],'passive rack launches three separate missiles directly from their left, nose and right hardpoints');
  ok(volley299.independent&&volley299.reacquired,'space missiles keep corresponding independent locks and reacquire when one dies');
  ok(volley299.forward&&volley299.primary===1,'passive missiles keep moving forward and preserve the selected Shadow Orb primary');
  ok(Math.abs(volley299.dmg-volley299.expected)<1e-8,'full Shadow Orb payload receives the requested 35 percent damage increase');
  ok(vm.runInContext('STAGE5_SKY_LEAD>=5&&Snd.TAME.spaceLaserCannon.g===.30',ctxv),'stage-5 sky lead is extended and the cannon report receives the quieter mix');
  var impact299=JSON.parse(vm.runInContext(`(function(){
    var b={x:250,y:250},before=explosions.length,n=0,hit=0,B=Audio.SFX.expBig,S=Audio.SFX.expSmall,V=Audio.SFX.spaceVolleyHit;
    Audio.SFX.expBig=Audio.SFX.expSmall=function(){n++;};Audio.SFX.spaceVolleyHit=function(){hit++;};spaceImpact(b,'volley',3,40);
    Audio.SFX.expBig=B;Audio.SFX.expSmall=S;Audio.SFX.spaceVolleyHit=V;return JSON.stringify({visual:explosions.length-before,generic:n,hit:hit});
  })()`,ctxv));
  ok(impact299.visual===2&&impact299.generic===0&&impact299.hit===1,'Volley impact keeps both authored explosion layers with one warhead report and no duplicate generic explosion sounds');
  var mix299=JSON.parse(vm.runInContext(`(function(){
    var old=Snd.play,flag=Snd._regentMix,pref=Snd.vol.sfx,out=[];Snd._regentMix=false;Snd.play=function(k,v){out.push(v);return true;};
    regentCombatMixArm();run.stage=5;boss={dead:false,_xenoRig:{}};Snd.play('spaceLaserCannon',1);run.stage=4;Snd.play('spaceLaserCannon',1);run.stage=5;Snd.play('announce',1);
    Snd.play=old;Snd._regentMix=flag;boss=null;return JSON.stringify({out:out,preserved:Snd.vol.sfx===pref});
  })()`,ctxv));
  ok(mix299.out[0]===.40&&mix299.out[1]===1&&mix299.out[2]===1,'Regent combat mix reserves effects headroom while preserving voices and normal gain outside the encounter');
  ok(mix299.preserved,'encounter sound headroom does not change the player sound preference');
  vm.runInContext('boss=null;bossActive=false;subBoss=null;subBossActive=false;enemies=[];eBullets=[];pBullets=[];Snd.loopStopAll();',ctxv);
}
'''
replace("console.log('\\n============================================');",tests+"\nconsole.log('\\n============================================');")
expected=s.replace('\n','\r\n').encode('utf-8')
if p.read_bytes() not in [baseline.read_bytes(),expected]:
 raise ValueError('Suite has subsequent edits; inspect the generated source before replacing them.')
p.write_bytes(expected);print('Updated stage-1–5 behavior checks with CRLF preserved')
