// Separate VM so resetting stages here cannot change another suite fixture's run.
const fs=require('fs'),path=require('path'),Module=require('module');
const harness=fs.readFileSync(path.join(__dirname,'test_fl.js'),'utf8');
const boot=harness.slice(0,harness.indexOf('/* top-level const/let'));
const code=`(()=>{
  campaign.bonusUnlocked=1;run.mode='arcade';beginStage(9);
  const arcadeKeeps=campaign.bonusUnlocked===1;
  run.mode='campaign';beginStage(9);
  const campaignSpends=campaign.bonusUnlocked===0;
  if(!arcadeKeeps||!campaignSpends)throw Error('Bonus unlock must belong to Campaign');
  return {arcadeKeeps,campaignSpends};
})()`;
const m=new Module(__filename,module);m.filename=__filename;m.paths=module.paths;
m._compile(boot+'module.exports=vm.runInContext('+JSON.stringify(code)+',ctxv);',__filename);
module.exports=m.exports;
if(require.main===module)console.log(JSON.stringify(module.exports));
