const fs=require('fs'),path=require('path');const p=path.join(__dirname,'test_fl.js'),s=fs.readFileSync(p,'utf8');
if(/(^|[^\r])\n/.test(s))throw new Error('suite must remain CRLF');
const old="  vm.runInContext(\"eBullets.length=0; boss._ovState='fight'; boss._ovPhase=3; boss.fireCd=0; boss._rkN=0;\", ctxv);\r\n";
const neu="  vm.runInContext(\"eBullets.length=0; boss._ovState='fight'; boss._ovPhase=3; boss.fireCd=0; boss._rkN=0; boss._ovChargeCd=999; player.invuln=999;\", ctxv);\r\n";
const old2="  ok(rkMoved, 'rockets travel across the screen (not stuck at the launch point)');\r\n";
const neu2=old2+"  vm.runInContext(\"player.invuln=0;\",ctxv);\r\n";
if(s.split(old).length-1!==1||s.split(old2).length-1!==1)throw new Error('rocket fixture marker mismatch');
const out=s.replace(old,neu).replace(old2,neu2);if(/(^|[^\r])\n/.test(out))throw new Error('suite endings changed');
fs.writeFileSync(p,out,'utf8');console.log('stabilized Overlord rocket fixture against unrelated charge/player collision');
