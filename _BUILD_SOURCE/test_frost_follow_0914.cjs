const fs=require('fs'),path=require('path'),Module=require('module');
const harness=fs.readFileSync(path.join(__dirname,'test_fl.js'),'utf8');
const boot=harness.slice(0,harness.indexOf('/* top-level const/let'));
const test=`const result=vm.runInContext(\`(()=>{
const checks=[];function check(ok,name){checks.push({name,ok:!!ok});if(!ok)throw Error(name);}
state=GS.PLAY;run.stage=3;camX=0;player.x=310;player.y=430;player.dead=false;
const e={x:100,y:120,w:80};enemyGlideTick(e,1,{follow:true,targetX:400,speed:100});check(e.x===200&&e.y===120,'horizontal speed bound and unchanged Y');
enemyGlideTick(e,4,{follow:true,targetX:210,speed:100});check(e.x===210,'no target overshoot');
enemyGlideTick(e,1,{follow:true,targetX:-100,speed:1000});check(e.x>=camLeftX()+40,'hull stays within camera bounds');
const saved=e.x;enemyGlideTick(e,-1,{follow:true});enemyGlideTick(e,NaN,{follow:true});check(e.x===saved,'invalid delta cannot move unit');
spawnSubBoss('frostcruiser');const b=subBoss;b.enter=false;b.x=100;b.y=shipBossStationY(b);b.t=0;
const before=b.x;jungleCruiserStalk(b,.1);check(b.x>before&&b.x-before<=17.501,'frost uses speed-bounded player follow');
const sampled=b._jc.targetX;player.x=90;jungleCruiserStalk(b,.05);check(b._jc.targetX===sampled,'tracking delay prevents instant input mirroring');
jungleCruiserStalk(b,.2);check(b._jc.targetX===90,'tracking refreshes after sampling window');
player.x=280;jungleCruiserSetState(b,'riseNorth');b.y=-b.h; jungleCruiserDirector(b,.02);check(b._jc.state==='returnTop'&&Math.abs(b.x-280)<1,'offscreen return samples player X');
const lane=b.x;player.x=150;jungleCruiserDirector(b,.1);check(b.x===lane,'return descent stays on committed vertical lane');
b.y=shipBossStationY(b)-1;jungleCruiserDirector(b,.02);check(b._jc.state==='frostTrack'&&!b._jcGhost,'arrival opens follow window and restores collision');
jungleCruiserDirector(b,.2);check(b.x<lane,'post-return follows moved player');
b._jc.t=1.14;jungleCruiserDirector(b,.02);check(b._jc.state==='beamCharge','follow ends at laser commitment');
const target=b._jc.targetX;player.x=400;jungleCruiserDirector(b,.1);check(b._jc.targetX===target,'charge no longer samples player');
spawnSubBoss('junglecruiser');const j=subBoss;j.enter=false;j.y=shipBossStationY(j)-1;jungleCruiserSetState(j,'returnTop');jungleCruiserDirector(j,.02);check(j._jc.state==='beamCharge','jungle cruiser retains original direct charge return');
return {passed:checks.length,failed:0,checks};})()\`,ctxv);console.log(JSON.stringify(result,null,2));`;
const m=new Module(__filename,module);m.filename=__filename;m.paths=module.paths;m._compile(boot+test,__filename);
