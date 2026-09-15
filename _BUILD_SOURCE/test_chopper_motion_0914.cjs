const fs=require('fs'),path=require('path'),Module=require('module');
const harness=fs.readFileSync(path.join(__dirname,'test_fl.js'),'utf8');
const boot=harness.slice(0,harness.indexOf('/* top-level const/let'));
const test=`const result=vm.runInContext(\`(()=>{
const checks=[];function check(ok,name){checks.push({name,ok:!!ok});if(!ok)throw Error(name);}
beginStage(1);state=GS.PLAY;run.stage=1;camX=0;player.x=360;player.y=430;player.dead=false;
function make(){spawnBoss('damkeeper');const b=boss;b.enter=false;b.x=240;b.y=112.64;updateOverlordX(b,0);b.fireCd=999;b._ovChargeCd=999;return b;}
function simulate(hz){const b=make();for(let i=0;i<hz;i++)updateOverlordX(b,1/hz);return {x:b.x,y:b.y};}
const slow=simulate(30),fast=simulate(120);check(Math.abs(slow.x-fast.x)<.001,'hunt displacement independent of frame rate');check(Math.abs(slow.y-fast.y)<.4,'hover bob stable across frame rates');
let b=make();const x=b.x;updateOverlordX(b,.1);check(b.x-x<=15.501,'normal hunt speed bounded');
const sampled=b._ovTargetX;player.x=120;updateOverlordX(b,.05);check(b._ovTargetX===sampled,'chopper tracking has reaction delay');
updateOverlordX(b,.2);check(b._ovTargetX===120,'tracking refreshes toward player');
b=make();b._ovFlightT=3.1;updateOverlordX(b,.01);const phase=b._ovOrbitStart;check(Number.isFinite(phase)&&b._ovFlight==='orbit','orbit latches a starting phase');
let jumps=0,last=b.x;for(let i=0;i<130;i++){updateOverlordX(b,1/60);jumps=Math.max(jumps,Math.abs(b.x-last));last=b.x;}
check(b._ovOrbitStart===phase,'crossing centre never flips orbit phase');check(jumps<12,'orbit frame displacement stays bounded');
check(b.fireCd>900&&b._ovPhase===0,'motion does not change inactive attack state');
return {passed:checks.length,failed:0,checks};})()\`,ctxv);console.log(JSON.stringify(result,null,2));`;
const m=new Module(__filename,module);m.filename=__filename;m.paths=module.paths;m._compile(boot+test,__filename);
