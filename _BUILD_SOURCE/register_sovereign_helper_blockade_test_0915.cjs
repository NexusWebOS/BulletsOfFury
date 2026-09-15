const fs=require('fs'),path=require('path');
const p=path.resolve(__dirname,'test_fl.js');
let s=fs.readFileSync(p,'utf8');
const line="require('./test_sovereign_helper_blockade_0915.cjs')(vm,ctxv,ok);";
if(!s.includes(line)){
  const anchor="require('./test_continue_up_rewards_0915.cjs')(vm,ctxv,ok);";
  if(!s.includes(anchor))throw new Error('test anchor missing');
  s=s.replace(anchor,anchor+'\r\n'+line);
}
if(s.replace(/\r\n/g,'').includes('\n'))throw new Error('test_fl.js lost CRLF policy');
fs.writeFileSync(p,s,'utf8');
console.log('REGISTERED_SOVEREIGN_HELPER_BLOCKADE_TEST_0915');
