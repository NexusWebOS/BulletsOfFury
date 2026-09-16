const fs=require('fs'),path=require('path'),file=path.resolve(__dirname,'..','assets','game.js');
let s=fs.readFileSync(file,'utf8');
const from="function hammerBossDraw(b){\n  const h=b._hammer;hammerBossAtmosphereDraw(b);\n  if(h.state==='curl'&&h.ballWarn)";
const to="function hammerBossDraw(b){\n  const h=b._hammer;hammerBossAtmosphereDraw(b);\n  if(h.state==='mega_charge'){const k=clamp(h.t/1.65,0,1);combatWarningDraw(b,{x:b.x,y:b.y+36,ex:b.x,ey:VH,progress:k,width:VW*.24,alertX:b.x+78,alertY:b.y-78});}\n  if(h.state==='curl'&&h.ballWarn)";
const n=s.split(from).length-1;if(n!==1)throw new Error(`mega-wave draw anchor: expected one match, got ${n}`);s=s.replace(from,to);
fs.writeFileSync(file,s,'utf8');console.log('PATCHED_ARCHMAGE_MEGA_WARNING_0916');
