const fs=require('fs'),path=require('path'),Module=require('module');
const harness=fs.readFileSync(path.join(__dirname,'test_fl.js'),'utf8');
const boot=harness.slice(0,harness.indexOf('/* top-level const/let'));
const code=fs.readFileSync(path.join(__dirname,'boss_design_checks_0915.js'),'utf8');
const tail='console.log(JSON.stringify(vm.runInContext('+JSON.stringify(code)+',ctxv),null,2));';
const m=new Module(__filename,module);m.filename=__filename;m.paths=module.paths;m._compile(boot+tail,__filename);
