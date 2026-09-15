const fs=require('fs'),path=require('path'),Module=require('module');
const harness=fs.readFileSync(path.join(__dirname,'test_fl.js'),'utf8');
const boot=harness.slice(0,harness.indexOf('/* top-level const/let'));
const test=`
const result=vm.runInContext(\`(()=>{
 const checks=[];function check(ok,name){checks.push({name,ok:!!ok});if(!ok)throw Error(name);}
 state=GS.PLAY;const b={enter:true,dead:false};
 encounterClockTick(b,true,10);check(!b._fightClock,'entrance excluded');
 b.enter=false;for(let i=0;i<120;i++)encounterClockTick(b,true,.5);
 check(encounterClockText(b._fightClock.seconds)==='01:00','sixty seconds rolls to next minute');
 state='paused';encounterClockTick(b,true,30);check(b._fightClock.seconds===60,'pause excluded');
 state=GS.OPTIONS;encounterClockTick(b,true,30);check(b._fightClock.seconds===60,'options excluded');
 state=GS.PLAY;b.enter=true;encounterClockTick(b,true,2);check(b._fightClock.seconds===62,'later transformation does not reset or stop fight');
 encounterClockTick(b,false,2);check(b._fightClock.seconds===62,'inactive encounter excluded');
 encounterClockTick(b,true,NaN);encounterClockTick(b,true,-1);check(b._fightClock.seconds===62,'invalid deltas excluded');
 player.dead=true;encounterClockTick(b,true,3);check(b._fightClock.seconds===65,'player death cannot reduce speed-run elapsed time');player.dead=false;
 b.dead=true;encounterClockTick(b,true,3);check(b._fightClock.seconds===65&&b._fightClock.finished,'boss defeat freezes retained result');
 const next={enter:false,dead:false};encounterClockTick(next,true,.5);check(next._fightClock.seconds===.5,'new encounter begins with its own clock');
 const mech={enter:false,dead:false,_mech:{phase:'assemble'}};encounterClockTick(mech,true,5);check(!mech._fightClock,'mechanical assembly excluded');
 check(encounterClockText(59.99)==='00:59'&&encounterClockText(6000)==='99:59','format has stable two-digit fields');
 return {passed:checks.length,failed:0,checks};
})()\`,ctxv);console.log(JSON.stringify(result,null,2));`;
const m=new Module(__filename,module);m.filename=__filename;m.paths=module.paths;m._compile(boot+test,__filename);
