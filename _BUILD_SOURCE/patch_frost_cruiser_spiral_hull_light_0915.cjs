const fs=require('fs');const path=require('path');const file=path.resolve(__dirname,'..','assets','game.js');let s=fs.readFileSync(file,'utf8');
if(/\r\n/.test(s))throw new Error('assets/game.js must remain LF-only');
const from="      ctx.globalCompositeOperation='lighter';ctx.globalAlpha=0.28+0.52*J.charge;\n      ctx.drawImage(tint,-w*.5,-h*.5,w,h);";
const to="      ctx.globalCompositeOperation='lighter';\n      ctx.globalAlpha=J.state==='frostRocketCharge'?(0.10+0.22*J.charge):(0.28+0.52*J.charge);\n      ctx.drawImage(tint,-w*.5,-h*.5,w,h);";
const n=s.split(from).length-1;if(n!==1)throw new Error('expected one charge overlay match, got '+n);s=s.replace(from,to);
if(/\r\n/.test(s))throw new Error('patch introduced CRLF');fs.writeFileSync(file,s,'utf8');console.log('rebalanced Frost rocket charge hull light');
