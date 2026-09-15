const fs=require('fs'),path=require('path');
const p=path.resolve(__dirname,'test_fl.js');
let b=fs.readFileSync(p),s=b.toString('utf8');
if(!s.includes('\r\n'))throw new Error('test_fl.js must remain CRLF');
const needle="require('./test_sovereign_giant_strike_0915.cjs')(vm,ctxv,ok);\r\n";
if((s.split(needle).length-1)!==1)throw new Error('registration anchor mismatch');
s=s.replace(needle,needle+"require('./test_razorback_duo_0915.cjs')(vm,ctxv,ok);\r\n");
fs.writeFileSync(p,s,'utf8');
console.log('REGISTERED_RAZORBACK_DUO_TEST_0915');
