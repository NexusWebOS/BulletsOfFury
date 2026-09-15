const fs=require('fs'),path=require('path'),p=path.resolve(__dirname,'test_fl.js');let s=fs.readFileSync(p,'utf8');const line="require('./test_stage9_horizon_shared_volley_warning_0915.cjs')(vm,ctxv,ok);";
if(!s.includes(line)){const mark="require('./test_stage8_vile_shared_annihilation_warning_0915.cjs')(vm,ctxv,ok);";if(!s.includes(mark))throw new Error('registration anchor missing');s=s.replace(mark,mark+'\r\n'+line);}
const old="eBullets.length=0;F.core._fire=0;s9VoidHorizonTick(subBoss,1/60);return JSON.stringify({kind:subBoss.kind";
const now="eBullets.length=0;F.core._fire=0;s9VoidHorizonTick(subBoss,1/60);for(var j=0;j<39;j++)s9VoidHorizonTick(subBoss,1/60);return JSON.stringify({kind:subBoss.kind";
if(s.includes(old))s=s.replace(old,now);else if(!s.includes(now))throw new Error('legacy Stage-9 armed-body assertion anchor missing');
s=s.replace(/(?<!\r)\n/g,'\r\n');fs.writeFileSync(p,s,'utf8');console.log('REGISTERED_STAGE9_HORIZON_SHARED_VOLLEY_WARNING_0915');
