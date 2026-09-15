const fs=require('fs'),path=require('path'),p=path.resolve(__dirname,'..','assets','game.js');let s=fs.readFileSync(p,'utf8');if(s.includes('\r'))throw new Error('game.js must remain LF-only');
function one(a,b,label){const n=s.split(a).length-1;if(n!==1)throw new Error(label+' expected once, found '+n);s=s.replace(a,b);}
one("  R.attack=list[++R.idx%list.length]; R.at=0; R.beat=-1; R.mgBeat=-1; R.charge=0;","  R.attack=list[++R.idx%list.length]; R.at=0; R.beat=-1; R.mgBeat=-1; R.charge=0; R.ramLocked=false;",'ram lock reset');
one(
"  } else if(R.attack==='ram'){\n    const W=(typeof worldWidth==='function')?worldWidth():VW;\n    if(t<1){ R.charge=t; R.tgt={x:b.x,y:b.y}; R.ramX=clamp(player.x, b.w*0.5, W-b.w*0.5);\n      if(R.pairSide){const L=camLeftX(),right=camRightX(),half=(L+right)*.5,gap=b.w*.5+9;R.ramX=clamp(R.ramX,R.pairSide<0?L+b.w*.5:half+gap,R.pairSide<0?half-gap:right-b.w*.5);}\n      if(R.beat<0){ R.beat=0; stageRevisionCue(b,'razorbackRam',.12); } }   // the rush winds up audibly\n    else if(t<2.5) R.tgt={x:R.ramX, y:VH*0.68};",
"  } else if(R.attack==='ram'){\n    const W=(typeof worldWidth==='function')?worldWidth():VW;combatWarningTick(b,'razorback-body-ram',Math.min(t,1),1.0);\n    if(t<1){ R.charge=t; R.tgt={x:b.x,y:b.y};\n      if(t<L23_FOV_YEL){R.ramX=clamp(player.x,b.w*0.5,W-b.w*0.5);\n        if(R.pairSide){const L=camLeftX(),right=camRightX(),half=(L+right)*.5,gap=b.w*.5+9;R.ramX=clamp(R.ramX,R.pairSide<0?L+b.w*.5:half+gap,R.pairSide<0?half-gap:right-b.w*.5);}}\n      else R.ramLocked=true;\n      if(R.beat<0){ R.beat=0; stageRevisionCue(b,'razorbackRam',.12); } }   // the rush winds up audibly\n    else if(t<2.5) R.tgt={x:R.ramX, y:VH*0.68};",
'shared ram state');
one(
"    if(R.attack==='ram'){ ctx.save(); ctx.strokeStyle='rgba(255,200,36,0.45)'; ctx.lineWidth=36*S;\n      ctx.beginPath(); ctx.moveTo(b.x,b.y); ctx.lineTo(R.ramX,VH*0.85); ctx.stroke(); ctx.restore(); }",
"    if(R.attack==='ram') combatWarningDraw(b,{x:b.x,y:b.y,ex:R.ramX,ey:VH*0.85,progress:R.charge,width:80*mul});",
'shared ram draw');
fs.writeFileSync(p,s,'utf8');console.log('PATCHED_RAZORBACK_SHARED_RAM_WARNING_0915');
