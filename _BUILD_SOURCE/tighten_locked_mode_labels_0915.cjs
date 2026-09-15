const fs=require('fs'),path=require('path');
const p=path.resolve(__dirname,'..','assets','game.js');let s=fs.readFileSync(p,'utf8');
if(s.includes('\r\n'))throw new Error('assets/game.js must remain LF');
const a="VW/2,rect.y+rect.h+9);",b="VW/2,rect.y+rect.h+5);";
if(s.split(a).length!==2)throw new Error('mode label anchor did not match exactly once');
s=s.replace(a,b);fs.writeFileSync(p,s,'utf8');console.log('tightened mode subtitles clear of neighboring plates');
