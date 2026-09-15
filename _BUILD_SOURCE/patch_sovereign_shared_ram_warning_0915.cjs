const fs=require('fs'),path=require('path'),p=path.resolve(__dirname,'..','assets','game.js');
let s=fs.readFileSync(p,'utf8');if(s.includes('\r'))throw new Error('game.js must remain LF-only');
function one(a,b,label){const n=s.split(a).length-1;if(n!==1)throw new Error(label+' expected once, found '+n);s=s.replace(a,b);}
one(
"    B={family:'rime',angles:[a],t:(owner.t||stateT||0),warm:1,released:false};",
"    B={family:'rime',angles:[a],t:(owner.t||stateT||0),warm:1,released:false,alertX:q.alertX,alertY:q.alertY};",
'shared alert anchor input');
one(
"  const sy=Math.max(L23_WARN_MINY,top-h-12);\n  ctx.save();ctx.imageSmoothingEnabled=false;ctx.globalAlpha=steady?.62:(red?1:.92);\n  ctx.drawImage(im,Math.round(b.x-w/2),Math.round(sy),w,h);",
"  const sy=Number.isFinite(B.alertY)?Math.max(L23_WARN_MINY,B.alertY):Math.max(L23_WARN_MINY,top-h-12),sx=Number.isFinite(B.alertX)?B.alertX:b.x;\n  ctx.save();ctx.imageSmoothingEnabled=false;ctx.globalAlpha=steady?.62:(red?1:.92);\n  ctx.drawImage(im,Math.round(sx-w/2),Math.round(sy),w,h);",
'shared alert anchor draw');
one(
"  if(S.mode==='ramTell'){\n    if(R.t<.40)R.lane=clamp(player.x,72,worldWidth()-72);else R.locked=true;\n    b.x+=(R.lane-b.x)*Math.min(1,dt*7);b.y+=(S.homeY-b.y)*Math.min(1,dt*6);\n    if(R.t>=1.0){S.mode='ramDive';R.t=0;stageRevisionCue(b,'sovereignFlyby',0,.90);}\n",
"  if(S.mode==='ramTell'){\n    if(R.t<.40)R.lane=clamp(player.x,72,worldWidth()-72);else R.locked=true;\n    b.x+=(R.lane-b.x)*Math.min(1,dt*7);b.y+=(S.homeY-b.y)*Math.min(1,dt*6);\n    combatWarningTick(b,'sovereign-unpowered-ram',R.t,1.0);\n    if(R.t>=1.0){S.mode='ramDive';R.t=0;stageRevisionCue(b,'sovereignFlyby',0,.90);}\n",
'shared warning tick');
one(
"  if(S.mode==='ramTell'){\n    const p=shipBossMount(b,'C'),key='bmfx_fov_'+l23FovPhase(R.t)+'_tall';\n    if(XART.rdy(key)){ctx.save();ctx.translate(R.lane,p.y);l23FovDraw(b,{family:'rime',angles:[Math.PI/2],t:R.t},0,p,R.t,38);ctx.restore();}\n  }\n",
"  if(S.mode==='ramTell'){\n    const p=shipBossMount(b,'C'),q=clamp(R.t/1.0,0,1);\n    combatWarningDraw(b,{x:p.x,y:p.y,ex:R.lane,ey:VH+40,progress:q,width:76,alertX:b.x,alertY:80});\n  }\n",
'shared warning renderer');
fs.writeFileSync(p,s,'utf8');console.log('PATCHED_SOVEREIGN_SHARED_RAM_WARNING_0915');
