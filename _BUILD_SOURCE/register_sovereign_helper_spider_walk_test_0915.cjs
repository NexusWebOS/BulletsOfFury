const fs=require('fs'),path=require('path'),p=path.resolve(__dirname,'test_fl.js');let s=fs.readFileSync(p,'utf8');
const line="require('./test_sovereign_helper_spider_walk_0915.cjs')(vm,ctxv,ok);",anchor="require('./test_sovereign_helper_enrage_0915.cjs')(vm,ctxv,ok);";
if(!s.includes(line)){if(!s.includes(anchor))throw new Error('anchor missing');s=s.replace(anchor,anchor+'\r\n'+line);}if(s.replace(/\r\n/g,'').includes('\n'))throw new Error('CRLF lost');
fs.writeFileSync(p,s,'utf8');console.log('REGISTERED_SOVEREIGN_HELPER_SPIDER_WALK_TEST_0915');
