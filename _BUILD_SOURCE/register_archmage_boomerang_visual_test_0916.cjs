const fs=require('fs'),path=require('path'),p=path.resolve(__dirname,'test_fl.js');let s=fs.readFileSync(p,'utf8');
const line="require('./test_archmage_boomerang_visual_0916.cjs')(vm,ctxv,ok);";
if(!s.includes(line)){
  const mark="require('./test_stage6_thunderhead_warning_0916.cjs')(vm,ctxv,ok);";
  if(!s.includes(mark))throw new Error('registration anchor missing');
  s=s.replace(mark,mark+'\r\n'+line);
}
s=s.replace(/(?<!\r)\n/g,'\r\n');fs.writeFileSync(p,s,'utf8');console.log('REGISTERED_ARCHMAGE_BOOMERANG_VISUAL_0916');
