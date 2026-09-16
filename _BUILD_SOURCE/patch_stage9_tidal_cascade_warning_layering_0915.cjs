const fs=require('fs'),path=require('path'),p=path.resolve(__dirname,'..','assets','game.js');let s=fs.readFileSync(p,'utf8');if(s.includes('\r'))throw new Error('game.js must remain LF-only');
function one(a,b,label){const n=s.split(a).length-1;if(n!==1)throw new Error(label+' expected once, found '+n);s=s.replace(a,b);}
one(
`function tidalCascadeDraw(b){
  const T=b&&b._s9Cascade;if(!T||T.wave>=T.waves)return;const cw=(T.right-T.left)/T.cols,
    k=clamp((T.t-T.warnAt)/T.rowTell,0,1),y=(b._drawY!=null?b._drawY:b.y)+b.h*.34;
  for(let i=0;i<T.cols;i++){
    if(i===T.gap||i===T.gap+1)continue;const x=T.left+(i+.5)*cw;
    combatWarningDraw(b,{x:x,y:y-(i&1)*18,ex:x,ey:VH+40,progress:k,width:Math.max(24,cw*.52),fieldOnly:true});
  }
  const p=shipBossMount(b,'C');combatWarningDraw(b,{x:p.x,y:p.y,ex:p.x,ey:VH+40,progress:k,alertOnly:true});
}`,
`function tidalCascadeDraw(b,front){
  const T=b&&b._s9Cascade;if(!T||T.wave>=T.waves)return;const cw=(T.right-T.left)/T.cols,
    k=clamp((T.t-T.warnAt)/T.rowTell,0,1),y=(b._drawY!=null?b._drawY:b.y)+b.h*.34;
  if(!front){for(let i=0;i<T.cols;i++){
    if(i===T.gap||i===T.gap+1)continue;const x=T.left+(i+.5)*cw;
    combatWarningDraw(b,{x:x,y:y-(i&1)*18,ex:x,ey:VH+40,progress:k,width:Math.max(24,cw*.52),fieldOnly:true});
  }}else{
    const p=shipBossMount(b,'C');combatWarningDraw(b,{x:p.x,y:p.y,ex:p.x,ey:VH+40,progress:k,alertOnly:true});
  }
}`,
'split Tidal Cascade fields and alert into two render layers');
one("  if(b._s9Cascade)tidalCascadeDraw(b);","  if(b._s9Cascade)tidalCascadeDraw(b,false);",'draw Cascade fields below authored hull');
one("    if(b._s4war&&typeof stage4WarfareDrawOver==='function')stage4WarfareDrawOver(b);\n    shipBossMuzzleDraw(b);\n    return true;","    if(b._s4war&&typeof stage4WarfareDrawOver==='function')stage4WarfareDrawOver(b);\n    shipBossMuzzleDraw(b);\n    if(b._s9Cascade)tidalCascadeDraw(b,true);\n    return true;",'draw Cascade alert above fallback hull');
one("  shipBossMuzzleDraw(b);\n  return true;\n}\n/* Encounter HP floors", "  shipBossMuzzleDraw(b);\n  if(b._s9Cascade)tidalCascadeDraw(b,true);\n  return true;\n}\n/* Encounter HP floors",'draw Cascade alert above authored hull');
fs.writeFileSync(p,s,'utf8');console.log('PATCHED_STAGE9_TIDAL_CASCADE_WARNING_LAYERING_0915');
