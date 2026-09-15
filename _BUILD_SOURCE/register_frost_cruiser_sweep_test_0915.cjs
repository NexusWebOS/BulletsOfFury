const fs=require('fs');const path=require('path');const file=path.resolve(__dirname,'test_fl.js');let src=fs.readFileSync(file,'utf8');
const from="require('./test_furnace_rollerball_0915.cjs')(vm,ctxv,ok);\r\n\r\nconsole.log('\\n============================================');";
const to="require('./test_furnace_rollerball_0915.cjs')(vm,ctxv,ok);\r\nrequire('./test_frost_cruiser_sweep_0915.cjs')(vm,ctxv,ok);\r\n\r\nconsole.log('\\n============================================');";
const n=src.split(from).length-1;if(n!==1)throw new Error('expected one suite tail, found '+n);src=src.replace(from,to);
if(/(^|[^\r])\n/.test(src))throw new Error('test_fl.js gained bare LF');fs.writeFileSync(file,src,'utf8');console.log('REGISTERED_FROST_CRUISER_SWEEP_TEST_0915');
