const fs=require('fs'),path=require('path'),p=path.resolve(__dirname,'test_fl.js');let s=fs.readFileSync(p,'utf8');
const line="require('./test_stage8_vile_aimed_fan_warning_0916.cjs')(vm,ctxv,ok);";
if(!s.includes(line)){
  const mark="require('./test_stage8_vile_crescent_wall_warning_0916.cjs')(vm,ctxv,ok);";
  if(!s.includes(mark))throw new Error('registration anchor missing');s=s.replace(mark,mark+'\r\n'+line);
}
const oldAudit="    var body = _fn285(f);\r\n    var calls = (body.match(/eMissileHoming\\(/g) || []).length;";
const newAudit="    var body = _fn285(f);\r\n    if(f==='vileAttack') body += _fn285('vileAimedFanTick');\r\n    var calls = (body.match(/eMissileHoming\\(/g) || []).length;";
if(s.includes(oldAudit))s=s.replace(oldAudit,newAudit);
else if(!s.includes("if(f==='vileAttack') body += _fn285('vileAimedFanTick');"))throw new Error('Vile Retina audit anchor missing');
s=s.replace(/(?<!\r)\n/g,'\r\n');fs.writeFileSync(p,s,'utf8');console.log('REGISTERED_STAGE8_VILE_AIMED_FAN_WARNING_0916');
