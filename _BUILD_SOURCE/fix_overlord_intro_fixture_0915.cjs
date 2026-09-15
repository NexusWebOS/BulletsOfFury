const fs=require('fs'),path=require('path');
const p=path.resolve(__dirname,'test_fl.js');let s=fs.readFileSync(p,'utf8');
if(/(^|[^\r])\n/.test(s))throw new Error('test_fl.js must remain CRLF');
const a="spawnBoss('damkeeper'); boss.enter=false; boss.y=boss.ty=140; boss.x=240;",b="spawnBoss('damkeeper'); boss._ovIntro.done=true; boss._noHit=false; boss.enter=false; boss.y=boss.ty=140; boss.x=240;";
if(s.split(a).length!==2)throw new Error('Overlord test fixture anchor must match once');
s=s.replace(a,b);fs.writeFileSync(p,s,'utf8');
if(/(^|[^\r])\n/.test(fs.readFileSync(p,'utf8')))throw new Error('test line endings changed');
console.log('updated the direct-fight Overlord fixture to bypass its presentation state');
