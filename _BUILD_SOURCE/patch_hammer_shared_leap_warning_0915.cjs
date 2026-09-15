const fs=require('fs'),path=require('path'),p=path.resolve(__dirname,'..','assets','game.js');let s=fs.readFileSync(p,'utf8');if(s.includes('\r'))throw new Error('game.js must remain LF-only');
function one(a,b,label){const n=s.split(a).length-1;if(n!==1)throw new Error(label+' expected once, found '+n);s=s.replace(a,b);}
one(
"  }else if(h.state==='warn'){\n    /* Commit immediately: the warning never chases the player after appearing. */\n    if(h.t>=1.2){hammerState(b,'leap');Audio.SFX.enemyShoot();}",
"  }else if(h.state==='warn'){\n    /* Commit immediately: the warning never chases the player after appearing. */\n    const warn=1.2;combatWarningTick(b,'chrome-hammer-leap',Math.min(h.t,warn),warn);\n    if(h.t>=warn){hammerState(b,'leap');Audio.SFX.enemyShoot();}",
'shared leap warning state');
one(
"  if(s==='warn'){\n    const ri=hammerFrame('reticle',0,h.t<.4?null:h.t<.8?'yellow':'red');",
"  if(s==='warn'){\n    const k=clamp(h.t/1.2,0,1);\n    combatWarningDraw(b,{x:b.x,y:b.y,ex:h.tx,ey:h.ty,progress:k,width:96});\n    const ri=hammerFrame('reticle',0,h.t<.4?null:h.t<.8?'yellow':'red');",
'shared leap warning draw');
fs.writeFileSync(p,s,'utf8');console.log('PATCHED_HAMMER_SHARED_LEAP_WARNING_0915');
