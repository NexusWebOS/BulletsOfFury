const fs=require('fs');
const path=require('path');
const root=path.resolve(__dirname,'..');
const game=path.join(root,'assets','game.js');
let s=fs.readFileSync(game,'utf8');
if(s.includes('\r'))throw new Error('assets/game.js must remain LF-only');
const backup=path.join(root,'_shots','backups','game_pre_olive_warden_circle_entry_0915.js');
fs.mkdirSync(path.dirname(backup),{recursive:true});
if(!fs.existsSync(backup))fs.writeFileSync(backup,s,'utf8');
function one(oldText,newText,label){
  const n=s.split(oldText).length-1;
  if(n!==1)throw new Error(label+' expected once, found '+n);
  s=s.replace(oldText,newText);
}
one(
  "H.dir=-H.dir;H.startA=Math.atan2((b.y-S.homeY)/38,(b.x-mid)/amp);H.log.push({mode:mode,t:b.t||0});",
  "H.dir=-H.dir;H.startA=Math.atan2((b.y-S.homeY)/38,(b.x-mid)/amp);H.circleFromX=b.x;H.circleFromY=b.y;H.log.push({mode:mode,t:b.t||0});",
  'capture circle ingress origin'
);
one(
  "b.x=mid+Math.cos(a)*H.amp;b.y=S.homeY+Math.sin(a)*38;",
  "const tx=mid+Math.cos(a)*H.amp,ty=S.homeY+Math.sin(a)*38,ingress=clamp(q/.22,0,1),blend=ingress*ingress*(3-2*ingress);\n    b.x=lerp(H.circleFromX,tx,blend);b.y=lerp(H.circleFromY,ty,blend);",
  'blend into circular orbit'
);
if(s.includes('\r'))throw new Error('patch introduced CR characters');
fs.writeFileSync(game,s,'utf8');
console.log('PATCHED_OLIVE_WARDEN_CIRCLE_ENTRY_0915');
