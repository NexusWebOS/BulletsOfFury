const fs=require('fs');
const path=require('path');
const p=path.join(__dirname,'test_fl.js');
let s=fs.readFileSync(p,'utf8');
const line="require('./test_continue_up_rewards_0915.cjs')(vm,ctxv,ok);";
if(s.includes(line)){console.log('ALREADY_REGISTERED_CONTINUE_UP_REWARDS_0915');process.exit(0);}
const anchor="require('./test_olive_warden_escorts_0915.cjs')(vm,ctxv,ok);";
const n=s.split(anchor).length-1;
if(n!==1)throw new Error('section 323 anchor expected once, found '+n);
s=s.replace(anchor,anchor+'\r\n'+line);
fs.writeFileSync(p,s,'utf8');
if(/(^|[^\r])\n/.test(s))throw new Error('test_fl.js lost CRLF-only form');
console.log('REGISTERED_CONTINUE_UP_REWARDS_0915');
