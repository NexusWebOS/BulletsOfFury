// Re-run the full suite with one explicit candidate in the recovery-layer slot.
const fs=require('fs'),path=require('path'),Module=require('module');
const file=path.join(__dirname,'test_fl.js');
const candidate=process.argv[2]||'./balance_recovery_stage2_candidate_1007b.js';
const line="require('./test_balance_recovery_1007b.cjs')(vm,ctxv,ok);";
const src=fs.readFileSync(file,'utf8').replace(line,"require('./test_balance_recovery_1007b.cjs')(vm,ctxv,ok,"+JSON.stringify(candidate)+");");
const m=new Module(file,module);m.filename=file;m.paths=Module._nodeModulePaths(__dirname);m._compile(src,file);
