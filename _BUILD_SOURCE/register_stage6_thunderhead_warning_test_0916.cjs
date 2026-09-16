const fs=require('fs'),path=require('path'),p=path.resolve(__dirname,'test_fl.js');let s=fs.readFileSync(p,'utf8');
const line="require('./test_stage6_thunderhead_warning_0916.cjs')(vm,ctxv,ok);";
if(!s.includes(line)){
  const mark="require('./test_stage9_tidal_cascade_warning_0915.cjs')(vm,ctxv,ok);";
  if(!s.includes(mark))throw new Error('registration anchor missing');
  s=s.replace(mark,mark+'\r\n'+line);
}
const oldLoop="for(var z=0;z<150;z++)carrierThunderheadTick(boss,1/60);";
const newLoop="for(var z=0;z<170;z++)carrierThunderheadTick(boss,1/60);";
if(s.includes(oldLoop))s=s.replace(oldLoop,newLoop);
if(!s.includes(newLoop))throw new Error('Thunderhead legacy simulation anchor missing');
s=s.replace(/(?<!\r)\n/g,'\r\n');fs.writeFileSync(p,s,'utf8');console.log('REGISTERED_STAGE6_THUNDERHEAD_WARNING_0916');
