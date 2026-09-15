const fs=require('fs'),path=require('path'),file=path.resolve(__dirname,'test_fl.js');let src=fs.readFileSync(file,'utf8');
if(!src.includes('\r\n'))throw new Error('test_fl.js must remain CRLF');
if(src.includes("require('./test_enemy_shield_stun_0915.cjs')")){console.log('Shield stun test already hooked.');process.exit(0);}
const a="require('./test_elemental_absorb_0915.cjs')(vm,ctxv,ok);\r\n\r\n// ===== 305.";
const b="require('./test_elemental_absorb_0915.cjs')(vm,ctxv,ok);\r\n\r\nrequire('./test_enemy_shield_stun_0915.cjs')(vm,ctxv,ok);\r\n\r\n// ===== 305.";
const n=src.split(a).length-1;if(n!==1)throw new Error('test hook expected once, found '+n);src=src.replace(a,b);
fs.writeFileSync(file,src,'utf8');console.log('Hooked shield stun regression section.');
