const fs=require('fs'),path=require('path'),p=path.resolve(__dirname,'test_fl.js');
let s=fs.readFileSync(p,'utf8');
const anchor="require('./test_archmage_spiked_ball_warning_0916.cjs')(vm,ctxv,ok);\r\n";
if(!s.includes(anchor))throw new Error('test harness anchor missing');
if(!s.includes('test_archmage_core_recovery_0916.cjs'))s=s.replace(anchor,anchor+"require('./test_archmage_core_recovery_0916.cjs')(vm,ctxv,ok);\r\n");
fs.writeFileSync(p,s,'utf8');
console.log('REGISTERED_ARCHMAGE_CORE_RECOVERY_TEST_0916');
