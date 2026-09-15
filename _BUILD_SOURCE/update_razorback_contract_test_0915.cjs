const fs=require('fs'),path=require('path'),p=path.resolve(__dirname,'test_fl.js');let s=fs.readFileSync(p,'utf8');
if(!s.includes('\r\n'))throw new Error('test_fl.js must remain CRLF');
const old="  ok(/rzbShot\\(b,m,R\\.turret\\+off,240,18,'rzbSonic'\\)/.test(_mv) && /R\\.waves\\.push/.test(_mv), 'the Sonic Hammer fires rounds AND a pressure wave');\r\n";
const next="  ok(/rzbShot\\(b,m,R\\.turret\\+off,(?:240|R\\.furious\\?300:240),(?:18|R\\.furious\\?22:18),'rzbSonic'\\)/.test(_mv) && /R\\.waves\\.push/.test(_mv), 'the Sonic Hammer fires rounds AND a pressure wave');\r\n";
if((s.split(old).length-1)!==1)throw new Error('Sonic Hammer assertion anchor mismatch');s=s.replace(old,next);fs.writeFileSync(p,s,'utf8');console.log('UPDATED_RAZORBACK_CONTRACT_TEST_0915');
